"""Which factor of the main training distribution slows learning? (RoPE, 2 heads, 2000 steps)
Reference: study_fillers (fixed len, 4 pairs, all queried, no lures) learns by ~900 steps;
P8 (main distribution) reached 0.45 at 2000 steps."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from context_lab.models import ModelConfig  # noqa: E402
from context_lab.data import TaskConfig  # noqa: E402
from context_lab.training import TrainConfig, train_model  # noqa: E402
tag = sys.argv[1]
common = dict(n_queries="all", single_query_prob=0.25, query_format="ans_marker")
cfgs = {
    "B_varlen_4pairs_nolure": TaskConfig(seq_len=(24, 64), n_pairs=4, n_lures=0, **common),
    "C_len48_2to8pairs_lures": TaskConfig(seq_len=48, n_pairs=(2, 8), n_lures=(0, 1), lure_prob=0.25, **common),
    "D_varlen_4pairs_nolure_nosingle": TaskConfig(seq_len=(24, 64), n_pairs=4, n_lures=0, n_queries="all",
                                                  single_query_prob=0.0, query_format="ans_marker"),
}
tr = TrainConfig(steps=2000, lr=3e-3, warmup_steps=100, eval_every=250, log_every=250, threads=2, val_examples=256)
train_model(ModelConfig(pos_method="rope", n_heads=2), cfgs[tag], tr,
            log_fn=lambda r: print(tag, r["step"], f"val={r['val_acc']:.3f} t={r['elapsed_s']:.0f}", flush=True))
