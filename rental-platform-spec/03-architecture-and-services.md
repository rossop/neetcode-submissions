# 03 — Architecture, Services & Build Order

**Related:** [01-core](./01-prd-core-platform.md) · [02-reputation](./02-prd-reputation-companion.md) · [05-roadmap](./05-roadmap-and-backlog.md)

This document decomposes the product into services, fixes the technology choices
(**Python now, Go later**), and — most importantly — answers **what to build first and why**.

---

## 1. Architectural stance

> **Start as a modular monolith, not microservices.** Extract services only when a clear
> seam (different scaling profile, different language, different team) justifies it.

A small team shipping an MVP should not pay the microservices tax (deploys, networking,
observability, data consistency across services) on day one. We build a **single Python
(FastAPI) application** organized into clean internal modules ("services") that map to the
domains below. When a module genuinely needs Go (concurrency, crypto throughput) or
independent scaling (the verification API, notification workers), we extract it.

```
                      ┌──────────────────────────────────────────────┐
   Landlord (web) ───▶│           CORE PLATFORM (Python/FastAPI)       │
   Tenant (web/PWA) ─▶│  modular monolith                              │
                      │  ┌────────┬──────────┬──────────┬───────────┐ │
                      │  │ Auth & │ Property  │ Tenancy  │ Documents │ │
                      │  │ Org    │ & Units   │ Lifecycle│ & E-sign  │ │
                      │  ├────────┼──────────┼──────────┼───────────┤ │
                      │  │ Ledger │ Maint.    │ Messaging│ Compliance│ │
                      │  │/Billing│ /Tickets  │ /Notify  │ /Deadlines│ │
                      │  └────────┴──────────┴──────────┴───────────┘ │
                      └───────────────┬───────────────────────────────┘
                                      │  (issue/verify attestations)
                      ┌───────────────▼───────────────────────────────┐
                      │   REPUTATION SERVICES                          │
                      │   ┌─────────────────────┐  ┌────────────────┐ │
   Renter wallet ────▶│   │ Issuance API (Py)   │  │ Verification   │ │
   (PWA / wallet) ───▶│   │ from tenancy data   │  │ API (Go, later)│ │
                      │   └─────────────────────┘  └────────────────┘ │
                      │   Wallet companion (web/PWA) + optional anchor │
                      └────────────────────────────────────────────────┘

   Shared infra: PostgreSQL · Redis (cache/queue) · Object storage (S3-compatible) ·
                 Background workers · Email provider · (later) payments + on-chain anchor
```

---

## 2. Technology choices

| Concern | Choice | Why |
|---------|--------|-----|
| Core web API | **Python + FastAPI** | Team is fluent → fastest path to value. Great typing, async, OpenAPI, ecosystem. |
| ORM / migrations | **SQLAlchemy + Alembic** | Mature, explicit migrations (critical for a ledger). |
| DB | **PostgreSQL** | Relational integrity for tenancies/ledger; JSONB for flexible doc metadata. |
| Cache / queue | **Redis** (+ a task runner, e.g. RQ/Celery/Arq) | Reminders, async jobs, rate limits. |
| Object storage | **S3-compatible** | Documents, photos, generated PDFs. |
| Frontend | **PWA** (React/Svelte) | Web-first; mobile via PWA; tenant flows are mobile-heavy. |
| Auth | Sessions/JWT + MFA; magic links for tenants | Low friction for tenants, secure for landlords. |
| E-sign (MVP) | In-house simple e-sign (hash + audit) | Good enough for ASTs/most IT contracts; pluggable qualified provider later. |
| **Reputation verification** | **Go** (later) | Concurrency + strong crypto libs for VC/DID/ZK verification throughput; a deliberate Go learning target on a well-bounded service. |
| Credentials | **W3C VC / DID, SD-JWT VC** | Portable, GDPR-aligned, EUDI-wallet-friendly. |
| Optional anchoring | **EAS on an L2** | Hashes/revocation only, gasless for users. |
| Deploy | Containers on a simple PaaS/VM first | Don't over-engineer infra pre-PMF. |

