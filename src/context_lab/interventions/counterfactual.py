"""Counterfactual input edits: does the model follow the *content* of the evidence?

Each edit changes the input in a controlled way and states what a model that
genuinely retrieves "the value bound to the queried key" must do:

| edit                | what changes                                   | genuine retrieval must            |
|---------------------|------------------------------------------------|-----------------------------------|
| ``value_edit``      | evidence value v -> v' (v' not in context)      | **follow**: predict v'             |
| ``key_swap``        | keys of the evidence pair and one distractor   | **follow**: predict the distractor |
|                     | pair are exchanged (values stay in place)      | pair's value                      |
| ``distractor_edit`` | one distractor value -> unused value           | **stay**: prediction unchanged     |
| ``filler_resample`` | every filler token resampled                   | **stay**: prediction unchanged     |
| ``evidence_move``   | evidence unit moved to a random other offset   | **stay**: prediction unchanged     |

Reference rates for a *value-type shortcut* (predict some in-context value
without binding it to its key, uniformly at random): follow ~ 1/n_pairs for
``value_edit`` and ``key_swap``; the "stay" edits are not informative for it.
A model that copies the most recent value is fooled by ``evidence_move``.

These edits test input-output behaviour on the evaluated distribution. They
provide evidence *about* the learned behaviour; they do not prove that a
general retrieval algorithm was learned (e.g. behaviour could differ off
distribution, or the model could combine partial strategies).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..data import Example, make_rng, move_evidence
from ..data.tasks import _rebuild
from ..data.vocab import DEFAULT_VOCAB
from ..evaluation import predict

EDITS = ("value_edit", "key_swap", "distractor_edit", "filler_resample", "evidence_move")
EXPECT = {"value_edit": "follow", "key_swap": "follow", "distractor_edit": "stay", "filler_resample": "stay",
          "evidence_move": "stay"}


def _unused_value(ex: Example, rng, vocab) -> int | None:
    """A value token of the vocabulary the run actually uses that does not occur anywhere in the input
    (None if every such token is already used -- possible with a shared vocabulary and many pairs)."""
    pool = vocab.keys() if ex.meta.get("value_vocab") == "shared" else vocab.values()
    present = set(ex.tokens)
    cands = [v for v in pool if v not in present]
    return int(rng.choice(cands)) if cands else None


def apply_edit(ex: Example, edit: str, rng, vocab=DEFAULT_VOCAB) -> tuple[Example, int] | None:
    """Return (edited example, target a genuine retriever should output) or None if
    the edit is not applicable to this example."""
    units = list(ex.meta["_units"])
    if edit == "value_edit":
        v2 = _unused_value(ex, rng, vocab)
        if v2 is None:
            return None
        new = [(k, o, t[:-1] + [v2]) if k == "evidence" else (k, o, t) for k, o, t in units]
        return _rebuild(ex, new, answer=v2), v2
    if edit == "key_swap":
        pairs = [i for i, u in enumerate(units) if u[0] == "pair"]
        ev = next(i for i, u in enumerate(units) if u[0] == "evidence")
        tkey = units[ev][2][:-1]
        cands = [i for i in pairs if units[i][2][:-1] != tkey and units[i][2][-1] != units[ev][2][-1]
                 and sum(1 for j in pairs if units[j][2][:-1] == units[i][2][:-1]) == 1]
        if not cands:
            return None
        i = cands[int(rng.integers(len(cands)))]
        k_ev, o_ev, t_ev = units[ev]
        k_p, o_p, t_p = units[i]
        new = list(units)
        new[ev] = ("pair", o_ev, t_p[:-1] + [t_ev[-1]])            # distractor key now bound to old answer
        new[i] = ("evidence", o_p, t_ev[:-1] + [t_p[-1]])          # query key now bound to distractor value
        out = _rebuild(ex, new, answer=t_p[-1])
        k = ex.meta["key_len"]
        out.meta.update(evidence_offset=o_p, evidence_key_pos=1 + o_p, evidence_value_pos=1 + o_p + k,
                        distance=out.ans_pos - (1 + o_p + k))
        return out, t_p[-1]
    if edit == "distractor_edit":
        pairs = [i for i, u in enumerate(units) if u[0] == "pair"]
        if not pairs:
            return None
        i = pairs[int(rng.integers(len(pairs)))]
        v2 = _unused_value(ex, rng, vocab)
        if v2 is None:
            return None
        new = list(units)
        k, o, t = new[i]
        new[i] = (k, o, t[:-1] + [v2])
        return _rebuild(ex, new), ex.answer
    if edit == "filler_resample":
        new = [(k, o, [int(rng.integers(vocab.filler_start, vocab.key_start))]) if k == "filler" else (k, o, t)
               for k, o, t in units]
        return _rebuild(ex, new), ex.answer
    if edit == "evidence_move":
        C, k = ex.meta["context_len"], ex.meta["key_len"]
        target = int(rng.integers(0, max(1, C - k)))
        return move_evidence(ex, target), ex.answer
    raise ValueError(edit)


def counterfactual_battery(model, examples: list[Example], seed: int = 0, vocab=DEFAULT_VOCAB) -> pd.DataFrame:
    """One row per (example, edit): original prediction, edited prediction and
    whether the model behaved as a genuine retriever would."""
    rng = make_rng(seed, "counterfactual")
    base = predict(model, examples)
    rows = []
    for edit in EDITS:
        pairs = [(i, apply_edit(ex, edit, rng, vocab)) for i, ex in enumerate(examples)]
        pairs = [(i, r) for i, r in pairs if r is not None]
        if not pairs:
            continue
        edited = predict(model, [r[0] for _, r in pairs])
        for j, (i, (ex2, tgt)) in enumerate(pairs):
            p0, p1 = int(base["pred"].iloc[i]), int(edited["pred"].iloc[j])
            ok = (p1 == tgt) if EXPECT[edit] == "follow" else (p1 == p0)
            rows.append({"edit": edit, "expect": EXPECT[edit], "example": i, "orig_pred": p0,
                         "orig_correct": float(base["correct"].iloc[i]), "edited_pred": p1, "target": tgt,
                         "behaves_as_retriever": float(ok), "edited_correct": float(p1 == tgt),
                         "n_pairs": examples[i].meta["n_pairs"], "seq_len": examples[i].meta["seq_len"]})
    return pd.DataFrame(rows)


def battery_summary(df: pd.DataFrame) -> dict:
    """Rate per edit, split by whether the original prediction was correct, plus
    the value-shortcut reference rate (mean 1/n_pairs) for the follow edits."""
    out = {}
    if df.empty:
        return out
    for edit, g in df.groupby("edit"):
        out[f"cf_{edit}_rate"] = float(g["behaves_as_retriever"].mean())
        c = g[g["orig_correct"] == 1]
        out[f"cf_{edit}_rate_given_orig_correct"] = float(c["behaves_as_retriever"].mean()) if len(c) else None
        out[f"cf_{edit}_n"] = int(len(g))
        if EXPECT[edit] == "follow":
            out[f"cf_{edit}_shortcut_reference"] = float(np.mean(1.0 / g["n_pairs"]))
    return out
