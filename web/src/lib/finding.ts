/** A 5 C's finding file, per spec/SCHEMAS.md §3: front matter, then five
 *  headings in a fixed order. This only moves the learner's words between
 *  form fields and the file. It writes no prose of its own. */

export const SECTIONS = ["Criteria", "Condition", "Cause", "Consequence", "Corrective action"] as const;
export const STATUSES = ["open", "remediated", "revalidated", "risk_accepted"] as const;
const KEYS = ["id", "module", "control_id", "title", "severity", "evidence", "status"];

export interface Finding {
  id: string; module: string; control_id: string; title: string;
  severity: string; evidence: string; status: string;
  sections: Record<string, string>;
}

export function blankFinding(path: string, moduleId: number): Finding {
  const id = path.split("/").pop()!.replace(/\.md$/, "");
  return {
    id, module: String(moduleId), control_id: "", title: "", severity: "null", evidence: "", status: "open",
    sections: Object.fromEntries(SECTIONS.map((s) => [s, ""])),
  };
}

const needsQuotes = (v: string) => v === "" || /^[\s\-?!&*|>%@`'"[\]{}]|[:#]|\s$/.test(v);

export function composeFinding(f: Finding): string {
  const evidence = f.evidence.split(/[,\n]/).map((s) => s.trim()).filter(Boolean);
  const front = [
    "---",
    `id: ${f.id}`,
    `module: ${f.module}`,
    `control_id: ${needsQuotes(f.control_id) ? JSON.stringify(f.control_id) : f.control_id}`,
    `title: ${needsQuotes(f.title) ? JSON.stringify(f.title) : f.title}`,
    `severity: ${f.severity.trim() || "null"}`,
    `evidence: [${evidence.join(", ")}]`,
    `status: ${f.status}`,
    "---",
  ].join("\n");
  const body = SECTIONS.map((s) => `## ${s}\n\n${(f.sections[s] ?? "").trim()}\n`).join("\n");
  return `${front}\n\n${body}`;
}

/** Returns null when the file is not in the form this editor writes, so the
 *  caller can fall back to a plain text editor and lose nothing. */
export function parseFinding(text: string): Finding | null {
  const m = /^---\n([\s\S]*?)\n---\n?([\s\S]*)$/.exec(text.replace(/\r\n/g, "\n"));
  if (!m) return null;
  const front: Record<string, string> = {};
  for (const line of m[1].split("\n")) {
    if (!line.trim()) continue;
    const kv = /^([a-z_]+):\s*(.*)$/.exec(line);
    if (!kv || !KEYS.includes(kv[1])) return null;
    let value = kv[2];
    if (value.startsWith('"')) {
      try { value = String(JSON.parse(value.replace(/\s+#.*$/, ""))); } catch { return null; }
    } else {
      value = value.replace(/\s+#.*$/, "").trim();
    }
    front[kv[1]] = value;
  }
  let evidence = front.evidence ?? "";
  if (evidence) {
    const list = /^\[(.*)\]$/.exec(evidence);
    if (!list) return null;
    evidence = list[1].split(",").map((s) => s.trim()).filter(Boolean).join(", ");
  }
  const sections: Record<string, string> = Object.fromEntries(SECTIONS.map((s) => [s, ""]));
  const chunks = m[2].split(/^## /m);
  if (chunks[0].trim()) return null;
  for (const chunk of chunks.slice(1)) {
    const nl = chunk.indexOf("\n");
    const title = (nl < 0 ? chunk : chunk.slice(0, nl)).trim();
    if (!(SECTIONS as readonly string[]).includes(title)) return null;
    sections[title] = nl < 0 ? "" : chunk.slice(nl + 1).trim();
  }
  return {
    id: front.id ?? "", module: front.module ?? "", control_id: front.control_id ?? "", title: front.title ?? "",
    severity: front.severity ?? "null", evidence, status: front.status ?? "open", sections,
  };
}
