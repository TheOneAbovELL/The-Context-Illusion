import sys; sys.path.insert(0, r"C:/Users/omjee/OneDrive/Desktop/PROJECTS/The Context Illusion/src")
from context_lab.models import ModelConfig
from context_lab.data import TaskConfig
from context_lab.training import TrainConfig, train_model
tag = sys.argv[1]
cfgs = {
 "P3_short_keylast": TaskConfig(seq_len=(16, 32), n_pairs=(2, 4), n_queries=(1, 4), query_format="key_last"),
 "P4_main_keylast": TaskConfig(seq_len=(24, 64), n_pairs=(2, 8), n_lures=(0, 1), lure_prob=0.25, n_queries=(1, 4), query_format="key_last"),
}
mc = ModelConfig(pos_method="rope", tok_init_std=0.02)
tr = TrainConfig(steps=int(sys.argv[2]), lr=3e-3, warmup_steps=100, eval_every=250, log_every=250, threads=2, val_examples=256)
train_model(mc, cfgs[tag], tr, log_fn=lambda r: print(tag, r["step"], f"loss={r['train_loss']:.3f} val={r['val_acc']:.3f} t={r['elapsed_s']:.0f}", flush=True))
