# 01 — PRD: Core Rental Management Platform

**Status:** Draft · **Owner:** Founder/Eng · **Audience:** small landlords (IT + UK)
**Related:** [03-architecture](./03-architecture-and-services.md) · [04-compliance](./04-compliance-it-uk.md) · [05-roadmap](./05-roadmap-and-backlog.md)

This PRD covers the **web application** that manages the full tenant lifecycle:
**find/screen → onboard → manage → offboard**. It is country-aware (Italy + UK) from
the data model up.

---

## 1. Lifecycle overview

```
  ┌──────────┐   ┌───────────┐   ┌────────────┐   ┌─────────────┐   ┌────────────┐
  │ PROPERTY │ → │  FIND &   │ → │  ONBOARD   │ → │   MANAGE    │ → │  OFFBOARD  │
  │  SETUP   │   │  SCREEN   │   │ (move-in)  │   │ (tenancy)   │   │ (move-out) │
  └──────────┘   └───────────┘   └────────────┘   └─────────────┘   └────────────┘
   units, docs    applicant,      contract,        rent ledger,      notice,
   certs, photos  reputation      deposit, KYC,    maintenance,      inspection,
                  request         e-sign, keys,    messages,         deposit return,
                                  inventory        compliance        final ledger,
                                                   reminders         attestation
```

Each stage below lists **user stories**, **functional requirements (FR)**, and
**country deltas** where Italy and the UK differ.

---

## 2. Stage: Property setup

### User stories
- As a landlord I add a property and its units so everything else hangs off it.
- As a landlord I store the property's certificates/documents and get warned before they expire.

### Functional requirements
- **FR-2.1** Create *Property* (address, country, type, ownership notes) and one or more
  *Units* (a whole flat is one unit; HMO/room-by-room is a unit per room).
- **FR-2.2** Attach documents to a property/unit with a **document type** and **expiry date**.
- **FR-2.3** Country-specific certificate checklist auto-populated (see compliance deltas).
- **FR-2.4** Photo gallery per unit (used later for inventory baselines).

### Country deltas
- **🇮🇹** Track **APE** (Attestato di Prestazione Energetica) and its validity (10 yrs),
  *categoria catastale*, *rendita catastale*, condominio details, *spese condominiali*.
- **🇬🇧** Track **EPC**, **Gas Safety Certificate (CP12, annual)**, **EICR (electrical, 5-yr)**,
  smoke/CO alarm checks, and (England) selective/HMO licensing where applicable.

---

## 3. Stage: Find & screen

> We are **not** building a listings marketplace. We support the *screening* step, which
> is where the reputation companion plugs in.

### User stories
- As a landlord I record applicants for a unit and compare them.
- As a landlord I request a **reputation proof** from an applicant (see PRD 02) instead of
  (or in addition to) demanding a guarantor and pay slips.
- As a renter I respond to a reputation request by sharing a selective proof from my wallet.

### Functional requirements
- **FR-3.1** Create *Applications* against a unit; capture contact + status
  (new → screening → approved/rejected → converted to tenancy).
- **FR-3.2** "Request reputation" action generates a link/QR the applicant opens in their
  wallet companion; the landlord sees a **verification result** (verified ✓ / not provided),
  never raw personal data unless the renter discloses it.
- **FR-3.3** Capture standard screening artifacts where the renter chooses to share them
  (employment ref, income proof, guarantor) — stored encrypted, with retention limits.
- **FR-3.4** Anti-discrimination guardrails: no fields for protected characteristics; the
  product nudges toward objective criteria (payment history, references) and away from
  informal/exclusionary signals.

### Country deltas
- **🇮🇹** *Garante* (guarantor) and *codice fiscale* capture; reputation proof is positioned
  as a privacy-preserving alternative to the heavy informal vetting common in Italy.
- **🇬🇧** **Right to Rent** immigration check is a *legal requirement* — we provide a guided
  checklist + evidence capture (we record that the check was performed and store the
  evidence; we are not an IDVT provider in MVP).

---

## 4. Stage: Onboard (move-in)

The highest-value, most error-prone stage. This is where compliance failures cost money.

### User stories
- As a landlord I generate a correct, country-appropriate contract and get it signed.
- As a landlord I handle the deposit correctly (protect/register it) and never miss the deadline.
- As a renter I sign electronically and receive my copy + my legally-required documents.

