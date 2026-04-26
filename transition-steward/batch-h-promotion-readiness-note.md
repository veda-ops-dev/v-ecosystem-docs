# Batch H Promotion Readiness Note

## 1. Purpose

This note reviews the Batch H VEDA family design work
(`transition-steward/batch-h-veda-family-design-pass.md`) together with its
four supporting notes — corrections, DataForSEO surface inventory, confidence
layer addendum, and the Firecrawl grounding set — and determines what is ready
for authority promotion into `veda/schema-reference.md`, what is not, what is
blocked by credits, and what the bounded authority update looks like.

It does not rewrite the design pass. It is a promotion decision note.

---

## 2. What Is Promotable Now

### Firecrawl families — all four, with corrections applied

All four Firecrawl families are promotable to governed canonical families in
`veda/schema-reference.md`. Their evidence basis is sufficient:

- `/scrape` per-page shape is live-payload confirmed from the baseline sample
- `/crawl` per-page families are doc-confirmed identical to `/scrape`
- `/crawl` operational behavior (24h expiration, non-determinism, errors endpoint)
  is doc-confirmed and consistent with the inventory note
- `/map` response shape is doc-confirmed
- The corrections note has applied official-doc verification and identified the
  `robotsBlocked` / `errors[]` structural distinction and the `/map` field additions

The four promotable families are:

**`CrawlJob`** — promote as defined in the design pass, with no corrections
needed beyond confirming the field list is consistent with the corrections doc.

**`CrawledPage`** — promote as defined. The per-page shape is the most
evidence-grounded family in the design pass.

**`CrawlFailureRecord`** — promote with the corrections applied: `failureClass`
discriminator (`scrape_error` / `robots_blocked`), `providerRecordId` and
`errorDetail` nullable for `robots_blocked` sub-type. Open question 12.5 (free-
text vs. enum for error type) is closed by the corrections note: free-text is
correct, no provider enum exists. Uniqueness key: `(projectId, crawlJobId,
pageUrl, failureClass)`.

**`DiscoveryObservation`** — promote with the corrections applied: add `urlLimit`
(int?) and `cacheIgnored` (boolean) fields for provenance. The 5,000 URL ceiling
is operational context, not a schema field, but must be noted in the family
description.

**`ObservatoryScope`** — promotable as a governed canonical family. Its design
is not provider-dependent. The design pass Section 6 definition is coherent,
the `planningProjectRef` as external locator (not FK) is correct, and the
`scopeType` enum is reasonable. Open question 12.2 (whether `TopicMonitor`
requires `ObservatoryScope`) can be explicitly deferred — `observatoryScopeId`
stays nullable on `TopicMonitor`, and the decision is recorded as deferred.

**`TopicMonitor`** — promotable with open question 12.3 explicitly deferred.
The `KeywordTarget` → `TopicMonitor` association mechanism (junction table vs.
FK on `KeywordTarget`) does not need to be resolved to promote `TopicMonitor`
as a canonical family. The deferred decision is: `TopicMonitor` exists as a
governing monitor record; the exact association mechanism to `KeywordTarget` is
governed in a follow-on schema update when the first implementation use case
arrives. The family itself can be promoted now.

### AI-surface families — five of six, promotable with required confidence markers

The five AI-surface families originally defined in the design pass are
promotable, but only if the authority doc text carries an explicit evidence-
posture note inside each family definition. This is a hard requirement, not a
suggestion. The confidence distinction must survive the promotion in
`veda/schema-reference.md` itself — not just in this note or the design pass.
A future engineer or LLM reading `schema-reference.md` alone must be able to
see which parts are payload-confirmed and which are docs-confirmed.

If the authority update flattens these families into uniformly "fully settled
canonical structure" without preserving those distinctions, the promotion should
not proceed as written. See Section 6 for the required inline evidence-posture
note.

The confidence layer addendum (`batch-h-dataforseo-confidence-layer.md`) is
authoritative on the confidence classification for each family:

