# 04 — Compliance: Italy 🇮🇹 & UK 🇬🇧

**Related:** [01-core-platform](./01-prd-core-platform.md) · [03-architecture](./03-architecture-and-services.md)

This is the domain knowledge that **shapes the product**. The platform encodes these as
**versioned rule packs** (templates, checklists, deadlines, tax parameters). It is *not legal
advice* — every flow links to official sources and shows disclaimers. **A qualified legal/tax
review is required before each country launch and whenever rules change.**

> ⚠️ Rules and figures below are a *product-modeling reference* as understood at spec time
> (2026). Treat amounts, percentages, and deadlines as parameters to be confirmed with a
> *commercialista* (IT) / solicitor (UK), not as authoritative legal values.

---

## 1. Italy 🇮🇹

### 1.1 Contract types (drives templates + tax)
| Type | Typical duration | Notes |
|------|------------------|-------|
| **4+4 (libero)** | 4 yrs + 4 yrs renewal | Free-market rent. |
| **3+2 (canale concordato)** | 3 yrs + 2 yrs | Rent within local agreement bands; **tax incentives** (cedolare 10%). |
| **Transitorio** | 1–18 months | Requires a documented transitory need. |
| **Studenti** (universitari) | 6–36 months | For university students in qualifying areas. |

→ Product: contract-type selector that drives the template, allowed durations, and tax options.

### 1.2 Registration (registrazione del contratto)
- Must be **registered with the Agenzia delle Entrate**, generally **within 30 days** of signing,
  via the **RLI** model (online).
- Store: registration number, date, office, and the F24/payment reference.
- **Product (v1):** guided checklist + **hard 30-day reminder** + document upload. *Assisted/automated
  filing is a later feature* (regulated, complex).

### 1.3 Taxation
- **Cedolare secca** (optional flat tax in place of IRPEF + registration/stamp tax):
  **21%** standard, **10%** for *canale concordato*. Electing it usually freezes rent updates.
- Otherwise **ordinary regime**: **imposta di registro** (~2% of annual rent, split landlord/tenant)
  + **imposta di bollo**, paid via **F24 ELIDE**, with annual renewals.
- → Product: **cedolare vs ordinary decision support**, record the election, schedule annual tax
  reminders if ordinary.

### 1.4 Deposit & money
- **Deposito cauzionale**: commonly **up to 3 months'** rent; may require **interest** to the tenant.
- → Product: cap validation, deposit tracking, interest reminder at return.

### 1.5 Documents & parties
- **Codice fiscale** for all parties; optional **garante** (guarantor).
- **APE** (energy performance certificate) — required, ~10-yr validity → tracked with expiry.
- *Spese condominiali* split (some on tenant, some on landlord).

### 1.6 Other obligations
- **Comunicazione** for certain tenants/short stays (e.g. *cessione di fabbricato* / hospitality
  reporting, *Portale Alloggiati* for short-term) — flag where relevant.
