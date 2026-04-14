# Firecrawl Inventory — /crawl and /map Surface (Doc-Confirmed)

## Purpose

This document records the confirmed response shapes and operational caveats
for the Firecrawl `/crawl` and `/map` endpoints.

It is a transition-support artifact, not authority doctrine.
It exists to ground the remaining Batch H schema design pass in confirmed
provider behavior rather than inference.

---

## How this was confirmed

Live payload samples for `/crawl` and `/map` were blocked by provider 502
errors at the time of this inventory. Response shapes and operational behavior
were confirmed against canonical Firecrawl documentation at
`docs.firecrawl.dev` (v2). Doc confirmation is sufficient for the schema
design pass because `/crawl` per-page families are the same as `/scrape`,
which is already baselined in this folder.

Live samples remain desirable for completeness. When the 502 situation
resolves, a live `/crawl` and `/map` sample set should be added to this
folder following the same capture-set posture as the existing scrape baseline.

---

## /map surface

### Purpose in Firecrawl

URL discovery. Accepts a starting URL and returns most known URLs for that
domain. Extremely fast. Intended as a pre-flight tool for identifying what
pages exist before deciding what to crawl.

### Response shape

```json
{
  "success": true,
  "links": [
    {
      "url": "https://example.com/page",
      "title": "Page Title",
      "description": "Page description"
    },
    ...
  ]
}
```

Top level: `success`, `links`.

Each link object: `url` (always present), `title` (optional), `description`
(optional). Title and description presence depends on the target website.

With the `search` param, results are ordered most-to-least relevant.

### Operational characteristics

- 1 credit per call, flat, regardless of URL count returned
- Speed-first: primarily sourced from sitemap + cached SERP results +
  previously crawled pages; not a fresh crawl
- Explicitly not guaranteed comprehensive; the docs state it may miss links
  not in the sitemap or SERP cache
- For thorough and up-to-date URL discovery, Firecrawl docs recommend `/crawl`
  instead

### VEDA observatory posture

`/map` is a URL discovery surface, not a page capture surface.

It is appropriate for:
- scoping a crawl job before committing credits
- pre-flight discovery of what pages exist at a domain
- building a candidate URL set for operator review before a targeted crawl

It is not appropriate for:
- treating the returned links as a canonical inventory of all pages at a domain
- substituting for `/crawl` when comprehensive coverage is required
- treating `title` and `description` as authoritative page metadata
  (they are SERP-cached or sitemap-derived, not live crawl observations)

Discovery observations from `/map` fit the `Discovery observations` family
defined in `veda/providers/firecrawl.md`. They are observable reality at
the time of the map call, not guaranteed complete reality.

---

## /crawl surface

### Purpose in Firecrawl

Multi-page crawl. Recursively discovers and scrapes every reachable subpage
from a starting URL. Handles sitemaps, JavaScript rendering, and rate limits
automatically.

### Job lifecycle

`/crawl` is async. The submit call returns a job ID immediately. Results are
retrieved by polling `GET /v2/crawl/{id}` or via webhook delivery.

Submit response:
```json
{
  "success": true,
  "id": "123-456-789",
  "url": "https://api.firecrawl.dev/v2/crawl/123-456-789"
}
```

### Status response shape (polling)

```json
{
  "status": "scraping | completed | failed",
  "total": 36,
  "completed": 10,
  "creditsUsed": 10,
  "expiresAt": "2024-00-00T00:00:00.000Z",
  "next": "https://api.firecrawl.dev/v2/crawl/123-456-789?skip=10",
  "data": [
    {
      "markdown": "...",
      "html": "...",
      "metadata": {
        "title": "...",
        "language": "en",
        "sourceURL": "https://...",
        "description": "...",
        "statusCode": 200
      }
    },
    ...
  ]
}
```

### Per-page families in data array

Each entry in the `data` array is a scrape object with the same families as
`/scrape`:

- `markdown` — normalized markdown extraction of the page
- `html` — rendered HTML of the page
- `metadata` — page metadata including `title`, `description`, `language`,
  `sourceURL`, `url`, `statusCode`, and provider/runtime fields (same mixed
  page/provider metadata pattern observed in the `/scrape` baseline)
- `links` — observed link emissions from the page (when requested)
- `rawHtml` — raw HTML (when requested)

The existing `/scrape` baseline in this folder is the correct foundation for
understanding what these families contain per page. No new canonical family
shapes are introduced by `/crawl` — it applies `/scrape` at scale.

### Delivery options

Three delivery models are available:
1. **Polling** — `GET /v2/crawl/{id}` until status is `completed` or `failed`
2. **WebSocket watcher** — real-time snapshots as pages are scraped
3. **Webhook** — per-page events delivered to an endpoint as crawling progresses

