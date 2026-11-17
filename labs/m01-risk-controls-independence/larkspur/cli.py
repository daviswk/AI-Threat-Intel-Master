"""Larkspur Desk access simulator: command-line interface.

Every write command works on a working copy (see `workcopy`). The generated
datasets are opened read-only and never modified.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import shutil
import sys

import duckdb

LAB = pathlib.Path(__file__).resolve().parents[1]
ROOT = LAB.parents[1]
DEFAULT_DB = LAB / "data" / "work" / "larkspur.duckdb"
SOURCES = {
    "planted": ROOT / "assurance-harness" / "data" / "m01" / "planted.duckdb",
    "clean": ROOT / "assurance-harness" / "data" / "m01" / "clean.duckdb",
    "snapshot-A": LAB / "data" / "q3_review_snapshot_A.duckdb",
    "snapshot-B": LAB / "data" / "q3_review_snapshot_B.duckdb",
}
TABLES = ["hr_identities", "iam_accounts", "entitlements", "access_requests", "access_reviews", "auth_events"]
REALMS = ["console", "reporting", "sandbox", "admin", "integration"]
METHODS = ["sso", "password", "api_token"]
TS_FMT = "%Y-%m-%d %H:%M:%S"


class CliError(Exception):
    def __init__(self, msg: str, code: int = 2):
        super().__init__(msg)
        self.code = code


# ---------------------------------------------------------------------------
# plumbing
# ---------------------------------------------------------------------------
def _rel(p: pathlib.Path) -> str:
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def _db_path(args) -> pathlib.Path:
    raw = getattr(args, "db", None) or os.environ.get("LARKSPUR_DB")
    p = pathlib.Path(raw) if raw else DEFAULT_DB
    if not p.is_absolute():
        p = (pathlib.Path.cwd() / p)
    return p.resolve()


def _is_protected(p: pathlib.Path) -> bool:
    p = p.resolve()
    if any(p == s.resolve() for s in SOURCES.values()):
        return True
    gen_dir = (ROOT / "assurance-harness" / "data").resolve()
    return gen_dir in p.parents


def _connect(args, write: bool) -> duckdb.DuckDBPyConnection:
    p = _db_path(args)
    if not p.is_file():
        raise CliError(f"no database at {_rel(p)}. Create a working copy first: "
                       "larkspur_cli.py workcopy --from planted")
    if write and _is_protected(p):
        raise CliError(f"{_rel(p)} is a generated dataset and is read-only. "
                       "Make a working copy with `workcopy` and point --db at it.")
    return duckdb.connect(str(p), read_only=not write)


def _now(args) -> str:
    at = getattr(args, "at", None)
    if at:
        try:
            return dt.datetime.strptime(at, TS_FMT).strftime(TS_FMT)
        except ValueError:
            raise CliError(f"--at must look like '2026-10-05 14:30:00', got {at!r}")
    return dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).strftime(TS_FMT)


def _rows(con, sql, params=()):
    cur = con.execute(sql, params)
    cols = [d[0] for d in cur.description]
    return cols, cur.fetchall()


def _fmt(v):
    if v is None:
        return ""
    if isinstance(v, dt.datetime):
        return v.strftime(TS_FMT)
    return str(v)


def _emit(args, cols, rows, title=None):
    if getattr(args, "json", False):
        print(json.dumps([{c: _fmt(v) if isinstance(v, dt.datetime) else v for c, v in zip(cols, r)}
                          for r in rows], indent=2, default=str))
        return
    if title:
        print(f"== {title} ({len(rows)})")
    if not rows:
        print("(no rows)")
        return
    cells = [[_fmt(v) for v in r] for r in rows]
    widths = [max(len(c), *(len(r[i]) for r in cells)) for i, c in enumerate(cols)]
    print("  ".join(c.ljust(w) for c, w in zip(cols, widths)))
    print("  ".join("-" * w for w in widths))
    for r in cells:
        print("  ".join(v.ljust(w) for v, w in zip(r, widths)))


def _emit_record(args, record: dict):
    if getattr(args, "json", False):
        print(json.dumps(record, indent=2, default=str))
    else:
        for k, v in record.items():
            print(f"{k}: {_fmt(v)}")


def _account(con, account_id):
    cols, rows = _rows(con, "SELECT * FROM iam_accounts WHERE account_id = ?", (account_id,))
    return dict(zip(cols, rows[0])) if rows else None


def _identity(con, hr_id):
    cols, rows = _rows(con, "SELECT * FROM hr_identities WHERE hr_id = ?", (hr_id,))
    if not rows:
        digits = "".join(ch for ch in hr_id if ch.isdigit())
        if digits:
            cols, rows = _rows(con, "SELECT * FROM hr_identities "
                                    "WHERE TRY_CAST(regexp_extract(hr_id, '[0-9]+') AS INTEGER) = ?",
                               (int(digits),))
    return dict(zip(cols, rows[0])) if rows else None


def _canonical(ident) -> str:
    digits = "".join(ch for ch in ident["hr_id"] if ch.isdigit())
    prefix = "C" if ident["worker_type"] == "contractor" else "E"
    return f"{prefix}{int(digits):06d}"


def _next_int(con, table, col):
    return int(con.execute(f"SELECT coalesce(max({col}), 0) + 1 FROM {table}").fetchone()[0])


def _next_request_id(con):
    n = con.execute("SELECT coalesce(max(CAST(substr(request_id, 4) AS BIGINT)), 0) + 1 "
                    "FROM access_requests").fetchone()[0]
    return f"REQ{int(n):07d}"


def _log_auth(con, account_id, at, method, result, reason, ip, collector):
    eid = _next_int(con, "auth_events", "event_id")
    con.execute("INSERT INTO auth_events VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (eid, at, account_id, method, result, reason, ip, collector))
    return eid


def _require_admin(con, actor, at):
    a = _account(con, actor)
    if a is None:
        raise CliError(f"actor {actor} not found", 2)
    if a["status"] != "active":
        _log_auth(con, actor, at, "sso", "failure", "account_disabled", "198.51.100.20", "admin-console")
        raise CliError(f"actor {actor} is disabled", 2)
    held = con.execute("SELECT count(*) FROM entitlements WHERE account_id = ? AND permission = 'iam.admin' "
                       "AND revoked_at IS NULL", (actor,)).fetchone()[0]
    if not held:
        _log_auth(con, actor, at, "sso", "failure", "not_authorized", "198.51.100.20", "admin-console")
        raise CliError(f"actor {actor} does not hold iam.admin", 2)
    _log_auth(con, actor, at, "sso", "success", None, "198.51.100.20", "admin-console")
    return a


def _approver_for(con, account):
    owner = _identity(con, account["owner_hr_id"]) if account["owner_hr_id"] else None
    if owner is None:
        return None
    return owner["manager_hr_id"]


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------
def cmd_workcopy(args):
    src = SOURCES[args.source]
    if not src.is_file():
        raise CliError(f"{_rel(src)} is missing; run `uv run --frozen python scripts/rehydrate.py` first")
    dest = pathlib.Path(args.to) if args.to else DEFAULT_DB
    if not dest.is_absolute():
        dest = pathlib.Path.cwd() / dest
    dest = dest.resolve()
    if _is_protected(dest):
        raise CliError("refusing to overwrite a generated dataset")
    if dest.exists() and not args.overwrite:
        raise CliError(f"{_rel(dest)} exists; pass --overwrite to replace it")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    print(f"working copy of {args.source} written to {_rel(dest)}")
    return 0


def cmd_info(args):
    con = _connect(args, write=False)
    p = _db_path(args)
    rows = [(t, con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]) for t in TABLES]
    print(f"database: {_rel(p)}{'  (read-only dataset)' if _is_protected(p) else ''}")
    _emit(args, ["table", "rows"], rows)
    return 0


def cmd_list_accounts(args):
    con = _connect(args, write=False)
    where, params = [], []
    for col, val in (("status", args.status), ("account_type", args.type), ("realm", args.realm),
                     ("owner_hr_id", args.owner)):
        if val:
            where.append(f"{col} = ?")
            params.append(val)
    if args.username_like:
        where.append("username LIKE ?")
        params.append(args.username_like)
    sql = ("SELECT account_id, username, account_type, realm, owner_hr_id, status, created_at, disabled_at "
           "FROM iam_accounts" + (" WHERE " + " AND ".join(where) if where else "") +
           " ORDER BY account_id LIMIT ?")
    cols, rows = _rows(con, sql, tuple(params) + (args.limit,))
    _emit(args, cols, rows)
    return 0


def cmd_describe_account(args):
    con = _connect(args, write=False)
    a = _account(con, args.account_id)
    if a is None:
        raise CliError(f"account {args.account_id} not found", 1)
    if args.json:
        out = {"account": a}
        for name, sql in (
            ("entitlements", "SELECT * FROM entitlements WHERE account_id = ? ORDER BY entitlement_id"),
            ("recent_auth_events", "SELECT * FROM auth_events WHERE account_id = ? ORDER BY event_ts DESC LIMIT 10"),
            ("access_reviews", "SELECT * FROM access_reviews WHERE account_id = ? ORDER BY review_id"),
        ):
            cols, rows = _rows(con, sql, (args.account_id,))
            out[name] = [dict(zip(cols, r)) for r in rows]
        print(json.dumps(out, indent=2, default=str))
        return 0
    _emit_record(args, a)
    print()
    cols, rows = _rows(con, "SELECT entitlement_id, permission, granted_at, granted_by, approval_ref, revoked_at "
                            "FROM entitlements WHERE account_id = ? ORDER BY entitlement_id", (args.account_id,))
    _emit(args, cols, rows, "entitlements")
    print()
    cols, rows = _rows(con, "SELECT event_id, event_ts, auth_method, result, failure_reason, source_ip "
                            "FROM auth_events WHERE account_id = ? ORDER BY event_ts DESC LIMIT 10",
                       (args.account_id,))
    _emit(args, cols, rows, "recent auth events (latest 10)")
    print()
    cols, rows = _rows(con, "SELECT review_id, reviewer_hr_id, decision, decided_at FROM access_reviews "
                            "WHERE account_id = ? ORDER BY review_id", (args.account_id,))
    _emit(args, cols, rows, "access reviews")
    return 0


def cmd_list_entitlements(args):
    con = _connect(args, write=False)
    where, params = [], []
    if args.account:
        where.append("account_id = ?")
        params.append(args.account)
    if args.permission:
        where.append("permission = ?")
        params.append(args.permission)
    if args.active_only:
        where.append("revoked_at IS NULL")
    sql = ("SELECT entitlement_id, account_id, permission, granted_at, granted_by, approval_ref, revoked_at "
           "FROM entitlements" + (" WHERE " + " AND ".join(where) if where else "") +
           " ORDER BY entitlement_id LIMIT ?")
    cols, rows = _rows(con, sql, tuple(params) + (args.limit,))
    _emit(args, cols, rows)
    return 0


def cmd_list_permissions(args):
    con = _connect(args, write=False)
    cols, rows = _rows(con, "SELECT permission, count(*) AS active_grants FROM entitlements "
                            "WHERE revoked_at IS NULL GROUP BY permission ORDER BY permission")
    _emit(args, cols, rows)
    return 0


def cmd_list_identities(args):
    con = _connect(args, write=False)
    where, params = [], []
    if args.status:
        where.append("hr_status = ?")
        params.append(args.status)
    if args.department:
        where.append("department = ?")
        params.append(args.department)
    if args.name_like:
        where.append("(given_name || ' ' || family_name) ILIKE ?")
        params.append(args.name_like)
    sql = ("SELECT hr_id, worker_type, given_name, family_name, department, job_title, manager_hr_id, "
           "hire_ts, termination_ts, hr_status FROM hr_identities" +
           (" WHERE " + " AND ".join(where) if where else "") + " ORDER BY hr_id LIMIT ?")
    cols, rows = _rows(con, sql, tuple(params) + (args.limit,))
    _emit(args, cols, rows)
    return 0


def cmd_describe_identity(args):
    con = _connect(args, write=False)
    ident = _identity(con, args.hr_id)
    if ident is None:
        raise CliError(f"identity {args.hr_id} not found", 1)
    _emit_record(args, ident)
    canon = _canonical(ident)
    if not args.json:
        print()
        cols, rows = _rows(con, "SELECT account_id, username, account_type, realm, status FROM iam_accounts "
                                "WHERE hr_id = ? OR owner_hr_id = ? ORDER BY account_id", (canon, canon))
        _emit(args, cols, rows, "accounts held or owned")
    return 0


def cmd_list_requests(args):
    con = _connect(args, write=False)
    where, params = [], []
    for col, val in (("account_id", args.account), ("status", args.status), ("request_type", args.type)):
        if val:
            where.append(f"{col} = ?")
            params.append(val)
    sql = ("SELECT request_id, request_type, account_id, permission, requested_by_hr_id, requested_at, "
           "approver_hr_id, status, decided_at, expires_at FROM access_requests" +
           (" WHERE " + " AND ".join(where) if where else "") + " ORDER BY request_id DESC LIMIT ?")
    cols, rows = _rows(con, sql, tuple(params) + (args.limit,))
    _emit(args, cols, rows)
    return 0


def cmd_authenticate(args):
    con = _connect(args, write=True)
    at = _now(args)
    a = _account(con, args.account_id)
    if a is None:
        print("authentication failed")
        return 1
    method = args.method or ("api_token" if a["account_type"] == "service" else "sso")
    ip = args.source_ip or ("192.0.2.10" if method == "api_token" else "198.51.100.10")
    collector = "api-gw-1" if method == "api_token" else "sso-gw-eu1"
    if args.bad_credential:
        reason = "token_invalid" if method == "api_token" else "bad_password"
        eid = _log_auth(con, a["account_id"], at, method, "failure", reason, ip, collector)
        print(f"authentication failed ({reason}); event {eid}")
        return 1
    if a["status"] != "active" and method != "api_token":
        eid = _log_auth(con, a["account_id"], at, method, "failure", "account_disabled", ip, collector)
        print(f"authentication failed (account_disabled); event {eid}")
        return 1
    eid = _log_auth(con, a["account_id"], at, method, "success", None, ip, collector)
    print(f"authenticated {a['account_id']} ({a['username']}) via {method} at {at}; event {eid}")
    return 0


def cmd_submit_request(args):
    con = _connect(args, write=True)
    at = _now(args)
    a = _account(con, args.account)
    if a is None:
        raise CliError(f"account {args.account} not found", 1)
    requester = _identity(con, args.requested_by)
    if requester is None:
        raise CliError(f"requester {args.requested_by} not found in HR", 1)
    approver = _approver_for(con, a)
    if approver is None:
        raise CliError("no approver of record could be resolved for this account", 1)
    rid = _next_request_id(con)
    con.execute("INSERT INTO access_requests VALUES (?, 'add_permission', ?, ?, ?, ?, ?, ?, 'pending', NULL, NULL, ?)",
                (rid, a["account_id"], a["owner_hr_id"], args.permission, _canonical(requester), at, approver,
                 args.justification))
    print(f"request {rid} submitted for {args.permission} on {a['account_id']}; approver of record {approver}")
    return 0


def cmd_approve_request(args):
    con = _connect(args, write=True)
    at = _now(args)
    cols, rows = _rows(con, "SELECT * FROM access_requests WHERE request_id = ?", (args.request_id,))
    if not rows:
        raise CliError(f"request {args.request_id} not found", 1)
    r = dict(zip(cols, rows[0]))
    if r["status"] != "pending":
        raise CliError(f"request {args.request_id} is {r['status']}, not pending")
    if args.approver != r["approver_hr_id"]:
        raise CliError(f"{args.approver} is not the approver of record ({r['approver_hr_id']})")
    status = "rejected" if args.reject else "approved"
    con.execute("UPDATE access_requests SET status = ?, decided_at = ? WHERE request_id = ?",
                (status, at, args.request_id))
    print(f"request {args.request_id} {status} by {args.approver} at {at}")
    return 0


def cmd_grant(args):
    con = _connect(args, write=True)
    at = _now(args)
    _require_admin(con, args.actor, at)
    a = _account(con, args.account)
    if a is None:
        raise CliError(f"account {args.account} not found", 1)
    dup = con.execute("SELECT count(*) FROM entitlements WHERE account_id = ? AND permission = ? AND revoked_at IS NULL",
                      (args.account, args.permission)).fetchone()[0]
    if dup:
        raise CliError(f"{args.account} already holds {args.permission}", 1)
    ref = args.approval_ref.strip() if args.approval_ref else None
    eid = _next_int(con, "entitlements", "entitlement_id")
    con.execute("INSERT INTO entitlements VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)",
                (eid, args.account, args.permission, at, args.actor, ref or None))
    print(f"granted {args.permission} to {args.account} as entitlement {eid} "
          f"(approval_ref {ref or 'none'}) at {at}")
    return 0


def cmd_create_account(args):
    con = _connect(args, write=True)
    at = _now(args)
    _require_admin(con, args.actor, at)
    if con.execute("SELECT count(*) FROM iam_accounts WHERE username = ?", (args.username,)).fetchone()[0]:
        raise CliError(f"username {args.username} already exists", 1)
    if args.type == "human":
        if not args.hr_id:
            raise CliError("--hr-id is required for a human account")
        ident = _identity(con, args.hr_id)
        if ident is None:
            raise CliError(f"identity {args.hr_id} not found in HR", 1)
        hr = owner = _canonical(ident)
        realm = args.realm or "console"
        email = args.email or ident["email"]
    else:
        if not args.owner_hr_id:
            raise CliError("--owner-hr-id is required for a service account")
        ident = _identity(con, args.owner_hr_id)
        if ident is None:
            raise CliError(f"owner {args.owner_hr_id} not found in HR", 1)
        hr, owner = None, _canonical(ident)
        realm = args.realm or "integration"
        email = args.email or f"{args.username}@svc.example.net"
    if realm not in REALMS:
        raise CliError(f"realm must be one of {', '.join(REALMS)}")
    seed = int(hashlib.sha256(f"{args.username}|{at}".encode()).hexdigest(), 16)
    while True:
        acc_id = f"LDA{100000 + seed % 900000}"
        if _account(con, acc_id) is None:
            break
        seed += 1
    con.execute("INSERT INTO iam_accounts VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?, NULL, NULL, ?)",
                (acc_id, args.username, args.type, realm, hr, owner, email, at, args.request_ref))
    print(f"created {args.type} account {acc_id} ({args.username}, realm {realm}, owner {owner}) at {at}")
    return 0


def cmd_disable_account(args):
    con = _connect(args, write=True)
    at = _now(args)
    _require_admin(con, args.actor, at)
    a = _account(con, args.account_id)
    if a is None:
        raise CliError(f"account {args.account_id} not found", 1)
    if a["status"] != "active":
        raise CliError(f"{args.account_id} is already {a['status']}", 1)
    con.execute("UPDATE iam_accounts SET status = 'disabled', disabled_at = ?, disable_reason = ? "
                "WHERE account_id = ?", (at, args.reason, args.account_id))
    print(f"disabled {args.account_id} ({a['username']}) at {at}, reason {args.reason}")
    return 0


def cmd_sql(args):
    if args.dataset:
        p = SOURCES[args.dataset]
        if not p.is_file():
            raise CliError(f"{_rel(p)} is missing; run `uv run --frozen python scripts/rehydrate.py` first")
        con = duckdb.connect(str(p), read_only=True)
    else:
        con = _connect(args, write=False)
    cols, rows = _rows(con, args.query)
    _emit(args, cols, rows[: args.limit] if args.limit else rows)
    if not args.json and args.limit and len(rows) > args.limit:
        print(f"... {len(rows) - args.limit} more rows (raise --limit)")
    return 0


# ---------------------------------------------------------------------------
# parser
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--db", help=f"working database (default {_rel(DEFAULT_DB)}, or $LARKSPUR_DB)")
    common.add_argument("--json", action="store_true", help="machine-readable output")
    timed = argparse.ArgumentParser(add_help=False)
    timed.add_argument("--at", help="event time 'YYYY-MM-DD HH:MM:SS' (UTC); default: now")

    ap = argparse.ArgumentParser(
        prog="larkspur_cli.py",
        description="Larkspur Desk identity and access layer (local simulator). "
                    "Start with: workcopy --from planted",
        epilog="Run `<command> --help` for the options of each command.")
    sub = ap.add_subparsers(dest="command", metavar="command")
    sub.required = True

    p = sub.add_parser("workcopy", help="copy a generated dataset to a writable working database")
    p.add_argument("--from", dest="source", required=True, choices=["planted", "clean"])
    p.add_argument("--to", help=f"destination (default {_rel(DEFAULT_DB)})")
    p.add_argument("--overwrite", action="store_true")
    p.set_defaults(fn=cmd_workcopy)

    p = sub.add_parser("info", parents=[common], help="show the database in use and its row counts")
    p.set_defaults(fn=cmd_info)

    p = sub.add_parser("list-accounts", parents=[common], help="list accounts in the IAM inventory")
    p.add_argument("--status", choices=["active", "disabled"])
    p.add_argument("--type", choices=["human", "service"])
    p.add_argument("--realm", choices=REALMS)
    p.add_argument("--owner", help="owner hr_id (canonical form, e.g. E012345)")
    p.add_argument("--username-like", help="SQL LIKE pattern, e.g. 'svc-int-%%'")
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(fn=cmd_list_accounts)

    p = sub.add_parser("describe-account", parents=[common], help="one account: details, entitlements, logins, reviews")
    p.add_argument("account_id")
    p.set_defaults(fn=cmd_describe_account)

    p = sub.add_parser("list-entitlements", parents=[common], help="list entitlement grants")
    p.add_argument("--account")
    p.add_argument("--permission", help="e.g. iam.admin")
    p.add_argument("--active-only", action="store_true")
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(fn=cmd_list_entitlements)

    p = sub.add_parser("list-permissions", parents=[common], help="permissions in use, with active grant counts")
    p.set_defaults(fn=cmd_list_permissions)

    p = sub.add_parser("list-identities", parents=[common], help="list HR identities")
    p.add_argument("--status", choices=["active", "terminated"])
    p.add_argument("--department")
    p.add_argument("--name-like", help="ILIKE pattern on 'given family', e.g. '%%kestrel%%'")
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(fn=cmd_list_identities)

    p = sub.add_parser("describe-identity", parents=[common], help="one HR identity and the accounts it holds or owns")
    p.add_argument("hr_id")
    p.set_defaults(fn=cmd_describe_identity)

    p = sub.add_parser("list-requests", parents=[common], help="list access requests")
    p.add_argument("--account")
    p.add_argument("--status", choices=["pending", "approved", "rejected"])
    p.add_argument("--type", choices=["new_account", "add_permission", "sod_exception", "privileged_nomination"])
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(fn=cmd_list_requests)

    p = sub.add_parser("authenticate", parents=[common, timed], help="log in as an account")
    p.add_argument("account_id")
    p.add_argument("--method", choices=METHODS, help="default: sso for human, api_token for service accounts")
    p.add_argument("--source-ip")
    p.add_argument("--bad-credential", action="store_true", help="simulate a wrong password or token")
    p.set_defaults(fn=cmd_authenticate)

    p = sub.add_parser("submit-request", parents=[common, timed], help="raise an access request (pending)")
    p.add_argument("--account", required=True)
    p.add_argument("--permission", required=True)
    p.add_argument("--requested-by", required=True, help="requester hr_id")
    p.add_argument("--justification", default="Required for role")
    p.set_defaults(fn=cmd_submit_request)

    p = sub.add_parser("approve-request", parents=[common, timed], help="approve (or --reject) a pending request")
    p.add_argument("request_id")
    p.add_argument("--approver", required=True, help="approver hr_id; must be the approver of record")
    p.add_argument("--reject", action="store_true")
    p.set_defaults(fn=cmd_approve_request)

    p = sub.add_parser("grant", parents=[common, timed], help="grant a permission to an account (admin)")
    p.add_argument("--actor", required=True, help="admin account performing the change (holds iam.admin)")
    p.add_argument("--account", required=True)
    p.add_argument("--permission", required=True)
    p.add_argument("--approval-ref", help="approved request id, e.g. REQ0001234")
    p.set_defaults(fn=cmd_grant)

    p = sub.add_parser("create-account", parents=[common, timed], help="create an account (admin)")
    p.add_argument("--actor", required=True, help="admin account performing the change (holds iam.admin)")
    p.add_argument("--username", required=True)
    p.add_argument("--type", choices=["human", "service"], required=True)
    p.add_argument("--realm", choices=REALMS, help="default: console (human) / integration (service)")
    p.add_argument("--hr-id", help="human accounts: the person's hr_id")
    p.add_argument("--owner-hr-id", help="service accounts: the owner's hr_id")
    p.add_argument("--email")
    p.add_argument("--request-ref", help="provisioning request id")
    p.set_defaults(fn=cmd_create_account)

    p = sub.add_parser("disable-account", parents=[common, timed], help="disable an account (admin)")
    p.add_argument("account_id")
    p.add_argument("--actor", required=True, help="admin account performing the change (holds iam.admin)")
    p.add_argument("--reason", default="manual", choices=["manual", "hr_termination", "access_review", "decommissioned"])
    p.set_defaults(fn=cmd_disable_account)

    p = sub.add_parser("sql", parents=[common], help="run a read-only SQL query")
    p.add_argument("query")
    p.add_argument("--dataset", choices=sorted(SOURCES), help="query a generated dataset directly (read-only)")
    p.add_argument("--limit", type=int, default=200, help="rows to print (0 = all)")
    p.set_defaults(fn=cmd_sql)
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except CliError as e:
        print(f"error: {e}", file=sys.stderr)
        return e.code
    except duckdb.Error as e:
        print(f"database error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
