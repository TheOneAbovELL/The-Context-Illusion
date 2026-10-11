import sys; sys.path.insert(0, r"C:/Users/omjee/OneDrive/Desktop/PROJECTS/The Context Illusion/src")
import torch
from context_lab.models import ModelConfig, save_checkpoint
from context_lab.data import TaskConfig, make_dataset
from context_lab.training import TrainConfig, train_model
from context_lab.evaluation import predict, accuracy_table
from context_lab.diagnostics import attention_role_profile
mc = ModelConfig(pos_method="rope", n_layers=2, tok_init_std=0.02)
tc = TaskConfig(seq_len=(24, 64), n_pairs=(2, 8), n_lures=(0, 1), lure_prob=0.25, n_queries=(1, 4), query_format="ans_marker")
tr = TrainConfig(steps=1500, lr=3e-3, warmup_steps=100, eval_every=500, log_every=500, threads=2, val_examples=256)
m, h, s = train_model(mc, tc, tr, log_fn=lambda r: print(r["step"], round(r["val_acc"], 3), flush=True))
save_checkpoint(m, "diag_model.pt")
ev = make_dataset(tc.replace(n_queries=1), 2000, 99, "diag")
df = predict(m, ev)
df["dist_bin"] = (df["distance"] // 10) * 10
for col in ["n_pairs", "n_lures", "dist_bin", "seq_len"]:
    t = accuracy_table(df, [col])[[col, "n", "acc"]]
    print(t.to_string(index=False))
prof = attention_role_profile(m, ev[:300])
cols = [c for c in prof.columns if c.startswith("attn_")]
print(prof.groupby(["layer", "head"])[cols].mean().round(3).T.to_string())