### Why Python first, Go later (the learning path)
- **Now:** velocity matters more than performance. The team writes Python well; the core
  platform is CRUD + workflow + integrations, where Python shines.
- **Later:** the **verification API** and **notification/anchoring workers** are
  concurrency- and crypto-heavy, latency-sensitive, and *well-bounded* — an ideal, low-risk
  place to learn Go without betting the core product on it. Extract behind a stable API.

---

## 3. Service catalog

| # | Service / module | Responsibility | Lang | Phase |
|---|------------------|----------------|------|-------|
| S1 | **Auth & Org** | Accounts, MFA, tenant magic-link, roles, audit log | Py | 0 |
| S2 | **Property & Units** | Properties, units, certificates, photos | Py | 1 |
| S3 | **Tenancy Lifecycle** | Applications, tenancies, contract gen, move-in/out, inventory | Py | 1 |
| S4 | **Documents & E-sign** | PDF generation, e-signature, document vault, hashing | Py | 1 |
| S5 | **Ledger & Billing** | Rent schedule, payments, arrears, statements; our own subscription billing | Py | 1 (manual) → 2 (integrations) |
| S6 | **Compliance & Deadlines** | Country rule sets, obligation queue, reminders, "mark done" audit | Py | 1 |
| S7 | **Maintenance** | Tickets, vendors, costs, photos | Py | 1/2 |
| S8 | **Messaging & Notifications** | Per-tenancy thread, email/in-app, (later) WhatsApp/SMS | Py | 1 (email) → later |
| S9 | **Reputation Issuance** | Build/sign attestations from tenancy data; deliver to wallet | Py | 3 |
| S10 | **Reputation Verification** | Verify VPs/VCs, check revocation/anchors, ZK predicates | **Go** | 3/4 |
| S11 | **Wallet Companion** | Renter PWA/app: DID, hold VCs, build presentations | Py/TS + crypto | 3 |
| S12 | **Anchoring & Revocation** | On-chain hash/revocation registry (EAS/L2), gas sponsorship | Go | 4 |
| S13 | **Country Rule Packs** | Versioned IT/UK templates, checklists, tax params (data, not a service) | data | 1 (IT), 2 (UK) |

---

## 4. Data model (core entities)

```
Org/Landlord ─┬─< Property ─< Unit ─< Tenancy ─┬─< TenancyParty (tenant/guarantor)
              │                                  ├─< RentCharge ─< Payment
              │                                  ├─< Document (typed, hashed, expiry)
              │                                  ├─< InventoryItem (check-in/out)
              │                                  ├─< MaintenanceTicket
              │                                  ├─< Message / ActivityEvent
              │                                  └─< Attestation (→ Reputation)
              └─< ComplianceObligation (per property/tenancy, country-driven)
AuditEvent (append-only, references any entity)
```

Key decisions:
- **Country/locale lives on the Tenancy** (a landlord can own in both IT and UK).
- **Ledger is append-only-ish** (corrections are entries, not edits) for trust + audit.
- **Documents store a content hash**; signature/served events are immutable audit records.
- **Reputation PII is minimized and separated** from on-chain anchors (see PRD 02 §6).

---

## 5. Build order (what to build first — and why)

> Principle: **ship the smallest thing that delivers real landlord value and creates the data
> the reputation network later depends on.** Sequence by *value ÷ risk*, and respect the
> network-effect dependency (reputation needs landlord supply first).

### Phase 0 — Foundations *(weeks 0–2)*
**Build:** private repo, CI, FastAPI skeleton, Postgres + migrations, **S1 Auth & Org**,
audit-log primitive, deploy pipeline, base PWA shell, i18n scaffold (IT/EN).
**Why first:** everything hangs off identity, data model, and a working deploy. Cheap, unblocks all.

