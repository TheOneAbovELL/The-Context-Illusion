import pytest

from context_lab.data import TaskConfig
from context_lab.models import ModelConfig
from context_lab.training import TrainConfig, train_model

EASY_TASK = TaskConfig(seq_len=(12, 24), n_pairs=1)   # one association: "copy the only value"


@pytest.fixture(scope="session")
def tiny_trained():
    """A tiny model trained on an easy task so behavioural tests have a model
    that actually solves something. ~20-60 s on CPU."""
    mc = ModelConfig(pos_method="rope", d_model=32, n_heads=2, n_layers=2, d_mlp=64, max_positions=128)
    tr = TrainConfig(steps=300, batch_size=32, lr=3e-3, warmup_steps=30, eval_every=100, log_every=100,
                     val_examples=128, seed=0)
    model, hist, summ = train_model(mc, EASY_TASK, tr)
    return model, EASY_TASK, hist, summ
