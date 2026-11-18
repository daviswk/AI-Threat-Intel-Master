"""The safety rules in section 2.4, proven against a throwaway repo.

    uv run python -m pytest web/tests -v
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from fixture_repo import BUILDER_SECRET, CANARY, PAIR_SECRET, PORT, SLUG, TOKEN
from server.paths import Repo
from server.watch import WATCH_TOPS, topic_for

LAB = f"labs/{SLUG}"
COLD = f"{LAB}/incubation/cold_attempt.md"


def get_file(client, path):
    return client.get("/api/file", params={"path": path})


# ---------------------------------------------------------------- sealed paths
@pytest.mark.parametrize("path", [
    f"{LAB}/.sealed/ANSWER_KEY.md",
    f"{LAB}/.SEALED/ANSWER_KEY.md",
    f"{LAB}/.sealed./ANSWER_KEY.md",
    f"{LAB}/evidence/../.sealed/ANSWER_KEY.md",
    "assurance-harness/generators/sealed_m01.py",
    "assurance-harness/generators/SEALED_m01.py",
    "assurance-harness/generators/m01_gen.py",
    f"{LAB}/data/planted_notes.txt",
])
def test_sealed_and_off_limits_paths_are_refused(client, path):
    r = get_file(client, path)
    assert r.status_code == 403, r.text
    assert CANARY not in r.text


def test_sealed_content_never_appears_in_any_read_endpoint(client):
    for url in ("/api/overview", "/api/module/1/room", "/api/arsenal", "/api/session"):
        r = client.get(url)
        assert r.status_code == 200, (url, r.text)
        assert CANARY not in r.text, url
        assert ".sealed" not in r.text, url
        assert "sealed_" not in r.text, url


def test_sealed_folders_are_not_listed_or_watched(repo_root):
    repo = Repo(repo_root)
    listed = list(repo.walk(LAB))
    assert f"{LAB}/README.md" in listed
    assert not [p for p in listed if ".sealed" in p or "/data/" in p]
    watched = [d.relative_to(repo.root).as_posix() for d in repo.watch_dirs(WATCH_TOPS)]
    assert LAB in watched
    assert not [d for d in watched if ".sealed" in d or d.endswith("/data") or "generators" in d or ".git" in d]
    assert topic_for(f"{LAB}/.sealed/ANSWER_KEY.md") is None
    assert topic_for("assurance-harness/generators/sealed_m01.py") is None


def test_symlink_into_sealed_folder_is_refused(client, repo_root):
    link = repo_root / LAB / "evidence" / "notes.md"
    try:
        os.symlink(repo_root / LAB / ".sealed" / "ANSWER_KEY.md", link)
    except (OSError, NotImplementedError):
        pytest.skip("this machine does not allow creating symlinks")
    r = get_file(client, f"{LAB}/evidence/notes.md")
    assert r.status_code == 403, r.text
    assert CANARY not in r.text


# ------------------------------------------------------------------- traversal
@pytest.mark.parametrize("path", [
    "../outside-secret.txt",
    f"{LAB}/../../outside-secret.txt",
    f"{LAB}/evidence/../../../../outside-secret.txt",
    "/etc/passwd",
    "C:/Windows/win.ini",
    "labs\\" + SLUG + "\\README.md",
    "..\\outside-secret.txt",
    ".git/config",
    ".env",
    "web/server/app.py",
    "scripts/sync_up.sh",
    "",
])
def test_traversal_absolute_and_unlisted_paths_are_refused(client, path):
    r = get_file(client, path)
    assert r.status_code in (403, 422), r.text
    assert CANARY not in r.text


def test_symlink_leaving_the_repo_is_refused(client, repo_root):
    link = repo_root / LAB / "evidence" / "escape.md"
    try:
        os.symlink(repo_root.parent / "outside-secret.txt", link)
    except (OSError, NotImplementedError):
        pytest.skip("this machine does not allow creating symlinks")
    r = get_file(client, f"{LAB}/evidence/escape.md")
    assert r.status_code == 403, r.text
    assert CANARY not in r.text


def test_an_allowlisted_file_is_served(client):
    r = get_file(client, f"{LAB}/README.md")
    assert r.status_code == 200
    assert r.json()["content"] == "# Lab readme\n"


# ----------------------------------------------------------------------- token
def test_write_without_token_is_refused(client, repo_root):
    r = client.put("/api/authored", json={"path": COLD, "content": "x", "base_sha256": None})
    assert r.status_code == 403, r.text
    assert not (repo_root / COLD).exists()


def test_write_with_wrong_token_is_refused(client, repo_root):
    r = client.put("/api/authored", json={"path": COLD, "content": "x", "base_sha256": None},
                   headers={"X-MC-Token": TOKEN + "x"})
    assert r.status_code == 403, r.text
    assert not (repo_root / COLD).exists()


@pytest.mark.parametrize("name", ["harness", "sync_up", "sync_down"])
def test_subprocess_without_token_is_refused(client, name):
    assert client.post(f"/api/run/{name}").status_code == 403


def test_heuristic_append_without_token_is_refused(client, repo_root):
    before = (repo_root / "HEURISTICS.md").read_bytes()
    r = client.post("/api/heuristics", json={"pattern": "a", "verify": "b", "evidence": "c"})
    assert r.status_code == 403
    assert (repo_root / "HEURISTICS.md").read_bytes() == before


def test_write_with_token_lands_where_the_module_loop_expects(client, repo_root, auth):
    r = client.put("/api/authored", json={"path": COLD, "content": "My diagnosis.", "base_sha256": None}, headers=auth)
    assert r.status_code == 200, r.text
    assert (repo_root / LAB / "incubation" / "cold_attempt.md").read_bytes() == b"My diagnosis.\n"
    assert not list((repo_root / LAB / "incubation").glob("*.tmp"))


# ----------------------------------------------------------------- stale write
def test_stale_write_is_refused_and_shows_the_disk_version(client, repo_root, auth):
    first = client.put("/api/authored", json={"path": COLD, "content": "version one", "base_sha256": None}, headers=auth)
    loaded_sha = first.json()["sha256"]
    (repo_root / COLD).write_bytes(b"edited in the terminal\n")      # changed behind the app's back
    r = client.put("/api/authored", json={"path": COLD, "content": "version two", "base_sha256": loaded_sha}, headers=auth)
    assert r.status_code == 409, r.text
    assert r.json()["error"] == "stale"
    assert r.json()["disk_content"] == "edited in the terminal\n"
    assert (repo_root / COLD).read_bytes() == b"edited in the terminal\n"


def test_creating_over_a_file_that_appeared_is_refused(client, repo_root, auth):
    (repo_root / LAB / "incubation").mkdir(parents=True)
    (repo_root / COLD).write_bytes(b"already here\n")
    r = client.put("/api/authored", json={"path": COLD, "content": "mine", "base_sha256": None}, headers=auth)
    assert r.status_code == 409
    assert (repo_root / COLD).read_bytes() == b"already here\n"


# ------------------------------------------------------------- write allowlist
@pytest.mark.parametrize("path", [
    "STATE.json",
    "HEURISTICS.md",
    "spec/CURRICULUM.md",
    f"{LAB}/README.md",
    f"{LAB}/NOTES.md",
    f"{LAB}/.sealed/ANSWER_KEY.md",
    f"{LAB}/incubation/other.md",
    f"{LAB}/incubation/../README.md",
    f"{LAB}/findings/F-02-1.md",
    f"{LAB}/gate/e-extra.md",
    "labs/m02-later-module/incubation/cold_attempt.md",
    "labs/m99-not-a-module/incubation/cold_attempt.md",
    "../outside-secret.txt",
    "web/server/app.py",
])
def test_write_outside_the_narrow_allowlist_is_refused(client, repo_root, auth, path):
    state_before = (repo_root / "STATE.json").read_bytes()
    r = client.put("/api/authored", json={"path": path, "content": "x", "base_sha256": None}, headers=auth)
    assert r.status_code == 403, r.text
    assert (repo_root / "STATE.json").read_bytes() == state_before
    assert (repo_root.parent / "outside-secret.txt").read_text(encoding="utf-8") == CANARY + "\n"


@pytest.mark.parametrize("name", [
    "procedures/LD-AC-03-toe.md", "procedures/LD-AC-03-tod.md", "findings/F-01-1.md",
    "gate/a-raw-trace.md", "gate/d-executive-pitch.md", "incubation/retrospective.md",
])
def test_every_learner_authored_path_is_writable(client, repo_root, auth, name):
    r = client.put("/api/authored", json={"path": f"{LAB}/{name}", "content": "mine", "base_sha256": None}, headers=auth)
    assert r.status_code == 200, r.text
    assert (repo_root / LAB / name).read_bytes() == b"mine\n"


def test_heuristic_is_appended_in_the_schema_format(client, repo_root, auth):
    sha = client.get("/api/arsenal").json()["heuristics"]["sha256"]
    r = client.post("/api/heuristics", headers=auth,
                    json={"pattern": "pattern X", "verify": "control Y", "evidence": "F-01-1", "base_sha256": sha})
    assert r.status_code == 200, r.text
    assert r.json()["id"] == "H-01-1"
    text = (repo_root / "HEURISTICS.md").read_text(encoding="utf-8")
    assert text.endswith("### H-01-1  (Module 01)\nIf pattern X → then verify control Y.\nEvidence: F-01-1\n")
    stale = client.post("/api/heuristics", headers=auth,
                        json={"pattern": "p", "verify": "v", "evidence": "e", "base_sha256": sha})
    assert stale.status_code == 409


# ------------------------------------------------------------- host and origin
def test_foreign_host_is_refused(client):
    assert client.get("/api/overview", headers={"Host": "evil.example"}).status_code == 403
    assert client.get("/api/overview", headers={"Host": f"127.0.0.1:{PORT + 1}"}).status_code == 403


def test_foreign_origin_is_refused(client, auth):
    assert client.get("/api/session", headers={"Origin": "https://evil.example"}).status_code == 403
    r = client.put("/api/authored", json={"path": COLD, "content": "x", "base_sha256": None},
                   headers={**auth, "Origin": "https://evil.example"})
    assert r.status_code == 403


def test_cross_site_fetch_is_refused(client):
    assert client.get("/api/session", headers={"Sec-Fetch-Site": "cross-site"}).status_code == 403


# ------------------------------------------------------------ fixed subprocesses
@pytest.mark.parametrize("name", ["rm -rf .", "harness;echo", "../sync_up", "validate"])
def test_only_named_commands_can_be_run(client, auth, name):
    r = client.post(f"/api/run/{name}", headers=auth)
    assert r.status_code in (404, 422), r.text


# ------------------------------------------------- stage-gated curriculum text
def test_briefing_holds_back_what_the_stage_has_not_earned(client):
    r = client.get("/api/module/1/room")
    assert r.status_code == 200
    assert "A visible dilemma paragraph." in r.text
    assert PAIR_SECRET not in r.text
    assert BUILDER_SECRET not in r.text
    held = [b for b in r.json()["briefing"] if b["withheld"]]
    assert held and all(b["markdown"] == "" for b in held)


def test_contrastive_pair_is_found_and_unlabelled(client):
    pairs = client.get("/api/module/1/room").json()["lab"]["pairs"]
    assert len(pairs) == 1
    assert pairs[0]["files"] == ["decisions.csv"]
    assert set(pairs[0]) == {"name", "a", "b", "files", "only_a", "only_b"}
