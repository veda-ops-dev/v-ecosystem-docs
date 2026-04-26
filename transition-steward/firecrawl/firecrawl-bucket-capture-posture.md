# Firecrawl Bucket Capture Posture

## Purpose

This document defines the current transition-support storage posture for Firecrawl capture artifacts.

It exists to answer one practical question:

> What exactly should a Firecrawl bucket hold, how should it be organized, and what must remain in canonical VEDA records rather than being left only in bucket storage?

This document is:
- a transition-support capture/storage posture note
- a concrete organization guide for Firecrawl bucket artifacts
- a guardrail against ad hoc bucket layouts that become unreadable to humans or LLMs

This document is **not**:
- final schema authority
- final implementation code
- bucket vendor-specific infrastructure doctrine
- permission to let the bucket become canonical truth

Settled architecture belongs in authority docs.
Concrete but still transition-stage bucket/capture decisions belong here.

---

## Core rule

The Firecrawl bucket is **evidence backing storage**.
It is not canonical truth.
It is not strategy.
It is not doctrine.

Canonical VEDA records must remain the system of record for:
- the fact that a capture occurred
- project scope
- provider identity
- capture time
- provenance
- stable references to the backing artifacts
- promoted hot-path query fields

The bucket exists to hold bulky, expensive, re-parsable evidence.

---

## Why the bucket exists

The bucket should preserve Firecrawl artifacts that are:
- expensive to re-pull
- large enough that they should not live directly in hot-path canonical rows
- useful to re-parse later as VEDA capture doctrine matures
- important for evidence review, provenance, and auditability

This is especially important for:
- raw provider response bodies
- raw HTML captures
- normalized markdown captures
- link dumps
- large metadata/discovery artifacts

---

## Capture-set rule

A **capture set** is:
- one provider
- one target URL
- one crawl attempt
- one capture timestamp

A capture set must not mix multiple target URLs into one artifact directory.
If multiple URLs are crawled, each URL gets its own capture set directory.

Re-crawls of the same URL create new capture sets.
They do not overwrite prior captures.

---

## Directory posture

Use one directory per capture set.

Recommended path shape:

```text
bucket/firecrawl/<project_slug>/<host>/<yyyy-mm-dd>/<capture_timestamp>--<url_slug>/
```

Example:

```text
bucket/firecrawl/acme/google.com/2026-04-12/2026-04-12T154200Z--seo-starter-guide/
```

This path shape is preferred because it is:
- chronologically sortable
- readable to humans
- readable to LLMs
- narrow enough to stay predictable
- specific enough to avoid collisions

Do not build deep, decorative folder trees.
Provider, project, host, date, and capture-set directory are sufficient.

---

## Manifest-first rule

Every capture set must contain a small `manifest.json`.

This should be the first file read by a human or LLM.
It is the table of contents for the capture set.

Minimum manifest contents:
- provider
- provider surface / endpoint
- project slug
- target URL
- normalized host
- capture timestamp
- crawl status
- formats requested
- artifact filenames present
- missing expected artifacts
- content hash if available
- capture-set identifier
- notes on partial or failed capture

Without a manifest, the bucket becomes difficult to review and difficult to use safely.

---

## Stable filename rule

Use the same filenames in every successful capture set where the artifacts exist.

Preferred filenames:
- `manifest.json`
- `raw-response.json`
- `raw-html.html`
- `markdown.md`
- `links.json`
- `failure.json` (only when needed)

Do not invent per-run filename variations.
Do not use "final", "new", "fixed", "real", or similar drift-prone names.

Consistency matters more than cleverness here.

---

## Minimum successful capture set

A successful or partially successful capture set should keep:
- `manifest.json`
- `raw-response.json`
- at least one extracted evidence artifact when present:
  - `raw-html.html`
  - `markdown.md`
  - `links.json`

If the run failed before those artifacts existed, the capture set should still keep:
- `manifest.json`
- `failure.json` or equivalent failure details in the manifest

A bucket folder containing only random blobs with no manifest is not an acceptable capture set.

---

## What the bucket should hold

The Firecrawl bucket should hold the following artifact families when present.

