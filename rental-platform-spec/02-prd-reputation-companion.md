# 02 — PRD: Renter Reputation Companion

**Status:** Draft · **Audience:** renters (credential holders) + landlords (issuers/verifiers)
**Related:** [01-core-platform](./01-prd-core-platform.md) · [03-architecture](./03-architecture-and-services.md) · [04-compliance](./04-compliance-it-uk.md)

A privacy-preserving system that lets renters **own a portable reputation** and lets
landlords **request and verify** it — without a centralized credit-bureau honeypot.
The "crypto wallet" provides **self-custody of keys, pseudonymity, and portability**, not
on-chain storage of personal data.

---

## 1. The trust problem we are solving

- In Italy, landlords distrust renters and fall back on informal, slow, exclusionary
  vetting (guarantors, "who do you know"). Renters with a genuinely good history can't prove it.
- A renter who paid on time for 6 years restarts at zero with each new landlord.
- The obvious "fix" — a central tenant credit bureau — is a privacy nightmare, distrusted
  by renters, hard under GDPR, and a single point of failure/abuse.

**Our approach:** the renter holds **verifiable credentials (VCs)** issued by past landlords
(and the platform) in a **self-custodied wallet**. They choose what to disclose, to whom,
and (eventually) can prove facts in **zero knowledge** ("no missed payments in 24 months")
without revealing identity or which landlord attested it.

---

## 2. Design principles

1. **Renter-owned & portable.** The renter, not us, holds the credentials. Works even if our
   platform disappears (standards-based).
2. **Data minimization / GDPR-first.** No personal data on a public ledger. On-chain (if used
   at all) holds only **salted hashes / commitments / revocation state** — never PII.
3. **Selective disclosure.** Share the *minimum* fact needed (a boolean/score, not a history).
4. **Pseudonymous by default.** A renter's wallet identity is a **DID**; linking it to a legal
   identity happens only when the renter chooses (e.g. to sign a lease).
5. **Sybil- and fraud-resistant.** Attestations are only meaningful if issuers are real and
   verified. We bind issuance to *real tenancies* in the core platform.
6. **No financial speculation.** No token, no coin to buy. Wallet = identity + credential store.

---

## 3. Key concepts (glossary)

