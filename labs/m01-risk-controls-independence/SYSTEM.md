# Larkspur Desk: identity and access layer

*Owner: IAM Operations (IT Operations). Maintained by the 1st line. Last updated for the Q3 2026 control assessment.*

## What it is

Larkspur Desk is our customer-support SaaS. Customers open tickets; support agents work them in the
agent console; admins manage access; service accounts run customer integrations. The identity and
access layer decides who can sign in to which part of Larkspur Desk and what they can do there.

Every person who works on Larkspur Desk (employee or contractor) is an **identity** in HR. An identity
holds one or more **human accounts**, one per realm it needs:

| Realm | Used for | Username suffix |
|---|---|---|
| `console` | The agent console. Every identity gets one on joining. | none |
| `reporting` | Dashboards and exports | `.rpt` |
| `sandbox` | Engineering test tenants | `.sbx` |
| `admin` | Platform and access administration | `.adm` |
| `integration` | **Service accounts** for customer integrations, ETL, webhooks, mailers, bots | `svc-*` |

Every service account has a named owner (an identity), recorded on the account.

Access is granted as **entitlements**: one permission on one account. Each realm has a baseline bundle
granted at account creation (for example `ticket.read` and `kb.read` in the console); everything else
is requested and approved.

Sign-in goes through two SSO gateways (`sso-gw-eu1`, `sso-gw-us1`) for people and the API gateway
(`api-gw-1`, token authentication) for service accounts. The gateways' authentication records are
exported nightly into the security data store as `auth_events`.

All timestamps are UTC.

## Tables and what each is the system of record for

| Table | System of record for | Fed by |
|---|---|---|
| `hr_identities` | Who works here: worker type, department, line manager, hire and termination time. | Nightly HR export. Includes the records migrated from the previous HRIS in 2021 (`record_source = 'hris_legacy_import'`), which keep their original identifier format. |
| `iam_accounts` | **The inventory of every account, human and service.** Status, realm, the identity it belongs to (`hr_id`) or the owner (`owner_hr_id`), creation and disable time. | IAM provisioning service. |
| `entitlements` | Which account holds which permission, since when, granted by whom, against which approval (`approval_ref`). | IAM provisioning service and the admin console. |
| `access_requests` | Requests and approvals: new accounts, additional permissions, separation-of-duties exceptions, privileged-role nominations. | Access request workflow. |
| `access_reviews` | Quarterly certification decisions, reviewer of record, revocations and when they were actioned. | Campaign tool. |
| `auth_events` | Sign-in telemetry (success and failure) for every account. | Gateway logs via the nightly export. |

Identifiers: account ids look like `LDA123456`; request ids `REQ0001234`. IAM stores HR identifiers in
canonical form (`E` for employees, `C` for contractors, then six digits, for example `E012345`), and the
same form is used for managers, owners, requesters, approvers and reviewers.

## Controls

| ID | Control | Type | Owner | Frequency | Criteria |
|---|---|---|---|---|---|
| LD-AC-01 | Every entitlement grant has an owner-approved request dated before the grant | Preventive | IAM Operations Lead | Every grant | NIST SP 800-53 AC-2 |
| LD-AC-02 | Accounts of terminated identities are disabled within 24 hours of HR termination | Preventive (automated) | IAM Operations Lead, with People Operations | Daily | AC-2 |
| LD-AC-03 | Every active account, human and service, is certified by its owner each quarter; revocations are actioned within 7 days | Detective | IAM Operations Lead (campaign); line managers and service owners (decisions) | Quarterly | AC-2, CA-7 |
| LD-AC-04 | No identity holds a toxic pair (`refund.issue` + `refund.approve`; `iam.admin` + `auditlog.admin`) | Preventive and detective | Head of Security | Every request; quarterly report | AC-5 |
| LD-AC-05 | Privileged roles are limited to named owners | Preventive | Head of Security | Every grant; annual renewal | AC-6 |

### LD-AC-01: Approved request before every grant

**How it operates.** Access is requested in the access request workflow and approved by the approver of
record: the line manager for a human account, and the service owner's line manager for a service
account. The provisioning service grants only on an approved request and stamps the request id on the
entitlement (`entitlements.approval_ref`). New accounts are created from an approved `new_account`
request, which also covers the realm's baseline bundle. IAM admins making a change in the admin
console record the approved request reference on the grant.

**Evidence.** Each row in `entitlements` carries its `approval_ref`; the matching row in
`access_requests` shows the approver, `status = 'approved'` and a `decided_at` earlier than the grant.

### LD-AC-02: Leavers disabled within 24 hours

**How it operates.** The nightly HR export carries terminations. The IAM leaver job matches each
terminated identity to its accounts and disables every human account it holds, setting
`disable_reason = 'hr_termination'`. Service accounts owned by a leaver are reassigned by the team
before the owner leaves. IAM Operations checks the daily leaver job report.

**Evidence.** `iam_accounts.disabled_at` against `hr_identities.termination_ts`. Our own monitoring
shows leavers disabled well inside 24 hours.

### LD-AC-03: Quarterly access review

**How it operates.** A campaign runs in the third month of every quarter.

- **Population.** Every account with status active in IAM at 00:00 UTC on the first day of the
  campaign (2026Q2: 2026-06-01; 2026Q3: 2026-09-01), human and service. Accounts created after that
  instant are picked up by the next campaign.
- **Reviewer of record.** The identity's line manager for human accounts; the named owner for
  service accounts. The review list is generated from the IAM extract and routed to reviewers through
  the HR reporting lines.
- **Window.** 21 days. Reviewers certify or revoke each account on their list, then sign off.
- **Revocations.** A revoke decision either removes one entitlement or disables the account. It raises
  a change ticket that IAM Operations actions within 7 days.
- **Completion.** IAM Operations chases until every reviewer has signed off. Every campaign to date
  has closed at 100%.

**Evidence.** `access_reviews` (one row per account per campaign, with reviewer, decision, decision
time, actioned time and sign-off time) and the campaign evidence package handed to the assessor
(review decisions, revocations, reviewer sign-offs, completion summary, control owner attestation).

### LD-AC-04: Separation of duties

**How it operates.** The request workflow blocks a request that would give an identity both halves of a
toxic pair, across all of that identity's accounts. Where a small team genuinely needs both, the Head
of Security can approve a time-bound exception (`access_requests.request_type = 'sod_exception'`,
with `expires_at` and a compensating control in the justification). A quarterly SoD report lists
every identity holding a toxic pair and the exception covering it.

**Evidence.** Active entitlements on active accounts, grouped by identity, against approved,
unexpired `sod_exception` requests.

### LD-AC-05: Privileged roles limited to named owners

**How it operates.** `iam.admin`, `auditlog.admin` and `tenant.config` are privileged. They are granted
only to `admin`-realm accounts of identities named by the Head of Security through a
`privileged_nomination` request, renewed every year. Service accounts never hold privileged
permissions.

**Evidence.** Active privileged entitlements against approved, unexpired `privileged_nomination`
requests for the same identity and permission.

## Telemetry

`auth_events` records every sign-in attempt that reaches a gateway: time, account, method (`sso`,
`password`, `api_token`), result, failure reason, source IP and collector. Admin-console actions are
authenticated through SSO and appear as `sso` events from the `admin-console` collector. The nightly
export is the source for security monitoring and for any look-back on account use.

## Operating the simulator

The local simulator in `larkspur/` runs the same layer against a working copy of a dataset. See
`README.md` for commands.
