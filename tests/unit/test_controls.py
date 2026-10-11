"""Regression tests for shortcut controls and counterfactual edits."""

import pytest

from context_lab.data import TaskConfig, check_example, make_dataset, make_rng, oracle
from context_lab.data.baselines import baseline_accuracies, best_fixed_offset
from context_lab.interventions.counterfactual import EDITS, EXPECT, apply_edit


def test_shuffled_induction_has_no_positional_solution():
    """Regression: the original induction sanity check repeated the sequence in the same
    order, so 'copy the token n-1 positions back' solved it without content matching."""
    exs = make_dataset(TaskConfig(task="induction", induction_order="shuffled", seq_len=34), 500, 0, "r")
    acc, _ = best_fixed_offset(exs)
    assert acc < 0.15                                    # ~1/(n-1) = 0.0625 expected
    assert len({e.meta["match_offset"] for e in exs}) >= 10
    assert all(check_example(e) == [] for e in exs)


def test_fixed_induction_is_solved_by_position_alone():
    exs = make_dataset(TaskConfig(task="induction", induction_order="fixed", seq_len=34), 200, 0, "r")
    acc, d = best_fixed_offset(exs)
    assert acc == 1.0 and d == 16
    assert {e.meta["match_offset"] for e in exs} == {17}


def test_induction_aux_targets_and_oracle():
    exs = make_dataset(TaskConfig(task="induction", n_queries="all", seq_len=(20, 41)), 200, 1, "a")
    for e in exs:
        assert check_example(e) == []
        assert oracle(e) == e.answer
        assert len(e.meta["_aux"]) == e.meta["half_len"] - 2


def test_recall_eval_has_no_strong_positional_shortcut():
    exs = make_dataset(TaskConfig(seq_len=64, query_format="ans_marker"), 500, 0, "p")
    assert baseline_accuracies(exs)["best_fixed_offset"] < 0.25


@pytest.mark.parametrize("fmt", ["ans_marker", "key_last"])
@pytest.mark.parametrize("edit", EDITS)
def test_counterfactual_edits_define_the_right_target(edit, fmt):
    rng = make_rng(0, "cf-test")
    exs = make_dataset(TaskConfig(seq_len=(32, 64), n_pairs=(2, 8), n_lures=(0, 1), query_format=fmt), 150, 0, "cf")
    applied = 0
    for ex in exs:
        r = apply_edit(ex, edit, rng)
        if r is None:
            continue
        new, target = r
        applied += 1
        assert check_example(new) == [], (edit, check_example(new))
        assert oracle(new) == target                    # the edit's stated target is the true answer
        if EXPECT[edit] == "stay":
            assert target == ex.answer
        else:
            assert target != ex.answer or edit == "key_swap"
        assert len(new.tokens) == len(ex.tokens)
    assert applied > 100


def test_displayed_aux_answers_create_an_elimination_shortcut():
    """Regression (found 2026-10-11): '<qry> K <ans> V' auxiliary blocks display distractor values;
    when every pair is queried the scored answer is the only undisplayed value."""
    cfg = TaskConfig(n_pairs=4, n_lures=0, n_queries=4, single_query_prob=0.0, query_format="ans_marker",
                     seq_len=48, aux_show_answers=True)
    b = baseline_accuracies(make_dataset(cfg, 400, 0, "elim"))
    assert b["elimination"] > 0.85 and b["random_context"] < 0.35


def test_hidden_aux_answers_remove_the_elimination_shortcut():
    cfg = TaskConfig(n_pairs=(2, 8), n_lures=(0, 1), n_queries="all", single_query_prob=0.25,
                     query_format="ans_marker", seq_len=(24, 64), aux_show_answers=False)
    exs = make_dataset(cfg, 400, 0, "hidden")
    b = baseline_accuracies(exs)
    assert abs(b["elimination"] - b["random_context"]) < 1e-9
    for e in exs:
        assert check_example(e) == []
        assert not any(t in e.meta["_aux_region"] for _, t in e.meta["_aux"])   # no answer token inserted
        for pos, ans in e.meta["_aux"]:
            assert e.tokens[pos] == 3                                         # supervised at <ans>


def test_knockout_handles_more_than_one_chunk_per_length():
    """Regression: the knockout hook was built per length group but applied to predict()'s own
    sub-batches of 128, so groups larger than 128 mis-indexed (crash at example 129)."""
    import torch

    from context_lab.interventions.causal import evidence_positions, knockout_predict
    from context_lab.models import ModelConfig, Transformer
    torch.manual_seed(0)
    model = Transformer(ModelConfig(d_model=16, n_heads=2, n_layers=1, d_mlp=32)).eval()
    exs = make_dataset(TaskConfig(seq_len=24, n_pairs=3), 300, 0, "ko")       # one length, 300 examples
    full = knockout_predict(model, exs, 0, evidence_positions)
    single = [knockout_predict(model, [e], 0, evidence_positions).iloc[0] for e in exs[125:135]]
    assert len(full) == 300
    for k, row in enumerate(single):                                          # identical to one-by-one
        assert abs(full.iloc[125 + k]["loss"] - row["loss"]) < 1e-4
