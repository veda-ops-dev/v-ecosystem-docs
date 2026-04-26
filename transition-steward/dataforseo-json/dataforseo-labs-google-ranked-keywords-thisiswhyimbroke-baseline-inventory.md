# DataForSEO Labs Inventory — Google Ranked Keywords Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-labs-google-ranked-keywords-thisiswhyimbroke-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to help VedaOps decide:

- what `ranked_keywords` data belongs in VEDA as canonical observatory truth
- how this surface differs from `keywords_for_site` and `keyword_overview`
- what actual ranking-state observations it contributes
- what later may feed VEDA Strategy as derived intelligence

---

## Sample request profile

Observed request settings in sample payload:

- API family: `dataforseo_labs`
- Search engine: `google`
- Function: `ranked_keywords`
- Target domain: `thisiswhyimbroke.com`
- Location code: `2840`
- `item_types = ["organic"]`
- `load_rank_absolute = false`
- `limit = 25`
- `historical_serp_mode = "live"`
- `ignore_synonyms = false`
- `include_clickstream_data = false`

Important implication:
this is not just domain keyword discovery.
It is a domain-scoped ranking-state surface that couples provider keyword context with the target domain's observed SERP placement for each returned keyword.

---

## High-level structural conclusions

1. `ranked_keywords` is a compound domain-visibility surface, not a plain keyword list.
2. The result root contains both:
   - domain-level aggregate metrics
   - per-keyword ranked result rows
3. Each row combines two major families:
   - `keyword_data` — provider keyword context
   - `ranked_serp_element` — the target domain's observed ranking snapshot for that keyword
4. This surface is materially closer to domain visibility observability than either `keywords_for_site` or `keyword_overview`.
5. The sample shows meaningful row variation:
   - some rows have `avg_backlinks_info`
   - some rows do not
   - some rows have `keyword_difficulty = 0`
   - some rows have non-zero difficulty
   - some rows show `is_another_language = true`
   - some rows show `rank_changes.is_up = true`
   - some rows show `is_new = true`

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
- `metrics`
- `metrics_absolute`
- `items[]`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This should likely be treated as a ranked-keyword visibility observation run for a target domain.
`total_count` is especially important because the returned 25 rows are only a sample window into a much larger ranked-keyword universe.

---

## A. Aggregate visibility metrics (`metrics`)

### What was observed
The root `metrics` object includes per-surface aggregates.
Observed families:
- `organic`
- `paid`
- `featured_snippet`
- `local_pack`
- `ai_overview_reference`

In this sample:
- `organic` is fully populated
- `paid` is present but zeroed/null
- `featured_snippet`, `local_pack`, and `ai_overview_reference` are null

The populated `organic` block includes:
- rank-bucket counts (`pos_1`, `pos_2_3`, `pos_4_10`, etc.)
- `etv`
- `count`
- `estimated_paid_traffic_cost`
- `is_new`
- `is_up`
- `is_down`
- `is_lost`

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This is a domain-level visibility summary layer, not a row-level keyword layer.
It gives VEDA a compact snapshot of how the domain is distributed across ranking buckets at the time of observation.

### Notes
`metrics_absolute` is null here, so do not invent doctrine around it yet.

---

## B. Ranked keyword row

### What was observed
Each returned row includes:
- `keyword_data`
- `ranked_serp_element`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This is the core row family for the endpoint.
A ranked keyword row should likely be modeled as a domain+keyword+observed-ranking record, not as a mere keyword suggestion.

---

## C. Provider keyword context (`keyword_data`)

### What was observed
`keyword_data` contains the same general provider subfamilies seen in other Labs surfaces:
- `keyword`
- language/location context
- `keyword_info`
- `keyword_properties`
- `serp_info`
- `avg_backlinks_info`
- `search_intent_info`
- normalized/clickstream slots

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This confirms that `ranked_keywords` does not just tell us that the domain ranks.
It also brings along provider keyword metrics and SERP context for the ranked term.
That makes it a richer observatory surface than a pure position report.

---

## D. Keyword metrics and properties

### What was observed
Within `keyword_data`, the sample includes:
- `search_volume`
- `monthly_searches`
- `search_volume_trend`
- `competition`
- `competition_level`
- `cpc`
- `categories`
- `keyword_difficulty`
- `detected_language`
- `is_another_language`
- `core_keyword`
- `synonym_clustering_algorithm`

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Important finding
This sample reinforces a recurring rule:
provider difficulty, competition, trend, and language classification belong in VEDA as provider-observed/provider-computed fields.
They are not VEDA-native strategic conclusions.

### Notes
The row variation around `detected_language` and `is_another_language` is useful.
It shows that ranked terms for a domain can include multilingual or classification-edge cases.

---

## E. SERP context signature (`keyword_data.serp_info`)

### What was observed
`serp_info` includes lightweight SERP context for the keyword, such as:
- `check_url`
- `serp_item_types`
- `se_results_count`
- `last_updated_time`
- `previous_updated_time`

