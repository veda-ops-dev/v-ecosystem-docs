# Firecrawl — provider posture for VEDA

## Purpose

This document defines how Firecrawl data is admitted into VEDA as observatory input.

It exists to answer:

```text
What Firecrawl data may enter VEDA as observatory truth, what must remain
raw observation rather than interpretation, and what bounded use does this
provider serve inside VEDA's observatory role?
```

This is a VEDA provider/doctrine document.

---

## Provider identity

| Field          | Value                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------ |
| Provider name  | Firecrawl                                                                                  |
| Classification | Observatory Input                                                                          |
| Role           | Supplies crawled external webpage content and structured page observations for VEDA intake |

---

## Why this provider belongs in VEDA

VEDA is the observatory truth system of the V Ecosystem.

Firecrawl supplies crawled external content — webpages rendered and normalized into structured observational records. That content is external reality as VEDA observes it at a specific capture time.

That makes Firecrawl a VEDA input provider, not a content generation, scoring, or interpretation engine.

VEDA records what was crawled and when.
VEDA does not decide what that content means or what should be done about it.

---

## What this provider may supply into VEDA

The following data families may be admitted into VEDA as observatory input:

* crawled webpage content (page body, normalized markdown or text extraction)
* structured page metadata (title, meta description, canonical URL, status code, response headers)
* crawled page link structure (outbound links and on-page link references as observed at capture time)
* structured data extracted from crawled pages (schema.org, OpenGraph, declared metadata)
* crawl job metadata (job identifier, target URL, capture timestamp, crawl depth context, job status)
* sitemap and discovery observations produced by crawling
* failure and partial-capture observations (blocked, timed out, rate limited, error status)

These are observatory records because they describe what an external web resource presented at a specific capture time.

---

## What this provider must NOT produce inside VEDA

Firecrawl must not be used inside VEDA to produce:

* content quality scoring
* opportunity scoring or prioritization
* gap detection against the V Forge content graph
* competitive content analysis or interpretation
* tactical recommendations based on crawled content
* content briefs, outlines, or rewrites derived from crawled pages
* planning decisions or execution instructions

Those belong outside VEDA.

Crawling a page records what that page presented at observation time.
It does not interpret what that page means or what the ecosystem should do next.

---

## Core observatory rule

A Firecrawl record is admissible into VEDA only when it preserves the distinction between:

* what Firecrawl crawled and returned at capture time
* what VedaOps may later derive from that crawled observation

The record in VEDA must remain an observatory record.

It may support later structural or strategic interpretation.
It must not embed that interpretation itself.

---

## Admitted observatory families

### 1. Crawled page observations

These record what a given external URL presented when crawled at a specific capture time, including normalized page content, metadata, and structural observations.

### 2. Crawl-derived structured data observations

These record structured data extracted from crawled pages (schema.org, OpenGraph, declared metadata). The observation records what was declared at capture time. Validation, interpretation, or normalization of that structured data into higher-level meaning belongs outside VEDA.

### 3. Crawl job observations

These record the identity, target, timing, status, and operational context of individual crawl jobs.

### 4. Crawl failure observations

These record blocked, timed-out, rate-limited, or errored crawl attempts with provenance context. A failed crawl is itself an observation — the absence of successful capture is observable reality and must be preserved as such.

### 5. Discovery observations

These record what URLs were discovered during sitemap processing, crawl expansion, or link-following operations. Discovery observations record what was surfaced; they do not classify the discovered targets.

---

## Relationship to existing VEDA record families

The exact placement of crawled page observations in VEDA's canonical schema is deferred. The relationship between Firecrawl-crawled pages and the existing `SourceItem` family (which already models captured external items including webpages) has not been formally settled.

Possible futures include:

* Firecrawl crawled pages land in the existing `SourceItem` family with crawl-specific provenance fields
* a new crawl-specific canonical family is established for crawled page observations with its own schema posture
* a bounded combination in which lightweight captures use `SourceItem` and structured crawl jobs use a new family

That question is owned by VEDA schema authority and must be resolved through governed doctrine work before implementation. Admission of Firecrawl as an observatory provider does not resolve it. See the Crawled page observability families entry in `../schema-reference.md`.

---

## Snapshot storage posture

Crawled page payloads may include substantial content that must be preserved as evidence.

This content must follow the blob and snapshot storage posture defined in `../data-boundaries.md` — addressable by stable reference, backing-store neutral, and not embedded directly in hot-path query fields.

Hot-path fields required for querying or filtering must be promoted to explicit schema columns per `../schema-reference.md`. Raw crawled payloads are evidence support, not the primary query target.

---

## Provenance requirements

Every Firecrawl observatory record admitted into VEDA must preserve sufficient provenance, including where available:

* provider name
* provider job or endpoint identifier
* target URL crawled
* crawl job identifier or batch reference
* capture timestamp
* retrieval timestamp
* crawl status (success, partial, failed) and error context if applicable
* crawler user agent or profile context if supplied
* content hash for deduplication where applicable

A record without provenance is not admissible observatory truth.

---

## Spend posture

Firecrawl is a paid provider. Paid provider governance applies per `../../governance/paid-data-pull-governance.md`.

Key constraints:

* crawl calls must be bounded by explicit scope before they are made
* crawl calls must not be self-authorized by agents without governed approval
* every paid crawl must produce a reportable outcome
* spend must be tracked against bounded per-project or per-scope caps
* unbounded whole-site crawling without explicit approval is a governance violation

The exact spend-tracking and approval mechanics follow the paid data pull governance rules. The provider classification here does not override those rules.

---

## Boundary rule

The existence of crawled page content does not make VEDA a content analysis engine, a competitive intelligence system, or a content recommendation system.

It only makes VEDA capable of observing and preserving external webpage content at specific capture times.

Interpretation belongs to VEDA Strategy.
Planning belongs to Project V.
Execution — including the content graph of what was built — belongs to V Forge.

Crawling an external page does not create a V Forge content graph record. The content graph represents what the ecosystem built. A crawled external page is what someone else published, observed at a point in time.

---

## Deferred questions

The following should remain deferred until later doctrine work is complete:

* exact VEDA canonical schema family for crawled page observations
* exact normalization model for extracted structured data
* exact deduplication and supersedence rules for re-crawls of the same URL
* exact retention and archival policy for crawled page snapshots
* exact VEDA Strategy models derived from crawled observations
* exact relationship between crawled page observations and the existing `SourceItem` family

These should not be guessed early. The admission of Firecrawl as an observatory provider does not settle these downstream schema and doctrine questions.

---

## Related docs

* `registry.md`
* `dataforseo-ai-optimization.md`
* `../observability-and-signal-role.md`
* `../schema-reference.md`
* `../data-boundaries.md`
* `../evidence-and-source-provenance.md`
* `../../ecosystem/external-provider-integration-doctrine.md`
* `../../governance/paid-data-pull-governance.md`
* `../../veda-strategy/veda-strategy.md`
