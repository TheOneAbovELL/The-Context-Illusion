import sys; sys.path.insert(0, r"C:/Users/omjee/OneDrive/Desktop/PROJECTS/The Context Illusion/src")
from context_lab.models import ModelConfig
from context_lab.data import TaskConfig
from context_lab.training import TrainConfig, train_model
pm, layers, steps = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
mc = ModelConfig(pos_method=pm, n_layers=layers, tok_init_std=1.0, pos_init_std=0.5, sinusoidal_scale=1.0)
tc = TaskConfig(seq_len=(24, 64), n_pairs=(2, 8), n_lures=(0, 1), lure_prob=0.25, query_format="ans_marker")
tr = TrainConfig(steps=steps, eval_every=250, log_every=250, threads=2, val_examples=256)
def log(r): print(pm, layers, r["step"], f"loss={r['train_loss']:.3f} acc={r['train_acc']:.3f} val={r['val_acc']:.3f} t={r['elapsed_s']:.0f}s", flush=True)
m, h, s = train_model(mc, tc, tr, log_fn=log)
print("SUMMARY", pm, layers, s, flush=True)
