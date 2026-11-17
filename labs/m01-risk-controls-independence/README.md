# Module 1 lab: Larkspur Desk identity and access layer

The system is described in [`SYSTEM.md`](SYSTEM.md). This page is how to build the data, run the
simulator and query the tables. All commands run from the **repo root**.

## 1. Build the data

The databases are not tracked in Git. A seeded generator rebuilds them byte-for-byte in content
(checked against committed checksums):

```
uv run --frozen python scripts/rehydrate.py            # build whatever is missing, verify everything
uv run --frozen python scripts/rehydrate.py --force    # rebuild everything
```

or the Module 1 generator on its own:

```
uv run --frozen python assurance-harness/generators/m01_iam.py --rehydrate [--force]
```

Generator: `assurance-harness/generators/m01_iam.py`, fixed seed `20260930`. Checksums:
`assurance-harness/generators/checksums/m01_iam.json` (sha256 of each table's rows in primary-key
order). A full rebuild takes under a minute. A non-zero exit means the local data is not the
expected dataset: stop and investigate.

| Database | What it is |
|---|---|
| `assurance-harness/data/m01/planted.duckdb` | Larkspur Desk, observation period 2026-04-01 to 2026-09-30 |
| `assurance-harness/data/m01/clean.duckdb` | Larkspur Desk, same period, second dataset |
| `labs/m01-risk-controls-independence/data/q3_review_snapshot_A.duckdb` | Identity tables behind evidence package A |
| `labs/m01-risk-controls-independence/data/q3_review_snapshot_B.duckdb` | Identity tables behind evidence package B |

Each database has the same six tables: `hr_identities`, `iam_accounts`, `entitlements`,
`access_requests`, `access_reviews`, `auth_events` (see `SYSTEM.md` for what each is the system of
record for). Approximate size: 3,000 identities, 12,000 accounts, 44,000 entitlements, 42,000
requests, 19,000 to 20,000 review decisions over two quarters, 115,000 to 120,000 auth events.

## 2. Query the data read-only

Never write to the generated databases. Open them read-only.

With the simulator's `sql` command:

```
uv run --frozen python labs/m01-risk-controls-independence/larkspur_cli.py sql --dataset snapshot-A "SELECT count(*) FROM iam_accounts WHERE status = 'active'"
uv run --frozen python labs/m01-risk-controls-independence/larkspur_cli.py sql --dataset planted --limit 0 "SELECT campaign_id, count(*) FROM access_reviews GROUP BY 1"
```

`--dataset` takes `planted`, `clean`, `snapshot-A`, `snapshot-B`. Add `--json` for machine-readable
output.

With DuckDB from Python:

```python
import duckdb
con = duckdb.connect("labs/m01-risk-controls-independence/data/q3_review_snapshot_A.duckdb", read_only=True)
print(con.sql("SELECT realm, status, count(*) FROM iam_accounts GROUP BY ALL ORDER BY ALL"))
```

Run it with `uv run --frozen python your_script.py`. Evidence CSVs can be read in the same session
with `con.read_csv('labs/m01-risk-controls-independence/evidence/q3_access_review/package_A/review_decisions.csv')`.

## 3. Q3 2026 access-review evidence

`evidence/q3_access_review/package_A/` and `package_B/` are two Q3 2026 user access review evidence
packages, as IAM Operations hands them to an assessor. Each package was produced from its own
system: package A from `data/q3_review_snapshot_A.duckdb`, package B from
`data/q3_review_snapshot_B.duckdb`. Each package's `README.md` lists its contents.

## 4. Run the simulator

```
uv run --frozen python labs/m01-risk-controls-independence/larkspur_cli.py --help
uv run --frozen python labs/m01-risk-controls-independence/larkspur_cli.py <command> --help
```

### Working copy first

Write commands only ever touch a working copy. Make one from a generated dataset:

```
uv run --frozen python labs/m01-risk-controls-independence/larkspur_cli.py workcopy --from planted
```

