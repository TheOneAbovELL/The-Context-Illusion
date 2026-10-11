"""Run diagnosis (architectural vs. experimental failure) and combined reports.

``diagnose_run`` turns a run record into an explicit checklist. Each item is
a *measured* check with a pass/warn/fail status; the "candidate explanations"
section lists which explanations remain open given those checks. These are
diagnostic hints, not conclusions.
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd

from ..experiments.registry import Registry
from ..utils.env import environment_report
from ..utils.md import md_table


def diagnose_run(reg: Registry, study: str, run_id: str) -> dict:
    m, cfg, st = reg.metrics(study, run_id), reg.config(study, run_id), reg.status(study, run_id)
    log = reg.train_log(study, run_id)
    ev = reg.load_eval(study, run_id)
    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    if st.get("status") != "completed":
        add("run completed", "fail", f"status={st.get('status')} error={st.get('error')}")
        return {"run_id": run_id, "checks": checks, "explanations": ["run did not complete"]}
    va, tr, co = m.get("validity", {}), m.get("training", {}), m.get("controls", {})
    add("data invariants (oracle parser)",
        "pass" if va.get("eval_examples_with_violations", 1) == 0 else "fail",
        f"{va.get('eval_examples_with_violations')} violations in {va.get('eval_examples_checked')} examples")
    add("train/eval leakage", "pass" if va.get("n_eval_in_train_sample", 0) == 0 else "warn",
        f"{va.get('n_eval_in_train_sample')} of {va.get('n_eval')} eval examples found in "
        f"{va.get('n_train_sampled')} sampled training examples")
    add("causal mask on trained model", "pass" if (va.get("mask_check_max_abs_diff") or 0) < 1e-4 else "fail",
        f"max |logit diff| when appending future tokens = {va.get('mask_check_max_abs_diff')}")
    vacc = tr.get("final_val_acc") or 0.0
    add("learned the in-distribution task", "pass" if vacc >= 0.95 else ("warn" if vacc >= 0.8 else "fail"),
        f"final in-distribution val acc = {vacc:.3f}")
    still = None
    if not log.empty and log["val_acc"].notna().sum() >= 3:
        v = log["val_acc"].dropna().to_numpy()
        still = float(v[-1] - v[-3])
        add("training converged (val acc plateau)", "pass" if still < 0.02 else "warn",
            f"val acc change over last two evals = {still:+.3f}")
    if np.isfinite(tr.get("final_train_loss", np.nan)):
        add("numerically finite training", "pass", f"final train loss {tr.get('final_train_loss'):.4f}")
    if co.get("evidence_removed_acc") is not None:
        er, ch = co["evidence_removed_acc"], co.get("chance_acc", 1 / 32)
        add("uses the evidence (evidence-removed control)", "pass" if er <= 3 * ch else "warn",
            f"accuracy with evidence removed = {er:.3f} (chance {ch:.3f})")
    offs = {k: v for k, v in co.items() if k.startswith("pos_offset_")}
    if offs:
        base = co.get("in_distribution_acc")
        drop = {k: (None if v is None else round(base - v, 3)) for k, v in offs.items()}
        add("sensitivity to absolute position shift (same content)", "info", f"accuracy drop by offset: {drop}")
    if not ev.empty and "length_regime" in ev:
        g = ev[~ev["grid"].str.startswith("control_")]
        by = g.groupby("length_regime")["correct"].mean().to_dict()
        add("interpolation vs extrapolation", "info", {k: round(v, 3) for k, v in by.items()})
        if (ev["status"] == "position_overflow").any():
            add("position table overflow", "info",
                f"{int((ev['status'] == 'position_overflow').sum())} rows unsupported (not extrapolated)")
        if ev["loss"].notna().any():
            add("finite evaluation losses", "pass" if np.isfinite(ev["loss"].dropna()).all() else "fail", "")

    expl = []
    status = {c["check"]: c["status"] for c in checks}
    if status.get("data invariants (oracle parser)") == "fail":
        expl.append("DATA: generator/evaluator bug -- fix before interpreting anything.")
    if status.get("learned the in-distribution task") in ("fail", "warn"):
        expl.append("OPTIMISATION / CAPACITY / TRAINING BUDGET: the model does not solve the training "
                    "distribution; any OOD failure is confounded. Try more steps, LR sweep, or more layers.")
        if still is not None and still >= 0.02:
            expl.append("Accuracy was still rising at the end -> insufficient training is the leading explanation.")
    if status.get("uses the evidence (evidence-removed control)") == "warn":
        expl.append("SHORTCUT: the model predicts the answer without the evidence -> check generator for cues.")
    if not expl and not ev.empty and "length_regime" in ev:
        g = ev[~ev["grid"].str.startswith("control_")]
        by = g.groupby("length_regime")["correct"].mean()
        if "extrapolation" in by and "in_range" in by and by["in_range"] - by["extrapolation"] > 0.1:
            pm = cfg.get("model", {}).get("pos_method")
            expl.append(f"DISTRIBUTION SHIFT in length (in-range {by['in_range']:.2f} vs extrapolation "
                        f"{by['extrapolation']:.2f}). Candidate mechanisms for `{pm}`: unseen absolute positions "
                        "(learned/sinusoidal; compare the position-offset control), larger relative distances than "
                        "trained (relative/RoPE), and attention dilution over more tokens (all methods; compare "
                        "the distractor/length grids at fixed distance). Distinguish with the controlled grids.")
    if not expl:
        expl.append("No validity problem detected; remaining differences must be explained with controlled grids.")
    return {"run_id": run_id, "checks": checks, "explanations": expl}


def diagnosis_markdown(d: dict) -> str:
    lines = [f"### Diagnosis `{d['run_id']}`", "", md_table(pd.DataFrame(d["checks"])), "", "Candidate explanations:"]
    lines += [f"* {e}" for e in d["explanations"]]
    return "\n".join(lines) + "\n"


def build_lab_report(reg: Registry | None = None, path=None) -> str:
    """Collect environment, study reports and per-run diagnoses into one file."""
    reg = reg or Registry()
    env = environment_report()
    lines = ["# The Context Illusion -- generated lab report", "",
             f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')} from local registry `{reg.root}`.", "",
             "## Environment", "", "```", *[f"{k}: {v}" for k, v in env["software"].items()],
             *[f"{k}: {v}" for k, v in env["hardware"].items()], "```", ""]
    if env.get("cloud_sync_warning"):
        lines += [f"> {env['cloud_sync_warning']}", ""]
    for study in reg.list_studies():
        sd = reg.summary_dir(study)
        lines += [f"## Study `{study}`", ""]
        rt = reg.runs_table(study)
        lines += [md_table(rt.drop(columns=["error"], errors="ignore")), ""]
        if (sd / "study_report.md").exists():
            lines += [f"Full study report: `{sd / 'study_report.md'}`", ""]
        if (sd / "analysis" / "analysis_report.md").exists():
            lines += [f"Mechanistic analysis: `{sd / 'analysis' / 'analysis_report.md'}`", ""]
        for rid in reg.run_ids(study):
            lines.append(diagnosis_markdown(diagnose_run(reg, study, rid)))
    text = "\n".join(lines)
    out = path or (reg.artifacts / "reports" / "lab_report.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return str(out)
