# V Ecosystem Audit Program

## Purpose

This folder contains the layered audit plan and Claude audit prompts for hard-reviewing the V Ecosystem docs without overwhelming the reviewer or collapsing distinct review layers into one vague mega-audit.

This folder exists to answer:

```text
How should the V Ecosystem docs be audited in a smart layered sequence,
what should each audit inspect,
and what prompts should be used so each audit complements the others
instead of duplicating or diluting them?
```

This is a planning and quality-control cluster.
It is not doctrine.
It is not authority over the ecosystem docs.
It is an internal review support layer.

---

## Core Rule

The V Ecosystem docs should be audited in bounded layers.

Do not ask for one giant review of the whole corpus.
That produces shallow pattern-matching, false confidence, missed contradictions, and expensive summary theater.

Each audit in this folder is designed to:
- inspect one logical layer at a time
- produce findings that improve the next audit
- distinguish doctrine issues from implementation issues from planning/history issues
- prefer bounded fixes over churn

---

## Audit sequence

### Phase 0 — Audit posture
Lock reviewer behavior before asking for findings.

### Audit 1 — Root / hierarchy / document-role audit
Check authority hierarchy, live vs historical posture, shadow-authority risk, and root navigability.

### Audit 2 — Ecosystem foundation audit
Check ecosystem-level law, ADR alignment, vocabulary consistency, and cross-system framing.

### Audit 3 — Governance spine audit
Check whether governance docs actually constrain the ecosystem coherently.

### Audit 4 — Project V authority + build-spec audit
Check Project V identity, schema/API/readiness/audit coherence, and implementation sufficiency.

### Audit 5 — VEDA authority + build-spec audit
Check pure-observatory posture, provenance/error/model clarity, and build-spec sufficiency.

### Audit 6 — V Forge authority + operability audit
Check execution-system identity, first-pass scope consistency, playbook/schema/surface alignment, and anti-drift posture.

### Audit 7 — Cross-system interface audit
Check whether seams preserve ownership and boundary clarity under real operational pressure.

### Audit 8 — Extension/runtime doctrine audit
Check whether the Tier 1 runtime law is coherent across memory, state, governance, orchestration, and tool posture.

### Audit 9 — Runtime implementation-companion audit
Check whether the Tier 3 runtime docs are subordinate, implementation-usable, and free of shadow-doctrine drift.

### Audit 10 — Verification / hammer / implementation-readiness audit
Check whether the ecosystem can be built and verified from the docs without hidden assumptions.

### Audit 11 — Final synthesis audit
Only after layered audits are complete, synthesize the real remaining risks and bounded next fixes.

---

## Operating rules

- Fix real issues between audits.
- Do not pile up ten audits before patching anything.
- Do not ask for giant rewrites.
- Do not flatten doctrine, implementation companion, planning, and history into one blob.
- Use canonical docs as primary truth.
- Treat planning and review support material as support, not authority.

---

## Files in this folder

- `audit-posture.md` — reusable reviewer posture prompt
- `audit-01-root-hierarchy-prompt.md` — first audit prompt
- later audit prompts should be added here as they are created and used

---

## Usage

Use this folder when:
- running Claude audits over the docs corpus
- sequencing review passes intelligently
- preserving reusable prompt assets
- preventing future audit sessions from rediscovering how to review the docs well
