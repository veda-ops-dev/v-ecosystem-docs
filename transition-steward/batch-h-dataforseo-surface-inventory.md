# DataForSEO AI Optimization API — Surface Inventory for VEDA Family Design

## Purpose

This note records the confirmed structure of the DataForSEO AI Optimization API
product suite, verified against official DataForSEO documentation at
`docs.dataforseo.com`.

It exists to resolve open question 12.4 from the Batch H design pass:

> AI-surface platforms not yet sampled. The design pass designed `AiSurfaceRun`
> to carry a `platform` field accommodating multiple platforms. Only ChatGPT LLM
> Responses had been sampled. Other platforms may return structurally different
> response shapes.

This note also identifies structural facts about the DataForSEO product suite
that were not visible at the time of provider admission, with implications for
VEDA family design.

This is a transition-support inventory note, not authority doctrine.
It must be read alongside `batch-h-veda-family-design-pass.md` and
`batch-h-veda-family-design-pass-corrections.md` before authority-doc
promotion work begins.

Sources verified:
- `https://docs.dataforseo.com/v3/ai_optimization-overview/`
- `https://docs.dataforseo.com/v3/ai_optimization-llm_mentions-overview/`
- `https://docs.dataforseo.com/v3/ai_optimization-llm_mentions-search-live/`
- `https://docs.dataforseo.com/v3/ai_optimization-chat_gpt-llm_responses-overview/`
- `https://docs.dataforseo.com/v3/ai_optimization-perplexity-llm_responses-live/`
- `https://dataforseo.com/help-center/what-is-llm-scraper-api-and-what-data-does-it-provide`
- `https://dataforseo.com/help-center/how-to-track-llm-responses-with-dataforseo-apis`
- `https://dataforseo.com/update/fan-out-queries-and-brand-entities`
- `https://dataforseo.com/help-center/how-to-access-search-queries-data-from-chatgpt`

---

## 1. The DataForSEO AI Optimization API is four distinct sub-products

The design pass and the provider admission doc treated DataForSEO AI Optimization
as a single provider with a unified data surface. The official docs reveal it is
four structurally distinct sub-products with meaningfully different response
shapes and data semantics:

| Sub-product | What it supplies | VEDA relevance |
|---|---|---|
| **LLM Responses API** | Live or standard structured responses from ChatGPT, Claude, Gemini, Perplexity — what the model said, with annotations (cited sources) and `fan_out_queries` | Raw AI-surface response capture; mentions, citations, fan-out queries in structured form |
| **LLM Scraper API** | Scraped results from ChatGPT and Gemini web UI — includes `sources`, `fan_out_queries`, `search_results`, structured `items` (text blocks, tables, images, product listings) | Richer citation/entity/fan-out data from live UI surface; structurally different from LLM Responses |
| **LLM Mentions API** | Pre-aggregated mention data for keywords/domains across AI platforms — includes `ai_search_volume`, `monthly_searches`, `sources`, `search_results`, `brand_entities`, `fan_out_queries` | Observatory metrics surface; aggregated, not per-observation-run |
| **AI Keyword Data API** | Search volume estimates based on how frequently keywords are used in AI tools | Keyword intelligence; borderline observatory vs. derived; likely VEDA Strategy territory, not raw observation |

This is a critical structural finding. The design pass assumed a single
`AiSurfaceRun` → child observations model. That model fits LLM Responses and LLM
Scraper well, but it does not fit LLM Mentions, which is an aggregated metrics
surface, not a per-run observation surface.

---

## 2. LLM Responses API — confirmed structure

**Supported platforms:** ChatGPT, Claude, Gemini, Perplexity.

**Delivery methods:**
- ChatGPT, Gemini, Claude: Standard (POST/GET) and Live
- Perplexity: Live only

**Per-result fields confirmed from official docs:**

```
result[]:
  model_name
  input_tokens
  output_tokens
  web_search (boolean)
  money_spent
  datetime
  items[]:
    type: "message"
    sections[]:
      type: "text"
      text: "<response text>"
  annotations[]:           ← cited sources (only when web_search: true)
    title
    url
  fan_out_queries[]        ← background queries model used (ChatGPT, Gemini, Claude, Perplexity)
```

