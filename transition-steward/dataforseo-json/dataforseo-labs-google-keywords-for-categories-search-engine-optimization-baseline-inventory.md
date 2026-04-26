# DataForSEO Labs Inventory — Google Keywords For Categories (Search Engine Optimization) Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-labs-google-keywords-for-categories-search-engine-optimization-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to help VedaOps decide:

- what `keywords_for_categories` data belongs in VEDA as canonical observatory truth
- whether a narrower category reduces the noise seen in the broad Arts & Entertainment baseline
- what additional comparison pulls are still needed before any category-keyword doctrine hardens

---

## Sample request profile

Observed request settings in sample payload:

- API family: `dataforseo_labs`
- Search engine: `google`
- Function: `keywords_for_categories`
- Category code: `13316`
- Category label used in UI: `Search Engine Optimization`
- Location code: `2840`
- Language code: `en`
- `include_serp_info = false`
- `category_intersection = true`
- `order_by = ["keyword_info.search_volume,desc"]`
- `limit = 10`
- `offset = 0`
- `ignore_synonyms = false`
- `include_clickstream_data = false`

Important note:
although the intended test posture was to disable category intersection for a single-category pull, the actual saved payload shows `category_intersection = true`. This file documents the actual payload, not the intended setting.

---

## High-level structural conclusions

1. This is the same `keywords_for_categories` endpoint family already seen in the Arts & Entertainment baseline.
2. The endpoint shape is consistent: root traversal metadata plus compound keyword rows.
3. The narrower category does **not** eliminate noisy high-volume returns.
4. Returned rows remain a mix of:
   - SEO-adjacent terms
   - generic web / website terms
   - navigational brand terms
   - clearly off-target or weakly related rows
5. This confirms that a narrower category alone does not yet guarantee clean strategic targeting.

---

## Result-root structure

### What was observed
The result root includes:
- `seed_categories`
- `location_code`
- `language_code`
- `total_count`
- `items_count`
- `offset`
- `offset_token`
- `items[]`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
The root again behaves like a category-keyword discovery observation run.
`total_count = 362108` indicates a large traversable result set even for this narrower category.

---

## A. Keyword discovery row

### What was observed
Each row includes:
- `keyword`
- location/language context
- `keyword_info`
- `keyword_properties`
- `serp_info`
- `avg_backlinks_info`
- `search_intent_info`
- normalized/clickstream slots

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This matches the prior category baseline and confirms a stable row family for the endpoint.

---

## B. Provider keyword metrics (`keyword_info`)

### What was observed
`keyword_info` includes:
- `competition`
- `competition_level`
- `cpc`
- `search_volume`
- `low_top_of_page_bid`
- `high_top_of_page_bid`
- `categories`
- `monthly_searches`
- `search_volume_trend`
- `last_updated_time`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This confirms the endpoint continues to return the standard Labs keyword metric family for each discovered row.

---

## C. Provider keyword properties (`keyword_properties`)

### What was observed
`keyword_properties` includes:
- `core_keyword`
- `synonym_clustering_algorithm`
- `keyword_difficulty`
- `detected_language`
- `is_another_language`
- `words_count`

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Important finding
The sample still contains noisy variation:
- some rows are marked `is_another_language = true`
- some rows are strongly navigational
- some rows look only weakly SEO-related despite the narrower category

That means this endpoint still requires downstream filtering or additional comparison sampling before strategic use.

---

## D. Category association evidence

### What was observed
Category association appears through:
- root `seed_categories = [13316]`
- row-level `keyword_info.categories[]`, which often includes `13316` among several other category codes

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
Rows are multi-category, not exclusive to SEO.
This matters because it helps explain why the result set can still drift into broader web, site, or brand-adjacent territory.

---

## E. Backlink context (`avg_backlinks_info`)

### What was observed
When present, `avg_backlinks_info` includes:
- `backlinks`
- `dofollow`
- `referring_pages`
- `referring_domains`
- `referring_main_domains`
- `rank`
- `main_domain_rank`
- `last_updated_time`

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Notes
This remains a provider authority-context family, not recommendation logic.

---

## F. Search intent (`search_intent_info`)

### What was observed
`search_intent_info` includes:
- `main_intent`
- `foreign_intent`
- `last_updated_time`

Observed values in this sample include:
- informational
- navigational
- mixed foreign-intent combinations

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Notes
Intent remains useful as provider classification, but this sample reinforces that provider intent alone does not rescue category precision.

---

## G. SERP context (`serp_info`)

### What was observed
`serp_info = null` for all rows in this sample.

### Why
The payload confirms:
- `include_serp_info = false`

### VedaOps placement
- **Deferred pending more samples**

### Notes
A SERP-info-enabled comparison sample is still needed.

---

## H. Clickstream / normalized fields

### What was observed
The sample includes null-only structural slots for:
- `keyword_info_normalized_with_bing`
- `keyword_info_normalized_with_clickstream`
- `clickstream_keyword_info`

### VedaOps placement
- **Deferred pending more samples**

### Notes
Do not model these yet.

---

## What this sample teaches compared with Arts & Entertainment

The narrower SEO category improves the experiment in one important way:
- it confirms the earlier noise problem was **not only** caused by a gigantic broad category

But it does **not** fully solve the problem.
This sample still returns rows such as:
- generic brand / site navigational terms
- ambiguous web terms
- terms that are only loosely tied to SEO as a strategic domain

So the current working conclusion is:
`keywords_for_categories` is a real observatory surface, but category membership alone is not a reliable proxy for high-quality project targeting.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
Reasons:
- stable endpoint family
- useful comparison against the broad-category baseline
- confirms row shape consistency and category-noise risk

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:
- category-keyword discovery run root
- discovered keyword row
- provider keyword metrics
- provider keyword properties
- provider category arrays
- provider backlink context
- provider intent classification
- traversal metadata (`offset`, `offset_token`)

Archive-first / defer:
- SERP context until sampled
- clickstream fields until sampled
- any assumption that narrower category choice is enough to produce strategically clean rows
- any strategy-layer interpretation of these rows inside VEDA

---

## VEDA vs VEDA Strategy placement summary

## Belongs in VEDA now
- category-scoped keyword discovery observations
- provider keyword metrics
- provider keyword properties
- provider category arrays
- provider backlink context
- provider intent classification
- traversal metadata

## Later may feed VEDA Strategy
- category cleanup and relevance scoring
- strategic filtering of noisy category returns
- intent-aware and authority-aware prioritization
- cross-category comparison work

## Must not be done inside VEDA
- assuming category membership equals strategic relevance
- using raw search volume as final project value
- treating this surface as a ready-made target list

---

## Most important findings from this sample

1. The endpoint shape is stable across categories.
2. A narrower SEO category still returns noisy rows.
3. Multi-category row membership is likely part of the reason for that noise.
4. A SERP-info-enabled comparison is still the next most useful low-cost follow-up.
5. This surface remains useful for observatory intake, but not yet reliable as direct strategic targeting input.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `veda/schema-reference.md`
- future Labs and category-keyword observability doctrine

It is not itself authority doctrine.
