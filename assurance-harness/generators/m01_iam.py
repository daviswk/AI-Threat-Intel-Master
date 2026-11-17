"""Larkspur Desk identity and access data generator (Module 1).

Builds the six identity-and-access tables of Larkspur Desk for the
observation period 2026-04-01 00:00:00 to 2026-09-30 23:59:59 (UTC, stored as
naive TIMESTAMP) and loads them into DuckDB:

    assurance-harness/data/m01/planted.duckdb
    assurance-harness/data/m01/clean.duckdb
    labs/m01-risk-controls-independence/data/q3_review_snapshot_A.duckdb
    labs/m01-risk-controls-independence/data/q3_review_snapshot_B.duckdb

All four share one schema. The two snapshot databases are the systems of
record behind the Q3 2026 access-review evidence packages in
labs/m01-risk-controls-independence/evidence/q3_access_review/.

Generator contract: see the docstring of scripts/rehydrate.py.

Usage (from the repo root):
    uv run --frozen python assurance-harness/generators/m01_iam.py --rehydrate
    uv run --frozen python assurance-harness/generators/m01_iam.py --rehydrate --force

Maintainer-only flags (rewrite tracked artifacts; not used by rehydrate):
    --update-checksums   rebuild and rewrite checksums/m01_iam.json
    --write-evidence     rewrite the evidence packages
    --write-answer-key   rewrite the lab's sealed answer key

Determinism: one fixed seed (SEED). Every random stream is a random.Random
seeded from a string derived from SEED. Only integer arithmetic and basic
float operations (+ - * /) are used on random draws; no wall-clock time, no
hash(), no set or dict iteration order, no DuckDB random().
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import pathlib
import random
import shutil
import sys
import time
import types
from datetime import datetime, timedelta

import duckdb

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import sealed_m01_plant as plant  # noqa: E402

SEED = 20260930
GENERATOR = "m01_iam"

DATA_DIR = ROOT / "assurance-harness" / "data" / "m01"
LAB_DIR = ROOT / "labs" / "m01-risk-controls-independence"
LAB_DATA_DIR = LAB_DIR / "data"
EVIDENCE_DIR = LAB_DIR / "evidence" / "q3_access_review"
SEALED_KEY = LAB_DIR / ".sealed" / "ANSWER_KEY.md"
CHECKSUMS = HERE / "checksums" / f"{GENERATOR}.json"

DATASETS = {
    "planted": DATA_DIR / "planted.duckdb",
    "clean": DATA_DIR / "clean.duckdb",
    "q3_review_snapshot_A": LAB_DATA_DIR / "q3_review_snapshot_A.duckdb",
    "q3_review_snapshot_B": LAB_DATA_DIR / "q3_review_snapshot_B.duckdb",
}
MAIN_IDENTITIES = 3000

# ---------------------------------------------------------------------------
# Time: integer seconds since EPOCH, formatted only on output.
# ---------------------------------------------------------------------------
EPOCH = datetime(2016, 1, 1)
MINUTE, HOUR, DAY = 60, 3600, 86400


def T(y, m, d, hh=0, mm=0, ss=0) -> int:
    return int((datetime(y, m, d, hh, mm, ss) - EPOCH).total_seconds())


def fmt(s):
    if s is None:
        return None
    return (EPOCH + timedelta(seconds=s)).strftime("%Y-%m-%d %H:%M:%S")


P0 = T(2026, 4, 1)              # observation period start (inclusive)
P1 = T(2026, 10, 1)             # observation period end (exclusive)
TERM_CUTOFF = T(2026, 9, 28)    # last HR termination day in the export
CAMPAIGNS = [                   # (campaign_id, population as-at, window end exclusive)
    ("2026Q2", T(2026, 6, 1), T(2026, 6, 22)),
    ("2026Q3", T(2026, 9, 1), T(2026, 9, 22)),
]
LEGACY_CUTOVER = T(2021, 1, 1)  # records hired before this came from the previous HRIS

# ---------------------------------------------------------------------------
# Schema (identical in every database). Last element: checksum sort key.
# ---------------------------------------------------------------------------
SCHEMA = [
    ("hr_identities", [
        ("hr_id", "VARCHAR"), ("worker_type", "VARCHAR"), ("given_name", "VARCHAR"),
        ("family_name", "VARCHAR"), ("email", "VARCHAR"), ("department", "VARCHAR"),
        ("job_title", "VARCHAR"), ("manager_hr_id", "VARCHAR"), ("hire_ts", "TIMESTAMP"),
        ("termination_ts", "TIMESTAMP"), ("hr_status", "VARCHAR"), ("record_source", "VARCHAR"),
    ], "hr_id"),
    ("iam_accounts", [
        ("account_id", "VARCHAR PRIMARY KEY"), ("username", "VARCHAR"), ("account_type", "VARCHAR"),
        ("realm", "VARCHAR"), ("hr_id", "VARCHAR"), ("owner_hr_id", "VARCHAR"), ("email", "VARCHAR"),
        ("status", "VARCHAR"), ("created_at", "TIMESTAMP"), ("disabled_at", "TIMESTAMP"),
        ("disable_reason", "VARCHAR"), ("provisioning_request_id", "VARCHAR"),
    ], "account_id"),
    ("entitlements", [
        ("entitlement_id", "BIGINT PRIMARY KEY"), ("account_id", "VARCHAR"), ("permission", "VARCHAR"),
        ("granted_at", "TIMESTAMP"), ("granted_by", "VARCHAR"), ("approval_ref", "VARCHAR"),
        ("revoked_at", "TIMESTAMP"), ("revoke_reason", "VARCHAR"),
    ], "entitlement_id"),
    ("access_requests", [
        ("request_id", "VARCHAR PRIMARY KEY"), ("request_type", "VARCHAR"), ("account_id", "VARCHAR"),
        ("subject_hr_id", "VARCHAR"), ("permission", "VARCHAR"), ("requested_by_hr_id", "VARCHAR"),
        ("requested_at", "TIMESTAMP"), ("approver_hr_id", "VARCHAR"), ("status", "VARCHAR"),
        ("decided_at", "TIMESTAMP"), ("expires_at", "TIMESTAMP"), ("justification", "VARCHAR"),
    ], "request_id"),
    ("access_reviews", [
        ("review_id", "VARCHAR PRIMARY KEY"), ("campaign_id", "VARCHAR"), ("account_id", "VARCHAR"),
        ("reviewer_hr_id", "VARCHAR"), ("reviewer_role", "VARCHAR"), ("decision", "VARCHAR"),
        ("revoke_action", "VARCHAR"), ("revoked_permission", "VARCHAR"), ("decided_at", "TIMESTAMP"),
        ("actioned_at", "TIMESTAMP"), ("signed_off_at", "TIMESTAMP"),
    ], "review_id"),
    ("auth_events", [
        ("event_id", "BIGINT PRIMARY KEY"), ("event_ts", "TIMESTAMP"), ("account_id", "VARCHAR"),
        ("auth_method", "VARCHAR"), ("result", "VARCHAR"), ("failure_reason", "VARCHAR"),
        ("source_ip", "VARCHAR"), ("collector", "VARCHAR"),
    ], "event_id"),
]

# ---------------------------------------------------------------------------
# Organisation reference data (all fictional).
# ---------------------------------------------------------------------------
GIVEN = ["Ada", "Bram", "Cleo", "Dario", "Edda", "Femi", "Greta", "Hugo", "Ines", "Joss",
         "Kaito", "Lena", "Mateo", "Nia", "Oren", "Pia", "Quinn", "Rafa", "Sana", "Teo",
         "Uma", "Vik", "Wren", "Xia", "Yusuf", "Zora", "Amara", "Bodhi", "Cyra", "Dex",
         "Elio", "Fern", "Gus", "Hana", "Ivo", "Jun", "Kira", "Lior", "Mira", "Nils",
         "Odile", "Pax", "Rhea", "Soren", "Tova", "Ugo", "Vera", "Wim", "Yara", "Zev",
         "Alba", "Bea", "Cass", "Dani", "Emre", "Faye", "Gil", "Hollis", "Isa", "Jules"]
FAMILY = ["Abernathy", "Bellweather", "Castellan", "Dunmore", "Everly", "Fairbrook", "Galloway",
          "Hartigan", "Ilsley", "Juniper", "Kestrel", "Lindqvist", "Marchetti", "Northcote",
          "Okafor", "Pellegrini", "Quill", "Rosethorn", "Sandoval", "Thistlewood", "Underhill",
          "Vasquez", "Whitlock", "Yardley", "Zeller", "Ashdown", "Brightwater", "Coldwell",
          "Delacroix", "Elsworth", "Foxglove", "Greaves", "Holloway", "Ivanova", "Jessup",
          "Kowalczyk", "Larchmont", "Moreau", "Nakamura", "Oyelaran", "Pemberton", "Ravensworth",
          "Saltmarsh", "Tanaka", "Umberfield", "Vollmer", "Wainwright", "Achterberg", "Bramley",
          "Cardenas", "Draycott", "Esposito", "Featherstone", "Goldberg", "Halvorsen", "Ishikawa",
          "Kingsley", "Lockwood", "Mbeki", "Nightingale", "Ostrander", "Penhallow", "Rutherford",
          "Silverstone", "Trelawney", "Verhoeven", "Westergaard", "Youngblood", "Zamora", "Mistry"]

# name, weight, director dept, titles, P(reporting), P(sandbox), P(admin), owns service accounts
DEPTS = [
    ("Support", 30, "Support", ["Support Agent", "Senior Support Agent", "Support Specialist"], 0.35, 0.02, 0.0, False),
    ("Support Operations", 6, "Support", ["Support Operations Analyst", "Workforce Planner"], 0.7, 0.05, 0.0, True),
    ("Billing", 7, "Finance", ["Billing Specialist", "Billing Analyst"], 0.7, 0.0, 0.0, False),
    ("Customer Success", 9, "Customer Success", ["Customer Success Manager", "Integration Consultant"], 0.6, 0.1, 0.0, True),
    ("Engineering", 17, "Engineering", ["Software Engineer", "Senior Software Engineer", "Staff Engineer"], 0.3, 0.85, 0.0, True),
    ("Platform SRE", 5, "Engineering", ["Site Reliability Engineer", "Senior SRE"], 0.4, 0.9, 0.4, True),
    ("Security", 3, "Security", ["Security Engineer", "Security Analyst"], 0.4, 0.5, 0.45, False),
    ("IT Operations", 3, "IT Operations", ["IT Operations Engineer", "IAM Engineer"], 0.4, 0.2, 0.5, True),
    ("Finance", 4, "Finance", ["Financial Analyst", "Accountant"], 0.8, 0.0, 0.0, False),
    ("Sales", 8, "Sales", ["Account Executive", "Sales Development Rep"], 0.6, 0.0, 0.0, False),
    ("People", 2, "People", ["People Partner", "Recruiter"], 0.3, 0.0, 0.0, False),
    ("Legal", 1, "People", ["Counsel", "Contracts Manager"], 0.3, 0.0, 0.0, False),
    ("Data", 4, "Engineering", ["Data Engineer", "Analytics Engineer"], 0.9, 0.6, 0.0, True),
]
DEPT = {d[0]: d for d in DEPTS}
DIRECTOR_DEPTS = ["Support", "Customer Success", "Engineering", "Finance", "Sales", "IT Operations", "People"]

BASELINE = {
    "console": ["kb.read", "ticket.read"],
    "reporting": ["report.run"],
    "sandbox": ["sandbox.read"],
    "admin": ["tenant.read"],
    "integration": ["api.ticket.read"],
}
CATALOG = {
    "console": ["ticket.write", "ticket.assign", "ticket.merge", "kb.edit", "customer.read",
                "customer.notes", "macro.edit", "csat.view", "customer.export"],
    "reporting": ["report.schedule", "report.export", "billing.read", "dashboard.edit"],
    "sandbox": ["sandbox.deploy", "feature.flag.edit", "sandbox.logs"],
    "admin": ["auditlog.read", "integration.manage", "user.unlock"],
    "integration": ["api.ticket.write", "api.customer.read", "api.webhook.manage", "api.export",
                    "api.kb.read", "api.attachment.read"],
}
ADD_RANGE = {"console": (3, 6), "reporting": (0, 2), "sandbox": (0, 2), "admin": (1, 2), "integration": (1, 3)}
RESTRICTED = ["auditlog.admin", "iam.admin", "refund.approve", "refund.issue", "tenant.config"]
PRIVILEGED = ["auditlog.admin", "iam.admin", "tenant.config"]
TOXIC_PAIRS = [("refund.issue", "refund.approve"), ("iam.admin", "auditlog.admin")]
SERVICE_PURPOSES = ["int", "int", "int", "etl", "webhook", "mailer", "bot", "sync"]
EVENT_RATE = {"console": 0.12, "reporting": 0.03, "sandbox": 0.03, "admin": 0.06, "integration": 0.052}
JUSTIFICATIONS = ["Required for role", "Covering queue for team", "New responsibilities",
                  "Project access", "Integration onboarding", "Customer escalation support",
                  "Quarterly reporting", "Backfill for colleague on leave"]


def weighted_index(r: random.Random, weights) -> int:
    total = sum(weights)
    x = r.randrange(total)
    acc = 0
    for i, w in enumerate(weights):
        acc += w
        if x < acc:
            return i
    return len(weights) - 1


class Profile:
    """Default profile: the build hooks do nothing."""

    def after_provisioning(self, world):
        pass

    def population(self, world, campaign_id, accounts):
        return accounts

    def finalize(self, world):
        pass


CONSTANTS = types.SimpleNamespace(
    SEED=SEED, P0=P0, P1=P1, MINUTE=MINUTE, HOUR=HOUR, DAY=DAY, T=T, fmt=fmt,
    CAMPAIGNS=CAMPAIGNS, PRIVILEGED=PRIVILEGED, TOXIC_PAIRS=TOXIC_PAIRS,
)


# ---------------------------------------------------------------------------
# World builder
# ---------------------------------------------------------------------------
class World:
    def __init__(self, label: str, n_identities: int, profile: Profile | None = None):
        self.label = label
        self.N = n_identities
        self.profile = profile or Profile()
        self.k = CONSTANTS
        self.R = random.Random(f"{SEED}|{label}|base")
        self.identities: list[dict] = []
        self.by_canon: dict[str, dict] = {}
        self.accounts: list[dict] = []
        self.acct_by_id: dict[str, dict] = {}
        self.requests: list[dict] = []
        self.entitlements: list[dict] = []
        self.reviews: list[dict] = []
        self.events: list[dict] = []
        self.excluded: list[str] = []
        self.extended: list[str] = []
        self.special: dict[str, list[str]] = {}
        self.manifest: dict = {}

    # -- helpers ----------------------------------------------------------
    def sub_rng(self, *parts) -> random.Random:
        return random.Random("|".join([str(SEED), self.label] + [str(p) for p in parts]))

    def review_rng(self, campaign_id: str, account_id: str) -> random.Random:
        return self.sub_rng("review", campaign_id, account_id)

    def ents_of(self, account_id: str) -> list[dict]:
        return self._ents_by_acct.get(account_id, [])

    def accounts_of(self, canon: str) -> list[dict]:
        return sorted((a for a in self.accounts if a["hr"] == canon), key=lambda a: a["id"])

    def reviewer_for(self, a: dict) -> tuple[str, str]:
        if a["type"] == "human":
            return self.by_canon[a["hr"]]["manager"], "line_manager"
        return a["owner"], "service_owner"

    def approver_for(self, a: dict) -> str:
        if a["type"] == "human":
            return self.by_canon[a["hr"]]["manager"]
        return self.by_canon[a["owner"]]["manager"]

    # -- build ------------------------------------------------------------
    def build(self) -> "World":
        self._identities()
        self._accounts()
        self._provisioning()
        self._assign_request_and_entitlement_ids()
        self.profile.after_provisioning(self)
        self._reviews()
        self._events()
        self.profile.finalize(self)
        return self

    def _identities(self):
        R, N = self.R, self.N
        nums = R.sample(range(10000, 100000), N)
        n_dir = len(DIRECTOR_DEPTS)
        n_mgr = max(len(DEPTS) * 2, N // 12)
        names_seen: dict[str, int] = {}
        directors: dict[str, str] = {}
        managers_by_dept: dict[str, list[str]] = {d[0]: [] for d in DEPTS}
        weights = [d[1] for d in DEPTS]
        for i in range(N):
            if i < 3:
                role = "exec"
                dept = ["Executive", "Executive", "Security"][i]
                title = ["Chief Executive Officer", "Chief Operating Officer", "Head of Security"][i]
            elif i < 3 + n_dir:
                role = "director"
                dept = DIRECTOR_DEPTS[i - 3]
                title = f"Director, {dept}"
            elif i < 3 + n_dir + n_mgr:
                role = "manager"
                j = i - 3 - n_dir
                dept = DEPTS[j][0] if j < len(DEPTS) else DEPTS[weighted_index(R, weights)][0]
                title = f"{dept} Manager"
            else:
                role = "staff"
                dept = DEPTS[weighted_index(R, weights)][0]
                title = None
            if role == "staff":
                title = R.choice(DEPT[dept][3])
                contractor = R.random() < 0.22
            else:
                contractor = False
            prefix = "C" if contractor else "E"
            num = nums[i]
            canon = f"{prefix}{num:06d}"
            given, family = R.choice(GIVEN), R.choice(FAMILY)
            local = f"{given}.{family}".lower()
            names_seen[local] = names_seen.get(local, 0) + 1
            if names_seen[local] > 1:
                local = f"{local}{names_seen[local]}"
            email = f"{local}@{'contractors.example.org' if contractor else 'example.com'}"
            # hire
            if role != "staff":
                hire = T(2016, 1, 4) + R.randrange(0, 300) * DAY + 9 * HOUR
            else:
                r1, r2, r3, r4 = R.random(), R.random(), R.random(), R.random()
                frac = max(r1, r2) if r3 < 0.7 else r4
                start, end = T(2017, 1, 2), T(2026, 9, 14)
                hire = start + int(frac * ((end - start) // DAY)) * DAY + 9 * HOUR
            # termination (staff only)
            a, b, c, d, hh = R.random(), R.random(), R.random(), R.random(), R.randrange(0, 9 * HOUR)
            term = None
            if role == "staff":
                if hire < P0 - 60 * DAY and a < (0.22 if contractor else 0.09):
                    lo = hire + 30 * DAY
                    span_days = (P0 - DAY - lo) // DAY
                    if span_days > 0:
                        term = lo - (lo % DAY) + int(b * span_days) * DAY + 9 * HOUR + hh
                elif hire < TERM_CUTOFF - 14 * DAY and c < (0.17 if contractor else 0.07):
                    lo = max(hire + 14 * DAY, P0)
                    lo = lo - (lo % DAY)
                    span_days = (TERM_CUTOFF - lo) // DAY
                    if span_days > 0:
                        term = lo + int(d * span_days) * DAY + 9 * HOUR + hh
            # identifier as it appears in the HR export
            e, variant = R.random(), R.randrange(4)
            legacy = role in ("manager", "staff") and hire < LEGACY_CUTOVER and e < 0.13
            if legacy:
                raw = [f"{prefix}-{num:06d}", f"{prefix.lower()}{num:06d}", f"{prefix}{num}", f"{num:06d}"][variant]
            else:
                raw = canon
            ident = {
                "idx": i, "canon": canon, "raw": raw, "num": num, "role": role, "dept": dept,
                "title": title, "contractor": contractor, "given": given, "family": family,
                "email": email, "hire": hire, "term": term, "legacy": legacy, "manager": None,
                "owns_services": False,
            }
            self.identities.append(ident)
            self.by_canon[canon] = ident
            if role == "director":
                directors[dept] = canon
            if role == "manager":
                managers_by_dept[dept].append(canon)
        ceo, coo, hos = (self.identities[i]["canon"] for i in range(3))
        self.ceo, self.coo, self.hos = ceo, coo, hos
        directors["Security"] = hos
        for ident in self.identities:
            role, dept = ident["role"], ident["dept"]
            if ident["canon"] == ceo:
                ident["manager"] = coo
            elif ident["canon"] in (coo, hos):
                ident["manager"] = ceo
            elif role == "director":
                ident["manager"] = ceo if dept in ("Engineering", "Finance", "Sales") else coo
            elif role == "manager":
                ident["manager"] = directors[DEPT[dept][2]]
            else:
                ident["manager"] = R.choice(managers_by_dept[dept])

        # special roles (named privileged holders and separation-of-duties exception holders)
        def eligible(dept):
            return sorted(
                (x["canon"] for x in self.identities
                 if x["dept"] == dept and x["role"] in ("staff", "manager") and x["term"] is None
                 and not x["legacy"] and x["hire"] < T(2024, 1, 1)),
            )
        sp = {}
        sp["iam.admin"] = R.sample(eligible("IT Operations"), 7)
        sp["auditlog.admin"] = R.sample(eligible("Security"), 5)
        sp["tenant.config"] = R.sample(eligible("Platform SRE"), 9)
        billing_approvers = R.sample(eligible("Billing"), 8)
        sp["refund.approve"] = sorted(billing_approvers + R.sample(eligible("Finance"), 6))
        sp["dual_iam_audit"] = sorted(sp["auditlog.admin"])[:2]
        sp["dual_refund"] = sorted(R.sample(sorted(billing_approvers), 6))
        for key in ("iam.admin", "auditlog.admin", "tenant.config"):
            sp[key] = sorted(sp[key])
        self.special = sp
        self.special_ids = sorted(set(sp["iam.admin"] + sp["auditlog.admin"] + sp["tenant.config"]
                                      + sp["refund.approve"]))

        # service-account owners
        owner_cands = sorted(x["canon"] for x in self.identities
                             if x["role"] in ("staff", "manager") and x["term"] is None
                             and DEPT[x["dept"]][7] and x["hire"] < T(2025, 1, 1))
        self.service_owners = sorted(R.sample(owner_cands, max(40, int(len(owner_cands) * 0.4))))
        for c in self.service_owners:
            self.by_canon[c]["owns_services"] = True

    def _accounts(self, decom_rate: float = 0.06):
        R = self.R
        user_seen: dict[str, int] = {}
        specials = self.special_ids
        for ident in self.identities:
            dept = DEPT.get(ident["dept"])
            p_rep = dept[4] if dept else 0.9
            p_sbx = dept[5] if dept else 0.0
            p_adm = dept[6] if dept else 0.0
            if ident["role"] in ("manager", "director", "exec"):
                p_rep = 0.85
            x_rep, x_sbx, x_adm = R.random(), R.random(), R.random()
            realms = ["console"]
            if x_rep < p_rep:
                realms.append("reporting")
            if x_sbx < p_sbx:
                realms.append("sandbox")
            is_special = ident["canon"] in specials
            if x_adm < p_adm or is_special:
                realms.append("admin")
            base = "".join(ch for ch in (ident["given"][0] + ident["family"]).lower() if ch.isalnum())
            user_seen[base] = user_seen.get(base, 0) + 1
            if user_seen[base] > 1:
                base = f"{base}{user_seen[base]}"
            end_limit = (ident["term"] if ident["term"] is not None else P1) - 2 * DAY
            for realm in realms:
                if realm == "console":
                    created = ident["hire"] + R.randrange(0, 2 * DAY)
                else:
                    lo = ident["hire"] + DAY
                    hi = end_limit
                    if realm == "admin" and is_special:
                        hi = min(hi, T(2025, 6, 1))
                    created = lo + R.randrange(max(HOUR, hi - lo))
                suffix = {"console": "", "reporting": ".rpt", "sandbox": ".sbx", "admin": ".adm"}[realm]
                self.accounts.append({
                    "id": None, "username": base + suffix, "type": "human", "realm": realm,
                    "hr": ident["canon"], "owner": ident["canon"], "email": ident["email"],
                    "created": created, "disabled": None, "reason": None, "prov_req": None,
                })
        n_service = int(self.N * 2.2)
        for k in range(n_service):
            owner = R.choice(self.service_owners)
            purpose = R.choice(SERVICE_PURPOSES)
            r1, r2, x, y = R.random(), R.random(), R.random(), R.random()
            lo = max(self.by_canon[owner]["hire"] + 30 * DAY, T(2018, 1, 1))
            hi = P1 - 3 * DAY
            created = lo + int(max(r1, r2) * (hi - lo))
            disabled = None
            if x < decom_rate:
                lo2 = created + 30 * DAY
                hi2 = P1 - DAY
                if hi2 > lo2:
                    disabled = lo2 + int(y * (hi2 - lo2))
            username = f"svc-{purpose}-{k + 1:05d}"
            self.accounts.append({
                "id": None, "username": username, "type": "service", "realm": "integration",
                "hr": None, "owner": owner, "email": f"{username}@svc.example.net",
                "created": created, "disabled": disabled,
                "reason": "decommissioned" if disabled is not None else None, "prov_req": None,
            })
        ids = R.sample(range(100000, 1000000), len(self.accounts))
        for a, n in zip(self.accounts, ids):
            a["id"] = f"LDA{n}"
            self.acct_by_id[a["id"]] = a
        # deprovisioning on HR termination
        for ident in self.identities:
            if ident["term"] is None:
                continue
            rr = self.sub_rng("deprov", ident["canon"])
            lag = HOUR // 4 + int(rr.random() * (19.75 * HOUR))
            ident["deprov_lag"] = lag
            for a in self.accounts_of(ident["canon"]):
                a["disabled"] = ident["term"] + lag + rr.randrange(0, 1800)
                a["reason"] = "hr_termination"

    def _new_request(self, rtype, a, subject, permission, requested_by, requested, approver,
                     status, decided, expires=None, justification=None):
        req = {"id": None, "type": rtype, "acct": a["id"], "subject": subject, "perm": permission,
               "by": requested_by, "requested": requested, "approver": approver, "status": status,
               "decided": decided, "expires": expires, "just": justification,
               "seq": len(self.requests)}
        self.requests.append(req)
        return req

    def _grant(self, a, perm, granted, req, granted_by="svc-provisioner"):
        e = {"id": None, "acct": a["id"], "perm": perm, "granted": granted, "by": granted_by,
             "req": req, "revoked": None, "revoke_reason": None}
        self.entitlements.append(e)
        return e

    def _account_end(self, a) -> int:
        end = a["disabled"] if a["disabled"] is not None else P1
        if a["type"] == "human":
            t = self.by_canon[a["hr"]]["term"]
            if t is not None:
                end = min(end, t)
        return end

    def _provisioning(self):
        R = self.R
        sp = self.special
        refund_ok_depts = ("Support", "Billing")
        for a in self.accounts:
            subject = a["hr"] if a["type"] == "human" else None
            requester = a["hr"] if a["type"] == "human" else a["owner"]
            approver = self.approver_for(a)
            decided = a["created"] - (10 * MINUTE + R.randrange(DAY))
            requested = decided - (10 * MINUTE + R.randrange(3 * DAY))
            req = self._new_request("new_account", a, subject or a["owner"], None, requester,
                                    requested, approver, "approved", decided,
                                    justification="Joiner provisioning" if a["type"] == "human"
                                    else "Integration onboarding")
            a["prov_req"] = req
            for perm in BASELINE[a["realm"]]:
                self._grant(a, perm, a["created"] + R.randrange(0, 30 * MINUTE), req)
            lo_k, hi_k = ADD_RANGE[a["realm"]]
            k = lo_k + R.randrange(hi_k - lo_k + 1)
            catalog = list(CATALOG[a["realm"]])
            owner_ident = self.by_canon[a["owner"]]
            if (a["realm"] == "console" and owner_ident["dept"] in refund_ok_depts
                    and a["owner"] not in sp["refund.approve"]):
                catalog.append("refund.issue")
            perms = R.sample(catalog, min(k, len(catalog)))
            lo = a["created"] + 4 * DAY
            hi = self._account_end(a) - DAY
            for perm in perms:
                g0, d0, q0, j = R.random(), R.randrange(MINUTE, 8 * HOUR), R.randrange(10 * MINUTE, 3 * DAY), R.randrange(len(JUSTIFICATIONS))
                if hi <= lo:
                    continue
                granted = lo + int(g0 * (hi - lo))
                decided = granted - d0
                requested = decided - q0
                req = self._new_request("add_permission", a, subject or a["owner"], perm, requester,
                                        requested, approver, "approved", decided,
                                        justification=JUSTIFICATIONS[j])
                self._grant(a, perm, granted, req)

        # restricted and privileged grants for named holders
        def admin_acct(canon):
            return next(x for x in self.accounts_of(canon) if x["realm"] == "admin")

        def console_acct(canon):
            return next(x for x in self.accounts_of(canon) if x["realm"] == "console")

        def restricted_grant(a, perm):
            lo = a["created"] + 4 * DAY
            hi = T(2026, 2, 1)
            granted = lo + R.randrange(max(DAY, hi - lo))
            decided = granted - R.randrange(HOUR, 8 * HOUR)
            requested = decided - R.randrange(HOUR, 2 * DAY)
            subject = a["hr"]
            req = self._new_request("add_permission", a, subject, perm, subject, requested,
                                    self.approver_for(a), "approved", decided,
                                    justification="Role-based privileged access")
            self._grant(a, perm, granted, req)

        holders = []
        for perm in ("iam.admin", "auditlog.admin", "tenant.config", "refund.approve"):
            for canon in sp[perm]:
                holders.append((perm, canon))
        for canon in sp["dual_iam_audit"]:
            holders.append(("iam.admin", canon))
        for perm, canon in holders:
            restricted_grant(admin_acct(canon), perm)
        for canon in sp["dual_refund"]:
            restricted_grant(console_acct(canon), "refund.issue")
        # privileged-role nominations (annual)
        for perm, canon in holders:
            if perm not in PRIVILEGED:
                continue
            a = admin_acct(canon)
            requested = T(2026, 3, 2) + R.randrange(0, 10 * DAY)
            decided = requested + R.randrange(HOUR, 3 * DAY)
            self._new_request("privileged_nomination", a, canon, perm,
                              self.by_canon[canon]["manager"], requested, self.hos, "approved",
                              decided, expires=T(2027, 3, 31, 23, 59, 59),
                              justification="Named owner for privileged role")
        # separation-of-duties exceptions
        for pair, group in (("refund.issue+refund.approve", "dual_refund"),
                            ("iam.admin+auditlog.admin", "dual_iam_audit")):
            for canon in sp[group]:
                a = admin_acct(canon)
                requested = T(2026, 1, 5) + R.randrange(0, 70 * DAY)
                decided = requested + R.randrange(HOUR, 4 * DAY)
                self._new_request("sod_exception", a, canon, pair, self.by_canon[canon]["manager"],
                                  requested, self.hos, "approved", decided,
                                  expires=T(2026, 12, 31, 23, 59, 59),
                                  justification="Small team; compensating review by Finance controller"
                                  if group == "dual_refund" else "On-call coverage; compensating log review")
        # rejected and pending requests
        n_acc = len(self.accounts)
        for _ in range(int(self.N * 0.4)):
            a = self.accounts[R.randrange(n_acc)]
            perm = R.choice(CATALOG[a["realm"]])
            u, d0 = R.random(), R.randrange(HOUR, 3 * DAY)
            lo, hi = a["created"] + DAY, self._account_end(a) - 4 * DAY
            if hi <= lo:
                continue
            requested = lo + int(u * (hi - lo))
            requester = a["hr"] if a["type"] == "human" else a["owner"]
            self._new_request("add_permission", a, requester, perm, requester, requested,
                              self.approver_for(a), "rejected", requested + d0,
                              justification=JUSTIFICATIONS[R.randrange(len(JUSTIFICATIONS))])
        for _ in range(int(self.N * 0.1)):
            a = self.accounts[R.randrange(n_acc)]
            perm = R.choice(CATALOG[a["realm"]])
            offs = R.randrange(2 * HOUR, 6 * DAY)
            if a["disabled"] is not None or self._account_end(a) < P1:
                continue
            requester = a["hr"] if a["type"] == "human" else a["owner"]
            self._new_request("add_permission", a, requester, perm, requester, P1 - offs,
                              self.approver_for(a), "pending", None,
                              justification=JUSTIFICATIONS[R.randrange(len(JUSTIFICATIONS))])
        # accounts whose quarterly decision may be a revocation
        named = set(self.special_ids)
        for a in self.accounts:
            o = self.by_canon[a["owner"]]
            a["rv"] = (not o["legacy"] and o["term"] is None and a["owner"] not in named)

    def _assign_request_and_entitlement_ids(self):
        reqs = sorted(self.requests, key=lambda r: (r["requested"], r["acct"], r["type"], r["perm"] or "", r["seq"]))
        for i, r in enumerate(reqs, 1):
            r["id"] = f"REQ{i:07d}"
        self.requests = reqs
        for a in self.accounts:
            a["prov_req_id"] = a["prov_req"]["id"]
        ents = sorted(self.entitlements, key=lambda e: (e["granted"], e["acct"], e["perm"]))
        for i, e in enumerate(ents, 1):
            e["id"] = 400000 + i
        self.entitlements = ents
        self._ents_by_acct: dict[str, list[dict]] = {}
        for e in ents:
            self._ents_by_acct.setdefault(e["acct"], []).append(e)

    def _reviews(self):
        excluded = set(self.excluded)
        extended = set(self.extended)
        rows = []
        for cid, snap, wend in CAMPAIGNS:
            pop = [a for a in self.accounts if a["id"] not in excluded and a["created"] < snap
                   and (a["disabled"] is None or a["disabled"] >= snap)]
            pop = self.profile.population(self, cid, pop)
            pop = sorted(pop, key=lambda a: a["id"])
            sessions: dict[str, int] = {}
            last: dict[str, int] = {}
            camp = []
            for n, a in enumerate(pop, 1):
                reviewer, role = self.reviewer_for(a)
                if reviewer not in sessions:
                    rr = self.sub_rng("session", cid, reviewer)
                    sessions[reviewer] = snap + rr.randrange(0, 17) * DAY + 8 * HOUR + rr.randrange(0, 8 * HOUR)
                r = self.review_rng(cid, a["id"])
                u, off, act, pick = r.random(), r.randrange(0, 3 * HOUR), r.randrange(2 * HOUR, 6 * DAY + 12 * HOUR), r.random()
                decided = sessions[reviewer] + off
                decision, action, perm, actioned = "certify", None, None, None
                if a["rv"] and u < 0.03:
                    if a["realm"] in ("reporting", "sandbox", "integration") and pick < 0.5:
                        action = "disable_account"
                    else:
                        removable = sorted(
                            (e for e in self.ents_of(a["id"])
                             if e["perm"] not in BASELINE[a["realm"]] and e["perm"] not in RESTRICTED
                             and e["granted"] < decided and e["revoked"] is None),
                            key=lambda e: e["perm"])
                        if removable:
                            action = "remove_entitlement"
                            ent = removable[r.randrange(len(removable))]
                            perm = ent["perm"]
                        elif a["realm"] != "console":
                            action = "disable_account"
                    if action is not None:
                        decision = "revoke"
                        actioned = decided + act
                        if action == "disable_account":
                            a["disabled"] = actioned
                            a["reason"] = "access_review"
                        else:
                            ent["revoked"] = actioned
                            ent["revoke_reason"] = "access_review"
                holder = self.by_canon[a["hr"]] if a["type"] == "human" else None
                if (holder is not None and holder["term"] is not None and decided >= holder["term"]
                        and a["hr"] not in extended):
                    decision, action, perm = "revoke", "disable_account", None
                    actioned = decided + 10 * MINUTE + act % (4 * HOUR)
                    if a["disabled"] is None or a["disabled"] > actioned:
                        a["disabled"] = actioned
                        a["reason"] = "access_review"
                last[reviewer] = max(last.get(reviewer, 0), decided)
                camp.append({"id": f"RV-{cid}-{n:06d}", "cid": cid, "acct": a["id"], "reviewer": reviewer,
                             "role": role, "decision": decision, "action": action, "perm": perm,
                             "decided": decided, "actioned": actioned})
            signoff = {rv: t + self.sub_rng("signoff", cid, rv).randrange(5 * MINUTE, 2 * HOUR)
                       for rv, t in sorted(last.items())}
            for row in camp:
                row["signed"] = signoff[row["reviewer"]]
            rows.extend(camp)
        self.reviews = rows

    def _events(self):
        extended = set(self.extended)
        out = []
        for a in sorted(self.accounts, key=lambda a: a["id"]):
            start = max(a["created"], P0)
            end = min(a["disabled"] if a["disabled"] is not None else P1, P1)
            if a["type"] == "human":
                t = self.by_canon[a["hr"]]["term"]
                if t is not None and a["hr"] not in extended:
                    end = min(end, t)
            if end <= start:
                continue
            r = self.sub_rng("auth", a["id"])
            days = (end - start) / DAY
            n = max(1, int(days * EVENT_RATE[a["realm"]] * (0.4 + 1.2 * r.random()) + 0.5))
            remote = r.random() < 0.4
            for i in range(n):
                ts = start + r.randrange(end - start)
                x, y, z = r.random(), r.random(), r.randrange(1, 255)
                if a["type"] == "service":
                    method, collector, ip = "api_token", "api-gw-1", f"192.0.2.{z}"
                    fail = x < 0.03
                    reason = ("token_expired" if y < 0.6 else "rate_limited") if fail else None
                else:
                    method = "sso" if (a["realm"] != "sandbox" or y < 0.7) else "password"
                    collector = "sso-gw-eu1" if y < 0.45 else "sso-gw-us1"
                    ip = f"203.0.113.{z}" if remote and y < 0.8 else f"198.51.100.{z}"
                    fail = x < 0.045
                    reason = ("bad_password" if y < 0.7 else "mfa_timeout") if fail else None
                out.append((ts, a["id"], i, method, "failure" if fail else "success", reason, ip, collector))
        out.sort(key=lambda e: (e[0], e[1], e[2]))
        self.events = [{"id": 7000001 + n, "ts": e[0], "acct": e[1], "method": e[3], "result": e[4],
                        "reason": e[5], "ip": e[6], "collector": e[7]} for n, e in enumerate(out)]

    # -- table rows -------------------------------------------------------
    def table_rows(self):
        excluded = set(self.excluded)
        t = {}
        t["hr_identities"] = sorted(
            ((i["raw"], "contractor" if i["contractor"] else "employee", i["given"], i["family"], i["email"],
              i["dept"], i["title"], i["manager"], fmt(i["hire"]), fmt(i["term"]),
              "terminated" if i["term"] is not None else "active",
              "hris_legacy_import" if i["legacy"] else "hris")
             for i in self.identities), key=lambda r: r[0])
        t["iam_accounts"] = sorted(
            ((a["id"], a["username"], a["type"], a["realm"], a["hr"], a["owner"], a["email"],
              "disabled" if a["disabled"] is not None else "active", fmt(a["created"]),
              fmt(a["disabled"]), a["reason"], a["prov_req_id"])
             for a in self.accounts if a["id"] not in excluded), key=lambda r: r[0])
        t["entitlements"] = [
            (e["id"], e["acct"], e["perm"], fmt(e["granted"]), e["by"],
             e["req"]["id"] if e["req"] is not None else None, fmt(e["revoked"]), e["revoke_reason"])
            for e in self.entitlements]
        t["access_requests"] = [
            (r["id"], r["type"], r["acct"], r["subject"], r["perm"], r["by"], fmt(r["requested"]),
             r["approver"], r["status"], fmt(r["decided"]), fmt(r["expires"]), r["just"])
            for r in self.requests]
        t["access_reviews"] = [
            (v["id"], v["cid"], v["acct"], v["reviewer"], v["role"], v["decision"], v["action"], v["perm"],
             fmt(v["decided"]), fmt(v["actioned"]), fmt(v["signed"]))
            for v in self.reviews]
        t["auth_events"] = [
            (e["id"], fmt(e["ts"]), e["acct"], e["method"], e["result"], e["reason"], e["ip"], e["collector"])
            for e in self.events]
        return t


def make_world(label: str, n_identities: int, profile: Profile | None = None) -> World:
    return World(label, n_identities, profile).build()


def build_worlds(names) -> dict[str, World]:
    """Build the in-memory worlds for the requested dataset names."""
    out: dict[str, World] = {}
    if "clean" in names:
        out["clean"] = make_world("main", MAIN_IDENTITIES)
    if "planted" in names:
        out["planted"] = make_world("main", MAIN_IDENTITIES, plant.main_profile(Profile))
    if any(n.startswith("q3_review_snapshot_") for n in names):
        pair, _ = plant.build_pair(make_world, Profile, MAIN_IDENTITIES, SEED)
        for letter in ("A", "B"):
            out[f"q3_review_snapshot_{letter}"] = pair[letter]
    return out


# ---------------------------------------------------------------------------
# DuckDB load and content checksums
# ---------------------------------------------------------------------------
def write_db(world: World, path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = path.parent / f"_build_{path.stem}"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)
    tmp_db = path.parent / f"_build_{path.name}"
    if tmp_db.exists():
        tmp_db.unlink()
    rows = world.table_rows()
    con = duckdb.connect(str(tmp_db))
    try:
        for table, cols, _key in SCHEMA:
            csv_path = tmp_dir / f"{table}.csv"
            with open(csv_path, "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh, lineterminator="\n")
                w.writerow([c for c, _ in cols])
                for r in rows[table]:
                    w.writerow(["" if v is None else v for v in r])
            con.execute(f"CREATE TABLE {table} ({', '.join(f'{c} {ty}' for c, ty in cols)})")
            con.execute(f"COPY {table} FROM '{csv_path.as_posix()}' "
                        "(FORMAT csv, HEADER true, NULLSTR '', DELIMITER ',', QUOTE '\"')")
        con.execute("CHECKPOINT")
    finally:
        con.close()
    shutil.rmtree(tmp_dir)
    os.replace(tmp_db, path)


def content_checksums(path: pathlib.Path) -> dict:
    con = duckdb.connect(str(path), read_only=True)
    try:
        out = {}
        for table, cols, key in SCHEMA:
            parts = ", ".join(f"coalesce(CAST({c} AS VARCHAR), '\\N')" for c, _ in cols)
            (digest,) = con.execute(
                f"SELECT sha256(coalesce(string_agg(concat_ws('|', {parts}), chr(10) ORDER BY {key}), '')) "
                f"FROM {table}").fetchone()
            out[table] = digest
        return out
    finally:
        con.close()


def file_sha256(p: pathlib.Path) -> str:
    data = p.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def evidence_hashes() -> dict:
    if not EVIDENCE_DIR.is_dir():
        return {}
    return {f.relative_to(ROOT).as_posix(): file_sha256(f)
            for f in sorted(EVIDENCE_DIR.rglob("*")) if f.is_file()}


def load_checksums() -> dict | None:
    if not CHECKSUMS.is_file():
        return None
    return json.loads(CHECKSUMS.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Evidence package (Q3 2026 user access review), as handed to an assessor
# ---------------------------------------------------------------------------
def write_evidence_package(world: World, letter: str) -> None:
    out = EVIDENCE_DIR / f"package_{letter}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    cid, snap, wend = CAMPAIGNS[1]
    rows = sorted((v for v in world.reviews if v["cid"] == cid), key=lambda v: v["acct"])
    accts = world.acct_by_id
    with open(out / "review_decisions.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["review_id", "account_id", "username", "account_type", "realm", "reviewer_hr_id",
                    "reviewer_role", "decision", "decided_at"])
        for v in rows:
            a = accts[v["acct"]]
            w.writerow([v["id"], v["acct"], a["username"], a["type"], a["realm"], v["reviewer"],
                        v["role"], v["decision"], fmt(v["decided"])])
    revs = [v for v in rows if v["decision"] == "revoke"]
    with open(out / "revocations.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["review_id", "account_id", "revoke_action", "permission", "decided_at", "actioned_at",
                    "change_ticket", "days_to_action"])
        for v in sorted(revs, key=lambda v: v["id"]):
            ticket = f"CHG{int(v['id'].rsplit('-', 1)[1]) + 310000:07d}"
            days = (v["actioned"] - v["decided"]) / DAY
            w.writerow([v["id"], v["acct"], v["action"], v["perm"] or "", fmt(v["decided"]),
                        fmt(v["actioned"]), ticket, f"{days:.1f}"])
    per: dict[str, list[dict]] = {}
    for v in rows:
        per.setdefault(v["reviewer"], []).append(v)
    with open(out / "reviewer_signoffs.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["reviewer_hr_id", "reviewer_name", "accounts_assigned", "accounts_completed", "signed_off_at"])
        for rv in sorted(per):
            ident = world.by_canon[rv]
            items = per[rv]
            w.writerow([rv, f"{ident['given']} {ident['family']}", len(items), len(items), fmt(items[0]["signed"])])
    n = len(rows)
    n_rev = len(revs)
    max_days = max(((v["actioned"] - v["decided"]) / DAY for v in revs), default=0.0)
    first_dec = min(v["decided"] for v in rows)
    last_dec = max(v["decided"] for v in rows)
    last_sign = max(v["signed"] for v in rows)
    summary = {
        "campaign_id": f"UAR-{cid}",
        "system": "Larkspur Desk identity and access layer",
        "population_as_at": fmt(snap),
        "review_window": {"opens": fmt(snap), "closes": fmt(wend - 1)},
        "accounts_in_scope": n,
        "accounts_human": sum(1 for v in rows if accts[v["acct"]]["type"] == "human"),
        "accounts_service": sum(1 for v in rows if accts[v["acct"]]["type"] == "service"),
        "decisions_recorded": n,
        "completion_rate": "100.0%",
        "certified": n - n_rev,
        "revoked": n_rev,
        "revocations_actioned": n_rev,
        "revocations_actioned_within_7_days": sum(1 for v in revs if v["actioned"] - v["decided"] <= 7 * DAY),
        "max_days_to_action": round(max_days, 1),
        "reviewers": len(per),
        "reviewers_signed_off": len(per),
        "first_decision_at": fmt(first_dec),
        "last_decision_at": fmt(last_dec),
        "last_sign_off_at": fmt(last_sign),
    }
    (out / "completion_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    readme = f"""# Q3 2026 User Access Review: evidence package {letter}

