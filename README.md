# The Context Illusion

A CPU-only research laboratory for studying **when, where and why small
Transformers lose access to relevant information as context grows** — with
controlled synthetic retrieval tasks, six positional representations behind
one interface, length-generalisation and interference experiments,
mechanistic diagnostics and causal interventions.

Everything runs locally: no GPU, no pretrained model, no network, no paid API.

> Results and their interpretation: **[docs/results.md](docs/results.md)**.
> What the results do *not* show: **[docs/limitations.md](docs/limitations.md)**.

## Quick start

```bash
python ctxlab.py env
```

```bash
python ctxlab.py smoke
```

```bash
python -m pytest
```

No installation is required (the launcher adds `src/` to the path). Optional:
`pip install -e .` provides a `ctxlab` command. Requirements: Python ≥ 3.10,
torch, numpy, pandas, scipy, matplotlib, pyyaml, statsmodels, psutil;
streamlit for the interface.

## What is inside

| component | where | notes |
|---|---|---|
| decoder-only Transformer | `src/context_lab/models` | pre-LN, explicit attention, hook points for every activation |
| positional schemes | `src/context_lab/positional` | NoPE, learned absolute (hard limit, no silent extrapolation), sinusoidal, T5 relative bias, ALiBi, RoPE |
| tasks A–F | `src/context_lab/data` | associative recall with controllable length / evidence position / distance / distractors / lures / near-miss keys; multi-hop chains; independent oracle validator; baselines |
| training | `src/context_lab/training` | AdamW, warm-up + cosine, answer-position loss, matched step budgets |
| evaluation | `src/context_lab/evaluation` | example-level rows, evaluation grids, Wilson / seed / paired statistics |
| diagnostics | `src/context_lab/diagnostics` | attention by role, score gaps, logit lens, evidence sweep, positional structure |
| interventions | `src/context_lab/interventions` | attention knockout with matched controls, activation patching, head ablation |
| experiments | `src/context_lab/experiments` + `configs/` | YAML study specs, cached runs, registry, aggregation, analysis |
| interface | `app/streamlit_app.py` | 12 sections, all backed by registry data |

## Reproducing the studies

Each research question is one spec in `configs/`. A study trains every
(variant, seed), evaluates all grids and controls, aggregates, and writes
`experiments/results/<study>/summary/study_report.md`.

```bash
python ctxlab.py study configs/study_main_pe.yaml --workers 3 --threads 2
```

```bash
python ctxlab.py analyze main_pe --seeds 0
```

```bash
python ctxlab.py report
```

See [docs/experimental_protocol.md](docs/experimental_protocol.md) for the full
list of studies and commands, and the exact configurations used.

Runs are cached by a hash of their resolved configuration; rerunning a study
only trains what is missing. `--force` retrains.

## Interface

```bash
streamlit run app/streamlit_app.py
```

## Documentation

* [Architecture](docs/architecture.md) — system design and data flow
* [Mathematics](docs/mathematics.md) — attention, masking, sinusoidal, RoPE, T5 bias, ALiBi, statistics, interventions
* [Datasets](docs/datasets.md) — every task, generator, split and validator
* [Experimental protocol](docs/experimental_protocol.md) — studies, controls, seeds, reproducibility
* [Results](docs/results.md) — measured results and supported conclusions
* [Limitations](docs/limitations.md)
* [References](docs/references.md)

## Local-only

The code makes no network calls and has no telemetry. Note: if the project
folder is inside OneDrive/Dropbox (as it is by default here), the sync client
may upload generated files; set `CTXLAB_RESULTS_DIR` and `CTXLAB_ARTIFACTS_DIR`
to a non-synced local path to prevent that.
