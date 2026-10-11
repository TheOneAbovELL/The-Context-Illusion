# Results

All numbers below are copied from machine-readable records in this repository;
the source file is given for every table. Evidence labels:

* **demonstrated** — measured in a controlled comparison with ≥ 3 seeds (or an exact property checked by tests);
* **suggestive** — measured, but single seed, confounded, or small sample;
* **refuted** — a hypothesis contradicted by a measurement;
* **open** — not tested, or inconclusive.

---

## 1. Calibration: getting a small Transformer to *retrieve* at all

Source: `experiments/calibration/pilots.csv` (built by `experiments/calibration/summarize.py`
from the logs in `experiments/calibration/logs/`). All pilots: seed 0, d_model 64, batch 64,
256 validation examples (Wilson 95% half-width ≈ ±6 points at 50%), in-distribution
validation accuracy of the final query. Pilots ran on a CPU shared with other workloads;
some were stopped early on purpose once their question was answered (marked).

### 1.1 What was observed

| pilots | change | result (val acc, last logged step) | label |
|---|---|---|---|
| R1 rope/learned/none | baseline: 1 query/seq, lr 1e-3, token init σ 1.0 | 0.35 / 0.35 / 0.32 @1750 (stopped) | — |
| B vs D | +1–3 auxiliary queries/seq at lr 3e-3 | 0.29 @2250 vs 0.50 @2500 | suggestive: denser supervision helps |
| C vs D | lr 1e-3 vs 3e-3 (both 1–4 queries) | 0.36 @2000 vs 0.50 @2500 | suggestive |
| E | lr 1e-2 | 0.31 @1000 (stopped) | suggestive: worse early |
| diag | breakdown of a stalled model (σ 0.02) | acc ≈ 1/n_pairs (0.54 @2 pairs … 0.19 @8 pairs); `<ans>` attention spread over **all value tokens** (≈ 0.8 of mass), evidence value share ≈ 1/n_pairs | **shortcut identified** (single model) |
| P1 vs P3 | `<ans>` marker vs key-last query format (easy task) | 0.64 vs 0.62 @1500 | **refuted**: my hypothesis that the `<ans>` format's self-match blocks learning |
| P6 vs P5 | same, with dense queries | 0.62 @3000 vs 0.47 @1000 (stopped); P6 ahead at every common checkpoint | suggestive: `<ans>` format learns *faster* |
| P6 vs P7 | 2 vs 3 layers (all else equal) | 0.62 vs 0.68 @3000 | **inconclusive**: one seed each, difference ≈ val-set noise, and depth is confounded with +50k parameters |
| Q1 vs Q2 | packed pairs vs fillers | 0.13 vs 0.63 @1000 | **not interpretable**: Q1 had ~2–3× more pairs (lower chance), so fillers were not isolated → controlled re-test in §3 |
| P8 vs P9 | RoPE vs learned, 2 heads | 0.48 vs 0.63 @3000 | suggestive (single seed) |

Single-association copy test (`n_pairs = 1`, 300 steps, d_model 32): with token-embedding
init σ = 1.0 the key-last model stayed at uniform-over-values loss (accuracy 0.02–0.05); with
σ = 0.02 it reached 1.00. The `<ans>` format reached 1.00 with both. → **demonstrated as a
reproducible failure of that configuration** (rerunnable in seconds; see the
`tiny_trained` fixture, which now uses σ = 0.02); the mechanism (large embeddings swamping
small attention outputs in a pre-LN residual stream) is a hypothesis.

### 1.2 Sanity checks and the corrected induction control

| check | result | label |
|---|---|---|
| copy the previous token (lag 1 and 3), 300 steps | RoPE and learned: 1.00; NoPE: 0.02 (σ 1.0) / 0.57 (σ 0.02) | demonstrated (attention + positional code work) |
| "induction" with the repeat in the **same order** | 1.00 within 200 steps | **flawed test** — the target is always n−1 positions back, so a position-only rule solves it (best fixed-offset baseline = 1.00; regression test `test_fixed_induction_is_solved_by_position_alone`) |
| induction with a **shuffled** repeat (content matching required; best fixed-offset baseline 0.087 ≈ chance 0.0625) | RoPE h4: chance after 2000 steps; learned h4: chance; learned h2: chance; **NoPE h4: onset ≈ step 1400, 0.58 @2000; RoPE h2: 0.97 @1200, 1.00 after** | suggestive (one seed each) → multi-seed study in §2 |

