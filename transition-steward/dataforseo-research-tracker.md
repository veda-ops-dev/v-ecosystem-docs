# DataForSEO Research Tracker

## Purpose

This is a transition-support tracking document for DataForSEO provider research, JSON sample payloads, and deferred observatory surfaces.

It exists to answer:

```
What DataForSEO endpoint families matter for VedaOps, what has already been sampled,
what is pending, what is deferred, what is currently accessible, and what should be
captured next at low cost vs higher cost?
```

**This document is not authority doctrine.**
**This document is not implementation truth.**
**This document is not a schema contract.**

It is a working tracker to prevent drift, redundant work, and budget-blind sample pulling.

### Deferred vs. Forgotten

Deferred does not mean forgotten.

Deferred means: not yet admitted into canonical observatory modeling. The surface matters; the work simply has not reached the point where it can be canonically modeled in VEDA's schema-reference without risk of premature lock-in.

When a surface moves from deferred to active, it must go through governed schema-reference design before VEDA canonical tables are defined for it.

---

## Status Legend

| Status | Meaning |
|---|---|
| **Canonical now** | Admitted to VEDA canonical observatory modeling. Schema design should proceed. |
| **Archive now, model later** | Pull and preserve raw JSON. Do not canonicalize yet. Modeling deferred pending schema-reference design. |
| **Deferred pending sample** | No sample yet. Need at least one baseline pull before deciding modeling posture. |
| **Deferred pending more samples** | At least one sample exists but structural variation is insufficiently understood. More pulls needed before modeling. |
| **Deferred pending access confirmation** | The surface may exist in docs or API, but current Playground/account access is not yet confirmed. |
| **Deferred pending schema-reference design** | Sample(s) exist. Structural behavior is understood. Canonical modeling blocked pending governed schema-reference work. |
| **Low priority / revisit later** | Not needed for current transition phase. Track but do not schedule now. |
| **Out of scope for current transition** | Not relevant to VEDA or VedaOps goals. Not tracked further unless scope changes. |

---

## Budget Legend

| Budget tier | Meaning |
|---|---|
| **Low** | Safe for cheap structural comparison work. Prefer for remaining small credit balances. |
| **Medium** | Useful but should be pulled deliberately, not casually repeated. |
| **High** | Expensive or cost-multiplying. Pull only when specifically justified or after refill. |

---

## Current Repo-Confirmed Sample Corpus

The following sample families are present in `transition-steward/dataforseo-json/` and have inventory notes:

1. SERP — Google Organic Advanced
2. SERP — Google Organic Advanced with AI Overview present
3. AI Optimization — ChatGPT LLM Responses
4. DataForSEO Labs — Keywords For Site
5. DataForSEO Labs — Keyword Overview
6. DataForSEO Labs — Ranked Keywords
7. DataForSEO Labs — Historical Rank Overview
8. DataForSEO Labs — Search Intent
9. DataForSEO Labs — Keywords For Categories

Important correction:
current repo evidence supports **AI Optimization — ChatGPT LLM Responses**, not a direct **LLM Mentions Search** baseline. Do not blur those two surfaces.

---

## Tracking Table

