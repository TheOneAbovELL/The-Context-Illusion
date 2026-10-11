"""Positional representations behind one interface (see ``base.py``)."""

from .absolute import LearnedAbsolute, Sinusoidal, sinusoidal_table
from .base import NoPositional, PositionalScheme, PositionOverflowError
from .relative import ALiBi, T5RelativeBias, alibi_slopes, t5_relative_bucket
from .rope import RoPE, apply_rope, rope_cos_sin

METHODS = ("none", "learned", "sinusoidal", "t5_relative", "alibi", "rope")


def build_positional(cfg) -> PositionalScheme:
    """Factory from a :class:`context_lab.models.ModelConfig`."""
    m = cfg.pos_method
    if m == "none":
        return NoPositional()
    if m == "learned":
        return LearnedAbsolute(cfg.d_model, cfg.max_positions, init_std=cfg.pos_init_std)
    if m == "sinusoidal":
        scale = cfg.sinusoidal_scale if cfg.sinusoidal_scale is not None else cfg.tok_init_std * 2 ** 0.5
        return Sinusoidal(cfg.d_model, base=cfg.sinusoidal_base, scale=scale)
    if m == "t5_relative":
        return T5RelativeBias(cfg.n_heads, cfg.rel_num_buckets, cfg.rel_max_distance)
    if m == "alibi":
        return ALiBi(cfg.n_heads)
    if m == "rope":
        return RoPE(cfg.d_model // cfg.n_heads, base=cfg.rope_base, scale=cfg.rope_scale)
    raise ValueError(f"unknown positional method {m!r}; choose from {METHODS}")


__all__ = [
    "ALiBi", "LearnedAbsolute", "METHODS", "NoPositional", "PositionOverflowError",
    "PositionalScheme", "RoPE", "Sinusoidal", "T5RelativeBias", "alibi_slopes",
    "apply_rope", "build_positional", "rope_cos_sin", "sinusoidal_table", "t5_relative_bucket",
]
