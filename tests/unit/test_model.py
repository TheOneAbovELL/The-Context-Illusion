import pytest
import torch

from context_lab.models import HOOK_POINTS, ModelConfig, Transformer, load_checkpoint, save_checkpoint

METHODS = ["none", "learned", "sinusoidal", "t5_relative", "alibi", "rope"]


def small(method="rope", **kw):
    return ModelConfig(pos_method=method, d_model=32, n_heads=4, n_layers=2, d_mlp=64, max_positions=128, **kw)


@pytest.mark.parametrize("method", METHODS)
def test_shapes(method):
    m = Transformer(small(method))
    x = torch.randint(0, 134, (3, 17))
    assert m(x).shape == (3, 17, 134)


@pytest.mark.parametrize("method", METHODS)
def test_causal_mask(method):
    """Logits at position t must not depend on tokens after t."""
    torch.manual_seed(1)
    m = Transformer(small(method)).eval()
    x = torch.randint(6, 134, (2, 20))
    y = x.clone()
    y[:, 12:] = torch.randint(6, 134, (2, 8))
    with torch.no_grad():
        a, b = m(x), m(y)
    assert torch.allclose(a[:, :12], b[:, :12], atol=1e-5)
    assert not torch.allclose(a[:, 12:], b[:, 12:], atol=1e-5)


def test_attention_probabilities_are_causal_and_normalised():
    m = Transformer(small()).eval()
    _, cache = m.run_with_cache(torch.randint(6, 134, (2, 9)))
    for l in range(2):
        A = cache[f"L{l}.attn.probs"]
        assert A.shape == (2, 4, 9, 9)
        assert torch.allclose(A.sum(-1), torch.ones(2, 4, 9), atol=1e-5)
        assert torch.all(A.triu(1) == 0)


def test_all_hook_points_cached():
    m = Transformer(small("learned"))
    _, cache = m.run_with_cache(torch.randint(6, 134, (1, 5)))
    for hp in HOOK_POINTS:
        names = [hp.format(l=l) for l in range(2)] if "{l}" in hp else [hp]
        for n in names:
            assert n in cache, n


def test_hook_can_replace_activation():
    m = Transformer(small()).eval()
    x = torch.randint(6, 134, (1, 8))
    base = m(x)
    out = m(x, hooks={"L1.resid_post": lambda t: torch.zeros_like(t)})
    assert not torch.allclose(base, out)
    # zeroed final residual -> LayerNorm(0) = bias -> identical logits at every position
    assert torch.allclose(out[0, 0], out[0, -1], atol=1e-5)


@pytest.mark.parametrize("method", METHODS)
def test_gradient_flow(method):
    torch.manual_seed(0)
    m = Transformer(small(method))
    if method == "t5_relative":
        torch.nn.init.normal_(m.pos.bias.weight)
    x = torch.randint(6, 134, (2, 10))
    m.lm_loss(x).backward()
    for name, p in m.named_parameters():
        if name == "pos.table.weight":       # only used rows receive gradient
            assert p.grad[:9].abs().sum() > 0 and p.grad[9:].abs().sum() == 0
            continue
        if name == "tok_emb.weight":
            assert p.grad.abs().sum() > 0
            continue
        assert p.grad is not None and torch.isfinite(p.grad).all(), name
        assert p.grad.abs().sum() > 0, name


@pytest.mark.parametrize("method", METHODS)
def test_checkpoint_roundtrip(tmp_path, method):
    m = Transformer(small(method)).eval()
    x = torch.randint(6, 134, (2, 11))
    save_checkpoint(m, tmp_path / "m.pt", extra={"note": "x"})
    m2, payload = load_checkpoint(tmp_path / "m.pt")
    assert payload["note"] == "x"
    with torch.no_grad():
        assert torch.equal(m(x), m2(x))


def test_deterministic_init_and_eval():
    torch.manual_seed(5)
    a = Transformer(small())
    torch.manual_seed(5)
    b = Transformer(small())
    x = torch.randint(6, 134, (2, 7))
    with torch.no_grad():
        assert torch.equal(a.eval()(x), b.eval()(x))
        assert torch.equal(a(x), a(x))


def test_generate_and_param_count():
    m = Transformer(small("learned"))
    out = m.generate(torch.randint(6, 134, (1, 4)), max_new_tokens=3)
    assert out.shape == (1, 7)
    assert m.n_params() - m.n_params(exclude_positional=True) == 128 * 32


def test_bad_config():
    with pytest.raises(ValueError):
        ModelConfig(d_model=30, n_heads=4)
    with pytest.raises(ValueError):
        Transformer(ModelConfig(pos_method="nonsense"))
