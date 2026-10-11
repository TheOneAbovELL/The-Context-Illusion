"""Minimal markdown table rendering (avoids an extra dependency on ``tabulate``)."""

from __future__ import annotations

import math

import pandas as pd


def _fmt(v, floatfmt: str, as_int: bool) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        if math.isnan(v):
            return "nan"
        return str(int(v)) if as_int else format(v, floatfmt)
    return str(v).replace("|", "\\|")


def _int_like(col: pd.Series) -> bool:
    """Columns whose non-missing values are all whole numbers (e.g. lengths that
    became float because another grid left them empty) print without decimals."""
    if not pd.api.types.is_float_dtype(col):
        return False
    v = col.dropna()
    return len(v) > 0 and bool((v == v.round()).all()) and bool((v.abs() >= 2).any())


def md_table(df: pd.DataFrame, floatfmt: str = ".3f", max_rows: int | None = None) -> str:
    if df is None or df.empty:
        return "_(no rows)_"
    if max_rows is not None and len(df) > max_rows:
        df = df.head(max_rows)
    cols = [str(c) for c in df.columns]
    int_cols = [_int_like(df[c]) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for row in df.itertuples(index=False):
        lines.append("| " + " | ".join(_fmt(v, floatfmt, ic) for v, ic in zip(row, int_cols)) + " |")
    return "\n".join(lines)
