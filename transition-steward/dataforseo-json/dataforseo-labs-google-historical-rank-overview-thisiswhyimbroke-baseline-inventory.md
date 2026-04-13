# DataForSEO Labs Inventory — Google Historical Rank Overview Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-labs-google-historical-rank-overview-thisiswhyimbroke-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to help VedaOps decide:

- what `historical_rank_overview` data belongs in VEDA as canonical observatory truth
- what temporal visibility families this endpoint contributes
- how this surface differs from `ranked_keywords`
- what later may feed VEDA Strategy as derived intelligence

---

## Sample request profile

Observed request settings in sample payload:

- API family: `dataforseo_labs`
- Search engine: `google`
- Function: `historical_rank_overview`
- Target domain: `thisiswhyimbroke.com`
- Location code: `2840`
- Language code: `en`
- `correlate = true`
- `ignore_synonyms = false`
- `date_from = 2024-01-01`
- `date_to = 2026-04-10`
- `include_clickstream_data = false`

Important implication:
this is a historical domain-visibility time series surface, not a current-keyword discovery surface.
It summarizes how the domain's rank distribution and estimated traffic metrics changed month by month across the requested window.

---

## High-level structural conclusions

1. `historical_rank_overview` is a monthly aggregate time-series surface.
2. It does not return row-level keywords or page-level ranked items.
3. Each item is a month snapshot with aggregate metrics by ranking bucket.
4. This surface is best understood as historical domain visibility observability, not keyword observability.
5. The time window is broad enough to support trend, growth/decline, and seasonality-aware later interpretation without turning VEDA itself into strategy.

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
- `items[]`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
The root should likely be treated as a historical visibility observation run for a target domain over a bounded date window.
`total_count = 27` and `items_count = 27` indicate one monthly snapshot per month across the requested range.

---

## A. Monthly historical snapshot row

### What was observed
Each item row includes:
- `year`
- `month`
- `metrics`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This is the core row family for the endpoint.
A historical rank overview row should likely be modeled as a domain+month aggregate visibility snapshot.

---

## B. Aggregate ranking-bucket metrics (`metrics.organic`)

### What was observed
The populated `organic` metrics block includes:
- `pos_1`
- `pos_2_3`
- `pos_4_10`
- `pos_11_20`
- `pos_21_30`
- `pos_31_40`
- `pos_41_50`
- `pos_51_60`
- `pos_61_70`
- `pos_71_80`
- `pos_81_90`
- `pos_91_100`
- `etv`
- `count`
- `estimated_paid_traffic_cost`
- `is_new`
- `is_up`
- `is_down`
- `is_lost`
- clickstream slots, null in this sample

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This is one of the clearest aggregate visibility families seen so far.
It gives VEDA a month-by-month record of:
- how many rankings the domain held in each bucket
- approximate traffic-value context through `etv`
- movement-state counts (`is_new`, `is_up`, `is_down`, `is_lost`)

### Notes
This should be preserved directly as provider-observed/provider-computed temporal visibility data.

---

## C. Paid metrics block (`metrics.paid`)

### What was observed
A `paid` block is present for every month, but in this sample it is entirely zeroed.

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
Even a zeroed paid block is meaningful.
It shows the endpoint shape reserves space for paid visibility metrics, even when the observed domain has no current paid activity represented here.

### Notes
Do not over-model paid doctrine from this one sample, but do preserve the structural family.

---

## D. Clickstream-related fields

### What was observed
Within both `organic` and `paid`, the sample includes null clickstream-related fields:
- `clickstream_etv`
- `clickstream_gender_distribution`
- `clickstream_age_distribution`

### VedaOps placement
- **Deferred pending more samples**

### Important finding
This confirms the historical surface has structural slots for clickstream-enriched variants.
That makes a later clickstream-enabled comparison straightforward.

### Notes
Do not model these yet from null-only evidence.

---

## What this sample adds beyond `ranked_keywords`

Compared with `ranked_keywords`, this endpoint removes row-level keyword detail and instead adds:
- month-over-month aggregate visibility snapshots
- long-run trendability
- rank-bucket history
- historical ETV and estimated paid traffic cost progression
- historical movement-state counts at domain level

This matters because:
- `ranked_keywords` answers: what does the domain rank for now, and how are individual ranked rows structured?
- `historical_rank_overview` answers: how has the domain's overall visibility posture changed across time?

---

## What this sample appears good for

Strong observatory uses:
- historical domain visibility baselining
- observing gross growth/decline over time
- preserving monthly rank-bucket distribution history
- preserving temporal ETV history
- preserving temporal movement-state counts

Not a good fit for:
- page-level or keyword-level reasoning by itself
- canonical per-keyword rank history without additional endpoint coverage

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
Reasons:
- this is a high-value temporal aggregate surface
- future schema work may want to revisit how month rows are modeled
- clickstream-enriched variants may need later comparison against the untouched baseline

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:
- historical visibility observation run root
- monthly historical visibility snapshot
- organic rank-bucket metrics
- paid metrics family presence
- temporal ETV / estimated paid cost series
- temporal movement-state counts

Archive-first / defer:
- clickstream fields until sampled
- any attempt to infer cause from the trend series inside VEDA
- any strategic scoring derived from month-over-month changes

---

## VEDA vs VEDA Strategy placement summary

## Belongs in VEDA now
- historical domain visibility snapshots
- monthly rank-bucket counts
- historical ETV and estimated paid traffic cost
- historical aggregate movement-state counts
- paid-family structural presence

## Later may feed VEDA Strategy
- dominance/decline interpretation
- trend break detection
- seasonal opportunity interpretation
- recovery/erosion pattern analysis
- rank-bucket-based prioritization

## Must not be done inside VEDA
- deciding whether the domain is strategically winning or failing
- turning historical trend shifts into recommendations inside the observatory layer
- inferring root cause from aggregate metrics alone

---

## Most important findings from this sample

1. `historical_rank_overview` is a monthly aggregate visibility time-series surface.
2. It complements `ranked_keywords` rather than replacing it.
3. It is strong observatory truth for temporal domain visibility, not row-level keyword truth.
4. The endpoint preserves both rank-bucket counts and movement-state counts over time.
5. Paid and clickstream families are structurally present even when not populated in this sample.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `veda/schema-reference.md`
- future Labs and temporal-visibility doctrine

It is not itself authority doctrine.
