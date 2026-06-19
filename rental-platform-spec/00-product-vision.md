# 00 — Product Vision

## 1. Vision statement

> Give small landlords in Italy and the UK a single tool that runs the entire tenant
> lifecycle correctly — including the country-specific legal, tax, and safety steps —
> and give renters a portable, privacy-preserving reputation they own, so trust
> between strangers stops being the bottleneck to renting.

## 2. The problem

### Landlord side
- Small landlords (1–10 units) manage tenancies in their heads, in spreadsheets, and
  over chat. They miss compliance deadlines (energy certs, gas safety, contract
  registration), mishandle deposits, and have weak paper trails when disputes happen.
- In **Italy**, the contract must be *registered* with the Agenzia delle Entrate, taxes
  paid (registration tax or *cedolare secca*), and the right contract type chosen
  (4+4, 3+2 concordato, transitorio, students). Getting this wrong is expensive.
- In the **UK**, deposits must be protected in a government-backed scheme within 30 days,
  Right to Rent checks are mandatory, and a stack of certificates (EPC, gas, electrical)
  must be served — or the landlord loses the ability to evict and faces fines.

### Renter side
- Renters have **no portable reputation**. A great tenant of 6 years starts from zero
  with every new landlord.
- In **Italy** specifically, landlords *distrust* renters and over-rely on informal
  signals (referrals, "knowing the family", guarantors), which is slow, exclusionary,
  and discriminatory.
- Existing "tenant screening" is a centralized credit-bureau model: a privacy honeypot
  that renters rightly distrust and that is hard to square with GDPR.

## 3. Our bet

1. **Win small landlords with a country-correct lifecycle tool** (the boring, valuable part).
2. **Use that landlord supply to bootstrap a renter reputation network** where:
   - The renter holds their reputation in a **self-custodied wallet** (pseudonymous).
   - Landlords issue **signed attestations** ("paid on time for 18 months", "left the
     property in good condition") as **verifiable credentials**.
   - Renters **selectively disclose** proofs to prospective landlords — eventually with
     **zero-knowledge proofs** so they can prove "no missed payments in 2 years" without
     revealing who they are or which landlord said so.
3. Keep **personal data off public ledgers** (GDPR-first). The "crypto wallet" is for
   *key custody, pseudonymity, and portability* — not for storing personal data on-chain.

## 4. Personas

| Persona | Description | Primary jobs-to-be-done |
|---------|-------------|--------------------------|
| **Giulia — Italian small landlord** | Owns 2 flats in Bologna, rents to students/young professionals. Not a tax expert. | Pick the right contract, register it, track rent, get a trustworthy tenant, avoid fines. |
| **Tom — UK accidental landlord** | Inherited / moved-in-together and now rents out one flat in Manchester. | Stay legal (deposit protection, certs, Right to Rent), collect rent, handle repairs. |
| **Marco — prospective renter (IT)** | Young professional, good payment history, keeps being asked for a guarantor. | Prove he's a reliable tenant *without* over-sharing personal data. |
| **Aisha — prospective renter (UK)** | Moving cities, strong references from past landlords. | Carry her good reputation to a new city/landlord quickly. |
| **(Later) Agency / portfolio landlord** | 10–50 units, maybe a small letting agency. | Everything above at scale, multi-user, reporting. |

We **start with Giulia and Tom** (small landlords) and **Marco/Aisha** (renters in the
reputation network). Agencies are a *scale-up* persona, not an MVP target.

## 5. Scope guardrails (what we are NOT doing first)

- ❌ Not a property *listing/marketplace* (no competing with Idealista / Rightmove on search).
- ❌ Not a payments processor — we *integrate* (Stripe/GoCardless/SEPA) rather than hold funds.
- ❌ Not building our own blockchain. We use existing standards (W3C VCs, DIDs, optionally EAS).
- ❌ Not enterprise multi-region scale on day one. Single-region, two countries.
- ❌ Not legal advice. We encode *checklists and deadlines*, with disclaimers and links to
  official sources; we are not a substitute for a commercialista / solicitor.

## 6. Positioning

- **vs. spreadsheets/WhatsApp**: structure, deadlines that don't get missed, an audit trail.
- **vs. enterprise PM suites (e.g. agency software)**: cheaper, self-serve, country-correct,
  no training needed.
- **vs. tenant-screening bureaus**: renter-owned, privacy-preserving, portable, GDPR-native.

## 7. Success metrics (north stars)

| Phase | Metric | Target signal |
|-------|--------|---------------|
| Core MVP | Activated landlords (≥1 active tenancy fully set up) | 50 landlords, IT |
| Core MVP | Compliance deadlines surfaced & acted on | >80% of due items actioned before deadline |
| Reputation | Attestations issued per active tenancy | ≥1 at offboarding |
| Reputation | Reputation shares requested by *new* landlords | network effect proof |
| Scale | Paid conversion of active landlords | pricing validation |

## 8. Business model (directional, not a commitment)

- **Free tier**: 1 unit, core lifecycle.
- **Paid tier (per landlord, flat or per-unit)**: multiple units, e-signature volume,
  compliance reminders, document storage, reputation requests.
- **Reputation**: issuing attestations is free (we *want* supply); *verifying/requesting*
  a reputation proof during screening is a paid landlord action or part of the paid tier.
- Renters are **never** charged and **always** control disclosure.
