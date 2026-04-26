# Firecrawl Inventory — Google SEO Starter Guide Baseline Scrape

## Purpose

This document captures the observable structure of the current Firecrawl baseline sample set for:

- `firecrawl-api-scrape-google-seo-starter-guide-baseline.json`
- `firecrawl-scrape-google-seo-starter-guide-baseline-json.json`
- `firecrawl-scrape-google-seo-starter-guide-baseline-links.json`
- `firecrawl-scrape-google-seo-starter-guide-baseline-markdown.md`

It is a transition-support artifact, not authority doctrine.
It exists to document what Firecrawl actually returned so later VEDA and bucket documentation can be grounded in observed provider structure rather than assumptions.

---

## Sample request profile

Observed target and capture posture:

- Provider: `firecrawl`
- Surface: single-page `scrape`
- Target URL: `https://developers.google.com/search/docs/fundamentals/seo-starter-guide`
- Captured families requested: `markdown`, `links`, `rawHtml`
- Intent: baseline provider-structure inspection
- Not a crawl
- Not a search
- Not structured extraction / prompt-guided JSON

---

## Current baseline artifact set

## 1. Raw API scrape artifact

File:
- `firecrawl-api-scrape-google-seo-starter-guide-baseline.json`

Observed raw API top level:
- `success`
- `data`

Observed `data` families:
- `markdown`
- `rawHtml`
- `metadata`
- `links`

Observed payload scale from the saved sample:
- markdown length: `43250`
- raw HTML length: `426251`
- links count: `101`

### Important finding
This file is the strongest current Firecrawl baseline artifact because it reflects the direct API response shape rather than a Playground session wrapper.

---

## 2. Playground JSON artifact

File:
- `firecrawl-scrape-google-seo-starter-guide-baseline-json.json`

Observed posture:
- this is not the raw API scrape response
- it is a Playground/session wrapper that contains scrape output inside `data`

Observed wrapper families from prior inspection:
- `data`
- `scrape_id`
- `id`
- `startedAt`
- `endedAt`
- `endpoint`
- `formState`
- `status`
- `version`
- `isPreview`

Observed scrape-related families nested inside `data`:
- `markdown`
- `rawHtml`
- `metadata`
- `links`
- plus Playground/request-state fields such as request options and extraction-state fields

### Important finding
This file is useful evidence for UI-mediated behavior, but it must not be treated as canonical Firecrawl API shape.

---

## 3. Markdown export artifact

File:
- `firecrawl-scrape-google-seo-starter-guide-baseline-markdown.md`

Observed behavior:
- preserves substantial page content
- preserves headings and article body
- preserves many inline links
- also captures significant page chrome and UI residue

Observed noise examples:
- duplicated navigation blocks
- duplicated `On this page` sections
- footer/support/resource blocks
- language-selector expansion
- feedback serialization blob beginning with `[[[`
- stray UI remnants such as `Info`, `Chat`, and `API`

### Important finding
Firecrawl markdown is useful as a normalized content representation, but this sample is not clean main-content truth. It over-captures chrome and UI residue.

---

## 4. Links export artifact

File:
- `firecrawl-scrape-google-seo-starter-guide-baseline-links.json`

Observed posture:
- raw link dump
- structurally useful
- not yet classified into internal vs external vs anchors vs chrome

### Important finding
The links family should be treated as observed page link structure, not as a curated semantic graph.

---

## Raw API versus Playground distinction

## Raw API
Current observed direct API response shape:

```json
{
  "success": true,
  "data": {
    "markdown": "...",
    "rawHtml": "...",
    "metadata": { ... },
    "links": [ ... ]
  }
}
```

## Playground
Current saved Playground JSON is a broader session/export wrapper around scrape data.

### Steward rule
For Firecrawl baseline documentation:
- raw API files describe provider response shape
- Playground files describe UI-mediated capture state
- markdown and links exports are derived convenience artifacts, not the canonical provider wrapper

---

## Metadata observations

Observed metadata families in the raw API sample include both page metadata and provider/runtime metadata, including examples such as:

- `description`
- `title`
- `ogUrl`
- `og:url`
- `ogTitle`
- `og:title`
- `ogDescription`
- `og:description`
- `ogImage`
- `og:image`
- `language`
- `favicon`
- `sourceURL`
- `url`
- `statusCode`
- `contentType`
- `proxyUsed`
- `cacheState`
- `cachedAt`
- `creditsUsed`
- `concurrencyLimited`
- `scrapeId`

### Important finding
Firecrawl metadata is a mixed family. It contains both page-observed metadata and scrape/runtime metadata. Those should not be flattened together as if they are the same observational layer.

---

## VEDA versus archive posture

## VEDA-admissible observatory families
Potential observatory families supported by this baseline:
- page content observation
- page link observation
- page metadata observation
- scrape/runtime provenance observation

## Archive / bucket posture
Keep raw provider artifacts because:
- raw API shape matters
- markdown is noisier than canonical observatory truth
- metadata mixes page-level and provider/runtime fields
- links will likely need later classification before any stronger modeling

## Deferred
Still deferred pending more sampling:
- API versus Playground default-parity beyond this one comparison
- whether `onlyMainContent` materially changes content cleanliness for this page family
- whether other Firecrawl surfaces should be admitted into canonical observatory modeling
- any stable schema decisions beyond this baseline scrape family

---

## Most important findings from this sample set

1. The direct Firecrawl API scrape shape is now confirmed.
2. The saved Playground JSON is not the same thing as the raw API response.
3. Firecrawl markdown can preserve real content while also capturing substantial page chrome and UI residue.
4. Firecrawl links are useful raw structural evidence but require later classification.
5. Firecrawl metadata mixes page metadata with scrape/runtime metadata and should be separated conceptually in later modeling.

---

## Steward note

This file is a transition-support interpretation of the current Firecrawl baseline sample set.
It should inform later updates to Firecrawl provider notes, bucket documentation, and future VEDA capture modeling.

It is not itself authority doctrine.
