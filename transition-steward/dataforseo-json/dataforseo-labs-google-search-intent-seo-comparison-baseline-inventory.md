# DataForSEO Labs Inventory — Google Search Intent (`seo`) Comparison Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-labs-google-search-intent-seo-comparison-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to compare a second direct `search_intent` sample against the earlier `gifts for men` baseline and to document how the endpoint behaves on a broad keyword.

---

## Sample request profile

Observed request settings in sample payload:

- API family: `dataforseo_labs`
- Search engine: `google`
- Function: `search_intent`
- Keyword: `seo`
- Language code: `en`

### Cost observation
- `cost = 0.0011`

This remains one of the cheapest structural comparison surfaces currently sampled.

---

## High-level structural conclusions

1. The endpoint shape is unchanged from the earlier direct search-intent sample.
2. The direct endpoint continues to provide a clean `label + probability` output.
3. The sample is useful because it confirms the endpoint works well as a very cheap comparison surface.
4. On this keyword, the provider assigns a very strong navigational classification.

---

## Result-root structure

### What was observed
The result root includes:
- `language_code`
- `items_count`
- `items[]`

### VedaOps placement
- **VEDA canonical observatory truth**

---

## A. Keyword intent row

### What was observed
Each row includes:
- `keyword`
- `keyword_intent`
- `secondary_keyword_intents`

### VedaOps placement
- **VEDA canonical observatory truth**

---

## B. Primary intent object (`keyword_intent`)

### What was observed
The primary intent object includes:
- `label`
- `probability`

Observed values:
- `label = navigational`
- `probability = 0.9823565`

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Important finding
This sample confirms the direct search-intent endpoint can return a very high-confidence classification on broad terms.
That makes it useful for comparison against the embedded `search_intent_info` family in `keyword_overview`.

---

## C. Secondary intents (`secondary_keyword_intents`)

### What was observed
- `secondary_keyword_intents = null`

### VedaOps placement
- **VEDA canonical observatory truth**
- **Deferred pending more samples**

### Notes
The structural slot remains present, but this sample does not populate it.

---

## Comparison note vs Keyword Overview (`seo`)

This sample pairs well with:
- `dataforseo-labs-google-keyword-overview-seo-comparison-baseline.json`

Why:
- both use the same keyword
- the direct endpoint gives `label + probability`
- the embedded `keyword_overview.search_intent_info` gives provider intent without the same compact direct object shape

That makes this a clean comparison pair.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
Reasons:
- very cheap comparison surface
- good pair with the `keyword_overview` sample on the same keyword
- useful for confirming direct-provider intent behavior

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:
- search-intent observation run root
- keyword intent observation row
- primary provider intent label
- primary provider intent probability
- secondary-intent presence / absence

Archive-first / defer:
- assumptions about richer secondary-intent structure until more samples exist
- any strategy-layer conversion of intent probability into final project scoring inside VEDA

---

## Most important findings from this sample

1. The direct `search_intent` endpoint remains structurally clean and stable.
2. `seo` is classified as `navigational` with very high probability.
3. This is a good cheap comparison sample because it pairs cleanly with the `keyword_overview` sample on the same keyword.
4. Secondary intents remain unpopulated in this sample.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `veda/schema-reference.md`

It is not itself authority doctrine.
