# Batch H — VEDA Family Design Pass

## 1. Purpose

This note closes the remaining Batch H family-design seam.

Batch H partial work has already landed. What remains deferred in `veda/schema-reference.md` is the governed canonical family posture for:

- Firecrawl-related observatory families
- AI-surface observability families
- `observatory_scope`
- `topic_monitor`
- the explicit canonical-vs-archive boundary for these domains

This pass produces a concrete family-structure recommendation for each, with enough specificity to drive later governed updates to VEDA authority docs. It does not pretend to be final authority.

---

## 2. Status

This is a transition-support design pass only.

It is not yet authority doctrine.
It is not a governed schema authority update.
It is intended to support governed updates to `veda/schema-reference.md`, `veda/data-boundaries.md`, and potentially a new VEDA observatory-model doc.

All conclusions here must be reviewed before being promoted into authority documents.

---

## 3. Settled Inputs

The following are treated as fixed and are not reopened in this pass:

- VEDA is observatory-only
- Firecrawl is an admitted VEDA observatory provider (`veda/providers/firecrawl.md`, `veda/providers/registry.md`)
- DataForSEO AI Optimization is an admitted VEDA observatory provider (`veda/providers/dataforseo-ai-optimization.md`, `veda/providers/registry.md`)
- Pre-project observability is required — observation must not require an existing Project V project record
- Raw AI-surface observability belongs in VEDA; derived interpretation belongs in VEDA Strategy
- Bucket/blob backing storage is allowed for large evidence-heavy captures, but canonical VEDA rows must preserve provenance, stable references, and promoted hot-path fields
- `/crawl` and `/map` surface shapes are sufficiently confirmed via doc-confirmed inventory in `transition-steward/firecrawl/firecrawl-crawl-map-surface-inventory.md`
- The `/scrape` per-page family shape (`markdown`, `rawHtml`, `metadata`, `links`) is baselined in `transition-steward/firecrawl/firecrawl-api-scrape-google-seo-starter-guide-baseline-inventory.md`
- The 24-hour result expiration, non-determinism across runs, and separate errors endpoint are operational realities documented in the crawl/map inventory; these must inform schema design
- The existing `SourceItem` family exists in `veda/schema-reference.md` but does not currently govern Firecrawl crawled page observations
- The existing `KeywordTarget` family exists but is a target-definition record, not a monitoring organization record
- The existing thin `Project` partition exists but must not be conflated with `observatory_scope`

---

## 4. Firecrawl Observatory Family Posture

### Recommendation summary

Four distinct canonical families are recommended for the Firecrawl domain:

1. `CrawlJob` — crawl job observation
2. `CrawledPage` — per-page crawl observation
3. `CrawlFailureRecord` — crawl failure observation
4. `DiscoveryObservation` — URL discovery observation (`/map` surface)

Structured data extracted from crawled pages (schema.org, OpenGraph, declared metadata) does **not** warrant a separate family in the first pass. It is a promoted-field concern within `CrawledPage`, with raw payload archived to bucket.

---

### 4.1. `CrawlJob` — crawl job observation

**What it is:** A record that a specific multi-page crawl was initiated against a target domain or URL, with its lifecycle state, configuration context, and result provenance.

**Why it is a distinct family:** The 24-hour expiration, non-determinism, and errors endpoint documented in the operational inventory make the crawl job a real observatory entity with its own identity, lifecycle, and provenance. It is not just a field on a page record. Multiple `CrawledPage` records belong to one job. Failure at the job level is distinct from failure at the page level.

**Relation to `SourceItem`:** `CrawlJob` is not a `SourceItem` and must not be folded into it. `SourceItem` is the existing intake record for captured individual items (webpages, RSS items, video references). A crawl job is a governed multi-page crawl operation with async delivery, expiration, and error-endpoint semantics that have no analog in the `SourceItem` model.

