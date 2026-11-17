# Q3 2026 User Access Review: evidence package B

**Control:** LD-AC-03, quarterly certification of every active account (human and service) by its owner; revocations actioned within 7 days.
**Control owner:** IAM Operations Lead, IT Operations.
**Campaign:** UAR-2026Q3. Population as at 2026-09-01 00:00:00 UTC. Review window 2026-09-01 00:00:00 to 2026-09-21 23:59:59 UTC.
**Prepared by:** IAM Operations, for the Q3 2026 control assessment.

## Headline

| Measure | Result |
|---|---|
| Accounts in scope (active in IAM at the population date) | 9,855 |
| Human / service | 4,222 / 5,633 |
| Decisions recorded | 9,855 (100.0%) |
| Certified | 9,584 |
| Revoked | 271 |
| Revocations actioned within 7 days | 271 of 271 (max 6.5 days) |
| Reviewers / signed off | 526 / 526 |
| Decisions made | 2026-09-01 08:05:41 to 2026-09-17 18:56:19 UTC |
| Last reviewer sign-off | 2026-09-17 19:58:30 UTC |

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
`labs/m01-risk-controls-independence/data/q3_review_snapshot_B.duckdb`.
