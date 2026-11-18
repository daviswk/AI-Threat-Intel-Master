import { useState } from "react";
import { ApiError, send } from "../../api/client";
import type { Arsenal } from "../../api/types";
import { ErrorNote, Loading } from "../../components/ui";
import { useResource, useToast } from "../../lib/repo";

const pad = (n: number) => String(n).padStart(2, "0");

/** Appends one "If X → then verify Y" entry to HEURISTICS.md in the
 *  spec/SCHEMAS.md §5 format. The entry's words are the learner's. */
export function HeuristicForm({ moduleId }: { moduleId: number }) {
  const arsenal = useResource<Arsenal>("/api/arsenal", ["heuristics"]);
  const toast = useToast();
  const [x, setX] = useState("");
  const [y, setY] = useState("");
  const [evidence, setEvidence] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  if (arsenal.error) return <div className="pad"><ErrorNote>{arsenal.error}</ErrorNote></div>;
  if (!arsenal.data) return <Loading what="HEURISTICS.md" />;
  const { heuristics } = arsenal.data;
  if (!heuristics.exists) return <p className="empty pad">HEURISTICS.md does not exist in this repo.</p>;

  const n = Math.max(0, ...heuristics.entries.filter((h) => h.module === moduleId).map((h) => h.n)) + 1;
  const id = `H-${pad(moduleId)}-${n}`;
  const ready = x.trim() && y.trim() && evidence.trim();
  const preview = `### ${id}  (Module ${pad(moduleId)})\nIf ${x.trim().replace(/\.$/, "") || "<X>"} → then verify ${y.trim().replace(/\.$/, "") || "<Y>"}.\nEvidence: ${evidence.trim() || "<evidence>"}`;

  const append = async () => {
    setBusy(true);
    setError(null);
    try {
      const res = await send<{ id: string }>("POST", "/api/heuristics",
        { pattern: x, verify: y, evidence, base_sha256: heuristics.sha256 });
      toast(`Appended ${res.id} to HEURISTICS.md`);
      setX(""); setY(""); setEvidence("");
      arsenal.reload();
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "The backend did not answer.");
      arsenal.reload();
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="heur-form" onSubmit={(e) => { e.preventDefault(); if (ready) void append(); }}>
      <label className="field"><span className="eyebrow">If (architectural pattern X)</span>
        <input className="input" value={x} onChange={(e) => setX(e.target.value)} /></label>
      <label className="field"><span className="eyebrow">Then verify (control or failure mode Y)</span>
        <input className="input" value={y} onChange={(e) => setY(e.target.value)} /></label>
      <label className="field"><span className="eyebrow">Evidence (harness test or finding id from this repo)</span>
        <input className="input mono" value={evidence} onChange={(e) => setEvidence(e.target.value)} /></label>
      <div className="field"><span className="eyebrow">Will be appended to HEURISTICS.md</span><pre className="heur-preview">{preview}</pre></div>
      {error && <ErrorNote>{error}</ErrorNote>}
      <p className="empty">STATE.json's heuristics_added is updated by Claude Code, not here. Until then the map shows the count from this file and notes the difference.</p>
      <div><button className="btn btn-primary" type="submit" disabled={!ready || busy}>Append entry</button></div>
    </form>
  );
}
