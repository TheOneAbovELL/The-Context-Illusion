"""Command-line interface: ``python ctxlab.py <command>`` (or ``ctxlab`` if installed).

Commands
  env        environment audit (hardware, versions, paths, cloud-sync warning)
  gen        generate, print, validate and baseline examples of a task
  study      run a study spec (train + evaluate all variants x seeds), then aggregate
  aggregate  rebuild a study's summary tables, figures and report from the registry
  dynamics   evaluate intermediate checkpoints (accuracy + counterfactual battery over training)
  analyze    mechanistic analysis (attention, patching, knockout, ablation) of a study's runs
  interp     RoPE position interpolation at evaluation time (no fine-tuning) on a length grid
  inspect    show one example with prediction, logit lens and attention from a trained run
  diagnose   validity checklist (architectural vs experimental failure) for runs
  list       list studies and runs
  report     build the combined lab report from everything in the registry
  smoke      fast end-to-end check (tiny model, ~1 minute)
"""

from __future__ import annotations

import argparse
import json
import sys


def _parse_overrides(items):
    out = {}
    for it in items or []:
        k, v = it.split("=", 1)
        try:
            out[k] = json.loads(v)
        except json.JSONDecodeError:
            out[k] = v
    return out


def cmd_env(a):
    from ..utils.env import environment_report
    print(json.dumps(environment_report(), indent=2))


def cmd_gen(a):
    from ..data import TaskConfig, baseline_accuracies, check_example, dataset_summary, make_dataset
    from ..data.vocab import DEFAULT_VOCAB as V
    cfg = TaskConfig().replace(**_parse_overrides(a.set))
    exs = make_dataset(cfg, a.n, a.seed, a.stream)
    for e in exs[: a.show]:
        print(V.decode(e.tokens), "=>", V.token_str(e.answer))
        print("   ", {k: v for k, v in e.public_meta().items() if k != "answer"})
    bad = [(i, err) for i, e in enumerate(exs) for err in check_example(e)]
    print("summary:", dataset_summary(exs))
    print("invariant violations:", len(bad), bad[:5])
    print("baselines:", baseline_accuracies(exs))


def cmd_study(a):
    from ..experiments import load_spec, run_study
    spec = load_spec(a.config)
    seeds = [int(s) for s in a.seeds.split(",")] if a.seeds else None
    variants = a.variants.split(",") if a.variants else None
    res = run_study(spec, workers=a.workers, threads=a.threads, force=a.force, variants=variants, seeds=seeds)
    failed = [r for r in res if r["status"] == "failed"]
    print(f"done: {len(res)} runs, {len(failed)} failed")
    return 1 if failed else 0


def cmd_aggregate(a):
    from ..experiments.aggregate import aggregate_study
    print(aggregate_study(a.study))


def cmd_analyze(a):
    from ..experiments.analysis import analyze_study
    seeds = tuple(int(s) for s in a.seeds.split(","))
    variants = a.variants.split(",") if a.variants else None
    df = analyze_study(a.study, seeds=seeds, variants=variants, n=a.n, n_patch=a.n_patch)
    print(df.to_string())


def cmd_dynamics(a):
    from ..experiments.analysis import dynamics_study
    df = dynamics_study(a.study, n=a.n)
    print(df.to_string() if not df.empty else "no intermediate checkpoints found")


def cmd_interp(a):
    from ..experiments.analysis import rope_interpolation_study
    df = rope_interpolation_study(a.study, a.grid)
    print(df.groupby(["variant", "seq_len", "mode"])["acc"].mean().to_string() if not df.empty else "no RoPE runs")


def cmd_inspect(a):
    import torch

    from ..data import TaskConfig, TaskSampler
    from ..diagnostics import inspect_example
    from ..experiments.registry import Registry
    from ..models import load_checkpoint
    reg = Registry()
    model, payload = load_checkpoint(reg.checkpoint_path(a.study, a.run))
    # the model's evaluation format (single query only if single queries occurred in training)
    task = TaskConfig.from_dict(payload["task_config"]).eval_format().replace(**_parse_overrides(a.set))
    ex = TaskSampler(task, seed=a.seed, stream="inspect").example()
    r = inspect_example(model, ex)
    print(" ".join(r["tokens"]))
    print(f"answer={r['answer']} pred={r['pred']} correct={r['correct']} p_answer={r['p_answer']:.3f}")
    print("top-k:", r["top_k"])
    print("logit lens:", r["logit_lens"])
    print("meta:", r["meta"])
    L = model.cfg.n_layers
    vp = r["meta"].get("evidence_value_pos")
    if vp is not None:
        for l in range(L):
            print(f"attention <ans> -> evidence value, layer {l}:",
                  [round(float(x), 3) for x in r["attn"][l, :, -1, vp]])
    del torch