### Functional requirements
- **FR-4.1** **Tenancy** entity links unit + tenant(s) + dates + rent + deposit + contract type.
- **FR-4.2** **Contract generation** from country/region templates with merge fields; output PDF.
- **FR-4.3** **E-signature** flow (in-house simple e-sign for MVP; pluggable provider later).
  Capture signer identity, timestamp, IP, document hash → tamper-evident audit record.
- **FR-4.4** **Deposit handling workflow** with a country-specific checklist and a hard deadline
  reminder (see deltas). Record deposit amount, method, protection/registration reference.
- **FR-4.5** **Inventory / check-in report**: itemized condition + photos, tenant acknowledges.
- **FR-4.6** **Move-in packet**: contract copy + mandatory documents delivered to tenant, with
  proof of delivery (the renter must receive specific docs by law — see deltas).
- **FR-4.7** Keys/handover checklist.

### Country deltas
- **🇮🇹**
  - **Contract type selector**: *4+4 (libero)*, *3+2 (canale concordato)*, *transitorio
    (1–18 mo)*, *studenti (6–36 mo)*. Each drives template + tax options.
  - **Contract registration** with Agenzia delle Entrate (**RLI** model) within **30 days**:
    guided checklist, store registration number/date. (MVP: guide + reminder + document
    upload; *future*: assisted/automated filing.)
  - **Cedolare secca** decision support (flat tax **21%**, or **10%** for concordato) vs
    ordinary regime; record the election.
  - **Deposito cauzionale**: max **3 months'** rent; (some contracts require interest on it).
  - **Imposta di registro / imposta di bollo** tracking (F24 / F24 ELIDE).
- **🇬🇧**
  - **AST** (England/Wales) template; **PRT** for Scotland (different regime — flag, see compliance).
  - **Tenancy Deposit Protection**: deposit must be protected in a government scheme
    (**DPS / MyDeposits / TDS**) and **prescribed information** served within **30 days**.
    Hard-deadline reminder; store scheme + reference. **Deposit cap: 5 weeks' rent** (annual
    rent < £50k). MVP integrates *guidance + reminders*; scheme API integration is a later issue.
  - **Mandatory documents to tenant**: **How to Rent** guide (current version), **EPC**,
    **Gas Safety Certificate**, **EICR** — serving these is a precondition for a valid
    Section 21; we track that each was served and when.

> ⚠️ **Compliance reminders are the killer feature of this stage.** See PRD 02-independent
> "Compliance & deadlines engine" below.

---

## 5. Stage: Manage (during tenancy)

### User stories
- As a landlord I track rent due/paid and instantly see arrears.
- As a landlord I log maintenance requests and their resolution.
- As a landlord I keep all communication with the tenant in one auditable place.
- As a landlord I never miss a recurring compliance task (gas safety renewal, etc.).

### Functional requirements
- **FR-5.1** **Rent ledger**: scheduled charges (rent, condo fees), recorded payments,
  running balance, arrears highlighting, receipts. Multi-currency (**EUR**, **GBP**).
- **FR-5.2** **Payment integration** (later phase): reconcile via Stripe / GoCardless /
  SEPA direct debit / open-banking; MVP supports *manual* payment recording + reminders.
- **FR-5.3** **Maintenance tickets**: tenant-reportable, status, photos, costs, vendor notes.
- **FR-5.4** **Messaging / activity log**: timestamped, exportable thread per tenancy
  (so disputes have a paper trail). Email/notification fan-out.
- **FR-5.5** **Compliance & deadlines engine** (cross-cutting): a unified queue of upcoming
  obligations per property/tenancy (cert renewals, contract registration anniversaries,
  rent reviews, deposit deadlines) with reminders and a "mark done" audit trail.
- **FR-5.6** **Rent increase / review** support per country rules (e.g. ISTAT index for IT
  *concordato*; UK Section 13 / rent review clauses).
- **FR-5.7** **Documents vault** per tenancy with versioning.

### Country deltas
- **🇮🇹** Annual contract tax renewals (if not cedolare); ISTAT rent adjustment helper;
  *spese condominiali* split between landlord/tenant.
- **🇬🇧** Annual **Gas Safety** renewal reminder; periodic **EICR**; council-tax responsibility tracking.

---

## 6. Stage: Offboard (move-out)

