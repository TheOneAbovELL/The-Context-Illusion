import math

import pytest
import torch

from context_lab.models import ModelConfig, Transformer
from context_lab.positional import (ALiBi, LearnedAbsolute, PositionOverflowError, RoPE, Sinusoidal, T5RelativeBias,
                                    alibi_slopes, apply_rope, rope_cos_sin, sinusoidal_table, t5_relative_bucket)

METHODS = ["none", "learned", "sinusoidal", "t5_relative", "alibi", "rope"]


def test_learned_shapes_and_overflow():
    pe = LearnedAbsolute(16, max_positions=10)
    assert pe.input_embedding(torch.arange(10)).shape == (10, 16)
    with pytest.raises(PositionOverflowError):
        pe.input_embedding(torch.arange(11))


def test_sinusoidal_matches_formula():
    d = 8
    pe = sinusoidal_table(torch.arange(5), d)
    for t in range(5):
        for i in range(d // 2):
            ang = t / (10000 ** (2 * i / d))
            assert pe[t, 2 * i].item() == pytest.approx(math.sin(ang), abs=1e-6)
            assert pe[t, 2 * i + 1].item() == pytest.approx(math.cos(ang), abs=1e-6)
    assert Sinusoidal(d).input_embedding(torch.arange(1000)).shape == (1000, d)  # no overflow


def test_rope_preserves_norm_and_is_relative():
    torch.manual_seed(0)
    dh = 16
    q, k = torch.randn(dh), torch.randn(dh)

    def score(m, n):
        cm, sm = rope_cos_sin(torch.tensor([m]), dh)
        cn, sn = rope_cos_sin(torch.tensor([n]), dh)
        return (apply_rope(q[None], cm, sm) * apply_rope(k[None], cn, sn)).sum().item()

    assert score(3, 1) == pytest.approx(score(103, 101), abs=1e-4)
    assert score(10, 0) == pytest.approx(score(50, 40), abs=1e-4)
    assert score(10, 0) != pytest.approx(score(11, 0), abs=1e-4)
    cos, sin = rope_cos_sin(torch.arange(7), dh)
    x = torch.randn(7, dh)
    assert torch.allclose(apply_rope(x, cos, sin).norm(dim=-1), x.norm(dim=-1), atol=1e-5)
    # position 0 is the identity rotation
    c0, s0 = rope_cos_sin(torch.tensor([0]), dh)
    assert torch.allclose(apply_rope(x[:1], c0, s0), x[:1])


def test_rope_module_shapes():
    r = RoPE(8)
    q = torch.randn(2, 3, 5, 8)
    q2, k2 = r.rotate_qk(q, q.clone(), torch.arange(5))
    assert q2.shape == q.shape and k2.shape == q.shape


def test_t5_buckets_monotone_and_clamped():
    n = torch.arange(0, 400)
    b = t5_relative_bucket(n, num_buckets=32, max_distance=128)
    assert (b[1:] >= b[:-1]).all()
    assert b[:16].tolist() == list(range(16))          # exact region
    assert b.max().item() == 31
    assert (b[128:] == 31).all()                       # every distance >= max_distance shares the last bucket
    assert t5_relative_bucket(torch.tensor([-5]), 32, 128).item() == 0


def test_t5_bias_shape():
    m = T5RelativeBias(n_heads=4)
    pos = torch.arange(6)
    assert m.attention_bias(pos, pos).shape == (4, 6, 6)


def test_alibi():
    s = alibi_slopes(4)
    assert torch.allclose(s, torch.tensor([2 ** -2, 2 ** -4, 2 ** -6, 2 ** -8]))
    assert len(alibi_slopes(6)) == 6
    b = ALiBi(4).attention_bias(torch.arange(5), torch.arange(5))
    assert b.shape == (4, 5, 5)
    assert b[0, 4, 0].item() == pytest.approx(-4 * 0.25)
    assert b[0, 2, 2].item() == 0.0


@pytest.mark.parametrize("method", METHODS)
def test_translation_invariance_of_full_model(method):
    """Shifting every absolute position must not change the output of
    translation-invariant schemes; absolute schemes must change."""
    torch.manual_seed(0)
    cfg = ModelConfig(pos_method=method, d_model=32, n_heads=4, n_layers=2, d_mlp=64, max_positions=256)
    model = Transformer(cfg).eval()
    if method == "t5_relative":
        torch.nn.init.normal_(model.pos.bias.weight)  # non-trivial bias
    x = torch.randint(6, 100, (2, 20))
    with torch.no_grad():
        a = model(x)
        b = model(x, pos_offset=50)
    same = torch.allclose(a, b, atol=1e-4)
    assert same == model.pos.translation_invariant, method


def test_learned_model_refuses_overflow():
    model = Transformer(ModelConfig(pos_method="learned", max_positions=16, d_model=16, n_heads=2, d_mlp=32))
    with pytest.raises(PositionOverflowError):
        model(torch.zeros(1, 17, dtype=torch.long))
    model(torch.zeros(1, 16, dtype=torch.long))
