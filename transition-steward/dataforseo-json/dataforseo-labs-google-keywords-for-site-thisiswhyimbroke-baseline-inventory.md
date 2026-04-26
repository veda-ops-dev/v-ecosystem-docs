# DataForSEO Labs Inventory — Google Keywords For Site Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-labs-google-keywords-for-site-thisiswhyimbroke-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to help VedaOps decide:

- what `keywords_for_site` data belongs in VEDA as canonical observatory truth
- which provider-supplied keyword metrics should be preserved directly
- what variability exists across returned keyword rows
- what later may feed VEDA Strategy as derived intelligence

---

## Sample request profile

Observed request settings in sample payload:

- API family: `dataforseo_labs`
- Search engine: `google`
- Function: `keywords_for_site`
- Target domain: `thisiswhyimbroke.com`
- Location code: `2840`
- Language code: `en`
- `include_subdomains = true`
- `include_serp_info = true`
- `limit = 10`
- `ignore_synonyms = false`
- `include_clickstream_data = false`

Important implication:
this is a domain-scoped keyword discovery sample with embedded keyword metrics, SERP context, backlink summaries, and search-intent classification.

---

## High-level structural conclusions

1. `keywords_for_site` is not just a keyword list. Each row is a multi-part keyword observatory record.
2. The result root includes pagination state through `offset` and `offset_token`, which means this surface is designed for deep traversal rather than one-shot sampling.
3. Returned keyword rows can vary materially in completeness:
   - some rows include populated `serp_info` and `avg_backlinks_info`
   - some rows have `serp_info = null`
   - some rows have `serp_info` present but mostly null-valued internals
   - some rows have `keyword_difficulty = null`
4. This surface clearly combines multiple provider families into one row shape:
   - keyword metrics
   - keyword properties
   - SERP context
   - backlink context
   - intent classification
5. This is a strong Phase 1 surface for VEDA because it shows domain-relevant keyword discovery without requiring VEDA Strategy to infer relevance from scratch.

---

## Result-root structure

### What was observed
The result root includes:
- `se_type`
- `target`
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
The root should likely be treated as a domain-keyword-discovery observation run.
`offset_token` is especially important because it signals this endpoint is intended to support continued retrieval of a large result set.

---

## Observed row families and placement guidance

## A. Keyword discovery row

### What was observed
Each item row includes:
- `keyword`
- target/location/language context
- `keyword_info`
- `keyword_properties`
- `serp_info`
- `avg_backlinks_info`
- `search_intent_info`
- optional normalized/clickstream blocks (null in this sample)

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This is the core row family for `keywords_for_site`.
It should likely be modeled as a domain-scoped keyword observation, not as a raw keyword string list.

---

## B. Keyword metrics (`keyword_info`)

### What was observed
`keyword_info` includes provider-supplied metrics such as:
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
This confirms VEDA does not need to invent baseline keyword metric fields when the provider already gives them.
These are provider observations or provider-computed metrics and should be preserved as named observatory fields.

### Notes
The `monthly_searches` array and `search_volume_trend` object are especially valuable because they show trend/time-shape, not just a single scalar.

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
This sample confirms `keyword_difficulty` appears as a provider-supplied field in this surface and may be:
- populated with numeric values
- populated with `0`
- `null`

That means downstream logic must not assume it is always present or always meaningful without context.

### Notes
`keyword_difficulty` should be preserved directly in VEDA, but not treated as VEDA’s own strategic score.

---

## D. SERP context (`serp_info`)

### What was observed
When populated, `serp_info` includes:
- `check_url`
- `serp_item_types`
- `se_results_count`
- `last_updated_time`
- `previous_updated_time`

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This sample is especially useful because `serp_info` varies across rows:
- some rows have rich SERP context
- some rows have null SERP context
- some rows have a partial object with null-valued internals

This means `include_serp_info = true` does not guarantee uniformly complete SERP context per row.