**Minimum canonical fields:**
- `id` (uuid)
- `projectId` (uuid, FK → Project)
- `provider` (text — `firecrawl` for now; allows future additional crawl providers)
- `jobRef` (text — the provider-issued job ID; e.g. Firecrawl's `id` field)
- `targetUrl` (text — the starting URL for the crawl)
- `targetHost` (text — normalized host of the target, for indexing/grouping)
- `observatoryScopeId` (uuid? — FK → ObservatoryScope if pre-project; nullable if project-linked)
- `submittedAt` (timestamptz)
- `completedAt` (timestamptz?)
- `expiresAt` (timestamptz — Firecrawl 24h window; must be preserved)
- `status` (enum: `submitted`, `scraping`, `completed`, `failed`, `expired`)
- `pageCompleted` (int? — total pages completed per provider status poll)
- `pageAttempted` (int? — total pages attempted per provider status poll)
- `creditsUsed` (int?)
- `bucketRef` (text? — reference to bucket capture set root path)
- `capturedAt` (timestamptz — when VEDA recorded the job result)
- `errorsFetched` (boolean — whether the errors endpoint was called)
- `crawlConfig` (jsonb? — bounded job configuration context: maxDepth, maxConcurrency, etc.)
- `createdAt` (timestamptz)

**Uniqueness:** `(projectId, provider, jobRef)` — one canonical record per provider job ID per project.

**Posture:** Mutable within bounds. Status progresses from `submitted` → `scraping` → `completed` or `failed`. `expired` is a terminal state set when the 24h window closes without bucket capture. State changes emit EventLog entries.

**Why recommended over alternatives:** Folding crawl job metadata into `CrawledPage` would duplicate it N times per job and make job-level querying awkward. Folding it into `SourceItem` would force `SourceItem` to model async job semantics it was not designed for. A distinct `CrawlJob` family is the clean choice.

---

### 4.2. `CrawledPage` — per-page crawl observation

**What it is:** A canonical record of what a specific external URL presented when crawled at a specific capture time, including promoted page metadata, structural observations, and a reference to the bucket-archived evidence.

**Why it is a distinct family:** The per-page observation is the core observatory record for external webpage content. It is time-stamped, URL-bound, and append-friendly. Its provenance ties to a `CrawlJob`. It has its own promoted fields (page metadata, status code) that differ structurally from `SERPSnapshot` and `SourceItem`. Folding it into `SourceItem` is possible but loses the crawl-job relation and the specific field/provenance model for crawled pages.

**Relation to `SourceItem`:** `CrawledPage` is not `SourceItem`. The recommendation is a distinct family with a defined relationship. If a `CrawledPage` record is later used as a `SourceItem`-equivalent for intake into other VEDA flows, a governed link or a governed intake record may be created — but the `CrawledPage` canonical record is its own family. Do not force crawled page observations into `SourceItem` to avoid adding a table.

**Minimum canonical fields:**
- `id` (uuid)
- `projectId` (uuid, FK → Project)
- `crawlJobId` (uuid, FK → CrawlJob)
- `provider` (text)
- `pageUrl` (text — the observed page URL)
- `normalizedUrl` (text? — deduplicated/normalized URL form for uniqueness logic)
- `capturedAt` (timestamptz — when this page was scraped)
- `statusCode` (int? — HTTP status code as returned by provider)
- `contentType` (text? — content type from provider metadata)
- `pageTitle` (text? — title tag value as observed; promoted from metadata)
- `pageDescription` (text? — meta description as observed; promoted from metadata)
- `pageLanguage` (text? — language as observed)
- `canonicalUrl` (text? — canonical URL as declared on page)
- `ogTitle` (text? — OG title if present)
- `ogDescription` (text? — OG description if present)
- `linkCount` (int? — count of observed link emissions)
- `bucketRef` (text? — reference to bucket capture set for this page)
- `markdownArchived` (boolean — whether markdown is in bucket)
- `rawHtmlArchived` (boolean — whether raw HTML is in bucket)
- `linksArchived` (boolean — whether link dump is in bucket)
- `structuredDataPresent` (boolean? — whether schema.org/OG structured data was observed)
- `providerRunMetadata` (jsonb? — bounded provider/runtime fields: `proxyUsed`, `cacheState`, `cachedAt`, `creditsUsed` — distinct from page-observed fields)
- `createdAt` (timestamptz)

**Uniqueness:** `(projectId, crawlJobId, pageUrl)` — one page record per URL per crawl job per project. Re-crawls produce new `CrawlJob` records and new `CrawledPage` records, not updates to prior records.

**Posture:** Append-only. A new crawl of the same URL is a new record under a new job. Prior records are history. Supersedence and re-crawl comparison are analytical concerns, not schema mutations.

**Structured data (schema.org, OG, declared metadata):** Does not warrant a separate family in the first pass. Promoted key fields (`pageTitle`, `pageDescription`, `canonicalUrl`, `ogTitle`, `ogDescription`, `structuredDataPresent`) live as explicit columns. The raw structured data extraction, if needed, is archived to bucket in the raw response and may be re-parsed later. A governed `CrawledPageStructuredData` family may be warranted later if structured data observation becomes a primary querying surface — but that decision requires more implementation evidence before governing it as a separate family.

---

### 4.3. `CrawlFailureRecord` — crawl failure observation

**What it is:** A canonical record of a page-level crawl failure — a page that Firecrawl attempted to scrape but failed (network error, timeout, robots.txt block, etc.) as returned by the Firecrawl errors endpoint.

**Why it is a distinct family:** The `data` array in a completed Firecrawl job contains only successfully scraped pages. Failures are only available via the separate errors endpoint (`GET /v2/crawl/{id}/errors`). A completed crawl with a non-empty `data` array is not evidence of complete coverage — it is evidence of what was successfully scraped. Failure records are a real observatory observation, not just a missing row in `CrawledPage`. They require their own canonical family so that "absent from `CrawledPage`" does not silently mean "successfully not-found" versus "failed to scrape."

**Minimum canonical fields:**
- `id` (uuid)
- `projectId` (uuid, FK → Project)
- `crawlJobId` (uuid, FK → CrawlJob)
- `provider` (text)
- `pageUrl` (text — the URL that failed)
- `errorType` (text — provider-supplied error classification)
- `errorDetail` (text? — provider-supplied error detail)
- `capturedAt` (timestamptz — when this failure record was recorded)
- `createdAt` (timestamptz)

**Uniqueness:** `(projectId, crawlJobId, pageUrl)` — one failure record per URL per job per project.

**Posture:** Append-only. Failure records are not mutable after creation. If a later re-crawl succeeds for the same URL, a new `CrawledPage` record is created under the new job — the old failure record remains.

**Why not fold into `CrawledPage`:** Folding failures into `CrawledPage` with a status field would blur the distinction between "successfully scraped page observation" and "failure to observe." The observation pattern (`entity + observation + time`) applies differently here — the observation is the failure event itself, not a page content observation. Keep them as distinct families.

---

### 4.4. `DiscoveryObservation` — URL discovery observation

**What it is:** A canonical record of a URL discovery event produced by the Firecrawl `/map` surface — a set of URLs observed to exist at a domain at a point in time, along with their SERP-cached or sitemap-derived metadata.

**Why it is a distinct family:** `/map` is not a page-content capture. It is a fast, pre-flight URL inventory surface. Its output is SERP-cached or sitemap-derived — not live crawl observations. It does not belong in `CrawledPage` (no page content captured) and it does not belong in `CrawlJob` (not a crawl job). The `firecrawl.md` provider doc already names "Discovery observations" as an admitted observatory family. This is the canonical implementation of that family.

**Minimum canonical fields:**
- `id` (uuid)
- `projectId` (uuid, FK → Project)
- `provider` (text)
- `targetUrl` (text — the root URL submitted to `/map`)
- `targetHost` (text — normalized host)
- `capturedAt` (timestamptz)
- `urlCount` (int — number of URLs returned)
- `searchParam` (text? — if a search filter was applied to the map call)
- `bucketRef` (text? — reference to bucket archive of raw link list)
- `isComprehensive` (boolean — always false for `/map`; carry this field as an explicit reminder that map results may miss links)
- `createdAt` (timestamptz)

**Individual URL records:** Individual discovered URLs from a `/map` call do not need their own canonical rows in the first pass. The URL list is archived to bucket. The `DiscoveryObservation` record is the canonical anchor for the discovery event. If URL-level querying becomes necessary later, a `DiscoveryUrl` child family may be governed then. For now, the aggregate observation record is sufficient.

**Uniqueness:** `(projectId, provider, targetHost, capturedAt)` — one discovery observation per host per capture moment per project.

**Posture:** Append-only. Re-mapping the same domain produces a new record.

---

### 4.5. What stays in `SourceItem`

`SourceItem` remains the canonical intake family for individually captured external items — webpages captured manually or through operator-directed capture, RSS items, video references, and similar source artifacts. Firecrawl-sourced `CrawledPage` records are a distinct family. There is no requirement to route crawled pages through `SourceItem`. If a `CrawledPage` observation is later used as an input into a broader intake or triage flow, that routing decision can be governed then. For now, keep the families separate.

---

## 5. AI-Surface Observability Family Posture

### Recommendation summary

Five distinct canonical families are recommended for the AI-surface observability domain:

1. `AiSurfaceRun` — a specific AI-surface observation run (the governing anchor)
2. `AiMentionObservation` — mention observations
3. `AiCitationObservation` — citation observations
4. `AiFanOutQueryObservation` — fan-out query observations
5. `AiEntityObservation` — brand/entity observations

AI-surface response/context metadata is handled as fields on `AiSurfaceRun`, not as a separate family.

---

### 5.1. Why a run-anchor family is needed

DataForSEO's AI Optimization product returns observations that are scoped to a specific query, platform, locale, language, and time. Multiple observation types (mentions, citations, fan-out queries, entities) may result from a single provider call. Without a run-anchor record, these child observations float without a coherent provenance anchor.

This mirrors the `CrawlJob` → `CrawledPage` relationship. An observation run is to AI-surface observations what a crawl job is to crawled page observations.

Provider-returned aggregate metrics also belong on the run record, not promoted to child observations.

---

### 5.2. `AiSurfaceRun` — AI-surface observation run

**What it is:** A canonical record anchoring a specific DataForSEO AI Optimization provider call — the platform, query, locale, language, and time context for a set of AI-surface observations.

**Minimum canonical fields:**
- `id` (uuid)
- `projectId` (uuid, FK → Project)
- `provider` (text — `dataforseo` for now)
- `platform` (text — e.g. `chatgpt`, `perplexity`, `gemini`, `google_ai_overview`, `bing_copilot`)
- `query` (text — the query submitted to the provider)
- `locale` (text)
- `language` (text?)
- `device` (text?)
- `capturedAt` (timestamptz)
- `rawPayload` (jsonb — full provider response; evidence archive)
- `payloadSchemaVersion` (text?)
- `providerTaskId` (text? — provider-issued task/result ID)
- `mentionCount` (int? — provider-returned count, if available)
- `citationCount` (int? — provider-returned count, if available)
- `fanOutQueryCount` (int? — provider-returned count, if available)
- `entityCount` (int? — provider-returned count, if available)
- `observatoryScopeId` (uuid? — FK → ObservatoryScope if applicable)
- `createdAt` (timestamptz)

**Uniqueness:** `(projectId, provider, platform, query, locale, capturedAt)` — one run record per query/platform/locale/capture moment per project.

**Posture:** Append-only. A new provider pull for the same query at a later time produces a new run record.

**Provider-computed metrics note:** Count fields (`mentionCount`, `citationCount`, etc.) are promotions of what the provider returned. They are observable attributes of what the provider reported, not VEDA-derived or VEDA-validated metrics. Their provenance is explicit via `provider` and `capturedAt`.

---

### 5.3. `AiMentionObservation` — mention observations

**What it is:** A canonical record of a specific mention — when a keyword, brand, product, domain, or page was mentioned in an AI-surface response during the observation run.

**Minimum canonical fields:**
- `id` (uuid)
- `projectId` (uuid)
- `aiSurfaceRunId` (uuid, FK → AiSurfaceRun)
- `provider` (text)
- `platform` (text)
- `mentionedEntity` (text — what was mentioned: keyword, brand, domain, page)
- `mentionType` (text — e.g. `brand`, `domain`, `page`, `keyword`, `product`)
- `mentionContext` (text? — surrounding context text if returned by provider)
- `position` (int? — ordinal position in response if available)
- `capturedAt` (timestamptz — from parent run)
- `createdAt` (timestamptz)

**Uniqueness:** `(projectId, aiSurfaceRunId, mentionedEntity, mentionType)` — one mention record per entity per type per run per project.

**Posture:** Append-only.

---

### 5.4. `AiCitationObservation` — citation observations

**What it is:** A canonical record of a specific citation — when a source domain or page was cited, linked, quoted, or referenced by an AI surface during the observation run.

**Why distinct from mentions:** Citations are source-attribution events (a specific domain/page was cited as a source). Mentions are entity-appearance events (a brand or keyword appeared in output text). These are structurally different observations with different downstream use in VEDA Strategy. Combining them into one family would require awkward discriminators and make querying fragile.

**Minimum canonical fields:**
- `id` (uuid)
- `projectId` (uuid)
- `aiSurfaceRunId` (uuid, FK → AiSurfaceRun)
- `provider` (text)
- `platform` (text)
- `citedUrl` (text — the specific cited URL if available)
- `citedDomain` (text — the domain of the cited source)
- `citationType` (text? — e.g. `inline_link`, `source_card`, `footnote`; preserve if provider returns it)
- `citationPosition` (int? — ordinal position if available)
- `capturedAt` (timestamptz — from parent run)
- `createdAt` (timestamptz)

**Uniqueness:** `(projectId, aiSurfaceRunId, citedUrl)` — one citation per URL per run per project. If only a domain is available (no specific URL), use `(projectId, aiSurfaceRunId, citedDomain)` with a null `citedUrl`.

**Posture:** Append-only.

---

### 5.5. `AiFanOutQueryObservation` — fan-out query observations

**What it is:** A canonical record of a related query generated or explored by the AI surface as part of its response construction — the follow-on query signals observed in AI-surface behavior.

**Why distinct:** Fan-out queries are a structurally distinct observation type. They are not about what entities were mentioned or cited — they are about what related queries the AI surface generated. VEDA Strategy's use of these observations (identifying query expansion patterns, topic clustering signals) depends on them being clearly distinct from mention or citation records.

**Minimum canonical fields:**
- `id` (uuid)
- `projectId` (uuid)
- `aiSurfaceRunId` (uuid, FK → AiSurfaceRun)
- `provider` (text)
- `platform` (text)
- `fanOutQuery` (text — the related query observed)
- `queryPosition` (int? — ordinal position if available)
- `capturedAt` (timestamptz — from parent run)
- `createdAt` (timestamptz)

**Uniqueness:** `(projectId, aiSurfaceRunId, fanOutQuery)` — one fan-out query record per query string per run per project.

**Posture:** Append-only.

---

### 5.6. `AiEntityObservation` — brand/entity observations

**What it is:** A canonical record of a structured brand or entity appearance surfaced by the provider — distinct from a free-text mention, representing a structured entity recognition result.

**Why distinct from mentions:** Provider-returned entity observations are structured entity recognition outputs (brand, organization, product, person) that may carry additional structured attributes (entity type, confidence, knowledge graph ID). These are structurally more specific than a free-text mention and should not be conflated with the more general `AiMentionObservation`.

**Minimum canonical fields:**
- `id` (uuid)
- `projectId` (uuid)
- `aiSurfaceRunId` (uuid, FK → AiSurfaceRun)
- `provider` (text)
- `platform` (text)
- `entityName` (text)
- `entityType` (text? — `brand`, `organization`, `product`, `person`, etc.)
- `entityUrl` (text? — entity URL or knowledge graph reference if returned)
- `capturedAt` (timestamptz — from parent run)
- `createdAt` (timestamptz)

**Uniqueness:** `(projectId, aiSurfaceRunId, entityName, entityType)` — one entity record per name/type per run per project.

**Posture:** Append-only.

---

### 5.7. What must remain provider-provenance-visible

All five AI-surface families must carry `provider` and `platform` as explicit columns. Platform behavior differs materially across ChatGPT, Perplexity, Gemini, Google AI Overview, and Bing Copilot — those differences must be preserved as structure, not collapsed into a generic observation field. Different providers may also define mention, citation, and entity observations differently; the `provider` field ensures that provenance is explicit and that VEDA Strategy can account for provider-level behavioral differences when deriving intelligence.

---

### 5.8. What does not get a separate family in this pass

- AI-surface response/context metadata: handled as fields on `AiSurfaceRun`, not a separate family.
- Google AI Overview citation/source observations: subsumed under `AiCitationObservation` with `platform = 'google_ai_overview'`. The distinction between Google AI Overview and other platforms is preserved via the `platform` field. A separate family is not warranted at this stage.
- Provider-computed aggregate metrics: promoted to count fields on `AiSurfaceRun`. They are observable attributes of what the provider returned, preserved with explicit provider/capture provenance.

---

## 6. `observatory_scope` Posture

### What it is

`ObservatoryScope` is a governing scoping container for observatory observation work that exists independently of a Project V planning project — or that precedes one. It represents a defined area of interest that VEDA is watching, with its own lifecycle, whether or not a planning project has yet been committed.

### Why it is not just the existing thin `Project` partition

VEDA's existing `Project` record is a thin observatory partitioning container whose primary job is multi-project record isolation. It does not model the *intent* or *shape* of what is being watched. It answers "which project does this record belong to?" not "what is this observation effort focused on?"

`ObservatoryScope` answers the second question. It models an intentional watching focus — a domain, a topic cluster, a competitor, a keyword space, a content surface — that may:

- exist before a Project V planning project is created
- exist without ever generating a Project V planning project
- span multiple topic monitors or keyword targets
- be linked to a planning project after one is created

This is the "pre-project observability is required" requirement made concrete in schema.

### Whether it is pre-project, project-linked, or both

`ObservatoryScope` must support all three states:
- **pre-project:** created and active without a linked Project V planning project
- **project-linked:** associated with an existing Project V planning project by reference (external ID/locator, not FK)
- **both over time:** starts pre-project, gains a project link when a planning project is committed

The schema must not force a project link at creation time.

### What it scopes

`ObservatoryScope` scopes:
- crawl jobs
- AI-surface observation runs
- potentially topic monitors
- potentially other future observatory operations that need a pre-project scoping anchor

It does **not** replace the existing `Project` partition record. Every `ObservatoryScope` record still belongs to a VEDA `Project` — the `ObservatoryScope` is nested under the `Project` partition, not a replacement for it.

### Minimum canonical fields

- `id` (uuid)
- `projectId` (uuid, FK → Project — the VEDA project partition this scope belongs to)
- `name` (text — human-readable scope name)
- `slug` (text — stable machine key)
- `scopeType` (enum — `domain`, `topic_cluster`, `competitor`, `keyword_space`, `custom`)
- `targetDomain` (text? — primary target domain if applicable)
- `description` (text?)
- `planningProjectRef` (text? — external locator/slug to the Project V planning project, if linked; null if pre-project)
- `lifecycleState` (enum — `active`, `paused`, `archived`)
- `createdAt` (timestamptz)
- `updatedAt` (timestamptz)

### What it must not become

`ObservatoryScope` must not become:
- a rich planning orchestration record (that is Project V's domain)
- a shadow of Project V's planning project state
- a place where scoring, prioritization, or gap detection results are stored (that is VEDA Strategy's domain)
- a general-purpose tagging or grouping mechanism unrelated to observation work
- a second canonical project partition that competes with the existing thin `Project` record

---

## 7. `topic_monitor` Posture

### What it is

`TopicMonitor` is a governing monitoring definition record for a topic or query cluster that VEDA tracks over time. It organizes one or more `KeywordTarget` records — and potentially other observation targets — under a named, intentional monitoring commitment.

### How it relates to `KeywordTarget`

`KeywordTarget` is a governed decision to observe a specific query within a locale and device scope. It answers: "watch this exact query, in this locale, on this device." It is a fine-grained observation target, not a monitoring strategy record.

`TopicMonitor` answers: "we are tracking this topic area over time, and here are the keyword targets and other signals that represent it." It is the organizing layer above `KeywordTarget` records.

The relationship is:
- one `TopicMonitor` → many `KeywordTarget` records (association, not FK dependency)
- `KeywordTarget` records may exist without a `TopicMonitor` (they are valid standalone observation targets)
- `TopicMonitor` provides grouping, intent, lifecycle, and scoping without taking over ownership of `KeywordTarget` identity

### Why it is needed beyond `KeywordTarget`

- Pre-project observability requires a layer that can track a topic area before specific keyword targets are defined
- AI-surface observation runs may be topically organized without mapping 1:1 to individual keyword targets
- Signal routing to VEDA Strategy benefits from topic-level anchoring, not just individual keyword-level anchoring
- Operator intent for a monitoring effort is expressed at the topic level, not at the individual keyword level

### What it organizes

`TopicMonitor` organizes:
- associated `KeywordTarget` records (via a junction table or association)
- potentially associated `AiSurfaceRun` records by topic context
- potentially associated `ObservatoryScope` (a topic monitor lives under a scope)

### Minimum canonical fields

- `id` (uuid)
- `projectId` (uuid, FK → Project)
- `observatoryScopeId` (uuid? — FK → ObservatoryScope; optional if topic monitors can stand alone)
- `name` (text)
- `slug` (text)
- `intent` (text? — operator-stated purpose for this monitoring effort)
- `topicDescription` (text?)
- `lifecycleState` (enum — `active`, `paused`, `archived`)
- `createdAt` (timestamptz)
- `updatedAt` (timestamptz)

### What it must not become

`TopicMonitor` must not become:
- a scoring or prioritization record (that is VEDA Strategy)
- a content brief or planning document (that is Project V)
- a substitute for `KeywordTarget` identity — it organizes, it does not replace
- a vehicle for implementation to avoid governing `KeywordTarget` properly
- a general-purpose tagging system

---

## 8. Canonical vs Archive/Blob Boundary

This section defines the boundary for the Firecrawl and AI-surface domains.

### 8.1. Firecrawl canonical vs archive boundary

**Belongs in canonical VEDA rows:**
- The fact that a crawl job occurred, its lifecycle state, and its provenance (`CrawlJob`)
- Per-page observations: URL, capture time, promoted metadata fields (`CrawledPage`)
- The fact that a page failed to crawl (`CrawlFailureRecord`)
- The fact that a discovery/map operation occurred and its result count (`DiscoveryObservation`)
- Stable references to bucket artifacts (bucket path / `bucketRef`)
- `expiresAt` on `CrawlJob` — this is canonical because the 24h window is operationally critical; once expired with no bucket capture, the raw artifact is permanently unavailable
- `errorsFetched` on `CrawlJob` — canonical flag so that absence of failure records does not silently mean "no failures" vs "errors endpoint not called"

**Belongs in bucket/archive:**
- Full raw API response payload (`raw-response.json`)
- Full raw HTML capture (`raw-html.html`)
- Normalized markdown capture (`markdown.md`)
- Observed link dump (`links.json`)
- Full discovery URL list from `/map` (the list of URLs; only the aggregate observation record is canonical)
- Failure detail artifact (`failure.json`) when needed

**Must not live only in bucket:**
- Job identity, lifecycle state, expiration, and provenance
- Page-level observation facts needed for querying (URL, status code, title, capture time)
- Failure records (their existence is canonical observatory truth)
- Bucket artifact references

**Must not be promoted prematurely:**
- Markdown as clean page content truth — it is noisy; do not treat it as canonical page body until normalization rules are governed
- Link structure as a semantic relationship graph — it is observed link emissions; normalization into internal/external/nav/content distinctions must be a governed later step
- Provider/runtime fields (`proxyUsed`, `cacheState`, `creditsUsed`) — archive in raw payload; do not promote as page truth

### 8.2. AI-surface canonical vs archive boundary

**Belongs in canonical VEDA rows:**
- The observation run record with platform, query, locale, and capture time (`AiSurfaceRun`)
- Individual mention, citation, fan-out query, and entity observations (child family records)
- Provider-returned aggregate counts promoted to `AiSurfaceRun` fields
- `provider` and `platform` as explicit columns on all records — must not be buried in JSON

**Belongs in `rawPayload` JSONB on `AiSurfaceRun` (hot-observation archive, not bucket):**
- Full provider response body — this is smaller and more structured than crawl artifacts; JSONB on the row is appropriate
- Provider-specific response wrapper fields
- Fields not yet promoted

**AI-surface observations do not require a separate bucket archive in the first pass.** The full provider response is small enough for JSONB on `AiSurfaceRun`. The child family records capture the semantically meaningful observations. Bucket storage for AI-surface data may be governed later if response sizes or retention requirements warrant it.

**Must not be promoted prematurely:**
- Provider-computed aggregate metrics as VEDA-validated metrics — they are what the provider returned, not independently validated by VEDA
- Platform behavioral patterns as strategic conclusions — those belong in VEDA Strategy

---

## 9. Identity, Uniqueness, and Mutation Posture

### 9.1. Firecrawl families

| Family | Identity basis | Uniqueness | Posture | Re-run/supersedence |
|---|---|---|---|---|
| `CrawlJob` | `(projectId, provider, jobRef)` | Natural unique key | Mutable — status progresses | New job = new record; no overwrites |
| `CrawledPage` | `(projectId, crawlJobId, pageUrl)` | Natural unique key | Append-only | New crawl = new job = new records |
| `CrawlFailureRecord` | `(projectId, crawlJobId, pageUrl)` | Natural unique key | Append-only | Failure records persist; new crawl success = new `CrawledPage` under new job |
| `DiscoveryObservation` | `(projectId, provider, targetHost, capturedAt)` | Natural unique key | Append-only | New map call = new record |

**Re-crawl posture:** A re-crawl of the same target is a new `CrawlJob` with new `CrawledPage` records. The old records are history. There is no supersedence mutation. Comparison across crawl runs is analytical work, not a schema mutation pattern.

**Non-determinism posture:** Because Firecrawl `/crawl` is explicitly non-deterministic across runs, each `CrawlJob` record must carry its configuration context (`crawlConfig` JSONB) so that analysis of cross-run differences accounts for configuration context. Do not assume two jobs with the same `targetUrl` produced comparable results without examining their configuration and completion state.

### 9.2. AI-surface families

| Family | Identity basis | Uniqueness | Posture | Re-run/supersedence |
|---|---|---|---|---|
| `AiSurfaceRun` | `(projectId, provider, platform, query, locale, capturedAt)` | Natural unique key | Append-only | New pull = new run record |
| `AiMentionObservation` | `(projectId, aiSurfaceRunId, mentionedEntity, mentionType)` | Natural unique key | Append-only | Belongs to parent run; not independently superseded |
| `AiCitationObservation` | `(projectId, aiSurfaceRunId, citedUrl)` | Natural unique key | Append-only | As above |
| `AiFanOutQueryObservation` | `(projectId, aiSurfaceRunId, fanOutQuery)` | Natural unique key | Append-only | As above |
| `AiEntityObservation` | `(projectId, aiSurfaceRunId, entityName, entityType)` | Natural unique key | Append-only | As above |

### 9.3. `ObservatoryScope` and `TopicMonitor`

Both are mutable governance records, not observation records. They may have their lifecycle state updated. State changes should emit `EventLog` entries. They are not append-only.

---

## 10. Implementation Anti-Drift Rules

The following are explicit prohibitions while these families are being promoted into authority docs.

**10.1.** Do not stuff Firecrawl crawled page data into `SourceItem`. `SourceItem` is the intake family for individually captured source artifacts. `CrawledPage` is a distinct family with different provenance, lifecycle, and crawl-job semantics. Forcing Firecrawl data into `SourceItem` avoids a governed table but destroys the observability model.

**10.2.** Do not stuff AI-surface observations into `SERPSnapshot`. `SERPSnapshot` is for SERP observations. AI-surface mentions, citations, fan-out queries, and entity observations are structurally distinct and require their own families. Using `SERPSnapshot` as a container for AI-surface data is a boundary violation.

**10.3.** Do not hide unresolved Firecrawl or AI-surface schema in JSON blobs on unrelated families. JSON blobs are evidence support, not a junk drawer for deferred schema design.

**10.4.** Do not treat Firecrawl markdown as already-clean canonical page content. It is noisy and includes navigation chrome and UI residue. Archive it; do not model it as clean page truth.

**10.5.** Do not treat `/map` title/description fields as authoritative page metadata. They are SERP-cached or sitemap-derived, not live crawl observations.

**10.6.** Do not treat provider-computed aggregate metrics (mention counts, citation counts, etc. from DataForSEO) as VEDA-validated canonical truth. They are observable attributes of what the provider returned. Their provenance is explicit; they are not independently validated by VEDA.

**10.7.** Do not conflate `ObservatoryScope` with VEDA's existing thin `Project` partition record. `ObservatoryScope` is a scoping container for observation intent. `Project` is a record isolation partition. They coexist; `ObservatoryScope` is nested under `Project`, not a replacement for it.

**10.8.** Do not conflate `TopicMonitor` with `KeywordTarget`. `TopicMonitor` organizes; `KeywordTarget` identifies. Do not turn `TopicMonitor` into a planning record or a scoring record.

**10.9.** Do not create `ObservatoryScope` or `TopicMonitor` as ad hoc tables or JSON shortcuts before their families are governed and promoted into `veda/schema-reference.md`.

**10.10.** Do not call the Firecrawl errors endpoint optional. Absence of `CrawlFailureRecord` entries for a completed job must mean the errors endpoint was called and no failures were found — not that the endpoint was never called. The `errorsFetched` flag on `CrawlJob` enforces this distinction.

**10.11.** Do not skip bucket capture because it seems optional. For `CrawlJob` records, the 24-hour expiration window means bucket capture is required before the window closes. If a completed job has no bucket reference and `expiresAt` has passed, the raw artifact is gone.

**10.12.** Do not let different platforms' AI-surface observations be flattened. `platform` must be an explicit column on all AI-surface families. ChatGPT, Perplexity, and Google AI Overview observations are different observations and must remain distinguishable.

---

## 11. Recommended Authority-Update Targets

The following authority docs should be updated based on this design pass, in order of dependency:

### Primary targets

**`veda/schema-reference.md`** — The "Deferred Owned Domains" section for crawled page observability, AI-surface observability, and `observatory_scope`/`topic_monitor` should be replaced with governed canonical family definitions based on this pass. This is the highest-priority update.

**`veda/data-boundaries.md`** — The canonical-vs-archive boundary rules for Firecrawl and AI-surface domains should be added as explicit data boundary entries.

### Secondary targets

**`veda/providers/firecrawl.md`** — The "Admitted observatory families" section currently names families at a high level. It should be updated to reference the governed canonical family names (`CrawlJob`, `CrawledPage`, `CrawlFailureRecord`, `DiscoveryObservation`) once they are promoted into schema authority.

**`veda/providers/dataforseo-ai-optimization.md`** — The "Admitted observatory families" section should be updated to reference the governed canonical family names (`AiSurfaceRun`, `AiMentionObservation`, `AiCitationObservation`, `AiFanOutQueryObservation`, `AiEntityObservation`) once promoted.

### Optional / conditional

**New `veda/observatory-family-index.md`** — If the number of governed VEDA families continues growing beyond the current eight, a lightweight family index doc may help orientation without bloating `schema-reference.md`. This is not urgently required — assess after the schema-reference update is complete.

Do not create a new authority doc purely because this design pass was thorough. The existing doc structure is sufficient for the updates required.

---

## 12. Open Questions

These remain unresolved after this pass and should be addressed before or during the authority-update step.

**12.1.** Exact `CrawledPage` deduplication posture across re-crawls: this pass recommends append-only with new job = new records. Whether VEDA should maintain a "current/latest" materialized view per URL for fast querying is unresolved. Needs operational input from the first actual crawl use case before governing.

**12.2.** `ObservatoryScope` ↔ `TopicMonitor` cardinality and dependency: this pass leaves `observatoryScopeId` optional on `TopicMonitor`. Whether a `TopicMonitor` may exist without an `ObservatoryScope` or whether the scope is always required needs a concrete use case to validate before governing as a constraint.

**12.3.** `KeywordTarget` → `TopicMonitor` association mechanism: the association mechanism (junction table vs FK on `KeywordTarget`) is not specified here. This is an implementation decision that needs to be governed before the `TopicMonitor` family is promoted to schema authority.

**12.4.** AI-surface platforms not yet sampled: this pass designs `AiSurfaceRun` to carry a `platform` field that accommodates multiple platforms. However, only ChatGPT LLM Responses has been sampled via DataForSEO. Other platforms (Perplexity, Gemini, Bing Copilot) may return structurally different response shapes. The `rawPayload` JSONB and the provider-provenance fields are designed to accommodate this, but platform-specific field promotion decisions are deferred until those surfaces are sampled.

**12.5.** `CrawlFailureRecord` error taxonomy: Firecrawl error classification from the errors endpoint is doc-confirmed but not live-sampled. A governed `errorType` enum vs free-text field decision is deferred pending an actual errors-endpoint sample.

---

## 13. Related Files

Authority docs read for this pass:

- `transition-steward/transition-plan.md`
- `veda/schema-reference.md`
- `veda/data-boundaries.md`
- `veda/providers/registry.md`
- `veda/providers/firecrawl.md`
- `veda/providers/dataforseo-ai-optimization.md`
- `veda/veda.md`
- `veda/system-invariants.md`
- `veda/observability-and-signal-role.md`
- `veda/evidence-and-source-provenance.md`
- `ecosystem/external-provider-integration-doctrine.md`

Transition-support material read for grounding:

- `transition-steward/firecrawl/README.md`
- `transition-steward/firecrawl/firecrawl-crawl-map-surface-inventory.md`
- `transition-steward/firecrawl/firecrawl-api-scrape-google-seo-starter-guide-baseline-inventory.md`
- `transition-steward/firecrawl/firecrawl-bucket-capture-posture.md`

Target authority update destinations:

- `veda/schema-reference.md` (primary)
- `veda/data-boundaries.md` (primary)
- `veda/providers/firecrawl.md` (secondary)
- `veda/providers/dataforseo-ai-optimization.md` (secondary)