**Key structural facts:**
- `annotations` = citations. Each annotation carries `title` and `url`. Present
  only when `web_search: true`. If model attempts web search but finds nothing,
  array returns empty.
- `fan_out_queries` = background queries the model performed. Now available for
  all four platforms (ChatGPT, Gemini, Claude, Perplexity) per December 2025
  update.
- `items` = the actual structured response content. Contains text sections.
  In LLM Responses, these are text blocks.
- `input_tokens`, `output_tokens`, `money_spent` = provider cost/size metadata.
  Observatory provenance — should be archived in `rawPayload` on `AiSurfaceRun`,
  not promoted as VEDA canonical truth.

**Design pass alignment:** The LLM Responses shape fits the `AiSurfaceRun` +
`AiCitationObservation` (from `annotations`) + `AiFanOutQueryObservation` (from
`fan_out_queries`) model well. No structural correction needed for this surface.

**What is absent from LLM Responses that LLM Scraper adds:** Tables, images,
product listings, structured entity data, `search_results` (all background
retrieval, not just cited sources).

---

## 3. LLM Scraper API — confirmed structure

**Supported platforms:** ChatGPT and Gemini web UI scrape.

**Different from LLM Responses:** LLM Scraper scrapes the live web UI rather than
calling the model API. This means it captures what users actually see in the
ChatGPT/Gemini interface, including richer structured elements.

**Per-result fields confirmed from official docs:**

```
result[]:
  keyword
  location_code
  language_code
  model
  check_url
  datetime
  markdown               ← full response formatted as markdown
  sources[]:             ← all sources the LLM cited in its final answer
    title
    text (snippet)
    url
    publication_date
  items[]:               ← structured response elements
    type: "chat_gpt_text" / "gemini_text"
    type: "chat_gpt_table" / "gemini_table"
    type: "chat_gpt_images" / "gemini_images"
    (additional structured types)
  search_results[]       ← all web search outputs the model retrieved (including
                           unused entries, not just cited sources)
  fan_out_queries[]      ← queries ChatGPT used in web search (requires
                           force_web_search: true; not guaranteed)
  brand_entities[]       ← structured brand entity appearances (from Dec 2025
                           update; ChatGPT only initially)
```

**Key structural facts:**
- `sources` = cited sources in LLM Scraper (equivalent to `annotations` in LLM
  Responses). Fields are richer: `title`, `text` snippet, `url`,
  `publication_date`.
- `search_results` = all background retrieval, including entries the model did
  NOT cite. Distinct from `sources` (cited only). This is an important
  distinction for VEDA — background retrieval vs. actual citations are different
  observations.
- `brand_entities` = structured brand entity array. Present for ChatGPT LLM
  Scraper (as of December 2025 update). Each entity has structured data on brand
  titles and entity properties. This is what the design pass modeled as
  `AiEntityObservation`.
- `markdown` = full response as markdown. Large; belongs in `rawPayload` archive
  on `AiSurfaceRun`, not as a promoted canonical field.
- `items` type names are platform-specific (`chat_gpt_text`, `gemini_text`,
  etc.). This is a schema design implication: if items are ever canonicalized,
  the type vocabulary must accommodate platform-specific values.

**Design pass implications:**
- `AiCitationObservation` maps to `sources[]` in LLM Scraper, which has more
  fields than `annotations[]` in LLM Responses (adds `text` snippet and
  `publication_date`). The canonical family should accommodate both. The richer
  LLM Scraper shape should set the ceiling: `citedUrl`, `citedDomain`,
  `snippetText` (nullable), `publicationDate` (nullable).
- `search_results` (background retrieval, not cited) is a structurally distinct
  observation from `sources` (cited). The design pass did not model this
  separately. See Section 6 below.
- `brand_entities` from LLM Scraper confirms `AiEntityObservation` is the right
  family. The structured entity data validates the design.

---

## 4. LLM Mentions API — confirmed structure and critical design implication

**This is the most architecturally significant finding from this verification
pass.**

