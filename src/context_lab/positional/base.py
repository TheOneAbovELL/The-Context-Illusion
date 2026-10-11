"""Common interface for positional representations.

A positional scheme can influence the model at exactly three points, and every
scheme implements all three (returning ``None`` / identity when unused):

1. ``input_embedding(positions)``  -> (T, d_model) added to token embeddings
   (learned absolute, sinusoidal).
2. ``rotate_qk(q, k, positions)``  -> rotated (q, k) inside every attention layer
   (RoPE).
3. ``attention_bias(q_pos, k_pos)`` -> (H, Tq, Tk) additive bias on the attention
   logits before the softmax (T5 relative bias, ALiBi).

Keeping the three entry points explicit means the attention implementation is
identical for every method; only the positional scheme changes. That is the
main fairness control of the positional-encoding comparison.

``positions`` is always a 1-D LongTensor of absolute positions
(``pos_offset + arange(T)``). Methods that are translation invariant
(RoPE, relative bias, ALiBi, NoPE) must produce identical attention logits for
any offset; this is checked in ``tests/unit/test_positional.py``.
"""

from __future__ import annotations

import torch
from torch import nn


class PositionOverflowError(ValueError):
    """Raised when a scheme with a finite position table is asked for a position
    outside of it. We never silently clamp or wrap."""


class PositionalScheme(nn.Module):
    name: str = "base"
    #: True if the attention logits depend only on (query_pos - key_pos)
    translation_invariant: bool = False

    def input_embedding(self, positions: torch.Tensor) -> torch.Tensor | None:  # (T,) -> (T, d)
        return None

    def rotate_qk(self, q: torch.Tensor, k: torch.Tensor, positions: torch.Tensor):
        return q, k

    def attention_bias(self, q_pos: torch.Tensor, k_pos: torch.Tensor) -> torch.Tensor | None:
        return None

    def describe(self) -> dict:
        return {"name": self.name, "translation_invariant": self.translation_invariant,
                "n_params": sum(p.numel() for p in self.parameters())}


class NoPositional(PositionalScheme):
    """NoPE: no explicit positional information. A causal decoder can still
    infer some position information from the causal mask (e.g. by attending
    uniformly to all previous tokens), see Haviv et al. 2022 / Kazemnejad et
    al. 2023. Used here as a control."""

    name = "none"
    translation_invariant = True
