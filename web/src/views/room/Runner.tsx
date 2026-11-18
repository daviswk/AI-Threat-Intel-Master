import { useEffect, useRef } from "react";
import { motion } from "motion/react";
import { Play } from "lucide-react";
import type { ResultRecord, RunState } from "../../api/types";
import { ErrorNote, Glyph } from "../../components/ui";

const WORD = { pass: "PASS", fail: "FAIL", error: "ERROR", skip: "SKIP" } as const;

/** Runs the harness through the backend and shows pytest's own output.
 *  A flag goes green only when pytest reports that test as passed. Per
 *  spec/SCHEMAS.md §2 a green test means the procedure is sound; the control's
 *  conclusion lives in the result record and is shown separately below. */
export function Runner({ run, target, results, onRun }: {
  run: RunState; target: string; results: ResultRecord[]; onRun: () => void;
}) {
  const term = useRef<HTMLPreElement>(null);
  useEffect(() => { if (term.current) term.current.scrollTop = term.current.scrollHeight; }, [run.output]);

  const tests = run.tests ?? [];
  const files = [...new Set(tests.map((t) => t.file))];
  const started = run.running || run.code !== null || run.error !== null;

  return (
    <div className="panel pane-run" aria-label="Test runner">
      <div className="pane-head">
        <span className="pane-title">Harness</span>
        <code className="run-cmd" title={run.cmd}>{run.cmd || `uv run --frozen python -m pytest ${target}`}</code>
        <button className="btn btn-primary" onClick={onRun} disabled={run.running}>
          <Play aria-hidden="true" />{run.running ? "Running" : "Verify & Run Harness"}
        </button>
      </div>

      <div className="run-body">
        <div className="flags" aria-label="Test outcomes" aria-live="polite">
          {run.running && <div className="flag" data-outcome="running"><Glyph s="running" /><span>pytest is running</span><b /></div>}
          {!run.running && !started && <p className="empty" style={{ padding: 8 }}>No run in this session. Flags appear here, one per test, when pytest finishes.</p>}
          {!run.running && run.code !== null && tests.length === 0 && (
            <p className="empty" style={{ padding: 8 }}>{run.note ?? `pytest exited with code ${run.code} and reported no tests.`}</p>
          )}
          {!run.running && files.map((file) => (
            <div key={file} style={{ display: "grid", gap: 4 }}>
              <div className="eyebrow">{file}</div>
              {tests.filter((t) => t.file === file).map((t, i) => (
                // Pass/fail feedback: each flag settles into place as its result lands.
                <motion.div key={t.name} className="flag" data-outcome={t.outcome} title={`${t.file}::${t.name}`}
                  initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.2, delay: i * 0.03 }}>
                  <Glyph s={t.outcome} /><span>{t.name}</span><b>{WORD[t.outcome]}</b>
                </motion.div>
              ))}
            </div>
          ))}
        </div>
        <pre className="term" ref={term} role="log" aria-label="Harness output" tabIndex={0}>
          {run.cmd && <span className="dim">$ {run.cmd}{"\n"}</span>}
          {run.output}
          {run.code !== null && <span className="dim">{"\n"}exit code {run.code}{run.note ? ` · ${run.note}` : ""}{"\n"}</span>}
        </pre>
      </div>

      {run.error && <div className="pad"><ErrorNote>{run.error}</ErrorNote></div>}
      <div className="records">
        {results.length === 0
          ? <span>No result records in assurance-harness/results/ for this module yet.</span>
          : <>
            <span>Control conclusions from result records (not test outcomes):</span>
            {results.map((r, i) => (
              <span className="record" key={i} title={r.path}>
                {r.error ? `${r.path}: ${r.error}` : `${r.control_id} · ${r.dataset} · ${r.exceptions ?? "?"} exceptions · ${r.conclusion}`}
              </span>
            ))}
          </>}
      </div>
    </div>
  );
}
