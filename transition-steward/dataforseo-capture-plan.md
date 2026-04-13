# DataForSEO Capture Plan

## Purpose

This document is the operational pull list for the transition-support DataForSEO JSON corpus.

It exists to answer one question clearly:

> What sample payloads have already been captured, what is still supposed to be captured, and what should be deferred for later?

This document is:
- a transition-support capture checklist
- a working intake plan for representative JSON payloads
- a memory aid so the capture workflow does not depend on chat history

This document is **not**:
- authority doctrine
- schema authority
- implementation truth
- VEDA Strategy logic

Settled architecture belongs in authority docs.
Deferred or in-progress provider sample work belongs here.

---

## Ground Rules

1. **Filename must match the actual payload.**
   Before saving a file, confirm the JSON `path` and `data.function` match the intended endpoint.

2. **Raw JSON is preserved as pulled.**
   Do not edit payload contents.

3. **Inventory notes are separate files.**
   JSON samples stay raw. Interpretation belongs in paired `-inventory.md` files.

4. **Provider fields are observatory inputs, not strategy conclusions.**
   Keyword difficulty, intent, ETV, backlink context, AI response wrappers, and SERP feature signatures are provider observations or provider-computed metrics.

5. **Deferred does not mean forgotten.**
   Deferred means the sample is not needed yet, or the surface is not ready for canonical modeling.

6. **Playground UI can mislead.**
   Validate the saved payload, not just the screen label.

---

## Status Legend

| Status | Meaning |
|---|---|
| **Complete** | JSON sample is saved and valid for the intended endpoint family. |
| **Complete — inventory pending** | JSON sample is saved and valid, but the paired `-inventory.md` file still needs to be written. |
| **Pending** | This sample is still supposed to be captured next. |
| **Needs correction** | A sample was saved under the wrong name or from the wrong endpoint and needs re-pull or rename. |
| **Deferred** | Valuable later, but not needed for the current first-pass corpus. |
| **Later expansion** | Intentionally postponed follow-up or variant sample after the baseline corpus is stable. |

---

## Current Captured Baseline Corpus

These files are already in the repo and should remain part of the first-pass corpus.

| Capture | Status | File |
|---|---|---|
| SERP — Google Organic baseline | **Complete** | `transition-steward/dataforseo-json/dataforseo-serp-google-organic-best-crm-software-baseline.json` |
| SERP — Google Organic AI Overview-heavy baseline | **Complete** | `transition-steward/dataforseo-json/dataforseo-serp-google-organic-weather-forecast-ai-overview-baseline.json` |
| AI Optimization — ChatGPT — LLM Responses baseline | **Complete** | `transition-steward/dataforseo-json/dataforseo-ai-optimization-chatgpt-llm-responses-best-crm-software-baseline.json` |
| Labs — Keywords For Site baseline | **Complete** | `transition-steward/dataforseo-json/dataforseo-labs-google-keywords-for-site-thisiswhyimbroke-baseline.json` |
| Labs — Keyword Overview baseline | **Complete** | `transition-steward/dataforseo-json/dataforseo-labs-google-keyword-overview-gifts-for-men-baseline.json` |
| Labs — Search Intent baseline | **Complete — inventory pending** | `transition-steward/dataforseo-json/dataforseo-labs-google-search-intent-gifts-for-men-baseline.json` |
| Labs — Ranked Keywords baseline | **Complete — inventory pending** | `transition-steward/dataforseo-json/dataforseo-labs-google-ranked-keywords-thisiswhyimbroke-baseline.json` |
| Labs — Historical Rank Overview baseline | **Complete — inventory pending** | `transition-steward/dataforseo-json/dataforseo-labs-google-historical-rank-overview-thisiswhyimbroke-baseline.json` |

### Notes on the current corpus

