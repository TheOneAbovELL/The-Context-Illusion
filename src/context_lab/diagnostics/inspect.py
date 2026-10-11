"""Mechanistic diagnostics (observational).

These tools *describe* internal quantities. Attention weights show where a
head reads from, not what information is used or whether it is causally
important; for causal claims use :mod:`context_lab.interventions`.

Roles
-----
Every position of an example is labelled with a role derived from the
generator's unit structure: ``bos``, ``evidence_key``, ``evidence_value``,
``distractor_key``, ``distractor_value``, ``lure_key``, ``lure_filler``,
``filler``, ``query_marker``, ``query_key``, ``ans``; multi-hop:
``target_link_src/arrow/dst``, ``link_src/arrow/dst``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

from ..data import Example, collate, move_evidence
from ..data.vocab import DEFAULT_VOCAB


# ----------------------------------------------------------------------------- roles
def position_roles(ex: Example) -> list[str]:
    if ex.meta["task"] == "induction":
        T = len(ex.tokens)
        roles = ["bos"] + ["filler"] * (T % 2)
        n = ex.meta["half_len"]
        roles += ["first_half"] * n + ["second_half"] * (n - 1)
        roles[ex.meta["evidence_key_pos"]] = "evidence_key"
        roles[ex.meta["evidence_value_pos"]] = "evidence_value"
        roles[-1] = "ans"
        return roles
    roles = ["bos"]
    for kind, _, toks in ex.meta["_units"]:
        n = len(toks)
        if kind == "evidence":
            roles += ["evidence_key"] * (n - 1) + ["evidence_value"]
        elif kind == "pair":
            roles += ["distractor_key"] * (n - 1) + ["distractor_value"]
        elif kind == "lure":
            roles += ["lure_key"] * (n - 1) + ["lure_filler"]
        elif kind == "filler":
            roles += ["filler"]
        elif kind in ("link", "target_link"):
            p = "target_link" if kind == "target_link" else "link"
            roles += [f"{p}_src", f"{p}_arrow", f"{p}_dst"]
        else:
            roles += [kind] * n
    roles += ["aux_query"] * len(ex.meta.get("_aux_region", []))
    q = ex.meta["_query"]
    roles += ["query_marker"] + ["query_key"] * (len(q) - 2) + ["ans"]
    assert len(roles) == len(ex.tokens), (len(roles), len(ex.tokens))
    return roles


# ----------------------------------------------------------------------------- single example
@torch.no_grad()
def inspect_example(model, ex: Example, top_k: int = 5, vocab=DEFAULT_VOCAB, pos_offset: int = 0) -> dict:
    """Everything needed to look at one example: tokens, roles, prediction,
    attention maps, per-layer logit lens and attention from <ans> to evidence."""
    b = collate([ex])
    logits, cache = model.run_with_cache(b["tokens"], pos_offset=pos_offset)
    ap = ex.ans_pos
    probs = torch.softmax(logits[0, ap], -1)
    top = torch.topk(probs, top_k)
    L = model.cfg.n_layers
    attn = np.stack([cache[f"L{l}.attn.probs"][0].numpy() for l in range(L)])     # (L, H, T, T)
    scores = np.stack([cache[f"L{l}.attn.scores"][0].numpy() for l in range(L)])
    lens = []
    for l in range(L):
        r = cache[f"L{l}.resid_post"][0, ap]
        p = torch.softmax(model.unembed(model.ln_f(r)), -1)
        lens.append({"layer": l, "p_answer": float(p[ex.answer]), "top": vocab.token_str(int(p.argmax())),
                     "p_top": float(p.max())})
    roles = position_roles(ex)
    return {
        "tokens": [vocab.token_str(t) for t in ex.tokens], "roles": roles, "answer": vocab.token_str(ex.answer),
        "pred": vocab.token_str(int(probs.argmax())), "correct": int(probs.argmax()) == ex.answer,
        "p_answer": float(probs[ex.answer]),
        "top_k": [(vocab.token_str(int(i)), float(v)) for v, i in zip(top.values, top.indices)],
        "attn": attn, "scores": scores, "logit_lens": lens, "meta": ex.public_meta(),
    }


# ----------------------------------------------------------------------------- batched role statistics
ROLE_GROUPS = ("bos", "evidence_key", "evidence_value", "distractor_key", "distractor_value", "lure_key",
               "lure_filler", "filler", "query_marker", "query_key", "ans", "target_link_src",
               "target_link_arrow", "target_link_dst", "link_src", "link_arrow", "link_dst")


@torch.no_grad()
def attention_role_profile(model, examples: list[Example], batch_size: int = 128) -> pd.DataFrame:
    """For each example x layer x head: attention mass from the <ans> position
    to each role, plus pre-softmax scores to the evidence value and to the best
    competing distractor value (the *score gap*), and the number of attended
    positions (softmax dilution grows with the number of competitors)."""
    rows = []
    by_len: dict = {}
    for e in examples:
        by_len.setdefault(len(e.tokens), []).append(e)
    for group in by_len.values():
        for s in range(0, len(group), batch_size):
            exs = group[s:s + batch_size]
            b = collate(exs)
            logits, cache = model.run_with_cache(b["tokens"])
            pred = logits[:, -1].argmax(-1)
            for i, ex in enumerate(exs):
                roles = np.array(position_roles(ex))
                ap = ex.ans_pos
                for l in range(model.cfg.n_layers):
                    A = cache[f"L{l}.attn.probs"][i, :, ap].numpy()     # (H, T)
                    S = cache[f"L{l}.attn.scores"][i, :, ap].numpy()
                    for h in range(A.shape[0]):
                        row = {"ex": id(ex), "layer": l, "head": h, "correct": float(pred[i] == ex.answer),
                               **{k: v for k, v in ex.public_meta().items()
                                  if k in ("seq_len", "distance", "evidence_norm_pos", "n_pairs", "n_lures",
                                           "hops", "query_type", "evidence_offset")}}
                        for r in set(roles):
                            row[f"attn_{r}"] = float(A[h, roles == r].sum())
                        ev = roles == "evidence_value"
                        dv = roles == "distractor_value"
                        if ev.any():
                            row["score_evidence_value"] = float(S[h, ev].max())
                            row["score_best_distractor_value"] = float(S[h, dv].max()) if dv.any() else np.nan
                            row["score_gap"] = row["score_evidence_value"] - row["score_best_distractor_value"]
                            ek = roles == "evidence_key"
                            row["score_evidence_key"] = float(S[h, ek].max())
                        row["attn_entropy"] = float(-(A[h] * np.log(A[h] + 1e-12)).sum())
                        rows.append(row)
    df = pd.DataFrame(rows)
    for r in ROLE_GROUPS:
        c = f"attn_{r}"
        if c in df:
            df[c] = df[c].fillna(0.0)
    return df


@torch.no_grad()
def logit_lens(model, examples: list[Example], batch_size: int = 128) -> pd.DataFrame:
    """P(answer) decoded from the residual stream at <ans> after each layer
    (using the final LayerNorm and unembedding). Intermediate decodings are only
    indicative: earlier layers were never trained to be read this way."""
    rows = []
    by_len: dict = {}
    for e in examples:
        by_len.setdefault(len(e.tokens), []).append(e)
    for group in by_len.values():
        for s in range(0, len(group), batch_size):
            exs = group[s:s + batch_size]
            b = collate(exs)
            _, cache = model.run_with_cache(b["tokens"])
            ans = b["answers"]
            for l in range(model.cfg.n_layers):
                r = cache[f"L{l}.resid_post"][:, -1]
                p = torch.softmax(model.unembed(model.ln_f(r)), -1)
                pa = p[torch.arange(len(exs)), ans]
                ok = p.argmax(-1) == ans
                for i, ex in enumerate(exs):
                    rows.append({"layer": l, "p_answer": float(pa[i]), "correct_at_layer": float(ok[i]),
                                 "seq_len": ex.meta["seq_len"], "distance": ex.meta.get("distance")})
    return pd.DataFrame(rows)


@torch.no_grad()
def evidence_sweep(model, ex: Example, offsets=None, layer: int | None = None) -> pd.DataFrame:
    """Controlled sensitivity: keep the context content fixed, move only the
    evidence unit across offsets, and record prediction, P(answer), attention
    from <ans> to the evidence value per head, and the cosine similarity of the
    final <ans> residual to its value at the original offset."""
    assert ex.meta["task"] == "recall"
    C, k = ex.meta["context_len"], ex.meta["key_len"]
    offsets = offsets if offsets is not None else list(range(0, C - k, max(1, (C - k) // 24)))
    layer = model.cfg.n_layers - 1 if layer is None else layer
    variants = [move_evidence(ex, o) for o in offsets]
    b = collate([ex] + variants)
    logits, cache = model.run_with_cache(b["tokens"])
    ref = cache[f"L{model.cfg.n_layers - 1}.resid_post"][0, -1]
    rows = []
    for i, v in enumerate(variants, start=1):
        p = torch.softmax(logits[i, -1], -1)
        vp = v.meta["evidence_value_pos"]
        A = cache[f"L{layer}.attn.probs"][i, :, -1, vp]
        resid = cache[f"L{model.cfg.n_layers - 1}.resid_post"][i, -1]
        row = {"evidence_offset": v.meta["evidence_offset"], "distance": v.meta["distance"],
               "evidence_norm_pos": v.meta["evidence_norm_pos"], "p_answer": float(p[ex.answer]),
               "correct": float(p.argmax() == ex.answer),
               "resid_cos_to_original": float(F.cosine_similarity(resid, ref, dim=0))}
        for h in range(A.shape[0]):
            row[f"attn_ev_value_L{layer}H{h}"] = float(A[h])
        rows.append(row)
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- positional structure
@torch.no_grad()
def positional_structure(model, max_pos: int = 256) -> dict:
    """Method-specific view of what position information the model has.

    learned / sinusoidal : cosine-similarity matrix of the positional vectors
                           and their norms (untrained rows of a learned table
                           stay at initialisation).
    t5_relative          : learned bias per head as a function of distance.
    alibi                : fixed linear bias per head.
    rope                 : expected q.k for identical random q = k as a function
                           of relative distance ("long-term decay", Su et al.).
    """
    pos = model.pos
    name = pos.name
    out = {"method": name}
    if name in ("learned", "sinusoidal"):
        n = min(max_pos, getattr(pos, "max_positions", max_pos))
        P = pos.input_embedding(torch.arange(n))
        Pn = F.normalize(P, dim=-1)
        out["cos_sim"] = (Pn @ Pn.T).numpy()
        out["norms"] = P.norm(dim=-1).numpy()
    elif name == "t5_relative":
        out["bias_by_distance"] = pos.bias_by_distance(max_pos).numpy()
    elif name == "alibi":
        out["bias_by_distance"] = (-pos.slopes[:, None] * torch.arange(max_pos)[None].float()).numpy()
    elif name == "rope":
        from ..positional import apply_rope, rope_cos_sin
        dh = model.cfg.head_dim
        g = torch.Generator().manual_seed(0)
        x = torch.randn(512, dh, generator=g)
        cos, sin = rope_cos_sin(torch.arange(max_pos), dh, pos.base, pos.scale)
        k_rot = apply_rope(x[:, None, :], cos[None], sin[None])        # (N, P, dh) keys at positions
        q0 = apply_rope(x[:, None, :], cos[:1][None], sin[:1][None])   # query at position 0
        out["mean_qk_by_distance"] = (k_rot * q0).sum(-1).mean(0).numpy() / dh
    return out
