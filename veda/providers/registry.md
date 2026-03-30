# VEDA Provider Registry

## Purpose

This document is the authoritative registry of external data providers
currently integrated with VEDA.

It exists to answer:

```text
What external providers does VEDA currently integrate with, what is each
provider's classification, what data does it supply, and what governance
posture applies to its use?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the registry of all active external provider integrations in VEDA
- the classification, data type, trust posture, and spend posture for each provider
- what each provider may supply and what constraints apply
- the record that must be updated when providers are added, modified, or removed

---

## Out of Scope

This document does not define:

- the doctrine governing how providers are classified and admitted
- implementation-specific API credential or auth mechanics
- the detailed ingest pipeline design for each provider

Those belong in the external-provider-integration-doctrine and implementation docs.

---

## System

- veda

---

## Core Rule

Only providers listed in this registry are active integrations in VEDA.

A provider that is not in this registry has not been admitted through the
governed provider admission process and must not be integrated.

Adding a provider to this registry requires completing the full admission
process defined in:
`../../ecosystem/external-provider-integration-doctrine.md`

---

## Registry Format

Each provider entry must record:

- **Name** — the provider name
- **Classification** — Observatory Input, Execution Tooling, or Planning Support
- **Data supplied** — what data the provider contributes to VEDA
- **Trust posture** — the trust classification for data from this provider
- **Spend posture** — Free, Bounded Paid, or Approval-Required Paid
- **Approval posture** — what approval is required before use
- **Status** — Active, Paused, or Deprecated
- **Admitted** — the date the provider was admitted through the governed process

---

## Current Registry

> No providers have been formally admitted through the governed admission process yet.
> This registry is the authoritative record. When providers are admitted,
> they must be recorded here before integration proceeds.

---

## Registry Update Rule

This document must be updated when:

- a new provider is admitted (add the entry)
- a provider's classification, trust posture, or spend posture changes (update the entry)
- a provider is deprecated or removed (mark as Deprecated with the date and reason)

Registry updates that add a new provider must occur after the full admission
process is complete, not before.
A provider listed here as Active is asserting that the admission process has been completed.

---

## Related Docs

- `../../ecosystem/external-provider-integration-doctrine.md`
- `../veda.md`
- `../system-invariants.md`
- `../mcp-surface.md`
- `../../governance/paid-data-pull-governance.md`
- `../../governance/external-action-governance.md`