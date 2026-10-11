"""Controlled synthetic retrieval tasks.

Every example has the shape

    <bos> [context of C tokens] <qry> KEY        -> target = VALUE   (query_format="key_last", default)
    <bos> [context of C tokens] <qry> KEY <ans>  -> target = VALUE   (query_format="ans_marker")

and the model is scored on its next-token prediction at the final position
(index T-1). With ``ans_marker`` the predicting position's previous token is
the query key, so a "match previous tokens" retrieval rule also matches the
predicting position itself; ``key_last`` (the standard associative-recall
format) has no such self-match. See docs/results.md (calibration). The context is assembled from *units*:

* ``pair``      KEY VALUE              (a distractor association)
* ``evidence``  KEY* VALUE*            (the association the query asks about)
* ``lure``      KEY* FILLER            (the query key in a non-key role: misleading,
                                        non-matching pattern -- never followed by a value)
* ``filler``    FILLER                 (single irrelevant token)
* ``link`` / ``target_link``  A -> B   (multi-hop task)

The layout engine (:func:`layout_context`) places the relevant unit(s) at
requested token offsets and distributes the remaining units uniformly in the
remaining gaps, so the *position* of the evidence, the *length* of the
sequence and the *number of distractors* can be set independently. When an
exact offset is impossible (e.g. a dense context with no fillers) the
evidence is snapped to the nearest feasible offset and the *actual* offset is
recorded in ``meta`` -- evaluation always bins on actual values.

Tasks
-----
``recall``    (Tasks A-D, F)  single-item associative recall with controllable
              length, evidence position or distance, distractor count, distractor
              key repetition, lures, and compound keys with near-miss distractors.
``multihop``  (Task E) chains A -> B -> C; ``<qry> A`` asks for the chain end,
              ``<nxt> A`` for the immediate successor (single hop).
"""

from __future__ import annotations

import copy
import zlib
from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np
import torch

from .vocab import ANS, ARROW, BOS, DEFAULT_VOCAB, NXT, PAD, QRY, Vocab

Range = Any  # int, or [lo, hi] inclusive


class LayoutError(ValueError):
    pass


