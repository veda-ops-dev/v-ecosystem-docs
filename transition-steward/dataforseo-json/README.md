# DataForSEO JSON Samples — Folder README

## Folder Purpose

This folder contains representative DataForSEO API sample payloads and paired inventory notes collected during the VedaOps documentation transition.

These samples are transition-support artifacts.

They exist to answer:

```
What does the actual DataForSEO response structure look like for a given endpoint family,
and what fields, types, and structural variations should VEDA's canonical modeling account for?
```

---

## Rules

1. **Samples are transition-support artifacts — not authority doctrine.** Nothing in this folder overrides `veda/schema-reference.md`, `veda/providers/registry.md`, or any ecosystem-level doctrine doc.
2. **Samples are not schema contracts.** The presence of a field in a sample payload does not mean VEDA must canonically model that field.
3. **Raw payloads should be paired with inventory notes.** Every `.json` file should have a companion `.md` inventory file with the same base filename.
4. **Filenames encode provider + family + context + variant.** See the Naming Pattern section below.
5. **Do not store credentials, account data, or billing information** in this folder.
6. **Do not confuse provider archives with canonical truth.** The JSON here is raw observatory evidence, not final doctrine.

---

## Current Contents

### SERP — Google Organic Advanced

**`dataforseo-serp-google-organic-best-crm-software-baseline.json`**
— Baseline sample for SERP Google Organic Advanced (keyword: `best crm software`, US, en).

**`dataforseo-serp-google-organic-best-crm-software-baseline-inventory.md`**
— Inventory for the above sample.

**`dataforseo-serp-google-organic-weather-forecast-ai-overview-baseline.json`**
— Baseline sample for SERP Google Organic Advanced with an AI Overview present (keyword: `weather forecast`, US, en).

**`dataforseo-serp-google-organic-weather-forecast-ai-overview-baseline-inventory.md`**
— Inventory for the above sample.

---

### AI Optimization — ChatGPT LLM Responses

**`dataforseo-ai-optimization-chatgpt-llm-responses-best-crm-software-baseline.json`**
— Baseline sample for AI Optimization ChatGPT LLM Responses (keyword: `best crm software`).

**`dataforseo-ai-optimization-chatgpt-llm-responses-best-crm-software-baseline-inventory.md`**
— Inventory for the above sample.

Important note:
this is a **ChatGPT LLM Responses** sample, not proof of a direct **LLM Mentions Search** endpoint shape.

---

### DataForSEO Labs — Keywords For Site

**`dataforseo-labs-google-keywords-for-site-thisiswhyimbroke-baseline.json`**
— Baseline sample for Labs Keywords For Site on `thisiswhyimbroke.com`.

**`dataforseo-labs-google-keywords-for-site-thisiswhyimbroke-baseline-inventory.md`**
— Inventory for the above sample.

---

### DataForSEO Labs — Keyword Overview

**`dataforseo-labs-google-keyword-overview-gifts-for-men-baseline.json`**
— Baseline sample for Labs Keyword Overview (keyword: `gifts for men`).

**`dataforseo-labs-google-keyword-overview-gifts-for-men-baseline-inventory.md`**
— Inventory for the above sample.

---

### DataForSEO Labs — Ranked Keywords

**`dataforseo-labs-google-ranked-keywords-thisiswhyimbroke-baseline.json`**
— Baseline sample for Labs Ranked Keywords on `thisiswhyimbroke.com`.

**`dataforseo-labs-google-ranked-keywords-thisiswhyimbroke-baseline-inventory.md`**
— Inventory for the above sample.

---

### DataForSEO Labs — Historical Rank Overview

**`dataforseo-labs-google-historical-rank-overview-thisiswhyimbroke-baseline.json`**
— Baseline sample for Labs Historical Rank Overview on `thisiswhyimbroke.com`.

**`dataforseo-labs-google-historical-rank-overview-thisiswhyimbroke-baseline-inventory.md`**
— Inventory for the above sample.

---

### DataForSEO Labs — Search Intent

**`dataforseo-labs-google-search-intent-gifts-for-men-baseline.json`**
— Baseline sample for Labs Search Intent (keyword: `gifts for men`).

**`dataforseo-labs-google-search-intent-gifts-for-men-baseline-inventory.md`**
— Inventory for the above sample.

---

### DataForSEO Labs — Keywords For Categories

