"""Example-level evaluation and evaluation grids.

Every evaluated example yields one row with the model's prediction and the
example's controlled variables, so any aggregate (by length, position,
distance, distractor count, hop depth, ...) is computed from the same
example-level table, and never from a single headline number.

Evaluation grids
----------------
A grid is a base TaskConfig plus a Cartesian product of overrides, e.g.

    {"name": "length_x_pos", "vary": {"seq_len": [32, 64, 128],
                                      "evidence_pos": [0.0, 0.5, 1.0]}, "n": 300}

All cells of a grid draw their *content* (keys, values, distractor counts)
from the same deterministic stream ``eval/<grid>`` seeded by ``eval_seed``;
placement uses a per-example sub-stream. So (i) cells are paired -- example i
differs between cells only in the varied factor and its layout -- and (ii) the
eval seed is the same for every run of a study, so all models are scored on
*identical* examples (paired method comparisons). Evaluation seeds are
disjoint by construction from training streams (different stream names), and
the overlap is also measured empirically (``leakage_check``).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

from ..data import Example, TaskConfig, TaskSampler, collate, overlap_count
from ..positional import PositionOverflowError


@dataclass
class GridSpec:
    name: str
    vary: dict
    base: dict | None = None
    n: int = 300

    @classmethod
    def from_dict(cls, d: dict) -> "GridSpec":
        return cls(name=d["name"], vary=d.get("vary", {}), base=d.get("base"), n=int(d.get("n", 300)))

    def cells(self):
        keys = list(self.vary)
        for combo in itertools.product(*(self.vary[k] for k in keys)):
            yield dict(zip(keys, combo))


def cell_name(cell: dict) -> str:
    return ",".join(f"{k}={v}" for k, v in cell.items()) or "default"


def build_cell_config(train_task: TaskConfig, grid: GridSpec, cell: dict) -> TaskConfig:
    over = dict(grid.base or {})
    over.update(cell)
    if "seq_len" in over and "length_choices" not in over:
        over["length_choices"] = None
    return train_task.replace(**over)


def grid_examples(train_task: TaskConfig, grid: GridSpec, eval_seed: int) -> list[tuple[dict, list[Example]]]:
    out = []
    for cell in grid.cells():
        cfg = build_cell_config(train_task, grid, cell)
        # one content stream per grid: cells are *paired* (example i has the same keys, values and
        # distractor draws in every cell; only the varied factor and placement change)
        sampler = TaskSampler(cfg, seed=eval_seed, stream=f"eval/{grid.name}")
        out.append((cell, [sampler.example() for _ in range(grid.n)]))
    return out


@torch.no_grad()
def predict(model, examples: list[Example], batch_size: int = 128, pos_offset: int = 0,
            hooks: dict | None = None) -> pd.DataFrame:
    """Score examples; returns one row per example (input order preserved)."""
    model.eval()
    rows: list = [None] * len(examples)
    by_len: dict = {}
    for i, e in enumerate(examples):
        by_len.setdefault(len(e.tokens), []).append(i)
    for idxs in by_len.values():
        for s in range(0, len(idxs), batch_size):
            chunk = idxs[s:s + batch_size]
            b = collate([examples[i] for i in chunk])
            try:
                logits = model(b["tokens"], pos_offset=pos_offset, hooks=hooks)
            except PositionOverflowError as err:
                for i in chunk:
                    rows[i] = {"status": "position_overflow", "error": str(err), "correct": np.nan,
                               "pred": -1, "loss": np.nan, "p_answer": np.nan, "p_pred": np.nan,
                               "answer_rank": np.nan, "entropy": np.nan, "margin": np.nan}
                continue
            lg = logits[torch.arange(len(chunk)), b["ans_pos"]].float()
            logp = F.log_softmax(lg, -1)
            ans = b["answers"]
            pred = lg.argmax(-1)
            lp_ans = logp[torch.arange(len(chunk)), ans]
            rank = (lg > lg[torch.arange(len(chunk)), ans][:, None]).sum(-1)
            masked = lg.clone()
            masked[torch.arange(len(chunk)), ans] = float("-inf")
            margin = lg[torch.arange(len(chunk)), ans] - masked.max(-1).values
            ent = -(logp.exp() * logp).sum(-1)
            for j, i in enumerate(chunk):
                rows[i] = {"status": "ok", "error": "", "correct": float(pred[j] == ans[j]),
                           "pred": int(pred[j]), "loss": float(-lp_ans[j]), "p_answer": float(lp_ans[j].exp()),
                           "p_pred": float(logp[j, pred[j]].exp()), "answer_rank": int(rank[j]),
                           "entropy": float(ent[j]), "margin": float(margin[j])}
    df = pd.DataFrame(rows)
    meta = pd.DataFrame([e.public_meta() for e in examples])
    return pd.concat([meta.reset_index(drop=True), df], axis=1)


def evaluate_grid(model, train_task: TaskConfig, grid: GridSpec, eval_seed: int,
                  train_len_range: tuple[int, int] | None = None, cached=None) -> pd.DataFrame:
    parts = []
    for cell, exs in (cached or grid_examples(train_task, grid, eval_seed)):
        df = predict(model, exs)
        df.insert(0, "grid", grid.name)
        df.insert(1, "cell", cell_name(cell))
        for k, v in cell.items():
            df[f"cell_{k}"] = v if not isinstance(v, (list, tuple)) else str(v)
        parts.append(df)
    out = pd.concat(parts, ignore_index=True)
    if train_len_range is not None:
        lo, hi = train_len_range
        out["length_regime"] = np.where(out["seq_len"] > hi, "extrapolation",
                                        np.where(out["seq_len"] < lo, "shorter", "in_range"))
    return out


def leakage_check(train_task: TaskConfig, train_seed: int, eval_sets: list[list[Example]],
                  n_train: int = 20000) -> dict:
    """Generate ``n_train`` examples from the actual training stream and count
    exact duplicates in the evaluation sets."""
    s = TaskSampler(train_task, seed=train_seed, stream="train")
    train = [s.example() for _ in range(n_train)]
    all_eval = [e for es in eval_sets for e in es]
    return {"n_train_sampled": n_train, "n_eval": len(all_eval),
            "n_eval_in_train_sample": overlap_count(train, all_eval)}


def training_length_range(task: TaskConfig) -> tuple[int, int]:
    if task.length_choices:
        return (min(task.length_choices), max(task.length_choices))
    if isinstance(task.seq_len, int):
        return (task.seq_len, task.seq_len)
    return (int(task.seq_len[0]), int(task.seq_len[1]))
