import pandas as pd
import pytest

from context_lab.evaluation import accuracy_table, mcnemar_exact, paired_difference, seed_aggregate, wilson_ci


def test_wilson_known_values():
    lo, hi = wilson_ci(50, 100)
    assert lo == pytest.approx(0.4038, abs=1e-3) and hi == pytest.approx(0.5962, abs=1e-3)
    lo, hi = wilson_ci(0, 20)
    assert lo == 0.0 and hi == pytest.approx(0.1611, abs=1e-3)
    lo, hi = wilson_ci(20, 20)
    assert hi == 1.0 and lo == pytest.approx(0.8389, abs=1e-3)


def test_accuracy_table_counts_unsupported():
    df = pd.DataFrame({"g": ["a"] * 4 + ["b"] * 2, "correct": [1, 0, 1, float("nan"), 1, 1], "loss": [0.1] * 6})
    t = accuracy_table(df, ["g"]).set_index("g")
    assert t.loc["a", "n"] == 3 and t.loc["a", "n_unsupported"] == 1
    assert t.loc["a", "acc"] == pytest.approx(2 / 3)
    assert t.loc["b", "acc"] == 1.0


def test_seed_aggregate_and_paired():
    ps = pd.DataFrame({"m": ["x"] * 3 + ["y"] * 3, "seed": [0, 1, 2] * 2, "c": [1] * 6,
                       "acc": [0.9, 0.8, 0.7, 0.5, 0.6, 0.4], "n": [100] * 6})
    ag = seed_aggregate(ps, ["m"]).set_index("m")
    assert ag.loc["x", "mean"] == pytest.approx(0.8) and ag.loc["x", "n_seeds"] == 3
    assert ag.loc["x", "t_lo"] < 0.8 < ag.loc["x", "t_hi"]
    d = paired_difference(ps, "m", "x", "y", ["c"])
    assert d["mean_diff"].iloc[0] == pytest.approx(0.3) and d["seeds_a_better"].iloc[0] == 3


def test_mcnemar():
    r = mcnemar_exact([1, 1, 1, 1, 0], [0, 0, 0, 0, 0])
    assert r["a_only"] == 4 and r["b_only"] == 0 and r["p_value"] == pytest.approx(0.125)
    assert mcnemar_exact([1, 0], [1, 0])["p_value"] == 1.0
