"""Dataset validation: an *independent* oracle parser that re-derives the answer
from the token sequence alone (it never reads the generator's metadata), plus
invariant checks that compare the metadata against the tokens.

If the generator and the oracle disagree, the data -- not the model -- is wrong.
"""

from __future__ import annotations

from collections import Counter

from .tasks import Example
from .vocab import ANS, ARROW, BOS, DEFAULT_VOCAB, NXT, PAD, QRY, Vocab


class AmbiguousExample(ValueError):
    pass


def query_block_len(tokens, key_len: int) -> int:
    """Length of the final query block, detected from the tokens themselves:
    ``<qry> K..`` (key_last) or ``<qry> K.. <ans>`` (ans_marker)."""
    return key_len + 1 + int(tokens[-1] == ANS)


def parse_recall(tokens, key_len: int, vocab: Vocab = DEFAULT_VOCAB):
    """Return (pairs, query_key) where pairs is a list of (key_tuple, value, key_pos).
    Auxiliary training query blocks (``<qry> K [<ans>] V``) are skipped."""
    k = key_len
    ql = query_block_len(tokens, k)
    marker = ql == k + 2
    q = tokens[-ql:]
    if q[0] != QRY:
        raise ValueError("malformed query block")
    qkey = tuple(q[1:1 + k])
    ctx_end = len(tokens) - ql
    pairs, i = [], 1
    while i < ctx_end:
        if tokens[i] == QRY:            # auxiliary query block: <qry> K.. [<ans>] [V]
            i += 1 + k + int(marker)
            if i < ctx_end and vocab.kind(tokens[i]) == "value":
                i += 1                  # displayed answer (aux_show_answers=True)
            continue
        window = tokens[i:i + k]
        if (i + k < ctx_end and len(window) == k and all(vocab.kind(t) == "key" for t in window)
                and vocab.kind(tokens[i + k]) == "value"):
            pairs.append((tuple(window), tokens[i + k], i))
            i += k + 1
        else:
            i += 1
    return pairs, qkey


def parse_recall_positional(tokens, vocab: Vocab = DEFAULT_VOCAB):
    """Shared-vocabulary recall (packed context, key_len 1): pairs are identified by POSITION.
    The context is <bos> followed by (key, value) pairs, then at most one filler, then the query
    region; auxiliary blocks start with <qry>."""
    ql = query_block_len(tokens, 1)
    q = tokens[-ql:]
    if q[0] != QRY:
        raise ValueError("malformed query block")
    first_q = tokens.index(QRY)
    pairs, i = [], 1
    while i < first_q:
        if vocab.kind(tokens[i]) == "filler":     # a leftover filler can sit anywhere; pairs stay contiguous
            i += 1
            continue
        if i + 1 < first_q and vocab.kind(tokens[i]) == "key" and vocab.kind(tokens[i + 1]) == "key":
            pairs.append(((tokens[i],), tokens[i + 1], i))
            i += 2
        else:
            raise ValueError(f"cannot parse shared-vocabulary pair at position {i}")
    return pairs, (q[1],)


def oracle_recall(tokens, key_len: int, vocab: Vocab = DEFAULT_VOCAB, positional: bool = False) -> int:
    pairs, qkey = parse_recall_positional(tokens, vocab) if positional else parse_recall(tokens, key_len, vocab)
    hits = [v for key, v, _ in pairs if key == qkey]
    if len(hits) != 1:
        raise AmbiguousExample(f"query key matched {len(hits)} associations")
    return hits[0]


def parse_links(tokens, vocab: Vocab = DEFAULT_VOCAB) -> dict:
    succ: dict = {}
    for i in range(1, len(tokens) - 2):
        a, arrow, b = tokens[i:i + 3]
        if arrow == ARROW and vocab.kind(a) == "entity" and vocab.kind(b) == "entity":
            if a in succ:
                raise AmbiguousExample(f"entity {a} has two successors")
            succ[a] = b
    return succ


def oracle_multihop(tokens, vocab: Vocab = DEFAULT_VOCAB) -> int:
    qtok, e = (tokens[-3], tokens[-2]) if tokens[-1] == ANS else (tokens[-2], tokens[-1])
    if qtok not in (QRY, NXT):
        raise ValueError("malformed query block")
    succ = parse_links(tokens, vocab)
    if e not in succ:
        raise AmbiguousExample("query entity has no outgoing link")
    if qtok == NXT:
        return succ[e]
    seen = {e}
    while e in succ:
        e = succ[e]
        if e in seen:
            raise AmbiguousExample("cycle")
        seen.add(e)
    return e


def oracle_induction(tokens) -> int:
    """Successor of the earliest occurrence of the final token."""
    q = tokens[-1]
    i = tokens.index(q)
    if i >= len(tokens) - 2:
        raise AmbiguousExample("final token has no earlier occurrence with a successor")
    return tokens[i + 1]


