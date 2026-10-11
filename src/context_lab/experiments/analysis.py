"""Post-hoc mechanistic analysis of trained runs (Study 7 and diagnostics).

For each selected run this computes, on an in-distribution set and on a
longer-than-training set (identical examples for every run):

* attention role profile at <ans> (+ score gap between evidence value and
  the best competing distractor value)                           [observational]
* logit lens                                                      [observational]
* evidence sweep: move only the evidence, record P(answer)         [controlled input change]
* attention knockout of evidence vs. matched control positions    [causal, direct path]
* residual-stream activation patching (value corruption)          [causal]
* head ablation                                                   [causal]
* positional structure of the scheme                              [parameter inspection]
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import torch
import yaml

from ..data import TaskSampler, collate
from ..diagnostics import attention_role_profile, evidence_sweep, logit_lens, positional_structure
from ..evaluation.evaluator import training_length_range
from ..interventions import head_ablation_study, knockout_study, patching_study, summarize_patching
from ..models import load_checkpoint
from ..utils.md import md_table
from ..visualization import plots
from .registry import Registry, write_json
from .spec import StudySpec


def _sets(task, eval_seed: int, n: int, long_len: int):
    task = task.eval_format()
    s_in = TaskSampler(task, seed=eval_seed, stream="analysis/in_distribution")
    in_d = [s_in.example() for _ in range(n)]
    s_long = TaskSampler(task.replace(seq_len=long_len, length_choices=None), seed=eval_seed,
                         stream=f"analysis/long_{long_len}")
    long_d = [s_long.example() for _ in range(n)]
    return in_d, long_d


def analyze_run(reg: Registry, study: str, run_id: str, n: int = 200, n_patch: int = 32,
                long_factor: float = 2.0) -> dict:
    cfg = reg.config(study, run_id)
    model, payload = load_checkpoint(reg.checkpoint_path(study, run_id))
    from ..data import TaskConfig
    task = TaskConfig.from_dict(cfg["task"])
    lo, hi = training_length_range(task)
    long_len = int(hi * long_factor)
    long_note = ""
    if model.cfg.pos_method == "learned" and long_len > model.cfg.max_positions:
        long_note = (f"long set capped from {long_len} to the learned table size {model.cfg.max_positions} "
                     "(positions beyond the table are refused, not extrapolated)")
        long_len = model.cfg.max_positions
    in_d, long_d = _sets(task, int(cfg["eval_seed"]), n, long_len)
    out = reg.summary_dir(study) / "analysis" / run_id
    out.mkdir(parents=True, exist_ok=True)
    res: dict = {"run_id": run_id, "variant": cfg["variant"], "pos_method": cfg["model"]["pos_method"],
                 "train_len_range": [lo, hi], "long_len": long_len,
                 "long_note": long_note}
    L = model.cfg.n_layers

    # observational: attention roles
    prof = pd.concat([attention_role_profile(model, in_d).assign(set="in_distribution"),
                      attention_role_profile(model, long_d).assign(set=f"long_{long_len}")], ignore_index=True)
    prof.to_parquet(out / "attention_roles.parquet", index=False)
    if "attn_evidence_value" in prof:
        cols = [c for c in ("attn_evidence_value", "attn_evidence_key", "attn_distractor_value", "score_gap",
                            "attn_entropy") if c in prof]          # induction has no distractor roles
        head_tbl = prof.groupby(["set", "layer", "head"])[cols].mean().reset_index()
        head_tbl.to_csv(out / "attention_by_head.csv", index=False)
        last = head_tbl[(head_tbl["set"] == "in_distribution") & (head_tbl["layer"] == L - 1)]
        rh = int(last.sort_values("attn_evidence_value", ascending=False)["head"].iloc[0])
        res["retrieval_head"] = {"layer": L - 1, "head": rh}
        sel = prof[(prof["layer"] == L - 1) & (prof["head"] == rh)]
        scols = [c for c in ("attn_evidence_value", "score_gap", "attn_entropy") if c in sel]
        res["retrieval_head_stats"] = (sel.groupby(["set", "correct"])[scols]
                                       .mean().reset_index().to_dict(orient="records"))
        # by distance on the long set
        sel_long = sel[sel["set"] != "in_distribution"].copy()
        if not sel_long.empty:
            sel_long["distance_bin"] = pd.cut(sel_long["distance"], [0, 16, 32, 64, 128, 256, 1024]).astype(str)
            dcols = [c for c in ("attn_evidence_value", "score_gap", "correct") if c in sel_long]
            res["retrieval_head_by_distance_long"] = (
                sel_long.groupby("distance_bin")[dcols].mean().reset_index().to_dict(orient="records"))
    # logit lens
    ll = pd.concat([logit_lens(model, in_d).assign(set="in_distribution"),
                    logit_lens(model, long_d).assign(set=f"long_{long_len}")])
    res["logit_lens"] = ll.groupby(["set", "layer"])[["p_answer", "correct_at_layer"]].mean().reset_index() \
        .to_dict(orient="records")
    # controlled input change: evidence sweep (average over examples, long set)
    if task.task == "recall":
        sweeps = []
        for i, ex in enumerate(long_d[:24]):
            d = evidence_sweep(model, ex)
            d["example"] = i
            sweeps.append(d)
        sw = pd.concat(sweeps, ignore_index=True)
        sw.to_csv(out / "evidence_sweep_long.csv", index=False)
        sw["norm_bin"] = (sw["evidence_norm_pos"] * 10).round() / 10
        res["evidence_sweep_long"] = sw.groupby("norm_bin")[["p_answer", "correct", "resid_cos_to_original"]] \
            .mean().reset_index().to_dict(orient="records")
        # causal: activation patching
        pt = patching_study(model, in_d, kind="value", max_examples=n_patch)
        pt.to_parquet(out / "patching_value.parquet", index=False)
        ps = summarize_patching(pt)
        ps.to_csv(out / "patching_value_by_role.csv", index=False)
        res["patching_value_by_role"] = ps.to_dict(orient="records")
    if task.task in ("recall", "induction"):
        # causal: attention knockout of the evidence vs matched control positions
        ko = pd.concat([knockout_study(model, in_d).assign(set="in_distribution"),
                        knockout_study(model, long_d).assign(set=f"long_{long_len}")], ignore_index=True)
        ko.to_csv(out / "knockout.csv", index=False)
        res["knockout"] = ko.to_dict(orient="records")
    # causal: head ablation
    ha = head_ablation_study(model, in_d)
    ha.to_csv(out / "head_ablation.csv", index=False)
    res["head_ablation"] = ha.to_dict(orient="records")
    # positional structure
    struct = positional_structure(model, max_pos=max(256, long_len))
    np.savez(out / "positional_structure.npz", **{k: v for k, v in struct.items() if isinstance(v, np.ndarray)})
    write_json(out / "analysis.json", res)
    return res


def analyze_study(study: str, seeds=(0,), variants=None, registry: Registry | None = None, n: int = 200,
                  n_patch: int = 32) -> pd.DataFrame:
    reg = registry or Registry()
    spec = StudySpec.from_dict(yaml.safe_load((reg.study_dir(study) / "study_spec.yaml").read_text(encoding="utf-8")))
    rows = []
    for rid in reg.run_ids(study):
        cfg = reg.config(study, rid)
        if cfg.get("seed") not in seeds or (variants and cfg.get("variant") not in variants):
            continue
        if not reg.is_complete(study, rid):
            continue
        print(f"[analyze {study}] {rid}", flush=True)
        r = analyze_run(reg, study, rid, n=n, n_patch=n_patch)
        rows.append(r)
    out = reg.summary_dir(study) / "analysis"
    out.mkdir(parents=True, exist_ok=True)
    _analysis_report(spec, rows, out)
    return pd.DataFrame([{k: v for k, v in r.items() if not isinstance(v, (list, dict))} for r in rows])


def _analysis_report(spec: StudySpec, rows: list[dict], out) -> None:
    lines = [f"# Mechanistic analysis: {spec.title}", "",
             "Observational measures (attention, logit lens) describe internal quantities; only knockout, "
             "patching and ablation are interventions. Knockout measures only the *direct* <ans>-to-evidence "
             "read in a layer; patching restoration is reported per position role.", ""]
    ko_rows, lens_rows, sweep_rows, ha_rows, pr_rows = [], [], [], [], []
    for r in rows:
        tag = r["variant"]
        for k in r.get("knockout", []):
            ko_rows.append({"variant": tag, **k})
        for k in r.get("logit_lens", []):
            lens_rows.append({"variant": tag, **k})
        for k in r.get("evidence_sweep_long", []):
            sweep_rows.append({"variant": tag, **k})
        for k in r.get("head_ablation", []):
            ha_rows.append({"variant": tag, **k})
        for k in r.get("patching_value_by_role", []):
            pr_rows.append({"variant": tag, **k})
        lines += [f"## `{r['run_id']}` ({r['pos_method']})", "",
                  f"* training lengths {r['train_len_range']}, long set length {r['long_len']} {r.get('long_note', '')}",
                  f"* retrieval head (max attention to evidence value, last layer, in-distribution): "
                  f"{r.get('retrieval_head')}", ""]
        if r.get("retrieval_head_stats"):
            lines += ["Retrieval-head attention to evidence value and score gap, by correctness:", "",
                      md_table(pd.DataFrame(r["retrieval_head_stats"])), ""]
        if r.get("retrieval_head_by_distance_long"):
            lines += ["Long set, retrieval head by evidence distance:", "",
                      md_table(pd.DataFrame(r["retrieval_head_by_distance_long"])), ""]
    if ko_rows:
        ko = pd.DataFrame(ko_rows)
        lines += ["## Attention knockout (accuracy)", "", md_table(ko), ""]
        k2 = ko[ko["condition"] != "none"].copy()
        k2["cond"] = k2["condition"] + "@L" + k2["layer"].astype(str) + " " + k2["set"].str.slice(0, 7)
        plots.bar_by_entity(k2, "cond", "variant", "acc", "Accuracy under attention knockout (evidence vs control)",
                            out / "fig_knockout.png", ylabel="accuracy")
        lines += ["![knockout](fig_knockout.png)", ""]
    if lens_rows:
        lines += ["## Logit lens: P(answer) after each layer", "", md_table(pd.DataFrame(lens_rows)), ""]
    if sweep_rows:
        sw = pd.DataFrame(sweep_rows)
        plots.line_by_entity(sw.rename(columns={"p_answer": "mean"}), "norm_bin", "variant",
                             "Evidence sweep on long inputs: P(answer) vs evidence position",
                             out / "fig_evidence_sweep.png", xlabel="normalised evidence position", err=None,
                             ylabel="mean P(answer)")
        lines += ["## Evidence sweep (same context, only the evidence moves; long set)", "",
                  md_table(sw), "", "![sweep](fig_evidence_sweep.png)", ""]
    if pr_rows:
        pr = pd.DataFrame(pr_rows)
        lines += ["## Activation patching (value corruption): mean restoration by layer and role", "",
                  md_table(pr[pr["count"] > 0]), ""]
    if ha_rows:
        lines += ["## Head ablation (zeroed head output; in-distribution)", "", md_table(pd.DataFrame(ha_rows)), ""]
    (out / "analysis_report.md").write_text("\n".join(lines), encoding="utf-8")


# ----------------------------------------------------------------------------- learning dynamics
@torch.no_grad()
def circuit_scores(model, examples) -> dict:
    """Attention-based markers of the retrieval circuit (observational):
    prev_token_score   max over layer-0 heads of the mean attention from position t to t-1
                       (context positions) -- the 'previous-token head' that binds a value to its key;
    evidence_attention max over last-layer heads of the attention from the prediction position to
                       the evidence value (the token that must be copied);
    value_type_share   last-layer attention (best head) spread over ALL value tokens -- the signature
                       of the value-type shortcut when evidence_attention ~ value_type_share / n_pairs."""
    from ..diagnostics import position_roles
    by_len: dict = {}
    for e in examples:
        by_len.setdefault(len(e.tokens), []).append(e)
    L = model.cfg.n_layers
    prev, evid, vshare = [], [], []
    for group in by_len.values():
        b = collate(group)
        _, cache = model.run_with_cache(b["tokens"])
        A0 = cache["L0.attn.probs"]                               # (B, H, T, T)
        T = A0.shape[-1]
        idx = torch.arange(1, T)
        prev.append(A0[:, :, idx, idx - 1].mean(-1))              # (B, H)
        AL = cache[f"L{L - 1}.attn.probs"][:, :, -1]              # (B, H, T) from the prediction position
        for i, e in enumerate(group):
            vp = e.meta.get("evidence_value_pos")
            if vp is not None:
                evid.append(float(AL[i, :, vp].max()))
            roles = position_roles(e)
            vals = [j for j, r in enumerate(roles) if r in ("evidence_value", "distractor_value")]
            if vals and e.meta["task"] == "recall":
                vshare.append(float(AL[i][:, vals].sum(-1).max()))
    out = {"prev_token_score": float(torch.cat(prev).mean(0).max()) if prev else float("nan"),
           "evidence_attention": float(np.mean(evid)) if evid else float("nan")}
    if vshare:
        out["value_type_share"] = float(np.mean(vshare))
    return out


def dynamics_run(reg: Registry, study: str, run_id: str, n: int = 300) -> pd.DataFrame:
    """Evaluate every intermediate checkpoint of a run on one fixed in-distribution set
    (single-query format): accuracy overall and by number of pairs, and -- for recall --
    the counterfactual battery (does the prediction follow the evidence content?)."""
    from ..data import TaskConfig
    from ..evaluation import predict
    from ..interventions.counterfactual import battery_summary, counterfactual_battery
    cfg = reg.config(study, run_id)
    task = TaskConfig.from_dict(cfg["task"])
    task = task.eval_format()
    s = TaskSampler(task, seed=int(cfg["eval_seed"]), stream="analysis/dynamics")
    exs = [s.example() for _ in range(n)]
    order_sets = {}
    if task.task == "induction":     # shortcut vs content learned, separately over time
        for order in ("shuffled", "fixed"):
            so = TaskSampler(task.replace(induction_order=order), seed=int(cfg["eval_seed"]),
                             stream="analysis/dynamics")
            order_sets[order] = [so.example() for _ in range(n)]
    ckdir = reg.checkpoint_path(study, run_id).with_suffix("")
    paths = sorted(ckdir.glob("step_*.pt")) if ckdir.exists() else []
    rows = []
    for p in paths:
        model, payload = load_checkpoint(p)
        df = predict(model, exs)
        row = {"run_id": run_id, "variant": cfg["variant"], "seed": cfg["seed"], "step": int(payload["step"]),
               "acc": float(df["correct"].mean()), "mean_p_answer": float(df["p_answer"].mean())}
        if "n_pairs" in df:
            for k, g in df.groupby(pd.cut(df["n_pairs"], [0, 2, 4, 6, 100], labels=["1-2", "3-4", "5-6", "7+"]),
                                   observed=True):
                row[f"acc_pairs_{k}"] = float(g["correct"].mean())
            row["value_shortcut_reference"] = float(np.mean(1.0 / df["n_pairs"]))
        if task.task == "recall":
            row.update(battery_summary(counterfactual_battery(model, exs, seed=int(cfg["eval_seed"]))))
        for order, oexs in order_sets.items():
            row[f"acc_{order}_order"] = float(predict(model, oexs)["correct"].mean())
        row.update(circuit_scores(model, exs))
        rows.append(row)
    out = pd.DataFrame(rows)
    if not out.empty:
        d = reg.summary_dir(study) / "dynamics"
        d.mkdir(parents=True, exist_ok=True)
        out.to_csv(d / f"{run_id}.csv", index=False)
    return out


def dynamics_study(study: str, registry: Registry | None = None, n: int = 300) -> pd.DataFrame:
    reg = registry or Registry()
    parts = [dynamics_run(reg, study, rid, n=n) for rid in reg.run_ids(study) if reg.is_complete(study, rid)]
    df = pd.concat([p for p in parts if not p.empty], ignore_index=True) if any(not p.empty for p in parts) \
        else pd.DataFrame()
    d = reg.summary_dir(study) / "dynamics"
    d.mkdir(parents=True, exist_ok=True)
    if df.empty:
        return df
    df.to_csv(d / "dynamics_all.csv", index=False)
    agg = df.groupby(["variant", "step"]).agg(mean=("acc", "mean"), min=("acc", "min"), max=("acc", "max")) \
        .reset_index()
    plots.line_by_entity(agg, "step", "variant", f"{study}: in-distribution accuracy at saved checkpoints",
                         d / "fig_dynamics_acc.png", xlabel="training step")
    for col, lab in (("prev_token_score", "previous-token head score (layer 0)"),
                     ("evidence_attention", "attention to the evidence value (last layer)")):
        if col in df and df[col].notna().any():
            a3 = df.groupby(["variant", "step"]).agg(mean=(col, "mean"), min=(col, "min"), max=(col, "max"))                 .reset_index()
            plots.line_by_entity(a3, "step", "variant", f"{study}: {lab}", d / f"fig_dynamics_{col}.png",
                                 xlabel="training step", ylabel=lab)
    if "acc_shuffled_order" in df:
        long = pd.concat([df.assign(order=o, acc_o=df[f"acc_{o}_order"]) for o in ("shuffled", "fixed")])
        long["series"] = long["variant"] + " | " + long["order"] + " order"
        a4 = long.groupby(["series", "step"]).agg(mean=("acc_o", "mean"), min=("acc_o", "min"),
                                                  max=("acc_o", "max")).reset_index()
        plots.line_by_entity(a4, "step", "series", f"{study}: accuracy on each order over training",
                             d / "fig_dynamics_order_acc.png", xlabel="training step")
    if "cf_value_edit_rate" in df:
        agg2 = df.groupby(["variant", "step"]).agg(mean=("cf_value_edit_rate", "mean"),
                                                   min=("cf_value_edit_rate", "min"),
                                                   max=("cf_value_edit_rate", "max")).reset_index()
        plots.line_by_entity(agg2, "step", "variant",
                             f"{study}: prediction follows an edited evidence value (genuine retrieval -> 1)",
                             d / "fig_dynamics_value_edit.png", xlabel="training step",
                             ylabel="follow rate (value edit)",
                             chance=float(df["cf_value_edit_shortcut_reference"].mean()))
    return df


# ----------------------------------------------------------------------------- RoPE position interpolation
def rope_interpolation_study(study: str, grid_name: str = "length", registry: Registry | None = None) -> pd.DataFrame:
    """Evaluation-time intervention on trained RoPE models: for evaluation lengths L above the maximum
    training length T, multiply positions by T/L (linear position interpolation, Chen et al. 2023)
    WITHOUT any fine-tuning, and compare with plain RoPE on the identical examples. Interpolation
    keeps every relative distance inside the trained range but compresses the angles of nearby tokens,
    which the model never saw -- so it can help or hurt; that is what is measured."""
    from ..data import TaskConfig
    from ..evaluation import GridSpec, grid_examples, predict
    reg = registry or Registry()
    spec = StudySpec.from_dict(yaml.safe_load((reg.study_dir(study) / "study_spec.yaml").read_text(encoding="utf-8")))
    gd = next((g for g in spec.eval_grids if g["name"] == grid_name), None)
    if gd is None:
        raise ValueError(f"study {study} has no grid {grid_name}")
    rows = []
    for rid in reg.run_ids(study):
        cfg = reg.config(study, rid)
        if cfg.get("model", {}).get("pos_method") != "rope" or not reg.is_complete(study, rid):
            continue
        model, _ = load_checkpoint(reg.checkpoint_path(study, rid))
        task = TaskConfig.from_dict(cfg["task"])
        _, hi = training_length_range(task)
        for cell, exs in grid_examples(task, GridSpec.from_dict(gd), int(cfg["eval_seed"])):
            L = int(cell.get("seq_len", 0))
            for mode in ("plain", "interpolated"):
                scale = (hi / L) if (mode == "interpolated" and L > hi) else 1.0
                if mode == "interpolated" and scale == 1.0:
                    continue
                model.pos.scale = scale
                acc = float(predict(model, exs)["correct"].mean())
                rows.append({"run_id": rid, "variant": cfg["variant"], "seed": cfg["seed"], "seq_len": L,
                             "mode": mode, "rope_scale": scale, "acc": acc, "n": len(exs)})
            model.pos.scale = 1.0
    df = pd.DataFrame(rows)
    out = reg.summary_dir(study) / "rope_interpolation"
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "rope_interpolation.csv", index=False)
    if not df.empty:
        df["series"] = df["variant"] + " | " + df["mode"]
        agg = df.groupby(["series", "seq_len"]).agg(mean=("acc", "mean"), min=("acc", "min"),
                                                    max=("acc", "max")).reset_index()
        plots.line_by_entity(agg, "seq_len", "series", f"{study}: RoPE plain vs position interpolation (no fine-tuning)",
                             out / "fig_rope_interpolation.png", xlabel="evaluation length", train_max=None)
    return df
