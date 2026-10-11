"""Build pilots.csv from the calibration logs (measured values) and the explicit
configuration of each pilot (taken from the scripts in this folder).

Usage (from the project root): python experiments/calibration/summarize.py
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGS = HERE / "logs"

# label, log, planned steps, config fields.  Common to all main-task pilots unless noted:
# recall task, seq_len 24-64, 2-8 pairs, lures (0-1, p=0.25), d_model 64, 2 layers, d_mlp 256, seed 0,
# batch 64, AdamW, cosine schedule, 256 validation examples (single in-distribution val stream).
PILOTS = [
    ("R1-rope", "pilot_rope2.log", 2500, dict(pos="rope", heads=4, layers=2, lr=1e-3, tok_std=1.0, fmt="ans_marker", queries="1", task="main")),
    ("R1-learned", "pilot_learned2.log", 2500, dict(pos="learned", heads=4, layers=2, lr=1e-3, tok_std=1.0, fmt="ans_marker", queries="1", task="main")),
    ("R1-none", "pilot_none2.log", 2500, dict(pos="none", heads=4, layers=2, lr=1e-3, tok_std=1.0, fmt="ans_marker", queries="1", task="main")),
    ("B", "p2_B.log", 2500, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=1.0, fmt="ans_marker", queries="1", task="main")),
    ("C", "p2_C.log", 2500, dict(pos="rope", heads=4, layers=2, lr=1e-3, tok_std=1.0, fmt="ans_marker", queries="1-4", task="main")),
    ("D", "p2_D.log", 2500, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=1.0, fmt="ans_marker", queries="1-4", task="main")),
    ("E", "p3_E.log", 3000, dict(pos="rope", heads=4, layers=2, lr=1e-2, tok_std=1.0, fmt="ans_marker", queries="1-4", task="main")),
    ("F", "p3_F.log", 3000, dict(pos="rope", heads=4, layers=3, lr=3e-3, tok_std=1.0, fmt="ans_marker", queries="1-4", task="main")),
    ("G", "p4_G.log", 3000, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=0.02, fmt="ans_marker", queries="1-4", task="main")),
    ("diag", "diag.log", 1500, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=0.02, fmt="ans_marker", queries="1-4", task="main")),
    ("P1", "probe_P1.log", 1500, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=0.02, fmt="ans_marker", queries="1-4", task="short: len 16-32, 2-4 pairs, no lures")),
    ("P2", "probe_P2.log", 1500, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=0.02, fmt="ans_marker", queries="1-4", task="short; d_model 128")),
    ("P3", "probe_P3.log", 1500, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=0.02, fmt="key_last", queries="1-4", task="short: len 16-32, 2-4 pairs, no lures")),
    ("P4", "probe_P4.log", 3000, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=0.02, fmt="key_last", queries="1-4", task="main")),
    ("P5", "probe_P5.log", 3000, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=0.02, fmt="key_last", queries="all(+25% single)", task="main")),
    ("P6", "probe_P6.log", 3000, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=0.02, fmt="ans_marker", queries="all(+25% single)", task="main")),
    ("P7", "probe_P7.log", 3000, dict(pos="rope", heads=4, layers=3, lr=3e-3, tok_std=0.02, fmt="ans_marker", queries="all(+25% single)", task="main")),
    ("Q1", "probe_Q1.log", 1000, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=0.02, fmt="ans_marker", queries="all(+25% single)", task="len 24-40, packed with pairs (no fillers)")),
    ("Q2", "probe_Q2.log", 1000, dict(pos="rope", heads=4, layers=2, lr=3e-3, tok_std=0.02, fmt="ans_marker", queries="all(+25% single)", task="len 24-40, 2-6 pairs + fillers")),
    ("P8", "probe_P8.log", 3000, dict(pos="rope", heads=2, layers=2, lr=3e-3, tok_std=0.02, fmt="ans_marker", queries="all(+25% single)", task="main")),
    ("P9", "probe_P9.log", 3000, dict(pos="learned", heads=2, layers=2, lr=3e-3, tok_std=0.02, fmt="ans_marker", queries="all(+25% single)", task="main")),
]

LINE = re.compile(r"(?:^|\s)(\d+)\s+(?:loss=[\d.]+\s+)?(?:acc=[\d.]+\s+)?val=([\d.]+)|^(\d+)\s+([\d.]+)$")


def parse(path: Path):
    pts = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.search(r"\s(\d+)\s+loss=[\d.]+.*?val=([\d.]+)", " " + line)
        if m:
            pts.append((int(m.group(1)), float(m.group(2))))
            continue
        m = re.match(r"^(\d+)\s+([\d.]+)$", line.strip())     # diag.log format
        if m:
            pts.append((int(m.group(1)), float(m.group(2))))
    return pts


def main():
    rows = []
    for label, log, planned, cfg in PILOTS:
        p = LOGS / log
        pts = parse(p) if p.exists() else []
        last_step, last_val = pts[-1] if pts else (None, None)
        best = max(pts, key=lambda x: x[1]) if pts else (None, None)
        rows.append({"pilot": label, "log": log, **cfg, "planned_steps": planned, "last_logged_step": last_step,
                     "last_val_acc": last_val, "best_val_acc": best[1], "best_at_step": best[0],
                     "status": "completed" if last_step == planned else f"stopped at {last_step}",
                     "curve": " ".join(f"{s}:{v:.3f}" for s, v in pts)})
    out = HERE / "pilots.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['pilot']:11s} {r['pos']:8s} h{r['heads']} L{r['layers']} lr={r['lr']:<6} tok={r['tok_std']:<5} "
              f"{r['fmt']:10s} q={r['queries']:18s} last={r['last_val_acc']} @ {r['last_logged_step']} ({r['status']})")
    # induction controls
    for p in sorted(LOGS.glob("induction_*.log")):
        txt = p.read_text(encoding="utf-8", errors="replace").strip().splitlines()
        print(p.name, "->", txt[-1] if txt else "(empty)")


if __name__ == "__main__":
    main()
