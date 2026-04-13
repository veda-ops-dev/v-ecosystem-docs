# DataForSEO AI Optimization Inventory — ChatGPT LLM Responses Baseline

## Purpose

This document captures the observable structure of the sample payload:

- `dataforseo-ai-optimization-chatgpt-llm-responses-best-crm-software-baseline.json`

It is a transition-support artifact, not authority doctrine.
It exists to help VedaOps decide:

- what AI Optimization / ChatGPT response data belongs in VEDA as canonical observatory truth
- what should remain raw provider archive only
- what later may feed VEDA Strategy as derived intelligence
- what should be deferred until provider doctrine and schema-reference work harden

---

## Sample request profile

Observed request settings in sample payload:

- API family: `ai_optimization`
- Surface: `chat_gpt`
- Function: `llm_responses`
- Mode: `live`
- User prompt: `What are the best crm for my business.`
- Requested model: `gpt-5`
- Max output tokens: `2048`
- System message supplied: yes
- Requested web search: `true`

Important implication:
this sample is not citation-only data.
It is answer-behavior observability for a ChatGPT surface.

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
- useful for provider-response auditability and run-level cost tracking
- not the primary canonical answer-surface observation itself

### 2. Request/configuration block
Primary fields under `data`:

- `api`
- `function`
- `se`
- `user_prompt`
- `model_name`
- `max_output_tokens`
- `system_message`
- `web_search`

Classification:
- **Canonical answer-observation root candidate inputs**
- this is the requested configuration that shaped the response

### 3. Result/runtime block
Primary fields under `result[0]`:

- `model_name`
- `input_tokens`
- `output_tokens`
- `reasoning_tokens`
- `web_search`
- `money_spent`
- `datetime`
- `items`
- `fan_out_queries`

Classification:
- **Canonical answer-observation root candidate runtime metadata**
- records what actually happened, which may differ from what was requested

### 4. Typed response item stream
Primary payload under `result[0].items[]`.

Observed item families in this sample:

- `reasoning`
- `message`

Critical structural conclusion:
this is a **typed response-item stream**, not just one flat answer blob.
Any first-pass VEDA modeling should treat response items as typed observations.

---

## Observed answer-surface families and placement recommendations

## A. Answer observation root

### What was observed
The sample contains one answer/run root with shared context for all returned items.

### VedaOps placement
- **VEDA canonical observatory truth**

### Likely canonical fields
- provider / API family / surface
- requested prompt
- requested model
- requested system message presence
- requested web-search flag
- resolved model name
- runtime datetime
- token counts
- provider cost / spend fields
- actual web-search flag
- fan-out query presence / absence

### Notes
This should likely be the parent record for all typed answer-item observations.

---

## B. Requested behavior vs actual behavior

### What was observed
The request block asked for:
- `web_search = true`

But the returned runtime block reports:
- `web_search = false`

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Why this matters
This is one of the most important findings in the sample.
It means the answer surface can diverge from requested configuration.
For answer-surface observability, VEDA should preserve:
- what was requested
- what actually happened

Later, VEDA Strategy may interpret patterns such as:
- when a surface asks clarifying questions instead of answering
- when web-search mode is requested but not actually used
- when fan-out behavior appears or does not appear

---

## C. Reasoning item

### What was observed
The first response item is:
- `type = reasoning`

It contains `sections[]`, each with:
- `type = summary_text`
- `text`

Observed content characteristics:
- clarifying-questions intent
- acknowledgement of missing business context
- explicit mention of considering web search for substantial advice
- no external search output actually present in this sample

### VedaOps placement
- **VEDA canonical observatory truth**, conservatively

### Recommended treatment
Canonicalize now:
- item type
- section order/index
- section type
- section text

### Notes
This appears to be reasoning-summary exposure, not raw hidden chain-of-thought.
Even so, VEDA should treat it as answer-surface output, not as strategy.
Do not let this drift into recommendation logic inside VEDA.

---

## D. Message item

### What was observed
The second response item is:
- `type = message`

It contains `sections[]`, each with:
- `type = text`
- `text`
- `annotations`

Observed message behavior:
- asks 10 clarifying questions
- gives a conditional starter shortlist
- provides category-based CRM suggestions
- invites follow-up for tailored ranking and implementation plan

### VedaOps placement
- **VEDA canonical observatory truth**

### Recommended treatment
Canonicalize now:
- item type
- section order/index
- section type
- section text
- annotations presence / absence

### Notes
This is the visible answer payload and likely the most important surface artifact for later answer-behavior analysis.

---

## E. Section typing

### What was observed
Within items, sections are also typed.
Observed section types include:

- `summary_text`
- `text`

### VedaOps placement
- **VEDA canonical observatory truth**

