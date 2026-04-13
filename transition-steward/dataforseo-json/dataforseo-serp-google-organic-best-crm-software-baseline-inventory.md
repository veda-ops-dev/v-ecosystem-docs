# DataForSEO SERP Inventory — Google Organic Advanced Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-serp-google-organic-best-crm-software-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to help VedaOps decide:

- what DataForSEO SERP data families belong in VEDA as canonical observatory truth
- what should remain raw provider archive only
- what should be deferred until schema-reference and provider doctrine work harden
- what later may feed VEDA Strategy as derived intelligence

---

## Sample request profile

Observed request settings in sample payload:

- API family: `serp`
- Search engine: `google`
- Search type: `organic`
- Function: `live`
- Mode: `advanced`
- Keyword: `best crm software`
- Location code: `2840`
- Language code: `en`
- Device: `desktop`
- OS: `windows`
- Depth: `20`
- People Also Ask click depth: `2`

Important implication:
this is already beyond a minimal 10-blue-links capture.
The response includes AI Overview and expanded PAA behavior.

---

## Top-level structural layers

### 1. Provider task envelope
Top-level fields:

- `id`
- `status_code`
- `status_message`
- `time`
- `cost`
- `result_count`
- `path`
- `data`

Classification:
- **Raw provider metadata / observatory provenance**
- useful for `veda.api_response_log`-style provenance and provider-response auditability
- not the primary canonical SERP observation itself

### 2. Query/result context block
Primary fields under `result[0]`:

- `keyword`
- `type`
- `se_domain`
- `location_code`
- `language_code`
- `check_url`
- `datetime`
- `spell`
- `refinement_chips`
- `item_types`
- `se_results_count`
- `pages_count`
- `items_count`

Classification:
- **Canonical SERP observation root candidate**
- defines the query context and the scope of all child SERP items

### 3. Typed SERP item stream
Primary payload under `result[0].items[]`.

Observed item families in this sample:

- `ai_overview`
- `organic`
- `people_also_ask`
- `people_also_search`
- `perspectives`
- `discussions_and_forums`
- `related_searches`

Critical structural conclusion:
this is a **polymorphic typed-item stream**, not a flat result list.
Any first-pass VEDA modeling should treat SERP items as typed observations.

---

## Observed item families and placement recommendations

## A. SERP observation root

### What was observed
The sample contains one query/run root with shared context for all returned items.

### VedaOps placement
- **VEDA canonical observatory truth**

### Likely canonical fields
- provider
- search engine / search type
- keyword
- location code
- language code
- device
- OS
- datetime observed
- check URL
- result count metadata
- item type inventory
- request configuration used for this observation

### Notes
This should likely be the parent record for all typed item observations.

---

## B. Shared SERP item fields

### What was observed
Most item types carry common fields such as:

- `type`
- `rank_group`
- `rank_absolute`
- `page`
- `position`
- `xpath`
- `rectangle`

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This strongly suggests a shared item root record plus per-type detail handling.
Do not model all SERP data as a single flat result table with many nullable columns.

---

## C. Organic result observations

### What was observed
Organic items include rich structured fields such as:

- `domain`
- `title`
- `url`
- `breadcrumb`
- `website_name`
- `is_image`
- `is_video`
- `is_featured_snippet`
- `is_malicious`
- `is_web_story`
- `description`
- `pre_snippet`
- `extended_snippet`
- `highlighted`
- `links`
- `timestamp`
- `faq`
- `about_this_result`
- `related_result`

### VedaOps placement
- **VEDA canonical observatory truth**

### Recommended posture
Canonicalize a strong core subset now:
- rank fields
- domain
- URL
- title
- description
- website name
- key booleans
- timestamp when present

Archive-first / defer some detail until justified:
- every nullable nested field
- every auxiliary organic child structure
- geometry / rectangle fields

---

## D. AI Overview observation

### What was observed
The sample contains a top-level `ai_overview` item with:

- rank and page placement
- `asynchronous_ai_overview`
- top-level `markdown`
- nested `items`
- nested `references`
- `rectangle`

### VedaOps placement
- **VEDA canonical observatory truth**

### Why this matters
AI Overview is clearly a first-class observatory family, not just another organic snippet.
It has its own internal structure and its own reference/citation surface.

### Recommended canonical treatment
Treat AI Overview as its own typed SERP feature family.

Canonicalize now:
- presence / absence
- rank fields
- async flag
- markdown/text summary representation
- child element records
- reference/source records

Defer full normalization of every nested variant until more samples are collected.

---

## E. AI Overview child elements

### What was observed
Nested `ai_overview_element` items include combinations of:

- `position`
- `title`
- `text`
- `markdown`
- `images`
- `references`

### VedaOps placement
- **VEDA canonical observatory truth**

### Recommended treatment
Canonicalize as child records of the parent AI Overview observation.
At minimum retain:
- element order/index
- title
- text
- markdown
- whether images exist

Keep full nested image details archive-first unless later use justifies first-pass modeling.

---

## F. AI Overview references / citations

### What was observed
The top-level AI Overview includes structured references with:

- `source`
- `domain`
- `url`
- `title`
- `text`
- position metadata

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Why this matters
This is one of the clearest bridges from observatory truth to later strategy work.
VEDA should own the fact that a source was cited.
VEDA Strategy may later interpret:
- citation opportunity
- citation gap
- source dominance
- answer-surface visibility patterns

