"""Absolute positional representations added to the token embeddings.

Learned:     x_t = E[token_t] + P[t],  P in R^{max_positions x d} (trainable)
Sinusoidal:  x_t = E[token_t] + PE(t), PE(t)_{2i} = sin(t / 10000^{2i/d}),
                                       PE(t)_{2i+1} = cos(t / 10000^{2i/d})
"""

from __future__ import annotations

import torch
from torch import nn

from .base import PositionalScheme, PositionOverflowError


class LearnedAbsolute(PositionalScheme):
    """Trainable lookup table with a hard maximum.

    Positions >= ``max_positions`` raise :class:`PositionOverflowError`.
    Rows that are inside the table but were never seen in training keep their
    random initialisation (embeddings are excluded from weight decay in the
    trainer, so they are not even shrunk). The evaluator therefore reports
    which evaluation positions were never trained (``trained_max_position``).
    """

    name = "learned"
    translation_invariant = False

    def __init__(self, d_model: int, max_positions: int, init_std: float = 0.02):
        super().__init__()
        self.max_positions = max_positions
        self.table = nn.Embedding(max_positions, d_model)
        nn.init.normal_(self.table.weight, std=init_std)

    def input_embedding(self, positions: torch.Tensor) -> torch.Tensor:
        hi = int(positions.max())
        if hi >= self.max_positions:
            raise PositionOverflowError(
                f"learned absolute embedding has {self.max_positions} rows; "
                f"position {hi} requested. Refusing to extrapolate silently.")
        return self.table(positions)


def sinusoidal_table(positions: torch.Tensor, d_model: int, base: float = 10000.0) -> torch.Tensor:
    """(T,) -> (T, d_model). Interleaved sin/cos as in Vaswani et al. (2017)."""
    half = d_model // 2
    inv_freq = base ** (-torch.arange(half, dtype=torch.float32) * 2.0 / d_model)  # (d/2,)
    angles = positions.float()[:, None] * inv_freq[None, :]                    # (T, d/2)
    pe = torch.zeros(positions.shape[0], d_model)
    pe[:, 0::2] = torch.sin(angles)
    pe[:, 1::2] = torch.cos(angles[:, : d_model - half])
    return pe


class Sinusoidal(PositionalScheme):
    """Fixed sinusoidal encoding; defined for every integer position, so there
    is no overflow, but positions beyond training are still *unseen inputs*."""

    name = "sinusoidal"
    translation_invariant = False

    def __init__(self, d_model: int, base: float = 10000.0, scale: float = 1.0):
        super().__init__()
        self.d_model, self.base, self.scale = d_model, base, scale

    def input_embedding(self, positions: torch.Tensor) -> torch.Tensor:
        return self.scale * sinusoidal_table(positions, self.d_model, self.base).to(positions.device)

    def describe(self) -> dict:
        return {**super().describe(), "base": self.base, "scale": self.scale}
