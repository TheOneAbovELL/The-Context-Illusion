import sys; sys.path.insert(0, r"C:/Users/omjee/OneDrive/Desktop/PROJECTS/The Context Illusion/src")
from context_lab.models import ModelConfig
from context_lab.data import TaskConfig
from context_lab.training import TrainConfig, train_model
tag = sys.argv[1]
base = dict(seq_len=(24, 40), n_queries="all", single_query_prob=0.25, query_format="ans_marker")
cfgs = {"Q1_dense": TaskConfig(fill_pairs=True, **base),
        "Q2_fillers": TaskConfig(n_pairs=(2, 6), **base)}
mc = ModelConfig(pos_method="rope")
tr = TrainConfig(steps=1000, lr=3e-3, warmup_steps=100, eval_every=200, log_every=200, threads=2, val_examples=256)
train_model(mc, cfgs[tag], tr, log_fn=lambda r: print(tag, r["step"], f"loss={r['train_loss']:.3f} acc={r['train_acc']:.3f} val={r['val_acc']:.3f} t={r['elapsed_s']:.0f}", flush=True))
