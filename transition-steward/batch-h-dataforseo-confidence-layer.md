# Batch H — DataForSEO Confidence Layer Addendum

## Purpose

This note applies an explicit confidence-layer distinction to the DataForSEO
work in Batch H, based on a clarification about the prior workflow.

It exists to answer:

```text
Which parts of the DataForSEO AI-surface family design are grounded in actual
captured payloads, and which are grounded in official docs only — and what
should that distinction mean when the design is promoted into authority docs?
```

This must be read alongside:
- `batch-h-veda-family-design-pass.md`
- `batch-h-veda-family-design-pass-corrections.md`
- `batch-h-dataforseo-surface-inventory.md`

And is directly informed by:
- `transition-steward/dataforseo-capture-plan.md`
- `transition-steward/dataforseo-json/` (the captured payload corpus)

This is a transition-support note, not authority doctrine.

---

## Background: The Prior DataForSEO Workflow

Before the Batch H design work, the working method for DataForSEO was:

1. Pull real payloads from the DataForSEO Playground under chosen settings
2. Save the raw JSON to the repo
3. Build inventory notes from actual payload structure
4. Use those inventories as the primary source of truth for schema design

This is the correct method. Actual captured response payloads beat vendor
marketing pages and API reference docs for schema design work. The field names,
nesting, optional presence, and data shapes in real payloads are more reliable
than what documentation describes.

That workflow produced the following confirmed corpus — **payload-confirmed**:

| Captured | File |
|---|---|
| SERP — Google Organic baseline | `dataforseo-serp-google-organic-best-crm-software-baseline.json` |
| SERP — Google Organic AI Overview-heavy | `dataforseo-serp-google-organic-weather-forecast-ai-overview-baseline.json` |
| AI Optimization — ChatGPT LLM Responses | `dataforseo-ai-optimization-chatgpt-llm-responses-best-crm-software-baseline.json` |
| Labs — Keywords For Site | `dataforseo-labs-google-keywords-for-site-thisiswhyimbroke-baseline.json` |
| Labs — Keyword Overview | `dataforseo-labs-google-keyword-overview-gifts-for-men-baseline.json` |
| Labs — Search Intent | `dataforseo-labs-google-search-intent-gifts-for-men-baseline.json` |
| Labs — Ranked Keywords | `dataforseo-labs-google-ranked-keywords-thisiswhyimbroke-baseline.json` |
| Labs — Historical Rank Overview | `dataforseo-labs-google-historical-rank-overview-thisiswhyimbroke-baseline.json` |

The LLM Mentions, LLM Scraper, and AI Keyword Data surfaces were explicitly
deferred in `dataforseo-capture-plan.md` — LLM Mentions and LLM Scraper because
the credit unlock was not worth it yet, AI Keyword Data because it was not needed
for the first corpus.

---

## The Confidence Layer Distinction

For Batch H DataForSEO work there are now two distinct confidence levels.
These must be preserved when content is promoted into authority docs.

---

### Confidence Level 1 — Payload-Confirmed

Grounded in: actual captured Playground JSON payloads in `transition-steward/dataforseo-json/`

**Applies to:**
- ChatGPT LLM Responses family (`AiSurfaceRun` + child observation families)
  — one baseline payload captured and confirmed
- SERP families — two baseline payloads captured and confirmed
- Labs keyword families — multiple baseline payloads captured and confirmed

**What this means for authority promotion:**
Design decisions grounded at this level may be promoted with high confidence.
Field names, nesting, and optional presence are grounded in real observed
payloads.

---

### Confidence Level 2 — Docs-Confirmed, Unsampled

Grounded in: official DataForSEO documentation at `docs.dataforseo.com` only.
No playground payload captured. No real response JSON in the repo.

**Applies to:**
- LLM Scraper (ChatGPT and Gemini UI scrape) — explicitly deferred in capture plan
- LLM Mentions API — explicitly deferred in capture plan; credit unlock not yet
  done
- Gemini LLM Responses — pending in capture plan; no payload captured yet
- Claude LLM Responses — pending in capture plan; no payload captured yet
- Perplexity LLM Responses — pending in capture plan; no payload captured yet
- AI Keyword Data — explicitly deferred in capture plan
- `AiMentionCluster` family (new family identified in inventory note) — entirely
  docs-derived; no payload exists in the repo

**What this means for authority promotion:**
Design decisions grounded at this level carry genuine uncertainty. The structural
patterns inferred from official docs are a reasonable basis for provisional
design, but they are not yet validated against real payloads. Promotion to
authority docs should carry explicit provisional markers for these sections, and
the design must be treated as subject to correction when live payloads are
captured.

---

## Implications for Each Design Pass Element

### `AiSurfaceRun` and the four child families (LLM Responses surface)
**Confidence: Payload-Confirmed for ChatGPT. Docs-Confirmed for Gemini, Claude, Perplexity.**

