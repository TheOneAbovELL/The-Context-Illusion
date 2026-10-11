# Limitations guide

Read this before citing any number produced by this laboratory.

## 1. Synthetic tasks

* The tasks isolate *one* capability — exact retrieval of an association from
  context — under controlled interference. Natural-language long-context use
  involves paraphrase, partial matches, reasoning over many facts, and
  pre-trained priors; none of that is modelled.
* Keys and values are atomic tokens (or two-token compounds). "Similarity" is
  defined structurally (shared sub-tokens, the same key in a non-key role),
  not semantically.
* Fillers are i.i.d. uniform tokens. Real "irrelevant context" is
  structured and can look relevant; our filler is the easy case.
* Every example has exactly one correct answer by construction. Real
  retrieval failures often stem from ambiguity, which we exclude on purpose.

## 2. Small models, small budgets

* Models have ~0.1–0.2 M parameters, 2–3 layers, width 64, trained for a few
  thousand steps on a shared, contended CPU. Behaviour of 1e9-parameter models
  trained on trillions of tokens can differ qualitatively (different circuits,
  different positional usage, different failure modes).
* Optimisation budgets are matched in *steps*, not in tokens or wall-clock:
  longer training sequences give a model more tokens per step (Study 4
  confounds training length with token count).
* Hyperparameters (learning rate, auxiliary queries, initialisation) were
  calibrated on RoPE pilot runs (see `docs/results.md`); other positional
  methods may have different optimal settings, so a method that trains worse
  may be *under-tuned* rather than inferior.
* Three seeds (two in some studies) give very wide across-seed intervals;
  differences smaller than the seed spread should be treated as unresolved.

## 3. Length extrapolation

* "Longer than training" here means up to 4× the maximum training length (≤ 256
  tokens). Behaviour at 100× is not tested.
* A learned absolute table of size 512 has untrained rows beyond the training
  length; their behaviour depends on the initialisation scale chosen
  (σ = 0.02, equal to the token embeddings). Different initialisations would give different extrapolation
  numbers. This is a property of the experimental setup, not a law of learned
  positions. With a table sized to the training length, evaluation beyond it
  is refused (`PositionOverflowError`), never silently clamped.
* Longer evaluation sequences change several things at once: unseen absolute
  positions, unseen relative distances, more filler tokens to attend over, and
  shifted statistics of the attention softmax. Grids at fixed distance, the
  absolute-position offset control, and the distractor grids exist to separate
  these, but separation is partial.
* T5 relative bias makes all distances ≥ 128 indistinguishable *by
  construction*; ALiBi's fixed slopes penalise long distances *by
  construction*. Extrapolation results for these methods partly reflect those
  design constants (`rel_max_distance`, slopes), not only learning.

## 4. Interpreting diagnostics

* **Attention weight ≠ information use ≠ causal importance** (Jain & Wallace
  2019; Wiegreffe & Pinter 2019). High attention from `<ans>` to the evidence is
  consistent with, but does not prove, that the answer is read from there.
* Knockout blocks only the *direct* `<ans>`→evidence read in one layer;
  information can route through other positions, so a small knockout effect
  does not prove the evidence is unused.
* Activation patching results depend on the corruption chosen (here: change
  the evidence value, or change the queried key). Different corruptions answer
  different questions.
* Zero-ablation of heads moves activations off-distribution; it upper-bounds a
  head's importance rather than measuring it.
* Logit-lens decoding of intermediate layers uses the final LayerNorm and
  unembedding, which those layers were not trained for.
* Mechanistic analyses are run on one seed per variant (seed 0) for cost
  reasons; circuits can differ between seeds.

## 5. Statistics

* Wilson intervals assume i.i.d. examples within a cell. Paired cells (shared
  content stream) are correlated *across* cells, which helps paired
  comparisons but means cell intervals are not independent.
* No multiple-comparison correction is applied across the many cells; treat
  isolated "significant" cells with suspicion and look for consistent trends.

## 6. Engineering

* CPU-only, float32. Runtime numbers were measured while unrelated workloads
  (other projects' training and benchmark processes) shared the CPU, so
  wall-clock times are upper bounds and not comparable across runs.
* The project folder is inside OneDrive; unless `CTXLAB_RESULTS_DIR` /
  `CTXLAB_ARTIFACTS_DIR` are pointed elsewhere, OneDrive may sync results to
  Microsoft's cloud. The code itself never transmits anything.
