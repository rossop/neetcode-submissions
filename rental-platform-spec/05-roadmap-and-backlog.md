# 05 — Roadmap & Feature Backlog (→ GitHub Issues)

**Related:** [03-architecture / build order](./03-architecture-and-services.md#5-build-order-what-to-build-first--and-why)

This is the canonical backlog. **Each feature becomes a GitHub Issue.** PRs reference the
issue number (`Closes #N`). The `#E0x` codes below are stable backlog IDs; replace them with
real issue numbers once issues are created (a mapping table is at the bottom).

**Conventions**
- Repo is **private**.
- Labels: `phase:0..4`, `area:core`, `area:reputation`, `area:compliance`, `country:it`,
  `country:uk`, `lang:python`, `lang:go`, `type:feature|spike|infra|legal`.
- Milestones = phases. An issue is "done" when its acceptance criteria pass + audit/tests exist.

---

## Phase 0 — Foundations  *(milestone: `M0`)*
| ID | Title | Labels | Acceptance (short) |
|----|-------|--------|--------------------|
| E01 | Create private repo + CI + license/secret hygiene | phase:0, infra | Private repo, CI runs lint+test on PRs |
| E02 | FastAPI skeleton + Postgres + Alembic migrations | phase:0, infra, lang:python | App boots, migration baseline, healthcheck |
| E03 | Auth & Org: landlord signup, MFA, tenant magic-link | phase:0, area:core | Login/MFA works; tenant can open a magic link |
| E04 | Append-only audit log primitive | phase:0, area:core | Sensitive actions emit immutable events |
| E05 | Deploy pipeline + environments (staging/prod) | phase:0, infra | Push-to-deploy to staging |
| E06 | PWA shell + i18n scaffold (IT/EN) | phase:0, area:core | Locale switch, base layout |

## Phase 1 — Core MVP (Italy first)  *(milestone: `M1`)*
| ID | Title | Labels | Acceptance (short) |
|----|-------|--------|--------------------|
| E10 | Property & Units CRUD + certificate docs w/ expiry | phase:1, area:core, country:it | Add property/unit, attach APE w/ expiry |
| E11 | IT rule pack v1 (contract types, durations, tax params) | phase:1, area:compliance, country:it | Versioned data drives templates |
| E12 | Tenancy lifecycle: applications → tenancy entity | phase:1, area:core | Create/track applications, convert to tenancy |
| E13 | IT contract generation (4+4, 3+2, transitorio, studenti) | phase:1, area:core, country:it | Correct PDF per type w/ merge fields |
| E14 | Simple in-house e-signature + document hashing | phase:1, area:core | Signed PDF, tamper-evident audit record |
| E15 | Compliance & Deadlines engine + reminders | phase:1, area:compliance | Obligation queue, email reminders, mark-done audit |
| E16 | IT registration (30-day) reminder + data capture | phase:1, area:compliance, country:it | Reminder fires; reg. number stored |
| E17 | Cedolare vs ordinary decision support + election record | phase:1, area:compliance, country:it | Election recorded; annual tax reminder if ordinary |
| E18 | Deposit handling (≤3 mo cap, interest reminder) | phase:1, area:core, country:it | Cap validated; return reminder |
| E19 | Rent ledger: schedule, manual payments, arrears | phase:1, area:core | Charges/payments, running balance, arrears flag |
| E20 | Move-in inventory / check-in report + photos | phase:1, area:core | Itemized condition, tenant acknowledges |
| E21 | Move-out: check-out diff + deposit settlement + final ledger | phase:1, area:core | Deductions itemized, statement generated |
| E22 | Email notifications + per-tenancy activity log | phase:1, area:core | Threaded, exportable, email fan-out |
| E23 | GDPR basics: retention schedule, export, erasure (w/ holds) | phase:1, area:compliance, type:legal | Export + erasure honor legal holds |

## Phase 2 — UK support + payments  *(milestone: `M2`)*
| ID | Title | Labels | Acceptance (short) |
|----|-------|--------|--------------------|
| E30 | UK rule pack v1 (AST E&W) + Scotland PRT flag | phase:2, area:compliance, country:uk | AST templates; Scotland flagged |
| E31 | Deposit protection 30-day reminder + prescribed info served | phase:2, area:compliance, country:uk | Reminder + scheme/ref + served evidence |
| E32 | Deposit-cap validation (5/6 weeks) | phase:2, area:compliance, country:uk | Cap enforced by annual rent |
| E33 | Right to Rent checklist + evidence + recheck reminders | phase:2, area:compliance, country:uk | Check recorded; recheck reminder |
| E34 | UK certs: EPC/Gas(annual)/EICR(5y)/alarms + served tracking | phase:2, area:compliance, country:uk | Each cert tracked + served evidence |
| E35 | How to Rent (versioned) served at start | phase:2, area:compliance, country:uk | Current version served + recorded |
| E36 | Section 21/8 notices (configurable for Renters' Rights Bill) | phase:2, area:compliance, country:uk | Notice capture; templates versioned |
| E37 | Payment integration (Stripe/GoCardless/SEPA) + reconciliation | phase:2, area:core | Payments reconcile to ledger |
| E38 | Maintenance tickets (tenant-reportable, vendors, costs) | phase:2, area:core | Ticket lifecycle + photos + costs |
| E39 | Subscription billing for landlords (free/paid tiers) | phase:2, area:core | Plan limits enforced |

## Phase 3 — Reputation companion MVP  *(milestone: `M3`)*
| ID | Title | Labels | Acceptance (short) |
|----|-------|--------|--------------------|
| E50 | Reputation data model + attestation schemas (VC) | phase:3, area:reputation | Versioned VC schemas for tenancy attestations |
| E51 | DPIA + legal review of reputation system | phase:3, type:legal, area:reputation | DPIA signed off before launch |
| E52 | Issuance API: build attestation from tenancy data (platform-signed) | phase:3, area:reputation, lang:python | One-click issue at offboarding |
| E53 | Wallet companion (PWA): DID + hold VCs (custodial-but-exportable) | phase:3, area:reputation | Renter receives & stores VC, can export |
| E54 | Selective disclosure (SD-JWT VC) | phase:3, area:reputation | Disclose one field, not whole VC |
| E55 | Verification: request presentation + verify (in core) | phase:3, area:reputation | Landlord sees verified facts only |
| E56 | Revocation + dispute mechanism | phase:3, area:reputation | Issuer revoke; renter dispute flag |
| E57 | Issuer registry + Sybil resistance (real-tenancy binding) | phase:3, area:reputation | Only real tenancies can issue |

## Phase 4 — Privacy hardening + scale (Go)  *(milestone: `M4`)*
| ID | Title | Labels | Acceptance (short) |
|----|-------|--------|--------------------|
| E60 | Extract Verification API to **Go** behind stable contract | phase:4, area:reputation, lang:go | Parity + higher throughput |
| E61 | On-chain anchoring + revocation registry (EAS/L2), gasless | phase:4, area:reputation, lang:go | Hash/revocation anchored; users pay no gas |
| E62 | Self-custodied wallets / `did:pkh` (crypto-wallet identity) | phase:4, area:reputation | Renter can self-custody keys |
| E63 | BBS+/ZK predicate proofs ("≥N on-time payments") | phase:4, area:reputation | Predicate proven w/o revealing data |
| E64 | Proof-of-personhood (opt-in, assurance levels) | phase:4, area:reputation | Raises assurance; opt-in |
| E65 | EUDI Wallet (eIDAS 2.0) interop spike | phase:4, area:reputation, type:spike | Compatibility assessment |
| E66 | Observability, data-residency review, perf hardening | phase:4, infra | SLOs + dashboards |
| E67 | WhatsApp/SMS notifications | phase:4, area:core | Opt-in WhatsApp reminders |

---

## Dependency notes
- Phase 1 depends on Phase 0 (E02–E04).
- Reputation (Phase 3) depends on tenancy + ledger + offboarding (E19, E21) producing real data.
- Go extraction (E60) depends on the Python verification service (E55) being proven.
- Legal/DPIA (E51) **gates** the reputation launch.

## Issue-number mapping (fill in when issues are created)
| Backlog ID | GitHub Issue # |
|------------|----------------|
| E01 | #__ |
| E02 | #__ |
| ... | ... |

> When opening a PR, put `Closes #<issue>` in the description and prefix the branch with the
> phase, e.g. `phase1/E13-it-contract-generation`.