@dataclass
class TaskConfig:
    task: str = "recall"                  # recall | multihop
    seq_len: Range = (32, 64)             # total length incl. <bos> and query block, inclusive range
    length_choices: list | None = None    # explicit set of lengths (overrides seq_len)
    # --- recall -----------------------------------------------------------------
    n_pairs: Range = (2, 8)               # associations in context (target + distractors)
    fill_pairs: bool = False              # use as many pairs as fit (dense context, no fillers)
    evidence_pos: float | None = None     # normalized evidence offset in [0, 1]
    evidence_distance: int | None = None  # tokens from evidence VALUE to the <ans> position
    n_lures: Range = 0                    # query-key occurrences in a non-key role
    lure_prob: float = 1.0                # probability that n_lures is drawn (else 0)
    repeat_distractor_keys: bool = False  # distractor keys may repeat among themselves
    key_len: int = 1                      # 1 = atomic keys; 2 = compound keys
    near_miss_frac: float = 0.0           # key_len>=2: share of distractors sharing the target's first sub-token
    query_format: str = "key_last"        # key_last: "<qry> K" -> V predicted at K;  ans_marker: "<qry> K <ans>" -> V
    n_queries: Any = 1                    # TRAINING densification: number of query blocks (int, [lo, hi] or
                                          # "all" = one per association); the extra "<qry> K V" blocks ask
                                          # about distractor pairs before the final (scored) query; eval uses 1
    single_query_prob: float = 0.0        # share of training sequences forced to a single query (keeps the
                                          # evaluation format inside the training distribution)
    value_vocab: str = "separate"         # separate: values from V0..V31 (a value-TYPE shortcut exists:
                                          # "answer with any value token"); shared: values drawn from the
                                          # key tokens K0..K31 (no type shortcut; requires no lures, so
                                          # pairs are identified by position; fillers are skipped)
    aux_show_answers: bool = True         # True: "<qry> K <ans> V" (answer inserted -> ELIMINATION SHORTCUT:
                                          # the scored answer is the only value not yet shown). False:
                                          # "<qry> K <ans>" supervised at <ans>, answer never inserted.
    # --- multihop ---------------------------------------------------------------
    hops: Range = (1, 2)
    n_chains: Range = (2, 4)              # chains in context, including the target chain
    query_types: tuple = ("end",)         # "end" (follow to chain end) and/or "next" (one hop)
    link_order: str = "random"            # random | forward | backward (order of target links)
    hop_gap: int | None = None            # exact token gap between consecutive target links
    # --- induction control ------------------------------------------------------
    induction_order: str = "shuffled"     # shuffled: second half permuted (content matching required)
                                          # fixed: same order (solvable by a fixed positional offset)
                                          # mixed: fixed with probability induction_fixed_prob, else shuffled
    induction_fixed_prob: float = 0.0     # share of shortcut-admitting (fixed-order) examples when "mixed"

    def to_dict(self) -> dict:
        d = asdict(self)
        for k, v in d.items():
            if isinstance(v, tuple):
                d[k] = list(v)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "TaskConfig":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def eval_format(self) -> "TaskConfig":
        """Same content distribution in the single-query evaluation format -- but only if
        single-query sequences are part of the training distribution; otherwise unchanged."""
        nq = self.n_queries
        has_single = (self.single_query_prob > 0 or nq == 1
                      or (isinstance(nq, (list, tuple)) and int(nq[0]) <= 1))
        return self.replace(n_queries=1, single_query_prob=0.0) if has_single else self

    def replace(self, **kw) -> "TaskConfig":
        d = self.to_dict()
        unknown = set(kw) - set(d)
        if unknown:
            raise KeyError(f"unknown TaskConfig fields: {sorted(unknown)}")
        d.update(kw)
        return TaskConfig.from_dict(d)


@dataclass
class Example:
    tokens: list[int]
    answer: int
    meta: dict = field(default_factory=dict)

    @property
    def ans_pos(self) -> int:
        return len(self.tokens) - 1

    def public_meta(self) -> dict:
        """Meta without private (``_``-prefixed) structures -- for DataFrames."""
        return {k: v for k, v in self.meta.items() if not k.startswith("_")}


# ----------------------------------------------------------------------------- helpers
def stable_hash(s: str) -> int:
    return zlib.crc32(s.encode("utf-8"))


def make_rng(seed: int, stream: str) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([int(seed), stable_hash(stream)]))


def draw(rng: np.random.Generator, spec: Range) -> int:
    if isinstance(spec, (int, np.integer)):
        return int(spec)
    lo, hi = spec
    return int(rng.integers(int(lo), int(hi) + 1))


def range_max(spec: Range) -> int:
    return int(spec) if isinstance(spec, (int, np.integer)) else int(spec[1])