### 1. Raw provider response
File:
- `raw-response.json`

Purpose:
- preserves the exact Firecrawl API response body
- preserves provider-native structure
- supports later re-parsing as canonical capture doctrine evolves

### 2. Raw HTML capture
File:
- `raw-html.html`

Purpose:
- preserves source-level page evidence
- preserves metadata, declared structured data, canonicals, hreflang, OG fields, and similar page-level facts
- provides the strongest source artifact when markdown extraction is noisy or lossy

### 3. Normalized markdown capture
File:
- `markdown.md`

Purpose:
- preserves the readable extraction view
- supports later chunking, retrieval, operator review, and comparison work
- remains useful even when noisy, so long as it is not mistaken for already-clean canonical page truth

### 4. Link dump
File:
- `links.json`

Purpose:
- preserves observed link structure as captured
- supports later internal/external, nav/content, anchor, and language-variant normalization
- remains evidence, not a pre-cleaned relationship graph

### 5. Failure or partial-capture artifact
File:
- `failure.json` or manifest failure block

Purpose:
- preserves the fact that a crawl failed, partially failed, timed out, or returned incomplete data
- prevents absence from being mistaken for clean non-existence

---

## What must remain in canonical VEDA records

The bucket must not be the only place where important observatory truth lives.

Canonical VEDA records must preserve at least:
- project scope
- provider identity
- target URL
- capture timestamp
- crawl status
- stable references to bucket artifacts
- provenance fields
- promoted hot-path fields needed for querying or filtering

If those things live only in the bucket, the bucket has started becoming a shadow database.

---

## Evidence versus interpretation rule

The bucket should contain:
- raw evidence
- evidence-heavy extracts
- provenance
- manifests
- failure artifacts

The bucket should not contain mixed-in:
- strategy notes
- recommendations
- freehand analysis docs inside capture folders
- canonical doctrine
- planning state

Interpretation belongs in paired inventory notes or authority docs, not inside raw evidence folders.

---

## LLM readability rule

The bucket must stay readable to an LLM without requiring guesswork.

That means:
- one predictable folder shape
- one predictable manifest filename
- one predictable artifact naming convention
- no mixed multi-URL folders
- no overwritten recrawls
- no hidden meaning stored only in operator memory

The point is not to make the bucket pretty.
The point is to make it legible and safe to navigate.

---

## Re-crawl rule

A re-crawl of the same URL is a new capture set.
It must not overwrite the prior set.

Why:
- observability depends on time-based comparison
- prior evidence may matter later
- parsing/normalization quality can improve later without destroying historical capture context

History is a feature, not clutter.

---

## Bucket anti-patterns

The Firecrawl bucket has drifted if it starts to:
- act as canonical truth rather than evidence backing storage
- hold only raw blobs without manifests
- hold interpretation mixed into raw capture directories
- overwrite prior re-crawls
- use inconsistent filenames across capture sets
- hide provenance only inside large JSON bodies with no promoted references elsewhere
- become a dumping ground for unrelated provider artifacts with no capture-set discipline

These are bucket failures, not harmless mess.

---

## Current recommended first-pass posture

For the current transition phase, the safest first-pass Firecrawl bucket posture is:

1. one capture set per URL per attempt per timestamp
2. one manifest per capture set
3. keep `raw-response.json` always
4. keep `raw-html.html`, `markdown.md`, and `links.json` when present
5. do not overwrite re-crawls
6. keep the bucket as evidence backing storage only
7. keep canonical VEDA records responsible for provenance, scope, and stable references

This is concrete enough for implementation guidance without pretending the final governed crawl-family schema is already settled.

---

## Related files

- `transition-steward/firecrawl/README.md`
- `transition-steward/firecrawl/firecrawl-api-scrape-google-seo-starter-guide-baseline-inventory.md`
- `transition-steward/transition-plan.md`
- `veda/providers/firecrawl.md`
- `veda/schema-reference.md`
- `veda/data-boundaries.md`
- `veda/evidence-and-source-provenance.md`

This document is the current transition-support storage posture for Firecrawl captures.
Authority-doc promotion should remain narrow and deliberate.