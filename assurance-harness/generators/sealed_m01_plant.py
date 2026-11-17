# SEALED: Module 1 planting logic and answer-key writer. The learner must not read this file before the Module 1 gate.
"""Planted conditions for the Module 1 `planted` dataset and the Q3 contrastive pair.

Imported by m01_iam.py. Holds no data of its own; every draw comes from
random.Random seeded from the generator's fixed SEED.
"""
from __future__ import annotations

import pathlib
import random

P_LATE = [0.02, 0.04, 0.08, 0.15, 0.25, 0.38]  # Apr..Sep share of leavers disabled late


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _legacy_owned(w, a) -> bool:
    return w.by_canon[a["owner"]]["legacy"]


def _certify_both(w, a) -> bool:
    if not a["rv"]:
        return True
    return all(w.review_rng(cid, a["id"]).random() >= 0.03 for cid, _s, _e in w.k.CAMPAIGNS)


def _month_index(k, ts) -> int:
    bounds = [k.T(2026, m, 1) for m in (5, 6, 7, 8, 9)]
    return sum(1 for b in bounds if ts >= b)


# ---------------------------------------------------------------------------
# main planted dataset
# ---------------------------------------------------------------------------
def main_profile(Profile):
    class MainPlanted(Profile):
        def after_provisioning(self, w):
            _plant_main(w)

        def population(self, w, campaign_id, accounts):
            return [a for a in accounts if not _legacy_owned(w, a)]

        def finalize(self, w):
            _finalize_main(w)

    return MainPlanted()


def _plant_main(w):
    k = w.k
    T, DAY, HOUR, MINUTE = k.T, k.DAY, k.HOUR, k.MINUTE
    prng = random.Random(f"{k.SEED}|{w.label}|plant")
    m = w.manifest

    # PF-05 lapsed exceptions ----------------------------------------------
    sod = sorted((r for r in w.requests if r["type"] == "sod_exception"), key=lambda r: r["id"])
    refund = [r for r in sod if r["perm"].startswith("refund")]
    iam = [r for r in sod if r["perm"].startswith("iam")]
    lapse_sod = sorted(prng.sample(refund, 4), key=lambda r: r["id"]) + prng.sample(iam, 1)
    for r, exp in zip(lapse_sod, [T(2026, 5, 31, 23, 59, 59), T(2026, 6, 30, 23, 59, 59),
                                  T(2026, 7, 31, 23, 59, 59), T(2026, 8, 31, 23, 59, 59),
                                  T(2026, 9, 15, 23, 59, 59)]):
        r["expires"] = exp
    noms = sorted((r for r in w.requests if r["type"] == "privileged_nomination"), key=lambda r: r["id"])
    lapse_nom = sorted(prng.sample(noms, 3), key=lambda r: r["id"])
    for r, exp in zip(lapse_nom, [T(2026, 6, 30, 23, 59, 59), T(2026, 7, 31, 23, 59, 59),
                                  T(2026, 8, 31, 23, 59, 59)]):
        r["expires"] = exp
    m["lapsed_sod"] = lapse_sod
    m["lapsed_nom"] = lapse_nom

    # PF-03 orphaned accounts of departed contractors ------------------------
    managers = sorted({i["manager"] for i in w.identities if i["manager"]})
    mgr_set = set(managers)
    cutoff = T(2026, 4, 6)
    busy = set()
    for r in w.requests:
        if r["requested"] >= cutoff:
            busy.add(r["by"])
            busy.add(r["subject"])
    for e in w.entitlements:
        if e["granted"] >= cutoff:
            busy.add(w.acct_by_id[e["acct"]]["owner"])

    def orphan_ok(i, contractor):
        if not (i["role"] == "staff" and i["contractor"] == contractor and i["term"] is None
                and i["canon"] not in mgr_set and not i["owns_services"]
                and i["canon"] not in w.special_ids and i["hire"] < T(2026, 1, 1)
                and i["canon"] not in busy):
            return False
        accts = w.accounts_of(i["canon"])
        return all(a["disabled"] is None and _certify_both(w, a) for a in accts)

    legacy_c = sorted((i for i in w.identities if i["legacy"] and orphan_ok(i, True)), key=lambda i: i["canon"])
    if len(legacy_c) < 2:
        legacy_c += sorted((i for i in w.identities if i["legacy"] and orphan_ok(i, False)), key=lambda i: i["canon"])
    canon_c = sorted((i for i in w.identities if not i["legacy"] and orphan_ok(i, True)), key=lambda i: i["canon"])
    orphans = sorted(prng.sample(legacy_c, 2), key=lambda i: i["canon"]) + prng.sample(canon_c, 1)
    for i in orphans:
        i["term"] = T(2026, 4, 6) + prng.randrange(0, 50) * DAY + 16 * HOUR + prng.randrange(0, 2 * HOUR)
        w.extended.append(i["canon"])
    m["orphans"] = [i["canon"] for i in orphans]

    # PF-02 deprovisioning drift ---------------------------------------------
    orphan_set = set(m["orphans"])
    leavers = sorted((i for i in w.identities if i["term"] is not None and k.P0 <= i["term"] < k.P1
                      and i["canon"] not in orphan_set), key=lambda i: i["canon"])
    late = []
    for i in leavers:
        mi = _month_index(k, i["term"])
        u, x = prng.random(), prng.random()
        is_late = u < P_LATE[mi]
        if is_late:
            lag = 24 * HOUR + int(2 * HOUR + x * (12 * HOUR + mi * 30 * HOUR))
            late.append(i["canon"])
        else:
            lag = i["deprov_lag"] + mi * 36 * MINUTE
        for a in w.accounts_of(i["canon"]):
            if a["reason"] != "hr_termination":
                continue
            d = i["term"] + lag + prng.randrange(0, 1800)
            if d >= k.P1:
                a["disabled"], a["reason"] = None, None
            else:
                a["disabled"] = d
    m["late_leavers"] = late

    # PF-04 accounts missing from inventory ----------------------------------
    cut = T(2026, 3, 1)
    svc = [a for a in sorted(w.accounts, key=lambda a: a["id"])
           if a["type"] == "service" and a["disabled"] is None and a["created"] < cut
           and not _legacy_owned(w, a) and _certify_both(w, a)]
    hum = [a for a in sorted(w.accounts, key=lambda a: a["id"])
           if a["type"] == "human" and a["realm"] in ("reporting", "sandbox") and a["disabled"] is None
           and a["created"] < cut and w.by_canon[a["hr"]]["term"] is None and not _legacy_owned(w, a)
           and a["hr"] not in w.special_ids and a["hr"] not in orphan_set and _certify_both(w, a)]
    hidden = prng.sample(svc, 11) + prng.sample(hum, 5)
    w.excluded = sorted(a["id"] for a in hidden)
    admins = sorted(x["id"] for c in w.special["iam.admin"] for x in w.accounts_of(c) if x["realm"] == "admin")
    m["hidden_granter"] = prng.choice(admins)


