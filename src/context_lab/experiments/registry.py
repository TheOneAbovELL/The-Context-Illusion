"""Local experiment registry (plain files; no database, no remote logging).

<results_dir>/<study>/
    study_spec.yaml                  copy of the spec that produced the runs
    runs/<run_id>/
        config.json                  fully resolved RunSpec
        env.json                     software versions + hardware
        status.json                  running | completed | failed (+ error, traceback, timings)
        train_log.csv                training curve (measured)
        eval.parquet                 example-level evaluation rows (measured)
        metrics.json                 machine-readable summary (measured + derived)
        report.md                    human-readable run report
    summary/                         study-level aggregates, plots, analyses, report
<artifacts_dir>/checkpoints/<study>/<run_id>.pt
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from ..utils.env import artifacts_dir, results_dir


def _read_json(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")
    tmp.replace(p)


class Registry:
    def __init__(self, root: Path | None = None, artifacts: Path | None = None):
        self.root = Path(root) if root else results_dir()
        self.artifacts = Path(artifacts) if artifacts else artifacts_dir()

    # paths
    def study_dir(self, study: str) -> Path:
        return self.root / study

    def run_dir(self, study: str, run_id: str) -> Path:
        return self.study_dir(study) / "runs" / run_id

    def summary_dir(self, study: str) -> Path:
        return self.study_dir(study) / "summary"

    def checkpoint_path(self, study: str, run_id: str) -> Path:
        return self.artifacts / "checkpoints" / study / f"{run_id}.pt"

    # queries
    def list_studies(self) -> list[str]:
        if not self.root.exists():
            return []
        return sorted(p.name for p in self.root.iterdir() if (p / "runs").exists())

    def run_ids(self, study: str) -> list[str]:
        d = self.study_dir(study) / "runs"
        return sorted(p.name for p in d.iterdir() if p.is_dir()) if d.exists() else []

    def status(self, study: str, run_id: str) -> dict:
        return _read_json(self.run_dir(study, run_id) / "status.json", {"status": "missing"})

    def config(self, study: str, run_id: str) -> dict:
        return _read_json(self.run_dir(study, run_id) / "config.json", {})

    def metrics(self, study: str, run_id: str) -> dict:
        return _read_json(self.run_dir(study, run_id) / "metrics.json", {})

    def is_complete(self, study: str, run_id: str) -> bool:
        return (self.status(study, run_id).get("status") == "completed"
                and self.checkpoint_path(study, run_id).exists()
                and (self.run_dir(study, run_id) / "eval.parquet").exists())

    def runs_table(self, study: str) -> pd.DataFrame:
        rows = []
        for rid in self.run_ids(study):
            st, cfg, m = self.status(study, rid), self.config(study, rid), self.metrics(study, rid)
            tr = m.get("training", {})
            rows.append({"run_id": rid, "variant": cfg.get("variant"), "seed": cfg.get("seed"),
                         "pos_method": cfg.get("model", {}).get("pos_method"), "status": st.get("status"),
                         "elapsed_s": st.get("elapsed_s"), "error": st.get("error", ""),
                         "final_val_acc": tr.get("final_val_acc"), "final_train_loss": tr.get("final_train_loss"),
                         "steps": tr.get("steps_completed"), "n_params": tr.get("n_params")})
        return pd.DataFrame(rows)

    def train_log(self, study: str, run_id: str) -> pd.DataFrame:
        p = self.run_dir(study, run_id) / "train_log.csv"
        return pd.read_csv(p) if p.exists() else pd.DataFrame()

    def load_eval(self, study: str, run_id: str) -> pd.DataFrame:
        p = self.run_dir(study, run_id) / "eval.parquet"
        return pd.read_parquet(p) if p.exists() else pd.DataFrame()

    def load_all_evals(self, study: str, only_completed: bool = True) -> pd.DataFrame:
        parts = []
        for rid in self.run_ids(study):
            if only_completed and self.status(study, rid).get("status") != "completed":
                continue
            df = self.load_eval(study, rid)
            if df.empty:
                continue
            cfg = self.config(study, rid)
            df.insert(0, "run_id", rid)
            df.insert(1, "variant", cfg.get("variant"))
            df.insert(2, "seed", cfg.get("seed"))
            df.insert(3, "pos_method", cfg.get("model", {}).get("pos_method"))
            parts.append(df)
        return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