**Control:** LD-AC-03, quarterly certification of every active account (human and service) by its owner; revocations actioned within 7 days.
**Control owner:** IAM Operations Lead, IT Operations.
**Campaign:** UAR-{cid}. Population as at {fmt(snap)} UTC. Review window {fmt(snap)} to {fmt(wend - 1)} UTC.
**Prepared by:** IAM Operations, for the Q3 2026 control assessment.

## Headline

| Measure | Result |
|---|---|
| Accounts in scope (active in IAM at the population date) | {n:,} |
| Human / service | {summary['accounts_human']:,} / {summary['accounts_service']:,} |
| Decisions recorded | {n:,} ({summary['completion_rate']}) |
| Certified | {n - n_rev:,} |
| Revoked | {n_rev:,} |
| Revocations actioned within 7 days | {summary['revocations_actioned_within_7_days']:,} of {n_rev:,} (max {summary['max_days_to_action']} days) |
| Reviewers / signed off | {len(per):,} / {len(per):,} |
| Decisions made | {fmt(first_dec)} to {fmt(last_dec)} UTC |
| Last reviewer sign-off | {fmt(last_sign)} UTC |

## Contents

| File | What it is |
|---|---|
| `review_decisions.csv` | One row per account on the review list: the reviewer of record, their role, the decision and when it was made. |
| `revocations.csv` | Every revoke decision with the change ticket and the time it was actioned in IAM. |
| `reviewer_signoffs.csv` | Each reviewer's assignment count, completion count and sign-off time. |
| `completion_summary.json` | The figures in the table above, as produced by the campaign tool. |
| `control_owner_attestation.md` | The control owner's attestation for the campaign. |

