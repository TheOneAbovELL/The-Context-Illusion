"""Rotary positional embeddings (Su et al., 2021, RoFormer).

For a head dimension d_h (even), split each query/key vector into d_h/2 2-D
planes and rotate plane i at position m by the angle m * theta_i with
theta_i = base^{-2i/d_h}:

    [x'_a]   [cos(m θ_i)  -sin(m θ_i)] [x_a]
    [x'_b] = [sin(m θ_i)   cos(m θ_i)] [x_b]

Because rotations are orthogonal and R(mθ)^T R(nθ) = R((n - m)θ),

    <R_m q, R_n k> = <q, R_{n-m} k>,

so the attention logit depends on positions only through n - m.
Values are *not* rotated, so the residual stream carries no explicit position.

Pairing convention: we use the "rotate-half" layout (plane i = dims (i, i + d_h/2)),
as in GPT-NeoX/LLaMA implementations. The interleaved layout of the original
paper (plane i = dims (2i, 2i+1)) is equivalent up to a fixed permutation of
the head dimensions, which the learned W_Q/W_K absorb.

Shapes: q, k: (B, H, T, d_h); positions: (T,).
"""

from __future__ import annotations

import torch

from .base import PositionalScheme


def rotate_half(x: torch.Tensor) -> torch.Tensor:
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)


def rope_cos_sin(positions: torch.Tensor, head_dim: int, base: float = 10000.0, scale: float = 1.0):
    """Return cos, sin of shape (T, head_dim). ``scale`` < 1 implements linear
    position interpolation (Chen et al., 2023); default 1.0 = plain RoPE."""
    inv_freq = base ** (-torch.arange(0, head_dim, 2, dtype=torch.float32) / head_dim)  # (d_h/2,)
    angles = (positions.float() * scale)[:, None] * inv_freq[None, :]                   # (T, d_h/2)
    angles = torch.cat((angles, angles), dim=-1)                                        # (T, d_h)
    return angles.cos(), angles.sin()


def apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    return x * cos + rotate_half(x) * sin


class RoPE(PositionalScheme):
    name = "rope"
    translation_invariant = True

    def __init__(self, head_dim: int, base: float = 10000.0, scale: float = 1.0):
        super().__init__()
        assert head_dim % 2 == 0, "RoPE needs an even head dimension"
        self.head_dim, self.base, self.scale = head_dim, base, scale

    def rotate_qk(self, q, k, positions):
        cos, sin = rope_cos_sin(positions, self.head_dim, self.base, self.scale)
        cos, sin = cos.to(q.dtype), sin.to(q.dtype)
        return apply_rope(q, cos, sin), apply_rope(k, cos, sin)

    def describe(self) -> dict:
        return {**super().describe(), "base": self.base, "scale": self.scale}
