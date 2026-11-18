"""Read spec/CURRICULUM.md and spec/MODULE_LOOP.md as structured sections.

Nothing here rewrites the spec. It only cuts the Markdown at its own headings
so the app can show one module, one stage, and the chain between modules.
"""
from __future__ import annotations

import re

STAGES = ["preflight", "incubation", "ingestion", "lab", "heuristics", "gate", "complete"]
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
MODULE_TITLE = re.compile(r"^Module (\d+):\s*(.*)$")
INPUT_FROM = re.compile(r"Input \(from M(\d+)\)")
STAGE_TITLE = re.compile(r"^Stage (\d): `(\w+)`")

# Productive struggle (CLAUDE.md law 1): while a module is in progress, parts
# of its curriculum section are held back until the stage that needs them.
# Each rule is (heading prefix, first stage at which the block is shown).
# The builder and attacker briefs stay back until the module is complete.
# Set WITHHOLD to False to show every section at every stage.
WITHHOLD = True
WITHHOLD_RULES = [
    ("i/o contract", "preflight"), ("sources", "preflight"),
    ("stage 1", "incubation"),
    ("concepts", "ingestion"), ("reading map", "ingestion"), ("cert mapping", "ingestion"),
    ("stage 3", "lab"), ("3.3", "lab"), ("mental models", "lab"),
    ("register columns", "lab"), ("gate", "lab"),
    ("3.1", "complete"), ("3.2", "complete"),
]
WITHHOLD_DEFAULT = "ingestion"
# Inside "Stage 1", the dilemma is shown at incubation; the description of how
# the contrastive pair differs waits for ingestion.
PAIR_PARAGRAPH = re.compile(r"^\*\*Contrastive pair", re.M)


def _headings(lines: list[str]):
    fenced = False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = HEADING.match(line)
        if m:
            yield i, len(m.group(1)), m.group(2)


def module_sections(text: str) -> dict[int, dict]:
    """{module id: {title, level, blocks, inputs}} for every module heading."""
    lines = text.splitlines()
    heads = list(_headings(lines))
    out: dict[int, dict] = {}
    for idx, (line_no, level, title) in enumerate(heads):
        m = MODULE_TITLE.match(title)
        if not m or level > 2:
            continue
        end = len(lines)
        inner = []
        for later_no, later_level, later_title in heads[idx + 1:]:
            if later_level <= level:
                end = later_no
                break
            inner.append((later_no, later_level, later_title))
        blocks = []
        starts = [(line_no, level, None)] + inner
        for j, (start, blevel, btitle) in enumerate(starts):
            stop = starts[j + 1][0] if j + 1 < len(starts) else end
            body = "\n".join(lines[start + 1:stop]).strip()
            body = re.sub(r"\n-{3,}\s*$", "", body).strip()
            blocks.append({"title": btitle, "level": blevel, "markdown": body})
        whole = "\n".join(lines[line_no:end])
        out[int(m.group(1))] = {
            "title": m.group(2), "level": level, "blocks": blocks,
            "inputs": sorted({int(x) for x in INPUT_FROM.findall(whole)}),
        }
    return out


def edges(sections: dict[int, dict]) -> list[list[int]]:
    """[[from, to], ...] taken only from 'Input (from MN)' lines in the spec."""
    return [[src, mod] for mod in sorted(sections) for src in sections[mod]["inputs"]]


def _first_stage(title: str | None) -> str:
    if title is None:
        return "preflight"
    low = title.casefold()
    for prefix, stage in WITHHOLD_RULES:
        if low.startswith(prefix):
            return stage
    return WITHHOLD_DEFAULT


def briefing(section: dict, *, in_progress: bool, stage: str) -> list[dict]:
    """The module's blocks. For the module in progress, blocks not yet due are
    returned without their text, so held-back content never leaves the server."""
    blocks = []
    now = STAGES.index(stage) if stage in STAGES else 0
    for block in section["blocks"]:
        due = _first_stage(block["title"])
        if not (WITHHOLD and in_progress) or STAGES.index(due) <= now:
            text = block["markdown"]
            cut = None
            if (WITHHOLD and in_progress and block["title"]
                    and block["title"].casefold().startswith("stage 1")
                    and now < STAGES.index("ingestion")):
                cut = PAIR_PARAGRAPH.search(text)
            if cut:
                blocks.append({**block, "markdown": text[:cut.start()].strip(), "withheld": False})
                blocks.append({"title": "Contrastive pair: how it was built", "level": block["level"] + 1,
                               "markdown": "", "withheld": True, "until": "ingestion"})
            else:
                blocks.append({**block, "withheld": False})
        else:
            blocks.append({"title": block["title"], "level": block["level"], "markdown": "",
                           "withheld": True, "until": due})
    return blocks


def stage_sections(text: str) -> dict[str, str]:
    """{stage name: Markdown of its 'Stage N' section} from MODULE_LOOP.md."""
    lines = text.splitlines()
    heads = [h for h in _headings(lines) if h[1] <= 2]
    out: dict[str, str] = {}
    for idx, (line_no, level, title) in enumerate(heads):
        m = STAGE_TITLE.match(title)
        if not m or level != 2:
            continue
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        body = "\n".join(lines[line_no:end]).strip()
        out[m.group(2)] = re.sub(r"\n-{3,}\s*$", "", body).strip()
    return out