def cmd_diagnose(a):
    from ..experiments.registry import Registry
    from ..reporting import diagnose_run, diagnosis_markdown
    reg = Registry()
    rids = [a.run] if a.run else reg.run_ids(a.study)
    for rid in rids:
        print(diagnosis_markdown(diagnose_run(reg, a.study, rid)))


def cmd_list(a):
    from ..experiments.registry import Registry
    reg = Registry()
    for s in reg.list_studies():
        print(f"== {s}")
        print(reg.runs_table(s).to_string(index=False))


def cmd_report(a):
    from ..reporting import build_lab_report
    print(build_lab_report())


def cmd_smoke(a):
    import time

    from ..experiments import StudySpec, run_study
    from ..experiments.analysis import analyze_study
    t0 = time.time()
    spec = StudySpec.from_dict({
        "name": "smoke", "title": "Smoke test (tiny, not a scientific result)",
        "research_question": "Does the pipeline run end to end?",
        "hypothesis": "Pipeline executes; numbers are meaningless at this budget.",
        "independent_variables": ["pos_method"], "controlled_variables": ["everything else"],
        "primary_metric": "exact-match accuracy", "expected_failure_modes": ["undertrained"],
        "seeds": [0], "eval_seed": 7,
        "model": {"d_model": 32, "n_heads": 2, "n_layers": 2, "d_mlp": 64, "max_positions": 128},
        "train_task": {"seq_len": [16, 32], "n_pairs": [2, 4]},
        "train": {"steps": 60, "batch_size": 32, "eval_every": 30, "log_every": 30, "val_examples": 64},
        "variants": [{"name": "rope", "model": {"pos_method": "rope"}},
                     {"name": "learned", "model": {"pos_method": "learned"}}],
        "eval_grids": [{"name": "length", "vary": {"seq_len": [16, 32, 64]}, "n": 40},
                       {"name": "position", "vary": {"evidence_pos": [0.0, 0.5, 1.0]}, "base": {"seq_len": 32},
                        "n": 40}],
        "analyses": {"leakage_check": 500, "control_n": 64, "position_offset": [0, 32]},
        "reference_variant": "rope",
    })
    res = run_study(spec, workers=1, threads=a.threads, force=True)
    analyze_study("smoke", seeds=(0,), n=24, n_patch=4)
    print(res)
    print(f"smoke finished in {time.time() - t0:.1f}s")
    return 0 if all(r["status"] in ("completed", "cached") for r in res) else 1


def main(argv=None):
    p = argparse.ArgumentParser(prog="ctxlab", description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("env").set_defaults(fn=cmd_env)
    g = sp.add_parser("gen")
    g.add_argument("--set", nargs="*", help="TaskConfig overrides, e.g. task=multihop hops=[2,2] seq_len=64")
    g.add_argument("--n", type=int, default=200)
    g.add_argument("--show", type=int, default=3)
    g.add_argument("--seed", type=int, default=0)
    g.add_argument("--stream", default="cli")
    g.set_defaults(fn=cmd_gen)
    s = sp.add_parser("study")
    s.add_argument("config")
    s.add_argument("--workers", type=int, default=1)
    s.add_argument("--threads", type=int, default=2)
    s.add_argument("--force", action="store_true")
    s.add_argument("--variants")
    s.add_argument("--seeds")
    s.set_defaults(fn=cmd_study)
    ag = sp.add_parser("aggregate")
    ag.add_argument("study")
    ag.set_defaults(fn=cmd_aggregate)
    an = sp.add_parser("analyze")
    an.add_argument("study")
    an.add_argument("--seeds", default="0")
    an.add_argument("--variants")
    an.add_argument("--n", type=int, default=200)
    an.add_argument("--n-patch", type=int, default=32)
    an.set_defaults(fn=cmd_analyze)
    dy = sp.add_parser("dynamics")
    dy.add_argument("study")
    dy.add_argument("--n", type=int, default=300)
    dy.set_defaults(fn=cmd_dynamics)
    ip = sp.add_parser("interp")
    ip.add_argument("study")
    ip.add_argument("--grid", default="length")
    ip.set_defaults(fn=cmd_interp)
    ins = sp.add_parser("inspect")
    ins.add_argument("study")
    ins.add_argument("run")
    ins.add_argument("--set", nargs="*")
    ins.add_argument("--seed", type=int, default=0)
    ins.set_defaults(fn=cmd_inspect)
    d = sp.add_parser("diagnose")
    d.add_argument("study")
    d.add_argument("--run")
    d.set_defaults(fn=cmd_diagnose)
    sp.add_parser("list").set_defaults(fn=cmd_list)
    sp.add_parser("report").set_defaults(fn=cmd_report)
    sm = sp.add_parser("smoke")
    sm.add_argument("--threads", type=int, default=2)
    sm.set_defaults(fn=cmd_smoke)
    a = p.parse_args(argv)
    rc = a.fn(a)
    return rc or 0


if __name__ == "__main__":
    sys.exit(main())
