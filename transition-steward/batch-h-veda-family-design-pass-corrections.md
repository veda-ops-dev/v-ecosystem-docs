# Batch H Design Pass — Corrections from Official Docs

## Purpose

This note records corrections to `batch-h-veda-family-design-pass.md` based on
verification against official Firecrawl v2 documentation at `docs.firecrawl.dev`.

It exists to answer:

```text
What did the design pass get wrong or leave underspecified that official provider
docs now resolve, and what must change before the design pass is promoted into
authority docs?
```

This is a transition-support correction note.
It is not itself authority doctrine.
It must be read alongside `batch-h-veda-family-design-pass.md` before any
authority-doc promotion work begins.

Sources verified:
- `https://docs.firecrawl.dev/api-reference/endpoint/crawl-get-errors`
- `https://docs.firecrawl.dev/api-reference/endpoint/map`
- `https://docs.firecrawl.dev/api-reference/endpoint/crawl-post`

---

## Correction 1 — `CrawlFailureRecord`: `robotsBlocked` is a separate top-level field

### What the design pass assumed

`CrawlFailureRecord` modeled crawl failures as a single family with an `errorType`
free-text field covering all failure modes, including robots.txt blocks.

### What the official docs actually say

The `GET /v2/crawl/{id}/errors` response has two structurally distinct top-level
fields:

```json
{
  "errors": [
    {
      "id": "<string>",
      "timestamp": "<string>",
      "url": "<string>",
      "error": "<string>"
    }
  ],
  "robotsBlocked": ["<string>"]
}
```

- `errors` — array of scrape jobs that failed. Each entry carries `id`,
  `timestamp`, `url`, and `error` (free-text string). These are pages Firecrawl
  attempted to scrape and failed for technical reasons (network errors, timeouts,
  provider-side failures).
- `robotsBlocked` — a separate array of URL strings only. No error detail, no
  timestamp, no per-record ID. These are URLs Firecrawl declined to attempt
  because robots.txt blocked them.

These are structurally different observations:
- A scrape error is an attempted-and-failed observation with per-page detail.
- A robots-blocked URL is an observation that scraping was not attempted due to
  policy, with no detail beyond the URL.

### Correction to the design pass

`CrawlFailureRecord` as designed is insufficient. Two options:

**Option A (recommended): Two sub-types via a `failureClass` discriminator**

Add a `failureClass` column to `CrawlFailureRecord`:
- `failureClass = 'scrape_error'` — sourced from `errors[]`; carries `id`,
  `timestamp`, `url`, `error` string
- `failureClass = 'robots_blocked'` — sourced from `robotsBlocked[]`; carries
  only `url`; `errorDetail`, `providerRecordId`, and `capturedAt` are null or
  set to the job's completion time

This keeps the family unified (both are "this URL was not successfully scraped")
while preserving the structural difference.

**Option B: Two separate families**

`CrawlScrapeError` and `CrawlRobotsBlock` as distinct families. More precise but
adds schema surface for a distinction that is operationally simple.

**Recommendation:** Option A. The behavioral difference (attempted-and-failed vs
not-attempted-by-policy) is captured by `failureClass`. Querying "all URLs not
successfully captured in this job" spans both sub-types and is the most common
use case. A discriminator is cleaner than two families for this.

### Revised minimum canonical fields for `CrawlFailureRecord`

- `id` (uuid)
- `projectId` (uuid, FK → Project)
- `crawlJobId` (uuid, FK → CrawlJob)
- `provider` (text)
- `pageUrl` (text)
- `failureClass` (enum: `scrape_error`, `robots_blocked`)
- `providerRecordId` (text? — provider's `id` field; present for `scrape_error`,
  null for `robots_blocked`)
- `errorDetail` (text? — provider's `error` string; present for `scrape_error`,
  null for `robots_blocked`)
- `failureTimestamp` (timestamptz? — provider's `timestamp` for `scrape_error`;
  null for `robots_blocked`)
- `capturedAt` (timestamptz — when VEDA recorded this failure)
- `createdAt` (timestamptz)

**Uniqueness:** `(projectId, crawlJobId, pageUrl, failureClass)` — one failure
record per URL per failure class per job per project.

---

## Correction 2 — Open question 12.5 is resolved: `error` is free-text, no provider enum

### What the design pass said

Open question 12.5 deferred the `errorType` enum vs free-text decision pending a
live errors-endpoint sample.

### What the official docs actually say