Webhook events: `crawl.started`, `crawl.page` (per page), `crawl.completed`,
`crawl.failed`. Each `crawl.page` event delivers page data in real time.
Webhook requests include an `X-Firecrawl-Signature` header (HMAC-SHA256)
for authenticity verification.

The delivery model choice is an implementation decision for VEDA's observatory
operations layer, not a schema design question.

---

## Critical operational caveats

These three caveats must be carried forward into the Batch H schema design
pass and any VEDA implementation work that uses Firecrawl `/crawl`.

### 1. 24-hour result expiration

Crawl job results are available via the Firecrawl API for **24 hours only**
after job completion. After that window closes, results are only viewable in
Firecrawl's own activity logs — not retrievable via API.

**Implication for VEDA:** Bucket capture of crawl artifacts is not optional.
It is required. If a crawl job completes and its output is not captured to
the bucket before the 24-hour window closes, the raw provider artifacts are
permanently unavailable. The bucket-first posture defined in
`firecrawl-bucket-capture-posture.md` must be enforced at the implementation
level, not treated as a nice-to-have.

### 2. Non-determinism across runs

Firecrawl explicitly documents that crawl results vary between runs of the
same configuration. Pages are scraped concurrently; link discovery order
depends on network timing. Near `maxDiscoveryDepth` limits, different branches
of a site may be explored to different extents depending on which pages load
fastest during that run.

**Implication for VEDA:** Observatory records from separate `/crawl` runs of
the same target are not bitwise comparable. A re-crawl does not produce an
identical observation to the prior crawl — it produces a new observation with
its own capture time, coverage profile, and page set. Re-crawl comparison
logic must account for this. Trust posture for individual crawl run observations
should preserve the non-determinism context (capture time, run configuration,
completion status) rather than treating a crawl result as a reproducible
snapshot.

To reduce non-determinism when it matters, Firecrawl docs recommend:
`maxConcurrency: 1` or `sitemap: "only"` (if the site has a comprehensive
sitemap). These are operational choices, not schema design choices.

### 3. Crawl errors are a separate endpoint

The `data` array in a completed `/crawl` response contains only pages
Firecrawl **successfully scraped**. Pages that failed due to network errors,
timeouts, or robots.txt blocks are silently absent from `data`.

A dedicated errors endpoint exists: `GET /v2/crawl/{id}/errors`.

**Implication for VEDA:** A completed crawl with a non-empty `data` array is
not evidence of complete domain coverage. It is evidence of what was
successfully scraped in that run. Failure to call the errors endpoint means
silently incomplete capture with no indication of what was missed. Crawl
failure observations (defined as an admitted observatory family in
`veda/providers/firecrawl.md`) require the errors endpoint to be populated.
VEDA's capture completeness posture must treat the errors check as required,
not optional.

---

## Pagination note

For crawl responses exceeding 10MB, the API returns a `next` URL parameter
pointing to the next page of results. Direct API callers must follow `next`
until it is absent. SDK callers get this handled automatically.

---

## VEDA placement summary

### `/map` output

| Family | Posture |
|---|---|
| Discovered URL list | Discovery observations — archive, model selectively |
| `title` / `description` from map | Not authoritative page metadata; SERP-cached or sitemap-derived; archive as discovery context only |

### `/crawl` per-page output

| Family | Posture |
|---|---|
| `markdown` | Archive now, model selectively — same posture as `/scrape` baseline |
| `html` / `rawHtml` | Raw evidence — archive always |
| `metadata` (page fields) | Canonical observatory truth candidate — selective promotion, split page vs provider fields |
| `metadata` (provider/runtime fields) | Archive; do not promote as page truth |
| `links` | Observatory family — archive; model selectively after normalization |
| Crawl job metadata | Canonical observatory truth — job ID, target URL, timestamps, status |
| Crawl failure records | Canonical observatory truth — failure is an observation; must be preserved |

---

## Relationship to existing baseline

The `/scrape` baseline and its inventory note are the ground truth for
per-page family shapes. This document does not re-derive them. When the
schema design pass for Batch H residual opens, use both this document and
the scrape baseline together.

---

## Steward note

This inventory is doc-confirmed, not live-payload-confirmed. When live
samples become available, add them to this folder and note any discrepancies
between doc-confirmed shapes and actual observed payloads.

The three caveats in this document (expiration, non-determinism, errors
endpoint) are grounded in canonical Firecrawl documentation and should be
treated as settled operational reality, not provisional speculation.

---

## Related files

- `README.md`
- `firecrawl-api-scrape-google-seo-starter-guide-baseline-inventory.md`
- `firecrawl-bucket-capture-posture.md`
- `transition-plan.md`
- `../../veda/providers/firecrawl.md`
- `../../veda/schema-reference.md`
- `../../veda/data-boundaries.md`
