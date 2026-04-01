# V Forge Controlled Vocabularies

## Purpose

This document defines the canonical first-pass controlled vocabularies for V Forge.

It exists to answer:

```text
What enum-like values are officially allowed across V Forge schema, API contracts,
execution workflows, and operator tooling — and what rules govern how those values
are extended or changed?
```

This is the canonical registry for V Forge first-pass controlled vocabularies.

If another doc lists values that conflict with this registry, this registry wins
until the conflict is resolved explicitly through a governed architecture decision.

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- all controlled vocabulary values used by first-pass V Forge schema, API contracts,
  and execution workflows
- the single source of truth for any V Forge field that uses a restricted value set
- the rules for adding, removing, or renaming vocabulary values

---

## Out of Scope

This document does not define:

- exact column types or SQL representations
- API request/response payload shape beyond vocabulary values
- content graph structural rules (those belong in `schema-authority.md`)
- Project V vocabulary (governed by `../project-v/controlled-vocabularies.md`)
- VEDA vocabulary (governed by VEDA's own controlled-vocabularies doc)
- surface taxonomy research detail or rationale

---

## System

- v-forge

---

## Core Rule

Controlled vocabulary values must not drift across docs, schema, routes, and implementation.

An operator, developer, or LLM must not need to reconstruct canonical values by reading
multiple files. This file is the single source of truth for first-pass V Forge vocabulary
values.

Adding, removing, or renaming a value is a governed architecture event, not a local
implementation convenience. Follow the Vocabulary Change Rule at the end of this document.

Free-text values must not replace controlled vocabulary fields where governance is intended.
A field that accepts a controlled vocabulary must reject values not listed in this registry.

---

## Relationship to Schema Authority

`schema-authority.md` defines which record families carry controlled vocabulary fields
and names those fields.

This document defines the exact allowed values for each of those fields.

The authority chain is:

- `v-forge.md` → identity and ownership
- `schema-authority.md` → record families and field posture
- `controlled-vocabularies.md` (this doc) → allowed values
- `schema-specification.md` → exact column-level implementation

This document is subordinate to `schema-authority.md`. It must not silently
introduce field posture changes or expand the schema ownership of V Forge beyond
what `schema-authority.md` defines.

---

## Scope Boundary

These vocabularies are bounded to first-pass V Forge scope as defined in
`schema-authority.md` and the V Forge initial scope decision.

First-pass scope includes:

- two first-class project types: `content_affiliate` and `plugin_product`
- deeply modeled surfaces: website and GitHub/release
- lightly tracked surfaces: YouTube, social, newsletter, store listings
- deferred domains: experimentation/optimization, SaaS/runtime/commercial

Vocabulary values for deferred domains must not be pre-admitted.
If a value does not have a first-pass record family or field to attach to, it does not
belong in this document.

---

## Vocabulary Tables

---

### `project_type`

**Governs:** The thin local Project anchor record in V Forge. Identifies what kind of
project the execution scope belongs to, so that surface type and playbook routing can
use project type as a scoping filter where useful.

**Note:** Project V is the canonical owner of project identity. This vocabulary exists
in V Forge only to support local execution scoping. V Forge must not use it to replicate
Project V planning structure.

| Value | Meaning |
|---|---|
| `content_affiliate` | A content, affiliate, or lead-generation web property. Primary surfaces: website. May include YouTube, social, newsletter as operated surfaces. |
| `plugin_product` | A plugin, extension, or software product. Primary surfaces: GitHub/release, store listings. May include website, social, newsletter as operated surfaces. |

**Extension note:** Additional project types are not first-pass. Adding a new value
requires a governed schema expansion review because project type affects surface type
defaults, playbook routing, and scope classification.

---

### `surface_type`

**Governs:** The `Surface` record. Identifies what kind of execution surface is registered.

| Value | Meaning | Depth |
|---|---|---|
| `website` | Owned web property with a content graph. Deeply modeled. | Core |
| `github_repo` | GitHub repository used as the release surface for a plugin/product. Deeply modeled. | Core |
| `youtube_channel` | Operated YouTube channel. Lightly tracked. | Light |
| `social_profile` | Operated social media profile (any platform). Lightly tracked. | Light |
| `newsletter` | Operated email newsletter. Lightly tracked. | Light |
| `store_listing` | Distribution store listing (e.g., WordPress plugin directory, Chrome Web Store). Tracked through Surface and StorePublication records. | Light |

**Extension note:** Additional surface types (e.g., podcast feed, community platform,
SaaS product surface, paid ad surface) are not first-pass. Promoting a lightly tracked
surface to deeply modeled status requires a governed schema expansion review.
Experimental or runtime surface types must not be pre-admitted.

**Constraint:** Surface type must match the project type in practice. A `content_affiliate`
project would not register a `github_repo` as its primary surface under normal conditions.
This is enforced by operational convention rather than hard constraint in first pass, but
operator tooling should validate surface type compatibility where possible.

---

### `ownership_class`

**Governs:** The `Surface` record. Identifies the relationship between V Forge and the surface.

| Value | Meaning |
|---|---|
| `owned` | V Forge owns and operates this surface directly as part of the project's execution footprint. The project controls it. |
| `operated` | V Forge actively operates this surface (publishes content, releases, etc.) but does not have full platform ownership (e.g., YouTube channel, social profile on a third-party platform). |
| `referenced` | V Forge tracks this surface for distribution or reference purposes but does not actively operate it within this project's execution scope. |

**Extension note:** Additional ownership classes are not anticipated for first pass.

---

### `surface_status`

**Governs:** The `Surface` record lifecycle.

| Value | Meaning |
|---|---|
| `active` | The surface is actively operated within this project's execution scope. |
| `paused` | The surface is temporarily not being operated but remains registered. |
| `retired` | The surface is no longer actively operated. Retained for history. |

---

### `content_archetype`

**Governs:** The `Page` record in the content graph. Classifies the structural role
of a piece of content within the project.

| Value | Meaning |
|---|---|
| `pillar` | A comprehensive, authoritative resource on a broad topic. Typically long-form. Usually the hub of a content cluster. |
| `spoke` | A focused post targeting a specific sub-topic, supporting a pillar. Part of a content cluster. |
| `comparison` | A structured comparison of products, tools, or options. Typically conversion-oriented. |
| `review` | An evaluation of a specific product, tool, or service. |
| `listicle` | A list-structured post (e.g., "Top 10 X for Y"). |
| `tutorial` | Step-by-step instructional content. |
| `landing_page` | A conversion-oriented page. May not be content-rich but is a published surface node. |
| `changelog` | A version-indexed record of changes to a product or project. Primarily used in plugin/product projects. |
| `homepage` | The root page of a website surface. |
| `category_page` | A taxonomic grouping page. Typically auto-generated or template-driven. |
| `documentation` | A product or plugin documentation page — setup guides, configuration references, API docs, support pages, or operational references. Distinct from `tutorial` (which is instructional and standalone), `changelog` (which is version-indexed), and `landing_page` (which is conversion-oriented). Primarily used in plugin/product projects. |
| `standalone` | A page that does not fit neatly into pillar-spoke or other structural archetypes. Published and tracked, but not cluster-aligned. |

**Extension note:** Additional archetypes should be added only when an execution workflow
requires a distinct classification that existing values cannot support. Do not add archetypes
for speculative content types.

---

### `publication_status`

**Governs:** The `Page` record. Tracks the operational publication state of the page.

| Value | Meaning |
|---|---|
| `draft` | Created in V Forge but not yet published. |
| `published` | Live and publicly accessible. Includes pages that have been updated since initial publication — update history belongs in `PublicationEvent`, not in this field. |
| `archived` | No longer actively published. Retained for history. May redirect. |
| `redirected` | Has been formally redirected to another URL. The original page no longer resolves independently. |
| `unpublished` | Was published but has been taken down without being archived. |

**Boundary note:** `publication_status` is a resting-state field, not an event log. Page update history is recorded through `PublicationEvent` records with `publication_event_type = updated`. Do not add event-like values (e.g., `updated`, `refreshed`) to this vocabulary — they belong in `publication_event_type`.

---

### `content_decay_status`

**Governs:** The `Page` record. Indicates whether the page's content freshness has been
evaluated and what the result was.

| Value | Meaning |
|---|---|
| `not_evaluated` | No decay evaluation has been performed. Default state. |
| `current` | Evaluated and considered up to date. |
| `aging` | Evaluated and flagged as showing signs of aging. Review recommended but not urgent. |
| `stale` | Evaluated and considered stale. Refresh or update is warranted. |
| `critical` | Evaluated and critically outdated. Continued publication at this state is a quality risk. |

**Note:** Content decay status is set by V Forge execution workflows (operator-driven or
LLM-assisted). It must not be derived from VEDA signal and stored here as though V Forge
originated the signal. Decay status reflects V Forge's execution-side assessment of the
page's content freshness, optionally informed by signal consumed through the governed
VEDA interface.

---

### `schema_markup_type`

**Governs:** The `Page` record. Records what structured data markup schema type has been
applied to the page, if any.

| Value | Meaning |
|---|---|
| `none` | No schema markup applied. |
| `article` | Schema.org Article or BlogPosting markup. |
| `faq` | Schema.org FAQPage markup. |
| `how_to` | Schema.org HowTo markup. |
| `product` | Schema.org Product markup. |
| `review` | Schema.org Review or AggregateRating markup. |
| `breadcrumb` | Schema.org BreadcrumbList markup. |
| `local_business` | Schema.org LocalBusiness markup. |
| `software_application` | Schema.org SoftwareApplication markup. Primarily used on plugin/product project surfaces. |
| `multiple` | More than one schema type applied. The specific types should be noted in a metadata field rather than listed here. |

**Extension note:** Additional schema types should be added when first-pass execution
workflows need to track a distinct type for operational purposes. Do not pre-admit
rarely used schema types as speculative completeness.

---

### `topic_type`

**Governs:** The `Topic` record in the content graph. Classifies what kind of topic
the entry represents.

| Value | Meaning |
|---|---|
| `primary` | A top-level topic the project actively targets and builds content around. |
| `secondary` | A topic the project covers but that is subordinate to a primary topic. |
| `entity_topic` | A topic organized around a named entity (product, brand, person, tool) rather than a conceptual subject. |
| `structural` | A topic used for navigational or structural purposes (e.g., a category or hub topic) rather than direct content targeting. |

---

### `entity_type`

**Governs:** The `Entity` record in the content graph. Classifies what kind of named
thing the entity represents.

| Value | Meaning |
|---|---|
| `product` | A named product (software, physical, or digital). |
| `brand` | A named brand or company. |
| `person` | A named individual. |
| `tool` | A named tool, service, or platform (may overlap with product but is operationally distinct in SEO/content contexts). |
| `concept` | A named concept, methodology, or framework that appears as a recurring entity across content. |

---

### `link_type`

**Governs:** The `InternalLink` record in the content graph. Classifies the functional
role of an internal link.

| Value | Meaning |
|---|---|
| `contextual` | An in-body link placed within the prose of a page to link to a related or supporting page. |
| `navigational` | A link in a navigation element (menu, header, sidebar, breadcrumb). |
| `related_post` | A link in a "related posts" or "you might also like" module, typically template-driven. |
| `footer` | A link placed in the site footer. |

---

### `publication_event_type`

**Governs:** The `PublicationEvent` record. Classifies what kind of publication action
was recorded.

| Value | Meaning |
|---|---|
| `published` | The page was published for the first time. |
| `updated` | An existing published page was updated. |
| `republished` | The page was republished after being archived or unpublished. |
| `archived` | The page was archived. |
| `redirected` | The page was redirected to another URL. |
| `unpublished` | The page was taken down without being archived. |

---

### `store_publication_status`

**Governs:** The `StorePublication` record. Tracks the review and publication status
of a release submitted to a distribution store surface.

| Value | Meaning |
|---|---|
| `pending_review` | Submitted to the store but not yet reviewed or approved. |
| `published` | Approved and live on the store. |
| `rejected` | Reviewed and rejected by the store. |
| `withdrawn` | Withdrawn from the store by the operator before or after publication. |

---

### `distribution_content_type`

**Governs:** The `DistributionAction` record. Identifies the type of source content
that was distributed.

| Value | Meaning |
|---|---|
| `page` | A website page from the content graph. |
| `release` | A versioned release from the GitHub/release surface. |
| `video` | A YouTube video from the video tracking records. |
| `newsletter_issue` | A newsletter issue from the newsletter tracking records. |

**Extension note:** Additional distribution content types would require the corresponding
source record family to exist in the first-pass schema. Do not add values for deferred
surface types.

---

### `video_visibility_status`

**Governs:** The `Video` record (Domain 6, light-tracked). Tracks the YouTube visibility
state of a tracked video.

| Value | Meaning |
|---|---|
| `public` | Visible to anyone on YouTube. |
| `unlisted` | Not listed publicly but accessible via direct URL. |
| `private` | Only accessible to the channel owner. Not publicly reachable. |

**Boundary note:** Premiere, scheduled, and age-restricted states are not first-pass
vocabulary. The `Video` record is lightly tracked — this vocabulary covers only the
basic visibility states needed for execution-side surface awareness.

---

### `playbook_type`

**Governs:** The `Playbook` record. Classifies the kind of workflow task the playbook
addresses.

| Value | Meaning |
|---|---|
| `content_creation` | Playbook for creating new content on a surface (new page, new post). |
| `content_update` | Playbook for updating or refreshing existing content. |
| `publication` | Playbook for the publication or release process for a surface. |
| `distribution` | Playbook for cross-surface distribution of content or releases. |
| `maintenance` | Playbook for recurring maintenance activities on a surface or content asset. |
| `release` | Playbook for the release process for a plugin/product surface. |
| `store_submission` | Playbook for submitting a release to a distribution store. |
| `surface_setup` | Playbook for the initial setup or configuration of a new surface. |
| `audit` | Playbook for auditing a surface or content set for execution-quality issues. |

**Extension note:** Additional playbook types are added when a distinct repeatable
workflow class is scoped and a playbook doc is being created for it. Do not
pre-admit playbook types for unscoped future workflows.

---

### Domain 7 — Execution Continuity Vocabularies

The following vocabularies govern the Domain 7 record families defined in `schema-authority.md`.

---

#### `execution_entry_status`

**Governs:** The `ExecutionEntry` record. Tracks the lifecycle state of a V Forge-side
execution entry.

| Value | Meaning |
|---|---|
| `received` | Handoff or execution authorization has been received. Not yet checked for sufficiency. |
| `pending_clarification` | Handoff has been checked and found insufficient for bounded execution. Execution has not begun. Clarification or sufficiency resolution is required before execution can proceed. Distinct from `paused` and `blocked` — those imply execution was already active. |
| `active` | Handoff has been checked, found sufficient, and execution is in progress. |
| `paused` | Execution has been paused pending clarification, approval, or external condition. |
| `completed` | Execution has completed within the approved scope. |
| `blocked` | Execution is blocked and cannot continue without external resolution. |
| `returned` | A return-to-planning has been formally triggered for this execution entry. |
| `closed` | Execution entry has been closed (either completed or formally resolved through another path). |

---

#### `execution_finding_type`

**Governs:** The `ExecutionFinding` record. Classifies what kind of finding was produced
during execution.

| Value | Meaning |
|---|---|
| `blocker` | A finding that prevents execution from continuing. Requires resolution before progress can resume. |
| `changed_condition` | A condition that has changed since the handoff was prepared, affecting execution legitimacy or scope. |
| `decision_point` | A point in execution where a decision is required before continuing. |
| `scope_gap` | A gap in the handoff scope that prevents clean bounded execution. |
| `quality_issue` | An execution-side quality concern identified during work. |
| `informational` | A bounded finding that does not block execution but is worth recording for continuity and review. |

---

#### `execution_finding_status`

**Governs:** The `ExecutionFinding` record lifecycle.

| Value | Meaning |
|---|---|
| `open` | Finding is recorded and has not been resolved. |
| `resolved_locally` | Finding has been resolved within execution scope without requiring return-to-planning. |
| `returned` | Finding has been formally returned to Project V through a `ReturnToPlanning` record. |
| `invalidated` | Finding was recorded but later determined to be inapplicable or incorrect. |

---

#### `maintenance_type`

**Governs:** The `MaintenanceRecord` record. Classifies the kind of maintenance activity performed.

| Value | Meaning |
|---|---|
| `content_refresh` | Content on a page was reviewed and refreshed for accuracy or freshness. |
| `content_update` | Content on a page was substantively updated (new information added, structure changed). |
| `broken_link_repair` | Internal or external broken links were identified and repaired. |
| `schema_markup_update` | Structured data markup on a page was updated or corrected. |
| `redirect_management` | A redirect was created, updated, or reviewed. |
| `release_patch` | A patch release was issued for a plugin/product surface. |
| `store_listing_update` | A store listing (description, screenshots, metadata) was updated. |
| `surface_configuration` | Surface-level configuration was updated (e.g., site settings, plugin settings). |
| `dependency_update` | A dependency (plugin, library, theme) was updated as part of surface maintenance. |

**Extension note:** Additional maintenance types should be added as the real operational
maintenance taxonomy becomes clearer through execution. Do not pre-admit maintenance types
for deferred surface types or speculative workflows.

---

## Admission and Extension Rule

A controlled vocabulary change is a governed architecture event.

When a value is added, removed, or renamed:

1. Update this registry first
2. Update `schema-authority.md` if the change affects a named field constraint there
3. Update `schema-specification.md` if the change affects a column definition
4. Update API contract docs if the affected field is exposed through the API
5. Update operator tooling and LLM guidance docs if affected
6. Update hammer expectations if the vocabulary field is verified by the hammer layer

Do not silently extend controlled values in implementation first.

### Rules for adding a new value

Before adding a value to any vocabulary in this document:

- confirm that a first-pass record family and field exist in `schema-authority.md`
  that would use this value
- confirm that the value represents a real execution concept that first-pass V Forge
  scope already covers
- confirm that the value is not a stand-in for a deferred domain
  (experimentation, SaaS/runtime, commercial surfaces, deep social analytics)
- confirm that the value has stable, distinct meaning that cannot be covered by
  an existing value

### Rules for removing or renaming a value

Removing or renaming a controlled vocabulary value is a breaking change if any existing
data records carry the old value. Deprecation and migration planning are required before
removal. Renaming requires a migration strategy for existing records.

---

## Anti-Drift Rules

V Forge controlled vocabularies have drifted if:

### 1. Deferred domain values appear
If vocabulary values appear for experimentation, A/B testing, SaaS/runtime surfaces,
commercial surfaces, advanced engagement analytics, or other deferred domains, the
vocabularies have drifted.

### 2. Free-text replaces governed vocabulary
If a field that carries execution-relevant classification is left as free text because
no vocabulary was defined, and classification is therefore invented locally at
implementation time, the vocabulary layer has failed. The correct response is to define
the vocabulary here before implementation proceeds.

### 3. A value set is extended without governance
If implementation, migration scripts, or API route handlers introduce new values for
a governed field without updating this document first, the vocabulary has drifted.

### 4. Light-tracked surface vocabulary expands without governance
If the vocabulary tables for YouTube, social, newsletter, or store listing concepts
expand significantly beyond what their minimal first-pass schema depth requires, the
vocabulary has drifted.

### 5. Planning-truth vocabularies appear in V Forge
If vocabulary values are added to classify planning states, readiness posture, orchestration
stages, or other concepts that belong to Project V, the vocabularies have drifted.
V Forge vocabulary governs execution truth, not planning truth.

### 6. Observatory vocabularies appear in V Forge
If vocabulary values are added to classify VEDA-originated signals, observation types,
evidence provenance, or raw data source categories, the vocabularies have drifted.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- this file is the canonical single source of truth for all allowed V Forge vocabulary values
- values not listed here are not allowed without a governed change
- adding a value silently in implementation is a vocabulary failure
- vocabulary is bounded to first-pass scope — deferred domains have no pre-admitted values
- `content_affiliate` and `plugin_product` are the two supported project types
- website and `github_repo` are the deeply modeled surface types
- YouTube, social, newsletter, and store listing have minimal vocabulary coverage because
  they are lightly tracked in first pass
- Domain 7 execution continuity vocabularies exist to support the four record families
  named in `schema-authority.md` and must not be expanded into shadow-planning vocabulary

---

## Usage

This document should be used:

- as the first reference when setting any V Forge field that accepts restricted values
- when implementing schema column definitions, API validation logic, and operator forms
- when writing hammer expectations that verify vocabulary-governed fields
- when proposing a vocabulary change through the governed change path
- when reviewing whether an implementation value matches the governed enum set

---

## Related Docs

- `v-forge.md`
- `schema-authority.md`
- `schema-specification.md`
- `system-invariants.md`
- `../project-v/controlled-vocabularies.md`
- `../ecosystem/vocabulary.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
