"""Training loop.

* Data are generated on the fly from a seeded stream (``stream="train"``);
  the in-distribution validation set uses an independent stream ("val").
* Each batch shares one sequence length drawn from the training length
  distribution, so no padding is ever needed during training.
* Loss: cross-entropy of the answer token at the final <ans> position
  (``loss_on="answer"``). ``loss_on="all"`` adds the ordinary next-token loss
  over every position (mostly unpredictable noise for these tasks).
* AdamW, linear warm-up then cosine decay to ``min_lr_frac * lr``. Weight decay
  is applied only to Linear weight matrices -- *not* to embeddings, positional
  tables or LayerNorm -- so unused rows of a learned position table keep their
  initial values exactly (relevant for length extrapolation).
* A fixed number of optimisation steps for every method (matched budgets).
  Early stopping is available but off by default.
"""

from __future__ import annotations

import math
import time
from dataclasses import asdict, dataclass, field

import numpy as np
import torch
import torch.nn.functional as F

from ..data import TaskConfig, TaskSampler, collate, make_dataset
from ..models import ModelConfig, Transformer


class TrainingDiverged(RuntimeError):
    pass


@dataclass
class TrainConfig:
    steps: int = 3000
    batch_size: int = 64
    lr: float = 1e-3
    min_lr_frac: float = 0.1
    warmup_steps: int = 200
    weight_decay: float = 0.01
    beta1: float = 0.9
    beta2: float = 0.98
    grad_clip: float = 1.0
    eval_every: int = 250
    log_every: int = 50
    val_examples: int = 512
    seed: int = 0
    threads: int = 2
    loss_on: str = "answer"            # answer | all
    early_stop_acc: float | None = None
    checkpoint_steps: list = field(default_factory=list)   # extra checkpoints for learning-dynamics analysis

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "TrainConfig":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed % (2**32))


def lr_at(step: int, cfg: TrainConfig) -> float:
    if step < cfg.warmup_steps:
        return cfg.lr * (step + 1) / cfg.warmup_steps
    prog = (step - cfg.warmup_steps) / max(1, cfg.steps - cfg.warmup_steps)
    return cfg.lr * (cfg.min_lr_frac + (1 - cfg.min_lr_frac) * 0.5 * (1 + math.cos(math.pi * min(1.0, prog))))


def param_groups(model: Transformer, weight_decay: float):
    decay, no_decay = [], []
    for name, p in model.named_parameters():
        if not p.requires_grad:
            continue
        is_matrix = p.dim() == 2 and not name.startswith(("tok_emb", "pos.")) and "emb" not in name
        (decay if is_matrix else no_decay).append(p)
    return [{"params": decay, "weight_decay": weight_decay}, {"params": no_decay, "weight_decay": 0.0}]


def answer_logits(model: Transformer, batch: dict, **fw) -> torch.Tensor:
    logits = model(batch["tokens"], **fw)
    return logits[torch.arange(logits.size(0)), batch["ans_pos"]]


@torch.no_grad()
def quick_eval(model: Transformer, examples, batch_size: int = 256) -> dict:
    model.eval()
    by_len: dict = {}
    for e in examples:
        by_len.setdefault(len(e.tokens), []).append(e)
    n, correct, loss = 0, 0, 0.0
    for group in by_len.values():
        for i in range(0, len(group), batch_size):
            b = collate(group[i:i + batch_size])
            lg = answer_logits(model, b)
            loss += F.cross_entropy(lg, b["answers"], reduction="sum").item()
            correct += (lg.argmax(-1) == b["answers"]).sum().item()
            n += len(b["answers"])
    model.train()
    return {"val_loss": loss / n, "val_acc": correct / n}


