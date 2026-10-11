"""Statistics used in reports.

* Wilson score interval for a binomial proportion (per run, per cell). It is
  well behaved near 0 and 1, unlike the normal approximation. It treats
  examples as independent draws from the cell's generating distribution; it
  says nothing about seed-to-seed (training) variability.
* Across seeds: mean, sample std, and a t-based 95% interval of the mean. With
  3 seeds that interval is wide (t_{0.975,2} = 4.30) -- this is intended: the
  report must not overstate certainty.
* Paired method comparison: per-seed differences on the *same* evaluation
  examples; we report the mean difference, its t-interval, and how many seeds
  agree in sign. We do not claim significance from a single seed.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats as sstats


def wilson_ci(k: float, n: float, z: float = 1.959964) -> tuple[float, float]:
    if n <= 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


def accuracy_table(df: pd.DataFrame, by: list[str], correct_col: str = "correct") -> pd.DataFrame:
    """Per-group n, accuracy and Wilson 95% CI. Rows with NaN ``correct``
    (e.g. unsupported positions) are counted separately as ``n_unsupported``."""
    rows = []
    for key, g in df.groupby(by, dropna=False, sort=True):
        key = key if isinstance(key, tuple) else (key,)
        valid = g[correct_col].dropna()
        n, k = len(valid), float(valid.sum())
        lo, hi = wilson_ci(k, n)
        row = dict(zip(by, key))
        row.update(n=n, n_unsupported=int(g[correct_col].isna().sum()), acc=k / n if n else float("nan"),
                   ci_lo=lo, ci_hi=hi, err_rate=1 - k / n if n else float("nan"))
        if "loss" in g:
            row["mean_loss"] = float(g["loss"].mean())
        if "p_answer" in g:
            row["mean_p_answer"] = float(g["p_answer"].mean())
        rows.append(row)
    return pd.DataFrame(rows)


def t_interval(x, conf: float = 0.95) -> tuple[float, float]:
    x = np.asarray([v for v in x if not np.isnan(v)], dtype=float)
    if len(x) < 2:
        return (float("nan"), float("nan"))
    m, se = x.mean(), x.std(ddof=1) / math.sqrt(len(x))
    t = sstats.t.ppf(0.5 + conf / 2, len(x) - 1)
    return (m - t * se, m + t * se)


def seed_aggregate(per_seed: pd.DataFrame, by: list[str], value: str = "acc", seed_col: str = "seed") -> pd.DataFrame:
    """Aggregate a per-(group, seed) table across seeds."""
    rows = []
    for key, g in per_seed.groupby(by, dropna=False, sort=True):
        key = key if isinstance(key, tuple) else (key,)
        v = g[value].to_numpy(dtype=float)
        ok = v[~np.isnan(v)]
        lo, hi = t_interval(ok)
        nan = float("nan")
        row = dict(zip(by, key))
        row.update(n_seeds=len(ok), mean=float(ok.mean()) if len(ok) else nan,
                   std=float(ok.std(ddof=1)) if len(ok) > 1 else nan,
                   min=float(ok.min()) if len(ok) else nan, max=float(ok.max()) if len(ok) else nan,
                   t_lo=lo, t_hi=hi)
        if "n" in g:
            row["n_per_seed"] = int(g["n"].median())
        rows.append(row)
    return pd.DataFrame(rows)


def paired_difference(per_seed: pd.DataFrame, method_col: str, a: str, b: str, by: list[str],
                      value: str = "acc", seed_col: str = "seed") -> pd.DataFrame:
    """Mean of (a - b) across seeds that have both, per group in ``by``."""
    pa = per_seed[per_seed[method_col] == a].set_index(by + [seed_col])[value]
    pb = per_seed[per_seed[method_col] == b].set_index(by + [seed_col])[value]
    d = (pa - pb).dropna().reset_index()
    rows = []
    for key, g in d.groupby(by, sort=True):
        key = key if isinstance(key, tuple) else (key,)
        v = g[value].to_numpy()
        lo, hi = t_interval(v)
        rows.append({**dict(zip(by, key)), "a": a, "b": b, "mean_diff": float(v.mean()), "t_lo": lo,
                     "t_hi": hi, "n_seeds": len(v), "seeds_a_better": int((v > 0).sum()),
                     "seeds_b_better": int((v < 0).sum())})
    return pd.DataFrame(rows)


def mcnemar_exact(correct_a, correct_b) -> dict:
    """Exact McNemar test on paired per-example outcomes of two models on the
    same examples (within one seed). Tests example-level, not training-level,
    variability."""
    a, b = np.asarray(correct_a, bool), np.asarray(correct_b, bool)
    n01, n10 = int((~a & b).sum()), int((a & ~b).sum())
    n = n01 + n10
    p = 1.0 if n == 0 else min(1.0, 2 * sstats.binom.cdf(min(n01, n10), n, 0.5))
    return {"a_only": n10, "b_only": n01, "p_value": p}
