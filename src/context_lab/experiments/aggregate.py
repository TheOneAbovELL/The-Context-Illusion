"""Study-level aggregation: per-seed cell accuracies -> across-seed summaries,
paired method comparisons, baselines, validity flags, plots and a report.

Three kinds of numbers are kept apart in every output:
* measured  -- example-level outcomes and per-run accuracies (``per_seed_cells.csv``)
* derived   -- across-seed means / intervals / differences (``seed_summary.csv``, ``paired_*.csv``)
* reference -- algorithmic baselines on the identical evaluation examples (``baselines.csv``)
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from ..data.baselines import baseline_accuracies
from ..evaluation import GridSpec, accuracy_table, grid_examples, paired_difference, seed_aggregate
from ..evaluation.evaluator import training_length_range
from ..utils.md import md_table
from ..visualization import plots
from .registry import Registry, write_json
from .spec import StudySpec, resolve_runs

DERIVED_BINS = {
    "distance": [0, 8, 16, 32, 64, 128, 256, 512],
    "evidence_norm_pos": [-0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1.01],
}


def _cell_vars(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.startswith("cell_")]


def per_seed_cells(ev: pd.DataFrame) -> pd.DataFrame:
    grid_rows = ev[~ev["grid"].str.startswith("control_")]
    parts = []
    for grid, g in grid_rows.groupby("grid"):
        cv = [c for c in _cell_vars(g) if g[c].notna().any()]
        t = accuracy_table(g, ["variant", "pos_method", "seed"] + cv)
        t.insert(0, "grid", grid)
        parts.append(t)
    ctrl = ev[ev["grid"].str.startswith("control_")]
    if not ctrl.empty:
        t = accuracy_table(ctrl, ["grid", "cell", "variant", "pos_method", "seed"])
        parts.append(t)
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()


def derived_tables(ev: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Accuracy by *measured* per-example variables (actual distance, actual
    normalised position, number of distractors, ...) pooled over grids that
    vary them, per seed."""
    out = {}
    grid_rows = ev[~ev["grid"].str.startswith("control_") & ev["correct"].notna()].copy()
    if grid_rows.empty:
        return out
    for var, bins in DERIVED_BINS.items():
        if var in grid_rows and grid_rows[var].notna().any():
            grid_rows[f"{var}_bin"] = pd.cut(grid_rows[var], bins=bins).astype(str)
            t = accuracy_table(grid_rows, ["grid", "variant", "pos_method", "seed", f"{var}_bin"])
            out[f"by_{var}"] = t
    return out


def _chance(ev: pd.DataFrame) -> float:
    return 1 / 48 if (ev.get("task") == "multihop").all() else 1 / 32


