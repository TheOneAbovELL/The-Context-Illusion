"""Scientific validity tests: properties the experiments rely on for their
interpretation (not just "the code runs")."""

from pathlib import Path

import numpy as np
import pytest
import torch

from context_lab.data import TaskConfig, TaskSampler, check_example, make_rng, remove_evidence
from context_lab.data.baselines import baseline_accuracies
from context_lab.evaluation import GridSpec, grid_examples, predict
from context_lab.experiments import load_spec, resolve_runs
from context_lab.interventions import patching_study
from context_lab.models import ModelConfig, Transformer

CONFIG_DIR = Path(__file__).resolve().parents[2] / "configs"
STUDY_CONFIGS = sorted(CONFIG_DIR.glob("study_*.yaml"))


@pytest.mark.parametrize("path", STUDY_CONFIGS, ids=[p.stem for p in STUDY_CONFIGS])
def test_every_study_grid_is_feasible_valid_and_oracle_solvable(path):
    spec = load_spec(path)
    runs = resolve_runs(spec, seeds=[spec.seeds[0]])
    for run in runs:
        max_eval = 0
        for g in run.grids:
            small = GridSpec(g.name, g.vary, g.base, n=15)
            for cell, exs in grid_examples(run.task, small, spec.eval_seed):
                for e in exs:
                    assert check_example(e) == [], (path.name, g.name, cell)
                max_eval = max(max_eval, max(len(e.tokens) for e in exs))
                assert baseline_accuracies(exs)["oracle"] == 1.0
        # the training distribution itself is valid
        tr = [TaskSampler(run.task, 0).example() for _ in range(30)]
        assert all(check_example(e) == [] for e in tr)


@pytest.mark.parametrize("path", STUDY_CONFIGS, ids=[p.stem for p in STUDY_CONFIGS])
def test_spec_declares_scientific_design(path):
    spec = load_spec(path)
    assert spec.hypothesis and spec.independent_variables and spec.controlled_variables
    assert spec.primary_metric and spec.expected_failure_modes and len(spec.seeds) >= 1


def test_position_grid_is_paired_and_isolates_position():
    task = TaskConfig(seq_len=(24, 64), n_pairs=(2, 8))
    g = GridSpec("pos", {"evidence_pos": [0.0, 0.5, 1.0]}, base={"seq_len": 96}, n=60)
    cells = grid_examples(task, g, eval_seed=11)
    content = [[(e.answer, e.meta["n_pairs"], tuple(e.meta["_target_key"])) for e in exs] for _, exs in cells]
    assert content[0] == content[1] == content[2]          # same content in every cell
    pos = [np.mean([e.meta["evidence_norm_pos"] for e in exs]) for _, exs in cells]
    assert pos[0] < 0.02 and abs(pos[1] - 0.5) < 0.02 and pos[2] > 0.98


def test_fixed_distance_grid_separates_distance_from_absolute_position():
    task = TaskConfig()
    g = GridSpec("dist", {"seq_len": [48, 96, 192]}, base={"evidence_distance": 24}, n=30)
    cells = grid_examples(task, g, eval_seed=11)
    for cell, exs in cells:
        assert {e.meta["distance"] for e in exs} == {24}
        assert {e.meta["evidence_value_pos"] for e in exs} == {cell["seq_len"] - 25}


def test_rope_attention_scores_depend_only_on_relative_position():
    torch.manual_seed(0)
    m = Transformer(ModelConfig(pos_method="rope", d_model=32, n_heads=4, d_mlp=64)).eval()
    x = torch.randint(6, 134, (1, 16))
    _, c0 = m.run_with_cache(x)
    _, c1 = m.run_with_cache(x, pos_offset=77)
    for l in range(2):
        s0, s1 = c0[f"L{l}.attn.scores"], c1[f"L{l}.attn.scores"]
        finite = torch.isfinite(s0)
        assert torch.allclose(s0[finite], s1[finite], atol=1e-4)


@pytest.mark.slow
def test_evidence_removed_control_detects_evidence_use(tiny_trained):
    model, task, _, _ = tiny_trained
    exs = [TaskSampler(task, 9, "sci").example() for _ in range(200)]
    rng = make_rng(0, "rm")
    acc = predict(model, exs)["correct"].mean()
    acc_rm = predict(model, [remove_evidence(e, rng) for e in exs])["correct"].mean()
    assert acc > 0.8 and acc_rm < 0.15          # chance = 1/32


@pytest.mark.slow
def test_patching_has_builtin_negative_and_positive_controls(tiny_trained):
    model, task, _, _ = tiny_trained
    exs = [TaskSampler(task.replace(seq_len=20), 5, "patch").example() for _ in range(6)]
    df = patching_study(model, exs, kind="value", max_examples=6)
    assert not df.empty
    L = model.cfg.n_layers
    # positions strictly before the evidence value see identical inputs in clean and corrupt runs -> R = 0
    before = []
    for ei, ex in enumerate(exs):
        vp = ex.meta["evidence_value_pos"]
        before.append(df[(df["example"] == ei) & (df["position"] < vp)])
    before = [b for b in before if not b.empty]
    if before:
        assert np.allclose(np.concatenate([b["restoration"].to_numpy() for b in before]), 0.0, atol=1e-5)
    # patching the final residual at the answer position restores everything -> R = 1
    final = df[(df["layer"] == L) & (df["role"] == "ans")]
    assert np.allclose(final["restoration"], 1.0, atol=1e-4)
