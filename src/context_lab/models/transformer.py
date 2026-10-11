"""A small, fully instrumentable decoder-only Transformer (pre-LayerNorm).

Notation (shapes):
    B batch, T sequence length, D = d_model, H heads, d_h = D / H, V vocab.

Forward pass:
    x_0 = E[tokens] (+ P[positions] for additive schemes)            (B, T, D)
    for each layer l:
        a   = LN_1(x)                                                 (B, T, D)
        q,k,v = a W_Q, a W_K, a W_V  -> reshape to (B, H, T, d_h)
        q,k = rotate(q, k)              (RoPE only)
        S   = q k^T / sqrt(d_h) + bias  (relative/ALiBi only)          (B, H, T, T)
        S[i, j] = -inf for j > i        (causal mask)
        A   = softmax(S, dim=-1)                                       (B, H, T, T)
        z   = A v                                                      (B, H, T, d_h)
        x   = x + concat_h(z) W_O                                      (B, T, D)
        x   = x + W_2 GELU(W_1 LN_2(x))                                (B, T, D)
    logits = LN_f(x) W_U                                               (B, T, V)

Instrumentation: every named intermediate passes through ``self._hook(name, t)``.
Pass ``hooks={name: fn}`` to ``forward`` to read or *replace* an activation
(``fn(t) -> t' or None``), and ``cache={}`` to have detached copies stored.
Hook names are listed in :data:`HOOK_POINTS`.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import torch
import torch.nn.functional as F
from torch import nn

from ..positional import build_positional

HOOK_POINTS = (
    "embed.tok", "embed.pos", "L{l}.resid_pre", "L{l}.attn.q", "L{l}.attn.k", "L{l}.attn.v",
    "L{l}.attn.scores", "L{l}.attn.probs", "L{l}.attn.z", "L{l}.attn.out", "L{l}.resid_mid",
    "L{l}.mlp.out", "L{l}.resid_post", "final.ln", "logits",
)


@dataclass
class ModelConfig:
    vocab_size: int = 134
    d_model: int = 64
    n_heads: int = 4
    n_layers: int = 2
    d_mlp: int = 256
    dropout: float = 0.0
    pos_method: str = "rope"          # none | learned | sinusoidal | t5_relative | alibi | rope
    max_positions: int = 512          # learned table size (hard limit, no silent extrapolation)
    pos_init_std: float = 0.02        # learned table init (= token init: matched scale)
    tok_init_std: float = 0.02        # GPT-2-style; 1.0 prevented learning to copy (docs/results.md §1)
    sinusoidal_base: float = 10000.0
    sinusoidal_scale: float | None = None   # None -> tok_init_std * sqrt(2): same RMS as token embeddings
    rel_num_buckets: int = 32
    rel_max_distance: int = 128
    rope_base: float = 10000.0
    rope_scale: float = 1.0
    ln_eps: float = 1e-5
    tie_embeddings: bool = False

    def __post_init__(self):
        if self.d_model % self.n_heads:
            raise ValueError("d_model must be divisible by n_heads")

    @property
    def head_dim(self) -> int:
        return self.d_model // self.n_heads

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ModelConfig":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class _HookCtx:
    def __init__(self, hooks=None, cache=None):
        self.hooks = hooks or {}
        self.cache = cache

    def __call__(self, name: str, t: torch.Tensor) -> torch.Tensor:
        fn = self.hooks.get(name)
        if fn is not None:
            out = fn(t)
            if out is not None:
                t = out
        if self.cache is not None:
            self.cache[name] = t.detach()
        return t


class CausalSelfAttention(nn.Module):
    def __init__(self, cfg: ModelConfig, layer: int):
        super().__init__()
        self.cfg, self.layer = cfg, layer
        D = cfg.d_model
        self.W_q = nn.Linear(D, D, bias=False)
        self.W_k = nn.Linear(D, D, bias=False)
        self.W_v = nn.Linear(D, D, bias=False)
        self.W_o = nn.Linear(D, D, bias=False)
        self.drop = nn.Dropout(cfg.dropout)

    def forward(self, x, pos_scheme, positions, causal_mask, hk: _HookCtx):
        B, T, D = x.shape
        H, dh, p = self.cfg.n_heads, self.cfg.head_dim, f"L{self.layer}.attn"
        q = self.W_q(x).view(B, T, H, dh).transpose(1, 2)   # (B, H, T, dh)
        k = self.W_k(x).view(B, T, H, dh).transpose(1, 2)
        v = self.W_v(x).view(B, T, H, dh).transpose(1, 2)
        q, k = pos_scheme.rotate_qk(q, k, positions)        # identity unless RoPE
        q, k, v = hk(f"{p}.q", q), hk(f"{p}.k", k), hk(f"{p}.v", v)
        scores = q @ k.transpose(-1, -2) / math.sqrt(dh)    # (B, H, T, T)
        bias = pos_scheme.attention_bias(positions, positions)
        if bias is not None:
            scores = scores + bias.unsqueeze(0)
        scores = scores.masked_fill(causal_mask, float("-inf"))
        scores = hk(f"{p}.scores", scores)                  # interventions may add -inf here
        probs = torch.softmax(scores, dim=-1)
        probs = hk(f"{p}.probs", probs)
        z = self.drop(probs) @ v                            # (B, H, T, dh)
        z = hk(f"{p}.z", z)
        out = self.W_o(z.transpose(1, 2).reshape(B, T, D))
        return hk(f"{p}.out", out)


class MLP(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.fc1 = nn.Linear(cfg.d_model, cfg.d_mlp)
        self.fc2 = nn.Linear(cfg.d_mlp, cfg.d_model)
        self.drop = nn.Dropout(cfg.dropout)

    def forward(self, x):
        return self.drop(self.fc2(F.gelu(self.fc1(x))))


class Block(nn.Module):
    def __init__(self, cfg: ModelConfig, layer: int):
        super().__init__()
        self.layer = layer
        self.ln1 = nn.LayerNorm(cfg.d_model, eps=cfg.ln_eps)
        self.attn = CausalSelfAttention(cfg, layer)
        self.ln2 = nn.LayerNorm(cfg.d_model, eps=cfg.ln_eps)
        self.mlp = MLP(cfg)

    def forward(self, x, pos_scheme, positions, causal_mask, hk):
        l = self.layer
        x = hk(f"L{l}.resid_pre", x)
        x = x + self.attn(self.ln1(x), pos_scheme, positions, causal_mask, hk)
        x = hk(f"L{l}.resid_mid", x)
        x = x + hk(f"L{l}.mlp.out", self.mlp(self.ln2(x)))
        return hk(f"L{l}.resid_post", x)


class Transformer(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.cfg = cfg
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.pos = build_positional(cfg)
        self.blocks = nn.ModuleList([Block(cfg, l) for l in range(cfg.n_layers)])
        self.ln_f = nn.LayerNorm(cfg.d_model, eps=cfg.ln_eps)
        self.unembed = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        self._init_weights()
        if cfg.tie_embeddings:
            self.unembed.weight = self.tok_emb.weight

    def _init_weights(self):
        resid_scale = 1.0 / math.sqrt(2 * self.cfg.n_layers)
        for name, p in self.named_parameters():
            if name.startswith("pos."):
                continue  # positional schemes initialise themselves
            if name == "tok_emb.weight":
                nn.init.normal_(p, std=self.cfg.tok_init_std)
            elif p.dim() == 2:
                std = 0.02 * (resid_scale if name.endswith(("W_o.weight", "fc2.weight")) else 1.0)
                nn.init.normal_(p, std=std)
            elif name.endswith("bias"):
                nn.init.zeros_(p)

    # ------------------------------------------------------------------ forward
    def forward(self, tokens: torch.Tensor, pos_offset: int = 0, hooks: dict | None = None,
                cache: dict | None = None) -> torch.Tensor:
        """tokens: (B, T) LongTensor -> logits (B, T, V).

        ``pos_offset`` shifts every absolute position (used to test translation
        invariance and to probe absolute-position effects without changing the
        content). Raises PositionOverflowError for learned tables if exceeded.
        """
        B, T = tokens.shape
        hk = _HookCtx(hooks, cache)
        positions = torch.arange(pos_offset, pos_offset + T, device=tokens.device)
        x = hk("embed.tok", self.tok_emb(tokens))
        pe = self.pos.input_embedding(positions)
        if pe is not None:
            x = x + hk("embed.pos", pe).unsqueeze(0)
        causal_mask = torch.ones(T, T, dtype=torch.bool, device=tokens.device).triu(1)
        for blk in self.blocks:
            x = blk(x, self.pos, positions, causal_mask, hk)
        x = hk("final.ln", self.ln_f(x))
        return hk("logits", self.unembed(x))

    def run_with_cache(self, tokens, pos_offset: int = 0, hooks=None):
        cache: dict = {}
        logits = self.forward(tokens, pos_offset=pos_offset, hooks=hooks, cache=cache)
        return logits, cache

    # ------------------------------------------------------------- utilities
    def lm_loss(self, tokens: torch.Tensor, loss_mask: torch.Tensor | None = None) -> torch.Tensor:
        """Standard next-token loss: predict tokens[:, t+1] from tokens[:, :t+1].
        ``loss_mask`` (B, T-1) selects which next-token predictions count."""
        logits = self.forward(tokens[:, :-1])
        tgt = tokens[:, 1:]
        ce = F.cross_entropy(logits.reshape(-1, logits.size(-1)), tgt.reshape(-1), reduction="none")
        ce = ce.view_as(tgt).float()
        if loss_mask is None:
            return ce.mean()
        m = loss_mask.float()
        return (ce * m).sum() / m.sum().clamp(min=1)

    @torch.no_grad()
    def generate(self, tokens: torch.Tensor, max_new_tokens: int = 1, greedy: bool = True,
                 temperature: float = 1.0, generator: torch.Generator | None = None) -> torch.Tensor:
        for _ in range(max_new_tokens):
            logits = self.forward(tokens)[:, -1] / temperature
            if greedy:
                nxt = logits.argmax(-1, keepdim=True)
            else:
                nxt = torch.multinomial(torch.softmax(logits, -1), 1, generator=generator)
            tokens = torch.cat([tokens, nxt], dim=1)
        return tokens

    def n_params(self, exclude_positional: bool = False) -> int:
        return sum(p.numel() for n, p in self.named_parameters()
                   if not (exclude_positional and n.startswith("pos.")))


def save_checkpoint(model: Transformer, path, extra: dict | None = None) -> None:
    payload = {"model_config": model.cfg.to_dict(), "state_dict": model.state_dict(), **(extra or {})}
    torch.save(payload, path)


def load_checkpoint(path, map_location="cpu") -> tuple[Transformer, dict]:
    payload = torch.load(path, map_location=map_location, weights_only=False)
    model = Transformer(ModelConfig.from_dict(payload["model_config"]))
    model.load_state_dict(payload["state_dict"])
    model.eval()
    return model, payload