### Phase 1 — Core MVP, **Italy first** *(the revenue wedge)*
**Build:** S2 Property/Units, S3 Tenancy Lifecycle (IT contract types + generation + simple
e-sign S4), **S6 Compliance & Deadlines** (IT rule pack S13: registration 30-day reminder,
APE, cedolare election), **S5 Ledger** (manual payment recording + arrears), basic S8 email
notifications, move-in/inventory + move-out.
**Why this, why Italy:**
- The **onboarding + compliance + ledger** loop is where small landlords feel the most pain and
  legal risk → highest willingness to adopt/pay.
- **Italy first** because (a) the *trust gap* (our wedge into reputation later) is most acute in
  Italy, (b) contract-registration + cedolare pain is concrete and unaddressed by simple tools,
  and (c) it focuses the team on one rule pack before generalizing.
- **Compliance & deadlines is the "killer feature"** — it's what stops a landlord getting fined,
  so it earns trust and retention.

### Phase 2 — **UK support** + payments
**Build:** S13 UK rule pack (AST, deposit-protection reminders + prescribed info, Right-to-Rent
checklist, EPC/gas/EICR + How-to-Rent serving), Scotland PRT flag, S5 payment integrations
(Stripe/GoCardless/SEPA reconciliation), maintenance S7.
**Why second:** UK is a large, English-language market that validates the *multi-country* data
model we already designed for; do it once Italy proves the loop. Payments reduce manual work and
unlock subscription revenue.

### Phase 3 — **Reputation companion MVP**
**Build:** S9 Issuance (platform-signed attestations from tenancy data, one-click at offboarding),
S11 custodial-but-exportable wallet (DID + hold VCs), S10 Verification (request/verify presentation,
SD-JWT selective disclosure). No public chain yet.
**Why now (not earlier):** the reputation network is a **two-sided market**; it is worthless
without **issuers and real tenancy data**, which Phases 1–2 produce. The best attestation moment
(offboarding) only exists once landlords run full tenancies on us. Building reputation first would
be a cold-start failure.

### Phase 4 — **Privacy hardening + scale (Go)**
**Build:** self-custodied wallets / `did:pkh`, **S12 anchoring + revocation** (EAS/L2, gasless),
BBS+/ZK predicate proofs, EUDI-wallet interop, proof-of-personhood, extract **S10 Verification to
Go** for throughput. Observability, data-residency review, performance.
**Why last:** these increase trust/scale but aren't needed to validate the product; Go extraction
is safest once the service boundary and behavior are proven in Python.

```
Phase 0  Foundations            ▓▓
Phase 1  Core MVP (IT)            ▓▓▓▓▓▓▓▓   ← revenue wedge + data for reputation
Phase 2  UK + payments                  ▓▓▓▓▓▓
Phase 3  Reputation MVP                       ▓▓▓▓▓▓   ← needs Phase 1–2 supply
Phase 4  Privacy/scale (Go)                         ▓▓▓▓▓
```

### One-line justification of the order
**Foundations → make landlords successful & compliant (IT, then UK) → harvest that trust and data
into a renter reputation network → harden privacy and scale with Go where it pays off.**

---

## 6. Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Legal/tax rules wrong → landlord harmed | Versioned rule packs, disclaimers, links to official sources, legal review before each country launch. |
| Reputation cold-start | Don't build it first; seed from Phase 1–2 tenancies; make issuing one click at offboarding. |
| GDPR vs. blockchain immutability | No PII on-chain — hashes/commitments + off-chain VCs only; DPIA before launch. |
| Over-engineering infra pre-PMF | Modular monolith; extract to Go services only when justified. |
| Defamation / unfair attestations | Structured factual claims only; dispute + revocation; no protected fields. |
| Go learning slows delivery | Confine Go to bounded, non-critical-path services (verification/anchoring) behind stable APIs. |
