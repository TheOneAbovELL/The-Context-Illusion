import sys; sys.path.insert(0, r"C:/Users/omjee/OneDrive/Desktop/PROJECTS/The Context Illusion/src")
from context_lab.models import ModelConfig
from context_lab.data import TaskConfig
from context_lab.training import TrainConfig, train_model
tag = sys.argv[1]
cfgs = {
 "P1_short_2-4": (ModelConfig(pos_method="rope", tok_init_std=0.02), TaskConfig(seq_len=(16, 32), n_pairs=(2, 4), n_queries=(1, 4), query_format="ans_marker")),
 "P2_short_2-4_d128": (ModelConfig(pos_method="rope", d_model=128, d_mlp=512, tok_init_std=0.02), TaskConfig(seq_len=(16, 32), n_pairs=(2, 4), n_queries=(1, 4), query_format="ans_marker")),
}
mc, tc = cfgs[tag]
tr = TrainConfig(steps=1500, lr=3e-3, warmup_steps=100, eval_every=250, log_every=250, threads=2, val_examples=256)
train_model(mc, tc, tr, log_fn=lambda r: print(tag, r["step"], f"loss={r['train_loss']:.3f} val={r['val_acc']:.3f} t={r['elapsed_s']:.0f}", flush=True))