**`dataforseo-labs-google-keywords-for-categories-arts-and-entertainment-baseline.json`**
— Baseline sample for Labs Keywords For Categories (category: `Arts & Entertainment`, US, en, `category_intersection = true`, `include_serp_info = false`, `include_clickstream_data = false`).

**`dataforseo-labs-google-keywords-for-categories-arts-and-entertainment-baseline-inventory.md`**
— Inventory for the above sample.

Important note:
this broad category baseline is useful for endpoint-shape understanding, but it is noisy and not a clean strategic target list.

---

## Next Planned Additions

See `../dataforseo-research-tracker.md` for the full backlog and cost-aware plan.

### Low-price next pulls

| Filename | Endpoint family | Why next |
|---|---|---|
| `dataforseo-labs-google-keywords-for-categories-[narrower-category]-baseline.json` + inventory | Labs — Keywords For Categories | Cheap comparison sample to test whether current noise comes from broad category choice. |
| `dataforseo-labs-google-keywords-for-categories-[same-or-narrower-category]-serp-info.json` + inventory | Labs — Keywords For Categories | Same comparison family, but with `include_serp_info = true` to inspect SERP shape. |
| `dataforseo-labs-google-keyword-overview-[keyword]-comparison-baseline.json` + inventory | Labs — Keyword Overview | Cheap second keyword-centric baseline for structural comparison. |
| `dataforseo-labs-google-search-intent-[keyword]-comparison-baseline.json` + inventory | Labs — Search Intent | Cheap direct intent comparison sample. |

### Higher-price later pulls

| Filename | Endpoint family | Why later |
|---|---|---|
| `dataforseo-ai-optimization-google-llm-mentions-[keyword]-baseline.json` + inventory | AI Optimization — direct LLM mentions / search | Access not yet confirmed in current Playground/account state. |
| `dataforseo-ai-optimization-llm-mentions-aggregated-metrics-[context]-baseline.json` + inventory | AI Optimization — Aggregated Metrics | Access not yet confirmed and likely more expensive than current low-cost comparison work. |
| `dataforseo-labs-google-keyword-overview-[keyword]-clickstream-expansion.json` + inventory | Labs — Keyword Overview with clickstream | Known cost multiplier. Wait for refill. |
| `dataforseo-serp-google-ai-mode-[keyword]-baseline.json` + inventory | SERP — Google AI Mode Advanced | Structurally interesting, but not cheap first-priority work. |
| `dataforseo-serp-google-organic-[keyword]-rectangles-stress-test.json` + inventory | SERP — rectangle-enabled sampling | Cost-heavy stress sample. |
| `dataforseo-serp-google-organic-[keyword]-paa-depth-1.json` + inventory | SERP — PAA click-depth expansion | Useful later, but not budget-smart now. |

---

## Naming Pattern

```
dataforseo-[family-slug]-[search-engine-if-applicable]-[endpoint-slug]-[context]-[variant].json
```

### Family slug examples

| Family | Slug |
|---|---|
| SERP | `serp` |
| AI Optimization | `ai-optimization` |
| DataForSEO Labs | `labs` |
| Backlinks | `backlinks` |
| Keywords Data | `keywords-data` |

### Search engine / platform slug examples

| Engine / platform | Slug |
|---|---|
| Google | `google` |
| ChatGPT | `chatgpt` |
| Bing | `bing` |

### Variant tags

| Variant | Tag |
|---|---|
| Baseline (minimal flags) | `baseline` |
| Comparison baseline | `comparison-baseline` |
| With clickstream data | `clickstream-expansion` |
| With rectangles | `rectangles-stress-test` |
| PAA expanded | `paa-depth-[n]` |
| SERP info comparison | `serp-info` |

### Examples

```
dataforseo-serp-google-organic-best-crm-software-baseline.json
dataforseo-serp-google-organic-weather-forecast-ai-overview-baseline.json
dataforseo-labs-google-keyword-overview-gifts-for-men-baseline.json
dataforseo-labs-google-keywords-for-categories-arts-and-entertainment-baseline.json
dataforseo-ai-optimization-chatgpt-llm-responses-best-crm-software-baseline.json
dataforseo-ai-optimization-google-llm-mentions-[keyword]-baseline.json
```

---

## Related Docs

- `../dataforseo-research-tracker.md` — steering tracker for endpoint families, sample status, and low-cost vs high-cost follow-up work
- `../../veda/providers/registry.md` — active provider registry (authority doc)
- `../../veda/schema-reference.md` — canonical schema authority for VEDA observatory models