### Notes
`serp_item_types` is valuable because it gives VEDA a lightweight SERP-feature signature for a keyword without requiring a full SERP pull for every row.

---

## E. Average backlink context (`avg_backlinks_info`)

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

### Important finding
This sample confirms that `keywords_for_site` rows can embed lightweight authority context from backlink-style metrics.
That is powerful because it ties keyword discovery to a rough competitive-authority posture in one surface.

### Notes
These should be preserved as provider-supplied authority context, not treated as recommendations.

---

## F. Search intent (`search_intent_info`)

### What was observed
`search_intent_info` includes:
- `main_intent`
- `foreign_intent`
- `last_updated_time`

Observed values in this sample include combinations like:
- commercial + transactional
- transactional + commercial
- transactional only
- commercial only

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Important finding
This sample strengthens the case for preserving provider-supplied intent classification directly in VEDA.
It is not VEDA’s job to reinterpret intent at capture time.

---

## G. Normalized/clickstream fields

### What was observed
These fields are present in the row shape but null throughout this sample:
- `keyword_info_normalized_with_bing`
- `keyword_info_normalized_with_clickstream`
- `clickstream_keyword_info`

### VedaOps placement
- **Deferred pending more samples**

### Important finding
This sample confirms the structural slots already exist even when clickstream is disabled.
That means a later clickstream-enabled sample will be directly comparable against this baseline.

### Notes
Do not model these yet from null-only evidence.
Capture the clickstream expansion sample first.

---

## What this sample adds to VedaOps understanding

This sample proves that `keywords_for_site` is one of the strongest Phase 1 Labs surfaces because it combines:
- domain-relevant keyword discovery
- baseline keyword metrics
- trend data
- intent classification
- lightweight SERP feature signatures
- lightweight backlink/authority context

It also shows important variability and missingness, which is equally useful:
- row completeness is uneven
- provider metrics are not guaranteed to be populated uniformly
- `serp_info` and backlink context cannot be assumed present on every row

That makes this a strong observatory surface, but also one that needs conservative schema thinking later.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
Reasons:
- this surface combines multiple embedded provider subfamilies
- row completeness varies
- pagination state matters
- future clickstream-enabled comparison will benefit from untouched baseline payloads

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:
- domain keyword discovery run root
- discovered keyword row
- provider keyword metrics
- provider keyword properties
- SERP context signature
- backlink/authority context
- provider intent classification

Archive-first / defer:
- clickstream-normalized objects until sampled
- assumptions about category taxonomy meaning
- any deep synonym-clustering doctrine beyond preserving the field values

---

## VEDA vs VEDA Strategy placement summary

## Belongs in VEDA now
- target-domain keyword discovery observations
- provider keyword metrics
- provider keyword difficulty
- provider trend arrays
- SERP feature signatures
- provider backlink/authority context
- provider intent classification
- pagination state (`offset`, `offset_token`) as observation-run metadata

## Later may feed VEDA Strategy
- opportunity scoring
- keyword prioritization
- gap identification
- cluster formation
- difficulty-vs-demand interpretation
- SERP-feature-aware opportunity analysis

## Must not be done inside VEDA
- deciding which discovered keywords are strategically best
- scoring opportunities from this surface alone
- converting provider difficulty/intent into VEDA-native strategic conclusions

---

## Most important findings from this sample

1. `keywords_for_site` is a compound keyword observatory surface, not a simple suggestion list.
2. Each row can carry metrics, intent, SERP context, and backlink context together.
3. Row completeness varies materially; null handling will matter later.
4. Provider-supplied keyword difficulty is available here and should be preserved directly.
5. The clickstream/normalized fields exist structurally even when disabled, making later comparison clean.
6. `offset_token` confirms this surface is designed for large-scale traversal and should be treated as such.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `veda/providers/dataforseo-ai-optimization.md`
- `veda/schema-reference.md`
- future Labs and keyword-observability doctrine

It is not itself authority doctrine.