The LLM Mentions API is not a per-run observation surface. It is a
**pre-aggregated mentions database** that DataForSEO maintains continuously
across AI platforms. It does not return observations from a single API call to
an LLM. It returns aggregated metrics built from DataForSEO's ongoing AI
surface monitoring.

**Supported platforms:** Google AI Overviews (AIO), ChatGPT (confirmed in docs;
others implied).

**What the LLM Mentions Search endpoint returns per item:**

```
items[]:
  keyword (the query this mention cluster is for)
  platform
  location_code / language_code
  question          ← the AI-generated question
  answer            ← the AI-generated answer text
  sources[]:        ← sources cited in the answer
    domain
    url
    title
    publication_date
  search_results[]  ← background retrieval (not cited)
  ai_search_volume  ← estimated monthly AI search volume for this query
  monthly_searches[]:
    year, month, search_volume
  fan_out_queries[] ← related queries (available for Google AIO and ChatGPT)
  brand_entities[]  ← brand entity data (available for ChatGPT)
  first_response_at
  last_response_at  ← time range of observations in this mention cluster
```

**What this means for VEDA family design:**

LLM Mentions is **not** a source of `AiSurfaceRun` records. It is a source of
pre-aggregated, time-windowed mention clusters. The data model is:

> "For this query, on this platform, in this locale, here is a question-answer
> pair observed, the sources it cited, background retrieval, AI search volume,
> and monthly search trends."

This is structurally distinct from what `AiSurfaceRun` models (a specific
provider call at a specific capture time with raw response). Forcing LLM Mentions
data into the `AiSurfaceRun` → child observations pattern would corrupt the
model:
- `AiSurfaceRun` assumes a specific capture time from a specific call
- LLM Mentions items carry `first_response_at` and `last_response_at` time
  windows, not a single capture timestamp
- `ai_search_volume` and `monthly_searches` are aggregated metrics, not raw
  per-observation counts

**Required addition to the design pass:** A separate canonical family is needed
for LLM Mentions data. Call it `AiMentionCluster` or similar. It is a distinct
observatory record type from `AiSurfaceRun`. See Section 7 below for the
recommended posture.

---

## 5. AI Keyword Data API — boundary classification

The AI Keyword Data API returns search volume estimates based on how frequently
keywords appear in AI tool usage. It delivers `ai_search_volume` as a keyword-
level metric.

**VEDA vs. VEDA Strategy boundary:** This data is borderline. Raw volume
estimates for a specific keyword at a specific capture time could be modeled as
observatory input (what the provider returned about query frequency). But the
primary use of this data is strategic — it is used to decide which keywords to
prioritize. That decision-making use belongs in VEDA Strategy.

**Recommendation:** Classify AI Keyword Data API outputs as observatory input
only if the raw volume number is captured with explicit provider/timestamp
provenance. VEDA stores "what DataForSEO returned for this keyword at this
time." VEDA Strategy interprets "what that means for prioritization." Do not
conflate. The AI Keyword Data family, if governed, should look like a
`KeywordTarget`-adjacent observation record, not a strategic scoring record.

This family is out of scope for the current Batch H pass. Flag for future
governance when AI Keyword Data is first used in implementation.

---

## 6. `search_results` vs `sources` — a structural distinction the design pass missed

Both LLM Responses (`annotations`) and LLM Scraper (`sources`, `search_results`)
surface two distinct classes of source-related data:

- **Cited sources** (`annotations` / `sources`): what the model actually cited
  in its final answer. These are citation observations.
- **Background retrieval** (`search_results`): all web search outputs the model
  retrieved when looking up information, including entries it did NOT cite in the
  final answer. These are NOT citation observations — they are retrieval
  observations.

The design pass modeled `AiCitationObservation` for cited sources. It did not
model background retrieval at all.

**Whether VEDA should canonicalize background retrieval observations is a design
decision, not a confirmed gap.** Arguments:
- Background retrieval is observable external reality (what the AI surface
  retrieved at that observation time) and therefore fits the observatory model.
- However, background retrieval lists can be large and may have limited
  strategic utility at the raw level compared to citation data.