| Endpoint family | Status | Budget tier | Why it matters | Evidence in repo | Next action |
|---|---|---:|---|---|---|
| SERP — Google Organic Advanced | Archive now, model later | Medium | Primary SERP truth surface. Organic rank positions, SERP feature items, PAA, AI Overview structure, citation observability. | `dataforseo-serp-google-organic-best-crm-software-baseline.json` + inventory; `dataforseo-serp-google-organic-weather-forecast-ai-overview-baseline.json` + inventory | Keep raw archive. Defer canonical SERP modeling to schema-reference work. |
| AI Optimization — ChatGPT LLM Responses | Archive now, model later | High | AI-surface answer-behavior observability. Useful for visible answer sections, token/spend telemetry, and citation/source behavior. | `dataforseo-ai-optimization-chatgpt-llm-responses-best-crm-software-baseline.json` + inventory | Keep raw archive. Do not treat this as proof of LLM Mentions Search shape. |
| AI Optimization — LLM Mentions Search (Google / AIO-facing) | Deferred pending access confirmation | High | Needed to understand direct AI mention / citation surfaces outside ChatGPT answer-response payloads. | None yet | Confirm actual Playground/API access first, then pull one baseline. |
| AI Optimization — LLM Mentions Aggregated Metrics | Deferred pending access confirmation | High | Aggregated `ai_search_volume` / impression-type observability grouped by dimension. Potentially valuable later, but not yet verified in current Playground/account state. | None yet | Revisit after access changes or direct API confirmation. |
| SERP — Google AI Mode Advanced | Deferred pending sample | High | Distinct answer surface. Structurally different from Google Organic + AI Overview. | None yet | Pull only after refill or explicit priority need. |
| DataForSEO Labs — Keywords For Site | Archive now, model later | Medium | Domain keyword footprint baseline. Core domain-scoped observatory surface. | `dataforseo-labs-google-keywords-for-site-thisiswhyimbroke-baseline.json` + inventory | Keep raw archive. Later schema-reference work can separate discovery row from provider metric families. |
| DataForSEO Labs — Keyword Overview | Archive now, model later | Low | Per-keyword provider metric baseline. Core keyword observatory record. | `dataforseo-labs-google-keyword-overview-gifts-for-men-baseline.json` + inventory | Keep raw archive. One more controlled comparison sample is worthwhile later. |
| DataForSEO Labs — Ranked Keywords | Archive now, model later | Medium | Domain visibility observatory surface. Includes aggregate visibility metrics plus per-keyword target-domain ranking state. | `dataforseo-labs-google-ranked-keywords-thisiswhyimbroke-baseline.json` + inventory | Keep raw archive. Compare later against competitor surfaces only when needed. |
| DataForSEO Labs — Historical Rank Overview | Archive now, model later | High | Monthly domain visibility time-series. Strong temporal observatory surface. | `dataforseo-labs-google-historical-rank-overview-thisiswhyimbroke-baseline.json` + inventory | Do not casually repeat. Pull again only for a deliberate comparison need. |
| DataForSEO Labs — Search Intent | Archive now, model later | Low | Direct provider intent classification and intent probability surface. Also useful for comparing direct intent endpoint vs embedded intent fields. | `dataforseo-labs-google-search-intent-gifts-for-men-baseline.json` + inventory; embedded intent also present in Keyword Overview inventory | Keep raw archive. One more cheap comparison sample is optional later. |
| DataForSEO Labs — Keywords For Categories | Deferred pending more samples | Low | Category-scoped keyword discovery. Useful for category-level opportunity observability, but current broad sample is noisy and not yet doctrine-ready. | `dataforseo-labs-google-keywords-for-categories-arts-and-entertainment-baseline.json` + inventory | Pull controlled comparison samples: narrower category, then one SERP-info-enabled variant. |
| DataForSEO Labs — Keyword Suggestions | Deferred pending schema-reference design | Low | Google Autocomplete-type discovery. Useful once keyword observatory families are more settled. | None yet | Revisit after core keyword families are stabilized. |
| DataForSEO Labs — Related Keywords | Deferred pending schema-reference design | Low | Related-search discovery companion to keyword suggestions. | None yet | Revisit alongside Keyword Suggestions. |
| DataForSEO Labs — Keyword Ideas | Deferred pending sample | Medium | Distinct idea-generation surface using different provider logic from Overview/Suggestions. | None yet | Pull later after cheaper comparison work is complete. |
| DataForSEO Labs — Competitors / SERP Competitors | Deferred pending sample | Medium | Competitor discovery based on overlapping SERP behavior. | None yet | Pull only after domain visibility baselines are considered sufficient. |
| DataForSEO Labs — Competitors Domain | Deferred pending sample | Medium | Organic and paid competitor landscape by domain. | None yet | Revisit after ranked keyword work is mature. |
| DataForSEO Labs — Domain Intersection | Low priority / revisit later | Medium | Overlap / gap analysis between domains. Useful later, not current priority. | None yet | Revisit later. |
| DataForSEO Labs — Relevant Pages | Low priority / revisit later | Medium | Page-level visibility surface. Useful after domain-level observability is stable. | None yet | Revisit later. |
| DataForSEO Labs — Domain Rank Overview | Low priority / revisit later | Medium | Current domain visibility summary. Lower value right now than Ranked Keywords + Historical Rank Overview. | None yet | Revisit later. |
| DataForSEO Labs — Historical Keyword Data | Low priority / revisit later | Medium | Historical keyword volume enrichment. | None yet | Revisit after keyword observatory modeling is more settled. |
| DataForSEO Labs — Bulk Traffic Estimation | Low priority / revisit later | Medium | Bulk estimation surface. Potentially useful later, not current priority. | None yet | Revisit later. |
| DataForSEO Labs — Historical Bulk Traffic Estimation | Low priority / revisit later | High | Historical ETV estimation in bulk. Useful but not transition-critical. | None yet | Revisit later. |
| Backlinks — Summary / Bulk Ranks | Deferred pending sample | Medium | Standalone authority surface. Useful for competitor/domain profiling. | None yet | Pull one summary sample only after refill or explicit priority. |
| Backlinks — Backlink History | Low priority / revisit later | Medium | Historical backlink trend observability. Useful later, not blocking. | None yet | Revisit later. |
| SERP — Rectangle-enabled sampling | Deferred pending sample | High | Pixel-position observability. Valuable but cost-heavy. | None yet | Pull one stress-test only when justified. |
| SERP — PAA click-depth expansion | Deferred pending sample | High | Deeper PAA nesting observability. Cost rises with depth. | None yet | Pull depth 1 only when explicitly needed. |
| Labs — Clickstream-enabled expansions | Deferred pending sample | High | Adds clickstream-normalized fields and demographics. Important, but a known cost multiplier. | None yet | Wait for refill. Pull only controlled expansions after baseline shape is settled. |
| Keywords Data API — Google Ads Search Volume | Low priority / revisit later | Low | Lighter bulk volume surface. Secondary to richer Labs surfaces. | None yet | Revisit only if Labs bulk cost becomes a blocker. |
| Content Analysis API | Low priority / revisit later | Medium | Open-web citation/mention tracking. Interesting later, not current transition priority. | None yet | Revisit later. |
| OnPage API | Low priority / revisit later | Medium | Technical SEO audit surface. Not current observatory priority. | None yet | Revisit under specific pressure. |
| Business Data API | Out of scope for current transition | — | Local business profile observability. Not current project type scope. | None yet | Revisit only if scope expands. |
| App Data API | Out of scope for current transition | — | App store observability. Not current project type scope. | None yet | — |
| Merchant API | Out of scope for current transition | — | E-commerce listing observability. Not current project type scope. | None yet | — |
| Domain Technology API | Out of scope for current transition | — | Technographic surface. Not current VEDA observatory priority. | None yet | — |