### User stories
- As a landlord I serve/record notice correctly and run a structured move-out.
- As a landlord I compare check-in vs check-out condition and compute deposit deductions fairly.
- As a landlord I close the ledger, return the deposit, and **issue a reputation attestation**
  about the tenant.
- As a renter I receive a fair deposit return and **earn a portable attestation** I keep in my wallet.

### Functional requirements
- **FR-6.1** **Notice management**: record notice type, dates, grounds; country-specific validity hints.
- **FR-6.2** **Check-out inspection** referencing the check-in inventory; diff + photos.
- **FR-6.3** **Deposit settlement**: itemized deductions, dispute notes, return workflow; for UK,
  link to scheme's dispute process; for IT, deposit + any due interest return.
- **FR-6.4** **Final ledger reconciliation** and statement.
- **FR-6.5** **Attestation issuance** → the landlord issues a signed reputation credential
  about the tenancy (on-time payment record, property condition, would-rent-again). This is
  the hand-off into PRD 02. Issuing is **one click** at successful offboarding (the moment of
  highest goodwill and best data).
- **FR-6.6** **Archive** the tenancy with full document/audit retention per legal minimums,
  then GDPR-aligned deletion schedule.

### Country deltas
- **🇮🇹** *Disdetta*/recesso rules per contract type; registration of contract termination
  (*risoluzione*) at Agenzia delle Entrate; deposit + interest return.
- **🇬🇧** Section 21 (being reformed by the **Renters' Rights Bill** — keep template logic
  configurable) / Section 8 grounds; deposit scheme dispute path; PRT notice for Scotland.

---

## 7. Cross-cutting requirements

### 7.1 Identity, accounts, roles
- **FR-7.1** Landlord account (email/password + MFA), optional additional users later.
- **FR-7.2** Tenant lightweight account (magic link) to view their tenancy, documents,
  ledger, and to respond to reputation requests.
- **FR-7.3** Country/locale on the **tenancy**, not just the account (a landlord may own in both).

### 7.2 Internationalization & localization
- **FR-7.4** UI languages: **Italian** and **English** at launch.
- **FR-7.5** Locale-aware dates, currency (EUR/GBP), addresses, tax IDs (*codice fiscale* / UK).
- **FR-7.6** Legal templates and checklists are **versioned by country/region and date**
  (law changes; we must reproduce the rules that applied when a contract was made).

### 7.3 Documents & e-signature
- **FR-7.7** All generated docs are PDFs with a stored **content hash**; signatures and
  document-served events are tamper-evident and exportable as an evidence pack.

### 7.4 Notifications
- **FR-7.8** Email at MVP; in-app notification center; (later) WhatsApp/SMS for reminders,
  since landlords/tenants in IT live on WhatsApp.

### 7.5 Privacy, security, compliance (GDPR)
- **FR-7.9** GDPR is first-class: lawful basis per data category, **data-retention schedules**,
  **right to erasure** (with legal-hold exceptions), **data export**, audit log of access.
- **FR-7.10** PII encrypted at rest; least-privilege; full audit trail on sensitive actions.
- **FR-7.11** **Records of Processing** and a clear separation between *core platform* PII and
  the *reputation* system (which is designed to minimize PII — see PRD 02).

### 7.6 Auditability
- **FR-7.12** Every legally-significant action (sign, serve, protect deposit, register, issue
  attestation, deposit deduction) writes an immutable audit event.

---

## 8. Non-functional requirements
- Web-first, responsive (landlords on desktop, tenants on mobile).
- Single region per country data residency in EU (Italy/UK both served from EU region to
  keep GDPR simple; revisit UK adequacy as needed).
- p95 page load < 1.5s for core screens; reminders job reliability is the real SLO.
- Backups + point-in-time recovery for the ledger and audit log.

## 9. Out of scope (this PRD)
- Listings/marketplace search, accounting/bookkeeping export beyond CSV (later), mobile
  native apps (PWA first), agency multi-tenant org structures (scale-up), automated
  tax filing (assisted later).

## 10. Open questions
- Do we file Italian contract registration *for* the landlord (regulated, complex) or only
  guide+remind in v1? → **Guide+remind in v1.**
- In-house e-sign vs. eIDAS-qualified provider for legal weight? → simple e-sign MVP, pluggable
  qualified provider when a customer needs it.
- UK deposit scheme **API** integration timing (custodial vs insured)? → reminders first, API later.
