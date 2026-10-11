"""One-command launcher for The Context Illusion.

    python start.py              check the environment, run a quick self-check, open the interface
    python start.py --tests      ... and run the automated test suite first
    python start.py --studies    ... and (re)run every study first (cached runs are skipped)
    python start.py --full       tests + studies + lab report, then the interface
    python start.py --check      checks only, do not open the interface

Everything stays on this machine: the interface listens on localhost only and sends no usage statistics.
Stop the interface with Ctrl+C (only the process this launcher started is stopped).
"""

from __future__ import annotations

import argparse
import importlib
import os
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

REQUIRED = {"torch": "torch", "numpy": "numpy", "pandas": "pandas", "scipy": "scipy", "matplotlib": "matplotlib",
            "yaml": "pyyaml", "statsmodels": "statsmodels", "psutil": "psutil", "pyarrow": "pyarrow"}
UI = {"streamlit": "streamlit"}
TESTS = {"pytest": "pytest"}
# Studies in the order they were run for the published results (configs/study_<name>.yaml).
STUDIES = ["induction", "fillers", "value_type", "density", "shortcut_dose", "main_pe"]


def say(msg: str = "", kind: str = "") -> None:
    mark = {"ok": "[ ok ]", "warn": "[warn]", "fail": "[FAIL]", "step": "\n==>"}.get(kind, "      ")
    print(f"{mark} {msg}" if kind else msg, flush=True)