- The current **Historical Rank Overview** baseline uses a shorter valid date range (`2024-01-01` through `2026-04-10`). That is acceptable for baseline capture.
- The current **AI Optimization / ChatGPT / LLM Responses** baseline filename is usable, but it does **not** include the model name. Future captures should include the model in the filename.
- The current first-pass Labs spine is now present in raw JSON form.

---

## Immediate Next Required Work

These are the next items that should be done in order.

### 1. Write the missing inventory files

These JSON payloads are already saved and valid. They now need paired inventory notes.

| Priority | Status | File | Companion inventory to create |
|---|---|---|---|
| 1 | **Pending** | `dataforseo-labs-google-search-intent-gifts-for-men-baseline.json` | `dataforseo-labs-google-search-intent-gifts-for-men-baseline-inventory.md` |
| 2 | **Pending** | `dataforseo-labs-google-ranked-keywords-thisiswhyimbroke-baseline.json` | `dataforseo-labs-google-ranked-keywords-thisiswhyimbroke-baseline-inventory.md` |
| 3 | **Pending** | `dataforseo-labs-google-historical-rank-overview-thisiswhyimbroke-baseline.json` | `dataforseo-labs-google-historical-rank-overview-thisiswhyimbroke-baseline-inventory.md` |

### 2. Capture a clean model-labeled AI Optimization baseline

The existing ChatGPT LLM Responses baseline is valid, but future naming should include the model name.

| Status | Target | Exact filename |
|---|---|---|
| **Pending** | AI Optimization → LLM Responses → ChatGPT → strongest available model (`gpt-5` preferred; `gpt-5-mini` second; `o4-mini` acceptable fallback) | `dataforseo-ai-optimization-chatgpt-llm-responses-[model]-best-crm-small-business-baseline.json` |

#### Recommended baseline settings

- Function: `LLM Responses`
- SE: `ChatGPT`
- Model: `gpt-5` if available
- Web Search: `Enable`
- Web Search Country: `United States`
- Force Web Search: `Disable`
- Prompt: a current, citation-friendly business query
- Max Output Tokens: `2048`
- Message Chain: empty

#### Validation before saving

Confirm in the saved JSON:
- `path` includes `ai_optimization / chat_gpt / llm_responses / live`
- `data.function = llm_responses`
- response contains the resolved model actually used

---

## Next Capture Queue

These are the next JSON captures to add after the missing inventory files are written.

### A. AI Optimization — model and provider comparison pulls

These help separate endpoint behavior from model/provider behavior.

| Order | Status | Why it matters | Exact filename |
|---|---|---|---|
| 1 | **Pending** | Smaller ChatGPT comparison against the clean baseline | `dataforseo-ai-optimization-chatgpt-llm-responses-[secondary-model]-best-crm-small-business-baseline.json` |
| 2 | **Pending** | Claude answer-surface wrapper comparison | `dataforseo-ai-optimization-claude-llm-responses-[model]-best-crm-small-business-baseline.json` |
| 3 | **Pending** | Gemini answer-surface wrapper comparison | `dataforseo-ai-optimization-gemini-llm-responses-[model]-best-crm-small-business-baseline.json` |
| 4 | **Pending** | Perplexity answer-surface wrapper comparison | `dataforseo-ai-optimization-perplexity-llm-responses-[model]-best-crm-small-business-baseline.json` |

#### Validation before saving

For each of the above, confirm:
- `path` contains the correct provider family
- `data.function = llm_responses`
- filename includes the actual provider and chosen model

### B. SERP expansion pulls

These are useful structural variants after the baseline SERP set is stable.

| Order | Status | Why it matters | Exact filename |
|---|---|---|---|
| 5 | **Later expansion** | One controlled PAA nesting sample | `dataforseo-serp-google-organic-[keyword]-paa-depth-1.json` |
| 6 | **Later expansion** | One rectangles/pixel-position stress sample | `dataforseo-serp-google-organic-[keyword]-rectangles.json` |

#### Validation before saving