---

## Cost-Aware Next Capture Plan

### Low-price next pulls

These are the best follow-up pulls when credit is limited and the goal is **structural learning**, not bulk harvesting.

1. **Keywords For Categories — narrower category baseline**
   - Keep cheap settings:
     - `limit = 10`
     - `offset = 0`
     - `include_clickstream_data = false`
     - `include_serp_info = false`
   - Goal: determine whether current noise came mainly from broad category choice.

2. **Keywords For Categories — SERP-info comparison**
   - Same category and same settings as the narrower baseline, except:
     - `include_serp_info = true`
   - Goal: observe `serp_info` shape for this endpoint without changing other variables.

3. **Keyword Overview — one controlled comparison sample**
   - Cheap baseline posture:
     - `include_serp_info = true`
     - `include_clickstream_data = false`
   - Goal: compare a second keyword-centric metric row against the current baseline.

4. **Search Intent — one direct comparison sample**
   - Goal: compare direct intent endpoint behavior on another keyword and confirm label/probability posture.

### Higher-price later pulls

These should wait until refill or explicit priority.

1. **AI Optimization — direct LLM mentions / search surfaces**
2. **AI Optimization — aggregated metrics surfaces**
3. **Historical Rank Overview repeats**
4. **Clickstream-enabled Labs expansions**
5. **SERP AI Mode / rectangle / deep PAA stress samples**

---

## Controlled-Sampling Rules

Use these rules unless there is a specific reason not to:

1. **Change one setting at a time.**
2. **Use `limit = 10` for cheap exploratory comparisons.**
3. **Use `limit = 25` for first baseline samples when budget allows.**
4. **Keep `offset = 0` for first-pass structure inspection.**
5. **Do not enable clickstream casually.**
6. **Do not treat broad-category head-term returns as strategy truth.**
7. **Do not treat Playground availability as guaranteed API availability, or vice versa. Confirm both separately when it matters.**

---

## Key Structural Risks to Track During Sampling

- **`load_async_ai_overview` default is false** — silently omits a significant subset of AI Overviews. Always set to `true` for AI Overview observation samples.
- **`include_clickstream_data` increases cost materially** — authorize before any repeated or bulk use.
- **ChatGPT LLM Responses and LLM Mentions Search are not the same surface** — do not collapse them into one family.
- **Direct API docs / product docs may not match current Playground visibility** — confirm actual access before writing pull plans as if they are immediately runnable.
- **`ai_search_volume` is not `search_volume`** — preserve as distinct named fields if and when aggregated metrics are sampled.
- **`search_intent_info` is provider-assigned** — it is an observatory attribute, not a VEDA-computed category.
- **Monthly searches array vs scalar volume** — preserve the full array, not just the current scalar.
- **Category-scoped discovery can be noisy** — broad categories can yield navigational, typo, and brand-heavy rows that are useful for endpoint understanding but not immediate strategic targeting.

---

## Related Files

- `transition-steward/dataforseo-json/README.md` — folder index for sample payloads
- `veda/providers/registry.md` — active provider registry (authority doc)
- `veda/schema-reference.md` — canonical schema authority (deferred AI-surface and crawled-content families noted there)
- `ecosystem/external-provider-integration-doctrine.md` — provider admission doctrine
