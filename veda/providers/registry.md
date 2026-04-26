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

### DataForSEO AI Optimization

| Field | Value |
|---|---|
| **Name** | DataForSEO AI Optimization |
| **Classification** | Observatory Input |
| **Data supplied** | LLM mention observations, LLM citation observations, cited source domain/page observations, AI-platform response metadata, Google AI Overview citation/source observations, fan-out query observations, brand entity observations, and related platform/time/location/language observation metadata |
| **Trust posture** | External provider data. Time-stamped observatory input. Useful for observing answer-surface behavior, but not canonical beyond the observation window and never self-interpreting. |
| **Spend posture** | Bounded Paid |
| **Approval posture** | Governed provider admission complete. Use remains subject to normal paid-data pull governance and operator-approved integration scope. |
| **Status** | Active |
| **Admitted** | 2026-04-09 |

**Admission doc:** `dataforseo-ai-optimization.md`

---

### Firecrawl

| Field | Value |
|---|---|
| **Name** | Firecrawl |
| **Classification** | Observatory Input |
| **Data supplied** | Crawled external webpage content (normalized markdown/text extraction), structured page metadata, on-page link structure observations, extracted structured data (schema.org, OpenGraph, declared metadata), crawl job metadata, sitemap and discovery observations, and crawl failure/partial-capture observations. |
| **Trust posture** | External provider data. Time-stamped observatory capture of external webpage content as presented at crawl time. Preserves what the provider returned; does not interpret or classify crawled content. |
| **Spend posture** | Bounded Paid |
| **Approval posture** | Governed provider admission complete. Use remains subject to normal paid-data pull governance, bounded per-scope crawl caps, and operator-approved integration scope. Unbounded whole-site crawling without explicit approval is a governance violation. |
| **Status** | Active |
| **Admitted** | 2026-04-09 |

**Admission doc:** `firecrawl.md`

---

## Admission Scope Notes

Admission of a provider to this registry settles the following at a governance level:

- provider identity and classification
- which observatory data families the provider is authorized to supply
- trust posture for data from this provider
- spend posture and approval posture
- admission status

Admission does NOT settle the following, which remain governed separately:

- exact VEDA canonical schema families that will hold records from this provider — see `../schema-reference.md` and its Deferred Owned Domains section
- exact normalization, deduplication, and provenance schema model for provider records
- exact retention, archival, and supersedence rules
- exact VEDA Strategy models that may later derive intelligence from these observations — see `../../veda-strategy/schema-authority.md`
- exact downstream tactical, strategic, or planning implications of the data

### DataForSEO AI Optimization — what admission settles vs. defers

Admission of DataForSEO AI Optimization settles that AI-surface observability — LLM mention observations, LLM citation observations, cited source/domain/page observations, fan-out query observations, brand entity observations, and AI-surface response metadata — is a VEDA-owned observatory domain.

Admission does not settle the exact VEDA canonical schema families for AI-surface observability, their normalization posture, how cross-platform observation context is represented, or the VEDA Strategy derivation models that may later be built on top of them. Those remain deferred per `../schema-reference.md` (AI-surface observability families) and must not be resolved by expedient JSON blobs on existing families or by ad hoc tables.

### Firecrawl — what admission settles vs. defers

Admission of Firecrawl settles that crawled external page observations — crawled page content, extracted structured data, crawl job metadata, crawl failure observations, and discovery observations — are a VEDA-owned observatory domain.

Admission does not settle whether crawled pages land in the existing `SourceItem` family, a new crawl-specific canonical family, or some bounded combination. That schema design is deferred per `../schema-reference.md` (Crawled page observability families) and must be resolved through governed doctrine work before implementation.

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
- `dataforseo-ai-optimization.md`
- `firecrawl.md`
- `../veda.md`
- `../schema-reference.md`
- `../data-boundaries.md`
- `../system-invariants.md`
- `../mcp-surface.md`
- `../../governance/paid-data-pull-governance.md`
- `../../governance/external-action-governance.md`
- `../../veda-strategy/veda-strategy.md`
- `../../veda-strategy/schema-authority.md`
