# Firecrawl Transition Notes

## Purpose

This folder holds transition-support Firecrawl samples and inventory notes.
It exists to document observed provider behavior so later VEDA capture and bucket/archive docs can be grounded in real payload structure.

This folder is not authority doctrine.
It is a steward workspace for sample evidence, payload inspection, and capture-boundary decisions.

---

## Current baseline set

### Primary raw API artifact
- `firecrawl-api-scrape-google-seo-starter-guide-baseline.json`

This is the current source-of-truth sample for direct Firecrawl scrape response shape in this folder.

Observed top level:
- `success`
- `data`

Observed scrape families inside `data`:
- `markdown`
- `rawHtml`
- `metadata`
- `links`

### Supporting exploratory artifacts
- `firecrawl-scrape-google-seo-starter-guide-baseline-json.json`
- `firecrawl-scrape-google-seo-starter-guide-baseline-links.json`
- `firecrawl-scrape-google-seo-starter-guide-baseline-markdown.md`

These are useful transition artifacts, but they are not the canonical raw API wrapper.
In particular, the saved Playground JSON is a UI/session wrapper around scrape data, not the raw direct API response.

---

## Current inventory notes

### Primary inventory
- `firecrawl-api-scrape-google-seo-starter-guide-baseline-inventory.md`

Use this as the current primary interpretation of the baseline set.
It documents:
- raw API shape
- Playground wrapper distinction
- markdown noise
- metadata mixing
- links-family posture
- VEDA versus archive placement

### Earlier baseline note
- `firecrawl-scrape-google-seo-starter-guide-baseline-inventory.md`

Keep for transition continuity, but treat the API baseline inventory as the more authoritative steward note because it is anchored explicitly to the direct API artifact.

---

## Current Firecrawl posture

### Settled enough for transition use
- direct API scrape shape is now observed
- direct API response family includes `markdown`, `rawHtml`, `metadata`, and `links`
- Playground wrapper output must not be treated as provider-response doctrine
- markdown is useful but noisy
- metadata contains both page-observed facts and provider/runtime facts
- links are observed emissions, not a pre-cleaned relationship graph

### Still deferred
- broader API/default parity questions beyond this baseline
- cleaner main-content extraction posture
- stable link normalization rules
- admission of any additional Firecrawl surfaces into canonical VEDA modeling

---

## VEDA and bucket guidance from the current baseline

### Good VEDA candidates
- scrape-run provenance
- observed page metadata
- observed link emissions
- retained source URL / page-source capture references

### Keep raw/archive always
- full raw API payload
- full raw HTML capture
- noisy markdown export
- Playground wrapper artifact

### Do not do yet
- treat markdown as already-clean canonical page truth
- treat links as already-normalized semantic relationships
- treat Playground wrapper fields as provider doctrine

---

## Steward rule for future Firecrawl samples

When a new Firecrawl sample is added:
1. inspect the actual payload
2. verify whether it is direct API output or UI-mediated export
3. identify the returned families
4. note what is page observation versus provider/runtime metadata
5. update the matching inventory note before broadening doctrine

---

## Current baseline target

Observed baseline target:
- `https://developers.google.com/search/docs/fundamentals/seo-starter-guide`

Observed intent:
- single-page scrape
- provider-structure inspection
- not crawl
- not search
- not structured extraction

---

## Steward note

This folder should stay repo-first, sample-grounded, and conservative.
Do not harden Firecrawl doctrine from Playground behavior alone when direct API evidence is available.
