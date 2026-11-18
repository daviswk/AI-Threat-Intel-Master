"""Start Mission Control: the local dashboard over this repo.

Usage (from the repo root):
    uv run python scripts/start_ui.py                # build if needed, serve, open the browser
    uv run python scripts/start_ui.py --no-browser
    uv run python scripts/start_ui.py --port 9000
    uv run python scripts/start_ui.py --no-build     # serve web/dist as it is
    uv run python scripts/start_ui.py --dev          # also accept the Vite dev server (npm run dev)

What it does:
  1. Builds the frontend into web/dist if it is missing or older than its
     sources. This needs Node 22.12 or newer; the first build also needs the
     network once, for `npm ci`. After that the app runs with no network.
  2. Starts the backend on 127.0.0.1 only, with a token generated for this
     launch. The token is kept in memory and never written to disk.
  3. Opens the dashboard in the default browser.

The app reads the repo and writes only files the learner authors. It never
writes STATE.json. See web/server/paths.py for the read and write allowlists.
"""
from __future__ import annotations

import argparse
import pathlib
import secrets
import shutil
import socket
import subprocess
import sys
import threading
import webbrowser

ROOT = pathlib.Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
DIST = WEB / "dist"
MIN_NODE = (22, 12)
BUILD_INPUTS = ["src", "index.html", "package.json", "package-lock.json", "vite.config.ts", "tsconfig.json"]


def newest(paths: list[pathlib.Path]) -> float:
    latest = 0.0
    for p in paths:
        if p.is_file():
            latest = max(latest, p.stat().st_mtime)
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file():
                    latest = max(latest, f.stat().st_mtime)
    return latest


def node_version() -> tuple[int, int] | None:
    node = shutil.which("node")
    if not node:
        return None
    try:
        out = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=20).stdout.strip()
        major, minor = out.lstrip("v").split(".")[:2]
        return int(major), int(minor)
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def ensure_frontend() -> bool:
    """Build web/dist when it is missing or stale. Returns True if dist is usable."""
    index = DIST / "index.html"
    built = index.stat().st_mtime if index.is_file() else 0.0
    if built and built >= newest([WEB / name for name in BUILD_INPUTS]):
        return True
    have = node_version()
    npm = shutil.which("npm")
    need = f"Node {MIN_NODE[0]}.{MIN_NODE[1]} or newer (with npm)"
    if not npm or have is None or have < MIN_NODE:
        found = "not found" if have is None else f"found {have[0]}.{have[1]}"
        if built:
            print(f"WARN: web/dist is older than its sources and cannot be rebuilt: {need} is required ({found}). Serving the existing build.")
            return True
        print(f"FAIL: the frontend is not built and cannot be: {need} is required ({found}).")
        return False
    lock = WEB / "node_modules" / ".package-lock.json"
    if not lock.is_file() or lock.stat().st_mtime < (WEB / "package-lock.json").stat().st_mtime:
        print("== Installing frontend packages (npm ci; needs the network this once) ==")
        if subprocess.run([npm, "ci", "--no-audit", "--no-fund"], cwd=WEB).returncode != 0:
            print("FAIL: npm ci failed. If you are offline, connect once and re-run.")
            return index.is_file()
    print("== Building the frontend (npm run build) ==")
    if subprocess.run([npm, "run", "build"], cwd=WEB).returncode != 0:
        print("FAIL: the frontend build failed.")
        return index.is_file()
    return True


def free_port(preferred: int) -> int:
    for port in range(preferred, preferred + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            try:
                probe.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise SystemExit(f"FAIL: no free port between {preferred} and {preferred + 19}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Start Mission Control on localhost.")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--no-build", action="store_true")
    parser.add_argument("--dev", action="store_true", help="also accept requests from the Vite dev server")
    args = parser.parse_args()

    if not args.no_build and not ensure_frontend():
        return 1

    try:
        import uvicorn
    except ImportError:
        print("FAIL: the UI packages are not installed. Run:  uv sync --frozen")
        return 1
    sys.path.insert(0, str(WEB))
    from server.app import create_app

    port = free_port(args.port)
    extra = ("http://127.0.0.1:5173", "http://localhost:5173") if args.dev else ()
    app = create_app(token=secrets.token_urlsafe(32), port=port, extra_origins=extra)
    url = f"http://127.0.0.1:{port}/"
    print(f"Mission Control: {url}   (Ctrl+C to stop)")
    if not args.no_browser:
        threading.Timer(1.0, webbrowser.open, args=[url]).start()
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning", access_log=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
