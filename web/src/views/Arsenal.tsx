import { useState } from "react";
import { fileUrl } from "../api/client";
import type { Arsenal as ArsenalData, FilePayload } from "../api/types";
import { ErrorNote, Loading, Markdown } from "../components/ui";
import { useResource } from "../lib/repo";

const pad = (n: number) => String(n).padStart(2, "0");

export function Arsenal() {
  const arsenal = useResource<ArsenalData>("/api/arsenal", ["heuristics", "flashcards", "portfolio"]);
  const [query, setQuery] = useState("");
  const [cert, setCert] = useState("all");
  const [index, setIndex] = useState(0);
  const [side, setSide] = useState<"front" | "back">("front");
  const [openPort, setOpenPort] = useState<string | null>(null);

  if (arsenal.error && !arsenal.data) return <section className="view pad"><ErrorNote>{arsenal.error}</ErrorNote></section>;
  if (!arsenal.data) return <section className="view"><Loading what="the arsenal" /></section>;
  const { heuristics, flashcards, certs, portfolio } = arsenal.data;

  const q = query.trim().toLowerCase();
  const found = heuristics.entries.filter((h) => !q || `${h.id} ${h.rule} ${h.evidence}`.toLowerCase().includes(q));
  const filter = cert === "all" || certs.some((c) => c.cert === cert) ? cert : "all";
  const deck = flashcards.filter((c) => filter === "all" || c.tags.some((t) => t.startsWith(`${filter}::`)));
  const card = deck[Math.min(index, Math.max(0, deck.length - 1))];
  const at = Math.min(index, Math.max(0, deck.length - 1));
  const move = (d: number) => { setIndex((at + d + deck.length) % deck.length); setSide("front"); };
  const port = portfolio.find((p) => p.path === openPort) ?? portfolio[0] ?? null;

  return (
    <section className="view view-arsenal" aria-label="Arsenal and Portfolio Vault">
      <div className="panel">
        <div className="pane-head">
          <span className="pane-title">Heuristics codex</span>
          <input className="input" type="search" placeholder="Search HEURISTICS.md" aria-label="Search heuristics"
            value={query} onChange={(e) => setQuery(e.target.value)} />
        </div>
        <div className="ars-body">
          {heuristics.entries.length === 0 && <p className="empty">HEURISTICS.md has no entries yet. Each module adds its own at the heuristics stage.</p>}
          {heuristics.entries.length > 0 && found.length === 0 && <p className="empty">No entry matches "{query}".</p>}
          {found.map((h) => (
            <div className="heur" key={h.id}>
              <span className="eyebrow">{h.id} · Module {pad(h.module)}</span>
              <p>{h.rule}</p>
              <small>Evidence: {h.evidence}</small>
            </div>
          ))}
        </div>
      </div>

      <div className="panel">
        <div className="pane-head">
          <span className="pane-title">Flashcards</span>
          {certs.length > 0 && (
            <span className="seg" role="group" aria-label="Filter by cert">
              {["all", ...certs.map((c) => c.cert)].map((c) => (
                <button key={c} aria-pressed={c === filter} onClick={() => { setCert(c); setIndex(0); setSide("front"); }}>{c}</button>
              ))}
            </span>
          )}
        </div>
        <div className="ars-body">
          {!card ? <p className="empty">No cards in flashcards/ yet. Each module emits 15 to 30 at the heuristics stage.</p> : (
            <>
              <button className="card" onClick={() => setSide(side === "front" ? "back" : "front")}
                aria-label={`Card ${at + 1} of ${deck.length}, ${side}. Activate to flip.`}>
                <span className="eyebrow">{side} · {card.file}</span>
                <p>{card[side]}</p>
              </button>
              <div className="card-nav">
                <button className="btn" onClick={() => move(-1)}>Previous</button>
                <span className="eyebrow">{at + 1} / {deck.length}</span>
                <button className="btn" onClick={() => move(1)}>Next</button>
              </div>
              <div className="certs">{card.tags.map((t) => <span className="cert" key={t}><span>{t}</span></span>)}</div>
            </>
          )}
        </div>
      </div>

      <div className="panel">
        <div className="pane-head"><span className="pane-title">Portfolio vault</span></div>
        <div className="ars-body">
          {!port ? <p className="empty">No write-ups in portfolio/ yet. Each module adds one sanitized piece.</p> : (
            <>
              <div className="port-list" role="tablist" aria-label="Portfolio write-ups">
                {portfolio.map((p) => (
                  <button key={p.path} role="tab" aria-selected={p.path === port.path} onClick={() => setOpenPort(p.path)}>
                    <span>{p.title ?? p.path.split("/").pop()}</span><small>{p.path}</small>
                  </button>
                ))}
              </div>
              <WriteUp path={port.path} />
            </>
          )}
        </div>
      </div>
    </section>
  );
}

function WriteUp({ path }: { path: string }) {
  const file = useResource<FilePayload>(fileUrl(path), ["portfolio"]);
  if (file.error) return <ErrorNote>{path}: {file.error}</ErrorNote>;
  if (!file.data) return <Loading what={path} />;
  return <Markdown source={file.data.body} />;
}
