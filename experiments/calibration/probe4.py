import sys; sys.path.insert(0, r"C:/Users/omjee/OneDrive/Desktop/PROJECTS/The Context Illusion/src")
from context_lab.models import ModelConfig
from context_lab.data import TaskConfig
from context_lab.training import TrainConfig, train_model
tag, fmt = sys.argv[1], sys.argv[2]
tc = TaskConfig(seq_len=(24, 64), n_pairs=(2, 8), n_lures=(0, 1), lure_prob=0.25, n_queries="all", single_query_prob=0.25, query_format=fmt)
mc = ModelConfig(pos_method="rope", tok_init_std=0.02, n_layers=int(sys.argv[3]))
tr = TrainConfig(steps=3000, lr=3e-3, warmup_steps=100, eval_every=250, log_every=250, threads=2, val_examples=256)
train_model(mc, tc, tr, log_fn=lambda r: print(tag, r["step"], f"loss={r['train_loss']:.3f} acc={r['train_acc']:.3f} val={r['val_acc']:.3f} t={r['elapsed_s']:.0f}", flush=True))