For PAA depth sample, confirm the request reflects the PAA expansion setting.
For rectangles sample, confirm the request enabled rectangle geometry and the payload actually includes the extra geometry fields.

### C. Labs clickstream expansion

| Order | Status | Why it matters | Exact filename |
|---|---|---|---|
| 7 | **Later expansion** | Compare `keyword_overview` baseline against clickstream-enabled shape | `dataforseo-labs-google-keyword-overview-[keyword]-clickstream-expansion.json` |

#### Validation before saving

Confirm:
- endpoint is still `keyword_overview`
- clickstream-enabled objects are actually populated or at least structurally changed from baseline
- filename says `clickstream-expansion`

### D. Backlinks baseline

| Order | Status | Why it matters | Exact filename |
|---|---|---|---|
| 8 | **Pending** | Standalone authority/context baseline outside Labs embedding | `dataforseo-backlinks-summary-[domain]-baseline.json` |

---

## Conditional / Deferred Queue

These matter, but they should **not** interrupt the current baseline workflow.

| Surface | Status | Reason |
|---|---|---|
| AI Optimization — LLM Mentions | **Deferred** | Important if available, but do not invent a capture flow if the Playground or current docs path being used does not expose it clearly. Validate the surface exists before planning filenames. |
| AI Optimization — LLM Scraper | **Deferred** | Separate surface from LLM Responses. Useful later, not required for the first corpus. |
| AI Optimization — AI Keyword Data | **Deferred** | Useful later for AI-surface keyword visibility work; not needed before the baseline answer-surface corpus is stable. |
| SERP — Google AI Mode | **Deferred** | Valuable later if accessible, but structurally distinct from standard organic + AI Overview samples. |
| Labs — competitive and overlap surfaces (`SERP Competitors`, `Competitors Domain`, `Domain Intersection`, `Relevant Pages`) | **Deferred** | Good second-wave research. Not needed before the core observatory families are stable. |
| Labs — bulk utility surfaces (`Bulk Keyword Difficulty`, traffic estimation variants) | **Deferred** | Useful after the baseline keyword and rank surfaces are understood. |

---

## Capture Cards for Pending Pulls

Use these cards during manual Playground work.

### Capture card — AI Optimization / ChatGPT / LLM Responses baseline

- Confirm the screen is actually **LLM Responses**, not another AI Optimization function.
- Confirm the provider is **ChatGPT**.
- Select the strongest available model.
- Enable web search.
- Use a stable business comparison prompt.
- Save only after confirming the filename includes the chosen model.

### Capture card — provider comparison baselines

- Keep the prompt theme the same across ChatGPT / Claude / Gemini / Perplexity.
- Do not mix provider comparison with totally different prompts.
- Save each provider response under its own provider/model filename.

### Capture card — SERP expansion variants

- Pull only one PAA depth sample first.
- Pull only one rectangles sample first.
- Do not fan out cost-heavy SERP variants until the baseline set is inventoried.

### Capture card — Labs clickstream expansion

- Use the same keyword as the baseline keyword overview sample if possible.
- Pull the clickstream variant only after the baseline inventory is written.

---

## Known Cautions

1. **`LLM Responses` is not `LLM Mentions`.**
   Do not label answer-generation payloads as mention-observability payloads.

2. **Playground label drift is real.**
   Validate the payload path and function before naming the file.

3. **Historical range issues do not block baseline capture.**
   A shorter valid historical range is acceptable if the payload is structurally correct.

4. **Model name belongs in future AI filenames.**
   The existing legacy baseline is still valid, but future samples should include the model.

5. **Do not let deferred surfaces leak into authority docs.**
   Capture planning stays here; doctrine comes later.

---

## Related Files

- `transition-steward/dataforseo-research-tracker.md`
- `transition-steward/dataforseo-json/README.md`
- `transition-steward/transition-plan.md`

This capture plan is the operational checklist. The tracker remains the broader status map.
