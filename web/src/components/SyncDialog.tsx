import { useEffect, useRef, useState } from "react";
import { ApiError, get, run } from "../api/client";
import { useBus } from "../lib/repo";
import { ErrorNote } from "./ui";

export type SyncKind = "up" | "down";

/** Runs scripts/sync_up.sh or scripts/sync_down.sh through the backend and
 *  shows their output unchanged. Sync Up lists what will be committed first
 *  and waits for a go-ahead. Nothing here retries, forces or resolves. */
export function SyncDialog({ kind, onClose }: { kind: SyncKind; onClose: () => void }) {
  const ref = useRef<HTMLDialogElement>(null);
  const term = useRef<HTMLPreElement>(null);
  const bus = useBus();
  const [files, setFiles] = useState<string[] | null>(null);
  const [output, setOutput] = useState("");
  const [phase, setPhase] = useState<"confirm" | "running" | "done">(kind === "up" ? "confirm" : "running");
  const [code, setCode] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const script = kind === "up" ? "scripts/sync_up.sh" : "scripts/sync_down.sh";

  const start = async () => {
    setPhase("running");
    setOutput("");
    try {
      await run(kind === "up" ? "sync_up" : "sync_down", (e) => {
        if (e.t === "out") setOutput((o) => o + e.d);
        if (e.t === "exit") setCode(e.code);
      });
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "The backend did not answer.");
    } finally {
      setPhase("done");
      bus.refreshAll();
    }
  };

  useEffect(() => {
    ref.current?.showModal();
    if (kind === "up") {
      get<{ files: string[] }>("/api/sync/preview").then(
        (r) => setFiles(r.files),
        (e: unknown) => { setFiles([]); setError(e instanceof ApiError ? e.message : "The backend did not answer."); });
    } else {
      void start();
    }
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { if (term.current) term.current.scrollTop = term.current.scrollHeight; }, [output]);

  return (
    <dialog ref={ref} className="dialog" onClose={onClose} aria-labelledby="sync-title"
      onCancel={(e) => { if (phase === "running") e.preventDefault(); }}>
      <div className="dialog-head">
        <span className="pane-title" id="sync-title">Sync {kind === "up" ? "Up" : "Down"} · bash {script}</span>
        <button className="btn btn-quiet" onClick={() => ref.current?.close()} disabled={phase === "running"}>Close</button>
      </div>

      {kind === "up" && (
        <>
          <div className="eyebrow" style={{ padding: "12px 16px 0" }}>
            {files === null ? "Reading git status" : `Files that will be committed (${files.length})`}
          </div>
          <ul className="file-list">
            {files !== null && files.length === 0 && <li>Nothing to commit. The script still runs its checks and pushes.</li>}
            {files?.map((f) => <li key={f}>{f}</li>)}
          </ul>
        </>
      )}

      {error && <div className="pad"><ErrorNote>{error}</ErrorNote></div>}
      <pre className="term" ref={term} role="log" aria-label={`${script} output`} tabIndex={0}>
        {phase === "confirm" ? <span className="dim">Waiting for your go-ahead.</span> : output}
        {code !== null && <span className="dim">{"\n"}exit code {code}</span>}
      </pre>

      <div className="dialog-foot">
        {phase === "confirm" && <>
          <button className="btn" onClick={() => ref.current?.close()}>Cancel</button>
          <button className="btn btn-primary" onClick={() => void start()} disabled={files === null}>Run sync-up</button>
        </>}
        {phase === "running" && <span className="empty">Running. The script's own messages appear above, unchanged.</span>}
        {phase === "done" && <button className="btn btn-primary" onClick={() => ref.current?.close()}>Close</button>}
      </div>
    </dialog>
  );
}
