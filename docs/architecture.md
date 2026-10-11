# Architecture guide

## 1. Layout

```
The Context Illusion/
├── ctxlab.py                     CLI launcher (no install needed)
├── pyproject.toml                package + pytest configuration
├── configs/                      study specifications (YAML) – one file per research question
├── src/context_lab/
│   ├── models/transformer.py     decoder-only Transformer with hook points
│   ├── positional/               none | learned | sinusoidal | t5_relative | alibi | rope
│   ├── data/                     vocab, task generators, layout engine, validator, baselines
│   ├── training/trainer.py       AdamW + warm-up/cosine, answer-position loss
│   ├── evaluation/               example-level prediction, grids, statistics
│   ├── diagnostics/inspect.py    roles, attention profiles, logit lens, evidence sweep, positional structure
│   ├── interventions/causal.py   attention knockout, activation patching, head ablation
│   ├── experiments/              spec → runs, runner, registry, aggregation, mechanistic analysis
│   ├── visualization/plots.py    matplotlib figures from measured tables only
│   ├── reporting/report.py       run diagnosis checklist, combined lab report
│   ├── utils/                    environment audit, paths, markdown tables
│   └── cli/main.py               command-line workflow
├── app/streamlit_app.py          local research interface (reads the registry)
├── tests/{unit,integration,scientific}/
├── docs/                         this guide, mathematics, datasets, protocol, limitations, results, references
├── experiments/results/          run records and study summaries (generated)
└── artifacts/{checkpoints,reports}/  checkpoints and combined reports (generated)
```

Generated data never live under `src/`. `CTXLAB_RESULTS_DIR` and
`CTXLAB_ARTIFACTS_DIR` relocate generated outputs (e.g. outside OneDrive).

## 2. Data flow

```
configs/study_X.yaml
   │  load_spec → StudySpec (hypothesis, variables, seeds, base configs, variants, grids)
   ▼
resolve_runs → RunSpec per (variant, seed)    run_id = <variant>_s<seed>_<sha1(config)[:8]>
   │
   ▼  execute_run (one process per run; ProcessPoolExecutor for parallel workers)
   ├─ TaskSampler(stream="train") ─► train_model ─► checkpoint (artifacts/checkpoints/<study>/<run_id>.pt)
   ├─ reload checkpoint (round-trip verified before evaluation)
   ├─ grid_examples(stream="eval/<grid>", eval_seed) ─► predict ─► eval.parquet (one row per example)
   ├─ controls: in-distribution, evidence removed, absolute position offset, causal-mask check
   ├─ validity: oracle check of every eval example, train/eval duplicate count
   └─ metrics.json, report.md, status.json, train_log.csv, env.json, config.json
   ▼
aggregate_study ─► per_seed_cells.csv (measured) ─► grid_*.csv, paired_vs_reference.csv (derived)
                 ─► baselines.csv (reference) ─► fig_*.png ─► study_report.md
   ▼
analyze_study (seed 0 per variant) ─► attention roles, logit lens, evidence sweep,
                                      knockout, patching, head ablation ─► analysis_report.md
   ▼
build_lab_report ─► artifacts/reports/lab_report.md (environment + all studies + per-run diagnoses)
```

## 3. Model

`Transformer(cfg)` = token embedding → positional scheme → `n_layers` pre-LN
blocks (causal multi-head attention + GELU MLP) → final LayerNorm → unembedding.
The attention is written out explicitly (no fused kernels) so every
intermediate can be read or replaced:

| hook | shape | meaning |
|---|---|---|
| `embed.tok`, `embed.pos` | (B,T,D), (T,D) | token and additive positional embeddings |
| `L{l}.resid_pre/mid/post` | (B,T,D) | residual stream before attention / after attention / after MLP |
| `L{l}.attn.q/k/v` | (B,H,T,d_h) | after RoPE rotation if applicable |
| `L{l}.attn.scores` | (B,H,T,T) | pre-softmax logits incl. bias and causal −∞ |
| `L{l}.attn.probs` | (B,H,T,T) | attention weights |
| `L{l}.attn.z` | (B,H,T,d_h) | per-head outputs before W_O |
| `L{l}.attn.out`, `L{l}.mlp.out` | (B,T,D) | block contributions |
| `final.ln`, `logits` | | |

`forward(tokens, pos_offset=0, hooks={name: fn}, cache={})`. A hook returning
a tensor replaces the activation (used by knockout, patching, ablation).

**Fairness control.** All six positional schemes plug into the same three
entry points (additive input, q/k rotation, logit bias); the attention code,
widths, depth, optimiser, data and step budget are identical. The only
parameter-count differences are the learned table (`max_positions × D`) and
the T5 bias (`buckets × H`), reported per run (`n_params_positional`).

## 4. Experiments

A study spec states the hypothesis, independent and controlled variables,
primary metric, seeds, expected failure modes, and any transparent scope
reductions (`scope_note`). Variants override parts of the base config.
Evaluation grids are Cartesian products of task-config overrides; all runs of
a study share the evaluation seed, so method comparisons are paired on
identical examples, and all cells of a grid share a content stream, so cells
are paired too.

Runs are cached by configuration hash: re-running a study only trains what is
missing or whose configuration changed (`--force` retrains). A failing run is
recorded with its traceback (`status.json`) and does not stop the study.

## 5. Interfaces

* **CLI** (`python ctxlab.py ...`): `env`, `gen`, `study`, `aggregate`,
  `analyze`, `inspect`, `diagnose`, `list`, `report`, `smoke`.
* **Streamlit** (`streamlit run app/streamlit_app.py`): twelve sections from
  environment status to report generation; every view reads the registry or a
  local checkpoint.

## 6. Determinism

Model initialisation: `torch.manual_seed(run seed)`. Data: NumPy
`SeedSequence([seed, crc32(stream)])`. Evaluation is deterministic (no
dropout; `model.eval()`). CPU float32 results can differ in the last bits
across thread counts; accuracy-level results are stable (tested:
`test_deterministic_init_and_eval`, checkpoint round-trip equality).
