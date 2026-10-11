"""Relative-position attention biases.

Both methods add a scalar b_h(i - j) to the attention logit of head h for query
position i and key position j; the value path and the residual stream receive
no positional signal at all.

T5 bucketed bias (Raffel et al., 2020)
--------------------------------------
For a causal model the relevant distance is n = i - j >= 0. Distances are
mapped to ``num_buckets`` buckets: the first ``num_buckets // 2`` buckets are
exact (n = 0, 1, ..., max_exact - 1); larger distances are bucketed
logarithmically up to ``max_distance``; *every distance >= max_distance shares
the last bucket*. Each (bucket, head) has one trainable scalar. The bias table
is shared across layers (as in T5). Extra cost: an (H, T, T) bias tensor per
forward pass, O(H T^2) memory -- the same order as the attention matrix itself.

Note: our implementation is the *unidirectional* variant (only n >= 0 is
meaningful because of the causal mask), so all ``num_buckets`` are spent on
non-negative distances.

ALiBi (Press et al., 2022)
--------------------------
b_h(i - j) = -m_h * (i - j) with fixed head-specific slopes
m_h = 2^{-8 h / H}, h = 1..H (geometric sequence for power-of-two H). No
trainable parameters.
"""

from __future__ import annotations

import math

import torch
from torch import nn

from .base import PositionalScheme


def t5_relative_bucket(distance: torch.Tensor, num_buckets: int, max_distance: int) -> torch.Tensor:
    """Map non-negative distances n = q_pos - k_pos to bucket ids (unidirectional T5).

    Negative distances (future keys, masked anyway) are mapped to bucket 0.
    """
    n = distance.clamp(min=0)
    max_exact = num_buckets // 2
    is_small = n < max_exact
    # log-spaced buckets in [max_exact, num_buckets - 1]
    n_f = n.float().clamp(min=1.0)
    val_if_large = max_exact + (
        torch.log(n_f / max_exact) / math.log(max_distance / max_exact) * (num_buckets - max_exact)
    ).long()
    val_if_large = val_if_large.clamp(max=num_buckets - 1)
    return torch.where(is_small, n, val_if_large)


class T5RelativeBias(PositionalScheme):
    name = "t5_relative"
    translation_invariant = True

    def __init__(self, n_heads: int, num_buckets: int = 32, max_distance: int = 128):
        super().__init__()
        assert max_distance > num_buckets // 2, "max_distance must exceed the exact-bucket range"
        self.n_heads, self.num_buckets, self.max_distance = n_heads, num_buckets, max_distance
        self.bias = nn.Embedding(num_buckets, n_heads)
        nn.init.zeros_(self.bias.weight)  # start position-agnostic

    def attention_bias(self, q_pos: torch.Tensor, k_pos: torch.Tensor) -> torch.Tensor:
        dist = q_pos[:, None] - k_pos[None, :]                            # (Tq, Tk)
        buckets = t5_relative_bucket(dist, self.num_buckets, self.max_distance)
        return self.bias(buckets).permute(2, 0, 1)                        # (H, Tq, Tk)

    def bias_by_distance(self, max_n: int) -> torch.Tensor:
        """(H, max_n) learned bias as a function of distance -- for diagnostics."""
        n = torch.arange(max_n)
        return self.bias(t5_relative_bucket(n, self.num_buckets, self.max_distance)).T

    def describe(self) -> dict:
        return {**super().describe(), "num_buckets": self.num_buckets, "max_distance": self.max_distance}


def alibi_slopes(n_heads: int) -> torch.Tensor:
    def pow2(n):
        start = 2 ** (-8.0 / n)
        return [start ** (i + 1) for i in range(n)]
    if math.log2(n_heads).is_integer():
        s = pow2(n_heads)
    else:  # recipe from the ALiBi reference implementation for non powers of two
        closest = 2 ** math.floor(math.log2(n_heads))
        s = pow2(closest) + pow2(2 * closest)[0::2][: n_heads - closest]
    return torch.tensor(s, dtype=torch.float32)


class ALiBi(PositionalScheme):
    name = "alibi"
    translation_invariant = True

    def __init__(self, n_heads: int):
        super().__init__()
        self.register_buffer("slopes", alibi_slopes(n_heads), persistent=False)

    def attention_bias(self, q_pos: torch.Tensor, k_pos: torch.Tensor) -> torch.Tensor:
        dist = (q_pos[:, None] - k_pos[None, :]).clamp(min=0).float()     # (Tq, Tk)
        return -self.slopes[:, None, None] * dist[None]                   # (H, Tq, Tk)

    def describe(self) -> dict:
        return {**super().describe(), "slopes": [round(float(s), 5) for s in self.slopes]}
