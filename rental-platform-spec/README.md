# Rental Platform — Product Specification

> A rental management platform for **small landlords** in **Italy 🇮🇹** and the **UK 🇬🇧**,
> plus a privacy-preserving **renter reputation companion** built on self-custodied
> wallets and verifiable credentials.

This directory holds the product requirement documents (PRDs), architecture, and
delivery plan. It is the source of truth for *what* we are building and *why*, and
the *order* in which to build it.

## Why this exists

Small landlords (1–10 units) are underserved. Existing tools are either:

- **Spreadsheets + WhatsApp + email** — no structure, deadlines missed, deposits
  mishandled, compliance documents expire silently; or
- **Enterprise property-management suites** — priced and designed for agencies
  managing hundreds of units, with steep onboarding.

We sit in the middle: opinionated, country-aware (IT + UK), and cheap to start.

The wedge is the **full tenant lifecycle**: *find/screen → onboard → manage →
offboard*, with the country-specific legal and tax steps baked in so a non-expert
landlord cannot accidentally break the law.

The differentiator is the **reputation companion**: in Italy especially, landlords
distrust tenants and have almost no portable way to check a prospective renter's
track record. We give renters a **self-custodied reputation** (they own it, it is
portable, it is privacy-preserving) and give landlords a way to request and verify
it — without building yet another centralized credit-bureau honeypot.

## Document index

| # | Document | What it covers |
|---|----------|----------------|
| — | [README.md](./README.md) | This overview + index |
| 00 | [00-product-vision.md](./00-product-vision.md) | Vision, personas, market, positioning, success metrics |
| 01 | [01-prd-core-platform.md](./01-prd-core-platform.md) | **Core PRD** — the rental management web app, full tenant lifecycle |
| 02 | [02-prd-reputation-companion.md](./02-prd-reputation-companion.md) | **Reputation PRD** — wallet-based renter reviews & verifiable credentials |
| 03 | [03-architecture-and-services.md](./03-architecture-and-services.md) | Service decomposition, tech choices (Python now, Go later), **what to build first & why** |
| 04 | [04-compliance-it-uk.md](./04-compliance-it-uk.md) | Italian + UK legal/tax/compliance requirements that shape the product |
| 05 | [05-roadmap-and-backlog.md](./05-roadmap-and-backlog.md) | Phased roadmap + feature backlog mapped to GitHub issues |

## TL;DR — what to build first

1. **Phase 0 — Foundations**: repo, auth, multi-country tenancy data model, deploy pipeline.
2. **Phase 1 — Core MVP (Italy first)**: properties, tenancies, documents, rent ledger,
   maintenance, compliance-deadline reminders. This is the revenue wedge.
3. **Phase 2 — UK support**: AST, deposit-protection scheme integration, Right to Rent.
4. **Phase 3 — Reputation companion (MVP)**: landlord-issued attestations, renter wallet,
   shareable reputation. Built once we have landlords using the core product (it needs supply).
5. **Phase 4 — Privacy hardening + scale**: zero-knowledge selective disclosure, Go services
   for the high-throughput verification/notification paths.

Rationale lives in [03-architecture-and-services.md](./03-architecture-and-services.md#build-order).

## Working conventions

- **Repository is private.**
- **Every feature is a GitHub Issue.** PRs reference the issue number in the title/body
  (e.g. `Closes #42`). The backlog in [05-roadmap-and-backlog.md](./05-roadmap-and-backlog.md)
  is the canonical list and maps 1:1 to issues.
- Stack: **Python (FastAPI) first** because the team is fluent; **Go later** for the
  concurrency- and crypto-heavy reputation/verification services (a deliberate learning path).