- VEDA Strategy can derive "what was retrieved but not cited" from the union of
  retrieval and citation observations.

**Recommendation for this pass:** Do not add a full background retrieval
canonical family yet. Preserve `search_results` in the `rawPayload` JSONB on
`AiSurfaceRun`. Flag this as a governed decision: if background retrieval
comparison becomes a VEDA Strategy use case, the canonical family can be
promoted from `rawPayload` into a governed `AiRetrievalObservation` family at
that time. Do not create the family speculatively.

---

## 7. New required family: `AiMentionCluster`

The LLM Mentions API requires a distinct VEDA canonical family that was not in
the design pass. This is not a correction to existing families — it is an
addendum.

### What it is

A canonical record of a pre-aggregated mention cluster from the DataForSEO LLM
Mentions API — a keyword-on-platform question-answer pair with associated
citation sources, AI search volume, and time-window provenance.

### Why it is distinct from `AiSurfaceRun`

`AiSurfaceRun` anchors a specific provider API call at a specific capture time.
`AiMentionCluster` is an aggregated observation over a time window from
DataForSEO's continuous monitoring database. The provenance model is different.
The time model is different. Forcing LLM Mentions into `AiSurfaceRun` would
corrupt the capture-time semantics of `AiSurfaceRun`.

### Minimum canonical fields

- `id` (uuid)
- `projectId` (uuid, FK → Project)
- `provider` (text — `dataforseo`)
- `platform` (text — `google_aio`, `chat_gpt`, etc.)
- `query` (text — the keyword/query this cluster is for)
- `locale` (text)
- `language` (text)
- `question` (text? — the AI-generated question associated with this mention)
- `aiSearchVolume` (int? — provider-returned AI search volume estimate for this
  query; provenance is explicit via provider/capturedAt)