Observed `serp_item_types` vary by row and include combinations such as:
- `ai_overview`
- `organic`
- `people_also_ask`
- `images`
- `popular_products`
- `video`
- `related_searches`
- `discussions_and_forums`
- `perspectives`
- `people_also_search`
- `short_videos`
- `local_pack`

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This surface gives a keyword-level feature-family signature while also tying that signature to the domain's ranked page.
That is valuable observatory context for later visibility interpretation.

---

## F. Ranked SERP element (`ranked_serp_element`)

### What was observed
Each row includes a `ranked_serp_element` block containing:
- `serp_item`
- `check_url`
- `serp_item_types`
- `se_results_count`
- `keyword_difficulty`
- `is_lost`
- `last_updated_time`
- `previous_updated_time`

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This is the decisive difference-maker for the surface.
It is the actual observed target-domain ranking snapshot, not just keyword metadata.

### Notes
This should likely be treated as the row's ranking-state child record.

---

## G. Ranked organic result snapshot (`ranked_serp_element.serp_item`)

### What was observed
The embedded `serp_item` is an organic result observation for the target domain, including:
- `type`
- `rank_group`
- `rank_absolute`
- `position`
- `xpath`
- `domain`
- `title`
- `url`
- `breadcrumb`
- `website_name`
- key booleans
- `description`
- `rating` when present
- `highlighted`
- `main_domain`
- `relative_url`
- `etv`
- `estimated_paid_traffic_cost`
- `rank_changes`
- `backlinks_info` when present
- `rank_info`

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This confirms the surface contains page-level ranking evidence for the target domain, including movement state through `rank_changes`.
That makes it much more operationally useful than a raw rank number alone.

### Notes
Canonicalize the strong core now:
- rank fields
- URL/domain/title
- description
- ETV / estimated paid traffic cost
- `rank_changes`
- `rank_info`

Archive-first / defer:
- full `xpath`
- every optional display detail
- rare child structures unless they recur in more samples

---

## H. Backlink context

### What was observed
Two backlink-like layers can appear:

1. `keyword_data.avg_backlinks_info`
2. `ranked_serp_element.serp_item.backlinks_info`

The first is a provider aggregate context.
The second, when present, is result-level backlink detail for the ranked page.

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Important finding
These two backlink contexts are not the same thing.
They should not be collapsed casually in later modeling.

---

## I. Intent classification

### What was observed
`search_intent_info` is present per keyword row, with fields such as:
- `main_intent`
- `foreign_intent`
- `last_updated_time`

Observed values include:
- transactional
- commercial
- combinations with foreign intent

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Notes
Preserve the provider intent classification directly.
Do not reinterpret it inside VEDA.

---

## What this sample adds beyond other Labs samples

Compared with the current `keywords_for_site` and `keyword_overview` samples, this surface adds:
- domain-level aggregate rank-bucket visibility metrics
- actual target-domain ranking snapshots per keyword
- rank movement state (`is_new`, `is_up`, `is_down`, `is_lost`)
- page/result-level observability tightly coupled to keyword context

This makes `ranked_keywords` one of the strongest Phase 1 surfaces for domain visibility observability.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
Reasons:
- this surface combines aggregate metrics and row-level rank evidence
- row completeness varies
- some result-level child structures appear only on some rows
- later doctrine may need to distinguish aggregate, keyword, and page-level layers more finely

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:
- ranked-keyword observation run root
- aggregate visibility metrics snapshot
- ranked keyword row
- provider keyword context
- SERP feature signature
- ranked SERP element observation
- ranked organic result snapshot
- rank movement state
- provider intent classification

Archive-first / defer:
- full `xpath`
- every nullable display-oriented field
- any assumption that current `item_types = ["organic"]` means the endpoint is forever organic-only in doctrine
- clickstream-normalized fields until sampled

---

## VEDA vs VEDA Strategy placement summary

## Belongs in VEDA now
- domain ranked-keyword observations
- aggregate rank-bucket visibility metrics
- provider keyword metrics and properties
- keyword-level SERP feature signatures
- actual target-domain ranking snapshots
- page/result-level movement state
- provider intent classification

## Later may feed VEDA Strategy
- opportunity scoring
- ranking-defense prioritization
- ranking-improvement prioritization
- feature-aware visibility interpretation
- page-vs-keyword leverage analysis
- trend-aware dominance/decline interpretation

## Must not be done inside VEDA
- deciding which rankings matter most strategically
- scoring opportunity from provider metrics and rank state inside VEDA
- converting `is_up`, `is_new`, or `keyword_difficulty` into strategic recommendations in the observatory layer

---

## Most important findings from this sample

1. `ranked_keywords` is a compound domain visibility surface, not a simple keyword list.
2. It includes both aggregate visibility metrics and per-keyword target-domain rank evidence.
3. The per-row `ranked_serp_element` is the key observatory family that distinguishes this endpoint from other Labs surfaces.
4. Row variation is real and must be handled conservatively.
5. Provider keyword context and ranking-state evidence coexist in the same row but should remain conceptually distinct.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `veda/schema-reference.md`
- future Labs and visibility-observability doctrine

It is not itself authority doctrine.
