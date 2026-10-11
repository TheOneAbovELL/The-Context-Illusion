"""Causal interventions.

1. Attention knockout -- at layer l, forbid the <ans> position from attending
   to a chosen set of positions (their pre-softmax scores are set to -inf, so
   the remaining attention renormalises). Compare knocking out the *evidence*
   positions with knocking out an equally sized set of *control* positions
   (a randomly chosen distractor pair). The difference is the causal effect
   attributable to the direct <ans> -> evidence read in that layer. Note that
   information can still reach <ans> indirectly through other positions; the
   knockout measures only the direct path.

2. Activation patching (clean -> corrupted) -- two inputs that differ in one
   controlled token:
     * ``value``  corruption: the evidence VALUE is replaced by another value
       (the correct answer changes from v to v'),
     * ``query``  corruption: the queried key is replaced by a distractor key.
   For each layer l and position p we run the corrupted input but overwrite
   the residual stream ``L{l}.resid_pre[p]`` with its value from the clean
   run, then measure the normalised logit-difference restoration

       R = (LD_patched - LD_corrupt) / (LD_clean - LD_corrupt),
       LD = logit(clean answer) - logit(corrupt answer).

   R ~ 1 means the patched activation alone carries the information needed to
   produce the clean answer; R ~ 0 means it is irrelevant (for this pair).
   Positions are aggregated by role across examples. Positions whose clean and
   corrupt activations are identical (before the edit, by causality) give R = 0
   by construction -- a built-in negative control.

3. Head ablation -- zero a head's output (``attn.z``) at every position.
"""

from __future__ import annotations

import pandas as pd
import torch

from ..data import Example, collate, corrupt_query, make_rng
from ..data.tasks import _rebuild
from ..data.vocab import DEFAULT_VOCAB
from ..diagnostics.inspect import position_roles
from ..evaluation import predict


# ----------------------------------------------------------------------------- knockout
def _knockout_hook(ans_pos: torch.Tensor, blocked: list[list[int]], heads=None):
    def fn(scores):  # (B, H, T, T)
        s = scores.clone()
        for b, positions in enumerate(blocked):
            if positions:
                hs = slice(None) if heads is None else heads
                s[b, hs, ans_pos[b], positions] = float("-inf")
        return s
    return fn


CHUNK = 128


def _chunks(examples: list[Example]):
    """Index lists of at most CHUNK examples that share one length. The knockout hook is built for
    exactly the examples of one forward pass (BUG FIX: hooks built per length group used to be applied
    to predict()'s own sub-batches of 128, mis-indexing every example after the 128th)."""
    by_len: dict = {}
    for i, e in enumerate(examples):
        by_len.setdefault(len(e.tokens), []).append(i)
    for idxs in by_len.values():
        for s in range(0, len(idxs), CHUNK):
            yield idxs[s:s + CHUNK]


@torch.no_grad()
def knockout_predict(model, examples: list[Example], layer: int, positions_fn, heads=None) -> pd.DataFrame:
    """Predict with <ans> -> positions_fn(ex) attention blocked at ``layer``."""
    return _multi_layer_knockout(model, examples, [layer], positions_fn, heads)


def evidence_positions(ex: Example) -> list[int]:
    return [i for i, r in enumerate(position_roles(ex)) if r in ("evidence_key", "evidence_value")]


def control_positions_factory(seed: int = 0):
    """Return a function giving the positions of one random distractor pair
    (same size and kind as the evidence unit). Falls back to random fillers."""
    rng = make_rng(seed, "knockout_control")

    def fn(ex: Example) -> list[int]:
        roles = position_roles(ex)
        pairs = [(1 + o, len(t)) for k, o, t in ex.meta["_units"] if k == "pair"]
        if pairs:
            s, n = pairs[int(rng.integers(len(pairs)))]
            return list(range(s, s + n))
        # no distractor pairs (e.g. induction): random non-evidence context positions of the same count
        fill = [i for i, r in enumerate(roles) if r in ("filler", "first_half")]
        n = len(evidence_positions(ex))
        return [int(x) for x in rng.choice(fill, size=min(n, len(fill)), replace=False)] if fill else []
    return fn


def knockout_study(model, examples: list[Example], seed: int = 0) -> pd.DataFrame:
    """Accuracy / P(answer) under: no intervention, evidence knockout and
    control knockout, for each layer separately and for all layers at once."""
    base = predict(model, examples)
    ctrl = control_positions_factory(seed)
    ctrl_cache = {id(e): ctrl(e) for e in examples}       # same control positions in every layer
    rows = [{"condition": "none", "layer": "-", "acc": base["correct"].mean(), "p_answer": base["p_answer"].mean(),
             "n": len(base)}]
    L = model.cfg.n_layers
    for layer in list(range(L)) + ["all"]:
        layers = range(L) if layer == "all" else [layer]
        for cond, fn in (("evidence", evidence_positions), ("control_pair", lambda e: ctrl_cache[id(e)])):
            if layer == "all":
                df = _multi_layer_knockout(model, examples, layers, fn)
            else:
                df = knockout_predict(model, examples, layer, fn)
            rows.append({"condition": cond, "layer": str(layer), "acc": df["correct"].mean(),
                         "p_answer": df["p_answer"].mean(), "n": len(df)})
    return pd.DataFrame(rows)