## How the review list is produced

The review list is the IAM extract of active accounts taken at the population date, routed to the
line manager (human accounts) or the named service owner (service accounts). Reviewers record their
decision in the campaign tool and sign off when their queue is empty. Revoke decisions raise a change
ticket that IAM Operations actions in the identity system.

The identity tables this campaign ran against are available read-only as
`labs/m01-risk-controls-independence/data/q3_review_snapshot_{letter}.duckdb`.
"""
    (out / "README.md").write_text(readme, encoding="utf-8")
    attestation = f"""# Control owner attestation: UAR-{cid}

I attest that the Q3 2026 user access review for Larkspur Desk was completed in line with control
LD-AC-03:

- every account on the review list was certified or revoked by its reviewer of record
  ({n:,} of {n:,}, 100.0%);
- all {len(per):,} reviewers signed off inside the review window, the last at {fmt(last_sign)} UTC;
- all {n_rev:,} revocations were actioned in the identity system within 7 days of the decision.

No exceptions were noted.

Signed: IAM Operations Lead, IT Operations
Date: {fmt(wend + 2 * DAY)[:10]}
"""
    (out / "control_owner_attestation.md").write_text(attestation, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def verify_dataset(name: str, expected: dict) -> list[str]:
    got = content_checksums(DATASETS[name])
    problems = []
    for table, _c, _k in SCHEMA:
        e, g = expected.get(table), got.get(table)
        if e != g:
            problems.append(f"{name}.{table}: content hash does not match")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rehydrate", action="store_true", help="build missing datasets and verify all of them")
    ap.add_argument("--force", action="store_true", help="rebuild every dataset even if present")
    ap.add_argument("--update-checksums", action="store_true", help="maintainer: rewrite checksums file")
    ap.add_argument("--write-evidence", action="store_true", help="maintainer: rewrite evidence packages")
    ap.add_argument("--write-answer-key", action="store_true", help="maintainer: rewrite the sealed answer key")
    args = ap.parse_args()
    if not (args.rehydrate or args.update_checksums or args.write_evidence or args.write_answer_key):
        ap.print_help()
        return 2
    t0 = time.perf_counter()

    if args.write_evidence or args.write_answer_key:
        pair, pair_manifest = plant.build_pair(make_world, Profile, MAIN_IDENTITIES, SEED)
        if args.write_evidence:
            for letter in ("A", "B"):
                write_evidence_package(pair[letter], letter)
            print(f"wrote evidence packages under {EVIDENCE_DIR.relative_to(ROOT).as_posix()}")
        if args.write_answer_key:
            planted = make_world("main", MAIN_IDENTITIES, plant.main_profile(Profile))
            plant.write_answer_key(SEALED_KEY, planted, pair, pair_manifest, CONSTANTS)
            print(f"wrote {SEALED_KEY.relative_to(ROOT).as_posix()}")

    if args.update_checksums:
        worlds = build_worlds(list(DATASETS))
        record = {"generator": GENERATOR,
                  "note": "sha256 content hashes only: each table's rows in primary-key order; evidence files with LF line endings.",
                  "datasets": {}, "evidence": {}}
        for name, path in DATASETS.items():
            write_db(worlds[name], path)
            record["datasets"][name] = content_checksums(path)
        record["evidence"] = evidence_hashes()
        CHECKSUMS.parent.mkdir(parents=True, exist_ok=True)
        CHECKSUMS.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {CHECKSUMS.relative_to(ROOT).as_posix()}")

    if args.rehydrate:
        expected = load_checksums()
        if expected is None:
            print(f"ERROR: {CHECKSUMS.relative_to(ROOT).as_posix()} is missing; cannot verify.")
            return 3
        todo = [n for n, p in DATASETS.items() if args.force or not p.is_file()]
        problems: list[str] = []
        if todo:
            worlds = build_worlds(todo)
            for name in todo:
                write_db(worlds[name], DATASETS[name])
                print(f"built {DATASETS[name].relative_to(ROOT).as_posix()}")
        for name in DATASETS:
            problems += verify_dataset(name, expected["datasets"][name])
        got_ev = evidence_hashes()
        for rel, digest in sorted(expected.get("evidence", {}).items()):
            if got_ev.get(rel) != digest:
                problems.append(f"evidence file changed or missing: {rel}")
        if problems:
            for p in problems:
                print("CHECKSUM MISMATCH:", p)
            if not args.force and not todo:
                print("Existing data does not match. Re-run with --force to rebuild.")
            return 1
        print(f"m01_iam: {len(DATASETS)} datasets verified against checksums "
              f"({'rebuilt ' + str(len(todo)) if todo else 'nothing to rebuild'}) "
              f"in {time.perf_counter() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