**`AiSurfaceRun`** — promotable. Payload-confirmed for ChatGPT LLM Responses
(one captured baseline in `dataforseo-json/`). Multi-platform posture
(`platform` field) is docs-confirmed. The authority text must state this
distinction explicitly in the family definition.

**`AiMentionObservation`** — promotable. Derives from the payload-confirmed
ChatGPT baseline.

**`AiCitationObservation`** — promotable with two field additions from the
surface inventory note (`snippetText` nullable, `publicationDate` nullable) to
accommodate LLM Scraper `sources[]` richer shape. These two fields must be
marked explicitly as docs-confirmed provisional in the authority text, pending
LLM Scraper payload capture.

**`AiFanOutQueryObservation`** — promotable. Extended to all four LLM Responses
platforms per December 2025 DataForSEO update, confirmed in the surface
inventory note. The design pass assumption that it was ChatGPT-only is outdated;
the platform extension requires no schema change — the `platform` field already
accommodates it.

**`AiEntityObservation`** — promotable. The `brand_entities` structure from LLM
Scraper (docs-confirmed) validates this family design. The authority text must
note that LLM Scraper details are docs-confirmed, not payload-confirmed.

---

## 3. What Is Not Promotable Yet

### `AiMentionCluster` — do not promote to governed family

The LLM Mentions API surface identified in `batch-h-dataforseo-surface-inventory.md`
requires a distinct `AiMentionCluster` family. This family is entirely
docs-confirmed with zero payload evidence. No LLM Mentions payload exists in
`dataforseo-json/`. The confidence layer addendum explicitly calls this the
most speculative element of the Batch H design work and recommends listing it
as deferred-but-owned, not a governed canonical family.

Promote `AiMentionCluster` as a deferred-but-owned domain in the "Deferred
Owned Domains" section of `veda/schema-reference.md`. Same treatment as the
original deferred families. Do not promote it to a governed canonical family
until at least one real LLM Mentions payload is captured and the
`aiMentionClusterId` FK approach for child observations is resolved.

### `AiRetrievalObservation` (background retrieval) — do not create

The `search_results` distinction (background retrieval vs. cited sources)
identified in the surface inventory note does not warrant a new canonical family
in this pass. The recommendation in the inventory note is correct: preserve
`search_results` in `rawPayload` JSONB on `AiSurfaceRun`. No payload evidence
exists for this. Do not create the family.

### AI Keyword Data API family — do not address in this pass

Explicitly out of scope per the surface inventory note. Flag for future
governance when first used. Do not include in the authority update.

### Open questions 12.1 and 12.2 — explicitly defer, do not block

Open question 12.1 (`CrawledPage` "current/latest" materialized view) and 12.2
(`ObservatoryScope` ↔ `TopicMonitor` cardinality) do not need to be resolved
before promotion. Record the deferral explicitly in the authority doc or in a
follow-on note. Do not let them block the promotion.

---

## 4. Credit-Blocked Items

These items are blocked specifically by missing DataForSEO provider credits
for unsampled surfaces:

**`AiMentionCluster` full family governance** — the LLM Mentions API requires
credits to pull real payloads. The family cannot move from deferred-but-owned
to governed canonical until payloads are captured. Resume condition: credits
unlocked → pull real LLM Mentions payload → inventory it → compare against
docs-confirmed design → promote only what is now evidenced.

**LLM Scraper payload confirmation** — `AiCitationObservation` `snippetText`
and `publicationDate` fields are docs-confirmed from LLM Scraper `sources[]`.
These can be promoted as provisional fields now. Full confirmation requires
LLM Scraper credits.

**Gemini, Claude, Perplexity LLM Responses platform comparison** — the
`dataforseo-capture-plan.md` lists these as pending. The multi-platform `platform`
field posture is docs-confirmed, not payload-confirmed for these platforms.
The authority update should note this. No credits are required to proceed with
the ChatGPT-payload-confirmed posture — only for confirming the other platforms.