### 1.3 Decisions taken from calibration

1. Token / learned-position init σ = 0.02 (and sinusoidal scaled to the same RMS).
2. Dense training supervision: every association queried in 75% of training
   sequences (`n_queries: all`, `single_query_prob: 0.25`), so the single-query
   evaluation format stays inside the training distribution.
3. `<ans>` query format (better in the only matched comparison, P5 vs P6).
4. 2 attention heads (d_h = 32) for every positional method, because the shuffled
   induction control learned only with d_h = 32 among the RoPE variants tried.
5. Because learning is a delayed phase transition whose timing depends on the method,
   every study uses a fixed, matched step budget and reports steps-to-90% and
   in-distribution accuracy. Runs that do not become competent are flagged and their
   out-of-distribution numbers are not used for claims about extrapolation.

What calibration did **not** establish: why associative recall (P8: 0.48) is so much
slower than shuffled induction (RoPE h2: 1.00 by step 1400) for the same architecture.
The leading hypothesis — supported only by the single `diag` breakdown — is that
recall offers a cheap partial solution (attend to all value tokens, ≈ 1/n_pairs
accuracy) that the induction control does not (its tokens are all of one type), and that
this shortcut creates a long plateau. The counterfactual battery and learning-dynamics
analysis (§4) test whether trained models follow the evidence *content*.

---

## 2. Induction control (multi-seed)

Spec `configs/study_induction.yaml`; sources `experiments/results/induction/summary/`. Length 34,
3,000 steps, 3 seeds per variant.

* **Fixed-order models are a positional shortcut (demonstrated).** Trained and tested on fixed order:
  1.00; tested on shuffled order: 0.067 (chance 0.0625) — 6 of 6 runs (RoPE and learned).
* **Shuffled-order models match content.** RoPE h2: 90% at 500 / 500 / 500 steps; RoPE h4: 900 / 700 /
  600; learned h4: 700 ×3; learned h2: 700 / 600 / never (seed 2 final 0.19); NoPE: never (final
  0.71–0.87).
* **Position shift +64:** learned-position models 0.05–0.20 (untrained table rows); RoPE and NoPE
  unchanged.
* **Length 34 → 96** (mean of 3 seeds): every method degrades (RoPE h2 1.00 → 0.35; learned h4 1.00 →
  0.32; NoPE h2 0.77 → 0.26), staying far above the random-in-context baseline (0.021 at 96). Length and
  number of candidates are confounded in this task.
* **RoPE interpolation at evaluation (no fine-tuning) hurts:** RoPE h2 at 66: 0.51 → 0.08; at 96:
  0.35 → 0.02.

## 3. Filler tokens (controlled)

> **Retracted (v1).** The study below used displayed auxiliary answers and therefore measured how fast the
> *elimination shortcut* is learned, not retrieval (development log, Phase 10). Its results are preserved
> in `experiments/results/fillers_v1_elimination_confounded/`. The v2 rerun with hidden answers
> (`experiments/results/fillers/`) did not learn retrieval in any condition (0.25–0.36 in all six runs),
> so the filler question is **inconclusive**. The v1 text is kept unchanged for the record.

Spec `configs/study_fillers.yaml`; sources `experiments/results/fillers/runs/*/metrics.json`,
`experiments/results/fillers/summary/study_report.md`. RoPE, 2 heads, 3,000 steps; every
sequence has exactly 4 associations, all 4 queried; evaluation in the training format
(400 examples per seed). Chance 1/32; random value from context 0.275; best fixed-offset
rule 0.352.

| condition | steps to 50% | steps to 90% | steps to 99% | final val acc | eval acc (400) |
|---|---|---|---|---|---|
| packed — 0 fillers, length 24 | 700 / 500 / 600 | 900 / 600 / 800 | 1400 / 1100 / 1100 | 1.00 / 1.00 / 1.00 | 1.000 (all seeds) |
| fillers — 24 fillers, length 48 | 700 / 700 / 800 | 900 / 800 / 2800 | 1700 / 1200 / not reached | 1.00 / 1.00 / 0.91 | 0.973 (0.917–1.000) |

Paired difference (fillers − packed) on identical evaluation examples: −0.028, t-interval
[−0.146, 0.091], packed better in 1 of 3 seeds, equal in 2.

