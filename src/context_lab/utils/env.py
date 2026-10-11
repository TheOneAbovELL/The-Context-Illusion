"""Environment audit, paths and software versions (all local; nothing is sent anywhere)."""

from __future__ import annotations

import importlib
import os
import platform
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def results_dir() -> Path:
    """Where run records live. Override with CTXLAB_RESULTS_DIR (e.g. to keep
    results outside a cloud-synced folder)."""
    return Path(os.environ.get("CTXLAB_RESULTS_DIR", PROJECT_ROOT / "experiments" / "results"))


def artifacts_dir() -> Path:
    """Checkpoints and generated reports. Override with CTXLAB_ARTIFACTS_DIR."""
    return Path(os.environ.get("CTXLAB_ARTIFACTS_DIR", PROJECT_ROOT / "artifacts"))


def software_versions() -> dict:
    out = {"python": sys.version.split()[0], "platform": platform.platform()}
    for m in ("torch", "numpy", "pandas", "scipy", "matplotlib", "statsmodels", "yaml", "streamlit"):
        try:
            out[m] = getattr(importlib.import_module(m), "__version__", "?")
        except Exception:  # noqa: BLE001 - optional packages
            out[m] = None
    return out


def hardware() -> dict:
    info = {"processor": platform.processor(), "machine": platform.machine(), "logical_cpus": os.cpu_count()}
    try:
        import psutil
        vm = psutil.virtual_memory()
        info.update(physical_cpus=psutil.cpu_count(logical=False), ram_total_gb=round(vm.total / 2**30, 2),
                    ram_available_gb=round(vm.available / 2**30, 2))
    except Exception:  # noqa: BLE001
        pass
    try:
        import torch
        info.update(torch_threads=torch.get_num_threads(), cuda_available=torch.cuda.is_available())
    except Exception:  # noqa: BLE001
        pass
    return info


def cloud_sync_warning() -> str | None:
    p = str(PROJECT_ROOT).lower()
    for marker in ("onedrive", "dropbox", "google drive", "icloud"):
        if marker in p:
            return (f"Project lives in a '{marker}' folder: files may be synced to that provider's cloud. "
                    "Set CTXLAB_RESULTS_DIR / CTXLAB_ARTIFACTS_DIR to a local, non-synced path to keep "
                    "results and checkpoints strictly on this machine.")
    return None


def environment_report() -> dict:
    return {"software": software_versions(), "hardware": hardware(), "project_root": str(PROJECT_ROOT),
            "results_dir": str(results_dir()), "artifacts_dir": str(artifacts_dir()),
            "cloud_sync_warning": cloud_sync_warning()}
