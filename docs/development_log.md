# Development log — The Context Illusion

A chronological record of what was built, what went wrong, what was fixed, and
which beliefs were overturned by evidence. Written during development (session of
2026-10-11) so that nothing depends on memory. Every claim points to a file,
log, or test.

Legend: **BUG** = a defect in code or design that was found and fixed;
**WRONG** = a hypothesis of mine that the evidence contradicted;
**DECISION** = a choice with its reason; **FINDING** = a measured result.

---

## Phase 0 — Environment audit (≈19:05)

* Project folder was empty except a Windows `desktop.ini`. Not a git repository
  (it is still not one: no `git init` was done without being asked).
* Hardware differed from the brief: **AMD Ryzen 5 7530U** (6 cores / 12 threads),
  not the 5300U mentioned; 15.3 GB RAM with only ~0.9 GB free at the start; AMD
  Radeon integrated graphics; no CUDA.
* Software: Python 3.13.3, torch 2.10.0+cpu, numpy 2.5.2, pandas 3.0.0, scipy
  1.17, matplotlib 3.10.8, streamlit 1.58, pytest 8.3.4, pyyaml, statsmodels,
  psutil already installed. `tabulate` was **missing** (relevant later).
* The folder lives inside **OneDrive** → synced to Microsoft's cloud by default.
  DECISION: do not move anything (it is the user's choice), but make outputs
  relocatable with `CTXLAB_RESULTS_DIR` / `CTXLAB_ARTIFACTS_DIR` and print a
  warning in `ctxlab env` (`utils/env.py: cloud_sync_warning`).
* Benchmark (scratch script): a 2-layer d=64 model took ~110 ms/step at T=64,
  and 6 threads were *not* faster than 2. Cause found later: **other projects'
  processes** ("Inside the Transformers" training, an `attention_lab`
  benchmark, Chess Engine tests) were running on the same CPU throughout the
  session. DECISION: never touch them; keep my parallelism at ≤ 3 workers × 2
  threads; report all runtimes as contention-affected upper bounds.

## Phase 1 — Core implementation (≈19:10–19:40)

Built in this order (all under `src/context_lab/`):

1. `positional/` — one interface with three hooks (additive input, q/k rotation,
   logit bias) so the attention code is identical for every method. Methods:
   none, learned (hard limit; raises `PositionOverflowError`), sinusoidal,
   T5 bucketed relative bias, ALiBi, RoPE (rotate-half layout).
   * Small clean-up: an unused helper in `absolute.py` was removed right away.
2. `models/transformer.py` — pre-LN decoder with explicit attention and a hook
   system (`hooks={name: fn}`, `cache={}`) at every intermediate
   (`HOOK_POINTS`). `pos_offset` argument to shift all positions (used for
   translation-invariance tests and the absolute-position control).
3. `data/vocab.py`, `data/tasks.py` — one fixed 134-token vocabulary; a
   *layout engine* that places evidence at exact offsets and distributes the rest.
4. `data/validate.py` — an **independent oracle parser** that recomputes the
   answer from tokens only, plus invariant checks.
5. `data/baselines.py` — oracle, naive induction, last value, random-in-context,
   chance.

First validation: 8 task configurations × 500 examples → 0 invariant violations;
baselines behaved as designed (lures fool naive induction: 0.53; one-hop
copying scores 0 on 2-hop chains).

**Performance fix (generator):** fillers were sampled one at a time with
`rng.choice(range)` → replaced by one vectorised `rng.integers` call
(`layout_context`).

## Phase 2 — Pilot round 1 and the training stack (≈19:40–20:00)

* Trainer (`training/trainer.py`): AdamW, warm-up + cosine, answer-only loss,
  weight decay only on Linear weight matrices (so unused learned-position rows
  stay exactly at initialisation), on-the-fly data, fixed validation stream.
* Pilot round 1 (RoPE / learned / NoPE, lr 1e-3, 1 query per sequence, token
  init σ = 1.0): all three stuck at ≈ 0.26–0.35 validation accuracy for 1,750
  steps — exactly the "guess a value that appears in the context" level (0.265).
  Logs: `experiments/calibration/logs/pilot_*2.log`.

## Phase 3 — Evaluation, diagnostics, interventions, registry, CLI (≈19:50–20:30)

* `evaluation/evaluator.py` — example-level prediction rows; grids; leakage check.
* `evaluation/stats.py` — Wilson intervals, across-seed t-intervals, paired
  differences, exact McNemar.
* `diagnostics/inspect.py` — role labels, attention-by-role, logit lens,
  evidence sweep, positional structure.
* `interventions/causal.py` — attention knockout with matched controls,
  activation patching, head ablation. Clean-up: removed leftover dummy code
  (`_np`, a pointless `hooks = {}`).
* `experiments/` — YAML study specs → runs with id `<variant>_s<seed>_<hash8>`;
  registry of plain files; aggregation; mechanistic analysis.
* **BUG (missing dependency):** the run report used `DataFrame.to_markdown()`,
  which needs `tabulate` (not installed). Fix: wrote `utils/md.py: md_table`
  instead of adding a dependency.
* **BUG (formatting):** integer columns that became float because of NaNs
  printed as `16.000`. First fix formatted every whole float as an int, which
  would also print accuracy `1.000` as `1`. Corrected to a *column-level* rule
  (`_int_like`).
* Smoke test (`python ctxlab.py smoke`) passed end-to-end in 80 s.

## Phase 4 — Training-signal pilots (round 2–3)

| pilot | change | result |
|---|---|---|
| B | lr 3e-3, 1 query | 0.29 @2250 |
| C | lr 1e-3, 1–4 queries | 0.36 @2000 |
| D | lr 3e-3, 1–4 queries | **0.50 @2500** (best so far) |
| E | lr 1e-2 | 0.31 @1000 (worse) |
| F | 3 layers | 0.45 @2250 |
| G | token init σ = 0.02 | 0.37 @2000 |

DECISION: implement **auxiliary training queries** (`n_queries`): extra
`<qry> K <ans> V` blocks about distractor pairs before the scored query, loss on
every `<ans>`; evaluation always uses one query (inside the training
distribution).

## Phase 5 — Unit tests and two real bugs they exposed

* **BUG (RNG design, found by a test):** `test_position_independent...` failed:
  changing *only* the evidence position changed *which* examples were generated,
  because content (keys, values, counts) and placement shared one random stream.
  FIX: every example now draws its content first, then one integer that seeds a
  private *placement* RNG. Consequence (a feature): evaluation cells within a grid
  are **paired** — example *i* has the same keys/values in every cell. Evaluation
  streams changed from `eval/<grid>/<cell>` to `eval/<grid>`.
* **BUG (analysis crash):** mechanistic analysis built a "long" set at 2× the
  training length without checking the learned table size →
  `PositionOverflowError` in the integration test. FIX: cap the long set at the
  table size *and record the cap* (`long_note`), never extrapolate silently.
* **BUG (statistics warning):** all-NaN groups (unsupported positions) produced
  "mean of empty slice" warnings. FIX: `seed_aggregate` filters NaNs explicitly.
* **BUG (test I wrote wrongly):** a corrupt-query test contained a meaningless
  boolean expression; also values can legitimately coincide across keys, so
  "answer changes" is not guaranteed. Rewritten to test the right property (a
  different key is queried and the oracle agrees).
* Silenced an unrelated `pytest-asyncio` plugin warning (`-p no:asyncio`).

## Phase 6 — Searching for why the model does not learn retrieval

**FINDING (diagnostic breakdown, `experiments/calibration/logs/diag.log`):** a
stalled model's accuracy ≈ 1/n_pairs (0.54 at 2 pairs, 0.25 at 4, 0.19 at 8) and
its `<ans>` position spreads ≈ 80% of attention over *all value tokens*, evidence
value share ≈ 1/n_pairs. It learned "answer with some value from the context",
not key matching. This is the **value-type shortcut**.

**WRONG #1 — the "self-match" hypothesis.** I argued that in the format
`<qry> K <ans>` the predicting position (`<ans>`) has the query key as its
previous token, so a "match previous tokens" rule also matches itself, and
proposed the standard `<qry> K` (key-last) format. Implemented as a configurable
`query_format` (so both stay testable). Evidence: easy task P1 (`<ans>`) 0.64 vs
P3 (key-last) 0.62 — no help; later under dense queries the `<ans>` format was
**better** (P6 0.62 vs P5 0.47). Also, the stalled model barely attended to
itself. Recorded as refuted. (The heredoc used for this patch broke the shell
once — `unexpected EOF` — and nothing ran; patches were thereafter written to
script files first.)

**BUG (initialisation, demonstrated):** with token embeddings at σ = 1.0, the
key-last model could not even learn to copy a *single* value (accuracy 0.02–0.05,
loss = ln 32 = uniform over values) while σ = 0.02 learned it perfectly. In a
pre-LN residual stream, large embeddings (norm ≈ 8) swamp the small initial
attention outputs (mechanism = hypothesis). FIX: default σ = 0.02 for token and
learned-position embeddings; sinusoidal scaled to the same RMS
(`sinusoidal_scale = σ·√2`) so it is not handicapped. The `tiny_trained` test
fixture failed until this was fixed.

**Sanity checks that passed:** copy-previous-token (lag 1 and 3) learned to 100%
in 300 steps by RoPE and learned; NoPE cannot. → attention and positional code
work.

**WRONG #2 — supervision density.** "Induction" (a random sequence repeated)
was learned in ≤ 200 steps with 16 or even 4 supervised positions, so I
concluded density was not the issue... but then:

**BUG (flawed sanity test) — the most instructive bug of the project.** The
"induction" sanity task repeated the sequence **in the same order**, so the
target is always exactly n−1 positions back: a purely *positional* rule solves it
without any content matching. The "fast induction" result was itself a
context illusion. FIX: shuffled the repeat (`experiments/calibration/
induction_density.py`, later `task: induction` with `induction_order:
shuffled|fixed`). With the shuffle, the same model learned **nothing** in 2,000
steps (≈ 0.06 = chance). Verified formally: best fixed-offset rule = 0.087
(shuffled) vs 1.000 (fixed); regression tests
`test_shuffled_induction_has_no_positional_solution`,
`test_fixed_induction_is_solved_by_position_alone`.

**WRONG #3 — "fillers are the obstacle".** Q1 (contexts packed with pairs) vs
Q2 (pairs + fillers): Q1 was *worse*. But Q1 had 2–3× more pairs (lower chance),
so the comparison did not isolate fillers. Later replaced by a controlled study
(Phase 9).

**Dense supervision** (`n_queries: "all"` = query every association,
`single_query_prob`): first attempt **BUG**: `n_q = 10**6` made the context
length negative, collapsing every example to a single query. FIX: set
`n_q = n_pairs` before the fitting loop.

**Calibration finding later overturned (WRONG #4):** shuffled-induction pilots
suggested head width was decisive (RoPE with 2 heads learned at step 1,200;
RoPE/learned with 4 heads did not by 2,000; NoPE with 4 heads did). In the
proper multi-seed study (Phase 9) almost every RoPE/learned variant learned by
step 900 — the pilot script differed (batch 32, constant LR, weight decay on
embeddings, 2,000 steps). Lesson: single-seed pilots with a different training
recipe are not evidence.

## Phase 7 — New directive: consolidation and shortcut detection (≈20:55)

The user's second brief asked to consolidate evidence and to make shortcut
detection first-class. Implemented:

* `interventions/counterfactual.py` — value edit, key swap (must *follow*);
  distractor edit, filler resampling, evidence move (must *stay*); with the
  value-shortcut reference rate 1/n_pairs. Refinement: key swaps with a distractor
  whose value equals the evidence value were excluded (cannot distinguish
  follow from stay).
* `baselines.best_fixed_offset` — optimistic upper bound for any positional rule.
* `task: induction` with shortcut-admitting (`fixed`) and shortcut-free
  (`shuffled`) orders; validator; roles. **BUG:** my validator asserted the
  fixed-order match offset is n−1; it is n (the successor is n−1 back) → 300
  false "errors"; fixed.
* Intermediate checkpoints (`checkpoint_steps`) and `ctxlab dynamics`.
* **BUG:** counterfactual rows added to `eval.parquet` had no `status` column →
  the integration test's "all rows ok" failed. Fixed.
* **BUG (design):** the in-distribution control always switched to the
  single-query format, which is out of distribution for studies that never train
  on single queries. FIX: `TaskConfig.eval_format()` switches only if
  single-query sequences are in training; used by runner, analysis, dynamics.
* Calibration consolidated into `experiments/calibration/pilots.csv`
  (`summarize.py`), with confounds documented (P6 vs P7: depth confounded with
  parameters, single seeds, difference within noise → inconclusive).

## Phase 8 — Figures

**BUG (visualisation):** colours were assigned from sorted variant names, so
`rope_h2` and `rope_h4` got unrelated colours; legends were clipped or covered
bars; axis labels showed internal names (`cell_induction_order`). FIX: colour
follows the positional-method family (`method_family`), variants of a family
differ by line style / hatch; legends below the plot; pretty labels.

## Phase 9 — Studies run so far

* **Induction control** (`study_induction.yaml`, 24 runs, 0 failed). FINDING
  (demonstrated, 6/6 runs): models trained on the fixed order (shortcut
  available) score **1.00** there and **0.067 = chance** on the shuffled order;
  shuffled-trained RoPE/learned models score 1.00 on both. The shortcut is learned
  in 100 steps vs 500–900 for content matching. NoPE learns partially (0.71–0.87).
  Absolute-position shift (+64) breaks learned-absolute models (0.05–0.20) but not
  RoPE/NoPE (untrained table rows; see caveat in results).
* **Fillers (controlled)** (`study_fillers.yaml`, 6 runs): 4 pairs, all queried;
  0 vs 24 fillers. Both learn (90% by 600–900 steps, one filler seed at 2,800).
  Fillers are not the obstacle; a small slowing effect is unresolved.
* **Factor-isolation probes** (`probe7.py`, single seed, 2,000 steps): variable
  length with 4 pairs (B) 0.58; fixed length with 2–8 pairs + lures (C) 0.57;
  variable length, 4 pairs, *always* all queried (D) 0.74; fixed-format filler
  study ≈ 1.0 by 900. → variable training length is the larger slowing factor,
  the 25% single-query share a smaller one (suggestive).
* Queue paused manually before the main study while B/C/D ran (to avoid wasting
  compute if the design changed), then resumed unchanged (logged in
  `experiments/logs/run_all.log`).

## Open at the time of writing

Main study (6 methods × 3 seeds, 6,000 steps) started 22:13; multi-hop,
training-length and similarity studies queued; then learning dynamics,
mechanistic analysis, extensions (shortcut dose-response, shared-vocabulary
recall, circuit-formation tracking, RoPE interpolation at evaluation), results
write-up, UI verification, and the book.

## Phase 10 — Extensions, UI check, and the elimination shortcut (≈22:15–23:00)

**Extensions implemented** (while the first main study ran):
* `HASH_EXEMPT_DEFAULTS` in `experiments/spec.py`: new configuration fields are left out of the
  run-id hash while at their default, so adding fields did not invalidate the 30 finished runs
  (verified: run ids before/after identical).
* `induction_order: mixed` + `induction_fixed_prob` and `configs/study_shortcut_dose.yaml`
  (shortcut dose-response: share p of shortcut-admitting examples).
* `analysis.circuit_scores`: previous-token score, evidence attention, value-type attention share at
  every saved checkpoint; induction runs also get accuracy on both orders over training.
* `analysis.rope_interpolation_study` + `ctxlab interp`: RoPE linear position interpolation at
  evaluation time (no fine-tuning). FINDING (induction study, 3 seeds × 2 variants): interpolation
  **hurts** strongly (RoPE h2 at length 66: plain 0.51 vs interpolated 0.08; at 96: 0.35 vs 0.02).

**UI verification** (browser pane, `.claude/launch.json`):
* **BUG (privacy):** Streamlit sends usage statistics by default — incompatible with the local-only
  rule. FIX: `.streamlit/config.toml` with `gatherUsageStats = false` (and the launch flag).
* **BUG (UI):** the example-inspection page forced the single-query format, which is out of
  distribution for models trained on other formats (a fillers model answered wrongly, P=0.005).
  FIX: use `TaskConfig.eval_format()` of the run; the same example family is then answered
  correctly (P = 0.92).
* **BUG (UX):** results pages defaulted to the alphabetically first study even if it had no matching
  grid. FIX: default to a study with matching grids (main study preferred).

**FINDING — the elimination shortcut (a context illusion inside the lab itself).**
* Symptom: the main-study RoPE runs had validation accuracy 0.60–0.66 but only 0.27–0.29 in the
  single-query in-distribution control (≈ value-guessing level 0.249); counterfactual key swap,
  *when the model was originally correct*, was followed 0.00–0.02 of the time; editing an
  irrelevant distractor value changed the prediction in ~53% of cases.
* Cause (design flaw, mine): the dense-supervision blocks `<qry> K <ans> V` **display** each
  queried distractor's value. With "query every association" the scored answer is the only context
  value not yet displayed → solvable by elimination without key–value binding.
* Verification (decisive): adding one or two *unqueried* decoy pairs to the fillers-study format,
  the models scored exactly the elimination baseline: 0.515 / 0.490 / 0.497 vs 0.502 (one decoy),
  0.367 / 0.383 / 0.340 vs 0.347 (two decoys).
* Consequences:
  1. The fillers-study conclusion (Phase 9) is **retracted** — it measured how fast elimination is
     learned. Results moved to `experiments/results/fillers_v1_elimination_confounded/` with a
     `SUPERSEDED.md` note; re-run with hidden answers.
  2. The main study was **stopped** after 3 completed runs (+3 interrupted, marked
     `interrupted`) to avoid ~1.5 h of wasted compute; moved to
     `main_pe_v1_elimination_confounded/`.
  3. All calibration "val acc" values of multi-query pilots (D, P5–P9, B2/C2/D2) were inflated by
     the same shortcut; only single-query pilots (R1, B) are honest.
  4. The induction results are **unaffected**: auxiliary induction targets are loss positions only;
     no answers are inserted into the sequence.
* FIX: `aux_show_answers: false` — auxiliary blocks are `<qry> K <ans>`, supervised at `<ans>`, answer
  never inserted. New baseline `elimination` (token-level, coincides with `random_context` when nothing
  is displayed). Regression tests `test_displayed_aux_answers_create_an_elimination_shortcut` and
  `test_hidden_aux_answers_remove_the_elimination_shortcut`. First version of the elimination
  baseline counted distinct values while `random_context` counts tokens → a 0.003 mismatch made the
  new test fail; fixed by making both token-level (definition made coherent, test not weakened).
* Lesson: the same tool the project built to detect shortcuts in models (counterfactual edits +
  explicit baselines) caught a shortcut in the project's own training design.

## Phase 11 — Factor isolation, dose-response and main study v2 (≈23:00 – 01:35)

* **Value-type 2×2** (`study_value_type.yaml`): only shared vocabulary + key-last learns recall (3/3);
  the other cells 0/9. FINDING: removing the value-type shortcut is necessary but not sufficient.
* **Supervision density** (`study_density.yaml`): 1 supervised position per induction sequence → not
  learned (0/3); 4 → 1/3; 15 → 3/3.
* **Knockout bug (B14):** knockout hooks were built for at most 128 examples; larger batches failed.
  FIX: evaluate in chunks of 128 (`causal._chunks`), regression test added; analyses rerun 00:00:52.
* **Shortcut dose-response** (`study_shortcut_dose.yaml`, 00:10–00:45): fixed order learned by step 200
  whenever p ≥ 0.25; content retrieval delayed (p 0: 500–700 → p 0.5: 1500–2100) and absent for
  p ≥ 0.75 within 3,000 steps.
* **Correction (own claim):** "p = 0 models all form a previous-token head" was based on seed means;
  per-seed checking showed a clean previous-token head only in seed 1. Claim retracted.
* **Main study v2** (00:45–01:35, 18 runs, 0 failed): only RoPE seed 0 learned retrieval; the recipe
  from single-seed probe S3 is not reliable across seeds and methods. Results in `results.md` §4.
* **Budget check** (probe11, RoPE seeds 1/2, 8,000 steps): not learned (0.24 / 0.31; key swap 0%).
* **FINDING (01:49):** RoPE interpolation at evaluation *helps* the retrieving recall model (0.37 → 0.83 at
  length 256) while it hurts the induction models — the effect is model-dependent.
