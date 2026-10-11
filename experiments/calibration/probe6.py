"""Main-task pilot with 2 heads (d_h = 32): dense training queries, <ans> format."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from context_lab.models import ModelConfig  # noqa: E402
from context_lab.data import TaskConfig  # noqa: E402
from context_lab.training import TrainConfig, train_model  # noqa: E402
tag, pm, heads, steps = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
tc = TaskConfig(seq_len=(24, 64), n_pairs=(2, 8), n_lures=(0, 1), lure_prob=0.25, n_queries="all",
                single_query_prob=0.25, query_format="ans_marker")
mc = ModelConfig(pos_method=pm, n_heads=heads)
tr = TrainConfig(steps=steps, lr=3e-3, warmup_steps=100, eval_every=250, log_every=250, threads=2, val_examples=256)
train_model(mc, tc, tr, log_fn=lambda r: print(tag, r["step"], f"loss={r['train_loss']:.3f} acc={r['train_acc']:.3f} "
                                                f"val={r['val_acc']:.3f} t={r['elapsed_s']:.0f}", flush=True))
