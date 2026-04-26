# DataForSEO Labs Inventory — Google Search Intent Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-labs-google-search-intent-gifts-for-men-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to help VedaOps decide:

- what `search_intent` data belongs in VEDA as canonical observatory truth
- how this endpoint differs from embedded `search_intent_info` fields in other Labs surfaces
- whether this sample is worth keeping as its own observatory family
- what later may feed VEDA Strategy as derived intelligence

---

## Sample request profile

Observed request settings in sample payload:

- API family: `dataforseo_labs`
- Search engine: `google`
- Function: `search_intent`
- Keywords: `['gifts for men']`
- Language code: `en`

Important implication:
this is a direct provider intent-classification call.
It is not a keyword-overview sample with intent embedded as one field among many.

---

## High-level structural conclusions

1. `search_intent` is a narrow, purpose-built classification surface.
2. The sample is structurally small but still useful because it returns both:
   - a primary intent label
   - an associated probability score
3. This shape differs from the `search_intent_info` blocks seen in `keyword_overview` and `keywords_for_site`.
4. That means the endpoint should not be silently treated as identical to the embedded-intent variant without more comparison.

---

## Result-root structure

### What was observed
The result root includes:
- `language_code`
- `items_count`
- `items[]`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This should likely be treated as a search-intent observation run for one or more requested keywords.

---

## A. Keyword intent row

### What was observed
Each item row includes:
- `keyword`
- `keyword_intent`
- `secondary_keyword_intents`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This is the core row family for the endpoint.
A search-intent row should be modeled as a provider intent observation for a keyword, not as a strategic conclusion.

---

## B. Primary intent object (`keyword_intent`)

### What was observed
The primary intent object includes:
- `label`
- `probability`

In this sample:
- `label = commercial`
- `probability = 0.8352958`

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Important finding
This is the strongest reason to keep the sample.
Unlike the embedded `search_intent_info` fields in other Labs samples, this endpoint gives an explicit probability value attached to the provider intent label.

### Notes
That probability should be preserved directly as provider output.
It must not be reinterpreted inside VEDA as a VEDA-native strategic weight.

---

## C. Secondary intent object (`secondary_keyword_intents`)

### What was observed
The sample includes:
- `secondary_keyword_intents = null`

### VedaOps placement
- **VEDA canonical observatory truth**
- **Deferred pending more samples**

### Important finding
Even though this sample does not populate secondary intents, it proves the endpoint shape allows for them.
That makes follow-up samples valuable before hardening any canonical schema shape beyond a simple nullable child family.

---

## What this sample adds beyond other intent fields

Compared with the embedded `search_intent_info` seen in `keyword_overview` and `keywords_for_site`, this endpoint appears to provide:
- a standalone intent-classification surface
- a direct `label`
- a direct `probability`
- possible secondary-intent structure

This means the surface is worth preserving separately for now.
It is not just a redundant copy of the embedded-intent fields based on current evidence.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
Reasons:
- this is the cleanest direct intent-only sample currently present
- later comparison with embedded `search_intent_info` may matter
- secondary-intent structure is not yet understood from one null-only sample

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:
- search-intent observation run root
- keyword intent observation row
- primary provider intent label
- provider intent probability
- secondary-intent family presence/absence

Archive-first / defer:
- assumptions about all possible secondary-intent shapes until more samples exist
- any attempt to collapse this endpoint into the embedded `search_intent_info` family without evidence

---

## VEDA vs VEDA Strategy placement summary

## Belongs in VEDA now
- provider search-intent observations
- provider intent label
- provider intent probability
- secondary-intent presence / absence

## Later may feed VEDA Strategy
- intent-confidence-aware prioritization
- intent segmentation
- comparison between provider intent surfaces
- weighting of keyword families by confidence and intent profile

## Must not be done inside VEDA
- deciding whether commercial intent makes the keyword strategically good
- turning provider intent probability into a final project score inside the observatory layer
- assuming this endpoint's classification is the canonical strategic interpretation

---

## Most important findings from this sample

1. `search_intent` is a distinct direct classification endpoint, not just a thin alias of `keyword_overview` based on current evidence.
2. The endpoint returns a primary intent label plus probability.
3. Secondary intent structure exists in shape, even though it is null in this sample.
4. This sample is worth keeping because it clarifies that provider intent observability may come in more than one structural form.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `veda/schema-reference.md`
- future Labs and intent-observability doctrine

It is not itself authority doctrine.
