"""Launcher that works without installing the package: ``python ctxlab.py <command>``."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from context_lab.cli.main import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
