"""Matplotlib figures built only from measured evaluation tables.

Design rules (applied everywhere):
* each positional method keeps one fixed colour *and* marker in every figure
  (identity never depends on colour alone, never on rank);
* one y-axis per chart; accuracy axes span [0, 1] with chance drawn as a
  dotted reference line;
* error bars are labelled with what they represent (seed spread vs Wilson CI);
* the training-length boundary is drawn on length axes so interpolation and
  extrapolation are visually separated.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

# Validated categorical order (reference palette, light mode), assigned per entity.
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
METHOD_ORDER = ["rope", "learned", "sinusoidal", "t5_relative", "alibi", "none"]
MARKERS = ["o", "s", "^", "D", "v", "X", "P", "*"]
TEXT, TEXT2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
SEQ_CMAP = matplotlib.colors.LinearSegmentedColormap.from_list(
    "seq_blue", ["#cde2fb", "#86b6ef", "#3987e5", "#256abf", "#184f95", "#0d366b"])


LINESTYLES = ["-", "--", ":", "-."]


def method_family(name: str) -> str | None:
    """'rope_h2' -> 'rope'; 't5_relative_short' -> 't5_relative'; unknown -> None."""
    for m in sorted(METHOD_ORDER, key=len, reverse=True):
        if name == m or name.startswith(m + "_"):
            return m
    return None


def style_for(name: str, all_names: list[str] | None = None) -> dict:
    """Stable style for an entity. Colour follows the positional-method family (never the
    rank of the entity); variants of the same family differ by line style and marker."""
    names = sorted(set(all_names or [name]) | {name})
    fam = method_family(name)
    if fam is None:
        others = [n for n in names if method_family(n) is None]
        i = len(METHOD_ORDER) + others.index(name)
        return {"color": PALETTE[i % len(PALETTE)], "marker": MARKERS[i % len(MARKERS)], "linestyle": "-"}
    sib = [n for n in names if method_family(n) == fam]
    j = sib.index(name)
    return {"color": PALETTE[METHOD_ORDER.index(fam)], "marker": MARKERS[j % len(MARKERS)],
            "linestyle": LINESTYLES[j % len(LINESTYLES)]}


def _ordered(names) -> list:
    names = list(dict.fromkeys(n for n in names if isinstance(n, str)))
    return sorted(names, key=lambda n: (METHOD_ORDER.index(method_family(n)) if method_family(n) else 99, n))


def _pretty(label: str) -> str:
    return label.replace("cell_", "").replace("_", " ")


def _setup(ax, title: str, xlabel: str, ylabel: str = "exact-match accuracy", chance: float | None = None,
           acc: bool = True):
    ax.set_facecolor(SURFACE)
    ax.set_title(title, fontsize=10, color=TEXT, loc="left")
    ax.set_xlabel(xlabel, fontsize=9, color=TEXT2)
    ax.set_ylabel(ylabel, fontsize=9, color=TEXT2)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.tick_params(colors=TEXT2, labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    if acc:
        ax.set_ylim(-0.02, 1.02)
    if chance is not None:
        ax.axhline(chance, color=TEXT2, linestyle=":", linewidth=1, label=f"chance ({chance:.3f})")


def line_by_entity(agg: pd.DataFrame, x: str, entity: str, title: str, path: Path, xlabel: str | None = None,
                   chance: float | None = None, train_max: float | None = None, logx: bool = False,
                   y: str = "mean", err: tuple[str, str] | None = ("min", "max"), err_label: str = "min-max over seeds",
                   facet: str | None = None, ylabel: str = "exact-match accuracy", acc: bool = True) -> Path:
    """Mean across seeds per entity vs x, with an error band (default min-max over seeds)."""
    facets = sorted(agg[facet].dropna().unique()) if facet else [None]
    ncol = min(len(facets), 3)
    nrow = int(np.ceil(len(facets) / ncol))
    names = _ordered(agg[entity].dropna().unique())
    width = max(4.6 * ncol, 6.5 if len(names) > 4 else 4.6)
    fig, axes = plt.subplots(nrow, ncol, figsize=(width, 3.4 * nrow + 0.35 * ((len(names) + 3) // 4)),
                             squeeze=False, facecolor=SURFACE)
    for k, fv in enumerate(facets):
        ax = axes[k // ncol][k % ncol]
        sub = agg if fv is None else agg[agg[facet] == fv]
        for name in names:
            d = sub[sub[entity] == name].sort_values(x)
            if d.empty:
                continue
            st = style_for(name, names)
            ax.plot(d[x], d[y], color=st["color"], marker=st["marker"], linestyle=st["linestyle"], markersize=5,
                    linewidth=2, label=name)
            if err and err[0] in d and d[err[0]].notna().any():
                ax.fill_between(d[x], d[err[0]], d[err[1]], color=st["color"], alpha=0.07, linewidth=0)
        t = title if fv is None else f"{title}\n{_pretty(facet)} = {fv}"
        _setup(ax, t, _pretty(xlabel or x), ylabel, chance if k == 0 else None, acc)
        if chance is not None and k > 0:
            ax.axhline(chance, color=TEXT2, linestyle=":", linewidth=1)
        if train_max is not None:
            ax.axvline(train_max, color=TEXT2, linestyle="--", linewidth=1)
            ax.text(train_max, 0.02 if acc else ax.get_ylim()[0], " max train length", fontsize=7, color=TEXT2,
                    rotation=90, va="bottom")
        if logx:
            ax.set_xscale("log", base=2)
    for k in range(len(facets), nrow * ncol):
        axes[k // ncol][k % ncol].axis("off")
    handles, labels = axes[0][0].get_legend_handles_labels()
    rows_leg = (len(labels) + 3) // 4
    fig.legend(handles, labels, loc="lower center", ncol=min(len(labels), 4), fontsize=8, frameon=False,
               bbox_to_anchor=(0.5, 0.0))
    fig.text(0.99, 0.005, f"band: {err_label}" if err else "", ha="right", fontsize=7, color=TEXT2)
    fig.tight_layout(rect=(0, 0.07 * rows_leg / max(1, nrow) + 0.03, 1, 1))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def heatmap_grid(agg: pd.DataFrame, row: str, col: str, entity: str, title: str, path: Path,
                 value: str = "mean", fmt: str = "{:.2f}") -> Path:
    """One heatmap per entity (sequential single-hue scale, 0..1)."""
    names = _ordered(agg[entity].dropna().unique())
    ncol = min(len(names), 3)
    nrow = int(np.ceil(len(names) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.4 * ncol, 3.4 * nrow), squeeze=False, facecolor=SURFACE)
    for k, name in enumerate(names):
        ax = axes[k // ncol][k % ncol]
        p = agg[agg[entity] == name].pivot_table(index=row, columns=col, values=value)
        im = ax.imshow(p.values, cmap=SEQ_CMAP, vmin=0, vmax=1, aspect="auto", origin="lower")
        ax.set_xticks(range(p.shape[1]), [str(c) for c in p.columns], fontsize=7, color=TEXT2)
        ax.set_yticks(range(p.shape[0]), [str(r) for r in p.index], fontsize=7, color=TEXT2)
        for i in range(p.shape[0]):
            for j in range(p.shape[1]):
                v = p.values[i, j]
                if not np.isnan(v):
                    ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=6.5,
                            color="#ffffff" if v > 0.55 else TEXT)
        ax.set_title(name, fontsize=9, color=TEXT, loc="left")
        ax.set_xlabel(_pretty(col), fontsize=8, color=TEXT2)
        ax.set_ylabel(_pretty(row), fontsize=8, color=TEXT2)
    for k in range(len(names), nrow * ncol):
        axes[k // ncol][k % ncol].axis("off")
    fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.7, label="accuracy (mean over seeds)")
    fig.suptitle(title, fontsize=10, color=TEXT, x=0.01, ha="left")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    return path


def training_curves(logs: dict[str, pd.DataFrame], path: Path, title: str = "Training curves") -> Path:
    """logs: label -> train_log DataFrame. Colour by method prefix of the label."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), facecolor=SURFACE)
    seen = set()
    names = _ordered({lab.split("|")[0] for lab in logs})
    for lab, df in logs.items():
        name = lab.split("|")[0]
        st = style_for(name, names)
        kw = dict(color=st["color"], linestyle=st["linestyle"], linewidth=1.2, alpha=0.85,
                  label=name if name not in seen else None)
        seen.add(name)
        axes[0].plot(df["step"], df["train_loss"], **kw)
        v = df.dropna(subset=["val_acc"])
        axes[1].plot(v["step"], v["val_acc"], marker=st["marker"], markersize=3, **{**kw, "label": None})
    _setup(axes[0], "train loss (answer CE)", "step", "loss", acc=False)
    _setup(axes[1], "in-distribution validation accuracy", "step")
    axes[0].set_yscale("log")
    rows_leg = (len(names) + 3) // 4
    fig.legend(loc="lower center", ncol=min(len(names), 4), fontsize=8, frameon=False)
    fig.suptitle(title, fontsize=10, color=TEXT, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.07 * rows_leg + 0.03, 1, 0.95))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def attention_heatmap(attn: np.ndarray, tokens: list[str], title: str, path: Path | None = None, ax=None):
    """attn: (T, T) attention matrix for one head."""
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=(7, 6), facecolor=SURFACE)
    ax.imshow(attn, cmap=SEQ_CMAP, vmin=0, vmax=max(1e-6, float(attn.max())))
    ax.set_xticks(range(len(tokens)), tokens, rotation=90, fontsize=5)
    ax.set_yticks(range(len(tokens)), tokens, fontsize=5)
    ax.set_title(title, fontsize=9, loc="left")
    ax.set_xlabel("key position (attended to)", fontsize=8)
    ax.set_ylabel("query position", fontsize=8)
    if own and path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(path, dpi=130)
        plt.close()
    return ax


