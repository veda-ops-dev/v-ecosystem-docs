# DataForSEO SERP Inventory — Google Organic Advanced AI Overview Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-serp-google-organic-weather-forecast-ai-overview-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to help VedaOps decide:

- what AI Overview-heavy SERP observations belong in VEDA as canonical observatory truth
- what feature families vary across SERP captures
- what should remain raw provider archive only
- what later may feed VEDA Strategy as derived intelligence

---

## Sample request profile

Observed request settings in sample payload:

- API family: `serp`
- Search engine: `google`
- Search type: `organic`
- Function: `live`
- Mode: `advanced`
- Keyword: `weather forecast`
- Location code: `2840`
- Language code: `en`
- Device: `desktop`
- OS: `windows`
- Depth: `20`
- `group_organic_results = true`
- `calculate_rectangles = false`
- `load_async_ai_overview = true`

Important implication:
this is a valid AI Overview capture sample because the returned `ai_overview` item is present and explicitly marked `asynchronous_ai_overview = true`.

---

## High-level structural conclusions

1. This sample confirms that `load_async_ai_overview = true` can surface a real asynchronous AI Overview item.
2. This sample shows a SERP feature mix that differs from the earlier CRM baseline sample.
3. This sample includes `top_stories` and `perspectives`, but does **not** include PAA, discussions/forums, or people-also-search.
4. This strengthens the rule that SERP observations must be modeled as a polymorphic typed-item stream, not a flat result list.
5. AI Overview references are preserved both at the top-level AI Overview item and within child AI Overview elements.

---

## Observed item families in this sample

Observed `item_types`:

- `ai_overview`
- `organic`
- `top_stories`
- `perspectives`
- `related_searches`

### Structural significance
Compared with the prior SERP baseline, this sample increases confidence that:
- SERP feature family presence varies materially by query
- AI Overview can coexist with news-like and social-perspective surfaces
- no single sample should be treated as the full SERP type universe

---

## Family-by-family placement guidance

## A. SERP observation root

### What was observed
The result root includes:
- keyword
- location/language context
- check URL
- datetime
- `item_types`
- `pages_count`
- `items_count`
- result count metadata

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This remains the parent record for all typed SERP item observations.

---

## B. AI Overview observation

### What was observed
The top-level `ai_overview` item includes:
- rank and page placement
- `asynchronous_ai_overview = true`
- full markdown body
- nested `items`
- nested `references`

### VedaOps placement
- **VEDA canonical observatory truth**

### Important finding
This sample is especially useful because it confirms the async-loading case, not just the existence of a top-level AI Overview shape.

### Recommended canonical treatment
Preserve now:
- AI Overview presence
- rank fields
- async flag
- markdown/text
- child elements
- citation/reference objects

---

## C. AI Overview child elements

### What was observed
This sample contains multiple `ai_overview_element` children, including:
- a summary body element
- a titled regional-highlight section
- a note/disclaimer section

Observed fields include:
- `position`
- `title`
- `text`
- `markdown`
- `references`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This strengthens the case that AI Overview child elements should be treated as ordered child records, not flattened into one answer blob.

---

## D. AI Overview references / citations

### What was observed
The sample includes structured citation/reference objects at two levels:

1. nested inside `ai_overview_element.references`
2. repeated in the top-level `ai_overview.references`

Observed fields include:
- `source`
- `domain`
- `url`
- `title`
- `text`
- position metadata

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Important finding
This sample suggests citation records may appear both:
- as element-local references
- and as top-level AI Overview reference collections

That duplication/overlap needs to be handled carefully in later doctrine/schema work.
Do not assume one citation layer only.

---

## E. Organic result observations

### What was observed
This sample includes standard organic result records with rich structured fields:
- domain
- title
- URL
- breadcrumb
- website name
- description
- booleans (`is_video`, `is_image`, etc.)
- timestamps when present
- sitelink-style child `links` on some results

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
The organic family is consistent with the prior baseline sample, which is good — it suggests a stable core organic shape even as surrounding feature families vary.

---

## F. Top stories

### What was observed
A `top_stories` block with child `top_stories_element` records containing:
- source
- domain
- title
- date
- timestamp
- URL
- image URL
- badges

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This is a distinct SERP feature family that should not be jammed into generic organic result modeling.
It likely belongs as a typed feature block plus child item rows.

---

## G. Perspectives

### What was observed
A `perspectives` block with child `perspectives_element` items containing:
- title
- URL
- domain
- date
- source
- timestamp

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This sample reinforces that perspectives is a meaningful distinct feature family, especially for social/video/creator-style surfaces.

---

## H. Related searches

### What was observed
`related_searches` appears on both page 1 and page 2.
Each block contains a list of suggested related queries.

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This confirms related searches may recur across pages and should probably be attached to both page context and parent SERP observation context.

---

## What this sample adds beyond the prior SERP baseline

Compared with `dataforseo-serp-google-organic-best-crm-software-baseline.json`, this sample adds strong evidence for:

- asynchronous AI Overview capture as a real observatory case
- `top_stories` as a distinct typed family worth preserving
- `perspectives` coexisting with AI Overview in a different query class
- SERP type variation by query intent and topic
- top-level vs nested AI Overview reference overlap

It also usefully lacks some prior feature families:
- no PAA
- no discussions and forums
- no people also search

That absence is useful because it prevents overfitting doctrine to one feature mix.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
Reasons:
- this sample includes async AI Overview behavior
- citation structure appears at multiple levels
- typed feature-family variation is significant
- future reprocessing may need the untouched payload

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:
- SERP observation root
- AI Overview observation
- AI Overview child element observation
- AI Overview citation/reference observation
- organic result observation
- top stories observation
- perspectives observation
- related search observation

Archive-first / defer:
- image URL assets from top stories
- every markdown nuance
- every repeated citation layer until reference dedup/posture is governed
- rectangle geometry (not present here)

---

## VEDA vs VEDA Strategy placement summary

## Belongs in VEDA now
- query/root SERP observation
- feature-family presence by SERP
- AI Overview content and structure
- AI Overview citations/references
- organic result observations
- top stories observations
- perspectives observations
- related search observations

## Later may feed VEDA Strategy
- citation opportunity analysis from AI Overview references
- feature-family prevalence by query class
- news/social/perspectives dominance interpretation
- answer-surface source concentration analysis

## Must not be done inside VEDA
- deciding which cited sources are strategically best
- scoring the value of top stories or perspectives exposure
- making content recommendations from this sample alone

---

## Most important findings from this sample

1. `load_async_ai_overview = true` successfully produced an async AI Overview observation.
2. AI Overview references exist both at child-element level and top-level block level.
3. `top_stories` is a distinct typed family and should be preserved as such.
4. `perspectives` is a meaningful SERP feature family, not just noise.
5. SERP feature-family variation across query classes is real and should be expected.
6. Raw response archive remains mandatory.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `veda/providers/dataforseo-ai-optimization.md`
- `veda/schema-reference.md`
- future SERP and AI-surface observability doctrine

It is not itself authority doctrine.
