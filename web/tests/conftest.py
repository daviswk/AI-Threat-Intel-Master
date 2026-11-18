"""A client for the app over a throwaway repo (see fixture_repo.py).

Run from the repo root:
    uv run python -m pytest web/tests -v
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # web/      -> import server
sys.path.insert(0, str(Path(__file__).resolve().parent))       # web/tests -> import fixture_repo

from fastapi.testclient import TestClient  # noqa: E402

from fixture_repo import PORT, TOKEN, build  # noqa: E402
from server.app import create_app  # noqa: E402


@pytest.fixture()
def repo_root(tmp_path: Path) -> Path:
    return build(tmp_path)


@pytest.fixture()
def client(repo_root: Path) -> TestClient:
    app = create_app(token=TOKEN, port=PORT, root=repo_root, dist=repo_root / "no-dist", watch_repo=False)
    with TestClient(app, base_url=f"http://127.0.0.1:{PORT}") as c:
        yield c


@pytest.fixture()
def auth() -> dict:
    return {"X-MC-Token": TOKEN}
