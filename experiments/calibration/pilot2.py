import sys, json; sys.path.insert(0, r"C:/Users/omjee/OneDrive/Desktop/PROJECTS/The Context Illusion/src")
from context_lab.models import ModelConfig
from context_lab.data import TaskConfig
from context_lab.training import TrainConfig, train_model
tag, pm, lr, nq, steps = sys.argv[1], sys.argv[2], float(sys.argv[3]), json.loads(sys.argv[4]), int(sys.argv[5])
mc = ModelConfig(pos_method=pm, n_layers=2, tok_init_std=1.0, pos_init_std=0.5, sinusoidal_scale=1.0)
tc = TaskConfig(seq_len=(24, 64), n_pairs=(2, 8), n_lures=(0, 1), lure_prob=0.25, n_queries=nq, query_format="ans_marker")
tr = TrainConfig(steps=steps, lr=lr, eval_every=250, log_every=250, threads=2, val_examples=256, warmup_steps=100)
def log(r): print(tag, r["step"], f"loss={r['train_loss']:.3f} acc={r['train_acc']:.3f} val={r['val_acc']:.3f} t={r['elapsed_s']:.0f}s", flush=True)
m, h, s = train_model(mc, tc, tr, log_fn=log)
print("SUMMARY", tag, s, flush=True)
