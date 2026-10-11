"""End-to-end: training, evaluation grids, position-controlled and longer-length
evaluation, registry records, caching, aggregation, diagnosis and reports."""

import json

import pandas as pd
import pytest

from context_lab.cli.main import main as cli_main
from context_lab.data import TaskConfig, make_dataset
from context_lab.evaluation import GridSpec, evaluate_grid, predict
from context_lab.experiments import Registry, StudySpec, execute_run, resolve_runs, run_study
from context_lab.experiments.aggregate import aggregate_study
from context_lab.experiments.analysis import analyze_study
from context_lab.reporting import build_lab_report, diagnose_run

pytestmark = pytest.mark.slow


def test_small_training_run_learns(tiny_trained):
    model, task, hist, summ = tiny_trained
    assert hist[-1]["train_loss"] < hist[0]["train_loss"]
    assert summ["final_val_acc"] > 0.8          # chance is 1/32
    assert summ["steps_completed"] == 300


def test_position_controlled_and_longer_evaluation(tiny_trained):
    model, task, _, _ = tiny_trained
    g = GridSpec("pos_len", {"seq_len": [16, 48], "evidence_pos": [0.0, 1.0]}, n=40)
    df = evaluate_grid(model, task, g, eval_seed=1, train_len_range=(12, 24))
    assert set(df["cell"]) == {"seq_len=16,evidence_pos=0.0", "seq_len=16,evidence_pos=1.0",
                               "seq_len=48,evidence_pos=0.0", "seq_len=48,evidence_pos=1.0"}
    assert set(df.loc[df["seq_len"] == 48, "length_regime"]) == {"extrapolation"}
    assert set(df.loc[df["seq_len"] == 16, "length_regime"]) == {"in_range"}
    near_start = df[df["cell_evidence_pos"] == 0.0]["evidence_norm_pos"]
    assert (near_start < 0.05).all()
    assert df["correct"].notna().all()


def _spec(tmp_name="itest"):
    return StudySpec.from_dict({
        "name": tmp_name, "title": "integration", "hypothesis": "h", "independent_variables": ["pos_method"],
        "controlled_variables": ["c"], "primary_metric": "acc", "expected_failure_modes": ["f"], "seeds": [0],
        "eval_seed": 3,
        "model": {"d_model": 16, "n_heads": 2, "n_layers": 1, "d_mlp": 32, "max_positions": 40},
        "train_task": {"seq_len": [16, 32], "n_pairs": [1, 3]},
        "train": {"steps": 20, "batch_size": 16, "eval_every": 10, "log_every": 10, "val_examples": 32},
        "variants": [{"name": "learned", "model": {"pos_method": "learned"}},
                     {"name": "rope", "model": {"pos_method": "rope"}}],
        "eval_grids": [{"name": "length", "vary": {"seq_len": [16, 32, 48]}, "n": 12}],
        "analyses": {"leakage_check": 200, "control_n": 24, "position_offset": [0, 16]},
        "reference_variant": "rope",
    })


def test_registry_run_cache_aggregate_report(tmp_path):
    reg = Registry(tmp_path / "results", tmp_path / "artifacts")
    spec = _spec()
    res = run_study(spec, workers=1, threads=1, registry=reg)
    assert {r["status"] for r in res} == {"completed"}
    for run in resolve_runs(spec):
        d = reg.run_dir(spec.name, run.run_id)
        for f in ("config.json", "env.json", "status.json", "train_log.csv", "eval.parquet", "metrics.json",
                  "report.md"):
            assert (d / f).exists(), f
        assert reg.checkpoint_path(spec.name, run.run_id).exists()
        cfg = json.loads((d / "config.json").read_text())
        assert cfg["config_hash"] in run.run_id
        ev = reg.load_eval(spec.name, run.run_id)
        m = reg.metrics(spec.name, run.run_id)
        assert m["validity"]["eval_examples_with_violations"] == 0
        assert m["validity"]["mask_check_max_abs_diff"] < 1e-4
        if run.variant == "learned":
            # seq_len 48 > max_positions 40: refused and recorded, not silently extrapolated
            over = ev[(ev["grid"] == "length") & (ev["seq_len"] == 48)]
            assert (over["status"] == "position_overflow").all() and over["correct"].isna().all()
        else:
            assert (ev["status"] == "ok").all()
    # cached on rerun
    again = run_study(spec, workers=1, threads=1, registry=reg, aggregate=False)
    assert {r["status"] for r in again} == {"cached"}
    rp = aggregate_study(spec.name, reg)
    text = rp.read_text(encoding="utf-8")
    assert "Validity flags" in text and "Grid `length`" in text
    assert (reg.summary_dir(spec.name) / "fig_length.png").exists()
    ps = pd.read_csv(reg.summary_dir(spec.name) / "per_seed_cells.csv")
    assert {"acc", "ci_lo", "ci_hi", "n"} <= set(ps.columns)
    rid = resolve_runs(spec)[0].run_id
    d = diagnose_run(reg, spec.name, rid)
    assert any(c["check"].startswith("data invariants") and c["status"] == "pass" for c in d["checks"])
    analyze_study(spec.name, seeds=(0,), registry=reg, n=12, n_patch=2)
    assert (reg.summary_dir(spec.name) / "analysis" / "analysis_report.md").exists()
    out = build_lab_report(reg, path=tmp_path / "lab.md")
    assert "Diagnosis" in open(out, encoding="utf-8").read()


def test_config_change_changes_run_id():
    a = resolve_runs(_spec())[0]
    s2 = _spec()
    s2.train["steps"] = 21
    b = resolve_runs(s2)[0]
    assert a.run_id != b.run_id and a.variant == b.variant


def test_failed_run_is_recorded(tmp_path):
    reg = Registry(tmp_path / "r", tmp_path / "a")
    spec = _spec("fails")
    spec.train_task["seq_len"] = [4, 5]            # too short to hold any association -> generator error
    run = resolve_runs(spec)[0]
    res = execute_run(run, reg, verbose=False)
    assert res["status"] == "failed"
    st = reg.status("fails", run.run_id)
    assert st["status"] == "failed" and "traceback" in st


def test_cli_gen_runs(capsys):
    assert cli_main(["gen", "--n", "30", "--show", "1", "--set", "task=multihop", "hops=2", "seq_len=48"]) == 0
    out = capsys.readouterr().out
    assert "invariant violations: 0" in out


def test_predict_reports_overflow_rows():
    from context_lab.models import ModelConfig, Transformer
    m = Transformer(ModelConfig(pos_method="learned", d_model=16, n_heads=2, d_mlp=32, max_positions=20))
    exs = make_dataset(TaskConfig(seq_len=(16, 30)), 20, 0, "o")
    df = predict(m, exs)
    assert set(df.loc[df["seq_len"] > 20, "status"]) <= {"position_overflow"}
    assert set(df.loc[df["seq_len"] <= 20, "status"]) <= {"ok"}
