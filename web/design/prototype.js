/* Phase A prototype behaviour. Vanilla JS over MOCK (mock-data.js).
   Every figure on screen is computed here from the mock records, the same
   way the real app will compute it from the repo. Nothing is stored. */
(function () {
  "use strict";
  const M = window.MOCK;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const params = new URLSearchParams(location.search);
  const LAB = "labs/m03-hyperscale-security/";
  const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];
  const M3_DATES = ["2026-12-22", "2026-12-27", "2026-12-29", "2027-01-03", "2027-01-09", "2027-01-11"];

  const ui = {
    view: params.get("view") || "map",
    selected: M.state.current_module,
    leftTab: "stage", paper: 0,
    workTab: "pair", pairFile: 0, file: null,
    card: 0, cardSide: "front", cardFilter: "all", port: 0, heurQuery: "",
    lastRun: null, running: false,
  };
  if (params.get("embed")) document.body.classList.add("embed");

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const pad = (n) => String(n).padStart(2, "0");
  const hrs = (n) => String(+n.toFixed(1));
  const inline = (s) => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  function md(src) {
    return src.split(/\n\n+/).map((block) => {
      const h = block.match(/^(#{1,3}) (.*)$/);
      if (h) return `<h${h[1].length}>${inline(h[2])}</h${h[1].length}>`;
      const lines = block.split("\n");
      if (lines.every((l) => /^- /.test(l))) return "<ul>" + lines.map((l) => `<li>${inline(l.slice(2))}</li>`).join("") + "</ul>";
      if (lines.every((l) => /^\d+\. /.test(l))) return "<ol>" + lines.map((l) => `<li>${inline(l.replace(/^\d+\. /, ""))}</li>`).join("") + "</ol>";
      return `<p>${inline(lines.join(" "))}</p>`;
    }).join("");
  }
  let toastTimer;
  function toast(msg) {
    const t = $("#toast");
    t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { t.hidden = true; }, 2600);
  }

  /* ---------- derivations ---------- */
  const current = () => M.state.modules[M.state.current_module - 1];
  const statusOf = (m) => (m.status === "complete" ? "complete" : m.status === "locked" ? "locked" : "active");
  const stageIndex = (m) => (m.status === "complete" ? 6 : m.id === M.state.current_module ? M.STAGES.indexOf(M.state.current_stage) : -1);
  function certCounts(cards) {
    const counts = new Map();
    cards.forEach((c) => {
      const certs = new Set(c.tags.split(/\s+/).filter((t) => t.includes("::")).map((t) => t.split("::")[0]));
      certs.forEach((k) => counts.set(k, (counts.get(k) || 0) + 1));
    });
    const order = ["CISA", "AAIA", "AIGP"];
    return [...counts.entries()].sort((a, b) => (order.indexOf(a[0]) + 99) % 99 - (order.indexOf(b[0]) + 99) % 99);
  }
  const certHtml = (cards) => certCounts(cards).map(([k, n]) => `<span class="cert"><b>${esc(k)}</b><span>${n} cards</span></span>`).join("");
  const cardsFor = (m) => M.flashcards.filter((c) => c.file === `flashcards/m${pad(m.id)}.csv`);

  /* ---------- campaign map ---------- */
  function renderSummary() {
    const mods = M.state.modules;
    const done = mods.filter((m) => m.status === "complete").length;
    const logged = M.state.time_log.reduce((a, e) => a + e.hours, 0);
    const planned = mods.reduce((a, m) => a + m.timebox_hours, 0);
    $("#mapSummary").innerHTML = `
      <div class="stat"><span class="eyebrow">Modules complete</span><b>${done}<small> / ${mods.length}</small></b></div>
      <div class="stat"><span class="eyebrow">Hours logged</span><b>${hrs(logged)}<small> / ${planned} planned</small></b></div>
      <div class="stat"><span class="eyebrow">Heuristics</span><b>${M.heuristics.length}</b></div>
      <div class="stat"><span class="eyebrow">Flashcards</span><b>${M.flashcards.length}</b></div>
      <div class="certs">${certHtml(M.flashcards)}</div>`;
  }

  function renderPath() {
    const path = $("#path");
    $$(".node", path).forEach((n) => n.remove());
    M.state.modules.forEach((m, i) => {
      const row = Math.floor(i / 4), col = row % 2 === 0 ? i % 4 : 3 - (i % 4);
      const st = statusOf(m), si = stageIndex(m);
      const ticks = M.STAGES.slice(0, 6).map((_, k) => `<i class="${k < si ? "done" : k === si ? "current" : ""}"></i>`).join("");
      const failing = st === "active" && ui.lastRun && ui.lastRun.failed ? ` <span class="fail-note">&#9670; ${ui.lastRun.failed} failing</span>` : "";
      const meta = st === "complete" ? `complete · ${hrs(m.hours_spent)} / ${m.timebox_hours} h`
        : st === "active" ? `${M.state.current_stage} · ${hrs(m.hours_spent)} / ${m.timebox_hours} h${failing}`
        : `locked · ${m.timebox_hours} h`;
      const b = document.createElement("button");
      b.className = "node"; b.dataset.id = m.id; b.dataset.status = st;
      b.setAttribute("aria-pressed", String(m.id === ui.selected));
      b.setAttribute("aria-label", `Module ${m.id}: ${m.title}, ${st}`);
      b.style.gridRow = row + 1; b.style.gridColumn = col + 1;
      b.innerHTML = `<span class="node-glyph"><span class="node-num" data-roman="${ROMAN[i]}">${pad(m.id)}</span></span>
        <span class="node-body"><span class="node-title">${esc(m.title)}</span><span class="node-meta">${meta}</span><span class="node-stages">${ticks}</span></span>`;
      b.addEventListener("click", () => { ui.selected = m.id; renderPath(); renderDetail(); });
      path.appendChild(b);
    });
    drawLines();
  }

  function drawLines() {
    const path = $("#path"), svg = $("#pathLines");
    if ($("#view-map").hidden) return;
    const anchor = getComputedStyle(document.body).getPropertyValue("--anchor").trim();
    const box = path.getBoundingClientRect();
    const pts = $$(".node", path).map((n) => {
      const r = (anchor === "node" ? n : $(".node-glyph", n)).getBoundingClientRect();
      return [r.left + r.width / 2 - box.left, r.top + r.height / 2 - box.top];
    });
    svg.setAttribute("viewBox", `0 0 ${box.width} ${box.height}`);
    svg.innerHTML = pts.slice(1).map((p, i) => {
      const reached = M.state.modules[i + 1].status !== "locked";
      return `<line x1="${pts[i][0]}" y1="${pts[i][1]}" x2="${p[0]}" y2="${p[1]}" class="${reached ? "reached" : ""}"/>`;
    }).join("");
  }

  function renderDetail() {
    const m = M.state.modules[ui.selected - 1], st = statusOf(m), si = stageIndex(m);
    const label = { complete: "complete", active: "in progress", locked: "locked" }[st];
    let html = `<div><div class="eyebrow">Module ${pad(m.id)} · ${label}</div><h2 class="md-title">${esc(m.title)}</h2></div>`;
    if (st === "locked") {
      html += `<p class="md-empty">Locked. Unlocks when Module ${pad(m.id - 1)} passes all four gate checks.</p>
        <div class="md-block"><div class="eyebrow">Time-box</div><div class="burn-legend"><span>${m.timebox_hours} h planned</span><span>not started</span></div></div>
        <div class="md-block"><div class="eyebrow">Contract</div><p class="md-empty">I/O contract only until this module's pre-flight.</p></div>`;
    } else {
      const track = M.STAGES.map((s, k) => {
        const entry = m.stage_history.find((h) => h.stage === s);
        const cls = k < si || st === "complete" ? "done" : k === si ? "current" : "";
        return `<li class="${cls}"><i></i><span>${s}</span><time>${entry ? entry.entered_on : ""}</time></li>`;
      }).join("");
      const over = m.hours_spent > m.timebox_hours;
      const pct = Math.min(100, (m.hours_spent / m.timebox_hours) * 100);
      const right = over ? `${hrs(m.hours_spent - m.timebox_hours)} h over` : `${hrs(m.timebox_hours - m.hours_spent)} h left`;
      const gateNames = { edge_case: "Edge case", pushback: "1st-line pushback", compression: "Four-tier compression", artifact_check: "Artifact check" };
      const gate = Object.keys(gateNames).map((k) => `<li data-result="${m.gate[k]}"><span>${gateNames[k]}</span><span>${m.gate[k]}</span></li>`).join("");
      const cards = cardsFor(m);
      html += `
        <div class="md-block"><div class="eyebrow">Stage</div><ol class="stage-track">${track}</ol></div>
        <div class="md-block"><div class="eyebrow">Time-box</div>
          <div class="burn" data-state="${over ? "over" : st === "complete" ? "done" : "live"}"><div class="burn-fill" style="width:${pct}%"></div><div class="burn-mark" title="80% of the time-box"></div></div>
          <div class="burn-legend"><span>${hrs(m.hours_spent)} of ${m.timebox_hours} h logged</span><span>${right} · mark at 80%</span></div></div>
        <div class="md-block"><div class="eyebrow">Gate · ${m.gate.attempts} attempt${m.gate.attempts === 1 ? "" : "s"}</div><ul class="gate-list">${gate}</ul></div>
        <div class="md-block"><div class="eyebrow">Cards by cert domain</div>${cards.length ? `<div class="card-tags">${certHtml(cards)}</div>` : `<span class="md-empty">No cards in flashcards/m${pad(m.id)}.csv yet.</span>`}</div>
        <div class="md-block"><div class="eyebrow">Outputs</div>${m.outputs.length ? `<ul class="md-paths">${m.outputs.map((o) => `<li>${esc(o)}</li>`).join("")}</ul>` : `<span class="md-empty">None recorded.</span>`}</div>`;
      if (st === "active") html += `<div class="md-foot"><button class="btn btn-primary" id="enterRoom">Enter room</button></div>`;
    }
    $("#moduleDetail").innerHTML = html;
    const enter = $("#enterRoom");
    if (enter) enter.addEventListener("click", () => setView("room"));
  }

  /* ---------- active room: left pane ---------- */
  function copyPrompt(text) {
    const done = () => toast("Copied to clipboard: " + text);
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, () => toast("Prompt: " + text));
    else toast("Prompt: " + text);
  }

  function renderBanner() {
    const b = M.banners[M.state.current_stage];
    const where = b.where === "app" ? "Next · in the app" : "Next · in Claude Code";
    $("#banner").innerHTML = `<span class="banner-where">${where}</span><p class="banner-text">${esc(b.text)}</p>
      <div class="banner-actions">${b.action ? `<button class="btn btn-primary" id="bannerOpen">${esc(b.action.label)}</button>` : ""}${b.cli ? `<button class="btn" id="bannerCopy" title="${esc(b.cli.label)}">Copy CLI prompt</button>` : ""}</div>`;
    if (b.action) $("#bannerOpen").addEventListener("click", () => { ui.workTab = "write"; ui.file = b.action.file; renderWork(); });
    if (b.cli) $("#bannerCopy").addEventListener("click", () => copyPrompt(b.cli.prompt));
  }

  function renderLeft() {
    $$("#leftTabs .tab").forEach((t) => t.setAttribute("aria-selected", String(t.dataset.tab === ui.leftTab)));
    const strip = $("#paperStrip"), reader = $("#reader");
    strip.hidden = ui.leftTab !== "papers";
    if (ui.leftTab === "stage") reader.innerHTML = md(M.stageText[M.state.current_stage]);
    else if (ui.leftTab === "briefing") reader.innerHTML = md(M.briefing);
    else {
      strip.innerHTML = M.papers.map((p, i) => `<button role="tab" aria-selected="${i === ui.paper}" data-i="${i}">${esc(p.split("/").pop())}</button>`).join("");
      $$("button", strip).forEach((b) => b.addEventListener("click", () => { ui.paper = +b.dataset.i; renderLeft(); }));
      reader.innerHTML = `<div class="placeholder">[ rendered Markdown of ${esc(M.papers[ui.paper])} ]<br>[ front matter shown as a source table: title, publisher, retrieved, licence ]<br>[ sanitized, raw HTML disabled ]</div>`;
    }
    reader.scrollTop = 0;
  }

  /* ---------- active room: workbench ---------- */
  function renderWork() {
    const now = { incubation: "pair", lab: "write", gate: "write" }[M.state.current_stage];
    $$("#workTabs .tab").forEach((t) => {
      t.setAttribute("aria-selected", String(t.dataset.tab === ui.workTab));
      const base = t.textContent.replace(/\s*now$/, "");
      t.innerHTML = esc(base) + (t.dataset.tab === now ? '<span class="now">now</span>' : "");
    });
    const body = $("#workBody");
    if (ui.workTab === "pair") renderPair(body);
    else if (ui.workTab === "write") renderWrite(body);
    else renderHeuristicForm(body);
  }

  function renderPair(body) {
    const f = M.pair.files[ui.pairFile];
    const differs = f.a.map((l, i) => l !== f.b[i]);
    const col = (name, lines) => `<div class="pair-col"><h4>${name}</h4>${lines.map((l, i) => `<div class="ln"${differs[i] ? " data-differs" : ""}><span>${i + 1}</span><span></span><span>${esc(l)}</span></div>`).join("")}</div>`;
    body.innerHTML = `
      <div class="pair-bar"><span class="eyebrow">${esc(M.pair.label)}</span><span class="spacer"></span>
        <span class="seg">${M.pair.files.map((x, i) => `<button aria-pressed="${i === ui.pairFile}" data-i="${i}">${esc(x.name)}</button>`).join("")}</span></div>
      <div class="pair-grid">${col("Artifact A", f.a)}${col("Artifact B", f.b)}</div>
      <div class="pair-note">${differs.filter(Boolean).length} lines differ, marked ~ on both sides. The viewer shows where the artifacts differ. It never indicates which one is effective.</div>`;
    $$(".pair-bar .seg button", body).forEach((b) => b.addEventListener("click", () => { ui.pairFile = +b.dataset.i; renderPair(body); }));
  }

  function renderWrite(body) {
    if (!ui.file) ui.file = (M.banners[M.state.current_stage].action || {}).file || M.myFiles[0].path;
    const groups = [...new Set(M.myFiles.map((f) => f.group))];
    const rail = groups.map((g) => `<div><div class="eyebrow">${g}</div>${M.myFiles.filter((f) => f.group === g).map((f) =>
      `<button role="tab" aria-selected="${f.path === ui.file}" data-path="${f.path}"><span>${esc(f.path.split("/").pop())}</span><span class="dirty">${f.saved ? "" : "edited"}</span></button>`).join("")}</div>`).join("");
    const f = M.myFiles.find((x) => x.path === ui.file);
    let fields;
    if (f.kind === "finding") {
      fields = `<div class="field-row">
          <label class="field"><span class="eyebrow">control_id</span><input class="input mono" data-front="control_id" value="${esc(f.front.control_id)}"></label>
          <label class="field"><span class="eyebrow">status</span><select class="input" data-front="status">${["open", "remediated", "revalidated", "risk_accepted"].map((s) => `<option${s === f.front.status ? " selected" : ""}>${s}</option>`).join("")}</select></label>
          <label class="field"><span class="eyebrow">title</span><input class="input" data-front="title" value="${esc(f.front.title)}" placeholder="One line"></label>
        </div>` + Object.keys(f.sections).map((h) => `<label class="field cs"><h5>${h}</h5><textarea class="textarea" data-section="${h}">${esc(f.sections[h])}</textarea></label>`).join("");
    } else {
      fields = `<textarea class="textarea fill" data-body aria-label="${esc(f.path)}" placeholder="Your words only. Nothing here drafts, completes or suggests.">${esc(f.body)}</textarea>`;
    }
    body.innerHTML = `<div class="write"><nav class="file-rail" aria-label="Files you author">${rail}</nav>
      <div class="editor"><div class="editor-head"><span class="editor-path">${LAB}${esc(f.path)}</span>
        <span class="save-state" data-dirty="${!f.saved}">${f.saved ? "matches file on disk" : "unsaved changes"}</span>
        <button class="btn btn-primary" id="saveBtn">Save</button></div>
        <div class="editor-body">${fields}</div></div></div>`;
    $$(".file-rail button", body).forEach((b) => b.addEventListener("click", () => { ui.file = b.dataset.path; renderWrite(body); }));
    const dirty = () => {
      f.saved = false;
      const s = $(".save-state", body); s.dataset.dirty = "true"; s.textContent = "unsaved changes";
      $(`.file-rail button[data-path="${f.path}"] .dirty`, body).textContent = "edited";
    };
    $$("[data-body]", body).forEach((el) => el.addEventListener("input", () => { f.body = el.value; dirty(); }));
    $$("[data-section]", body).forEach((el) => el.addEventListener("input", () => { f.sections[el.dataset.section] = el.value; dirty(); }));
    $$("[data-front]", body).forEach((el) => el.addEventListener("input", () => { f.front[el.dataset.front] = el.value; dirty(); }));
    $("#saveBtn", body).addEventListener("click", () => { f.saved = true; renderWrite(body); toast("Saved " + LAB + f.path); });
  }

  function renderHeuristicForm(body) {
    const mod = current();
    const n = M.heuristics.filter((h) => h.module === mod.id).length + 1;
    const id = `H-${pad(mod.id)}-${n}`;
    body.innerHTML = `<div class="heur-form">
      <label class="field"><span class="eyebrow">If (architectural pattern X)</span><input class="input" id="hx"></label>
      <label class="field"><span class="eyebrow">Then verify (control or failure mode Y)</span><input class="input" id="hy"></label>
      <label class="field"><span class="eyebrow">Evidence (harness test or finding id)</span><input class="input mono" id="he"></label>
      <div class="field"><span class="eyebrow">Will be appended to HEURISTICS.md</span><pre class="heur-preview" id="hp"></pre></div>
      <div><button class="btn btn-primary" id="hAdd" disabled>Append entry</button></div></div>`;
    const x = $("#hx"), y = $("#hy"), e = $("#he"), add = $("#hAdd");
    const rule = () => `If ${x.value.trim() || "<X>"} → then verify ${y.value.trim() || "<Y>"}.`;
    const update = () => {
      $("#hp").textContent = `### ${id}  (Module ${pad(mod.id)})\n${rule()}\nEvidence: ${e.value.trim() || "<evidence>"}`;
      add.disabled = !(x.value.trim() && y.value.trim() && e.value.trim());
    };
    [x, y, e].forEach((el) => el.addEventListener("input", update));
    update();
    add.addEventListener("click", () => {
      M.heuristics.push({ id, module: mod.id, rule: rule(), evidence: e.value.trim() });
      toast(`Appended ${id} to HEURISTICS.md`);
      renderHeuristicForm(body); renderSummary(); renderHeuristics();
    });
  }

  /* ---------- active room: harness ---------- */
  function renderFlags(outcomes) {
    let lastFile = null;
    $("#flags").innerHTML = M.harness.tests.map((t, i) => {
      const o = outcomes[i];
      const [file, name] = t.id.split("::");
      const word = { idle: "", running: "running", pass: "PASS", fail: "FAIL" }[o];
      const head = file !== lastFile ? `<div class="eyebrow">${esc(file)}</div>` : "";
      lastFile = file;
      return `${head}<div class="flag" data-outcome="${o}" title="${esc(t.id)}"><i></i><span>${esc(name)}</span><b>${word}</b></div>`;
    }).join("");
  }
  function renderRecords() {
    const el = $("#records");
    if (!ui.lastRun) { el.textContent = "No run yet in this session."; return; }
    el.innerHTML = `<span>Control conclusions from result records, separate from test outcome:</span>` +
      M.harness.records.map((r) => `<span class="record">${esc(r.control_id)} · ${r.dataset} · ${r.exceptions} exceptions · ${r.conclusion}</span>`).join("");
  }
  function runHarness() {
    if (ui.running) return;
    ui.running = true;
    const btn = $("#runBtn"), term = $("#term");
    btn.disabled = true; btn.textContent = "Running";
    term.innerHTML = "";
    const outcomes = M.harness.tests.map(() => "running");
    renderFlags(outcomes);
    let i = 0;
    (function step() {
      const [text, hits] = M.harness.lines[i];
      const span = document.createElement("span");
      if (i === 0) span.className = "dim";
      else if (/^(E |FAILED)/.test(text)) span.className = "err";
      span.textContent = text + "\n";
      term.appendChild(span); term.scrollTop = term.scrollHeight;
      if (hits) { hits.forEach((k) => { outcomes[k] = M.harness.tests[k].outcome; }); renderFlags(outcomes); }
      i += 1;
      if (i < M.harness.lines.length) return setTimeout(step, 200);
      ui.running = false;
      ui.lastRun = { failed: outcomes.filter((o) => o === "fail").length, passed: outcomes.filter((o) => o === "pass").length };
      btn.disabled = false; btn.innerHTML = "Verify &amp; Run Harness";
      renderRecords(); renderPath();
    })();
  }

  /* ---------- arsenal ---------- */
  function renderHeuristics() {
    const q = ui.heurQuery.toLowerCase();
    const list = M.heuristics.filter((h) => !q || (h.id + " " + h.rule + " " + h.evidence).toLowerCase().includes(q));
    $("#heurList").innerHTML = list.length
      ? list.map((h) => `<div class="heur"><span class="eyebrow">${esc(h.id)} · Module ${pad(h.module)}</span><p>${esc(h.rule)}</p><small>Evidence: ${esc(h.evidence)}</small></div>`).join("")
      : `<span class="empty">No entry matches "${esc(ui.heurQuery)}".</span>`;
  }
  function renderCards() {
    const certs = certCounts(M.flashcards).map(([k]) => k);
    $("#cardFilter").innerHTML = ["all", ...certs].map((c) => `<button aria-pressed="${c === ui.cardFilter}" data-c="${c}">${c}</button>`).join("");
    $$("#cardFilter button").forEach((b) => b.addEventListener("click", () => { ui.cardFilter = b.dataset.c; ui.card = 0; ui.cardSide = "front"; renderCards(); }));
    const deck = M.flashcards.filter((c) => ui.cardFilter === "all" || c.tags.includes(ui.cardFilter + "::"));
    const c = deck[ui.card];
    $("#cardView").innerHTML = `
      <button class="card" id="card" aria-label="Flip card"><span class="eyebrow">${ui.cardSide} · ${esc(c.file)}</span><p>${esc(c[ui.cardSide])}</p></button>
      <div class="card-nav"><button class="btn" id="cardPrev">Previous</button><span class="eyebrow">${ui.card + 1} / ${deck.length}</span><button class="btn" id="cardNext">Next</button></div>
      <div class="card-tags">${c.tags.split(/\s+/).map((t) => `<span class="cert"><span>${esc(t)}</span></span>`).join("")}</div>`;
    $("#card").addEventListener("click", () => { ui.cardSide = ui.cardSide === "front" ? "back" : "front"; renderCards(); });
    const move = (d) => { ui.card = (ui.card + d + deck.length) % deck.length; ui.cardSide = "front"; renderCards(); };
    $("#cardPrev").addEventListener("click", () => move(-1));
    $("#cardNext").addEventListener("click", () => move(1));
  }
  function renderPortfolio() {
    const p = M.portfolio[ui.port];
    $("#portView").innerHTML = `<div class="port-list">${M.portfolio.map((x, i) => `<button role="tab" aria-selected="${i === ui.port}" data-i="${i}"><span>${esc(x.title)}</span><small>${esc(x.path)}</small></button>`).join("")}</div>
      <div class="placeholder">[ rendered Markdown of ${esc(p.path)} ]<br>[ synthetic data only, sanitized, raw HTML disabled ]</div>`;
    $$("#portView .port-list button").forEach((b) => b.addEventListener("click", () => { ui.port = +b.dataset.i; renderPortfolio(); }));
  }

  /* ---------- sync dialog ---------- */
  function stream(term, lines, done) {
    let i = 0;
    (function step() {
      const span = document.createElement("span");
      if (/^(FAIL|WARN):/.test(lines[i])) span.className = "err";
      span.textContent = lines[i] + "\n";
      term.appendChild(span); term.scrollTop = term.scrollHeight;
      i += 1;
      if (i < lines.length) setTimeout(step, 160); else if (done) done();
    })();
  }
  function openSync(kind) {
    const dlg = $("#syncDialog"), term = $("#syncTerm"), files = $("#syncFiles"), foot = $("#syncFoot");
    term.innerHTML = ""; files.innerHTML = ""; foot.innerHTML = "";
    if (kind === "down") {
      $("#syncTitle").textContent = "Sync Down · bash scripts/sync_down.sh";
      foot.hidden = true;
      dlg.showModal();
      stream(term, M.sync.downLines);
    } else {
      $("#syncTitle").textContent = "Sync Up · bash scripts/sync_up.sh";
      files.innerHTML = `<div class="eyebrow file-list-title">Files that will be committed (${M.sync.upFiles.length})</div><ul class="file-list">${M.sync.upFiles.map((f) => `<li>${esc(f)}</li>`).join("")}</ul>`;
      term.innerHTML = '<span class="dim">Waiting for your go-ahead.\n</span>';
      foot.hidden = false;
      foot.innerHTML = `<button class="btn" id="syncCancel">Cancel</button><button class="btn btn-primary" id="syncGo">Run sync-up</button>`;
      $("#syncCancel").addEventListener("click", () => dlg.close());
      $("#syncGo").addEventListener("click", (e) => { e.target.disabled = true; term.innerHTML = ""; stream(term, M.sync.upLines); });
      dlg.showModal();
    }
  }

  /* ---------- shell ---------- */
  function setView(v) {
    ui.view = v;
    ["map", "room", "arsenal"].forEach((k) => { $("#view-" + k).hidden = k !== v; });
    $$(".view-tab").forEach((t) => { if (t.dataset.view === v) t.setAttribute("aria-current", "page"); else t.removeAttribute("aria-current"); });
    if (v === "map") requestAnimationFrame(drawLines);
  }
  function setDir(d) {
    document.body.dataset.dir = d;
    $$("#dirSeg button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.dir === d)));
    requestAnimationFrame(drawLines);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => requestAnimationFrame(drawLines));
  }
  function setStage(s) {
    const k = M.STAGES.indexOf(s);
    M.state.current_stage = s;
    current().stage_history = M3_DATES.slice(0, k + 1).map((d, i) => ({ stage: M.STAGES[i], entered_on: d }));
    $$("#stageSeg button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.stage === s)));
    ui.file = null;
    renderPath(); renderDetail(); renderBanner(); renderLeft(); renderWork();
  }

  $$(".view-tab").forEach((t) => t.addEventListener("click", () => setView(t.dataset.view)));
  $$("#leftTabs .tab").forEach((t) => t.addEventListener("click", () => { ui.leftTab = t.dataset.tab; renderLeft(); }));
  $$("#workTabs .tab").forEach((t) => t.addEventListener("click", () => { ui.workTab = t.dataset.tab; renderWork(); }));
  $$("#dirSeg button").forEach((b) => b.addEventListener("click", () => setDir(b.dataset.dir)));
  $$("#stageSeg button").forEach((b) => b.addEventListener("click", () => setStage(b.dataset.stage)));
  $("#runBtn").addEventListener("click", runHarness);
  $("#syncDown").addEventListener("click", () => openSync("down"));
  $("#syncUp").addEventListener("click", () => openSync("up"));
  $("#syncClose").addEventListener("click", () => $("#syncDialog").close());
  $("#heurSearch").addEventListener("input", (e) => { ui.heurQuery = e.target.value; renderHeuristics(); });
  window.addEventListener("resize", drawLines);

  $("#runCmd").textContent = M.harness.command;
  renderSummary();
  renderFlags(M.harness.tests.map(() => "idle"));
  renderRecords(); renderHeuristics(); renderCards(); renderPortfolio();
  setDir(["a", "b", "c"].includes(params.get("dir")) ? params.get("dir") : "a");
  setView(["map", "room", "arsenal"].includes(ui.view) ? ui.view : "map");
  setStage(["incubation", "lab", "gate"].includes(params.get("stage")) ? params.get("stage") : M.state.current_stage);
})();