**`AiEntityObservation` for LLM Scraper `brand_entities`** — docs-confirmed
for ChatGPT only; Gemini LLM Scraper brand entity behavior is unclear. Minor.
The family design is sound; this is a completeness gap, not a structural blocker.

---

## 5. Open Questions That Must Be Resolved or Explicitly Deferred

These are the design pass open questions as they now stand, after applying the
corrections note and the surface inventory note:

| # | Question | Status |
|---|---|---|
| 12.1 | `CrawledPage` deduplication / "latest" materialized view posture | Defer explicitly — needs operational implementation evidence |
| 12.2 | `ObservatoryScope` ↔ `TopicMonitor` cardinality; whether `TopicMonitor` requires a scope | Defer explicitly — `observatoryScopeId` nullable on `TopicMonitor`; decide when first implementation case arrives |
| 12.3 | `KeywordTarget` → `TopicMonitor` association mechanism (junction table vs FK) | Defer explicitly — `TopicMonitor` exists as a family; association mechanism governed in a follow-on schema update |
| 12.4 | AI-surface platforms not yet sampled | Substantially resolved — LLM Responses shape is platform-consistent at top level; remaining gaps are LLM Scraper Gemini brand entities and pending comparison captures. Mark in authority doc. |
| 12.5 | `CrawlFailureRecord` error taxonomy: enum vs free-text | Closed — `error` is free-text per official docs. Record as resolved. |

All three remaining open questions (12.1–12.3) should be recorded as explicitly
deferred in the authority doc, not left as silently open. The deferral is the
governance act, not the resolution.

---

## 6. Bounded Authority Update Justified Now

The justified update to `veda/schema-reference.md` is a bounded replacement of
the "Deferred Owned Domains" section with governed canonical family definitions,
plus one new deferred-but-owned entry.

**What moves from "Deferred Owned Domains" to "Canonical Record Families":**

- `CrawlJob` (with corrections applied — no changes to core fields)
- `CrawledPage`
- `CrawlFailureRecord` (with `failureClass` discriminator applied)
- `DiscoveryObservation` (with `urlLimit` and `cacheIgnored` fields added)
- `ObservatoryScope`
- `TopicMonitor` (with association mechanism deferred explicitly)
- `AiSurfaceRun` (with confidence note: ChatGPT payload-confirmed, multi-platform docs-confirmed)
- `AiMentionObservation`
- `AiCitationObservation` (with `snippetText` and `publicationDate` as docs-confirmed provisional fields)
- `AiFanOutQueryObservation`
- `AiEntityObservation`

**Critical requirement for the AI-surface families:** The `veda/schema-reference.md`
text for each of the five AI-surface families must carry an inline evidence-posture
note directly in the family definition — not only referenced from this note or the
design pass. The note should read approximately:

> **Evidence posture:** `AiSurfaceRun` and child observation families are
> payload-confirmed for ChatGPT LLM Responses (one baseline in
> `transition-steward/dataforseo-json/`). Multi-platform generalization
> (`platform` field accommodating Gemini, Claude, Perplexity) is docs-confirmed
> pending comparison payload captures. Fields marked provisional (`snippetText`,
> `publicationDate` on `AiCitationObservation`) are docs-confirmed from LLM
> Scraper sources and subject to correction when LLM Scraper payloads are
> captured.

If the authority update omits this inline marker and presents the AI-surface
families as uniformly settled canonical structure, the promotion should be
reverted and rewritten before merging. The confidence distinction must survive
in the doc itself, not only in transition-steward notes.

**What stays in "Deferred Owned Domains" (existing or new):**

- `GA4 observations` — unchanged; still deferred
- `YouTube enrichment data` — unchanged; still deferred
- `AiMentionCluster` — new deferred-but-owned entry (moved from design pass to explicit deferred status)
- `AiRetrievalObservation` (background retrieval / `search_results`) — new deferred-but-owned entry
- `AI Keyword Data` — new deferred-but-owned entry

**What also needs updating in the authority doc:**

