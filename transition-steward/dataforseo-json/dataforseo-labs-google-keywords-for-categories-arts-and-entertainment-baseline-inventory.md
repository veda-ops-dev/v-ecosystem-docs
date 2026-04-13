# DataForSEO Labs Inventory — Google Keywords For Categories Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-labs-google-keywords-for-categories-arts-and-entertainment-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to help VedaOps decide:

- what `keywords_for_categories` data belongs in VEDA as canonical observatory truth
- how this surface differs from other Labs keyword-discovery surfaces
- what the endpoint appears to use as category-scoped relevance
- what later may feed VEDA Strategy as derived intelligence

---

## Sample request profile

Observed request settings in sample payload:

- API family: `dataforseo_labs`
- Search engine: `google`
- Function: `keywords_for_categories`
- Category code: `10013`
- Location code: `2840`
- Language code: `en`
- `include_serp_info = false`
- `category_intersection = true`
- `limit = 25`
- `offset = 0`
- `ignore_synonyms = false`
- `include_clickstream_data = false`

Important implication:
this is a category-scoped keyword discovery sample, not a domain-scoped sample and not a single-keyword overview sample.
It is also a deliberately reduced baseline because SERP info and clickstream were disabled.

---

## High-level structural conclusions

1. `keywords_for_categories` is a real distinct discovery surface.
2. The result root includes pagination state through both `offset` and `offset_token`, which signals intended deep traversal rather than one-shot use.
3. Each returned row is a compound keyword observation, not a simple string list.
4. This sample does **not** expose SERP context because `include_serp_info = false`, so any SERP-family conclusions must remain deferred.
5. The broad category choice plus default volume-first retrieval yields many very large navigational and typo-heavy queries. That is useful for understanding the endpoint, but not evidence that the returned rows are immediately high-quality strategic targets.

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
This should likely be treated as a category-keyword discovery observation run.
`offset_token` is especially important because it confirms the endpoint is built for traversal across a very large result set.

---

## A. Keyword discovery row

### What was observed
Each item row includes:
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
This is the core row family for the endpoint.
It should be modeled as a category-scoped keyword observation, not as a strategy artifact.

---

## B. Keyword metrics (`keyword_info`)

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

### Important finding
This confirms the endpoint carries the same core provider keyword-metric family seen in other Labs keyword surfaces.
The row is not category label plus keyword only; it is already a provider-metric-bearing keyword record.

### Notes
Preserve `monthly_searches` and `search_volume_trend` directly.
Do not collapse them prematurely.

---

## C. Keyword properties (`keyword_properties`)

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
This sample shows strong row variation:
- some rows have non-null `keyword_difficulty`
- some rows have `keyword_difficulty = null`
- some rows are marked `is_another_language = true`
- some rows are clearly typo / variant / navigational forms

That means downstream logic must treat this surface conservatively.

---

## D. Category association signal

### What was observed
The most visible category association evidence in the row shape is:
- `seed_categories` at the result root
- `keyword_info.categories` per row

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This sample does not expose any explicit category relevance score or rationale field.
So at present, the observable category-linking posture appears to be:
- requested seed category set
- provider-returned category arrays per keyword

### Notes
That is enough to preserve observatory truth, but not enough to assume strong semantic purity of the results.

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

Some rows have this block populated.
Some rows have it null.

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Notes
Preserve it as provider authority context, not as recommendation logic.

---

## F. Search intent (`search_intent_info`)

### What was observed
`search_intent_info` includes:
- `main_intent`
- `foreign_intent`
- `last_updated_time`

Observed values in this sample include:
- navigational
- informational
- transactional
- mixed foreign-intent combinations

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Notes
Preserve the provider intent classification directly.
Do not reinterpret it inside VEDA.

---

## G. SERP context (`serp_info`)

### What was observed
`serp_info = null` for all rows in this sample.

### Why
This matches the request posture:
- `include_serp_info = false`

### VedaOps placement
- **Deferred pending more samples**

### Notes
Do not model SERP context from this sample.
A later expansion sample with `include_serp_info = true` is required.

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
This is useful baseline evidence for later clickstream-enabled comparison.
Do not model these yet.

---

## What this sample teaches about endpoint behavior

This particular sample is useful mainly for **shape** and **caution**, not for clean strategic targeting.

Why:
- the category is broad
- `category_intersection = true`
- the retrieval appears volume-heavy
- the returned rows include many typo, brand, and navigational head terms

So the main lesson is:
`keywords_for_categories` can return category-associated keywords with full metric families, but a broad category baseline can produce noisy head-term discovery rather than a neatly curated opportunity list.

That does **not** make the endpoint bad.
It means the endpoint needs more disciplined sampling before doctrine hardens.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
Reasons:
- this is a distinct discovery surface
- pagination state matters
- row quality and category purity need later comparison
- a later SERP-enabled or clickstream-enabled expansion will benefit from comparison against this baseline

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:
- category-keyword discovery run root
- discovered keyword row
- provider keyword metrics
- provider keyword properties
- provider category arrays
- provider backlink context
- provider intent classification
- pagination state (`offset`, `offset_token`)

Archive-first / defer:
- SERP context until sampled
- clickstream-normalized objects until sampled
- any assumption that broad-category head terms are strategically useful just because the endpoint returned them
- any doctrine claiming strong category precision from this one sample

---

## VEDA vs VEDA Strategy placement summary

## Belongs in VEDA now
- category-scoped keyword discovery observations
- provider keyword metrics
- provider keyword properties
- provider category arrays
- provider backlink context
- provider intent classification
- traversal metadata (`offset`, `offset_token`)

## Later may feed VEDA Strategy
- category-level opportunity prioritization
- category-family filtering and cleanup
- intent-aware category segmentation
- noise-vs-signal classification across category pulls

## Must not be done inside VEDA
- deciding which category keywords are strategically best
- treating search volume alone as strategic value
- interpreting typo-heavy or navigational-heavy returns as immediate target recommendations

---

## Most important findings from this sample

1. `keywords_for_categories` is a real distinct Labs surface.
2. It returns compound keyword rows with metrics, properties, backlink context, and intent.
3. `offset_token` confirms this surface is meant for deep traversal.
4. This baseline does not tell us anything about SERP context because SERP info was disabled.
5. Broad category sampling can produce noisy high-volume head terms, including typo and navigational queries.
6. The surface is worth keeping, but category precision should remain a transition question until more samples are reviewed.

---

## Recommended next sample posture

To understand this endpoint better, the next most useful follow-up would be one of these:

1. a narrower category pull
2. a repeat pull with `include_serp_info = true`
3. a commerce-heavier category comparison

Any of those would help determine whether the current noise profile is caused mainly by the category choice, the sort behavior, or the endpoint itself.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `veda/schema-reference.md`
- future Labs and category-keyword observability doctrine

It is not itself authority doctrine.