def ask(question: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    if not sys.stdin or not sys.stdin.isatty():
        return False
    return input(f"{question} [y/N] ").strip().lower() in ("y", "yes")


def run(args: list, **kw) -> int:
    say("$ " + " ".join(str(a) for a in args))
    return subprocess.call([str(a) for a in args], cwd=ROOT, **kw)


# --------------------------------------------------------------------------- checks
def check_python() -> None:
    if sys.version_info < (3, 10):
        say(f"Python {sys.version.split()[0]} found; 3.10 or newer is required.", "fail")
        sys.exit(1)
    say(f"Python {sys.version.split()[0]} ({sys.executable})", "ok")


def missing(packages: dict) -> list:
    out = []
    for module, pip_name in packages.items():
        try:
            importlib.import_module(module)
        except Exception:  # noqa: BLE001 - any import failure counts as missing
            out.append(pip_name)
    return out


def ensure_packages(packages: dict, purpose: str, assume_yes: bool) -> bool:
    need = missing(packages)
    if not need:
        say(f"packages for {purpose}: all present", "ok")
        return True
    say(f"missing packages for {purpose}: {', '.join(need)}", "warn")
    if not ask(f"Install {', '.join(need)} with pip now?", assume_yes):
        say(f"install them with:  {sys.executable} -m pip install {' '.join(need)}")
        return False
    if run([sys.executable, "-m", "pip", "install", *need]) != 0 or missing(packages):
        say("installation failed", "fail")
        return False
    say(f"installed {', '.join(need)}", "ok")
    return True


def environment_summary() -> None:
    from context_lab.utils.env import cloud_sync_warning, hardware, results_dir
    hw = hardware()
    say(f"CPU: {hw.get('processor') or hw.get('machine')}, {hw.get('logical_cpus')} logical cores, "
        f"RAM {hw.get('ram_available_gb', '?')} / {hw.get('ram_total_gb', '?')} GB free", "ok")
    say(f"results folder: {results_dir()}", "ok")
    warning = cloud_sync_warning()
    if warning:
        say(warning, "warn")


def self_check() -> bool:
    """Seconds-long check: data generation + independent oracle, and a forward pass for every positional scheme."""
    import torch

    from context_lab.data import TaskConfig, check_example, collate, make_dataset
    from context_lab.models import ModelConfig, Transformer
    ok = True
    for name, cfg in [("recall", TaskConfig()), ("multihop", TaskConfig(task="multihop")),
                      ("induction", TaskConfig(task="induction"))]:
        try:
            exs = make_dataset(cfg, 100, 0, f"start/{name}")
            problems = [p for e in exs for p in check_example(e)]
            if problems:
                ok = False
                say(f"task {name}: {len(problems)} validator problems, e.g. {problems[0]}", "fail")
            else:
                say(f"task {name}: 100 examples, oracle agrees with every answer", "ok")
        except Exception as e:  # noqa: BLE001
            ok = False
            say(f"task {name}: {type(e).__name__}: {e}", "fail")
    batch = collate(make_dataset(TaskConfig(), 4, 1, "start/forward"))["tokens"]
    for pm in ("none", "learned", "sinusoidal", "t5_relative", "alibi", "rope"):
        try:
            with torch.no_grad():
                logits = Transformer(ModelConfig(pos_method=pm)).eval()(batch)
            assert torch.isfinite(logits).all()
            say(f"model with {pm} positions: forward pass OK {tuple(logits.shape)}", "ok")
        except Exception as e:  # noqa: BLE001
            ok = False
            say(f"model with {pm} positions: {type(e).__name__}: {e}", "fail")
    return ok


# --------------------------------------------------------------------------- long steps
def run_tests() -> bool:
    return run([sys.executable, "-m", "pytest", "-q"]) == 0


def run_studies(workers: int, threads: int, assume_yes: bool) -> bool:
    say("Studies retrain only runs that are not cached. On a fresh copy this takes several hours on a laptop CPU.")
    if not ask("Run all studies now?", assume_yes):
        say("studies skipped")
        return True
    logs = ROOT / "experiments" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    ok = True
    for study in STUDIES:
        say(f"study {study} (log: experiments/logs/study_{study}.log)", "step")
        with open(logs / f"study_{study}.log", "a", encoding="utf-8") as fh:
            code = run([sys.executable, "ctxlab.py", "study", f"configs/study_{study}.yaml",
                        "--workers", workers, "--threads", threads], stdout=fh, stderr=subprocess.STDOUT)
        say(f"study {study}: exit code {code}", "ok" if code == 0 else "fail")
        ok &= code == 0
    return ok


# --------------------------------------------------------------------------- interface
def port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def launch_ui(port: int, open_browser: bool) -> int:
    first = port
    while not port_free(port):
        port += 1
        if port > first + 20:
            say(f"no free port between {first} and {port}", "fail")
            return 1
    if port != first:
        say(f"port {first} is in use by another program (left untouched); using {port}", "warn")
    url = f"http://localhost:{port}"
    proc = subprocess.Popen([sys.executable, "-m", "streamlit", "run", str(ROOT / "app" / "streamlit_app.py"),
                             "--server.port", str(port), "--server.address", "localhost",
                             "--server.headless", "true", "--browser.gatherUsageStats", "false"], cwd=ROOT)
    for _ in range(120):                                  # wait up to 60 s for the server
        if proc.poll() is not None:
            say("the interface stopped during start-up (see messages above)", "fail")
            return proc.returncode or 1
        if not port_free(port):
            break
        time.sleep(0.5)
    say(f"interface running at {url}  (Ctrl+C to stop)", "ok")
    if open_browser:
        webbrowser.open(url)
    try:
        return proc.wait()
    except KeyboardInterrupt:
        say("stopping the interface ...")
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tests", action="store_true", help="run the automated test suite")
    p.add_argument("--studies", action="store_true", help="run every study (cached runs are skipped)")
    p.add_argument("--full", action="store_true", help="tests + studies + lab report, then the interface")
    p.add_argument("--check", action="store_true", help="checks only; do not start the interface")
    p.add_argument("--port", type=int, default=8501)
    p.add_argument("--no-browser", action="store_true", help="do not open a browser tab")
    p.add_argument("--workers", type=int, default=3, help="parallel training runs for --studies")
    p.add_argument("--threads", type=int, default=2, help="CPU threads per training run")
    p.add_argument("-y", "--yes", action="store_true", help="answer yes to prompts (installs, long studies)")
    a = p.parse_args()
    os.chdir(ROOT)
    if a.full:
        a.tests = a.studies = True

    say("The Context Illusion: start-up", "step")
    check_python()
    if not ensure_packages(REQUIRED, "the laboratory", a.yes):
        return 1
    environment_summary()

    say("Quick self-check", "step")
    if not self_check():
        say("self-check failed; fix the problems above before running experiments", "fail")
        return 1

    if a.tests:
        say("Automated tests", "step")
        if not ensure_packages(TESTS, "tests", a.yes) or not run_tests():
            say("tests failed or could not run", "fail")
            return 1
    if a.studies:
        say("Studies", "step")
        if not run_studies(a.workers, a.threads, a.yes):
            say("at least one study failed; see experiments/logs/", "warn")
    if a.full:
        say("Lab report", "step")
        run([sys.executable, "ctxlab.py", "report"])
    if a.check:
        say("checks finished", "ok")
        return 0

    say("Interface", "step")
    if not ensure_packages(UI, "the interface", a.yes):
        return 1
    return launch_ui(a.port, not a.no_browser)


if __name__ == "__main__":
    sys.exit(main())