- The Controlled Vocabularies section must add the new enum values required by
  the promoted families: `ObservatoryScopeType`, `CrawlJobStatus`,
  `CrawlFailureClass`, `AiPlatform` (or equivalent). These follow from the
  family definitions.
- The "Records Eliminated or Transferred" section does not need changes.
- Structural Rules do not need changes.
- Anti-drift rules may gain one new entry: do not conflate `ObservatoryScope`
  with the existing thin `Project` partition record (this is already in the
  design pass anti-drift list and should be reflected).

**What `veda/data-boundaries.md` needs:**

One addition: an explicit "Crawled page observability and AI-surface observability
boundary" entry parallel to the existing bucket/snapshot posture section, stating
the canonical-vs-archive boundary for the Firecrawl and AI-surface families as
defined in design pass Section 8. The `data-boundaries.md` already has the bucket
storage posture entry; the addition is the family-specific canonical/archive
classification for the newly promoted families.

**This is a significant but bounded update.** It is not a rewrite of the doc.
It replaces one section, extends another, adds vocabulary entries, and adds one
data-boundaries note.

---

## 7. Biggest Anti-Drift Warning

**Do not promote `AiMentionCluster` as a governed canonical family.**

This is the highest-risk drift in the current batch. The family is well-designed,
well-described in the surface inventory note, and clearly needed. But it has zero
payload evidence. The confidence layer addendum explicitly flags it as the most
speculative element in the pass.

If `AiMentionCluster` is promoted to a governed canonical family now, it will
be implemented against docs-only schema assumptions. When LLM Mentions payloads
are eventually captured, the real shapes may differ from the docs. At that point,
correcting a promoted authority doc is harder than correcting a deferred-but-owned
entry. The deferred-but-owned treatment is the correct conservative call.

The secondary anti-drift risk is treating the five promotable AI-surface families
as equally payload-confirmed when they are not. The authority doc must preserve
the confidence distinction — `AiSurfaceRun` and its children are payload-confirmed
for ChatGPT LLM Responses, docs-confirmed for the rest. This distinction matters
when implementations rely on the schema and encounter a platform whose real
payload shape differs from the docs.

---

## 8. Recommended Next Move

**Execute the bounded authority update to `veda/schema-reference.md` described
in Section 6.**

Specifically:
1. Move the six Firecrawl / scope / monitor families (`CrawlJob`, `CrawledPage`,
   `CrawlFailureRecord`, `DiscoveryObservation`, `ObservatoryScope`, `TopicMonitor`)
   from "Deferred Owned Domains" into "Canonical Record Families" with corrections
   applied and explicit deferred decisions recorded for the three open questions
2. Move the five AI-surface families into "Canonical Record Families" **only if**
   each family definition carries the required inline evidence-posture note as
   specified in Section 6. Do not merge the AI-surface section without it.
3. Add `AiMentionCluster`, `AiRetrievalObservation`, and `AI Keyword Data` as
   new deferred-but-owned entries
4. Add required vocabulary entries for the new families
5. Add the data-boundaries note to `veda/data-boundaries.md`

Do this as a single reviewable PR. Do not try to also update the Firecrawl and
DataForSEO provider docs in the same PR — those are lower-priority secondary
updates and should come after the schema-reference promotion is accepted.

---

## 8. Related Files

- `transition-steward/batch-h-veda-family-design-pass.md` — primary design source
- `transition-steward/batch-h-veda-family-design-pass-corrections.md` — official-doc corrections
- `transition-steward/batch-h-dataforseo-surface-inventory.md` — DataForSEO sub-product inventory
- `transition-steward/batch-h-dataforseo-confidence-layer.md` — confidence classification
- `transition-steward/batch-h-waiting-on-provider-credits.md` — credit-block record
- `transition-steward/firecrawl/firecrawl-crawl-map-surface-inventory.md` — Firecrawl grounding
- `transition-steward/firecrawl/README.md` — Firecrawl baseline summary
- `veda/schema-reference.md` — authority update target (primary)
- `veda/data-boundaries.md` — authority update target (secondary)
- `veda/providers/registry.md` — no change required in this pass
