"""Phase 0 environment audit for the machine it runs on.

Collects the environment facts Phase 0 recorded for the desktop, runs the
model-routing check, decides whether travel mode applies, and writes one
section into spec/PHASE0.md. The section is delimited by markers, so re-running
replaces it instead of appending a duplicate.

Usage (from the repo root):
    uv run python scripts/phase0_audit.py --label "Laptop Environment" --write
    uv run python scripts/phase0_audit.py --skip-routing        # print only

No hostnames, user names, or paths are recorded: the output is committed.
"""
from __future__ import annotations

import argparse
import datetime
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PHASE0 = ROOT / "spec" / "PHASE0.md"

TOOLS = ["git", "uv", "node", "docker", "make", "gh", "opa", "gcloud", "tofu",
         "terraform", "ollama", "garak", "promptfoo"]


def run(cmd: list[str], timeout: int = 20) -> str | None:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                             encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    return (out.stdout or out.stderr).strip() or None


def ram_gb() -> float | None:
    system = platform.system()
    try:
        if system == "Windows":
            import ctypes

            class MemStatus(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            status = MemStatus()
            status.dwLength = ctypes.sizeof(MemStatus)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return status.ullTotalPhys / 2**30
        if system == "Darwin":
            out = run(["sysctl", "-n", "hw.memsize"])
            return int(out) / 2**30 if out else None
        for line in pathlib.Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) / 2**20
    except Exception:
        return None
    return None


def gpu() -> tuple[str, float | None, str]:
    """Return (description, dedicated VRAM in GB or None, kind)."""
    out = run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"])
    if out:
        name, _, mem = out.splitlines()[0].partition(",")
        try:
            vram = float(mem.strip()) / 1024
        except ValueError:
            vram = None
        return (f"{name.strip()}, {vram:.0f} GB VRAM" if vram else name.strip(), vram, "nvidia")
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        chip = run(["sysctl", "-n", "machdep.cpu.brand_string"]) or "Apple Silicon"
        return (f"{chip} (integrated GPU, unified memory)", None, "apple-silicon")
    return ("no discrete NVIDIA GPU detected", None, "none")


def first_line(text: str | None) -> str:
    return text.splitlines()[0].strip() if text else "missing"


def routing(skip: bool) -> tuple[str, list[str]]:
    if skip:
        return "NOT RUN (--skip-routing)", []
    if not shutil.which("claude"):
        return "NOT RUN (claude CLI not found)", []
    proc = subprocess.run([sys.executable, str(ROOT / "scripts" / "verify_routing.py")],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    rows = [ln for ln in proc.stdout.splitlines()
            if re.match(r"^(first-line-engineer|red-team|assurance-grader)\s", ln)]
    return ("VERIFIED" if proc.returncode == 0 else "NOT VERIFIED"), rows


def build_section(label: str, skip_routing: bool) -> str:
    today = datetime.date.today().isoformat()
    mem = ram_gb()
    gpu_desc, vram, gpu_kind = gpu()
    free = shutil.disk_usage(ROOT).free / 2**30
    travel = not (gpu_kind == "nvidia" and (vram or 0) >= 8)
    route_status, route_rows = routing(skip_routing)

    lines = [
        f"## {label}",
        "",
        f"Audited {today} by `scripts/phase0_audit.py`. Re-running replaces this section.",
        "",
        "| Item | Found |",
        "|---|---|",
        f"| OS | {platform.system()} {platform.release()} ({platform.machine()}) |",
        f"| Python (venv) | {platform.python_version()} |",
        f"| RAM | {f'{mem:.0f} GB' if mem else 'unknown'} |",
        f"| GPU | {gpu_desc} |",
        f"| Free disk (repo volume) | {free:.0f} GB |",
        f"| Claude Code | {first_line(run(['claude', '--version'])) if shutil.which('claude') else 'missing'} |",
        f"| `CLAUDE_CODE_SUBAGENT_MODEL` | {'SET (must be unset)' if os.environ.get('CLAUDE_CODE_SUBAGENT_MODEL') else 'unset'} |",
        f"| Vendored `socratic-tutor` skill | {'present' if (ROOT / '.claude/skills/socratic-tutor/SKILL.md').is_file() else 'MISSING'} |",
        f"| `socratic-tutor` agent file | {'PRESENT (must not exist)' if (ROOT / '.claude/agents/socratic-tutor.md').exists() else 'absent (correct)'} |",
        "",
        "| Tool | Status |",
        "|---|---|",
    ]
    for tool in TOOLS:
        path = shutil.which(tool)
        version = first_line(run([tool, "--version"])) if path else "missing"
        lines.append(f"| `{tool}` | {version} |")
    lines += [
        "",
        f"**Model routing on this machine: {route_status}**",
        "",
    ]
    if route_rows:
        lines += ["```", f"{'subagent':<22}{'frontmatter model':<24}{'served by':<28}result", *route_rows, "```", ""]
    if route_status.startswith("NOT RUN"):
        lines += ["Run `uv run python scripts/verify_routing.py` once Claude Code is installed and logged in.", ""]
    if route_status == "NOT VERIFIED":
        lines += ["A subagent was not served by its frontmatter model. Do not substitute a model; "
                  "confirm the change with the learner first (see §4).", ""]
    lines += [
        f"**travel_mode: {'on' if travel else 'off'}** "
        + ("(no NVIDIA GPU with 8 GB or more; Modules 6–7 use the travel-mode model sizing in §9)."
           if travel else "(NVIDIA GPU with 8 GB or more present; desktop sizing applies).")
    ]
    return "\n".join(lines) + "\n"


def write_section(label: str, section: str) -> None:
    slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
    start, end = f"<!-- env:{slug}:start -->", f"<!-- env:{slug}:end -->"
    block = f"{start}\n{section}{end}\n"
    text = PHASE0.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.S)
    if pattern.search(text):
        text = pattern.sub(lambda _: block, text)
    else:
        text = text.rstrip("\n") + "\n\n" + block
    PHASE0.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote '{label}' section to spec/PHASE0.md")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="Laptop Environment")
    ap.add_argument("--write", action="store_true", help="write the section into spec/PHASE0.md")
    ap.add_argument("--skip-routing", action="store_true")
    args = ap.parse_args()
    section = build_section(args.label, args.skip_routing)
    print(section)
    if args.write:
        write_section(args.label, section)
    return 0


if __name__ == "__main__":
    sys.exit(main())
