"""Entry point for the Larkspur Desk access simulator.

From the repo root:
    uv run --frozen python labs/m01-risk-controls-independence/larkspur_cli.py --help
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from larkspur.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
