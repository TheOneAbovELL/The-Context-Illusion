"""Simple algorithmic baselines. They give reference points that separate
"the task is hard" from "the model is failing":

* ``oracle``           exact parser (upper bound; 100% iff the data is well formed)
* ``naive_induction``  find the LAST occurrence of the query key in the context and
                       copy the token that follows it (multi-hop: copy the entity
                       after ``key ->``). Fooled by lures; does only one hop.
* ``last_value``       the most recent value/entity token in the context (recency bias)
* ``random_context``   expected accuracy of guessing uniformly among the value
                       tokens present in the context (computed exactly)
* ``chance``           1 / |answer vocabulary|
* ``elimination``      expected accuracy of choosing uniformly among the context values that
                       were NOT displayed as auxiliary answers (equals ``random_context`` when no
                       answers are displayed; high values reveal the elimination shortcut)
* ``best_fixed_offset`` accuracy of "copy the token exactly d positions before the
                       prediction", with d chosen to *maximise* accuracy on the very
                       examples being scored (an optimistic upper bound for any purely
                       positional rule; high values reveal a positional shortcut)
"""

from __future__ import annotations

import numpy as np

from .tasks import Example
from .validate import oracle
from .vocab import ARROW, DEFAULT_VOCAB, Vocab


def _answer_kind(ex: Example) -> str:
    return "value" if ex.meta["task"] == "recall" else "entity"


def _induction_baselines(examples: list[Example]) -> dict:
    """Induction control: random guess among the first-half tokens that have a successor."""
    return {"oracle": float(np.mean([oracle(e) == e.answer for e in examples])),
            "random_context": float(np.mean([1.0 / (e.meta["half_len"] - 1) for e in examples])),
            "chance": 1.0 / 48}


def _context(ex: Example) -> list[int]:
    tail = len(ex.meta["_query"]) + len(ex.meta.get("_aux_region", []))
    return ex.tokens[1:-tail]


def _context_values(ex: Example) -> list[int]:
    """Value tokens of the context associations, read from the unit structure (works for shared
    vocabularies, where a value is not identifiable by token type)."""
    if ex.meta["task"] == "recall" and ex.meta.get("_units") is not None:
        return [t[-1] for k, _, t in ex.meta["_units"] if k in ("pair", "evidence")]
    kind = _answer_kind(ex)
    return [t for t in _context(ex) if DEFAULT_VOCAB.kind(t) == kind]


def _query_key(ex: Example) -> list[int]:
    q = ex.meta["_query"]
    return list(q[1:1 + (ex.meta["key_len"] if ex.meta["task"] == "recall" else 1)])


def naive_induction(ex: Example, vocab: Vocab = DEFAULT_VOCAB) -> int:
    ctx = _context(ex)
    if ex.meta["task"] == "recall":
        k = ex.meta["key_len"]
        qk = _query_key(ex)
        for i in range(len(ctx) - k - 1, -1, -1):
            if ctx[i:i + k] == qk:
                return ctx[i + k]
        return -1
    e = _query_key(ex)[0]
    for i in range(len(ctx) - 3, -1, -1):
        if ctx[i] == e and ctx[i + 1] == ARROW:
            return ctx[i + 2]
    return -1


def last_value(ex: Example, vocab: Vocab = DEFAULT_VOCAB) -> int:
    vals = _context_values(ex)
    return vals[-1] if vals else -1


def random_context_expected(ex: Example, vocab: Vocab = DEFAULT_VOCAB) -> float:
    vals = _context_values(ex)
    return vals.count(ex.answer) / len(vals) if vals else 0.0


def elimination_expected(ex: Example, vocab: Vocab = DEFAULT_VOCAB) -> float:
    """Pick uniformly among the context value tokens whose value was not displayed as an auxiliary
    answer (token-level, like ``random_context``, so the two coincide when nothing is displayed)."""
    shown = {a for _, a in ex.meta.get("_aux", [])} if ex.meta.get("aux_show_answers", True) else set()
    cand = [t for t in _context_values(ex) if t not in shown]
    return cand.count(ex.answer) / len(cand) if cand else 0.0


def chance(ex: Example, vocab: Vocab = DEFAULT_VOCAB) -> float:
    return 1.0 / (vocab.n_values if _answer_kind(ex) == "value" else vocab.n_entities)


def best_fixed_offset(examples: list[Example], max_offset: int | None = None) -> tuple[float, int]:
    """(accuracy, d) of the best rule "predict tokens[ans_pos - d]" over d >= 1."""
    max_offset = max_offset or max(len(e.tokens) for e in examples)
    best = (0.0, 0)
    for d in range(1, max_offset):
        hits = [e.tokens[e.ans_pos - d] == e.answer for e in examples if e.ans_pos - d >= 0]
        acc = sum(hits) / len(examples)
        if acc > best[0]:
            best = (acc, d)
    return best


def baseline_accuracies(examples: list[Example], vocab: Vocab = DEFAULT_VOCAB) -> dict:
    if examples and examples[0].meta["task"] == "induction":
        out = _induction_baselines(examples)
        out["best_fixed_offset"], out["best_fixed_offset_d"] = best_fixed_offset(examples)
        return out
    out = {}
    for name, fn in (("oracle", oracle), ("naive_induction", naive_induction), ("last_value", last_value)):
        out[name] = float(np.mean([fn(e, vocab) == e.answer for e in examples]))
    out["random_context"] = float(np.mean([random_context_expected(e, vocab) for e in examples]))
    if examples[0].meta["task"] == "recall":
        out["elimination"] = float(np.mean([elimination_expected(e, vocab) for e in examples]))
    out["chance"] = float(np.mean([chance(e, vocab) for e in examples]))
    out["best_fixed_offset"], out["best_fixed_offset_d"] = best_fixed_offset(examples)
    return out