def bar_by_entity(df: pd.DataFrame, cat: str, entity: str, value: str, title: str, path: Path,
                  ylabel: str = "value", acc: bool = True, err: tuple[str, str] | None = None) -> Path:
    cats = list(dict.fromkeys(df[cat]))
    names = _ordered(df[entity].dropna().unique())
    w = 0.8 / max(1, len(names))
    rows_leg = (len(names) + 3) // 4
    fig, ax = plt.subplots(figsize=(max(6, 1.2 * len(cats) * max(1, len(names)) * 0.45 + 2), 3.6 + 0.3 * rows_leg),
                           facecolor=SURFACE)
    for i, name in enumerate(names):
        d = df[df[entity] == name].set_index(cat).reindex(cats)
        st = style_for(name, names)
        xs = np.arange(len(cats)) + (i - (len(names) - 1) / 2) * w
        yerr = None
        if err and err[0] in d:
            yerr = np.vstack([(d[value] - d[err[0]]).clip(lower=0), (d[err[1]] - d[value]).clip(lower=0)])
        hatch = {"--": "//", ":": "..", "-.": "xx"}.get(st["linestyle"])
        ax.bar(xs, d[value], width=w * 0.92, color=st["color"], label=name, yerr=yerr, hatch=hatch,
               edgecolor=SURFACE, linewidth=0.5, error_kw={"elinewidth": 1, "ecolor": TEXT2, "capsize": 2})
    ax.set_xticks(range(len(cats)), [str(c) for c in cats], fontsize=8, rotation=20)
    _setup(ax, title, _pretty(cat), ylabel, acc=acc)
    fig.legend(*ax.get_legend_handles_labels(), loc="lower center", fontsize=8, frameon=False,
               ncol=min(len(names), 4), bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(rect=(0, 0.08 * rows_leg + 0.03, 1, 1))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path