| Term | Meaning here |
|------|--------------|
| **Wallet** | App/extension holding the renter's keys + credentials (self-custodied). |
| **DID** (Decentralized Identifier) | The renter's pseudonymous identifier (e.g. `did:key`, `did:web`, or `did:pkh` from a wallet address). |
| **Verifiable Credential (VC)** | A signed statement by an issuer about a subject (W3C VC standard). E.g. landlord → renter: "12 on-time payments, tenancy 2023–2024." |
| **Issuer** | Who signs the VC (a verified landlord, or our platform on a landlord's behalf). |
| **Holder** | The renter (holds VCs in their wallet). |
| **Verifier** | A prospective landlord checking a proof. |
| **Verifiable Presentation (VP)** | What the holder sends a verifier: selected claims + proof. |
| **Selective disclosure** | Reveal only some fields of a VC (e.g. via BBS+ signatures / SD-JWT). |
| **ZK proof** | Prove a predicate (e.g. "score ≥ 4/5", "0 missed payments in 24mo") revealing nothing else. |
| **Attestation anchor** (optional) | A hash/commitment + revocation status recorded on-chain (e.g. **EAS**) so verifiers can confirm a credential is genuine & not revoked, without us being online. |

---

## 4. What gets attested

Attestations are **factual and tenancy-derived**, generated from core-platform data so they
are hard to fake and easy to defend:

- **Payment reliability**: count/percentage of on-time rent payments over the tenancy
  (derived from the rent ledger).
- **Tenancy duration & completion**: start/end, ended normally vs. eviction/abandonment.
- **Property condition**: check-out vs check-in delta summary, deposit deductions (yes/no, band).
- **Would rent again**: landlord boolean + optional short structured rating.
- **Identity assurance level** (optional): "this renter completed a verified ID check" — without
  exposing the ID itself.

Each attestation records: issuer DID, subject DID, claim set, validity window, the tenancy
reference (hashed), schema version, signature, and revocation pointer.

**We do not attest** free-text defamation, protected characteristics, or anything that can't
be tied to an objective event in a tenancy. Issuers see this guardrail at issuance time.

---

## 5. Core flows

### 5.1 Renter onboarding to wallet
1. Renter installs/opens the companion (PWA/app or supported wallet) and creates a DID.
2. Optional **proof-of-personhood / ID check** to raise their assurance level and resist Sybil
   abuse (one human ↔ one reputation; the ID data is not stored on us — only an assurance VC).
3. Wallet is now ready to receive credentials.

### 5.2 Issuing an attestation (landlord, at offboarding)
1. At successful move-out (PRD 01 FR-6.5), landlord clicks **"Issue attestation."**
2. Platform pre-fills factual claims from ledger/inventory; landlord confirms the boolean +
   rating fields.
3. Platform (or landlord's DID) **signs** the VC and delivers it to the renter's wallet
   (via link/QR / credential-offer protocol). Optionally **anchors** a hash on-chain (EAS).
4. Renter accepts the VC into their wallet. Audit event recorded on the core platform.

### 5.3 Requesting & verifying a reputation (new landlord, at screening)
1. New landlord clicks **"Request reputation"** on an application (PRD 01 FR-3.2) and chooses
   what they want to know (e.g. "payment reliability over last 24 months", "would-rent-again").
2. Renter receives a **presentation request**; their wallet builds a **Verifiable Presentation**
   disclosing only the requested claims (or a ZK proof of the predicate).
3. Verifier's result: ✅ verified (issuer signatures valid, not revoked, anchors match) + the
   disclosed facts — **no raw history, no issuer identity unless disclosed**.
4. The renter can decline; declining is not framed as guilt (anti-discrimination posture).

### 5.4 Revocation & dispute
- An issuer can **revoke** an attestation (e.g. issued in error) via the revocation registry.
- A renter can **dispute** an attestation; disputed attestations are flagged in presentations.
- Erasure: because VCs live in the renter's wallet and only hashes/commitments are anchored,
  GDPR erasure = renter discards the VC + issuer revokes + (anchor becomes a meaningless hash).

---

## 6. Privacy & GDPR architecture (critical)

> The single biggest design risk is putting personal data on an immutable ledger. We don't.

- **Off-chain by default.** VCs are stored in the renter's wallet and (encrypted) backup. The
  platform stores issuance metadata needed for audit, minimized.
- **On-chain (optional, later)** stores only: a **salted hash/commitment** of the credential,
  a **revocation flag**, and an **issuer registry** entry. None of this is PII; a hash without
  the off-chain VC is meaningless and not "personal data" if salts/keys are destroyed on erasure.
- **Selective disclosure** via **SD-JWT VC** or **BBS+** signatures so a renter reveals one field,
  not the whole credential.
- **ZK predicates** (later phase) via a proving scheme so "≥ N on-time payments" reveals nothing else.
- **Pseudonymity:** DIDs are not linked to legal identity by us; renters can use **per-relationship
  DIDs** to prevent cross-landlord correlation.
- **DPIA** (Data Protection Impact Assessment) is a required deliverable before the reputation
  network goes live.
- **Lawful basis:** consent for sharing presentations; legitimate interest carefully assessed for
  issuance; clear notices to both parties.

---

## 7. Anti-abuse / integrity
- **Issuer verification:** only landlords with a *real, completed tenancy* in the core platform
  can issue tenancy attestations; issuer DIDs are in a managed registry → strong Sybil resistance
  on the issuer side.
- **Subject Sybil resistance:** optional proof-of-personhood so one human can't farm many clean
  reputations or dodge a bad one by making a new wallet (trade-off vs. pseudonymity — opt-in,
  raises assurance level rather than being mandatory).
- **Collusion / fake-positive resistance:** weight attestations by issuer history; flag rings;
  factual claims are ledger-derived, not free-form.
- **Defamation / fairness:** structured claims only, dispute mechanism, no protected-characteristic
  fields, audit trail.

## 8. Standards & tech choices (see PRD 03 for service split)
- **W3C Verifiable Credentials & DIDs** as the backbone (portable, non-proprietary).
- **SD-JWT VC** for selective disclosure in v1 (simpler/EU-aligned, fits the **EUDI Wallet**
  direction); **BBS+** / ZK as a later upgrade.
- **DID methods**: start with `did:key` / `did:web`; support `did:pkh` (wallet-address-based) for
  users who want a crypto wallet as their identity.
- **Optional anchoring**: **Ethereum Attestation Service (EAS)** on a low-cost L2, used *only* for
  hashes/revocation — gasless/sponsored so renters never pay or hold crypto.
- **Crypto-heavy verification service** is a strong candidate to build in **Go** (good crypto libs,
  concurrency for verification throughput) — a deliberate learning target.

> 🇪🇺 **Watch the EUDI Wallet (eIDAS 2.0).** The EU is mandating digital identity wallets;
> aligning our credential formats (SD-JWT VC) with that standard is a strategic moat and keeps us
> from inventing a parallel system.

## 9. MVP vs. later
- **MVP (Phase 3):** landlord issues a *platform-signed* attestation from tenancy data; renter
  holds it in a simple custodial-but-exportable wallet; new landlord requests a presentation;
  verifier sees verified facts. Selective disclosure via SD-JWT. **No public chain required.**
- **Later (Phase 4):** self-custodied wallets / `did:pkh`, on-chain anchoring + revocation (EAS),
  BBS+/ZK predicates, EUDI-wallet interop, proof-of-personhood.

## 10. Success metrics
- Attestations issued per completed offboarding (target ≥ 1).
- Reputation requests by *new* landlords (network-effect proof).
- % of requests the renter fulfills (trust/UX proof).
- Disputed-attestation rate (integrity health).

## 11. Open questions
- Custodial vs. self-custodial wallet for the *MVP* (UX vs. purity)? → **custodial-but-exportable**
  in MVP, self-custody in Phase 4.
- Mandatory proof-of-personhood vs. opt-in (Sybil vs. privacy)? → **opt-in, assurance-level based**.
- Which L2 / anchoring service and who sponsors gas? → defer to Phase 4 spike.
- Legal review: is a tenancy attestation a "reference" / does it trigger credit-reference
  regulation in the UK? → **requires legal review before launch.**
