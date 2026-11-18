import { useCallback, useLayoutEffect, useRef, useState } from "react";
import { motion } from "motion/react";
import type { ModuleView, Overview, RunState } from "../api/types";
import { Glyph } from "../components/ui";

const pad = (n: number) => String(n).padStart(2, "0");
const hrs = (n: number) => String(+n.toFixed(1));
const GATE: [keyof ModuleView["gate"], string][] = [
  ["edge_case", "Edge case"], ["pushback", "1st-line pushback"],
  ["compression", "Four-tier compression"], ["artifact_check", "Artifact check"],
];

/** Serpentine grid slot for module index i: rows of four, alternating direction. */
function slot(i: number) {
  const row = Math.floor(i / 4);
  return { gridRow: row + 1, gridColumn: (row % 2 === 0 ? i % 4 : 3 - (i % 4)) + 1 };
}

export function CampaignMap({ overview, lastRun, stageChanged, onEnterRoom }: {
  overview: Overview; lastRun: RunState; stageChanged: number; onEnterRoom: () => void;
}) {
  const [selected, setSelected] = useState(overview.current_module);
  const pathRef = useRef<HTMLDivElement>(null);
  const [lines, setLines] = useState<{ x1: number; y1: number; x2: number; y2: number; reached: boolean }[]>([]);
  const [box, setBox] = useState({ w: 0, h: 0 });
  const failing = lastRun.tests?.filter((t) => t.outcome === "fail" || t.outcome === "error").length ?? 0;

  // Connectors come from the spec's own "Input (from MN)" lines (overview.edges).
  const draw = useCallback(() => {
    const el = pathRef.current;
    if (!el) return;
    const base = el.getBoundingClientRect();
    const centre = (id: number) => {
      const g = el.querySelector<HTMLElement>(`[data-node="${id}"] .node-glyph`)?.getBoundingClientRect();
      return g ? { x: g.left + g.width / 2 - base.left, y: g.top + g.height / 2 - base.top } : null;
    };
    setBox({ w: base.width, h: base.height });
    setLines(overview.edges.flatMap(([from, to]) => {
      const a = centre(from), b = centre(to);
      const target = overview.modules[to - 1];
      return a && b ? [{ x1: a.x, y1: a.y, x2: b.x, y2: b.y, reached: target.status !== "locked" }] : [];
    }));
  }, [overview]);

  useLayoutEffect(() => {
    draw();
    const el = pathRef.current;
    if (!el) return;
    const ro = new ResizeObserver(draw);
    ro.observe(el);
    document.fonts?.ready.then(draw);
    return () => ro.disconnect();
  }, [draw]);

  const t = overview.totals;
  const module = overview.modules[selected - 1];

  return (
    <section className="view view-map" aria-label="Campaign Map">
      <div className="map-main">
        <div className="map-summary">
          <div className="stat"><span className="eyebrow">Modules complete</span><b>{t.modules_complete}<small> / {t.modules}</small></b></div>
          <div className="stat"><span className="eyebrow">Hours logged</span><b>{hrs(t.hours_logged)}<small> / {hrs(t.hours_planned)} planned</small></b></div>
          <div className="stat"><span className="eyebrow">Heuristics</span><b>{t.heuristics}</b></div>
          <div className="stat"><span className="eyebrow">Flashcards</span><b>{t.cards}</b></div>
          <div className="certs" style={{ marginLeft: "auto" }}>
            {t.certs.length === 0
              ? <span className="empty">No cert-tagged cards yet.</span>
              : t.certs.map((c) => <span className="cert" key={c.cert}><b>{c.cert}</b><span>{c.cards} cards</span></span>)}
          </div>
        </div>

        <div className="path" ref={pathRef}>
          <svg className="path-lines" viewBox={`0 0 ${box.w} ${box.h}`} aria-hidden="true">
            {lines.map((l, i) => <line key={i} {...{ x1: l.x1, y1: l.y1, x2: l.x2, y2: l.y2 }} className={l.reached ? "reached" : ""} />)}
          </svg>
          {overview.modules.map((m, i) => (
            <button key={m.id} className="node" data-node={m.id} data-status={m.status} style={slot(i)}
              aria-pressed={m.id === selected} aria-label={`Module ${m.id}: ${m.title}, ${m.status}`}
              onClick={() => setSelected(m.id)}>
              {/* Stage-change feedback: the live node's block pulses once when STATE.json moves it. */}
              <motion.span className="node-glyph" key={m.status === "active" ? `a${stageChanged}` : "s"}
                initial={m.status === "active" && stageChanged > 0 ? { scale: 1.18 } : false}
                animate={{ scale: 1 }} transition={{ duration: 0.4 }}>
                {pad(m.id)}
              </motion.span>
              <span className="node-body">
                <span className="node-title">{m.title}</span>
                <span className="node-meta">
                  {m.status === "complete" && `complete · ${hrs(m.hours_spent)} / ${hrs(m.timebox_hours)} h`}
                  {m.status === "active" && `${m.stage} · ${hrs(m.hours_spent)} / ${hrs(m.timebox_hours)} h`}
                  {m.status === "locked" && `locked · ${hrs(m.timebox_hours)} h`}
                  {m.status === "active" && failing > 0 && <span className="fail-note"> &#9670; {failing} failing</span>}
                </span>
                <span className="node-stages" aria-hidden="true">
                  {overview.stages.slice(0, 6).map((s, k) => (
                    <i key={s} className={m.status === "complete" || k < m.stage_index ? "done" : k === m.stage_index ? "current" : ""} />
                  ))}
                </span>
              </span>
            </button>
          ))}
        </div>

        <div className="legend" aria-label="Status legend">
          {["complete", "active", "locked", "failing"].map((s) => <span className="chip" key={s}><Glyph s={s} />{s}</span>)}
        </div>
      </div>

      <ModuleDetail m={module} stages={overview.stages} onEnterRoom={onEnterRoom} />
    </section>
  );
}

function ModuleDetail({ m, stages, onEnterRoom }: { m: ModuleView; stages: string[]; onEnterRoom: () => void }) {
  const label = { complete: "complete", active: "in progress", locked: "locked" }[m.status];
  return (
    <aside className="panel module-detail" aria-live="polite" aria-label={`Module ${m.id} detail`}>
      <div>
        <div className="eyebrow">Module {pad(m.id)} · {label}</div>
        <h2 className="md-title">{m.title}</h2>
      </div>

      {m.status === "locked" ? (
        <>
          <p className="empty">Locked. Unlocks when Module {pad(m.id - 1)} passes all four gate checks.</p>
          <div className="md-block">
            <div className="eyebrow">Time-box</div>
            <div className="burn-legend"><span>{hrs(m.timebox_hours)} h planned</span><span>not started</span></div>
          </div>
          {!m.expanded && <div className="md-block"><div className="eyebrow">Contract</div>
            <p className="empty">I/O contract only until this module's pre-flight.</p></div>}
        </>
      ) : (
        <>
          <div className="md-block">
            <div className="eyebrow">Stage</div>
            <ol className="stage-track">
              {stages.map((s, k) => {
                const entered = m.stage_history.find((h) => h.stage === s)?.entered_on ?? "";
                const cls = m.status === "complete" || k < m.stage_index ? "done" : k === m.stage_index ? "current" : "";
                return <li key={s} className={cls} aria-current={cls === "current" ? "step" : undefined}><i /><span>{s}</span><time>{entered}</time></li>;
              })}
            </ol>
          </div>

          <div className="md-block">
            <div className="eyebrow">Time-box</div>
            <div className="burn" data-state={m.over_hours > 0 ? "over" : m.status === "complete" ? "done" : "live"}
              role="img" aria-label={`${hrs(m.hours_spent)} of ${hrs(m.timebox_hours)} hours logged`}>
              <div className="burn-fill" style={{ width: `${m.burn_pct}%` }} />
              <div className="burn-mark" title="80% of the time-box: Nice-to-haves get cut from here" />
            </div>
            <div className="burn-legend">
              <span>{hrs(m.hours_spent)} of {hrs(m.timebox_hours)} h logged</span>
              <span>{m.over_hours > 0 ? `${hrs(m.over_hours)} h over` : `${hrs(m.timebox_hours - m.hours_spent)} h left`} · mark at 80%</span>
            </div>
            {m.nice_to_haves_cut.length > 0 && <ul className="md-paths">{m.nice_to_haves_cut.map((c) => <li key={c}>cut: {c}</li>)}</ul>}
          </div>

          <div className="md-block">
            <div className="eyebrow">Gate · {m.gate.attempts} attempt{m.gate.attempts === 1 ? "" : "s"}</div>
            <ul className="gate-list">
              {GATE.map(([key, name]) => <li key={key} data-result={m.gate[key]}><span>{name}</span><span>{m.gate[key]}</span></li>)}
            </ul>
          </div>

          <div className="md-block">
            <div className="eyebrow">Cards by cert domain</div>
            {m.certs.length
              ? <div className="certs">{m.certs.map((c) => <span className="cert" key={c.cert}><b>{c.cert}</b><span>{c.cards} cards</span></span>)}</div>
              : <span className="empty">No cards in flashcards/m{pad(m.id)}.csv yet.</span>}
          </div>

          <div className="md-block">
            <div className="eyebrow">Outputs</div>
            {m.outputs.length
              ? <ul className="md-paths">{m.outputs.map((o) => <li key={o}>{o}</li>)}</ul>
              : <span className="empty">None recorded.</span>}
          </div>

          {m.notes.length > 0 && <div className="md-block">
            <div className="eyebrow">State and files disagree</div>
            <ul className="md-paths">{m.notes.map((n) => <li key={n}>{n}</li>)}</ul>
          </div>}

          {m.status === "active" && <div className="md-foot"><button className="btn btn-primary" onClick={onEnterRoom}>Enter room</button></div>}
        </>
      )}
    </aside>
  );
}
