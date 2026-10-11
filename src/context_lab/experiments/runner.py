"""Execute runs and studies.

``execute_run`` trains one (variant, seed), saves the checkpoint, evaluates
all grids plus built-in controls, and writes the run record. It never
shortens a configuration silently: the resolved configuration that actually
ran is what is stored, and the run id hashes it.

Built-in per-run controls (``analyses`` flags in the spec, all on by default):
* ``evidence_removed``  evaluate an in-distribution set with the evidence unit
  replaced by fillers -> accuracy should fall to about chance if the model
  really reads the evidence (shortcut detector).
* ``position_offset``   evaluate the *same* in-distribution examples with all
  absolute positions shifted by an offset (content unchanged). Translation-
  invariant schemes must be unaffected (up to float error); absolute schemes
  may change. Separates "unfamiliar absolute positions" from "longer context".
* ``data_validation``   run the oracle validator on every evaluation example.
* ``mask_check``        verify that the <ans> prediction is unaffected by
  appending tokens after it (causal-mask sanity check on the trained model).
"""

from __future__ import annotations

import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context

import numpy as np
import pandas as pd
import torch
import yaml

from ..data import TaskSampler, check_example, make_rng, multihop_query_variant, remove_evidence
from ..data.baselines import baseline_accuracies
from ..interventions.counterfactual import battery_summary, counterfactual_battery
from ..evaluation import (accuracy_table, evaluate_grid, grid_examples, leakage_check, predict,
                          training_length_range)
from ..models import Transformer, load_checkpoint, save_checkpoint
from ..training import train_model
from ..utils.env import environment_report
from ..utils.md import md_table
from .registry import Registry, write_json
from .spec import RunSpec, StudySpec, resolve_runs

DEFAULT_ANALYSES = {"evidence_removed": True, "position_offset": [0, 64, 192], "data_validation": True,
                    "mask_check": True, "leakage_check": 5000, "control_n": 400}


def _controls(model: Transformer, run: RunSpec, an: dict) -> tuple[pd.DataFrame, dict]:
    """Per-run control evaluations; returns (rows, summary)."""
    rows, summary = [], {}
    n = int(an.get("control_n", 400))
    ctrl_task = run.task.eval_format()   # training content, single-query format if that is in training
    sampler = TaskSampler(ctrl_task, seed=run.eval_seed, stream="eval/controls/in_distribution")
    base_exs = [sampler.example() for _ in range(n)]
    base = predict(model, base_exs)
    base.insert(0, "grid", "control_in_distribution")
    base.insert(1, "cell", "default")
    rows.append(base)
    summary["in_distribution_acc"] = float(base["correct"].mean())
    if an.get("evidence_removed", True) and run.task.task == "recall":
        rng = make_rng(run.eval_seed, "evidence_removed")
        ex_rm = [remove_evidence(e, rng) for e in base_exs]
        df = predict(model, ex_rm)
        df.insert(0, "grid", "control_evidence_removed")
        df.insert(1, "cell", "default")
        rows.append(df)
        summary["evidence_removed_acc"] = float(df["correct"].mean())
        summary["chance_acc"] = 1.0 / 32
    if an.get("counterfactual", True) and run.task.task == "recall":
        cf = counterfactual_battery(model, base_exs, seed=run.eval_seed)
        summary.update(battery_summary(cf))
        cf_rows = cf.rename(columns={"behaves_as_retriever": "correct"})
        cf_rows.insert(0, "grid", "control_counterfactual")
        cf_rows.insert(1, "cell", cf_rows.pop("edit"))
        cf_rows["status"] = "ok"
        rows.append(cf_rows)
    for off in an.get("position_offset", []) or []:
        df = predict(model, base_exs, pos_offset=int(off))
        df.insert(0, "grid", "control_position_offset")
        df.insert(1, "cell", f"pos_offset={off}")
        df["cell_pos_offset"] = int(off)
        rows.append(df)
        summary[f"pos_offset_{off}_acc"] = float(df["correct"].mean()) if df["status"].eq("ok").all() else None
    if run.task.task == "multihop" and an.get("composition_n"):
        comp, comp_summary = _composition_control(model, run, int(an["composition_n"]))
        rows.append(comp)
        summary.update(comp_summary)
    if an.get("mask_check", True):
        ex = base_exs[0]
        t = torch.tensor([ex.tokens])
        t_ext = torch.tensor([ex.tokens + [int(x) for x in np.random.default_rng(0).integers(6, 22, 7)]])
        with torch.no_grad():
            a = model(t)[0, ex.ans_pos]
            b = model(t_ext)[0, ex.ans_pos]
        summary["mask_check_max_abs_diff"] = float((a - b).abs().max())
    return pd.concat(rows, ignore_index=True), summary