def _finalize_main(w):
    hidden = set(w.excluded)
    w.requests = [r for r in w.requests if r["acct"] not in hidden]
    for e in w.entitlements:
        if e["acct"] in hidden:
            e["req"] = None
            e["by"] = w.manifest["hidden_granter"]
    disabled = {a["id"] for a in w.accounts if a["disabled"] is not None and a["id"] not in hidden}
    purged = [e for e in w.events if e["acct"] in disabled]
    w.events = [e for e in w.events if e["acct"] not in disabled]
    w.manifest["purged_events"] = purged


# ---------------------------------------------------------------------------
# contrastive pair
# ---------------------------------------------------------------------------
_BUILD = {}


def build_pair(make_world, Profile, base_n, seed):
    _BUILD["make_world"] = make_world
    class ReviewListFromJoin(Profile):
        def population(self, w, campaign_id, accounts):
            return [a for a in accounts if not _legacy_owned(w, a)]

    prng = random.Random(f"{seed}|pair")
    flawed = "A" if prng.random() < 0.5 else "B"
    good = "B" if flawed == "A" else "A"
    n_f = base_n + prng.randrange(-60, 61)
    wf = make_world(f"q3-snapshot-{flawed}", n_f, ReviewListFromJoin())
    cid, snap, _e = wf.k.CAMPAIGNS[1]
    active = [a for a in wf.accounts if a["created"] < snap and (a["disabled"] is None or a["disabled"] >= snap)]
    listed = sum(1 for v in wf.reviews if v["cid"] == cid)
    n_g = round(n_f * listed / len(active)) + prng.randrange(-12, 13)
    wg = make_world(f"q3-snapshot-{good}", n_g, None)
    manifest = {"flawed": flawed, "good": good, "n_flawed": n_f, "n_good": n_g}
    return {flawed: wf, good: wg}, manifest


