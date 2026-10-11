"""Local research interface for The Context Illusion.

Run:  streamlit run app/streamlit_app.py
Every table and figure here is read from the local experiment registry or
computed live from a local checkpoint; nothing is fabricated or fetched.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402
import torch  # noqa: E402

from context_lab.data import (DEFAULT_VOCAB, TaskConfig, TaskSampler, baseline_accuracies, check_example,  # noqa: E402
                              dataset_summary, make_dataset)
from context_lab.diagnostics import evidence_sweep, inspect_example, positional_structure  # noqa: E402
from context_lab.experiments import Registry  # noqa: E402
from context_lab.models import ModelConfig, Transformer, load_checkpoint  # noqa: E402
from context_lab.positional import METHODS  # noqa: E402
from context_lab.reporting import build_lab_report, diagnose_run, diagnosis_markdown  # noqa: E402
from context_lab.utils.env import environment_report  # noqa: E402
from context_lab.visualization import plots  # noqa: E402

st.set_page_config(page_title="The Context Illusion", layout="wide")
reg = Registry()
V = DEFAULT_VOCAB

PAGES = ["1 Environment", "2 Model configuration", "3 Dataset generator", "4 Training runs",
         "5 Length generalisation", "6 Position sensitivity", "7 Distractors & interference",
         "8 Positional-encoding comparison", "9 Example inspection", "10 Attention & activation diagnostics",
         "11 Experiment history", "12 Reports", "13 Shortcut detection & learning dynamics"]
page = st.sidebar.radio("Section", PAGES)
st.sidebar.caption("All data shown come from the local registry:\n" + str(reg.root))


@st.cache_resource
def _load(study: str, run_id: str):
    return load_checkpoint(reg.checkpoint_path(study, run_id))


def pick_study(key: str, default_contains: str | None = None):
    studies = reg.list_studies()
    if not studies:
        st.info("No studies in the registry yet. Run `python ctxlab.py smoke` or a study from the CLI.")
        return None
    idx = next((i for i, s in enumerate(studies) if default_contains and s == default_contains),
               next((i for i, s in enumerate(studies) if default_contains and default_contains in s), 0))
    return st.selectbox("Study", studies, index=idx, key=key)


def pick_run(study: str, key: str):
    rt = reg.runs_table(study)
    rt = rt[rt["status"] == "completed"]
    if rt.empty:
        st.info("No completed runs in this study.")
        return None
    return st.selectbox("Run", rt["run_id"].tolist(), key=key)


def _study_with_grid(name_filter: list[str]) -> str | None:
    """First study (main study preferred) that has an aggregated grid matching the filter."""
    studies = sorted(reg.list_studies(), key=lambda s: (s != "main_pe", s))
    for s in studies:
        if any(any(f in p.stem for f in name_filter) for p in reg.summary_dir(s).glob("grid_*.csv")):
            return s
    return None


def results_page(name_filter: list[str], title: str, default_study: str | None = None):
    st.header(title)
    study = pick_study(f"st_{title}", default_study or _study_with_grid(name_filter))
    if not study:
        return
    sd = reg.summary_dir(study)
    grids = sorted(p.stem.replace("grid_", "") for p in sd.glob("grid_*.csv"))
    sel = [g for g in grids if any(f in g for f in name_filter)] or grids
    if not sel:
        st.info("This study has no aggregated grids yet (run `python ctxlab.py aggregate <study>`).")
        return
    g = st.selectbox("Evaluation grid", sel)
    df = pd.read_csv(sd / f"grid_{g}.csv")
    for suffix in ("", "_heat"):
        p = sd / f"fig_{g}{suffix}.png"
        if p.exists():
            st.image(str(p))
    st.caption("mean = mean accuracy over seeds; min/max = seed range; t_lo/t_hi = t-interval over seeds "
               "(wide with few seeds).")
    st.dataframe(df, use_container_width=True)
    bl = sd / "baselines.csv"
    if bl.exists():
        b = pd.read_csv(bl)
        st.subheader("Algorithmic baselines on the identical examples")
        st.dataframe(b[b["grid"] == g], use_container_width=True)
    pv = sd / "paired_vs_reference.csv"
    if pv.exists() and pv.stat().st_size > 5:
        p = pd.read_csv(pv)
        if not p.empty:
            st.subheader("Paired per-seed differences vs reference variant")
            st.dataframe(p[p["grid"] == g], use_container_width=True)


# ---------------------------------------------------------------------------------------------------------
if page == PAGES[0]:
    st.header("Environment status")
    env = environment_report()
    if env.get("cloud_sync_warning"):
        st.warning(env["cloud_sync_warning"])
    c1, c2 = st.columns(2)
    c1.json(env["software"])
    c2.json(env["hardware"])
    st.write({"results_dir": env["results_dir"], "artifacts_dir": env["artifacts_dir"]})

elif page == PAGES[1]:
    st.header("Model configuration")
    c = st.columns(5)
    method = c[0].selectbox("Positional method", METHODS, index=METHODS.index("rope"))
    d = c[1].selectbox("d_model", [32, 64, 128], index=1)
    h = c[2].selectbox("heads", [2, 4, 8], index=1)
    L = c[3].selectbox("layers", [1, 2, 3, 4], index=1)
    mp = c[4].number_input("max_positions (learned)", 16, 4096, 512)
    cfg = ModelConfig(pos_method=method, d_model=d, n_heads=h, n_layers=L, d_mlp=4 * d, max_positions=int(mp))
    torch.manual_seed(0)
    m = Transformer(cfg)
    st.write({"parameters": m.n_params(), "positional parameters": m.n_params() - m.n_params(True),
              **m.pos.describe()})
    st.json(cfg.to_dict())
    st.subheader("Positional structure (fresh initialisation)")
    s = positional_structure(m, max_pos=256)
    fig, ax = plt.subplots(figsize=(6, 3))
    if "cos_sim" in s:
        ax.imshow(s["cos_sim"], cmap=plots.SEQ_CMAP)
        ax.set_title("cosine similarity between positional vectors")
    elif "bias_by_distance" in s:
        for i, row in enumerate(s["bias_by_distance"]):
            ax.plot(row, label=f"head {i}", color=plots.PALETTE[i % 8])
        ax.legend(fontsize=7)
        ax.set_xlabel("distance")
        ax.set_title("attention bias vs distance")
    elif "mean_qk_by_distance" in s:
        ax.plot(s["mean_qk_by_distance"], color=plots.PALETTE[0])
        ax.set_xlabel("relative distance")
        ax.set_title("RoPE: mean q·k / d_h for q = k (random), vs distance")
    else:
        ax.text(0.5, 0.5, "no explicit positional parameters", ha="center")
    st.pyplot(fig)

elif page == PAGES[2]:
    st.header("Dataset generator")
    task = st.selectbox("Task", ["recall", "multihop"])
    c = st.columns(4)
    L = c[0].slider("seq_len", 12, 512, 64)
    seed = c[1].number_input("seed", 0, 10**6, 0)
    n = c[2].number_input("examples (for validation)", 10, 5000, 300)
    show = c[3].number_input("examples to display", 1, 20, 3)
    if task == "recall":
        c = st.columns(5)
        npairs = c[0].slider("n_pairs", 1, 32, 6)
        pos = c[1].select_slider("evidence_pos", ["random", 0.0, 0.25, 0.5, 0.75, 1.0], "random")
        lures = c[2].slider("n_lures", 0, 6, 0)
        klen = c[3].selectbox("key_len", [1, 2])
        near = c[4].slider("near_miss_frac (key_len=2)", 0.0, 1.0, 0.0)
        cfg = TaskConfig(seq_len=L, n_pairs=npairs, n_lures=lures, key_len=klen, near_miss_frac=near,
                         evidence_pos=None if pos == "random" else float(pos))
    else:
        c = st.columns(4)
        hops = c[0].slider("hops", 1, 4, 2)
        nch = c[1].slider("n_chains", 1, 6, 3)
        order = c[2].selectbox("link_order", ["random", "forward", "backward"])
        qt = c[3].selectbox("query type", ["end", "next"])
        cfg = TaskConfig(task="multihop", seq_len=L, hops=hops, n_chains=nch, link_order=order, query_types=(qt,))
    try:
        exs = make_dataset(cfg, int(n), int(seed), "ui")
        for e in exs[: int(show)]:
            st.code(V.decode(e.tokens) + f"   =>  {V.token_str(e.answer)}")
            st.caption(str(e.public_meta()))
        bad = sum(1 for e in exs if check_example(e))
        (st.success if bad == 0 else st.error)(f"{bad} of {len(exs)} examples violate invariants (oracle check).")
        st.write("Realised distribution:", dataset_summary(exs))
        st.write("Baselines:", baseline_accuracies(exs))
    except Exception as err:  # noqa: BLE001
        st.error(f"Configuration infeasible: {err}")

elif page == PAGES[3]:
    st.header("Training runs")
    study = pick_study("train_study")
    if study:
        rt = reg.runs_table(study)
        st.dataframe(rt, use_container_width=True)
        p = reg.summary_dir(study) / "fig_training_curves.png"
        if p.exists():
            st.image(str(p))
        rid = pick_run(study, "train_run")
        if rid:
            st.line_chart(reg.train_log(study, rid).set_index("step")[["train_loss", "train_acc", "val_acc"]])
    st.subheader("Launch a study (runs in a background process; results appear in the registry)")
    cfgs = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "configs").glob("*.yaml"))
    c = st.columns(3)
    cfg = c[0].selectbox("Spec", cfgs) if cfgs else None
    workers = c[1].number_input("workers", 1, 6, 2)
    threads = c[2].number_input("threads per worker", 1, 6, 2)
    if cfg and st.button("Start study"):
        log = reg.root / "ui_launch.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        with open(log, "a", encoding="utf-8") as fh:
            subprocess.Popen([sys.executable, str(ROOT / "ctxlab.py"), "study", cfg, "--workers", str(workers),
                              "--threads", str(threads)], stdout=fh, stderr=subprocess.STDOUT, cwd=ROOT)
        st.success(f"Started. Log: {log}")
    log = reg.root / "ui_launch.log"
    if log.exists():
        st.text(log.read_text(encoding="utf-8")[-3000:])

elif page == PAGES[4]:
    results_page(["length", "train_len"], "Length generalisation")

elif page == PAGES[5]:
    results_page(["position", "distance"], "Position sensitivity")

elif page == PAGES[6]:
    results_page(["distract", "lure", "repeat", "similar", "near"], "Distractors & interference")

elif page == PAGES[7]:
    results_page([""], "Positional-encoding comparison")

elif page == PAGES[8]:
    st.header("Example-level prediction inspection")
    study = pick_study("ins_study")
    rid = pick_run(study, "ins_run") if study else None
    if rid:
        model, payload = _load(study, rid)
        # the model's own evaluation format (single query only if single queries were in training)
        task = TaskConfig.from_dict(payload["task_config"]).eval_format()
        st.caption(f"Training task of this run: `{payload['task_config']}`")
        c = st.columns(4)
        L = c[0].slider("seq_len", 12, 512, 64)
        seed = c[1].number_input("example seed", 0, 10**6, 0)
        over = {"seq_len": L, "length_choices": None}
        if task.task == "recall":
            pos = c[2].select_slider("evidence_pos", ["random", 0.0, 0.25, 0.5, 0.75, 1.0], "random")
            default_pairs = task.n_pairs if isinstance(task.n_pairs, int) else int(task.n_pairs[1])
            npairs = c[3].slider("n_pairs", 1, 24, default_pairs)
            over.update(n_pairs=npairs, evidence_pos=None if pos == "random" else float(pos))
        try:
            ex = TaskSampler(task.replace(**over), int(seed), "ui-inspect").example()
            r = inspect_example(model, ex)
        except Exception as err:  # noqa: BLE001
            st.error(str(err))
            st.stop()
        st.code(" ".join(r["tokens"]))
        (st.success if r["correct"] else st.error)(
            f"answer {r['answer']} | prediction {r['pred']} | P(answer) = {r['p_answer']:.3f}")
        st.write("Top-k:", r["top_k"])
        st.write("Logit lens (P(answer) after each layer):", pd.DataFrame(r["logit_lens"]))
        st.write("Controlled variables:", r["meta"])
        if task.task == "recall":
            st.subheader("Evidence sweep: same context, only the evidence moves")
            sw = evidence_sweep(model, ex)
            st.line_chart(sw.set_index("evidence_offset")[["p_answer", "resid_cos_to_original"]])
        st.session_state["inspect"] = (study, rid, r)

elif page == PAGES[9]:
    st.header("Attention & activation diagnostics")
    st.warning("Attention weights show where a head reads from; they are not proof of information use. "
               "Causal statements require the intervention results below.")
    if "inspect" in st.session_state:
        study, rid, r = st.session_state["inspect"]
        st.caption(f"Example from page 9, run {rid}")
        A = r["attn"]
        c = st.columns(2)
        layer = c[0].selectbox("layer", list(range(A.shape[0])))
        head = c[1].selectbox("head", list(range(A.shape[1])))
        fig, ax = plt.subplots(figsize=(8, 7))
        plots.attention_heatmap(A[layer, head], r["tokens"], f"layer {layer} head {head}", ax=ax)
        st.pyplot(fig)
        roles = np.array(r["roles"])
        row = A[layer, :, -1]
        df = pd.DataFrame({"role": roles, **{f"head{h}": row[h] for h in range(row.shape[0])}})
        st.write("Attention from <ans> by role (sum):", df.groupby("role").sum())
    else:
        st.info("Inspect an example on page 9 first to see its attention maps.")
    study = pick_study("diag_study")
    if study:
        ad = reg.summary_dir(study) / "analysis"
        rep = ad / "analysis_report.md"
        if rep.exists():
            for img in sorted(ad.glob("fig_*.png")):
                st.image(str(img))
            with st.expander("Full mechanistic analysis report"):
                st.markdown(rep.read_text(encoding="utf-8"))
        else:
            st.info("No analysis yet: `python ctxlab.py analyze <study>`.")

elif page == PAGES[10]:
    st.header("Experiment history")
    for s in reg.list_studies():
        st.subheader(s)
        st.dataframe(reg.runs_table(s), use_container_width=True)
    study = pick_study("hist_study")
    rid = pick_run(study, "hist_run") if study else None
    if rid:
        st.markdown(diagnosis_markdown(diagnose_run(reg, study, rid)))
        st.json(reg.config(study, rid))

elif page == PAGES[12]:
    st.header("Shortcut detection & learning dynamics")
    st.markdown(
        "A high score does not show *how* a model answers. These measured controls ask whether predictions "
        "follow the evidence **content**: `cf_value_edit_rate` = share of predictions that switch to an edited "
        "evidence value (genuine retrieval -> 1; a value-type shortcut -> ~1/n_pairs, shown as "
        "`cf_value_edit_shortcut_reference`); `cf_key_swap_rate` = follows swapped key bindings; "
        "`cf_distractor_edit_rate`, `cf_filler_resample_rate`, `cf_evidence_move_rate` = prediction unchanged "
        "under irrelevant edits; `evidence_removed_acc` should be near chance; `pos_offset_*` shows dependence on "
        "absolute positions with identical content.")
    study = pick_study("sc_study")
    if study:
        sd = reg.summary_dir(study)
        cb = sd / "controls_by_run.csv"
        if cb.exists():
            st.dataframe(pd.read_csv(cb), use_container_width=True)
        bl = sd / "baselines.csv"
        if bl.exists():
            st.subheader("Baselines incl. best fixed-offset (positional shortcut upper bound)")
            st.dataframe(pd.read_csv(bl), use_container_width=True)
        dd = sd / "dynamics"
        if dd.exists():
            st.subheader("Learning dynamics (intermediate checkpoints)")
            for img in sorted(dd.glob("fig_*.png")):
                st.image(str(img))
            p = dd / "dynamics_all.csv"
            if p.exists():
                st.dataframe(pd.read_csv(p), use_container_width=True)
        else:
            st.info("No intermediate checkpoints analysed yet: `python ctxlab.py dynamics <study>`.")

elif page == PAGES[11]:
    st.header("Report generation")
    if st.button("Build combined lab report"):
        path = build_lab_report(reg)
        st.success(path)
    p = reg.artifacts / "reports" / "lab_report.md"
    if p.exists():
        st.markdown(p.read_text(encoding="utf-8"))
    study = pick_study("rep_study")
    if study:
        sp = reg.summary_dir(study) / "study_report.md"
        if sp.exists():
            with st.expander("Study report"):
                st.markdown(sp.read_text(encoding="utf-8"))