- **TARI** (waste tax) responsibility.
- Termination (*disdetta*/*risoluzione*) rules per contract type; registration of termination.

### 1.7 Italy product checklist (what we encode)
- [ ] Contract-type-aware template + allowed duration
- [ ] 30-day **registration reminder** + storage of registration data
- [ ] Cedolare vs ordinary election + (if ordinary) annual tax reminders
- [ ] Deposit cap (≤3 months) + interest-at-return reminder
- [ ] Codice fiscale capture; optional garante
- [ ] APE on file with expiry reminder
- [ ] ISTAT rent-update helper (where applicable)
- [ ] Termination + termination-registration flow

---

## 2. United Kingdom 🇬🇧

> England & Wales use **Assured Shorthold Tenancies (AST)**. **Scotland** uses the
> **Private Residential Tenancy (PRT)** — a *different regime* (no fixed term, different notices,
> rent-control areas). Northern Ireland differs again. **MVP targets England/Wales AST**, with a
> **Scotland flag** and PRT support as a later rule-pack issue.

### 2.1 Tenancy & deposit
- **AST** is the default residential tenancy (England/Wales).
- **Tenancy deposit protection:** the deposit **must** be protected in a government-approved scheme
  (**DPS**, **MyDeposits**, **TDS**) and the **prescribed information** served to the tenant
  **within 30 days**. Failure → can't use Section 21 + penalties of 1–3× the deposit.
- **Deposit cap (Tenant Fees Act 2019):** **5 weeks' rent** (annual rent < £50k), **6 weeks'**
  (≥ £50k). Most letting fees to tenants are **banned**.
- → Product: **hard 30-day deposit-protection reminder**, scheme + reference capture, prescribed-info
  served tracking, deposit-cap validation. (Scheme **API** integration is a later issue; reminders first.)

### 2.2 Right to Rent (immigration check)
- Landlords in England must verify a tenant's **right to rent** before the tenancy and record
  evidence; failure is an offence.
- → Product: guided **Right to Rent checklist** + evidence capture + recheck reminders for
  time-limited statuses. (We record that the check was done; we're not an IDVT provider in MVP.)

### 2.3 Mandatory safety & documents (preconditions for Section 21)
| Item | Cadence |
|------|---------|
| **EPC** (Energy Performance Certificate) | Provided to tenant; min rating rules apply |
| **Gas Safety Certificate (CP12)** | **Annual**; serve to tenant |
| **EICR** (electrical installation) | Every **5 years** |
| **Smoke & CO alarms** | Working at start of tenancy / per regs |
| **How to Rent guide** | Current version served at start |
- → Product: track each cert with expiry/renewal reminders + **"served to tenant" evidence**, since
  serving these is a precondition for a valid Section 21 notice.

### 2.4 Ending a tenancy
- **Section 21** ("no-fault") and **Section 8** (grounds). The **Renters' Rights Bill** is reforming
  this (e.g. abolishing Section 21, periodic tenancies) → **keep notice/template logic configurable
  and versioned** so we can switch when it commences.
- → Product: notice type/grounds capture, validity hints, configurable templates.

### 2.5 Licensing & council tax
- **Selective / HMO licensing** varies by council (HMOs especially) → flag where the property may
  need a licence.
- **Council tax** responsibility tracking.

### 2.6 UK product checklist (what we encode)
- [ ] AST template (E&W); **Scotland PRT flag** (later: full PRT pack)
- [ ] **Deposit protection 30-day reminder** + scheme/reference + prescribed-info served
- [ ] Deposit-cap validation (5/6 weeks)
- [ ] **Right to Rent** checklist + evidence + recheck reminders
- [ ] EPC / Gas (annual) / EICR (5-yr) / alarms tracking + **served** evidence
- [ ] How to Rent (current version) served at start
- [ ] Section 21/8 notice support, **configurable for Renters' Rights Bill**
- [ ] HMO/selective licensing flag; council-tax responsibility

---

## 3. Cross-country: GDPR & data protection
- Lawful basis per data category; **retention schedules** (keep tenancy/tax records for legal
  minimums, then delete); **right to erasure** with legal-hold exceptions; **data export**.
- **DPIA** required before the reputation network launches (PRD 02 §6).
- Records of Processing Activities; encryption at rest; access audit log.
- Keep **reputation PII off any public ledger** — hashes/commitments only.

## 4. How compliance is implemented in the product
- **Rule packs are versioned data** (`country` × `region` × `effective_date`) so a tenancy is
  always governed by the rules in force when it was created.
- The **Compliance & Deadlines engine** (S6) turns rule packs into a per-property/tenancy
  **obligation queue** with reminders and a **"mark done" audit trail**.
- Every legally significant action emits an **immutable audit event** (PRD 01 §7.6).
- Every flow shows a **"not legal advice"** disclaimer and links to the official source
  (Agenzia delle Entrate, GOV.UK, deposit schemes, etc.).