def aggregate_study(study: str, registry: Registry | None = None) -> Path:
    reg = registry or Registry()
    sdir, out = reg.study_dir(study), reg.summary_dir(study)
    out.mkdir(parents=True, exist_ok=True)
    spec = StudySpec.from_dict(yaml.safe_load((sdir / "study_spec.yaml").read_text(encoding="utf-8")))
    runs_tbl = reg.runs_table(study)
    runs_tbl.to_csv(out / "runs.csv", index=False)
    ev = reg.load_all_evals(study)
    if ev.empty:
        (out / "study_report.md").write_text(f"# {spec.title}\n\nNo completed runs yet.\n", encoding="utf-8")
        return out / "study_report.md"
    entity = "variant"
    chance = _chance(ev)

    ps = per_seed_cells(ev)
    ps.to_csv(out / "per_seed_cells.csv", index=False)
    figs, sections = [], []

    # ---------------------------------------------------------------- per grid
    runs = resolve_runs(spec)
    train_ranges = {r.variant: training_length_range(r.task) for r in runs}
    base_task = runs[0].task
    baseline_rows = []
    for gd in spec.eval_grids:
        g = GridSpec.from_dict(gd)
        sub = ps[ps["grid"] == g.name]
        if sub.empty:
            continue
        keys = [f"cell_{k}" for k in g.vary]
        agg = seed_aggregate(sub, [entity] + keys)
        agg.insert(0, "grid", g.name)
        agg.to_csv(out / f"grid_{g.name}.csv", index=False)
        # baselines on the identical examples
        for cell, exs in grid_examples(base_task, g, spec.eval_seed):
            b = baseline_accuracies(exs)
            baseline_rows.append({"grid": g.name, **{f"cell_{k}": v for k, v in cell.items()}, **b})
        title = f"{g.name}"
        if len(keys) == 1:
            x = keys[0]
            numeric = pd.api.types.is_numeric_dtype(agg[x])
            tmax = None
            if x == "cell_seq_len":
                tm = {train_ranges.get(v, (0, 0))[1] for v in agg[entity].unique()}
                tmax = tm.pop() if len(tm) == 1 else None
            if numeric:
                figs.append(plots.line_by_entity(agg, x, entity, title, out / f"fig_{g.name}.png",
                                                 xlabel=x.replace("cell_", ""), chance=chance, train_max=tmax))
            else:
                figs.append(plots.bar_by_entity(agg, x, entity, "mean", title, out / f"fig_{g.name}.png",
                                                ylabel="accuracy", err=("min", "max")))
        elif len(keys) == 2:
            x, f = keys[1], keys[0]
            if pd.api.types.is_numeric_dtype(agg[x]):
                figs.append(plots.line_by_entity(agg, x, entity, title, out / f"fig_{g.name}.png",
                                                 xlabel=x.replace("cell_", ""), chance=chance, facet=f))
            figs.append(plots.heatmap_grid(agg, keys[0], keys[1], entity, title, out / f"fig_{g.name}_heat.png"))
        sections.append((g.name, agg, keys))
    bl = pd.DataFrame(baseline_rows)
    bl.to_csv(out / "baselines.csv", index=False)

    # ---------------------------------------------------------------- derived (measured per-example variables)
    der = derived_tables(ev)
    for name, t in der.items():
        t.to_csv(out / f"derived_{name}.csv", index=False)

    # ---------------------------------------------------------------- paired comparisons vs reference
    paired = []
    ref = spec.reference_variant
    if ref and ref in set(ps[entity]):
        for gd in spec.eval_grids:
            g = GridSpec.from_dict(gd)
            sub = ps[ps["grid"] == g.name]
            keys = [f"cell_{k}" for k in g.vary]
            for v in sorted(set(sub[entity]) - {ref}):
                d = paired_difference(sub, entity, v, ref, keys)
                if not d.empty:
                    d.insert(0, "grid", g.name)
                    paired.append(d)
    paired_df = pd.concat(paired, ignore_index=True) if paired else pd.DataFrame()
    paired_df.to_csv(out / "paired_vs_reference.csv", index=False)

    # ---------------------------------------------------------------- controls & training
    ctrl = ps[ps["grid"].astype(str).str.startswith("control_")]
    ctrl_agg = seed_aggregate(ctrl, ["grid", "cell", entity]) if not ctrl.empty else pd.DataFrame()
    ctrl_agg.to_csv(out / "controls.csv", index=False)
    logs = {}
    for rid in reg.run_ids(study):
        cfg = reg.config(study, rid)
        df = reg.train_log(study, rid)
        if not df.empty:
            logs[f"{cfg.get('variant')}|{cfg.get('seed')}"] = df
    if logs:
        figs.append(plots.training_curves(logs, out / "fig_training_curves.png", f"{spec.title}: training"))

    # ---------------------------------------------------------------- per-run control metrics (measured)
    crow = []
    for rid in reg.run_ids(study):
        m, cfg = reg.metrics(study, rid), reg.config(study, rid)
        if m:
            crow.append({"run_id": rid, "variant": cfg.get("variant"), "seed": cfg.get("seed"),
                         **{k: v for k, v in m.get("controls", {}).items()}})
    controls_by_run = pd.DataFrame(crow)
    controls_by_run.to_csv(out / "controls_by_run.csv", index=False)

    # ---------------------------------------------------------------- validity flags
    flags = []
    for rid in reg.run_ids(study):
        m = reg.metrics(study, rid)
        if not m:
            continue
        tr, va, co = m.get("training", {}), m.get("validity", {}), m.get("controls", {})
        if (tr.get("final_val_acc") or 0) < 0.9:
            flags.append(f"`{rid}`: in-distribution val acc {tr.get('final_val_acc'):.3f} < 0.90 -> undertrained or "
                         "unable to learn the task; out-of-distribution failures of this run are NOT evidence "
                         "about extrapolation.")
        if va.get("eval_examples_with_violations"):
            flags.append(f"`{rid}`: {va['eval_examples_with_violations']} evaluation examples violate data invariants.")
        if va.get("n_eval_in_train_sample"):
            flags.append(f"`{rid}`: {va['n_eval_in_train_sample']} eval examples also appear in a training sample.")
        if co.get("evidence_removed_acc") is not None and co["evidence_removed_acc"] > 3 * (co.get("chance_acc") or 0.03):
            flags.append(f"`{rid}`: evidence-removed accuracy {co['evidence_removed_acc']:.3f} is well above chance "
                         "-> possible shortcut.")
        if (va.get("mask_check_max_abs_diff") or 0) > 1e-4:
            flags.append(f"`{rid}`: causal mask check failed (diff {va['mask_check_max_abs_diff']:.2e}).")

    # ---------------------------------------------------------------- report
    lines = [f"# {spec.title}", "", f"*Study id:* `{spec.name}`  ", f"*Spec:* `{spec.source_path}`", "",
             "## Design", "", f"**Research question.** {spec.research_question}", "",
             f"**Hypothesis.** {spec.hypothesis}", "",
             f"**Independent variables:** {', '.join(map(str, spec.independent_variables))}  ",
             f"**Controlled variables:** {', '.join(map(str, spec.controlled_variables))}  ",
             f"**Primary metric:** {spec.primary_metric}  ", f"**Seeds:** {spec.seeds}  ",
             f"**Evaluation seed (shared by all runs):** {spec.eval_seed}", "",
             "**Expected failure modes:** " + "; ".join(map(str, spec.expected_failure_modes)), ""]
    if spec.scope_note:
        lines += ["**Scope note (transparent reductions):** " + spec.scope_note, ""]
    lines += ["## Runs (measured)", "", md_table(runs_tbl.drop(columns=["error"], errors="ignore")), ""]
    failed = runs_tbl[runs_tbl["status"] == "failed"] if not runs_tbl.empty else runs_tbl
    if not failed.empty:
        lines += ["**Failed runs:**", ""] + [f"* `{r.run_id}`: {r.error}" for r in failed.itertuples()] + [""]
    lines += ["## Validity flags", ""] + ([f"* {f}" for f in flags] or ["* none raised"]) + [""]
    lines += ["## Controls (mean, min and max over seeds)", "",
              md_table(ctrl_agg[["grid", "cell", entity, "n_seeds", "mean", "min", "max"]]) if not ctrl_agg.empty
              else "_none_", ""]
    if not controls_by_run.empty:
        lines += ["## Control metrics per run (measured)", "",
                  "`composition_end_given_both_hops` = accuracy on the chain end among contexts where both "
                  "single hops were answered correctly (multi-hop only).", "",
                  md_table(controls_by_run.sort_values(["variant", "seed"])), ""]
    for name, agg, keys in sections:
        cols = ["grid", entity] + keys + ["n_seeds", "n_per_seed", "mean", "std", "min", "max", "t_lo", "t_hi"]
        lines += [f"## Grid `{name}` (derived: mean across seeds; t-interval over seeds)", "",
                  md_table(agg[[c for c in cols if c in agg]]), ""]
        b = bl[bl["grid"] == name] if not bl.empty else bl
        if not b.empty:
            lines += ["Baselines on the identical examples (reference):", "",
                      md_table(b.drop(columns=["grid"])), ""]
    if not paired_df.empty:
        lines += [f"## Paired differences vs `{ref}` (per-seed differences on identical examples)", "",
                  md_table(paired_df), ""]
    lines += ["## Figures", ""] + [f"![{p.stem}]({p.name})" for p in figs] + [""]
    lines += ["## Reading guide", "",
              "* Per-seed Wilson intervals (in `per_seed_cells.csv`) capture example sampling only; the across-seed "
              "t-interval captures training variability but is very wide with 3 seeds.",
              "* Interpretation and conclusions are written separately in `docs/results.md`; this report is "
              "generated mechanically from the measured tables above.", ""]
    rp = out / "study_report.md"
    rp.write_text("\n".join(lines), encoding="utf-8")
    write_json(out / "summary.json", {"study": study, "n_runs": len(runs_tbl), "flags": flags,
                                      "figures": [p.name for p in figs]})
    return rp