def oracle(ex: Example, vocab: Vocab = DEFAULT_VOCAB) -> int:
    if ex.meta["task"] == "recall":
        return oracle_recall(ex.tokens, ex.meta["key_len"], vocab,
                             positional=ex.meta.get("value_vocab") == "shared")
    if ex.meta["task"] == "induction":
        return oracle_induction(ex.tokens)
    return oracle_multihop(ex.tokens, vocab)


def check_example(ex: Example, vocab: Vocab = DEFAULT_VOCAB) -> list[str]:
    """Return a list of violated invariants (empty list = valid)."""
    errs = []
    t, m = ex.tokens, ex.meta
    if len(t) != m["seq_len"]:
        errs.append(f"length {len(t)} != seq_len {m['seq_len']}")
    if t[0] != BOS:
        errs.append("first token is not <bos>")
    fmt = m.get("query_format", "key_last")
    if m["task"] != "induction" and (t[-1] == ANS) != (fmt == "ans_marker"):
        errs.append(f"final token inconsistent with query_format {fmt}")
    if PAD in t:
        errs.append("<pad> inside example")
    if max(t) >= vocab.size or min(t) < 0:
        errs.append("token id outside vocab")
    try:
        o = oracle(ex, vocab)
        if o != ex.answer:
            errs.append(f"oracle answer {o} != stored answer {ex.answer}")
    except (AmbiguousExample, ValueError) as e:
        errs.append(f"oracle failed: {e}")
    if m["task"] == "induction":
        n = m["half_len"]
        body = t[len(t) - (2 * n - 1):]
        first, second = body[:n], body[n:]
        if len(set(first)) != n or sorted(second) != sorted(first[:-1]):
            errs.append("induction halves malformed")
        for pos, ans in m.get("_aux", []):
            if oracle_induction(t[:pos + 1]) != ans:
                errs.append(f"auxiliary target at {pos} inconsistent")
        if m["induction_order"] == "fixed" and m["match_offset"] != n:
            errs.append("fixed order must have constant match offset n (successor n-1 back)")
    elif m["task"] == "recall":
        k = m["key_len"]
        ql = query_block_len(t, k)
        qk = tuple(t[len(t) - ql + 1:len(t) - ql + 1 + k])
        vp, kp = m["evidence_value_pos"], m["evidence_key_pos"]
        if t[vp] != ex.answer:
            errs.append("token at evidence_value_pos is not the answer")
        if tuple(t[kp:kp + k]) != qk:
            errs.append("evidence key does not match query key")
        if m.get("value_vocab") == "shared":
            pairs, _ = parse_recall_positional(t, vocab)
            if len(pairs) != m["n_pairs"]:
                errs.append(f"positional parse found {len(pairs)} pairs, meta says {m['n_pairs']}")
            if sum(1 for key, _, _ in pairs if key == qk) != 1:
                errs.append("query key is not a unique pair key")
            return errs
        if m["distance"] != len(t) - 1 - vp:
            errs.append("distance inconsistent with positions")
        pairs, _ = parse_recall(t, k, vocab)
        if len(pairs) != m["n_pairs"]:
            errs.append(f"parsed {len(pairs)} pairs, meta says {m['n_pairs']}")
        # lures: query key occurrences not followed by a value
        occ = sum(1 for i in range(1, len(t) - ql - k + 1) if tuple(t[i:i + k]) == qk)
        if occ != 1 + m["n_lures"]:
            errs.append(f"query key occurs {occ} times in context, expected {1 + m['n_lures']}")
    else:
        for h, pos in enumerate(m["_link_starts"]):
            chain = m["_chains"][0]
            if t[pos:pos + 3] != [chain[h], ARROW, chain[h + 1]]:
                errs.append(f"target link {h} not at recorded position {pos}")
    return errs


def token_signature(ex: Example) -> tuple:
    return tuple(ex.tokens) + (ex.answer,)


def overlap_count(a: list[Example], b: list[Example]) -> int:
    """Number of examples in ``b`` whose exact token sequence (and answer) also appears in ``a``."""
    sa = {token_signature(e) for e in a}
    return sum(token_signature(e) in sa for e in b)


def dataset_summary(examples: list[Example]) -> dict:
    lens = Counter(len(e.tokens) for e in examples)
    tasks = Counter(e.meta["task"] for e in examples)
    out = {"n_examples": len(examples), "tasks": dict(tasks),
           "length_min": min(lens), "length_max": max(lens),
           "length_mean": sum(k * v for k, v in lens.items()) / len(examples),
           "n_distinct_lengths": len(lens), "n_unique_sequences": len({token_signature(e) for e in examples})}
    return out
