import { useEffect, useMemo, useState } from "react";
import { diffArrays } from "diff";
import { ApiError, fileUrl, get } from "../../api/client";
import type { FilePayload, Pair } from "../../api/types";
import { ErrorNote, Loading } from "../../components/ui";
import { useOnChange } from "../../lib/repo";

interface Row { a: string | null; b: string | null; na: number | null; nb: number | null; differs: boolean }
const RENDER_CAP = 1500;

/** Line up two texts. A differing line gets the same neutral mark on both
 *  sides: the viewer shows where A and B differ, never which one is right. */
function align(a: string[], b: string[]): Row[] {
  const parts = diffArrays(a, b, { maxEditLength: 20000 });
  const rows: Row[] = [];
  let na = 0, nb = 0;
  if (!parts) {
    for (let i = 0; i < Math.max(a.length, b.length); i++) {
      rows.push({ a: a[i] ?? null, b: b[i] ?? null, na: i < a.length ? i + 1 : null, nb: i < b.length ? i + 1 : null, differs: a[i] !== b[i] });
    }
    return rows;
  }
  for (let i = 0; i < parts.length; i++) {
    const p = parts[i];
    if (!p.added && !p.removed) {
      for (const line of p.value) rows.push({ a: line, b: line, na: ++na, nb: ++nb, differs: false });
      continue;
    }
    const removed = p.removed ? p.value : [];
    const next = parts[i + 1];
    const added = p.added ? p.value : p.removed && next?.added ? next.value : [];
    if (p.removed && next?.added) i++;
    for (let k = 0; k < Math.max(removed.length, added.length); k++) {
      rows.push({
        a: removed[k] ?? null, b: added[k] ?? null,
        na: k < removed.length ? ++na : null, nb: k < added.length ? ++nb : null, differs: true,
      });
    }
  }
  return rows;
}

const lines = (text: string) => (text === "" ? [] : text.replace(/\n$/, "").split("\n"));

async function side(path: string): Promise<string | null> {
  try { return (await get<FilePayload>(fileUrl(path))).content; }
  catch (e) { if (e instanceof ApiError && e.status === 404) return null; throw e; }
}

export function PairViewer({ pairs }: { pairs: Pair[] }) {
  const [pairIndex, setPairIndex] = useState(0);
  const pair = pairs[Math.min(pairIndex, pairs.length - 1)];
  const [file, setFile] = useState<string | null>(null);
  const current = pair && (file && pair.files.includes(file) ? file : pair.files[0]);
  const [texts, setTexts] = useState<{ key: string; a: string | null; b: string | null } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [onlyDiff, setOnlyDiff] = useState(false);
  const [showAll, setShowAll] = useState(false);
  const [tick, setTick] = useState(0);
  useOnChange(["lab"], () => setTick((n) => n + 1));

  const key = pair && current ? `${pair.a}|${pair.b}|${current}` : "";
  useEffect(() => {
    if (!pair || !current) return;
    let live = true;
    setError(null);
    Promise.all([side(`${pair.a}/${current}`), side(`${pair.b}/${current}`)]).then(
      ([a, b]) => { if (live) setTexts({ key, a, b }); },
      (e: unknown) => { if (live) setError(e instanceof Error ? e.message : "could not load the pair"); });
    return () => { live = false; };
  }, [key, tick]);  // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => setShowAll(false), [key, onlyDiff]);

  const rows = useMemo(() => (texts && texts.key === key ? align(lines(texts.a ?? ""), lines(texts.b ?? "")) : null), [texts, key]);

  if (!pair) {
    return <p className="empty pad">No contrastive pair in this lab yet. A pair is two sibling folders under evidence/ whose names end in A and B.</p>;
  }
  const differing = rows?.filter((r) => r.differs).length ?? 0;
  const shown = rows ? (onlyDiff ? rows.filter((r) => r.differs) : rows) : [];
  const visible = showAll ? shown : shown.slice(0, RENDER_CAP);

  return (
    <>
      <div className="pair-bar">
        {pairs.length > 1 && (
          <span className="seg" role="group" aria-label="Pair">
            {pairs.map((p, i) => <button key={p.a} aria-pressed={p === pair} onClick={() => { setPairIndex(i); setFile(null); }}>{p.name}</button>)}
          </span>
        )}
        <span className="eyebrow">{pair.name}</span>
        <label><input type="checkbox" checked={onlyDiff} onChange={(e) => setOnlyDiff(e.target.checked)} />only lines that differ</label>
        <span style={{ flex: 1 }} />
        <span className="seg" role="group" aria-label="File in the pair">
          {pair.files.map((f) => <button key={f} aria-pressed={f === current} onClick={() => setFile(f)}>{f}</button>)}
        </span>
      </div>

      <div className="pair-grid" tabIndex={0} aria-label={`${current}: artifact A beside artifact B`}>
        <div className="pair-head"><h4>Artifact A</h4><h4>Artifact B</h4></div>
        {error && <div className="pad"><ErrorNote>{error}</ErrorNote></div>}
        {!rows && !error && <Loading what="both artifacts" />}
        {rows && texts && (texts.a === null || texts.b === null) && (
          <p className="empty pad">{current} exists only in artifact {texts.a === null ? "B" : "A"}.</p>
        )}
        {visible.map((r, i) => (
          <div className="pair-row" key={i}>
            <div className="ln" data-differs={r.differs && r.a !== null ? "" : undefined} data-absent={r.a === null ? "" : undefined}>
              <span>{r.na ?? ""}</span><span /><span>{r.a ?? ""}</span>
            </div>
            <div className="ln" data-differs={r.differs && r.b !== null ? "" : undefined} data-absent={r.b === null ? "" : undefined}>
              <span>{r.nb ?? ""}</span><span /><span>{r.b ?? ""}</span>
            </div>
          </div>
        ))}
        {shown.length > visible.length && (
          <div className="pad"><button className="btn" onClick={() => setShowAll(true)}>Show all {shown.length} rows</button></div>
        )}
      </div>

      <div className="pair-note">
        {rows ? `${differing} of ${rows.length} rows differ, marked ~ on both sides. ` : ""}
        The viewer shows where the artifacts differ. It never indicates which one is effective.
      </div>
    </>
  );
}