def _composition_control(model: Transformer, run: RunSpec, n: int) -> tuple[pd.DataFrame, dict]:
    """Same 2-hop context, three queries: chain end (<qry> e0), first hop (<nxt> e0), second hop
    (<nxt> e1). Measures whether correct single hops imply a correct composition."""
    task = run.task.replace(hops=2, query_types=["end"], seq_len=64, length_choices=None, n_chains=3)
    s = TaskSampler(task, seed=run.eval_seed, stream="eval/controls/composition")
    base = [s.example() for _ in range(n)]
    variants = {"end": base, "next_hop0": [multihop_query_variant(e, "next", 0) for e in base],
                "next_hop1": [multihop_query_variant(e, "next", 1) for e in base]}
    parts, corr = [], {}
    for name, exs in variants.items():
        df = predict(model, exs)
        df.insert(0, "grid", "control_composition")
        df.insert(1, "cell", name)
        df["composition_id"] = np.arange(len(exs))
        parts.append(df)
        corr[name] = df["correct"].to_numpy()
    both = (corr["next_hop0"] == 1) & (corr["next_hop1"] == 1)
    summ = {"composition_acc_end": float(corr["end"].mean()), "composition_acc_hop0": float(corr["next_hop0"].mean()),
            "composition_acc_hop1": float(corr["next_hop1"].mean()), "composition_both_hops": float(both.mean()),
            "composition_end_given_both_hops": float(corr["end"][both].mean()) if both.any() else None,
            "composition_end_given_not_both": float(corr["end"][~both].mean()) if (~both).any() else None,
            "composition_n": n}
    return pd.concat(parts, ignore_index=True), summ


def _run_report(run: RunSpec, metrics: dict, acc_cells: pd.DataFrame) -> str:
    tr = metrics["training"]
    lines = [f"# Run {run.run_id}", "", f"* study: `{run.study}`  variant: `{run.variant}`  seed: {run.seed}",
             f"* positional method: `{run.model.pos_method}`; layers={run.model.n_layers}, d_model={run.model.d_model}, "
             f"heads={run.model.n_heads}; parameters={tr['n_params']} (positional: {tr['n_params_positional']})",
             f"* task: `{run.task.task}`, training lengths {training_length_range(run.task)}",
             f"* training: {tr['steps_completed']} steps, {tr['train_time_s']:.0f}s, final train loss "
             f"{tr['final_train_loss']:.4f}, final in-distribution val acc {tr['final_val_acc']:.3f}",
             f"* steps to val acc 0.5/0.9/0.99: {tr['steps_to_val_acc_0.5']}/{tr['steps_to_val_acc_0.9']}/"
             f"{tr['steps_to_val_acc_0.99']}", "", "## Controls (measured)", ""]
    for k, v in metrics.get("controls", {}).items():
        lines.append(f"* {k}: {v}")
    lines += ["", "## Validity checks", ""]
    for k, v in metrics.get("validity", {}).items():
        lines.append(f"* {k}: {v}")
    lines += ["", "## Accuracy per evaluation cell (Wilson 95% CI over examples, this seed only)", ""]
    if not acc_cells.empty:
        show = acc_cells[["grid", "cell", "n", "n_unsupported", "acc", "ci_lo", "ci_hi", "mean_loss"]]
        lines.append(md_table(show))
    return "\n".join(lines) + "\n"