def layout_context(rng: np.random.Generator, C: int, fixed: list, free: list, n_fill: int,
                   filler_ids: range) -> tuple[list, list]:
    """Assemble a context of exactly ``C`` tokens.

    fixed : list of (offset, kind, tokens) placed exactly at ``offset``.
    free  : list of (kind, tokens), all of equal length m, distributed randomly
            in the gaps around fixed units, proportionally to gap size.
    n_fill: number of single filler tokens; must make the total length C.

    Returns (units, fixed_offsets) where units is a list of
    (kind, start_offset, tokens).
    """
    m = len(free[0][1]) if free else 1
    if any(len(t) != m for _, t in free):
        raise ValueError("free units must have equal length")
    total = sum(len(t) for _, _, t in fixed) + m * len(free) + n_fill
    if total != C:
        raise ValueError(f"unit lengths ({total}) do not add up to C={C}")
    fixed = sorted(fixed, key=lambda f: f[0])
    gaps, prev_end = [], 0
    for off, _, toks in fixed:
        gaps.append(off - prev_end)
        prev_end = off + len(toks)
    gaps.append(C - prev_end)
    if min(gaps) < 0:
        raise LayoutError("fixed units overlap or exceed the context")

    n_rem, f_rem, len_rem = len(free), n_fill, C - sum(len(t) for _, _, t in fixed)
    alloc = []
    for j, g in enumerate(gaps):
        if j == len(gaps) - 1:
            a, b = n_rem, f_rem
            if a * m + b != g:
                raise LayoutError("last gap cannot be filled exactly")
        else:
            lo = max(0, -(-(g - f_rem) // m))
            hi = min(n_rem, g // m)
            cap_future = sum(gk // m for gk in gaps[j + 1:])
            lo = max(lo, n_rem - cap_future)
            if lo > hi:
                raise LayoutError(f"gap {j} of size {g} cannot be filled")
            p = g / len_rem if len_rem > 0 else 0.0
            a = int(np.clip(rng.binomial(n_rem, p), lo, hi))
            b = g - a * m
        alloc.append((a, b))
        n_rem, f_rem, len_rem = n_rem - a, f_rem - b, len_rem - g

    order = list(rng.permutation(len(free)))
    fill_tokens = iter(rng.integers(filler_ids.start, filler_ids.stop, size=n_fill).tolist())
    units, offsets, pos, fi = [], [], 0, 0
    for j, (a, b) in enumerate(alloc):
        chunk = [free[order[fi + i]] for i in range(a)] + [("filler", None)] * b
        fi += a
        for idx in rng.permutation(len(chunk)):
            kind, toks = chunk[idx]
            if toks is None:
                toks = [next(fill_tokens)]
            units.append((kind, pos, list(toks)))
            pos += len(toks)
        if j < len(fixed):
            off, kind, toks = fixed[j]
            assert pos == off, (pos, off)
            units.append((kind, pos, list(toks)))
            offsets.append(pos)
            pos += len(toks)
    assert pos == C
    return units, offsets


def _snap_candidates(t: int, lo: int, hi: int):
    yield t
    for d in range(1, hi - lo + 1):
        for c in (t - d, t + d):
            if lo <= c <= hi:
                yield c


def units_to_tokens(units) -> list[int]:
    out = []
    for _, _, toks in units:
        out.extend(toks)
    return out


def _marker(cfg: TaskConfig) -> bool:
    if cfg.query_format not in ("key_last", "ans_marker"):
        raise ValueError(f"unknown query_format {cfg.query_format!r}")
    return cfg.query_format == "ans_marker"


# ----------------------------------------------------------------------------- recall
def _sample_keys(rng, cfg: TaskConfig, vocab: Vocab, n_pairs: int):
    keys = np.array(vocab.keys())
    k = cfg.key_len
    target = tuple(int(x) for x in rng.choice(keys, size=k, replace=False))
    distractors, near = [], 0
    seen = {target}
    tries = 0
    while len(distractors) < n_pairs - 1:
        tries += 1
        if tries > 10_000:
            raise LayoutError("could not sample distinct distractor keys")
        if k == 1:
            cand = (int(rng.choice(keys)),)
        elif rng.random() < cfg.near_miss_frac:
            cand = (target[0],) + tuple(int(x) for x in rng.choice(keys, size=k - 1, replace=False))
        else:
            cand = tuple(int(x) for x in rng.choice(keys, size=k, replace=False))
        if cand == target or (cand in seen and not cfg.repeat_distractor_keys):
            continue
        if len(set(cand)) != len(cand):
            continue
        seen.add(cand)
        near += int(k > 1 and cand[0] == target[0])
        distractors.append(cand)
    return target, distractors, near


def gen_recall(rng: np.random.Generator, cfg: TaskConfig, vocab: Vocab, L: int) -> Example:
    k = cfg.key_len
    marker = _marker(cfg)
    m, qlen = k + 1, k + 1 + int(marker)
    query_all = cfg.n_queries == "all"
    n_q = 1 if query_all else max(1, draw(rng, cfg.n_queries))
    single = rng.random() < cfg.single_query_prob
    n_pairs_drawn = draw(rng, cfg.n_pairs)
    if query_all:
        n_q = n_pairs_drawn          # one query per association (reduced below if it does not fit)
    if single:
        n_q = 1
    n_lures_drawn = draw(rng, cfg.n_lures) if rng.random() < cfg.lure_prob else 0
    blk = qlen + int(cfg.aux_show_answers)          # length of one auxiliary block
    while True:  # fewer auxiliary queries leave more room for the context
        C = L - 1 - qlen - (n_q - 1) * blk
        max_items = C // m if C >= m else 0
        n_lures = min(n_lures_drawn, max(0, max_items - 1))
        n_pairs = max_items - n_lures if cfg.fill_pairs else n_pairs_drawn
        n_pairs = max(1, min(n_pairs, max_items - n_lures))
        if not cfg.repeat_distractor_keys and k == 1:
            n_pairs = min(n_pairs, vocab.n_keys)
        if n_q == 1 or (max_items >= 1 and n_pairs >= n_q):
            break
        n_q = min(n_q - 1, max(1, n_pairs))
    if C < m:
        raise ValueError(f"seq_len {L} too short for key_len {k}")

    target_key, dkeys, n_near = _sample_keys(rng, cfg, vocab, n_pairs)
    if cfg.value_vocab == "shared":
        if n_lures or k != 1:
            raise ValueError("value_vocab='shared' requires no lures and key_len=1")
        vals = [int(v) for v in rng.choice(np.array(vocab.keys()), size=n_pairs, replace=True)]
    elif cfg.value_vocab == "separate":
        vals = [int(v) for v in rng.choice(np.array(vocab.values()), size=n_pairs, replace=True)]
    else:
        raise ValueError(f"unknown value_vocab {cfg.value_vocab}")
    evidence = list(target_key) + [vals[0]]
    free = [("pair", list(key) + [v]) for key, v in zip(dkeys, vals[1:])]
    free += [("lure", list(target_key) + [int(rng.choice(vocab.fillers()))]) for _ in range(n_lures)]
    n_fill = C - m * (n_pairs + n_lures)
    # Everything above is *content*; everything below is *placement* and uses its own RNG,
    # so the content stream does not depend on evidence position or length (paired cells).
    rng = np.random.default_rng(int(rng.integers(2**63)))

    max_t = C - m
    if cfg.evidence_distance is not None:
        t = L - 2 - k - int(cfg.evidence_distance)
        if not 0 <= t <= max_t:
            raise ValueError(f"evidence_distance {cfg.evidence_distance} infeasible for seq_len {L}")
    elif cfg.evidence_pos is not None:
        t = int(round(float(cfg.evidence_pos) * max_t))
    else:
        t = int(rng.integers(0, max_t + 1))
    requested = t
    for cand in _snap_candidates(t, 0, max_t):
        try:
            units, (t_actual,) = layout_context(rng, C, [(cand, "evidence", evidence)], free, n_fill,
                                                vocab.fillers())
            break
        except LayoutError:
            continue
    else:
        raise LayoutError("no feasible evidence offset")

    aux, aux_answers = [], []
    if n_q > 1:
        counts: dict = {}
        for key in dkeys:
            counts[key] = counts.get(key, 0) + 1
        uniq = [(key, v) for key, v in zip(dkeys, vals[1:]) if counts[key] == 1]
        if len(uniq) < n_q - 1:
            raise LayoutError("not enough unique distractor keys for auxiliary queries")
        for j in rng.permutation(len(uniq))[: n_q - 1]:
            key, v = uniq[int(j)]
            aux += [QRY] + list(key) + ([ANS] if marker else []) + ([v] if cfg.aux_show_answers else [])
            aux_answers.append(v)
    q = [QRY] + list(target_key) + ([ANS] if marker else [])
    ctx = units_to_tokens(units)
    tokens = [BOS] + ctx + aux + q
    ans_pos = len(tokens) - 1
    value_pos = 1 + t_actual + k
    aux_pos = [1 + C + blk * j + qlen - 1 for j in range(n_q - 1)]   # predicting position of block j
    meta = {
        "task": "recall", "seq_len": L, "context_len": C, "key_len": k, "query_format": cfg.query_format,
        "n_pairs": n_pairs, "n_distractor_pairs": n_pairs - 1, "n_lures": n_lures, "n_fillers": n_fill,
        "n_near_miss": n_near, "repeat_distractor_keys": bool(cfg.repeat_distractor_keys),
        "n_distinct_distractor_keys": len(set(dkeys)),
        "evidence_offset": t_actual, "evidence_offset_requested": requested,
        "evidence_norm_pos": t_actual / max_t if max_t > 0 else 0.0,
        "evidence_key_pos": 1 + t_actual, "evidence_value_pos": value_pos,
        "distance": ans_pos - value_pos, "answer": vals[0], "n_queries": n_q,
        "aux_show_answers": bool(cfg.aux_show_answers), "value_vocab": cfg.value_vocab,
        "_units": units, "_query": q, "_target_key": list(target_key),
        "_aux_region": aux, "_aux": list(zip(aux_pos, aux_answers)),
    }
    return Example(tokens, vals[0], meta)


# ----------------------------------------------------------------------------- multihop
def gen_multihop(rng: np.random.Generator, cfg: TaskConfig, vocab: Vocab, L: int) -> Example:
    marker = _marker(cfg)
    C = L - 1 - 2 - int(marker)
    h = draw(rng, cfg.hops)
    if 3 * h > C:
        raise ValueError(f"seq_len {L} too short for {h} hops")
    n_chains = draw(rng, cfg.n_chains)
    lens = [h] + [draw(rng, cfg.hops) for _ in range(max(0, n_chains - 1))]
    while len(lens) > 1 and (3 * sum(lens) > C or sum(x + 1 for x in lens) > vocab.n_entities):
        lens.pop()
    ents = [int(e) for e in rng.permutation(np.array(vocab.entities()))[: sum(x + 1 for x in lens)]]
    chains, i = [], 0
    for n in lens:
        chains.append(ents[i:i + n + 1])
        i += n + 1
    target = chains[0]
    tlinks = [[target[j], ARROW, target[j + 1]] for j in range(h)]
    free = [("link", [c[j], ARROW, c[j + 1]]) for c in chains[1:] for j in range(len(c) - 1)]
    n_fill = C - 3 * (h + len(free))

    qtype = str(rng.choice(list(cfg.query_types)))
    if qtype == "next":
        qi = int(rng.integers(0, h))
        q, answer = [NXT, target[qi]] + ([ANS] if marker else []), target[qi + 1]
    elif qtype == "end":
        qi = 0
        q, answer = [QRY, target[0]] + ([ANS] if marker else []), target[h]
    else:
        raise ValueError(f"unknown query type {qtype}")
    rng = np.random.default_rng(int(rng.integers(2**63)))   # placement RNG (see gen_recall)

    # slot order: slot s holds link order[s]
    if cfg.link_order == "forward":
        order = list(range(h))
    elif cfg.link_order == "backward":
        order = list(range(h))[::-1]
    elif cfg.link_order == "random":
        order = [int(x) for x in rng.permutation(h)]
    else:
        raise ValueError(f"unknown link_order {cfg.link_order}")

    if cfg.hop_gap is not None:
        g = int(cfg.hop_gap)
        span = 3 * h + g * (h - 1)
        if span > C:
            raise ValueError(f"hop_gap {g} infeasible for seq_len {L}")
        s = int(rng.integers(0, C - span + 1))
        fixed = [(s + slot * (3 + g), "target_link", tlinks[order[slot]]) for slot in range(h)]
        units, _ = layout_context(rng, C, fixed, free, n_fill, vocab.fillers())
    else:
        units, _ = layout_context(rng, C, [], free + [("target_link", t) for t in tlinks], n_fill,
                                  vocab.fillers())
        slots = [i for i, u in enumerate(units) if u[0] == "target_link"]
        for slot_rank, ui in enumerate(slots):
            kind, off, _ = units[ui]
            units[ui] = (kind, off, list(tlinks[order[slot_rank]]))

    tokens = [BOS] + units_to_tokens(units) + q
    ans_pos = len(tokens) - 1
    link_pos = {}
    for kind, off, toks in units:
        if kind == "target_link":
            link_pos[target.index(toks[0])] = 1 + off      # hop index -> absolute start position
    link_starts = [link_pos[j] for j in range(h)]
    relevant = [link_starts[qi]] if qtype == "next" else link_starts
    meta = {
        "task": "multihop", "seq_len": L, "context_len": C, "hops": h, "query_type": qtype,
        "query_format": cfg.query_format,
        "query_hop_index": qi, "n_chains": len(chains), "n_distractor_links": len(free),
        "n_fillers": n_fill, "link_order": cfg.link_order,
        "first_link_pos": link_starts[0], "last_link_pos": link_starts[-1],
        "max_distance": ans_pos - min(relevant), "min_distance": ans_pos - max(relevant) - 2,
        "link_span": (max(link_starts) - min(link_starts)) if h > 1 else 0,
        "evidence_norm_pos": (min(relevant) - 1) / max(1, C - 3), "answer": answer,
        "distance": ans_pos - (max(relevant) + 2),
        "_units": units, "_chains": chains, "_link_starts": link_starts, "_query": q,
    }
    return Example(tokens, answer, meta)


# ----------------------------------------------------------------------------- induction control
def gen_induction(rng: np.random.Generator, cfg: TaskConfig, vocab: Vocab, L: int) -> Example:
    """<bos> [pad filler if L is odd] A_1 .. A_n  B_1 .. B_{n-1}

    A is n distinct entities; B is a permutation of A_1..A_{n-1} (``shuffled``)
    or A_1..A_{n-1} in order (``fixed``). The target at every B position is the
    token that followed the same entity in A (A_n has no successor, so it is
    never queried). In ``fixed`` order the source is always n-1 positions back,
    so a purely positional rule solves the task; in ``shuffled`` order the
    offset varies and only content matching works. The final position is
    scored; with ``n_queries="all"`` every other B position is an auxiliary
    training target.
    """
    n = L // 2
    if n < 3:
        raise ValueError(f"seq_len {L} too short for the induction task")
    if n > vocab.n_entities:
        raise ValueError(f"seq_len {L} needs {n} distinct entities (> {vocab.n_entities})")
    first = [int(e) for e in rng.permutation(np.array(vocab.entities()))[:n]]
    order = cfg.induction_order
    if order == "mixed":
        order = "fixed" if rng.random() < cfg.induction_fixed_prob else "shuffled"
    if order == "shuffled":
        second = [first[int(i)] for i in rng.permutation(n - 1)]
    elif order == "fixed":
        second = first[:-1]
    else:
        raise ValueError(f"unknown induction_order {cfg.induction_order}")
    pad = [int(rng.integers(vocab.filler_start, vocab.key_start))] if L % 2 else []
    off = 1 + len(pad)                       # absolute position of A_1
    tokens = [BOS] + pad + first + second
    succ = {first[i]: first[i + 1] for i in range(n - 1)}
    src = {first[i]: off + i for i in range(n)}
    b0 = off + n                             # absolute position of B_1
    targets = [(b0 + j, succ[t]) for j, t in enumerate(second)]
    ans_pos, answer = targets[-1]
    # supervision density: "all" = every second-half position; an integer k = the last k positions
    if cfg.n_queries == "all":
        aux = targets[:-1]
    elif isinstance(cfg.n_queries, int) and cfg.n_queries > 1:
        aux = targets[-cfg.n_queries:-1]
    else:
        aux = []
    q = second[-1]
    meta = {
        "task": "induction", "seq_len": L, "half_len": n, "induction_order": order, "key_len": 1,
        "evidence_key_pos": src[q], "evidence_value_pos": src[q] + 1, "distance": ans_pos - (src[q] + 1),
        "match_offset": ans_pos - src[q], "evidence_norm_pos": (src[q] - off) / max(1, n - 1), "answer": answer,
        "n_queries": 1 + len(aux), "n_pairs": n - 1,
        "_units": [("filler", 1, pad)] * bool(pad) + [("first_half", off, first), ("second_half", b0, second)],
        "_query": [q], "_aux": aux,
    }
    assert len(tokens) == L and ans_pos == L - 1
    return Example(tokens, answer, meta)


GENERATORS = {"recall": gen_recall, "multihop": gen_multihop, "induction": gen_induction}


# ----------------------------------------------------------------------------- sampling API
class TaskSampler:
    """Seeded example stream. Different ``stream`` names give independent RNG
    streams from the same seed (e.g. "train", "val", "eval/<cell>")."""

    def __init__(self, cfg: TaskConfig, seed: int, stream: str = "train", vocab: Vocab = DEFAULT_VOCAB,
                 max_retries: int = 50):
        self.cfg, self.vocab, self.seed, self.stream = cfg, vocab, seed, stream
        self.rng = make_rng(seed, stream)
        self.gen = GENERATORS[cfg.task]
        self.max_retries = max_retries

    def draw_length(self) -> int:
        if self.cfg.length_choices:
            return int(self.rng.choice(self.cfg.length_choices))
        return draw(self.rng, self.cfg.seq_len)

    def example(self, L: int | None = None) -> Example:
        L = self.draw_length() if L is None else L
        last = None
        for _ in range(self.max_retries):
            try:
                return self.gen(self.rng, self.cfg, self.vocab, L)
            except LayoutError as e:   # random layout dead-end: resample
                last = e
        raise LayoutError(f"failed to generate after {self.max_retries} retries: {last}")

    def batch(self, B: int, L: int | None = None) -> dict:
        """A batch of B examples sharing one length (no padding needed)."""
        L = self.draw_length() if L is None else L
        return collate([self.example(L) for _ in range(B)])


def make_dataset(cfg: TaskConfig, n: int, seed: int, stream: str, vocab: Vocab = DEFAULT_VOCAB) -> list:
    s = TaskSampler(cfg, seed, stream, vocab)
    return [s.example() for _ in range(n)]


def collate(examples: list[Example]) -> dict:
    T = max(len(e.tokens) for e in examples)
    toks = torch.full((len(examples), T), PAD, dtype=torch.long)
    for i, e in enumerate(examples):
        toks[i, : len(e.tokens)] = torch.tensor(e.tokens, dtype=torch.long)
    out = {
        "tokens": toks,
        "ans_pos": torch.tensor([e.ans_pos for e in examples], dtype=torch.long),
        "answers": torch.tensor([e.answer for e in examples], dtype=torch.long),
    }
    aux = [(i, p, a) for i, e in enumerate(examples) for p, a in e.meta.get("_aux", [])]
    if aux:  # auxiliary (training-only) answer positions, flattened
        out["aux_rows"] = torch.tensor([r for r, _, _ in aux], dtype=torch.long)
        out["aux_pos"] = torch.tensor([p for _, p, _ in aux], dtype=torch.long)
        out["aux_answers"] = torch.tensor([a for _, _, a in aux], dtype=torch.long)
    return out


# ----------------------------------------------------------------------------- controlled edits
def _rebuild(ex: Example, units, query=None, answer=None) -> Example:
    q = query if query is not None else ex.meta["_query"]
    tokens = [BOS] + units_to_tokens(units) + list(ex.meta.get("_aux_region", [])) + list(q)
    meta = copy.copy(ex.meta)
    meta["_units"], meta["_query"] = units, list(q)
    new = Example(tokens, ex.answer if answer is None else answer, meta)
    new.meta["answer"] = new.answer
    return new


def _reoffset(units):
    out, pos = [], 0
    for kind, _, toks in units:
        out.append((kind, pos, toks))
        pos += len(toks)
    return out


def move_evidence(ex: Example, target_offset: int) -> Example:
    """Recall: move the evidence unit to the unit boundary closest to
    ``target_offset`` while keeping the relative order of all other units."""
    assert ex.meta["task"] == "recall"
    units = list(ex.meta["_units"])
    ev_i = next(i for i, u in enumerate(units) if u[0] == "evidence")
    ev = units.pop(ev_i)
    units = _reoffset(units)
    boundaries = [u[1] for u in units] + [sum(len(u[2]) for u in units)]
    best = int(np.argmin([abs(b - target_offset) for b in boundaries]))
    units.insert(best, ev)
    units = _reoffset(units)
    new = _rebuild(ex, units)
    t = next(u[1] for u in units if u[0] == "evidence")
    k, C = ex.meta["key_len"], ex.meta["context_len"]
    max_t = C - (k + 1)
    new.meta.update(evidence_offset=t, evidence_offset_requested=target_offset,
                    evidence_norm_pos=t / max_t if max_t else 0.0, evidence_key_pos=1 + t,
                    evidence_value_pos=1 + t + k, distance=new.ans_pos - (1 + t + k))
    return new


def remove_evidence(ex: Example, rng: np.random.Generator, vocab: Vocab = DEFAULT_VOCAB) -> Example:
    """Control: replace the evidence unit with fillers of equal length. The
    original answer is then *not determined by the context*; a model that
    still predicts it above chance is using a shortcut."""
    units = [(k, o, [int(rng.choice(vocab.fillers())) for _ in t]) if k == "evidence" else (k, o, t)
             for k, o, t in ex.meta["_units"]]
    new = _rebuild(ex, units)
    new.meta["evidence_removed"] = True
    return new


def corrupt_query(ex: Example, rng: np.random.Generator) -> Example | None:
    """Recall: same context, query a different (unique-key) distractor pair.
    Returns None if no distractor pair has a unique key."""
    pairs = [(tuple(t[:-1]), t[-1], o) for k, o, t in ex.meta["_units"] if k == "pair"]
    counts: dict = {}
    for key, _, _ in pairs:
        counts[key] = counts.get(key, 0) + 1
    tk = tuple(ex.meta["_target_key"])
    cands = [p for p in pairs if counts[p[0]] == 1 and p[0] != tk]
    if not cands:
        return None
    key, val, off = cands[int(rng.integers(len(cands)))]
    q = [QRY] + list(key) + ([ANS] if ex.meta.get("query_format") == "ans_marker" else [])
    new = _rebuild(ex, ex.meta["_units"], query=q, answer=val)
    new.meta.update(corrupted_from=ex.answer, corrupt_value_pos=1 + off + len(key))
    return new


def multihop_query_variant(ex: Example, qtype: str, hop_index: int = 0) -> Example:
    """Same multi-hop context, different query. ``next`` with hop_index i asks
    for the successor of the i-th chain node; ``end`` asks for the chain end
    starting from node ``hop_index``."""
    assert ex.meta["task"] == "multihop"
    chain = ex.meta["_chains"][0]
    h = len(chain) - 1
    tail = [ANS] if ex.meta.get("query_format") == "ans_marker" else []
    if qtype == "next":
        q, ans = [NXT, chain[hop_index]] + tail, chain[hop_index + 1]
    else:
        q, ans = [QRY, chain[hop_index]] + tail, chain[h]
    new = _rebuild(ex, ex.meta["_units"], query=q, answer=ans)
    new.meta.update(query_type=qtype, query_hop_index=hop_index, hops=h - hop_index if qtype == "end" else 1)
    return new
