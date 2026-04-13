# DataForSEO Labs Inventory — Google Keyword Overview (`seo`) Comparison Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-labs-google-keyword-overview-seo-comparison-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to compare a second keyword-level `keyword_overview` sample against the existing `gifts for men` baseline and to document what a broad, noisy keyword looks like in this endpoint.

---

## Sample request profile

Observed request settings in sample payload:

- API family: `dataforseo_labs`
- Search engine: `google`
- Function: `keyword_overview`
- Keyword: `seo`
- Location code: `2840`
- Language code: `en`
- `include_serp_info = true`
- `include_clickstream_data = false`

---

## High-level structural conclusions

1. The endpoint shape is consistent with the earlier `keyword_overview` sample.
2. This is a good comparison sample because `seo` is broad and noisy.
3. The payload confirms that `keyword_overview` can carry a strong SERP feature signature for a single keyword.
4. This sample reinforces that provider classifications can be surprising or counterintuitive and must be preserved as observed, not rewritten inside VEDA.

---

## Result-root structure

### What was observed
The result root includes:
- `location_code`
- `language_code`
- `items_count`
- `items[]`

### VedaOps placement
- **VEDA canonical observatory truth**

---

## A. Keyword overview row

### What was observed
The row includes:
- `keyword`
- `search_partners`
- `keyword_info`
- `keyword_properties`
- `serp_info`
- `avg_backlinks_info`
- `search_intent_info`
- normalized/clickstream slots

### VedaOps placement
- **VEDA canonical observatory truth**

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

Notable observed values:
- `search_volume = 135000`
- `cpc = 18.71`
- long monthly history is present

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This remains a strong keyword-metric observatory family and confirms the endpoint preserves long monthly history, not just a scalar volume.

---

## C. Keyword properties (`keyword_properties`)

### What was observed
`keyword_properties` includes:
- `core_keyword`
- `synonym_clustering_algorithm`
- `keyword_difficulty`
- `detected_language`
- `is_another_language`

Notable observed values:
- `keyword_difficulty = 100`
- `detected_language = id`
- `is_another_language = true`

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Important finding
This sample is a good reminder that provider language detection and difficulty outputs can look odd on very broad terms. Preserve them as provider output; do not reinterpret them inside VEDA.

---

## D. SERP context (`serp_info`)

### What was observed
`serp_info` includes:
- `check_url`
- `serp_item_types`
- `se_results_count`
- `last_updated_time`
- `previous_updated_time`

Observed `serp_item_types` include:
- `ai_overview`
- `organic`
- `people_also_ask`
- `product_considerations`
- `video`
- `related_searches`
- `images`

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This is one of the more useful observations from the sample. The term `seo` carries a rich SERP feature mix, including `ai_overview`, which makes it a useful comparison keyword even though it is strategically noisy.

---

## E. Backlink context (`avg_backlinks_info`)

### What was observed
`avg_backlinks_info` includes:
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

---

## F. Intent classification (`search_intent_info`)

### What was observed
`search_intent_info` includes:
- `main_intent`
- `foreign_intent`
- `last_updated_time`

Observed value:
- `main_intent = navigational`

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Important finding
For a term like `seo`, this provider intent classification can feel unintuitive, but that is exactly why it is useful as a comparison sample.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
Reasons:
- good second comparison sample for keyword overview
- broad term with rich SERP shape
- useful for comparing provider classifications on noisier keywords

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:
- keyword overview observation row
- provider keyword metrics
- provider keyword properties
- provider SERP context
- provider backlink context
- provider intent classification

Archive-first / defer:
- any attempt to turn this broad keyword into direct strategy inside VEDA
- any reinterpretation of provider language detection or intent labels

---

## Most important findings from this sample

1. `keyword_overview` shape remains stable.
2. `seo` is a useful structural comparison keyword because it is broad and noisy.
3. The sample confirms `ai_overview` can appear in keyword-level `serp_info` here.
4. Provider intent and language detection should be preserved as observed, even when they look odd.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `veda/schema-reference.md`

It is not itself authority doctrine.