This writes `labs/m01-risk-controls-independence/data/work/larkspur.duckdb` (untracked), which every
command uses by default. Use `--to PATH` for another location, `--overwrite` to reset it, and
`--db PATH` (or the `LARKSPUR_DB` environment variable) to point commands at it. The simulator
refuses to write to the generated databases.

Write commands stamp the current UTC time. Pass `--at "2026-10-05 09:00:00"` for a fixed,
re-runnable timeline.

### Commands

| Command | What it does | Writes |
|---|---|---|
| `info` | Database in use and row counts | nothing |
| `list-accounts [--status] [--type] [--realm] [--owner HR_ID] [--username-like PATTERN] [--limit N]` | Accounts in the IAM inventory | nothing |
| `describe-account ACCOUNT_ID` | Account, entitlements, latest sign-ins, review history | nothing |
| `list-entitlements [--account] [--permission] [--active-only] [--limit N]` | Entitlement grants | nothing |
| `list-permissions` | Permissions in use with active grant counts | nothing |
| `list-identities [--status] [--department] [--name-like PATTERN] [--limit N]` | HR identities | nothing |
| `describe-identity HR_ID` | One identity and the accounts it holds or owns | nothing |
| `list-requests [--account] [--status] [--type] [--limit N]` | Access requests, newest first | nothing |
| `authenticate ACCOUNT_ID [--method sso\|password\|api_token] [--source-ip IP] [--bad-credential]` | Sign in as an account | `auth_events` |
| `submit-request --account ID --permission P --requested-by HR_ID [--justification TEXT]` | Raise a pending request, routed to the approver of record | `access_requests` |
| `approve-request REQUEST_ID --approver HR_ID [--reject]` | Decide a pending request | `access_requests` |
| `grant --actor ADMIN_ACCOUNT --account ID --permission P [--approval-ref REQ_ID]` | Grant a permission | `entitlements`, `auth_events` (actor sign-in) |
| `create-account --actor ADMIN_ACCOUNT --username U --type human\|service [--realm R] [--hr-id HR_ID] [--owner-hr-id HR_ID] [--email E] [--request-ref REQ_ID]` | Create an account | `iam_accounts`, `auth_events` (actor sign-in) |
| `disable-account ACCOUNT_ID --actor ADMIN_ACCOUNT [--reason manual\|hr_termination\|access_review\|decommissioned]` | Disable an account | `iam_accounts`, `auth_events` (actor sign-in) |
| `sql "QUERY" [--dataset NAME] [--limit N]` | Read-only SQL | nothing |

Admin commands (`grant`, `create-account`, `disable-account`) need `--actor`: an active account
holding `iam.admin`. The actor's sign-in to the admin console is recorded in `auth_events`.

### Example session

```
L="uv run --frozen python labs/m01-risk-controls-independence/larkspur_cli.py"
$L workcopy --from planted --overwrite
$L list-entitlements --permission iam.admin --active-only
$L describe-account LDA120807
$L submit-request --account LDA120807 --permission integration.manage --requested-by E027190 --at "2026-10-05 09:00:00"
$L list-requests --account LDA120807 --status pending
$L approve-request REQ0042736 --approver <approver_hr_id shown above> --at "2026-10-05 10:00:00"
$L grant --actor LDA120807 --account LDA120807 --permission integration.manage --approval-ref REQ0042736 --at "2026-10-05 10:30:00"
$L authenticate LDA120807 --at "2026-10-05 11:00:00"
```

(Request ids are allocated by the working copy; use the id `submit-request` prints.)

## Layout

| Path | Contents |
|---|---|
| `SYSTEM.md` | The system and its five controls, as IAM Operations runs them |
| `larkspur/`, `larkspur_cli.py` | The simulator |
| `evidence/q3_access_review/` | Q3 2026 access-review evidence packages (tracked) |
| `data/` | Snapshot databases and working copies (untracked, rebuilt by the generator) |
