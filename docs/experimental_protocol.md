# Experimental protocol

## 1. Principles

1. **One question per study, one spec per study.** Each `configs/study_*.yaml`
   declares hypothesis, independent and controlled variables, primary
   metric, seeds, expected failure modes, and any scope reduction
   (`scope_note`). The spec copied into the results folder is the one that
   ran.
2. **Validate before interpreting.** Every run checks every evaluation example
   with the independent oracle parser, measures train/eval duplicates, checks
   the causal mask on the trained weights, and evaluates three controls. A run
   with in-distribution accuracy < 0.90 is flagged: its out-of-distribution
   numbers are not evidence about extrapolation.
3. **Matched comparisons.** Positional methods differ only in the positional
   scheme. All runs of a study share the evaluation seed (identical examples);
   cells within a grid share the content stream (paired cells).
4. **Measured ≠ derived ≠ reference.** `per_seed_cells.csv` (measured),
   `grid_*.csv` / `paired_vs_reference.csv` (derived across seeds),
   `baselines.csv` (algorithmic reference on the same examples).
5. **No silent changes.** Every reduction from the ideal design is written in
   the spec's `scope_note` and in `docs/results.md`; the configuration hash in
   the run id prevents a changed configuration from reusing old results.

## 2. Model and training (all studies unless stated)

| setting | value |
|---|---|
| architecture | decoder-only, pre-LN, 2 layers (multi-hop: 3), d_model 64, 2 heads (d_h 32; the induction study also tests 4), d_mlp 256, GELU, no dropout |
| embeddings | token σ 0.02, learned positions σ 0.02, table size 512 |
| optimiser | AdamW β=(0.9, 0.98), weight decay 0.01 on Linear weights only, grad-clip 1.0 |
| schedule | 100 warm-up steps, cosine to 0.1 × peak; peak LR 3e-3 |
| batch | 64 sequences, one length per batch drawn from the training range |
| query format | `<qry> K <ans>` → V (`query_format: ans_marker`) |
| supervision | every association queried in 75% of training sequences (`n_queries: all`), a single query in 25% (`single_query_prob: 0.25`); evaluation uses the single-query format |
| loss | cross-entropy at the scored `<ans>` and the auxiliary `<ans>` positions (equal weights) |
| budget | fixed number of steps per study, matched across variants (induction/fillers 3,000; others 6,000); checkpoints at 250…6,000 steps for the learning-dynamics analysis (main, multi-hop) |

These values come from the calibration in §6.

## 3. Studies

| study | spec | question | independent variables | variants × seeds |
|---|---|---|---|---|
| content-retrieval control | `study_induction.yaml` | does content-based retrieval emerge on a shortcut-free task; onset by method/head width; does a perfect score on a shortcut-admitting variant imply content retrieval? | `pos_method`, `n_heads`, training order (fixed vs shuffled) | 8 × 3 |
| filler tokens (controlled) | `study_fillers.yaml` | do irrelevant tokens slow learning, with #pairs and #queries fixed? | filler count 0 vs 24 | 2 × 3 |
| 1, 2, 3, 5 + Task D | `study_main_pe.yaml` | length, position, distance, distractors, lures, repeated keys; PE comparison | `pos_method`, `seq_len`, `evidence_pos`, `evidence_distance`, `n_pairs`, `n_lures`, `repeat_distractor_keys` | 6 × 3 |
| 4 | `study_train_length.yaml` | training-length mismatch | max train length {48, 96}, `pos_method` | 6 × 2 |
| 6 / Task E | `study_multihop.yaml` | hop depth, link order, link gap, composition | `hops`, `query_type`, `link_order`, `hop_gap` | 2 × 3 |
| Task C similarity | `study_similarity.yaml` | near-miss distractors | `near_miss_frac`, `n_pairs` | 2 × 2 |
| 7 | `ctxlab analyze <study>` | causal role of evidence reads | knockout layer, patch position/layer, ablated head | seed 0 per variant |

### Controls evaluated in every run

* **in-distribution** — fresh examples from the training distribution;
* **evidence removed** — the evidence unit replaced by fillers; accuracy must
  fall to about chance (1/32) if the model reads the evidence;
* **absolute position offset** — the same in-distribution examples with all
  positions shifted by +64/+192 (content unchanged): isolates sensitivity to
  absolute position from sequence length;
* **causal mask** — appending tokens after `<ans>` must not change its logits;
* **counterfactual battery** (recall) — value edit and key swap (prediction must *follow* the
  edited binding), distractor-value edit, filler resampling, evidence move (prediction must *stay*);
  reported with the value-shortcut reference rate 1/n_pairs (`interventions/counterfactual.py`);
* **best fixed-offset baseline** — accuracy of the best "copy the token d positions back" rule,
  tuned on the scored examples themselves (upper bound for any positional shortcut);
* **composition** (multi-hop) — chain end, first hop and second hop asked on
  identical contexts.

### Diagnostic strategy for "why did accuracy drop?"

| candidate cause | how it is checked |
|---|---|
| incorrect data generation | oracle validator on every example; unit tests per task variant |
| train/test leakage | duplicates of eval examples in 5,000 training samples |
| insufficient training / optimisation | in-distribution accuracy, training curve slope at the end, steps-to-0.9 |
| attention or masking bug | unit tests (mask, normalisation, translation invariance) + per-run mask check |
| positional limitation | absolute-offset control; fixed-distance grid (vary length) vs fixed-length grid (vary distance) |
| distractor interference | distractor/lure/repeat/near-miss grids at fixed length |
| distribution shift | `length_regime` column; train-length study |
| numerical instability | finite-loss checks; grad-norm logging |
| inappropriate metric | exact match reported together with loss, P(answer), rank, margin |

`python ctxlab.py diagnose <study>` prints this checklist per run.

## 4. Statistics

* Per cell and seed: accuracy with Wilson 95% interval (examples).
* Across seeds: mean, s.d., min–max, t-interval.
* Method comparisons: paired per-seed differences vs a reference variant
  (`reference_variant`), with the count of seeds favouring each side.
* We describe an effect as *supported* only if it is consistent in sign
  across all seeds and larger than the seed spread; otherwise *inconclusive*.

## 5. Reproducing

All studies in order (cached runs are skipped):

```bash
bash experiments/run_all.sh 3 2
```

Individually:

```bash
python ctxlab.py study configs/study_induction.yaml --workers 3 --threads 2
python ctxlab.py study configs/study_fillers.yaml --workers 3 --threads 2
python ctxlab.py study configs/study_main_pe.yaml --workers 3 --threads 2
python ctxlab.py study configs/study_multihop.yaml --workers 3 --threads 2
python ctxlab.py study configs/study_train_length.yaml --workers 3 --threads 2
python ctxlab.py study configs/study_similarity.yaml --workers 3 --threads 2
python ctxlab.py dynamics main_pe
python ctxlab.py analyze main_pe --seeds 0
python ctxlab.py report
```

A single run: `--variants rope --seeds 0`. Rebuild summaries without
training: `python ctxlab.py aggregate main_pe`.

## 6. Calibration (pilot runs, before any study)

See `docs/results.md §1` for the measured pilot curves and the decisions they
motivated.