- `firstObservedAt` (timestamptz — provider's `first_response_at`)
- `lastObservedAt` (timestamptz — provider's `last_response_at`)
- `capturedAt` (timestamptz — when VEDA pulled this record from DataForSEO)
- `rawPayload` (jsonb — full item payload; `answer`, `sources`, `search_results`,
  `monthly_searches`, `fan_out_queries`, `brand_entities` preserved here)
- `sourcesCount` (int? — count of cited sources in this cluster)
- `fanOutQueryCount` (int? — count of fan-out queries in this cluster)
- `observatoryScopeId` (uuid?)
- `createdAt` (timestamptz)

**Uniqueness:** `(projectId, provider, platform, query, locale, lastObservedAt)`
— one cluster record per query/platform/locale/observation-window end per
project. Because DataForSEO continuously updates its database, re-pulling the
same query at a later time may return an updated cluster. The `lastObservedAt`
field is the natural discriminator for versioning.

**Child observations:** `AiMentionCluster` may spawn child citation
observations (from its `sources[]`) and fan-out query observations (from its
`fan_out_queries[]`), using the same `AiCitationObservation` and
`AiFanOutQueryObservation` families defined in the design pass, with the
`aiSurfaceRunId` FK replaced or supplemented by an `aiMentionClusterId` FK.
This requires a schema adjustment: either the child families carry both FK fields
(nullable), or a parent discriminator approach is used. This is a detail for the
schema-reference update, not for this note to resolve.

**Posture:** Append-friendly. New pulls produce new records. History is preserved.

---

## 8. Platform coverage — open question 12.4 status

The design pass flagged that only ChatGPT LLM Responses had been sampled and
that other platforms might return structurally different shapes.

**What verification confirms:**

| Platform | LLM Responses | LLM Scraper | LLM Mentions |
|---|---|---|---|
| ChatGPT (OpenAI) | Yes (Standard + Live) | Yes | Yes |
| Gemini (Google) | Yes (Standard + Live) | Yes | Implied (AIO confirmed) |
| Claude (Anthropic) | Yes (Standard + Live) | No | No |
| Perplexity | Yes (Live only) | No | No |
| Google AI Overview | Via SERP API (separate product) | No | Yes |

**Structural differences across platforms confirmed:**
- LLM Responses response shape is consistent across platforms at the top level
  (`items`, `annotations`, `fan_out_queries`). Platform differences are in model
  behavior, not top-level schema shape.
- LLM Scraper is only ChatGPT and Gemini. Not available for Claude or Perplexity.
- `brand_entities` in LLM Scraper is currently ChatGPT-only per December 2025
  docs.
- `fan_out_queries` in LLM Responses was extended to all four platforms (ChatGPT,
  Gemini, Claude, Perplexity) per December 2025 update. This means the design
  pass assumption that fan-out queries were ChatGPT-only is now outdated.

**Resolution for open question 12.4:**
The top-level `AiSurfaceRun` schema is structurally sound across LLM Responses
platforms — the `platform` field + `rawPayload` JSONB handles platform
differences correctly. No structural correction needed to the five AI-surface
families for the LLM Responses surface.

For LLM Scraper, the richer `sources` structure (adds `snippetText` and
`publicationDate`) requires a field-level addition to `AiCitationObservation`
(see corrections note, Section relating to citation fields). This is a
field-level addition, not a family-level restructuring.

Open question 12.4 is substantially resolved. The remaining unknown is Gemini
LLM Scraper brand entity behavior (ChatGPT-confirmed, Gemini-unclear) — minor
and can be deferred.

---

## 9. Summary of design pass addenda required

The following are addenda to the design pass, not corrections to what was
already there:

| Item | Action required |
|---|---|
| `AiMentionCluster` family | Add as a new AI-surface family in the design pass and in `schema-reference.md` |
| `AiCitationObservation` — add `snippetText` and `publicationDate` fields | Field-level addition to accommodate LLM Scraper `sources[]` richer shape |
| Background retrieval (`search_results`) | Do not canonicalize yet; preserve in `rawPayload`; flag for future governance |
| `AiFanOutQueryObservation` — available for all four LLM Responses platforms | No schema change needed; the family is already designed correctly |
| `AiEntityObservation` — confirmed by LLM Scraper `brand_entities` | No schema change needed; validates the design |
| AI Keyword Data API | Out of scope for Batch H; flag for future governance |
| `AiMentionCluster` → child FK approach | Detail for schema-reference update; not resolved in this note |

---

## 10. What the design pass got right (confirmed by DataForSEO docs)

- Five distinct AI-surface families (run anchor + four child types) — confirmed
  as the right structural approach for LLM Responses and LLM Scraper
- `provider` and `platform` as explicit columns on all families — confirmed
  essential; platform behavior differs materially and platform names differ
  across sub-products
- `rawPayload` JSONB on run anchor as evidence archive — confirmed correct;
  response bodies contain many fields that should not be promoted prematurely
- Provider-computed aggregate metrics (counts) on run anchor, not child rows —
  confirmed correct
- `AiEntityObservation` as a distinct family — confirmed by `brand_entities`
  array structure in LLM Scraper
- No bucket archive needed for AI-surface data in first pass — confirmed; JSONB
  is appropriate for current response sizes

---

## 11. Related files

- `transition-steward/batch-h-veda-family-design-pass.md`
- `transition-steward/batch-h-veda-family-design-pass-corrections.md`
- `veda/providers/dataforseo-ai-optimization.md`
- `veda/schema-reference.md`

Official sources verified:
- `https://docs.dataforseo.com/v3/ai_optimization-overview/`
- `https://docs.dataforseo.com/v3/ai_optimization-llm_mentions-overview/`
- `https://docs.dataforseo.com/v3/ai_optimization-llm_mentions-search-live/`
- `https://docs.dataforseo.com/v3/ai_optimization-chat_gpt-llm_responses-overview/`
- `https://docs.dataforseo.com/v3/ai_optimization-perplexity-llm_responses-live/`
- `https://dataforseo.com/help-center/what-is-llm-scraper-api-and-what-data-does-it-provide`
- `https://dataforseo.com/help-center/how-to-track-llm-responses-with-dataforseo-apis`
- `https://dataforseo.com/update/fan-out-queries-and-brand-entities`
- `https://dataforseo.com/help-center/how-to-access-search-queries-data-from-chatgpt`
