# Firecrawl Inventory — API Scrape Baseline (Google SEO Starter Guide)

## Purpose

This document captures the observable structure of the Firecrawl baseline scrape artifacts for:

- `firecrawl-api-scrape-google-seo-starter-guide-baseline.json`
- `firecrawl-scrape-google-seo-starter-guide-baseline-json.json`
- `firecrawl-scrape-google-seo-starter-guide-baseline-links.json`
- `firecrawl-scrape-google-seo-starter-guide-baseline-markdown.md`

It is a transition-support artifact, not authority doctrine.
It exists to document what Firecrawl actually returns, what belongs to the raw API response versus the Playground wrapper, and what appears useful for VEDA capture versus raw archive retention.

---

## Sample request posture

Observed baseline target and intent:

- provider: `firecrawl`
- operation: single-page scrape
- target URL: `https://developers.google.com/search/docs/fundamentals/seo-starter-guide`
- requested output families: `markdown`, `links`, `rawHtml`
- no crawl
- no structured extraction prompt/schema
- no screenshots
- no search
- no interact

---

## High-level structural conclusion

The saved direct API artifact is the authoritative baseline for provider-response shape in this sample.

Observed raw API top level:

- `success`
- `data`

Observed raw API `data` families:

- `markdown`
- `rawHtml`
- `metadata`
- `links`

The saved Playground JSON is not the raw Firecrawl API response.
It is a Playground session wrapper that contains the scrape payload inside `data`, plus UI/session fields.

---

## Raw API response shape

### What was observed
The direct API sample returns:

- `success = true`
- `data.markdown`
- `data.rawHtml`
- `data.metadata`
- `data.links`

Observed baseline sizes/counts:

- `markdown` length: `43250`
- `rawHtml` length: `426251`
- `links` count: `101`

### VEDA placement
- **raw provider evidence**
- selective canonicalization candidate

### Notes
This is the cleanest current Firecrawl sample for modeling provider structure because it is not wrapped in Playground session state.

---

## Playground wrapper distinction

### What was observed
The saved Playground JSON adds top-level wrapper/session fields including:

- `scrape_id`
- `id`
- `startedAt`
- `endedAt`
- `endpoint`
- `formState`
- `status`
- `version`
- `isPreview`

Inside `data`, the same main scrape families are present:

- `markdown`
- `rawHtml`
- `metadata`
- `links`

Observed Playground links count:

- `262`

### VEDA placement
- **archive-only transition evidence**

### Important finding
Playground output should not be treated as canonical provider-response shape.
It is useful for transition comparison and exploratory capture only.

---

## `markdown` family behavior

### What was observed
The markdown output contains the main article content, but also substantial page chrome and UI residue, including:

- global site navigation
- repeated section/navigation blocks
- language-selector lists
- footer/support/tooling blocks
- UI residue such as `Info`, `Chat`, and `API`
- preserved page-level facts such as `Last updated 2025-12-10 UTC.`

### VEDA placement
- **archive now, model selectively later**

### Important finding
Firecrawl markdown is useful as a normalized content view, but it is not equivalent to clean main-content truth in this baseline.
It should not be admitted into canonical observatory doctrine as if it were already cleaned page truth.

---

## `rawHtml` family behavior

### What was observed
`rawHtml` is the largest and most source-level artifact in the direct API response.
The paired metadata indicates the scrape preserves page and response facts such as:

- page title/description families
- OG fields
- favicon
- language
- source URL / URL
- HTTP status/content type families
- provider/runtime fields such as `proxyUsed`, `cacheState`, `cachedAt`, `creditsUsed`, and `concurrencyLimited`

### VEDA placement
- **raw provider evidence**
- selective canonicalization candidate

### Important finding
`rawHtml` is the strongest baseline artifact for source-level page capture and later derived parsing.
It is also where provider/runtime metadata distinction must be kept explicit.

---

## `metadata` family behavior

### What was observed
The metadata object mixes page metadata and provider/runtime metadata in one family.
Observed keys include both page-facing values and Firecrawl/runtime fields.
Examples:

Page/meta families:
- `description`
- `title`
- `ogUrl` and `og:url`
- `ogTitle` and `og:title`
- `ogDescription` and `og:description`
- `ogImage` and `og:image`
- `language`
- `favicon`

Provider/runtime families:
- `scrapeId`
- `sourceURL`
- `url`
- `statusCode`
- `contentType`
- `proxyUsed`
- `cacheState`
- `cachedAt`
- `creditsUsed`
- `concurrencyLimited`

### VEDA placement
- **canonical observatory truth, selectively split by family**
- **do not keep as one undifferentiated modeled object**

### Important finding
Metadata normalization will require explicit separation between:

- page-observed metadata
- provider execution/provenance metadata

This should not be flattened blindly into one canonical entity.

---

## `links` family behavior

### What was observed
The direct API response returned `101` links.
The Playground-derived links artifact contains `262` links.
The captured links are broad page-level observations rather than curated semantic links.
They include navigational and utility links in addition to content-relevant links.

### VEDA placement
- **canonical observatory truth, selectively modeled**
- **raw archive retained**

### Important finding
Links are a real observatory family, but they should be treated as observed link emissions, not pre-cleaned relationship truth.
Internal/external, nav/content, anchor, and language-variant distinctions will need later normalization.

---

## Raw archive vs canonical truth recommendation

## Keep raw archive always
Keep all four saved artifacts because together they document:

- raw API provider shape
- Playground wrapper shape
- markdown normalization behavior
- link-output behavior

## Canonicalize selectively in first pass
Good first-pass canonical families from this baseline:

- scrape run provenance
- observed source URL / target URL
- page metadata observations
- provider/runtime execution metadata
- observed link emissions
- raw page-source capture reference

Archive-first / defer:

- treating markdown as already-clean main content
- treating links as already-normalized relationships
- treating Playground wrapper fields as provider doctrine

---

## VEDA vs later bucket/derivation posture

## Belongs in VEDA now
- provider scrape-run provenance
- observed page metadata
- observed link emissions
- retained raw-source capture references

## Bucket/archive support
- full raw API payload
- full raw HTML capture
- full noisy markdown export
- Playground session wrapper artifact

## Later derived work, not baseline doctrine
- main-content extraction cleanup rules
- link-family normalization
- page-content chunking rules
- strategy-layer use of page observations for citation or optimization workflows

---

## Most important findings from this sample

1. The direct API response is cleanly shaped as `success` plus `data`.
2. The actual scrape families observed are `markdown`, `rawHtml`, `metadata`, and `links`.
3. The saved Playground JSON is not raw provider shape; it is a Playground wrapper.
4. Markdown is useful but noisy and should not be treated as already-clean canonical page truth.
5. Metadata mixes page-observed facts and provider/runtime facts and must be split intentionally.
6. Links are a real observatory family, but not a pre-cleaned relationship graph.

---

## Steward note

This file is a transition-support interpretation of the current Firecrawl baseline sample set.
It should inform later updates to Firecrawl transition notes, bucket/capture docs, and VEDA observatory modeling.
It is not itself authority doctrine.