The `error` field in each `errors[]` entry is typed as a plain `<string>`. There
is no provider-supplied error classification taxonomy or enum. The provider
returns a human-readable error string.

### Resolution

Free-text field is the correct call. There is no provider enum to map.
Open question 12.5 is closed.

`CrawlFailureRecord.errorDetail` should be `text?` (free-text). If VEDA later
wants to classify errors into categories (network, timeout, auth, etc.), that
classification is a VEDA-derived field, not a promotion of a provider-supplied
enum. Any such classification must be governed before implementation adds it.

---

## Correction 3 — `DiscoveryObservation`: add `urlLimit` and `ignoreCache` fields

### What the design pass assumed

`DiscoveryObservation` carried `urlCount` (the number of URLs returned) but did
not capture the request parameters that affect the observation's provenance and
trustworthiness.

### What the official docs actually say

The `/map` endpoint accepts:
- `limit` — maximum URLs to return; official docs show up to **5,000** (the
  repo inventory note did not specify this ceiling)
- `ignoreCache` (boolean, default `false`) — when false, results are primarily
  sourced from sitemap + cached SERP/crawl data; when true, forces a fresher
  lookup

`ignoreCache` directly affects how the observation should be trusted. A map
result with `ignoreCache: false` is more likely to reflect cached state rather
than current site reality. This is provenance-relevant and belongs in the
canonical observation record.

`limit` is the cap applied to the request. Storing both `urlLimit` (what was
requested) and `urlCount` (what came back) allows later analysis to know whether
the result was truncated by the limit.

### Correction to the design pass

Add two fields to `DiscoveryObservation`:

- `urlLimit` (int? — the `limit` parameter sent in the request; null if default
  was used)
- `cacheIgnored` (boolean — whether `ignoreCache: true` was set; false if
  default)

The existing `isComprehensive` field (always false for `/map`) remains correct
and useful as an explicit reminder. `cacheIgnored` adds provenance precision
about whether the result reflects cached state or a fresher lookup.

### Note on the 5,000 URL ceiling

The official docs confirm `/map` supports up to 5,000 URLs. This is an
operational fact relevant to `DiscoveryObservation` interpretation — a result
returning exactly 5,000 URLs may have been truncated by the limit. Implementation
should treat a `urlCount` equal to `urlLimit` as a possible truncation signal,
not as evidence that the domain has exactly that many pages.

---

## Summary of changes required to the design pass

| Section | Change |
|---|---|
| 4.3 `CrawlFailureRecord` | Add `failureClass` discriminator; split `errors[]` vs `robotsBlocked[]` into two sub-types within one family; revise field list |
| 4.3 open question 12.5 | Closed — `error` is free-text, no provider enum |
| 4.4 `DiscoveryObservation` | Add `urlLimit` and `cacheIgnored` fields; note 5,000 URL ceiling |
| Section 9 identity table | Update `CrawlFailureRecord` uniqueness to `(projectId, crawlJobId, pageUrl, failureClass)` |
| Section 10 anti-drift rules | No changes required |
| Section 12 open questions | Remove 12.5 (resolved); 12.1–12.4 remain open |

No other sections of the design pass require correction based on official
Firecrawl docs verification.

---

## What the design pass got right (confirmed by official docs)

The following design pass conclusions are confirmed correct by official docs and
require no correction:

- 24-hour result expiration on crawl jobs — confirmed
- Non-determinism across crawl runs — confirmed
- Errors endpoint is separate from the main crawl status response — confirmed
- `/map` is not comprehensive and primarily uses sitemap + cached data — confirmed
- `/map` `title` and `description` are not authoritative page metadata — confirmed
- `/crawl` per-page families (`markdown`, `html`/`rawHtml`, `metadata`, `links`)
  match the `/scrape` baseline — confirmed
- `CrawlJob` as a distinct family from `CrawledPage` — confirmed by the async
  job model and job-level metadata
- `errorsFetched` flag on `CrawlJob` as a required provenance field — confirmed;
  without it, empty `CrawlFailureRecord` set is ambiguous

---

## Related files

- `transition-steward/batch-h-veda-family-design-pass.md`
- `transition-steward/firecrawl/firecrawl-crawl-map-surface-inventory.md`
- `veda/providers/firecrawl.md`
- `veda/schema-reference.md`

Official sources verified:
- `https://docs.firecrawl.dev/api-reference/endpoint/crawl-get-errors`
- `https://docs.firecrawl.dev/api-reference/endpoint/map`
- `https://docs.firecrawl.dev/api-reference/endpoint/crawl-post`
