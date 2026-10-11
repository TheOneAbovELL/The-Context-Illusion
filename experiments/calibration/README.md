# Calibration pilots (before any study)

These scripts and logs are the *actual* pilot runs used to choose the training
setup. They ran on a CPU shared with unrelated workloads, so wall-clock times
in the logs are not comparable.

Each script pins the configuration it used at the time (library defaults
changed afterwards: token init σ 1.0 → 0.02, query format `ans_marker` →
study-specific). Two code changes between pilot rounds also changed the exact
data streams: the content/placement RNG split (after round 2) and the
query-format option (before P3). Rerunning a script reproduces its
*configuration*; the exact numbers may differ slightly from the logs.

| log | script / args | what varied |
|---|---|---|
| `pilot_{rope,learned,none}2.log` | `pilot.py <method> 2 2500` | round 1: lr 1e-3, 1 query, σ_tok 1.0 (stopped at 1750) |
| `p2_B.log` | `pilot2.py B_lr3e-3 rope 3e-3 1 2500` | lr 3e-3, 1 query |
| `p2_C.log` | `pilot2.py C_nq4 rope 1e-3 "[1,4]" 2500` | lr 1e-3, 1–4 queries |
| `p2_D.log` | `pilot2.py D_lr3e-3_nq4 rope 3e-3 "[1,4]" 2500` | lr 3e-3, 1–4 queries |
| `p3_E.log` | `pilot3.py E_lr1e-2 rope 1e-2 2 3000` | lr 1e-2 |
| `p3_F.log` | `pilot3.py F_lr3e-3_L3 rope 3e-3 3 3000` | 3 layers |
| `p4_G.log` | `pilot4.py G_tok0.02 rope 3e-3 2 3000 0.02` | σ_tok 0.02 |
| `diag.log` | `diag_pilot.py` | breakdown of a stalled model by n_pairs / distance / attention role |
| `probe_P1/P2.log` | `probe.py P1_short_2-4` / `P2_short_2-4_d128` | easy task (2–4 pairs, length 16–32); width 128 |
| `probe_P3/P4.log` | `probe2.py P3_short_keylast 1500` / `P4_main_keylast 3000` | `key_last` query format |
| `probe_P5/P6.log` | `probe3.py P5_all_keylast key_last` / `P6_all_marker ans_marker` | query every association in training |

Run from the project root, e.g. `python experiments/calibration/pilot2.py D_lr3e-3_nq4 rope 3e-3 "[1,4]" 2500`.

The interpretation is in `docs/results.md §1`.
