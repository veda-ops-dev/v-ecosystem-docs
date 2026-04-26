# DataForSEO Labs Inventory — Google Keyword Overview Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-labs-google-keyword-overview-gifts-for-men-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to help VedaOps decide:

- what `keyword_overview` data belongs in VEDA as canonical observatory truth
- which provider-supplied keyword metrics should be preserved directly
- how this endpoint differs from `keywords_for_site`
- what later may feed VEDA Strategy as derived intelligence

---

## Sample request profile

Observed request settings in sample payload:

- API family: `dataforseo_labs`
- Search engine: `google`
- Function: `keyword_overview`
- Keyword: `gifts for men`
- Location code: `2840`
- Language code: `en`
- `include_serp_info = true`
- `include_clickstream_data = false`

Important implication:
this is a direct keyword-centric provider metrics sample, not a domain discovery sample.
It gives a focused view of one keyword with embedded metrics, SERP context, backlink context, and intent classification.

---

## High-level structural conclusions

1. `keyword_overview` is a compact single-keyword observatory surface.
2. The row shape is closely related to `keywords_for_site`, but the result root is simpler because there is no domain target, pagination token, or large discovery-run framing.
3. This sample confirms that a keyword overview can carry:
   - keyword metrics
   - long historical monthly search arrays
   - trend summary
   - keyword difficulty
   - SERP feature signature
   - backlink/authority context
   - intent classification
4. This sample is ideal for preserving provider-supplied baseline metrics without mixing them with domain relevance logic.

---

## Result-root structure

### What was observed
The result root includes:
- `se_type`
- `location_code`
- `language_code`
- `items_count`
- `items[]`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This should likely be treated as a keyword overview observation run.
It is much simpler than `keywords_for_site` because it is not a paginated discovery surface.

---

## Observed row families and placement guidance

## A. Keyword overview row

### What was observed
The returned row includes:
- `keyword`
- location/language context
- `search_partners`
- `keyword_info`
- `keyword_properties`
- `serp_info`
- `avg_backlinks_info`
- `search_intent_info`
- optional normalized/clickstream fields (null in this sample)

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This is the core keyword overview observation record.
It should be treated as a keyword-level observatory row, not as a strategy artifact.

---

## B. Keyword metrics (`keyword_info`)

### What was observed
`keyword_info` includes:
- `last_updated_time`
- `competition`
- `competition_level`
- `cpc`
- `search_volume`
- `low_top_of_page_bid`
- `high_top_of_page_bid`
- `categories`
- `monthly_searches`
- `search_volume_trend`

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This sample shows a very long `monthly_searches` history extending across multiple years, not just the recent 12-month window seen in some other surfaces.
That means `keyword_overview` is valuable not only for current metrics but also for long-horizon seasonality and recurring peak analysis.

### Notes
This strengthens the case that VEDA should preserve provider trend arrays directly rather than collapsing them immediately into one score.

---

## C. Keyword properties (`keyword_properties`)

### What was observed
`keyword_properties` includes:
- `core_keyword`
- `synonym_clustering_algorithm`
- `keyword_difficulty`
- `detected_language`
- `is_another_language`

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Important finding
This sample shows `keyword_difficulty = 0` for a very large keyword.
That is important because it reinforces an earlier lesson:
provider difficulty should be preserved, but not naively trusted as a complete strategic ranking score without context.

### Notes
Preserve provider difficulty directly.
Do not reinterpret it inside VEDA.

---

## D. SERP context (`serp_info`)

### What was observed
`serp_info` includes:
- `check_url`
- `serp_item_types`
- `se_results_count`
- `last_updated_time`
- `previous_updated_time`

Observed `serp_item_types` in this sample:
- `ai_overview`
- `organic`
- `popular_products`
- `perspectives`
- `people_also_ask`
- `related_searches`
- `images`

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This is a strong example of why `include_serp_info = true` is useful in Labs sampling.
It gives a lightweight feature-family signature for the keyword without requiring a separate full SERP pull just to know the surface mix.

---

## E. Average backlink context (`avg_backlinks_info`)

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

### Notes
This confirms `keyword_overview` can provide a compact authority-context layer alongside core keyword metrics.
That is useful observatory enrichment, but it remains provider context, not strategy.

---

## F. Search intent (`search_intent_info`)

### What was observed
`search_intent_info` includes:
- `main_intent`
- `foreign_intent`
- `last_updated_time`

This sample reports:
- `main_intent = commercial`
- `foreign_intent = null`

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Notes
This surface is useful because it gives VEDA a provider intent label directly tied to the keyword overview row.

---

## G. Normalized/clickstream fields

### What was observed
These fields are present but null in this sample:
- `keyword_info_normalized_with_bing`
- `keyword_info_normalized_with_clickstream`
- `clickstream_keyword_info`

### VedaOps placement
- **Deferred pending more samples**

### Notes
This is useful baseline evidence for later clickstream comparison.
Do not model these yet from null-only evidence.

---

## What this sample adds beyond `keywords_for_site`

Compared with `dataforseo-labs-google-keywords-for-site-thisiswhyimbroke-baseline.json`, this sample helps separate:

- **keyword-centric overview truth**
from
- **domain-scoped keyword discovery truth**

This matters because:
- `keywords_for_site` answers: “what keywords are relevant to this domain?”
- `keyword_overview` answers: “what is the provider’s metric profile for this keyword?”

This sample is therefore a cleaner baseline for:
- provider keyword metrics
- trend history
- feature signature
- intent label

without the additional noise of discovery ranking and domain relevance logic.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
Reasons:
- this surface carries long historical search arrays
- it includes multiple provider subfamilies in one compact row
- later clickstream-enabled comparison will be easier against untouched baseline payloads

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:
- keyword overview run root
- keyword overview row
- provider keyword metrics
- provider keyword properties
- SERP feature signature
- backlink/authority context
- provider intent classification

Archive-first / defer:
- clickstream-normalized objects until sampled
- any meaning inferred from category IDs beyond preserving them
- any attempt to reduce long monthly history into one canonical strategy score

---

## VEDA vs VEDA Strategy placement summary

## Belongs in VEDA now
- keyword overview observations
- provider keyword metrics
- long-horizon monthly search arrays
- provider keyword difficulty
- SERP feature signatures
- provider backlink/authority context
- provider intent classification

## Later may feed VEDA Strategy
- opportunity scoring
- seasonality-aware prioritization
- SERP-feature-aware interpretation
- difficulty-vs-demand analysis
- commercial-intent weighting

## Must not be done inside VEDA
- deciding whether the keyword is a good business target
- turning provider metrics into final strategic recommendations
- collapsing trend history into strategy conclusions inside the observatory layer

---

## Most important findings from this sample

1. `keyword_overview` is a clean keyword-centric observatory surface.
2. It preserves long historical monthly search data, which is strategically valuable later.
3. `include_serp_info = true` gives a useful feature-family signature without a full SERP pull.
4. Provider difficulty can be `0` even for a very large keyword, so it must be preserved carefully and interpreted later.
5. The normalized/clickstream structural slots are present even when disabled.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `veda/schema-reference.md`
- future Labs and keyword-observability doctrine

It is not itself authority doctrine.
