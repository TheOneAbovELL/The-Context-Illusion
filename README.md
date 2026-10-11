 <div align="center">

# 🧠 The Context Illusion

### A CPU-Only Research Laboratory for Transformer Context and Information Retrieval

**Investigating when, where and why small Transformers lose access to relevant information as context grows.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Transformers-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Experiments](https://img.shields.io/badge/Research-Controlled%20Experiments-6A5ACD)](#reproducing-the-studies)
[![Execution](https://img.shields.io/badge/Execution-CPU--Only-2E8B57)](#quick-start)
[![Privacy](https://img.shields.io/badge/Privacy-Local--Only-1F6FEB)](#local-only)

[Overview](#overview) · [Quick Start](#quick-start) · [Research Components](#what-is-inside) · [Experiments](#reproducing-the-studies) · [Documentation](#documentation) · [Limitations](docs/limitations.md)

</div>

---

## Overview

**The Context Illusion** is a CPU-only research laboratory for studying **when, where and why small Transformers lose access to relevant information as context grows** — with controlled synthetic retrieval tasks, six positional representations behind one interface, length-generalisation and interference experiments, mechanistic diagnostics and causal interventions.

Everything runs locally: **no GPU, no pretrained model, no network, no paid API.**

> **Research results:** [docs/results.md](docs/results.md) contains the results and their interpretation.
>
> **Interpretation boundaries:** [docs/limitations.md](docs/limitations.md) explains what the results do *not* show.

---

## Contents

- [Quick start](#quick-start)
- [What is inside](#what-is-inside)
- [Reproducing the studies](#reproducing-the-studies)
- [Interface](#interface)
- [Documentation](#documentation)
- [Local-only](#local-only)

---

## Quick start

**One command starts everything**: environment and package checks, a quick self-check of the data generators and all six positional schemes, then the local interface in your browser.

On Windows, you can also double-click `start.bat`.

### Start the laboratory

```bash
python start.py
```

### Launcher options

| Option | Behaviour |
|---|---|
| `--tests` | Run the test suite first |
| `--studies` | Rerun every study; cached runs are skipped |
| `--full` | Tests + studies + lab report |
| `--check` | Checks only, no interface |
| `--port N` | Select the interface port |
| `--no-browser` | Do not automatically open the browser |
| `-y` | Answer yes to prompts |

Stop the interface with `Ctrl+C`.

### Individual commands

Check the environment:

```bash
python ctxlab.py env
```

Run the smoke checks:

```bash
python ctxlab.py smoke
```

Run the test suite:

```bash
python -m pytest
```

### Requirements and installation

No installation is required: the launcher adds `src/` to the path.

Optional installation:

```bash
pip install -e .
```

This provides a `ctxlab` command.

**Requirements:** Python ≥ 3.10, `torch`, `numpy`, `pandas`, `scipy`, `matplotlib`, `pyyaml`, `statsmodels`, `psutil`, and `pyarrow`; `streamlit` for the interface.

---

## What is inside

The laboratory combines a small decoder-only Transformer, controlled synthetic data, multiple positional representations, reproducible training and evaluation, mechanistic diagnostics, causal interventions, and a study registry.

| Component | Location | Details |
|---|---|---|
| **Decoder-only Transformer** | `src/context_lab/models` | pre-LN, explicit attention, hook points for every activation |
| **Positional schemes** | `src/context_lab/positional` | NoPE, learned absolute (hard limit, no silent extrapolation), sinusoidal, T5 relative bias, ALiBi, RoPE |
| **Tasks A–F** | `src/context_lab/data` | Associative recall with controllable length / evidence position / distance / distractors / lures / near-miss keys; multi-hop chains; independent oracle validator; baselines |
| **Training** | `src/context_lab/training` | AdamW, warm-up + cosine, answer-position loss, matched step budgets |
| **Evaluation** | `src/context_lab/evaluation` | Example-level rows, evaluation grids, Wilson / seed / paired statistics |
| **Diagnostics** | `src/context_lab/diagnostics` | Attention by role, score gaps, logit lens, evidence sweep, positional structure |
| **Interventions** | `src/context_lab/interventions` | Attention knockout with matched controls, activation patching, head ablation |
| **Experiments** | `src/context_lab/experiments` + `configs/` | YAML study specs, cached runs, registry, aggregation, analysis |
| **Interface** | `app/streamlit_app.py` | 12 sections, all backed by registry data |

### Positional representations

Six positional schemes are available behind one interface:

1. **NoPE** — no explicit positional encoding.
2. **Learned absolute** — learned position representations with a hard limit and no silent extrapolation.
3. **Sinusoidal** — sinusoidal positional representations.
4. **T5 relative bias** — relative-position attention bias.
5. **ALiBi** — attention with linear positional biases.
6. **RoPE** — rotary positional embeddings.

### Controlled research tasks

Tasks A–F include associative retrieval experiments where the laboratory can control context length, evidence position, distance, distractors, lures, and near-miss keys. The task suite also includes multi-hop chains, an independent oracle validator, and baselines.

### Diagnostics and interventions

The laboratory includes attention-by-role analysis, score gaps, logit-lens inspection, evidence sweeps, positional-structure analysis, attention knockout with matched controls, activation patching, and head ablation.

These components provide tools for investigating model behaviour; the interpretation of specific findings should follow the reported results and limitations.

---

## Reproducing the studies

Each research question is one specification in `configs/`.

A study trains every `(variant, seed)`, evaluates all grids and controls, aggregates the results, and writes:

```text
experiments/results/<study>/summary/study_report.md
```

### Run a study

```bash
python ctxlab.py study configs/study_main_pe.yaml --workers 3 --threads 2
```

This invokes the `study_main_pe.yaml` specification with 3 workers and 2 threads.

### Analyse a study

```bash
python ctxlab.py analyze main_pe --seeds 0
```

### Generate the lab report

```bash
python ctxlab.py report
```

### Reproducibility and caching

Runs are cached by a hash of their resolved configuration. Rerunning a study only trains what is missing. `--force` retrains.

See [docs/experimental_protocol.md](docs/experimental_protocol.md) for the full list of studies and commands, and the exact configurations used.

---

## Interface

Launch the Streamlit interface directly with:

```bash
streamlit run app/streamlit_app.py
```

The interface is also launched by the main `python start.py` command after its checks.

The laboratory interface contains 12 sections, all backed by registry data.

---

## Documentation

The following documents provide the detailed technical and scientific context for the project.

| Document | Coverage |
|---|---|
| [Architecture](docs/architecture.md) | System design and data flow |
| [Mathematics](docs/mathematics.md) | Attention, masking, sinusoidal, RoPE, T5 bias, ALiBi, statistics, interventions |
| [Datasets](docs/datasets.md) | Every task, generator, split and validator |
| [Experimental protocol](docs/experimental_protocol.md) | Studies, controls, seeds, reproducibility |
| [Results](docs/results.md) | Measured results and supported conclusions |
| [Limitations](docs/limitations.md) | What the results do not show |
| [References](docs/references.md) | Research references |

### Results and interpretation

Read [docs/results.md](docs/results.md) for the measured results and supported conclusions.

Read [docs/limitations.md](docs/limitations.md) alongside the results to understand what is and is not established. The README does not substitute for those detailed research documents.

---

## Local-only

The code makes no network calls and has no telemetry.