def train_model(model_cfg: ModelConfig, task_cfg: TaskConfig, train_cfg: TrainConfig,
                log_fn=None, model: Transformer | None = None,
                checkpoint_fn=None) -> tuple[Transformer, list, dict]:
    """Train and return (model, history rows, summary). ``log_fn(row)`` is called per log step;
    ``checkpoint_fn(step, model)`` at every step listed in ``train_cfg.checkpoint_steps``."""
    torch.set_num_threads(max(1, train_cfg.threads))
    set_seed(train_cfg.seed)
    model = model or Transformer(model_cfg)
    model.train()
    opt = torch.optim.AdamW(param_groups(model, train_cfg.weight_decay), lr=train_cfg.lr,
                            betas=(train_cfg.beta1, train_cfg.beta2))
    sampler = TaskSampler(task_cfg, seed=train_cfg.seed, stream="train")
    val_set = make_dataset(task_cfg, train_cfg.val_examples, seed=train_cfg.seed, stream="val")

    history, t0 = [], time.time()
    win_loss, win_acc, win_n, win_gn, max_len_seen = 0.0, 0, 0, 0.0, 0
    steps_to = {0.5: None, 0.9: None, 0.99: None}
    last_val = {"val_loss": float("nan"), "val_acc": float("nan")}
    stopped_early = False
    for step in range(train_cfg.steps):
        for g in opt.param_groups:
            g["lr"] = lr_at(step, train_cfg)
        batch = sampler.batch(train_cfg.batch_size)
        max_len_seen = max(max_len_seen, batch["tokens"].shape[1])
        if train_cfg.loss_on == "all":
            logits = model(batch["tokens"])
            lg = logits[torch.arange(logits.size(0)), batch["ans_pos"]]
            loss = F.cross_entropy(lg, batch["answers"]) + F.cross_entropy(
                logits[:, :-1].reshape(-1, logits.size(-1)), batch["tokens"][:, 1:].reshape(-1))
        elif "aux_pos" in batch:  # final query + auxiliary training queries, equally weighted
            logits = model(batch["tokens"])
            lg = logits[torch.arange(logits.size(0)), batch["ans_pos"]]
            lg_aux = logits[batch["aux_rows"], batch["aux_pos"]]
            loss = F.cross_entropy(torch.cat([lg, lg_aux]), torch.cat([batch["answers"], batch["aux_answers"]]))
        else:
            lg = answer_logits(model, batch)
            loss = F.cross_entropy(lg, batch["answers"])
        if not torch.isfinite(loss):
            raise TrainingDiverged(f"non-finite loss at step {step}")
        opt.zero_grad(set_to_none=True)
        loss.backward()
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), train_cfg.grad_clip)
        opt.step()
        if checkpoint_fn is not None and (step + 1) in set(train_cfg.checkpoint_steps):
            model.eval()
            checkpoint_fn(step + 1, model)
            model.train()

        win_loss += loss.item() * len(lg)
        win_acc += (lg.argmax(-1) == batch["answers"]).sum().item()
        win_n += len(lg)
        win_gn += float(gn)
        is_eval = (step + 1) % train_cfg.eval_every == 0 or step + 1 == train_cfg.steps
        if (step + 1) % train_cfg.log_every == 0 or is_eval:
            row = {"step": step + 1, "train_loss": win_loss / win_n, "train_acc": win_acc / win_n,
                   "grad_norm": win_gn / max(1, train_cfg.log_every), "lr": lr_at(step, train_cfg),
                   "elapsed_s": time.time() - t0}
            if is_eval:
                last_val = quick_eval(model, val_set)
                for thr in steps_to:
                    if steps_to[thr] is None and last_val["val_acc"] >= thr:
                        steps_to[thr] = step + 1
            row.update(last_val if is_eval else {"val_loss": float("nan"), "val_acc": float("nan")})
            history.append(row)
            if log_fn:
                log_fn(row)
            win_loss, win_acc, win_n, win_gn = 0.0, 0, 0, 0.0
            if is_eval and train_cfg.early_stop_acc and last_val["val_acc"] >= train_cfg.early_stop_acc:
                stopped_early = True
                break
    model.eval()
    summary = {
        "steps_completed": history[-1]["step"] if history else 0, "stopped_early": stopped_early,
        "final_train_loss": history[-1]["train_loss"] if history else float("nan"),
        "final_val_loss": last_val["val_loss"], "final_val_acc": last_val["val_acc"],
        "steps_to_val_acc_0.5": steps_to[0.5], "steps_to_val_acc_0.9": steps_to[0.9],
        "steps_to_val_acc_0.99": steps_to[0.99],
        "train_time_s": time.time() - t0, "max_train_len_seen": max_len_seen,
        "n_params": model.n_params(), "n_params_positional": model.n_params() - model.n_params(True),
    }
    return model, history, summary