### Why this matters
The answer surface is hierarchical:
- answer run
- item type
- section type
- section content

This suggests a normalized parent/child pattern is safer than one giant text blob.

---

## F. Token and spend metrics

### What was observed
The runtime block includes:

- `input_tokens`
- `output_tokens`
- `reasoning_tokens`
- `money_spent`
- top-level `cost`

### VedaOps placement
- **VEDA canonical observatory truth**

### Why this matters
These are important for:
- provider observability
- run cost analysis
- prompt economics
- later strategy-side efficiency analysis

### Notes
Preserve both top-level provider cost and per-result spend fields where available.

---

## G. Fan-out queries

### What was observed
The sample includes:
- `fan_out_queries = null`

### VedaOps placement
- **VEDA canonical observatory truth**
- **later VEDA Strategy input**

### Why this matters
Even null is informative.
It tells us this answer run did not emit fan-out query behavior in a usable structured form.
For later observability, VEDA should preserve:
- whether fan-out queries are absent
- whether they are present
- what structure they use when present

This is likely important to your broader answer-surface / citation-surface modeling later.

---

## H. Prompt + system-message observability

### What was observed
The sample includes both:
- a user prompt
- a system message

### VedaOps placement
- **VEDA canonical observatory truth**, with caution

### Notes
This is useful because model behavior cannot be interpreted correctly without the prompt context that produced it.
However, long-term doctrine may need rules for:
- how much prompt text is stored canonically
- whether prompt templates vs raw prompt text are separated
- any governance around sensitive or internal system-message content

For this transition stage, preserving the actual prompt and system message in raw/provider-observation posture is useful.

---

## Raw archive vs canonical truth recommendation

## Keep raw JSON archive always
The full provider response should always be archived.
Reasons:

- the surface is hierarchical
- response item structure may evolve
- section types may expand
- fan-out behavior may appear in later samples
- requested vs actual behavior needs reprocessing later without re-calling provider APIs

## Canonicalize selectively in first pass
Good first-pass canonical families from this sample:

- answer observation root
- answer runtime metadata
- typed answer item observations
- typed section observations
- token / spend metrics
- requested vs actual web-search behavior
- fan-out query presence / absence

Archive-first / defer:
- over-modeling every text nuance as separate schema families
- assumptions about future section/item types from a single sample
- any interpretation about whether this was a “good” answer

---

## VEDA vs VEDA Strategy placement summary

## Belongs in VEDA now
- provider task provenance
- requested prompt / configuration
- resolved model/runtime metadata
- requested vs actual web-search flags
- typed response items
- typed response sections
- visible answer text
- reasoning-summary presence and content
- fan-out query presence / absence
- token and spend observability

## Later may feed VEDA Strategy
- answer-surface behavior classification
- prompt-shape effectiveness analysis
- “clarifying-question instead of answer” pattern analysis
- search-enabled vs search-disabled response pattern analysis
- cost/performance optimization by prompt family or surface
- fan-out query interpretation when present

## Must not be done inside VEDA
- deciding which prompts are strategically best
- scoring answer quality or conversion opportunity inside VEDA
- generating optimization recommendations from these observations
- interpreting behavioral patterns as strategy inside the observatory layer

---

## Most important findings from this sample

1. This surface is answer-behavior observability, not just citation data.
2. The response is a typed-item stream, not a single answer blob.
3. Reasoning-summary content is exposed as structured output.
4. Requested web search and actual web search can diverge.
5. Fan-out query absence is itself meaningful and should be preserved.
6. Token and spend metrics are first-class observatory data.
7. Raw response archive is mandatory.

---

## Recommended next sample captures

To avoid overfitting doctrine to a single response, collect at least these additional samples:

1. **Search-heavy sample**
   - a prompt more likely to force web search
   - confirm whether `web_search` becomes true in the returned result block

2. **Citation-heavy sample**
   - a prompt explicitly asking for cited sources or recent research
   - observe whether citation or annotation structures appear

3. **Fan-out-producing sample**
   - a prompt likely to trigger query expansion
   - observe `fan_out_queries` structure when non-null

4. **Comparative prompt sample**
   - same business topic, different prompt wording
   - compare answer behavior and runtime flags

5. **Different model/runtime sample**
   - if available through DataForSEO playground or API options
   - compare structure stability across model choices

These should be stored in the same transition-support folder and inventoried separately.

---

## Steward note

This file is a transition-support interpretation of one sample payload.
It should inform later updates to:

- `veda/providers/dataforseo-ai-optimization.md`
- future AI-surface observability provider/doctrine docs
- `veda/schema-reference.md`
- future answer-surface observability posture in VEDA
- later VEDA Strategy derivation doctrine

It is not itself authority doctrine.
