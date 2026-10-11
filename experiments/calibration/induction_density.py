"""Calibration control: how fast does this model learn *content-based* retrieval?

mode "fixed":    the second half repeats the first half in the same order. The
                 target is always 16 positions back -> solvable by position alone
                 (a flawed retrieval test; kept to document why).
mode "shuffled": the second half is a random permutation of the first half (distinct
                 tokens), so the next token can only be found by matching content
                 (classic induction: find my token earlier, copy its successor).
Loss on the last k positions.
Usage: python induction_density.py <mode> <k> [steps] [pos_method] [n_heads] [lr]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import torch  # noqa: E402
import torch.nn.functional as F  # noqa: E402

from context_lab.models import ModelConfig, Transformer  # noqa: E402

torch.set_num_threads(2)
mode, k = sys.argv[1], int(sys.argv[2])
steps = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
pm = sys.argv[4] if len(sys.argv) > 4 else "rope"
heads = int(sys.argv[5]) if len(sys.argv) > 5 else 4
lr = float(sys.argv[6]) if len(sys.argv) > 6 else 3e-3
torch.manual_seed(0)
m = Transformer(ModelConfig(pos_method=pm, n_heads=heads))
opt = torch.optim.AdamW(m.parameters(), lr)
accs = []
for s in range(steps):
    first = torch.stack([torch.randperm(64)[:16] + 22 for _ in range(32)])        # distinct tokens
    if mode == "fixed":
        second = first
    else:
        second = torch.stack([row[torch.randperm(16)] for row in first])
    x = torch.cat([torch.ones(32, 1, dtype=torch.long), first, second], 1)
    # target at second-half position p: the token that followed second[p] in the first half
    tgt_full = torch.zeros_like(second)
    for b in range(32):
        succ = {int(first[b, i]): int(first[b, i + 1]) for i in range(15)}
        for p in range(16):
            tgt_full[b, p] = succ.get(int(second[b, p]), -100)
    lg = m(x)[:, 17:][:, -k:]
    tgt = tgt_full[:, -k:]
    loss = F.cross_entropy(lg.reshape(-1, 134), tgt.reshape(-1), ignore_index=-100)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if (s + 1) % 200 == 0:
        ok = tgt != -100
        accs.append(round(((lg.argmax(-1) == tgt) & ok).sum().item() / ok.sum().item(), 3))
print(f"mode={mode} pos={pm} heads={heads} lr={lr} supervised/seq={k}: acc at every 200 steps = {accs}", flush=True)
