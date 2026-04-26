# DataForSEO Labs Inventory — Google Keywords For Categories (Search Engine Optimization) SERP-Info Comparison

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-labs-google-keywords-for-categories-search-engine-optimization-serp-info.json`

It is a transition-support artifact, not authority doctrine.
It exists to document what changes when `include_serp_info = true` is enabled for the same category baseline already captured for:

- `dataforseo-labs-google-keywords-for-categories-search-engine-optimization-baseline.json`

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
- `include_serp_info = true`
- `category_intersection = true`
- `order_by = ["keyword_info.search_volume,desc"]`
- `limit = 10`
- `offset = 0`
- `ignore_synonyms = false`
- `include_clickstream_data = false`

Important note:
this is a valid apples-to-apples comparison against the saved SEO baseline because the effective settings match except for `include_serp_info`.

---

## High-level structural conclusion

Enabling `include_serp_info` did **not** materially change the discovered keyword set in this comparison sample.

It **did** add a populated `serp_info` object to each returned row.

So this sample is best understood as:

- same category-discovery row family
- same noisy keyword-return behavior
- plus one new keyword-level SERP context family

---

## What stayed the same vs the baseline

The following appear unchanged relative to the saved SEO baseline:

- same endpoint family
- same category code
- same location/language
- same traversal shape
- same row families:
  - `keyword_info`
  - `keyword_properties`
  - `avg_backlinks_info`
  - `search_intent_info`
- same `total_count = 362108`
- same `items_count = 10`
- same general top-row ordering and same overall noise problem

### Important finding
This means `include_serp_info` is not acting like a different discovery algorithm in this sample.
It is acting like an enrichment toggle on top of the same discovered keyword rows.

---

## New row family: `serp_info`

### What was observed
When enabled, each row now includes a populated `serp_info` object with:

- `check_url`
- `serp_item_types`
- `se_results_count`
- `last_updated_time`
- `previous_updated_time`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This is a useful observatory enrichment family because it gives keyword-level SERP feature signatures without requiring a separate full SERP pull for every discovered keyword.

---

## SERP feature signature behavior

### What was observed
`serp_item_types` varies by keyword and can include combinations such as:

- `organic`
- `people_also_ask`
- `related_searches`
- `knowledge_graph`
- `local_pack`
- `product_considerations`
- `popular_products`
- `top_sights`
- `perspectives`
- `people_also_search`
- `video`

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This is the main added value of the SERP-info comparison.
It confirms the endpoint can provide lightweight keyword-level SERP feature signatures even when the discovered rows themselves remain noisy.

---

## What did not improve

The sample still returns weakly aligned rows, including:

- generic navigational brand queries
- ambiguous web/site terms
- clearly off-target terms for practical SEO project targeting

### Important finding
Turning on `include_serp_info` did **not** solve the category-noise problem.
It only added context about the SERP shape of those returned rows.

---

## Cost observation

### What was observed
This sample cost `0.011`, which matches the paired non-SERP-info SEO baseline sample.

### Steward note
That is useful in practice because it means this particular comparison added row-level SERP context without an obvious cost increase in the observed payload pair.
Do not generalize that too far beyond this exact comparison without more evidence.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
Reasons:
- this is the clean comparison pair for the SEO-category baseline
- it proves the structural effect of `include_serp_info`
- it adds a real new observatory family at low apparent cost

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:
- category-keyword discovery run root
- discovered keyword row
- provider keyword metrics
- provider keyword properties
- provider category arrays
- provider backlink context
- provider intent classification
- traversal metadata
- keyword-level `serp_info`
- keyword-level SERP feature signature (`serp_item_types`)
- keyword-level SERP results count and update timestamps

Archive-first / defer:
- any strategy-layer attempt to treat these rows as clean target candidates
- any assumption that category narrowing plus SERP info is sufficient for direct project selection

---

## VEDA vs VEDA Strategy placement summary

## Belongs in VEDA now
- category-scoped keyword discovery observations
- provider keyword metrics and properties
- provider category arrays
- provider backlink context
- provider intent classification
- keyword-level lightweight SERP context
- keyword-level feature-family signatures

## Later may feed VEDA Strategy
- filtering noisy category rows using SERP feature evidence
- identifying which discovered rows show commercial or opportunity-rich SERP shapes
- category-level relevance cleanup

## Must not be done inside VEDA
- treating the returned row set as a ready-made project target list
- converting SERP feature presence into recommendations inside the observatory layer

---

## Most important findings from this sample

1. `include_serp_info = true` adds a real new observatory family.
2. The discovered row set stayed effectively the same in this comparison.
3. The endpoint's category-noise problem remains.
4. Lightweight SERP feature signatures are now confirmed for this endpoint.
5. This comparison was worth capturing because it isolated one setting cleanly.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `veda/schema-reference.md`
- future Labs and category-keyword observability doctrine

It is not itself authority doctrine.