**Interpretation.** With the retrieval problem held fixed, 24 irrelevant filler tokens did
not prevent learning, and two of three seeds learned about as fast as without fillers. One
seed was markedly slower (90% at step 2,800). → *Refuted* as the explanation of the
main-task plateau; a small average slowing or a larger seed-to-seed variance is *possible
but unresolved* with three seeds. Fillers and length cannot be separated here (adding
fillers is adding length and spreading the pairs apart). The earlier Q1/Q2 pilot is
superseded: it changed the number of pairs together with the fillers.

A side result matters for the rest of the project: this fixed-format task (4 pairs, all
queried, fixed length, no lures) is learned by ~900 steps, whereas the main-study pilot
distribution (variable length 24–64, 2–8 pairs, lures, 25% single-query sequences) was not
learned after 3,000 steps by the same model (P8: 0.48). See §4.0.

## 4. Main study: length, position, distance, interference, positional methods

**v1** (displayed auxiliary answers) was stopped and preserved as
`experiments/results/main_pe_v1_elimination_confounded/`.

**v2** — spec `configs/study_main_pe.yaml` (shared vocabulary, key-last, hidden dense queries, 4 pairs,
length 24–64, 3,000 steps, 6 methods × 3 seeds); sources `experiments/results/main_pe/summary/`.

| method | seed 0 | seed 1 | seed 2 |
|---|---|---|---|
| RoPE | **0.99** | 0.30 | 0.26 |
| learned | 0.16 | 0.20 | 0.18 |
| sinusoidal | 0.20 | 0.19 | 0.16 |
| T5 bias | 0.28 | 0.21 | 0.28 |
| ALiBi | 0.19 | 0.38 | 0.17 |
| NoPE | 0.19 | 0.18 | 0.17 |

(final validation accuracy). **Negative result (demonstrated):** the recipe found in a single-seed probe
is not reliable; only RoPE seed 0 learned genuine retrieval (key-swap follow rate 1.00), ALiBi seed 1
partly (0.48). The positional-method comparison is therefore **unanswered**.

The one retrieving model (RoPE s0; suggestive — one model): length 32/64/96/128/192/256 →
0.99 / 1.00 / 0.92 / 0.80 / 0.65 / 0.37; no middle dip (at 256: 0.51 at the start → 0.31 next to the
query); distance 8/24/56 at length 128: 0.82 / 0.84 / 0.78; pairs 1→24 at length 64: 1.00 → 0.60.
Its accuracy jumps between steps 500 and 700.

* **RoPE interpolation at evaluation helps this model** (positions × 64/L): 128: 0.80 → 0.97; 192:
  0.65 → 0.89; 256: 0.37 → 0.83 — the opposite of the induction models (§2). Since interpolation keeps the
  token count, the decline beyond length 64 is mainly due to unseen relative distances (suggestive).
* **Mechanism (seed 0):** logit lens 0.04 → 1.00 (layer 0 → 1); ablating either layer-0 head → 0.02 /
  0.08, either layer-1 head → 0.91 / 0.77; knocking out layer-1 attention to the evidence value → 0.96;
  layer-1 heads' attention to the evidence value 0.42 / 0.37 in-distribution vs 0.10 / 0.08 at length 128.
* **Budget check:** RoPE seeds 1 and 2 retrained for 8,000 steps (`experiments/calibration/probe11.py`):
  validation 0.24 / 0.31, key swap followed in 0% of originally correct cases — not learned.

## 5. What makes key–value retrieval learnable

* **Value-type 2×2** (`study_value_type.yaml`, 3 seeds per cell): only shared vocabulary + key-last
  learned (3/3, 90% at 500–600 steps, all counterfactual follow rates ≈ 1.0); the other three cells 0/9
  (key-swap follow 0.00–0.07).
* **Supervision density on induction** (`study_density.yaml`): 1 supervised position: final 0.09 / 0.04 /
  0.07; 4: 0.27 / 1.00 / 0.06; 15: 1.00 ×3 (90% at 500).
* **Shortcut dose-response** (`study_shortcut_dose.yaml`, share p of fixed-order data): p = 0: 90% at
  500–700; 0.25: 1100–2400; 0.5: 1500–2100; 0.75: not learned (0.11–0.12); 0.95 and 1.0: shortcut only.
  The fixed order is learned by step 200 whenever p ≥ 0.25.