def execute_run(run: RunSpec, registry: Registry | None = None, force: bool = False, verbose: bool = True) -> dict:
    reg = registry or Registry()
    rid = run.run_id
    rdir = reg.run_dir(run.study, rid)
    if not force and reg.is_complete(run.study, rid):
        return {"run_id": rid, "status": "cached"}
    rdir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    started = time.strftime("%Y-%m-%d %H:%M:%S")
    write_json(rdir / "status.json", {"status": "running", "started": started})
    write_json(rdir / "config.json", {**run.to_dict(), "run_id": rid, "config_hash": run.config_hash})
    write_json(rdir / "env.json", environment_report())
    log_path = rdir / "train_log.csv"
    if log_path.exists():
        log_path.unlink()
    try:
        header = [True]

        def log_fn(row):
            pd.DataFrame([row]).to_csv(log_path, mode="a", header=header[0], index=False)
            header[0] = False
            if verbose:
                print(f"[{rid}] step {row['step']} loss {row['train_loss']:.3f} acc {row['train_acc']:.3f} "
                      f"val {row['val_acc']:.3f}", flush=True)

        def ckpt_fn(step, m):
            p = reg.checkpoint_path(run.study, rid).with_suffix("") / f"step_{step:06d}.pt"
            p.parent.mkdir(parents=True, exist_ok=True)
            save_checkpoint(m, p, extra={"run_id": rid, "step": step, "task_config": run.task.to_dict()})

        model, history, train_summary = train_model(run.model, run.task, run.train, log_fn=log_fn,
                                                    checkpoint_fn=ckpt_fn)
        ckpt = reg.checkpoint_path(run.study, rid)
        ckpt.parent.mkdir(parents=True, exist_ok=True)
        save_checkpoint(model, ckpt, extra={"run_id": rid, "task_config": run.task.to_dict(),
                                            "train_config": run.train.to_dict(), "train_summary": train_summary})
        # reload to verify checkpoint round-trip before evaluating
        model, _ = load_checkpoint(ckpt)
        an = {**DEFAULT_ANALYSES, **(run.analyses or {})}
        trange = training_length_range(run.task)
        parts, all_exs = [], []
        for g in run.grids:
            cached = grid_examples(run.task, g, run.eval_seed)
            all_exs += [e for _, exs in cached for e in exs]
            parts.append(evaluate_grid(model, run.task, g, run.eval_seed, trange, cached=cached))
        ctrl_rows, ctrl_summary = _controls(model, run, an)
        parts.append(ctrl_rows)
        ev = pd.concat(parts, ignore_index=True)
        if "length_regime" not in ev or ev["length_regime"].isna().any():
            lo, hi = trange
            ev["length_regime"] = np.where(ev["seq_len"] > hi, "extrapolation",
                                           np.where(ev["seq_len"] < lo, "shorter", "in_range"))
        ev.to_parquet(rdir / "eval.parquet", index=False)

        validity = {}
        if an.get("data_validation", True):
            n_bad = sum(1 for e in all_exs if check_example(e))
            validity["eval_examples_checked"] = len(all_exs)
            validity["eval_examples_with_violations"] = n_bad
        if an.get("leakage_check"):
            validity.update(leakage_check(run.task, run.train.seed, [all_exs], n_train=int(an["leakage_check"])))
        validity["mask_check_max_abs_diff"] = ctrl_summary.pop("mask_check_max_abs_diff", None)
        validity["position_overflow_rows"] = int((ev["status"] == "position_overflow").sum())
        acc_cells = accuracy_table(ev, ["grid", "cell"])
        metrics = {"run_id": rid, "training": train_summary, "controls": ctrl_summary, "validity": validity,
                   "grid_accuracy": {g: float(d["correct"].mean()) for g, d in ev.groupby("grid")},
                   "baselines_in_distribution": baseline_accuracies(all_exs[: min(len(all_exs), 2000)])
                   if all_exs else {},
                   "notes": "All values are measured on this run; CIs are example-level only."}
        write_json(rdir / "metrics.json", metrics)
        (rdir / "report.md").write_text(_run_report(run, metrics, acc_cells), encoding="utf-8")
        elapsed = time.time() - t0
        write_json(rdir / "status.json", {"status": "completed", "started": started,
                                          "finished": time.strftime("%Y-%m-%d %H:%M:%S"), "elapsed_s": elapsed})
        return {"run_id": rid, "status": "completed", "elapsed_s": elapsed,
                "val_acc": train_summary["final_val_acc"]}
    except Exception as e:  # noqa: BLE001 - record any failure in the registry
        write_json(rdir / "status.json", {"status": "failed", "started": started, "error": repr(e),
                                          "traceback": traceback.format_exc(), "elapsed_s": time.time() - t0})
        return {"run_id": rid, "status": "failed", "error": repr(e)}


def _job(run_dict_and_flags):
    run, force, root, art = run_dict_and_flags
    return execute_run(run, Registry(root, art), force=force, verbose=False)


def run_study(spec: StudySpec, workers: int = 1, threads: int = 2, force: bool = False, variants=None,
              seeds=None, registry: Registry | None = None, aggregate: bool = True) -> list[dict]:
    reg = registry or Registry()
    sdir = reg.study_dir(spec.name)
    sdir.mkdir(parents=True, exist_ok=True)
    (sdir / "study_spec.yaml").write_text(yaml.safe_dump(spec.to_dict(), sort_keys=False), encoding="utf-8")
    runs = resolve_runs(spec, variants=variants, seeds=seeds, threads=threads)
    print(f"[study {spec.name}] {len(runs)} runs, workers={workers}, threads/worker={threads}", flush=True)
    results = []
    if workers <= 1:
        for r in runs:
            res = execute_run(r, reg, force=force)
            print(f"[study {spec.name}] {res}", flush=True)
            results.append(res)
    else:
        with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("spawn")) as ex:
            futs = {ex.submit(_job, (r, force, reg.root, reg.artifacts)): r for r in runs}
            for f in as_completed(futs):
                res = f.result()
                print(f"[study {spec.name}] {time.strftime('%H:%M:%S')} {res}", flush=True)
                results.append(res)
    if aggregate:
        from .aggregate import aggregate_study
        aggregate_study(spec.name, reg)
    return results