The top-level family structure is grounded in the captured ChatGPT LLM Responses
baseline. The docs-based verification pass confirmed that LLM Responses schema
is consistent across platforms at the top level. However, the platform
comparisons in `dataforseo-capture-plan.md` are still pending — Claude, Gemini,
and Perplexity LLM Responses payloads have not been captured.

For authority promotion: mark the `AiSurfaceRun` family design as
payload-confirmed for ChatGPT. Mark the multi-platform posture (the `platform`
field accommodating all four providers) as docs-confirmed-only until the pending
provider comparison captures are done.

### `AiMentionCluster` (new family from inventory note)
**Confidence: Docs-Confirmed only. No payload. No prior workflow basis.**

The `AiMentionCluster` family was entirely derived from the official LLM Mentions
API docs. There is no playground payload for LLM Mentions in the repo. The
credit unlock has not been done. This family is the most speculative element of
the Batch H design work.

For authority promotion: `AiMentionCluster` should be listed as a
**deferred-but-owned** domain in `veda/schema-reference.md`, not as a fully
governed canonical family. The same pattern used for the original deferred
families applies here. It must not be implemented ad hoc, but its full family
design should not be locked into authority docs until at least one real LLM
Mentions payload is captured and inventoried.

### LLM Scraper structural findings
**Confidence: Docs-Confirmed only. No payload.**

The `AiCitationObservation` field additions (`snippetText`, `publicationDate`)
derived from LLM Scraper `sources[]` are docs-confirmed. They are reasonable
additions but should be treated as provisional until an LLM Scraper payload is
captured.

### Background retrieval (`search_results`) — recommendation to preserve in `rawPayload`
**Confidence: Docs-Confirmed for existence. No payload to evaluate field richness.**

The recommendation in the inventory note to not canonicalize `search_results`
yet is the right conservative call, and it aligns with the payload-first
principle. Do not govern what you have not seen.

### SERP and Labs families
**Confidence: Payload-Confirmed.**

These are out of scope for the AI-surface family design pass. The existing
baselines confirm payload shapes for these families. No change required.

---

## What Should Happen When Credits Are Added

When LLM Mentions credits are unlocked and the first LLM Mentions payload is
captured, treat it as a validation and correction input for `AiMentionCluster`
design — not a nice-to-have.

The capture workflow should follow the existing pattern:
1. Pull from Playground under chosen settings
2. Save raw JSON to `transition-steward/dataforseo-json/` with a clear filename
3. Write an inventory note documenting actual payload structure
4. Compare against the docs-confirmed design in the inventory note
5. Note any discrepancies
6. Only then promote `AiMentionCluster` from deferred-but-owned to governed
   canonical family

The same applies to LLM Scraper when that surface is sampled.

---

## How to Read the Three Batch H DataForSEO Documents Together

| Document | What it contains | Confidence grounding |
|---|---|---|
| `batch-h-veda-family-design-pass.md` — AI-surface sections | Full family designs for `AiSurfaceRun` and four child families | Payload-confirmed for ChatGPT LLM Responses; docs-confirmed for other platforms |
| `batch-h-dataforseo-surface-inventory.md` | Structural inventory of all four DataForSEO AI Optimization sub-products; identifies `AiMentionCluster` as a required new family | Docs-confirmed throughout; no new payload captures done in this note |
| This note | Explicit confidence-layer distinction for all DataForSEO design work | Meta-layer; references both the above and the capture plan |

**Reading order before authority update:** This note first, then design pass, then inventory note, then corrections note. This note sets the confidence context that governs how strongly to rely on each section of the others.

---

## Summary of What Should Be Promoted vs. Held

| Element | Promote to authority? | As what? |
|---|---|---|
| `AiSurfaceRun` family | Yes | Governed canonical family — note ChatGPT payload-confirmed, multi-platform docs-confirmed |
| `AiMentionObservation` | Yes | Governed canonical family |
| `AiCitationObservation` | Yes, with provisional `snippetText` / `publicationDate` fields | Governed canonical family — note LLM Scraper field additions are docs-confirmed only |
| `AiFanOutQueryObservation` | Yes | Governed canonical family |
| `AiEntityObservation` | Yes | Governed canonical family |
| `AiMentionCluster` | No — not yet | Deferred-but-owned; same treatment as the original deferred domains in schema-reference |
| LLM Scraper `search_results` as `AiRetrievalObservation` | No | Not yet; preserve in rawPayload; govern when payload captured |
| AI Keyword Data family | No | Deferred-but-owned; flag for future governance |

---

## Related Files

- `transition-steward/batch-h-veda-family-design-pass.md`
- `transition-steward/batch-h-veda-family-design-pass-corrections.md`
- `transition-steward/batch-h-dataforseo-surface-inventory.md`
- `transition-steward/dataforseo-capture-plan.md`
- `transition-steward/dataforseo-json/` (the confirmed payload corpus)
