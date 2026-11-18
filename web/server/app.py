"""FastAPI app. Reads are open to the local page; every write and every
subprocess needs the per-launch token (see security.py)."""
from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import content, curriculum, derive, runner, watch, writes
from .paths import PathRefused, Repo
from .security import Guard

REPO_ROOT = Path(__file__).resolve().parents[2]


class SaveBody(BaseModel):
    path: str
    content: str
    base_sha256: str | None = None


class HeuristicBody(BaseModel):
    pattern: str
    verify: str
    evidence: str
    base_sha256: str | None = None


def error(status: int, kind: str, reason: str, **extra) -> JSONResponse:
    return JSONResponse({"error": kind, "reason": reason, **extra}, status_code=status)


def create_app(*, token: str, port: int, root: Path | None = None, dist: Path | None = None,
               watch_repo: bool = True, extra_origins: tuple[str, ...] = ()) -> Guard:
    repo = Repo(root or REPO_ROOT)
    dist = dist if dist is not None else repo.root / "web" / "dist"
    hub = watch.Hub()
    stop = asyncio.Event()
    busy: set[str] = set()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        task = asyncio.create_task(watch.run(repo, hub, stop)) if watch_repo else None
        yield
        stop.set()
        if task:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    app = FastAPI(title="Mission Control", docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)

    @app.exception_handler(PathRefused)
    async def _refused(_, exc: PathRefused):
        return error(403, "refused", exc.reason)

    @app.exception_handler(FileNotFoundError)
    async def _missing(_, exc: FileNotFoundError):
        return error(404, "not_found", "no such file")

    @app.exception_handler(content.TooLarge)
    async def _large(_, exc: content.TooLarge):
        return error(413, "too_large", "file is too large to show")

    @app.exception_handler(runner.Unavailable)
    async def _unavailable(_, exc: runner.Unavailable):
        return error(503, "unavailable", str(exc))

    @app.exception_handler(ValueError)
    async def _bad_state(_, exc: ValueError):
        return error(500, "state_unreadable", str(exc))

    def spec_sections() -> dict[int, dict]:
        return curriculum.module_sections(content.read_text(repo, "spec/CURRICULUM.md") or "")

    def module_of(state: dict, module_id: int) -> dict:
        return state["modules"][module_id - 1]

    # ---------- session ----------
    @app.get("/api/session")
    def session():
        return {"token": token}

    # ---------- read path ----------
    @app.get("/api/overview")
    def overview():
        state = content.read_state(repo)
        return derive.overview(repo, state, curriculum.edges(spec_sections()))

    @app.get("/api/state/validity")
    def validity():
        """Runs scripts/validate_state.py. The schema is not reimplemented here."""
        code, output = runner.run_capture(repo, runner.validate_command())
        return {"valid": code == 0, "output": output}

    @app.get("/api/module/{module_id}/room")
    def room(module_id: int):
        if not 1 <= module_id <= 12:
            return error(404, "not_found", "no such module")
        state = content.read_state(repo)
        module = module_of(state, module_id)
        is_current = module_id == state["current_module"] and module["status"] != "complete"
        stage = state["current_stage"] if is_current else ("complete" if module["status"] == "complete" else "preflight")
        section = spec_sections().get(module_id)
        lab = content.lab(repo, state, module)
        stages = curriculum.stage_sections(content.read_text(repo, "spec/MODULE_LOOP.md") or "")
        return {
            "module": {"id": module_id, "slug": module["slug"], "title": module["title"], "status": module["status"]},
            "stage": stage, "is_current": is_current,
            "briefing": curriculum.briefing(section, in_progress=is_current, stage=stage) if section else [],
            "stage_markdown": stages.get(stage, ""),
            "banner": derive.banner(stage, lab) if is_current else {"where": "app", "text": "This is not the module in progress."},
            "prompts": derive.prompts(module_id, stage) if is_current else [],
            "literature": content.literature(repo, module_id),
            "lab": lab,
            "results": content.results(repo, module_id),
            "harness_target": runner.harness_target(repo, state["current_module"]),
            "heuristics_sha256": content.heuristics(repo)["sha256"],
        }

    @app.get("/api/file")
    def read_file(path: str = Query(..., max_length=400)):
        return content.file_payload(repo, path, content.read_state(repo))

    @app.get("/api/arsenal")
    def arsenal():
        cards = content.flashcards(repo)
        return {"heuristics": content.heuristics(repo), "flashcards": cards,
                "certs": content.cert_counts(cards), "portfolio": content.portfolio(repo)}

    # ---------- write path (token required by the guard) ----------
    @app.put("/api/authored")
    def save(body: SaveBody):
        state = content.read_state(repo)
        try:
            return writes.save_authored(repo, state, body.path, body.content, body.base_sha256)
        except writes.Stale as exc:
            disk = exc.disk
            return error(409, "stale", "The file changed on disk since you loaded it. Nothing was written.",
                         disk_sha256=None if disk is None else content.sha256(disk),
                         disk_content=None if disk is None else disk.decode("utf-8", errors="replace"))
        except writes.BadInput as exc:
            return error(422, "bad_input", str(exc))

    @app.post("/api/heuristics")
    def add_heuristic(body: HeuristicBody):
        state = content.read_state(repo)
        try:
            return writes.append_heuristic(repo, state, body.pattern, body.verify, body.evidence, body.base_sha256)
        except writes.Stale:
            return error(409, "stale", "HEURISTICS.md changed on disk since you loaded it. Nothing was written.")
        except writes.BadInput as exc:
            return error(422, "bad_input", str(exc))

    # ---------- subprocesses (fixed commands; token required) ----------
    @app.get("/api/sync/preview")
    def sync_preview():
        return {"files": runner.git_status(repo)}

    @app.post("/api/run/{name}")
    async def run(name: Literal["harness", "sync_down", "sync_up"]):
        if name in busy:
            return error(409, "busy", f"{name} is already running")
        finish = None
        junit = None
        if name == "harness":
            state = content.read_state(repo)
            junit = runner.junit_tempfile()
            cmd = runner.harness_command(repo, state["current_module"], junit)

            def finish(code: int) -> dict:
                tests = runner.parse_junit(junit)
                junit.unlink(missing_ok=True)
                note = "no harness tests yet (expected before the first lab)" if code == 5 else None
                return {"tests": tests, "note": note}
        else:
            cmd = runner.sync_command(name)
        busy.add(name)

        async def body():
            try:
                shown = " ".join(["uv" if name == "harness" else "bash", *cmd[1:]]) if cmd else ""
                if junit is not None:
                    shown = shown.rsplit(" --junitxml=", 1)[0]
                yield (json.dumps({"t": "cmd", "d": shown}) + "\n").encode()
                async for chunk in runner.stream(repo, cmd, finish):
                    yield chunk
            finally:
                busy.discard(name)
                if junit is not None:
                    junit.unlink(missing_ok=True)

        return StreamingResponse(body(), media_type="application/x-ndjson")

    # ---------- live updates ----------
    @app.get("/api/events")
    async def events():
        queue = hub.subscribe()

        async def body():
            try:
                yield b"retry: 2000\n\n: connected\n\n"
                while not stop.is_set():
                    try:
                        topics = await asyncio.wait_for(queue.get(), timeout=15)
                        yield f"event: change\ndata: {json.dumps(topics)}\n\n".encode()
                    except asyncio.TimeoutError:
                        yield b": keepalive\n\n"
            finally:
                hub.unsubscribe(queue)

        return StreamingResponse(body(), media_type="text/event-stream")

    @app.api_route("/api/{rest:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], include_in_schema=False)
    def no_such_api(rest: str):
        return error(404, "not_found", "no such endpoint")

    # ---------- the built frontend ----------
    if (dist / "index.html").is_file():
        app.mount("/", StaticFiles(directory=dist, html=True), name="ui")
    else:
        @app.get("/")
        def not_built():
            return PlainTextResponse(
                "Mission Control's frontend is not built yet.\n"
                "Run:  uv run python scripts/start_ui.py\n"
                "It builds web/dist (needs Node 22.12 or newer) and starts the app.\n", status_code=503)

    app.state.repo = repo
    app.state.hub = hub
    return Guard(app, token=token, port=port, extra_origins=extra_origins)