@torch.no_grad()
def _multi_layer_knockout(model, examples, layers, positions_fn, heads=None) -> pd.DataFrame:
    out = [None] * len(examples)
    for idxs in _chunks(examples):
        exs = [examples[i] for i in idxs]
        blocked = [positions_fn(e) for e in exs]
        b = collate(exs)
        hooks = {f"L{l}.attn.scores": _knockout_hook(b["ans_pos"], blocked, heads) for l in layers}
        df = predict(model, exs, hooks=hooks, batch_size=len(exs))
        for j, i in enumerate(idxs):
            out[i] = df.iloc[j]
    return pd.DataFrame(out).reset_index(drop=True)


# ----------------------------------------------------------------------------- activation patching
def corrupt_value(ex: Example, rng, vocab=DEFAULT_VOCAB) -> Example:
    """Replace the evidence VALUE with a different value token (new answer)."""
    vals = [v for v in vocab.values() if v != ex.answer]
    new_v = int(rng.choice(vals))
    units = [(k, o, (t[:-1] + [new_v]) if k == "evidence" else t) for k, o, t in ex.meta["_units"]]
    new = _rebuild(ex, units, answer=new_v)
    new.meta["corrupted_from"] = ex.answer
    return new


@torch.no_grad()
def patching_study(model, examples: list[Example], kind: str = "value", seed: int = 0,
                   max_examples: int = 64) -> pd.DataFrame:
    """Residual-stream patching over (layer, position), aggregated by role.

    Returns one row per (example, layer, position) with the restoration score R.
    ``layer = n_layers`` denotes the final residual (after the last block).
    """
    rng = make_rng(seed, f"patching/{kind}")
    rows = []
    L = model.cfg.n_layers
    names = [f"L{l}.resid_pre" for l in range(L)] + [f"L{L - 1}.resid_post"]
    for ei, ex in enumerate(examples[:max_examples]):
        cor = corrupt_value(ex, rng) if kind == "value" else corrupt_query(ex, rng)
        if cor is None:
            continue
        clean_ans, cor_ans = ex.answer, cor.answer
        b = collate([ex, cor])
        logits, cache = model.run_with_cache(b["tokens"])
        ld_clean = float(logits[0, -1, clean_ans] - logits[0, -1, cor_ans])
        ld_cor = float(logits[1, -1, clean_ans] - logits[1, -1, cor_ans])
        denom = ld_clean - ld_cor
        if abs(denom) < 1e-3:
            continue
        roles = position_roles(ex)
        T = len(ex.tokens)
        cor_tokens = b["tokens"][1:2].repeat(T, 1)               # one row per patched position
        for li, name in enumerate(names):
            clean_act = cache[name][0]                            # (T, D)

            def hook(t, clean_act=clean_act):
                t = t.clone()
                idx = torch.arange(T)
                t[idx, idx] = clean_act[idx]                      # row p patches position p
                return t
            lg = model(cor_tokens, hooks={name: hook})[:, -1]
            ld = (lg[:, clean_ans] - lg[:, cor_ans]).numpy()
            for p in range(T):
                rows.append({"example": ei, "layer": li, "position": p, "role": roles[p],
                             "rel_pos": p - T, "restoration": (ld[p] - ld_cor) / denom,
                             "clean_correct": float(logits[0, -1].argmax() == clean_ans),
                             "seq_len": T, "distance": ex.meta["distance"]})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- head ablation
@torch.no_grad()
def head_ablation_study(model, examples: list[Example]) -> pd.DataFrame:
    base = predict(model, examples)
    rows = [{"layer": "-", "head": "-", "acc": base["correct"].mean(), "p_answer": base["p_answer"].mean()}]
    for l in range(model.cfg.n_layers):
        for h in range(model.cfg.n_heads):
            def hook(z, h=h):
                z = z.clone()
                z[:, h] = 0.0
                return z
            df = predict(model, examples, hooks={f"L{l}.attn.z": hook})
            rows.append({"layer": l, "head": h, "acc": df["correct"].mean(), "p_answer": df["p_answer"].mean()})
    out = pd.DataFrame(rows)
    out["acc_drop"] = out["acc"].iloc[0] - out["acc"]
    return out


def summarize_patching(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    return (df.groupby(["layer", "role"])["restoration"]
            .agg(["mean", "std", "count"]).reset_index().sort_values(["layer", "mean"], ascending=[True, False]))