# ---------------------------------------------------------------------------
# answer key
# ---------------------------------------------------------------------------
def _unreviewed(w, cid, snap):
    hidden = set(w.excluded)
    reviewed = {v["acct"] for v in w.reviews if v["cid"] == cid}
    return sorted(a["id"] for a in w.accounts
                  if a["id"] not in hidden and a["created"] < snap
                  and (a["disabled"] is None or a["disabled"] >= snap) and a["id"] not in reviewed)


def _wrap(ids, per_line=8):
    lines = []
    for i in range(0, len(ids), per_line):
        lines.append("    " + ", ".join(ids[i:i + per_line]))
    return "\n".join(lines) if lines else "    (none)"


def write_answer_key(path: pathlib.Path, w, pair, pm, k):
    T, DAY, HOUR, fmt = k.T, k.DAY, k.HOUR, k.fmt
    m = w.manifest
    hidden = set(w.excluded)
    L = []
    add = L.append
    add("# SEALED ANSWER KEY: Module 1 (m01-risk-controls-independence)")
    add("")
    add("Written by `first-line-engineer` from the generator's own output "
        f"(`assurance-harness/generators/m01_iam.py`, SEED {k.SEED}). Format: `spec/SCHEMAS.md` section 4.")
    add("Not to be shown to the learner before the gate's artifact check. `red-team` does not read it.")
    add("")
    add("Datasets: `assurance-harness/data/m01/planted.duckdb` (all planted flaws below) and "
        "`assurance-harness/data/m01/clean.duckdb` (none of them; expected exceptions on every control = 0).")
    add("Observation period 2026-04-01 00:00:00 to 2026-09-30 23:59:59. Review campaigns 2026Q2 "
        "(population as at 2026-06-01 00:00:00, window to 2026-06-21) and 2026Q3 (as at 2026-09-01 00:00:00, "
        "window to 2026-09-21).")
    add("")
    add("Identifier note (realistic constraint, present in BOTH datasets): `hr_identities.hr_id` holds the raw HR "
        "export identifier. Rows with `record_source = 'hris_legacy_import'` use legacy formats "
        "(`E-012345`, `e012345`, `E12345`, `012345`). `iam_accounts.hr_id`, `owner_hr_id`, `manager_hr_id` and "
        "all reviewer/approver columns use the canonical form: prefix letter plus 6 digits. Normalise with: strip, "
        "upper-case, drop '-', take the digits as an integer and match on the number (numbers are unique across "
        "E and C).")
    n_legacy = sum(1 for i in w.identities if i["legacy"])
    add(f"Legacy-format identities in planted/clean: {n_legacy}.")
    add("")

    # PF-01
    add("---")
    add("")
    add("## PF-01")
    add("- **id:** PF-01")
    add("- **type:** incomplete_population")
    add("- **where:** `access_reviews` (planted), both campaigns. The review list was built by an inner join of "
        "`iam_accounts.owner_hr_id` to `hr_identities.hr_id` on the exact string. Accounts whose owner's HR record "
        "carries a legacy-format identifier fall out of the join silently, so they were never put in front of a "
        "reviewer. The campaign still shows 100% completion because completion is measured against the list.")
    for cid, snap, _e in k.CAMPAIGNS:
        ids = _unreviewed(w, cid, snap)
        n_h = sum(1 for x in ids if w.acct_by_id[x]["type"] == "human")
        listed = sum(1 for v in w.reviews if v["cid"] == cid)
        add(f"- **expected exceptions, {cid}:** {len(ids)} active accounts not reviewed "
            f"({n_h} human, {len(ids) - n_h} service); list size {listed}, population {listed + len(ids)}.")
        add(f"  - ids ({cid}):")
        add(_wrap(ids))
    add("- **which control it defeats:** LD-AC-03 (AC-2, CA-7).")
    add("- **detection:** reconcile each campaign's reviewed accounts to `iam_accounts` active at the population "
        "date (created_at < as-at and (disabled_at is null or disabled_at >= as-at)). Clean: 0 unreviewed.")
    add("")

    # PF-02 and PF-03: LD-AC-02 exceptions computed from final data
    term_by = {i["canon"]: i for i in w.identities if i["term"] is not None}
    exc = []
    for a in sorted(w.accounts, key=lambda a: a["id"]):
        if a["type"] != "human" or a["id"] in hidden or a["hr"] not in term_by:
            continue
        t = term_by[a["hr"]]["term"]
        if a["disabled"] is None:
            exc.append((a, "not_disabled", None))
        elif a["disabled"] > t + 24 * HOUR:
            exc.append((a, "late", (a["disabled"] - t) / HOUR))
    orphan_set = set(m["orphans"])
    drift_exc = [x for x in exc if x[0]["hr"] not in orphan_set]
    orph_exc = [x for x in exc if x[0]["hr"] in orphan_set]
    add("---")
    add("")
    add("## PF-02")
    add("- **id:** PF-02")
    add("- **type:** drift")
    add("- **where:** `iam_accounts.disabled_at` against `hr_identities.termination_ts` for leavers in the period "
        "(planted). The share of leavers disabled more than 24 hours after termination rises month by month "
        "(target rates Apr..Sep: " + ", ".join(f"{p:.0%}" for p in P_LATE) + "), and the lag of on-time disables "
        "creeps up too (about +36 minutes per month). Some September leavers are still active at period end.")
    leavers = sorted((i for i in w.identities if i["term"] is not None and k.P0 <= i["term"] < k.P1
                      and i["canon"] not in orphan_set), key=lambda i: i["canon"])
    exc_leavers = {x[0]["hr"] for x in drift_exc}
    by_month = {}
    for i in leavers:
        mi = _month_index(k, i["term"])
        by_month.setdefault(mi, [0, 0])
        by_month[mi][0] += 1
        if i["canon"] in exc_leavers:
            by_month[mi][1] += 1
    assert sum(v[1] for v in by_month.values()) == len(exc_leavers), "PF-02 breakdown does not sum to total"
    assert sum(v[0] for v in by_month.values()) == len(leavers)
    scoped_total = len(leavers)
    # literal population: every hr_identities row with termination_ts inside the period, as written to the DB
    p_lo, p_hi = fmt(k.P0), fmt(k.P1)
    literal = [0] * 6
    for row in w.table_rows()["hr_identities"]:
        t = row[9]
        if t is not None and p_lo <= t < p_hi:
            literal[int(t[5:7]) - 4] += 1
    db = path.parents[3] / "assurance-harness" / "data" / "m01" / "planted.duckdb"
    if db.is_file():
        import duckdb
        con = duckdb.connect(str(db), read_only=True)
        try:
            got = dict(con.execute(
                "SELECT month(termination_ts) - 4, count(*) FROM hr_identities "
                "WHERE termination_ts >= ? AND termination_ts < ? GROUP BY 1", (p_lo, p_hi)).fetchall())
        finally:
            con.close()
        assert [got.get(mi, 0) for mi in range(6)] == literal, "PF-02 literal counts differ from planted.duckdb"
    lit_total = sum(literal)
    other = [c for c in sorted(orphan_set) if k.P0 <= w.by_canon[c]["term"] < k.P1]
    for mi in range(6):
        n_other = sum(1 for c in other if _month_index(k, w.by_canon[c]["term"]) == mi)
        assert literal[mi] == by_month.get(mi, [0, 0])[0] + n_other, "PF-02 month denominator mismatch"
    assert sum(literal) == lit_total
    assert lit_total - len(other) == scoped_total, "PF-02 literal total minus PF-03 leavers != scoped total"
    names = ["Apr", "May", "Jun", "Jul", "Aug", "Sep"]
    add(f"- **PF-02 exception leavers / all leavers in the period, by termination month:** " + "; ".join(
        f"{names[mi]} {by_month.get(mi, [0, 0])[1]}/{literal[mi]}" for mi in range(6))
        + f". Denominators are the literal population: every `hr_identities` row in `planted.duckdb` with "
        f"`termination_ts` from 2026-04-01 00:00:00 up to (not including) 2026-10-01 00:00:00, "
        f"{lit_total} in total. {len(other)} of those leavers are accounted for under PF-03 (their accounts "
        "were never disabled) and are therefore not counted as PF-02 exceptions; the numerators count PF-02 "
        "exception leavers only and use the same exception rows as the totals below.")
    late_ids = [x[0]["id"] for x in drift_exc if x[1] == "late"]
    nd_ids = [x[0]["id"] for x in drift_exc if x[1] == "not_disabled"]
    add(f"- **expected exceptions:** {len(drift_exc)} human accounts belonging to {len({x[0]['hr'] for x in drift_exc})} "
        f"leavers: {len(late_ids)} disabled more than 24h after termination, {len(nd_ids)} still active at "
        "period end with termination more than 24h before it.")
    naive = sum(1 for x in drift_exc if term_by[x[0]["hr"]]["raw"] == x[0]["hr"])
    add(f"  - an exact-string join of `iam_accounts.hr_id` to `hr_identities.hr_id` finds only {naive} of these "
        "(the rest belong to legacy-format HR records).")
    add("  - late (account_id, hours after termination):")
    add(_wrap([f"{x[0]['id']} ({x[2]:.1f}h)" for x in drift_exc if x[1] == "late"], 5))
    add("  - not disabled:")
    add(_wrap(nd_ids))
    add("  - leavers (canonical hr_id): " + ", ".join(sorted({x[0]["hr"] for x in drift_exc})))
    add("- **which control it defeats:** LD-AC-02 (AC-2).")
    add("- **detection:** full population of leavers (normalised identifiers) against disable timestamps; trend by "
        "month. Clean: every leaver's human accounts disabled within 24h (max lag about 20.5h).")
    add("")

    add("---")
    add("")
    add("## PF-03")
    add("- **id:** PF-03")
    add("- **type:** planted_exception")
    add("- **where:** three contractors terminated in April-May 2026 in `hr_identities` (planted) whose accounts "
        "were never disabled and kept authenticating after termination (`auth_events`). This is the dilemma's "
        "'contractor who left in the spring'. Two of the three have legacy-format HR identifiers, so an exact join "
        "misses them, and the access review (PF-01) never listed their accounts. The third is canonical; its "
        "account was certified by the line manager in the review(s) after the person left.")
    for c in m["orphans"]:
        i = w.by_canon[c]
        accts = [a for a in w.accounts_of(c)]
        evs = [e for e in w.events if e["acct"] in {a["id"] for a in accts} and e["ts"] > i["term"]
               and e["result"] == "success"]
        last = max((e["ts"] for e in evs), default=None)
        certified = sorted({v["cid"] for v in w.reviews if v["acct"] in {a["id"] for a in accts}})
        add(f"  - {c} (HR export id `{i['raw']}`), terminated {fmt(i['term'])}; accounts "
            f"{', '.join(a['id'] for a in accts)}; {len(evs)} successful logins after termination, last "
            f"{fmt(last)}; certified in campaigns: {', '.join(certified) if certified else 'none (not on list)'}.")
    cat = _certify_after_termination(w)
    add(f"- **expected exceptions:** {len(orph_exc)} accounts not disabled (ids: "
        f"{', '.join(x[0]['id'] for x in orph_exc)}); {len(cat)} `access_reviews` rows with decision "
        f"'certify' dated after the holder's HR termination (ids: {', '.join(cat) if cat else 'none'}). "
        "These are the only certify-after-termination rows in planted; clean has none.")
    add("- **which control it defeats:** LD-AC-02 (AC-2); also LD-AC-03 (a departed person's account certified, "
        "or not reviewed at all).")
    add("")

    # PF-04
    add("---")
    add("")
    add("## PF-04")
    add("- **id:** PF-04")
    add("- **type:** missing_inventory")
    add("- **where:** 16 accounts that exist in `entitlements` and `auth_events` (planted) but have no row in "
        "`iam_accounts` and no `access_requests`. Backstory: created directly in the directory backend during an "
        "integration cut-over and never registered in IAM. Their entitlements carry `approval_ref` NULL and "
        f"`granted_by` = `{m['hidden_granter']}` (an IAM admin account). Account ids are random, so there is no "
        "sequence gap in `iam_accounts`; `access_requests` ids have gaps where their requests were removed.")
    n_ent = sum(1 for e in w.entitlements if e["acct"] in hidden)
    n_ev = sum(1 for e in w.events if e["acct"] in hidden)
    for x in w.excluded:
        a = w.acct_by_id[x]
        ne = sum(1 for e in w.entitlements if e["acct"] == x)
        nv = sum(1 for e in w.events if e["acct"] == x)
        add(f"  - {x} ({a['type']}, {a['realm']}, username `{a['username']}`): {ne} entitlements, {nv} auth events")
    add(f"- **expected exceptions:** 16 account ids (above); {n_ent} entitlement rows with no approval reference; "
        f"{n_ev} auth events from accounts outside the inventory.")
    add("- **which control it defeats:** LD-AC-03 (population: never reviewed because not in the system of record); "
        "also LD-AC-01 (grants with no approval).")
    add("- **detection:** reconcile distinct `account_id` in `entitlements` and `auth_events` to `iam_accounts`. "
        "Clean: every account id in every table exists in `iam_accounts`.")
    add("")

    # PF-05
    add("---")
    add("")
    add("## PF-05")
    add("- **id:** PF-05")
    add("- **type:** planted_exception")
    add("- **where:** `access_requests` rows of type `sod_exception` and `privileged_nomination` (planted) whose "
        "`expires_at` fell inside the period, while the covered entitlements stayed active to period end. In clean "
        "every exception expires 2026-12-31 and every nomination 2027-03-31.")
    for r in m["lapsed_sod"]:
        add(f"  - {r['id']} sod_exception `{r['perm']}` for {r['subject']} (account {r['acct']}), "
            f"expired {fmt(r['expires'])}")
    for r in m["lapsed_nom"]:
        add(f"  - {r['id']} privileged_nomination `{r['perm']}` for {r['subject']} (account {r['acct']}), "
            f"expired {fmt(r['expires'])}")
    add("- **expected exceptions:** 5 identities holding a toxic pair under a lapsed exception (LD-AC-04); "
        "3 privileged holdings whose named-owner nomination lapsed (LD-AC-05).")
    add("- **which control it defeats:** LD-AC-04 (AC-5) and LD-AC-05 (AC-6).")
    add("")

    # PF-06
    purged = m["purged_events"]
    acc_p = sorted({e["acct"] for e in purged})
    p0 = k.P0
    dis_in = sorted(a["id"] for a in w.accounts if a["id"] not in hidden and a["disabled"] is not None
                    and p0 <= a["disabled"] < k.P1)
    remaining = {e["acct"] for e in w.events}
    dis_in_zero = [x for x in dis_in if x not in remaining]
    add("---")
    add("")
    add("## PF-06")
    add("- **id:** PF-06")
    add("- **type:** survivorship")
    add("- **where:** `auth_events` (planted). The telemetry export only carries events for accounts that are not "
        "disabled at export time; when an account is disabled its history drops out. Every disabled account has "
        "zero events, including accounts that were active for months of the period, and the late-disabled leavers "
        "in PF-02. The only post-termination activity that survives is from accounts that were never disabled "
        "(PF-03). `event_id` is assigned before the export filter, so the sequence has gaps.")
    add(f"- **expected:** {len(purged)} events removed across {len(acc_p)} accounts; {len(dis_in)} accounts "
        f"disabled during the period, of which {len(dis_in_zero)} have zero auth events. Clean: every account "
        "disabled during the period has at least one event before its disable time, and `event_id` is contiguous "
        f"({7000001} upward).")
    add("- **which control it defeats:** the evidence for LD-AC-02 (any test of whether late-disabled accounts "
        "were used after termination returns a false 'no use') and the CA-7 monitoring claim under LD-AC-03.")
    add("")

    # PF-07 pair
    flawed, good = pm["flawed"], pm["good"]
    wf, wg = pair[flawed], pair[good]
    cid, snap, _e = k.CAMPAIGNS[1]
    om = _unreviewed(wf, cid, snap)
    om_q2 = _unreviewed(wf, k.CAMPAIGNS[0][0], k.CAMPAIGNS[0][1])
    n_h = sum(1 for x in om if wf.acct_by_id[x]["type"] == "human")
    listed_f = sum(1 for v in wf.reviews if v["cid"] == cid)
    listed_g = sum(1 for v in wg.reviews if v["cid"] == cid)
    add("---")
    add("")
    add("## PF-07 (stage 1 contrastive pair)")
    add("- **id:** PF-07")
    add("- **type:** incomplete_population")
    add(f"- **flawed package:** `evidence/q3_access_review/package_{flawed}/` (system of record "
        f"`data/q3_review_snapshot_{flawed}.duckdb`). Reconciling package: `package_{good}/`.")
    add(f"- **where:** the package's `review_decisions.csv` and that snapshot's `access_reviews` for 2026Q3. "
        f"List size {listed_f}; active accounts in `iam_accounts` at 2026-09-01 00:00:00: {listed_f + len(om)}. "
        f"Package {good}: list size {listed_g} = its active population (reconciles exactly).")
    add(f"- **expected exceptions:** {len(om)} active accounts omitted from the Q3 list ({n_h} human, "
        f"{len(om) - n_h} service). The same query also omitted {len(om_q2)} accounts in 2026Q2.")
    add("  - omitted account ids (2026Q3):")
    add(_wrap(om))
    add("- **why the omission is plausible:** the list query joins accounts to the HR export to route each account "
        "to a reviewer (manager or service owner), and does it as an inner join on the raw `hr_id` string. Owners "
        "whose HR records came from the previous HRIS keep legacy-format identifiers, so their accounts (human "
        "accounts of those people and service accounts they own) drop out without an error. Every account that "
        "does reach the list is reviewed, signed off and actioned, so completion is genuinely 100% of the list. "
        "Nothing in the package shows the gap: account ids are random, the human/service mix is unchanged, "
        "and the snapshot world was sized so the headline count matches the other package.")
    add("- **which control it defeats:** LD-AC-03.")
    add("")

    # bypasses in the simulator
    add("---")
    add("")
    add("## Simulator gaps (labs/m01-risk-controls-independence/larkspur/), for the red-team step")
    add("")
    for b in _bypass_entries(w, pair):
        add(b)
    add("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def _certify_after_termination(w):
    excluded = set(w.excluded)
    out = []
    for v in w.reviews:
        a = w.acct_by_id[v["acct"]]
        if v["decision"] != "certify" or a["type"] != "human" or a["id"] in excluded:
            continue
        t = w.by_canon[a["hr"]]["term"]
        if t is not None and v["decided"] >= t:
            out.append(v["id"])
    return sorted(out)


def _grant_signatures(w):
    """Entitlement ids matching the B-01 signature (approval_ref present but not an approved request for the
    same account and permission decided before the grant) and the B-02 signature (approval_ref NULL)."""
    reqs = {r["id"]: r for r in w.requests}
    b01, b02 = [], []
    for e in w.entitlements:
        if e["req"] is None:
            b02.append(e["id"])
            continue
        r = reqs.get(e["req"]["id"])
        ok = (r is not None and r["status"] == "approved" and r["decided"] is not None
              and r["decided"] < e["granted"] and r["acct"] == e["acct"]
              and (r["type"] != "add_permission" or r["perm"] == e["perm"]))
        if not ok:
            b01.append(e["id"])
    return sorted(b01), sorted(b02)


def _bypass_entries(w, pair):
    excluded = set(w.excluded)
    pf04_rows = sorted(e["id"] for e in w.entitlements if e["acct"] in excluded)
    p_b01, p_b02 = _grant_signatures(w)
    assert p_b01 == [], "planted has B-01-signature rows"
    assert p_b02 == pf04_rows, "planted B-02-signature rows differ from the PF-04 rows"
    clean = _BUILD["make_world"]("main", w.N)
    for other in (clean, pair["A"], pair["B"]):
        assert _grant_signatures(other) == ([], []), "B-01/B-02 signature rows outside planted"
    return [
        "What 'expected' means for the B entries: the count of rows **produced through the simulator** in the "
        "generated datasets is 0 for every B entry (no simulator command was used to build them). That is not "
        "the same as 'no row looks like it'. Rows with the literal B-02 signature (`entitlements.approval_ref` "
        f"NULL) do exist in planted: exactly {len(p_b02)}, and they are exactly the entitlement rows of the "
        "PF-04 accounts (all of them, and no other rows). Rows with the literal B-01 signature (approval_ref "
        "present but not resolving to an approved request for the same account and permission decided before "
        "the grant): 0 in planted. Clean, q3_review_snapshot_A and q3_review_snapshot_B: 0 rows with either "
        "signature. The key writer asserts all of this against the data when it writes this file.",
        "",
        "### B-01",
        "- **id:** B-01",
        "- **type:** bypass",
        "- **where:** `larkspur_cli.py grant --actor ADMIN --account ID --permission P --approval-ref X`.",
        "- **expected (observable behaviour):** succeeds for any value of X, including an id that does not "
        "exist in `access_requests`, one that is pending or rejected, one for another account or permission, or "
        "one decided after the grant. X is not stored verbatim: leading and trailing whitespace is stripped "
        "before storage, and a whitespace-only X is stored as NULL (which is then the B-02 case). Per "
        "invocation it writes exactly 1 row to `entitlements` (approval_ref = stripped X, granted_by = actor) "
        "and 1 row to `auth_events` (actor, method sso, collector admin-console, result success); 0 rows to "
        "`access_requests`. Exception population for a tester: entitlements whose approval_ref does not "
        "resolve to an approved request for the same account (and permission) decided before granted_at.",
        "- **which control it defeats:** LD-AC-01 (the grant looks approved if `entitlements` is inspected "
        "alone).",
        "",
        "### B-02",
        "- **id:** B-02",
        "- **type:** bypass",
        "- **where:** `larkspur_cli.py grant` without `--approval-ref` (or with a whitespace-only value).",
        "- **expected (observable behaviour):** succeeds. Per invocation: 1 row in `entitlements` with "
        "approval_ref NULL and granted_by = actor, 1 row in `auth_events` (the actor's admin-console sso "
        "success, which does not name the permission or target account), 0 rows in `access_requests`. Nothing "
        "blocks or alerts.",
        "- **which control it defeats:** LD-AC-01 as a preventive control (detectable only after the fact, as "
        "approval_ref NULL).",
        "",
        "### B-03",
        "- **id:** B-03",
        "- **type:** bypass",
        "- **where:** `larkspur_cli.py create-account` (T1136).",
        "- **expected (observable behaviour):** succeeds with no provisioning request; `--request-ref` is "
        "optional and is stored unvalidated. Per invocation: 1 row in `iam_accounts` (status active, "
        "provisioning_request_id NULL or the unvalidated value; no column of the row names the actor), 1 row in "
        "`auth_events` (actor admin-console sso success), 0 rows in `access_requests`, 0 rows in "
        "`entitlements`. The account is in the inventory, so the next complete review population includes it.",
        "- **which control it defeats:** depends on how LD-AC-01 is read; a grader should accept either "
        "attribution if the reasoning matches. (a) Reading LD-AC-01 by its control statement ('every "
        "entitlement grant has an owner-approved request dated before the grant'): create-account grants no "
        "entitlement, so none of LD-AC-01 to LD-AC-05 is defeated; it is a design gap against AC-2 account "
        "management, and any entitlement later granted to the account falls under B-01 or B-02. (b) Reading "
        "LD-AC-01 by its 'How it operates' paragraph in SYSTEM.md, which says new accounts are created from an "
        "approved `new_account` request and that admin-console changes record the approved request reference: "
        "account creation is inside LD-AC-01's operation, and B-03 defeats LD-AC-01 (an account exists with no "
        "approved `new_account` request).",
        "",
        "### B-04",
        "- **id:** B-04",
        "- **type:** bypass",
        "- **where:** `larkspur_cli.py authenticate ACCOUNT --method api_token` on an account with status "
        "disabled (T1078).",
        "- **expected (observable behaviour):** succeeds. Per invocation: 1 row in `auth_events` with result "
        "success, method api_token, collector api-gw-1, for the disabled account. The same call with method "
        "sso or password writes 1 row with result failure, reason account_disabled.",
        "- **which control it defeats:** LD-AC-02 (disabling the account does not stop token use, so the "
        "control's objective is not met even when the disable is on time).",
        "",
        "### B-05",
        "- **id:** B-05",
        "- **type:** survivorship",
        "- **where:** simulator telemetry (T1087).",
        "- **expected (observable behaviour):** `info`, `list-*`, `describe-*` and `sql` write 0 rows to any "
        "table. `authenticate` against an account id that is not in `iam_accounts` prints 'authentication "
        "failed' and writes 0 rows to any table. `grant`, `create-account` and `disable-account`: if the actor "
        "id is not in `iam_accounts`, 0 rows; if the actor is disabled or lacks iam.admin, exactly 1 "
        "`auth_events` row (actor, sso, admin-console, failure, reason account_disabled or not_authorized) and "
        "nothing else; if the actor is accepted, exactly 1 `auth_events` row (actor, sso, admin-console, "
        "success) plus the change itself (`grant`: 1 `entitlements` insert; `create-account`: 1 "
        "`iam_accounts` insert; `disable-account`: 1 `iam_accounts` row updated in status, disabled_at, "
        "disable_reason), or only the actor row if the target check then fails. Where the actor is recorded, "
        "per command: `grant` records the actor on the changed row itself (`entitlements.granted_by`) as well "
        "as in the sign-in row; `create-account` and `disable-account` record the actor only in the sign-in "
        "row (no column of the inserted or updated `iam_accounts` row names the actor). No row anywhere records "
        "which command ran or its parameters, and there is no separate admin audit table.",
        "- **which control it defeats:** none of LD-AC-01 to LD-AC-05 directly. It is a telemetry gap: "
        "discovery and failed attempts against non-existent accounts leave no record; a `grant` can be "
        "attributed directly from `entitlements.granted_by`, but a `create-account` or `disable-account` can "
        "be attributed only by joining the changed row's timestamp to the actor's sign-in row.",
    ]