---

## G. People Also Ask block

### What was observed
A top-level `people_also_ask` item containing nested `people_also_ask_element` records.

### VedaOps placement
- **VEDA canonical observatory truth**

### Recommended treatment
Treat the PAA block as a typed SERP feature with child question records.

---

## H. People Also Ask elements

### What was observed
Each PAA element may contain:

- `title`
- `seed_question`
- `xpath`
- `expanded_element`

### VedaOps placement
- **VEDA canonical observatory truth**

### Important structural finding
`expanded_element` is polymorphic.
Observed expansion types include:

- `people_also_ask_expanded_element`
- `people_also_ask_ai_overview_expanded_element`

### Why this matters
PAA and AI-surface observability overlap structurally.
This means PAA is not just a list of question titles.
It can contain AI-overview-style expansion behavior.

### Recommended treatment
Canonicalize now:
- question title
- seed question
- expansion type
- key expanded result source metadata when present

Defer over-modeling every possible expansion subtype until more samples are captured.

---

## I. PAA expanded result details

### What was observed
Non-AI PAA expansions may include:

- `featured_title`
- `url`
- `domain`
- `title`
- `description`
- `images`
- `timestamp`
- `table`

One observed sample contained a structured table with:
- `table_header`
- `table_content`

### VedaOps placement
- **VEDA canonical observatory truth**, but conservatively normalized

### Recommended treatment
Canonicalize source/result metadata.
Keep full table bodies and rarer nested structures archive-first unless they become strategic or operationally important.

---

## J. People Also Search

### What was observed
A `people_also_search` item with:
- block title
- string list of related suggested searches

### VedaOps placement
- **VEDA canonical observatory truth**

### Recommended treatment
This is lightweight enough to canonicalize as a SERP feature block plus child suggestion rows.

---

## K. Perspectives

### What was observed
A `perspectives` item with nested `perspectives_element` records containing:

- title
- URL
- domain
- date
- source
- timestamp

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
This appears valuable enough to preserve as its own typed feature family.
It may later inform strategy around creator/social/discussion answer surfaces.

---

## L. Discussions and forums

### What was observed
A `discussions_and_forums` item with child records containing:

- title
- URL
- domain
- source
- timestamp
- posts_count

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
Useful for understanding discussion-surface presence and forum-style result prevalence.
Likely worth canonicalizing as its own family.

---

## M. Related searches

### What was observed
A `related_searches` item with child string suggestions.
Observed on both page 1 and page 2.

### VedaOps placement
- **VEDA canonical observatory truth**

### Notes
Should probably be modeled as related-query suggestions attached to the SERP observation.
Potential later strategy input for expansion research, but first owned as observatory truth.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
The full provider response should always be archived.
Reasons:

- the response is structurally deep
- item families are polymorphic
- nested substructures will evolve
- some details should be reprocessed later without re-calling the provider

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:

- SERP observation root
- SERP item root
- organic result observation
- AI Overview observation
- AI Overview reference observation
- PAA block observation
- PAA question observation
- PAA expansion observation
- People Also Search suggestion observation
- Perspectives observation
- Discussions and forums observation
- Related search observation

Archive-first / defer:
- every image asset detail
- every rectangle field
- every markdown variant beyond practical needs
- every rare nested subtype
- all one-off feature-specific payloads not yet seen repeatedly

---

## VEDA vs VEDA Strategy placement summary

## Belongs in VEDA now
- provider task provenance
- SERP observation root
- typed SERP item observations
- organic result observations
- AI Overview observations
- AI Overview references/citations
- PAA observations and expansion shapes
- related-query / related-search observations
- perspectives observations
- discussions-and-forums observations

## Later may feed VEDA Strategy
- citation opportunity analysis from AI Overview references
- source/domain answer-surface share analysis
- PAA question gap analysis
- perspectives/discussion visibility interpretation
- query expansion / answer-surface prioritization

## Must not be done inside VEDA
- scoring citation opportunity
- deciding which SERP features matter most strategically
- recommending actions from these observations
- competitive interpretation or gap scoring

---

## Most important findings from this sample

1. This sample already exceeds a minimal SERP model.
2. The response is a typed-item stream, not a flat result list.
3. AI Overview is a first-class observatory family.
4. AI Overview includes structured references/citations that should be preserved canonically.
5. PAA expansion is polymorphic and overlaps with AI-surface observability.
6. Raw response archive is mandatory.
7. First-pass schema work should be conservative but should not pretend this is just organic ranking data.

---

## Recommended next sample captures

To avoid overfitting doctrine to a single response, collect at least these additional samples:

1. **AI/PAA expanded stress sample**
   - same general query class
   - `load_async_ai_overview = true`
   - higher or confirmed PAA depth

2. **Ungrouped organic structure sample**
   - `group_organic_results = false`

3. **Rectangle-enabled sample**
   - `calculate_rectangles = true`

4. **No-AIO control sample**
   - a query with no AI Overview if possible

5. **Different intent class sample**
   - transactional query
   - local query
   - branded query

These should be stored in the same transition-support folder and inventoried separately.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `veda/providers/dataforseo-ai-optimization.md`
- `veda/providers/registry.md`
- `veda/schema-reference.md`
- future DataForSEO provider/doctrine docs
- future AI-surface observability posture in VEDA

It is not itself authority doctrine.
