# V Forge Schema Specification

## Purpose

This document defines the first-pass concrete schema specification for V Forge.

It exists to answer:

```text
What are the fields, types, constraints, relationships, and mutation posture for
each first-pass V Forge record family — in enough detail that implementation can
proceed without inventing schema decisions?
```

Read this with:

- `schema-authority.md`
- `controlled-vocabularies.md`
- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`

If this document conflicts with `schema-authority.md`, the conflict must be resolved
explicitly. Neither should be silently ignored.

This is a Tier 2 project implementation build-spec authority document.

---

## Scope

This document governs:

- the exact first-pass V Forge record families
- fields, types, and constraints for each record family
- required vs optional fields
- uniqueness and identity rules
- key relationships between record families
- project-scoping rules per record family
- mutability posture where relevant
- transactional and atomicity posture where relevant

---

## Out of Scope

This document does not define:

- literal SQL DDL or migration scripts
- Prisma or ORM model files
- API route contracts or payload shapes beyond field posture
- detailed query patterns or endpoint families
- VEDA schema design
- Project V schema design
- experimentation, SaaS/runtime, or commercial layer schema (deferred)
- deep social analytics or advanced engagement schema (deferred)

Those belong in migration docs, API contract docs, and later governed extension docs.

---

## System

- v-forge

---

## Core Rule

V Forge schema must remain strictly aligned to V Forge execution truth ownership.

This means the first-pass schema may model:

- execution truth
- content graph truth
- publication and release continuity truth
- distribution tracking truth
- playbook routing truth
- execution continuity and lifecycle truth
- lightly tracked operated surface records

It must not model:

- Project V planning truth, readiness truth, or orchestration truth
- VEDA observatory truth, raw signal data, or evidence provenance
- convenience copies of another system's canonical state
- deferred future domains (experimentation, SaaS/runtime, commercial)

V Forge schema resides in V Forge's own database, separate from Project V's database
and VEDA's database. No direct database access crosses system boundaries.

---

## Relationship to Schema Authority and Controlled Vocabularies

`schema-authority.md` defines what domains and record families belong in first-pass
V Forge schema and what the ownership posture is for each domain.

`controlled-vocabularies.md` defines the exact allowed values for every controlled
vocabulary field in this spec.

This document is subordinate to both. It must not introduce new record families,
new ownership claims, or new vocabulary values beyond what those two documents establish.

The authority chain is:

- `v-forge.md` → identity and ownership
- `schema-authority.md` → domain and record family posture
- `controlled-vocabularies.md` → allowed enum values
- `schema-specification.md` (this doc) → concrete field-level spec
- `schema-specification.md` → migration and implementation authority

---

## Type Conventions

These specifications assume PostgreSQL.

Recommended baseline type posture:

- primary keys: `uuid`
- foreign keys: `uuid`
- short string fields: `text`
- longer content fields: `text`
- status and controlled-vocabulary fields: `text` constrained by application
  validation and a later check-constraint or enum strategy
- timestamps: `timestamptz`
- booleans: `boolean`
- counts and integer metrics: `integer`
- bounded flexible payloads only where explicitly justified: `jsonb`

---

## Schema-Wide Rules

### 1. All records are project-scoped
Every first-pass V Forge record family belongs to exactly one project, anchored
by `project_id`. No cross-project relations are permitted. Records must not exist
without a valid project anchor.

### 2. Project-compatibility enforcement
Where one project-scoped record references another, both must belong to the same
`project_id`. This must be enforced at both the application layer and, where
critical, at the database layer.

### 3. Controlled vocabulary enforcement
Fields that use controlled vocabularies must reject values not listed in
`controlled-vocabularies.md`. The canonical value sets are defined there, not
invented at implementation time.

### 4. `updated_at` maintenance rule
Where a record family carries `updated_at`, it must be updated by the application
mutation path in the same transaction as the governed write. The first-pass posture
does not depend on database triggers for `updated_at`.

### 5. No delete in first pass
No first-pass V Forge table exposes destructive delete behavior until deletion
semantics are explicitly modeled. Archival, retirement, and status transitions
are the first-pass lifecycle mechanisms.

Exceptions: `InternalLink`, `PageTopic`, and `PageEntity` records may be deleted
when the relationship they represent no longer exists. These are current-state
junction or link records, not history records — retaining stale links or stale
junctions would corrupt the content graph. Each exception is noted in the
corresponding record family section. All other first-pass families are no-delete.

### 6. Deterministic ordering support
All list surfaces must be supportable by explicit ordering with stable tie-breakers.
Schema design must support predictable queries without ambiguous ordering.

### 7. Extension hooks are not pre-built
Deferred future domains (experimentation, SaaS/runtime, commercial, advanced
engagement analytics) must not appear as empty columns, nullable foreign keys,
or speculative junction tables in first-pass schema.

---

## Controlled Vocabulary Fields — Master List

The following fields must use controlled vocabularies as defined in
`controlled-vocabularies.md`. No other values are valid.

- `Project.project_type`
- `Surface.surface_type`
- `Surface.ownership_class`
- `Surface.status`
- `Page.content_archetype`
- `Page.publication_status`
- `Page.content_decay_status`
- `Page.schema_markup_type`
- `Topic.topic_type`
- `Entity.entity_type`
- `InternalLink.link_type`
- `PublicationEvent.event_type`
- `Release` (no enum fields in first pass beyond surface reference)
- `StorePublication.status`
- `DistributionAction.source_content_type`
- `Video.visibility_status`
- `Playbook.playbook_type`
- `ExecutionEntry.status`
- `ExecutionFinding.finding_type`
- `ExecutionFinding.status`
- `MaintenanceRecord.maintenance_type`

---

## Record Family Specifications

---

## Domain 0 — Project Anchor

### 1. `Project`

**Purpose:** Thin local execution-side project anchor. Exists to scope all V Forge
records to a project identity and enforce referential integrity within the V Forge
database. This is not a replication of Project V planning truth — it carries only
the identity fields needed for local scoping.

**Fields:**

- `id uuid primary key`
- `project_id_external uuid not null` — the Project V project UUID this anchor corresponds to; used for cross-system reference when consuming handoffs or returning findings
- `project_type text not null` — controlled vocabulary: `project_type`
- `name text not null` — display name, copied from handoff context at anchor creation; not a canonical planning field
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id_external)` — one V Forge anchor per Project V project
- `name` must be non-empty
- `project_type` must use the controlled vocabulary

**Indexes:**
- unique index on `(project_id_external)`
- index on `(project_type, updated_at desc, id)`

**Mutability:**
- `name` may be updated if the project display name changes
- `project_type` must not change after anchor creation without governed review
- no delete in first pass

**Boundary note:** The `id` of this record is the `project_id` used to scope all other
V Forge records. The `project_id_external` field is the reference back to Project V.
V Forge must not use this record to replicate planning structure, readiness state, or
orchestration truth from Project V.

---

## Domain 1 — Surface Registry

### 2. `Surface`

**Purpose:** Registry of all execution surfaces a project operates on. The foundational
inventory that scopes all other execution records. May carry surface-specific
operational configuration as governed structured metadata.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `surface_type text not null` — controlled vocabulary: `surface_type`
- `ownership_class text not null` — controlled vocabulary: `ownership_class`
- `status text not null default 'active'` — controlled vocabulary: `surface_status`
- `name text not null` — human-readable surface name (e.g., "Main Blog", "Chrome Extension Repo")
- `url text null` — primary URL or canonical identifier for the surface where applicable
- `platform_id text null` — platform-specific identifier (e.g., GitHub repo full name, YouTube channel ID); format varies by surface type
- `operational_notes text null` — free-text operational context; governance-intended structured metadata should be added as explicit fields, not buried here
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, surface_type, url)` where `url` is not null; surface deduplication within a project
- for surfaces where `url` is null, the schema does not enforce uniqueness by constraint; operator tooling and the application layer must enforce that at most one surface of a given `surface_type` is registered per project when no URL distinguishes them. Registering duplicate null-URL surfaces of the same type within a project is an operational error.
- `surface_type`, `ownership_class`, and `status` must use controlled vocabularies
- `name` must be non-empty
- every surface belongs to exactly one project

**Indexes:**
- index on `(project_id, status, updated_at desc, id)`
- index on `(project_id, surface_type, status, updated_at desc, id)`
- index on `(project_id, ownership_class, updated_at desc, id)`

**Mutability:**
- `name`, `url`, `platform_id`, `operational_notes` may be updated
- `status` transitions via governed path only
- `surface_type` must not change after creation without governed review — changing type would affect all downstream scoped records

---

### 3. `SurfaceSnapshot`

**Purpose:** Periodic health and size snapshot for a surface. Captures surface-level
vitals at a point in time. Not full analytics — lightweight operational pulse only.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `surface_id uuid not null references Surface(id)`
- `snapshot_at timestamptz not null` — when this snapshot was recorded
- `page_count integer null` — total page/post count for website surfaces
- `subscriber_count integer null` — subscriber or follower count for newsletter/social/YouTube surfaces
- `install_count integer null` — install count for plugin/product store surfaces
- `star_count integer null` — GitHub star count for GitHub repo surfaces
- `notes text null` — optional freeform annotation
- `created_at timestamptz not null default now()`

**Constraints:**
- `surface_id` must reference a surface belonging to the same `project_id`
- `snapshot_at` must not be in the future at record creation

**Indexes:**
- index on `(project_id, surface_id, snapshot_at desc, id)`
- index on `(project_id, snapshot_at desc, id)`

**Mutability:**
- snapshot records are immutable after creation; they are point-in-time records
- no update, no delete in first pass

---

## Domain 2 — Content Graph

### 4. `Page`

**Purpose:** Core content graph unit. The URL-level node of a project's built content
on a website surface. Execution truth — changes when V Forge builds or modifies content.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `surface_id uuid not null references Surface(id)` — must reference a `website` surface
- `url text not null` — canonical URL of the page
- `slug text not null` — URL slug; may be derived from URL or set independently
- `title text not null`
- `content_archetype text not null` — controlled vocabulary: `content_archetype`
- `publication_status text not null default 'draft'` — controlled vocabulary: `publication_status`
- `schema_markup_type text not null default 'none'` — controlled vocabulary: `schema_markup_type`
- `content_decay_status text not null default 'not_evaluated'` — controlled vocabulary: `content_decay_status`
- `word_count integer null`
- `published_at timestamptz null` — first publish timestamp
- `last_modified_at timestamptz null` — last meaningful content modification
- `last_reviewed_at timestamptz null` — last decay/quality review
- `primary_topic_id uuid null references Topic(id)` — the page's primary topic; must belong to the same project
- `handoff_ref text null` — reference to the Project V handoff that produced or last updated this page; thin bounded reference, not a planning record
- `redirect_target_url text null` — populated only when `publication_status = 'redirected'`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, url)` — one canonical record per URL per project
- `surface_id` must reference a surface of `surface_type = 'website'` belonging to the same `project_id`
- `primary_topic_id` must reference a topic belonging to the same `project_id`
- all controlled vocabulary fields must use valid values
- if `publication_status = 'redirected'`, `redirect_target_url` must be non-null and non-empty
- `slug`, `title`, `url` must be non-empty

**Indexes:**
- unique index on `(project_id, url)`
- index on `(project_id, publication_status, updated_at desc, id)`
- index on `(project_id, content_archetype, publication_status, updated_at desc, id)`
- index on `(project_id, content_decay_status, updated_at desc, id)`
- index on `(project_id, surface_id, updated_at desc, id)`
- index on `(project_id, primary_topic_id)` where `primary_topic_id` is not null

**Mutability:**
- `title`, `slug`, `content_archetype`, `schema_markup_type`, `word_count`, `last_modified_at`, `last_reviewed_at`, `primary_topic_id`, `handoff_ref`, `redirect_target_url` may be updated
- `publication_status` and `content_decay_status` transition via governed paths
- `url` changes must be reviewed carefully — URL change means the existing page record should typically be retired and a redirect created, not silently mutated
- `published_at` is set once at first publish and not subsequently updated

---

### 5. `Topic`

**Purpose:** Topical vocabulary of a project. The set of topics the project targets
and builds content around. Used to classify pages and content clusters.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `name text not null` — topic name as it should appear in tooling and analysis
- `topic_type text not null` — controlled vocabulary: `topic_type`
- `parent_topic_id uuid null references Topic(id)` — optional shallow parent for one-level hierarchy; must belong to same project if present
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, name)` — topics are unique by name within a project
- `name` must be non-empty
- `topic_type` must use controlled vocabulary
- `parent_topic_id` must reference a topic belonging to the same `project_id`
- topic hierarchy is bounded to one level of depth in first pass — a topic with a `parent_topic_id` must not itself be set as a `parent_topic_id` for another topic

**Indexes:**
- unique index on `(project_id, name)`
- index on `(project_id, topic_type, updated_at desc, id)`
- index on `(project_id, parent_topic_id)` where `parent_topic_id` is not null

**Mutability:**
- `name`, `topic_type`, `parent_topic_id` may be updated with care; name changes affect any downstream references

---

### 6. `Entity`

**Purpose:** Named things that appear across pages of a project. The entity vocabulary
used to classify what a project writes about across its content graph.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `name text not null` — canonical entity name
- `entity_type text not null` — controlled vocabulary: `entity_type`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, name)` — entities are unique by name within a project
- `name` must be non-empty
- `entity_type` must use controlled vocabulary

**Indexes:**
- unique index on `(project_id, name)`
- index on `(project_id, entity_type, updated_at desc, id)`

**Mutability:**
- `entity_type` may be updated
- `name` changes must be made carefully — entity name is the primary key for human recognition

---

### 7. `InternalLink`

**Purpose:** Link structure between pages within the same project. Captures the
internal linking graph for content graph analysis.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `source_page_id uuid not null references Page(id)`
- `target_page_id uuid not null references Page(id)`
- `anchor_text text null`
- `link_type text not null` — controlled vocabulary: `link_type`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, source_page_id, target_page_id, link_type)` — one record per distinct link type between two pages
- `source_page_id` and `target_page_id` must both belong to the same `project_id`
- `source_page_id` and `target_page_id` must not be identical (no self-links)
- `link_type` must use controlled vocabulary

**Indexes:**
- unique index on `(project_id, source_page_id, target_page_id, link_type)`
- index on `(project_id, source_page_id)`
- index on `(project_id, target_page_id)`
- index on `(project_id, link_type, updated_at desc, id)`

**Mutability:**
- `anchor_text` and `link_type` may be updated
- if the link no longer exists, the record should be deleted or archived — link records represent current link structure, so first-pass delete semantics are permitted here with care

---

### 8. `PageTopic`

**Purpose:** Junction table linking pages to topics. Allows a page to be associated
with multiple topics, with one designated as primary.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `page_id uuid not null references Page(id)`
- `topic_id uuid not null references Topic(id)`
- `is_primary boolean not null default false`
- `created_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, page_id, topic_id)` — one junction per page-topic pair per project
- `page_id` and `topic_id` must both belong to the same `project_id`
- at most one `PageTopic` record per `page_id` may have `is_primary = true`; enforced by application logic; the first-pass posture does not add a partial unique index but this rule must be respected
- this constraint is consistent with `Page.primary_topic_id` — the two should be kept consistent when topics are assigned

**Indexes:**
- unique index on `(project_id, page_id, topic_id)`
- index on `(project_id, topic_id, page_id)`
- index on `(project_id, page_id, is_primary)`

**Mutability:**
- `is_primary` may be updated; only one per `page_id` should be `true`
- junction records may be deleted when a topic is removed from a page

---

### 9. `PageEntity`

**Purpose:** Junction table linking pages to named entities. Allows a page to be
associated with multiple entities.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `page_id uuid not null references Page(id)`
- `entity_id uuid not null references Entity(id)`
- `mention_context text null` — optional short note about how the entity is mentioned on the page
- `created_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, page_id, entity_id)` — one junction per page-entity pair per project
- `page_id` and `entity_id` must both belong to the same `project_id`

**Indexes:**
- unique index on `(project_id, page_id, entity_id)`
- index on `(project_id, entity_id, page_id)`

**Mutability:**
- `mention_context` may be updated
- junction records may be deleted when an entity is removed from a page

---

### 10. `ContentCluster`

**Purpose:** Pillar-spoke grouping structure. Associates a set of pages into a named
cluster anchored by a pillar page. Spoke pages are identified by their `primary_topic_id`
matching the cluster's `primary_topic_id` — this is the explicit query path for listing
spoke pages in a cluster.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `name text not null` — cluster name
- `pillar_page_id uuid not null references Page(id)` — the pillar page anchoring this cluster
- `primary_topic_id uuid not null references Topic(id)` — the topic that defines this cluster; spoke pages are those whose `Page.primary_topic_id` matches this value within the same project
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, name)` — clusters are unique by name within a project
- unique: `(project_id, pillar_page_id)` — one cluster per pillar page per project
- unique: `(project_id, primary_topic_id)` — one cluster per topic per project
- `pillar_page_id` must reference a page belonging to the same `project_id`
- `pillar_page_id` must reference a page with `content_archetype = 'pillar'`
- `primary_topic_id` must reference a topic belonging to the same `project_id`
- `name` must be non-empty

**Indexes:**
- unique index on `(project_id, name)`
- unique index on `(project_id, pillar_page_id)`
- unique index on `(project_id, primary_topic_id)`
- index on `(project_id, updated_at desc, id)`

**Spoke membership query pattern:** To list all spoke pages in a cluster, query
`Page` where `project_id = :project_id AND primary_topic_id = :cluster.primary_topic_id
AND content_archetype != 'pillar'`. The pillar page itself shares the same
`primary_topic_id` but is excluded by archetype.

**Mutability:**
- `name` may be updated
- `pillar_page_id` and `primary_topic_id` changes require governed review — both define the structural identity of the cluster

---

## Domain 3 — Publication and Release Continuity

### 11. `PublicationEvent`

**Purpose:** Event log of publication actions on a page. Preserves the history of
what publication actions were taken and when. Resting publication state lives on the
`Page` record; this record preserves the event history.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `surface_id uuid not null references Surface(id)`
- `page_id uuid not null references Page(id)`
- `event_type text not null` — controlled vocabulary: `publication_event_type`
- `event_at timestamptz not null` — when the publication action occurred
- `handoff_ref text null` — reference to the handoff that triggered this event, if applicable
- `notes text null`
- `created_at timestamptz not null default now()`

**Constraints:**
- `page_id` must reference a page belonging to the same `project_id`
- `surface_id` must reference a surface belonging to the same `project_id`
- `surface_id` on the event must match the surface of the referenced page
- `event_type` must use controlled vocabulary
- `event_at` must not be materially in the future at record creation

**Indexes:**
- index on `(project_id, page_id, event_at desc, id)`
- index on `(project_id, surface_id, event_at desc, id)`
- index on `(project_id, event_type, event_at desc, id)`

**Mutability:**
- publication event records are immutable after creation; they are an append-only event log
- no update, no delete in first pass

---

### 12. `Release`

**Purpose:** Versioned release record for plugin/product GitHub/release surfaces.
Represents a named, versioned immutable artifact that was released.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `surface_id uuid not null references Surface(id)` — must reference a `github_repo` surface
- `version_tag text not null` — semantic version tag (e.g., `v1.2.3`)
- `release_name text null` — optional display name for the release
- `changelog_summary text null` — summary of what changed in this release
- `is_prerelease boolean not null default false`
- `asset_count integer not null default 0` — number of release assets attached
- `published_at timestamptz not null` — when the release was published on the platform
- `handoff_ref text null` — reference to the handoff that produced this release
- `created_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, surface_id, version_tag)` — one release per version per repo per project
- `surface_id` must reference a surface of `surface_type = 'github_repo'` belonging to the same `project_id`
- `version_tag` must be non-empty

**Indexes:**
- unique index on `(project_id, surface_id, version_tag)`
- index on `(project_id, surface_id, published_at desc, id)`
- index on `(project_id, is_prerelease, published_at desc, id)`

**Mutability:**
- release records are largely immutable; they represent a versioned artifact
- `changelog_summary`, `release_name`, `asset_count` may be updated where corrections are needed
- `version_tag` and `published_at` must not change after creation
- no delete in first pass

---

### 13. `StorePublication`

**Purpose:** Record of a release being published to a distribution store surface
(e.g., WordPress plugin directory, Chrome Web Store). Tracks the review and
publication lifecycle of a store submission.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `release_id uuid not null references Release(id)`
- `store_surface_id uuid not null references Surface(id)` — must reference a `store_listing` surface
- `published_version text not null` — version string as it appears on the store
- `status text not null default 'pending_review'` — controlled vocabulary: `store_publication_status`
- `submitted_at timestamptz not null`
- `published_at timestamptz null` — populated when status reaches `published`
- `notes text null`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, release_id, store_surface_id)` — one submission per release per store per project
- `release_id` must reference a release belonging to the same `project_id`
- `store_surface_id` must reference a surface of `surface_type = 'store_listing'` belonging to the same `project_id`
- `status` must use controlled vocabulary
- if `status = 'published'`, `published_at` must be non-null

**Indexes:**
- unique index on `(project_id, release_id, store_surface_id)`
- index on `(project_id, status, updated_at desc, id)`
- index on `(project_id, store_surface_id, status, updated_at desc, id)`

**Mutability:**
- `status` transitions via governed path; `published_at` must be set atomically when status reaches `published`
- `notes` may be updated freely

---

## Domain 4 — Distribution Tracking

### 14. `DistributionAction`

**Purpose:** Records that content from one surface was distributed to another surface.
The primary cross-surface relational mechanism in V Forge. Transforms V Forge from a
collection of per-surface trackers into an integrated multi-surface execution system.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `source_surface_id uuid not null references Surface(id)` — surface the content originates from
- `source_content_type text not null` — controlled vocabulary: `distribution_content_type`
- `source_content_id uuid not null` — ID of the source content record (page, release, video, or newsletter issue)
- `distribution_surface_id uuid not null references Surface(id)` — surface it was distributed to
- `distribution_url text null` — URL of the distributed post, announcement, or content
- `distributed_at timestamptz not null`
- `notes text null`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- `source_surface_id` and `distribution_surface_id` must both belong to the same `project_id`
- `source_surface_id` and `distribution_surface_id` must not be identical
- `source_content_type` must use controlled vocabulary
- `source_content_id` must reference a record of the type indicated by `source_content_type`, belonging to the same `project_id`; this is enforced at the application layer since it is a polymorphic reference

**Indexes:**
- index on `(project_id, source_surface_id, source_content_type, source_content_id)`
- index on `(project_id, distribution_surface_id, distributed_at desc, id)`
- index on `(project_id, distributed_at desc, id)`

**Mutability:**
- `notes`, `distribution_url` may be updated
- `distributed_at`, `source_content_type`, `source_content_id` must not change after creation

---

## Domain 5 — Playbook Routing

### 15. `Playbook`

**Purpose:** Metadata routing record for playbooks. Tells the LLM or operator which
playbook doc applies for a given task type, surface type, and content archetype.
Actual playbook content lives as structured docs referenced by path — not as modeled
step/action sequences in the database.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `playbook_type text not null` — controlled vocabulary: `playbook_type`
- `name text not null` — human-readable playbook name
- `surface_type_scope text null` — if set, this playbook applies only to surfaces of this type; uses `surface_type` vocabulary; null means applies to all applicable surface types
- `content_archetype_scope text null` — if set, this playbook applies only to pages of this archetype; uses `content_archetype` vocabulary; null means applies to all applicable archetypes
- `version text not null default '1'` — playbook version identifier
- `status text not null default 'active'` — `active` or `retired`; not a full lifecycle enum
- `doc_path text not null` — path reference to the playbook doc; does not store playbook content inline
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, playbook_type, surface_type_scope, content_archetype_scope, version)` — one active routing record per playbook configuration per project
- `playbook_type` must use controlled vocabulary
- if `surface_type_scope` is not null, it must use the `surface_type` controlled vocabulary
- if `content_archetype_scope` is not null, it must use the `content_archetype` controlled vocabulary
- `doc_path` must be non-empty
- `name` must be non-empty

**Indexes:**
- index on `(project_id, playbook_type, status, updated_at desc, id)`
- index on `(project_id, surface_type_scope, playbook_type)` where `surface_type_scope` is not null
- index on `(project_id, status, updated_at desc, id)`

**Mutability:**
- `doc_path`, `name`, `version`, `status` may be updated
- `playbook_type`, `surface_type_scope`, `content_archetype_scope` define the routing key and must not change without a governed review
- playbook content lives in the docs layer, not in the database; the `doc_path` is the reference

---

## Domain 6 — Light-Tracked Operated Surfaces

### 16. `Video`

**Purpose:** Light tracking record for YouTube videos on a tracked YouTube channel surface.
Minimal first-pass model — operational awareness, not deep analytics.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `surface_id uuid not null references Surface(id)` — must reference a `youtube_channel` surface
- `youtube_video_id text not null` — the YouTube platform video ID
- `title text not null`
- `published_at timestamptz null`
- `duration_seconds integer null`
- `visibility_status text not null default 'public'` — controlled vocabulary: `video_visibility_status`
- `linked_page_id uuid null references Page(id)` — optional link to a related website page; must belong to same project
- `linked_release_id uuid null references Release(id)` — optional link to a related release; must belong to same project
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, youtube_video_id)` — one record per YouTube video ID per project
- `surface_id` must reference a surface of `surface_type = 'youtube_channel'` belonging to the same `project_id`
- `visibility_status` must use controlled vocabulary
- if `linked_page_id` is not null, it must reference a page belonging to the same `project_id`
- if `linked_release_id` is not null, it must reference a release belonging to the same `project_id`

**Indexes:**
- unique index on `(project_id, youtube_video_id)`
- index on `(project_id, surface_id, published_at desc, id)`
- index on `(project_id, visibility_status, published_at desc, id)`

**Mutability:**
- `title`, `visibility_status`, `linked_page_id`, `linked_release_id`, `duration_seconds` may be updated
- `youtube_video_id` must not change after creation

---

### 17. `SocialPost`

**Purpose:** Light tracking record for social media posts on a tracked social profile
surface. Minimal first-pass model for distribution awareness.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `surface_id uuid not null references Surface(id)` — must reference a `social_profile` surface
- `post_url text null` — URL of the post if available
- `content_summary text null` — short summary of the post content
- `posted_at timestamptz not null`
- `linked_content_type text null` — uses `distribution_content_type` vocabulary; identifies what was promoted
- `linked_content_id uuid null` — ID of the linked content record; must belong to same project
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- `surface_id` must reference a surface of `surface_type = 'social_profile'` belonging to the same `project_id`
- if `linked_content_type` is not null, it must use the `distribution_content_type` controlled vocabulary
- if `linked_content_id` is not null, `linked_content_type` must also be non-null

**Indexes:**
- index on `(project_id, surface_id, posted_at desc, id)`
- index on `(project_id, posted_at desc, id)`

**Mutability:**
- `content_summary`, `post_url`, `linked_content_type`, `linked_content_id` may be updated
- `posted_at` must not change after creation

---

### 18. `NewsletterIssue`

**Purpose:** Light tracking record for newsletter issues sent via a newsletter surface.
Minimal first-pass model — issue-level awareness for distribution tracking.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `surface_id uuid not null references Surface(id)` — must reference a `newsletter` surface
- `subject text not null` — email subject line
- `sent_at timestamptz not null`
- `audience_description text null` — brief description of the audience or list segment
- `open_rate_pct integer null` — aggregate open rate as an integer percentage (0–100); not normalized analytics
- `click_rate_pct integer null` — aggregate click rate as an integer percentage (0–100)
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- `surface_id` must reference a surface of `surface_type = 'newsletter'` belonging to the same `project_id`
- `subject` must be non-empty
- if `open_rate_pct` is not null, it must be in range 0–100
- if `click_rate_pct` is not null, it must be in range 0–100

**Indexes:**
- index on `(project_id, surface_id, sent_at desc, id)`
- index on `(project_id, sent_at desc, id)`

**Mutability:**
- `audience_description`, `open_rate_pct`, `click_rate_pct` may be updated as post-send data becomes available
- `subject`, `sent_at` must not change after creation

---

## Domain 7 — Execution Continuity Support

### 19. `ExecutionEntry`

**Purpose:** V Forge-side receipt of work entering execution. Records that a handoff
arrived, anchors subsequent execution tracking to that entry point. Does not replicate
planning content from Project V — carries only the reference and local execution state.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `handoff_id_external uuid not null` — the Project V handoff UUID this entry corresponds to; thin bounded reference, not a planning record
- `status text not null default 'received'` — controlled vocabulary: `execution_entry_status`
- `received_at timestamptz not null default now()` — when V Forge received the handoff
- `execution_started_at timestamptz null` — when execution actually became active
- `execution_completed_at timestamptz null` — when execution completed or was formally closed
- `scope_summary text null` — brief V Forge-side summary of what execution scope was received; not a copy of planning content, but a bounded operational note
- `notes text null`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- unique: `(project_id, handoff_id_external)` — one execution entry per Project V handoff per project
- `status` must use controlled vocabulary
- `execution_started_at` must not precede `received_at`
- `execution_completed_at` must not precede `execution_started_at` if both are present

**Indexes:**
- unique index on `(project_id, handoff_id_external)`
- index on `(project_id, status, updated_at desc, id)`
- index on `(project_id, received_at desc, id)`

**Status atomicity rule:**
- When status transitions to `active`, `execution_started_at` must be set in the same transaction if not already set
- When status transitions to `completed` or `closed`, `execution_completed_at` must be set in the same transaction if not already set

**Mutability:**
- `status` transitions via governed path
- `scope_summary`, `notes` may be updated
- `handoff_id_external` must not change after creation

---

### 20. `ExecutionFinding`

**Purpose:** A bounded finding produced during execution. Records a specific finding
scoped to an active execution entry. Findings are execution-originated and bounded —
they must not become a shadow planning system.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `execution_entry_id uuid not null references ExecutionEntry(id)`
- `finding_type text not null` — controlled vocabulary: `execution_finding_type`
- `status text not null default 'open'` — controlled vocabulary: `execution_finding_status`
- `title text not null` — short description of the finding
- `description text not null` — bounded description of what was found
- `return_to_planning_id uuid null references ReturnToPlanning(id)` — populated when finding has been formally returned; set atomically when `status` transitions to `returned`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- `execution_entry_id` must reference an entry belonging to the same `project_id`
- `finding_type` and `status` must use controlled vocabularies
- `title` and `description` must be non-empty
- if `status = 'returned'`, `return_to_planning_id` must be non-null
- if `return_to_planning_id` is not null, it must reference a record belonging to the same `project_id`

**Indexes:**
- index on `(project_id, execution_entry_id, status, created_at desc, id)`
- index on `(project_id, finding_type, status, created_at desc, id)`
- index on `(project_id, status, created_at desc, id)`

**Mutability:**
- `status` transitions via governed path; `return_to_planning_id` must be set atomically when status transitions to `returned`
- `description` may be amended; `title` may be corrected
- finding records are not deleted — they are `invalidated` through a status transition when determined inapplicable

---

### 21. `ReturnToPlanning`

**Purpose:** Records that a finding or condition was formally returned to Project V
for planning reconsideration. The schema representation of the V Forge-to-Project V
return path.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `execution_entry_id uuid not null references ExecutionEntry(id)`
- `return_reason text not null` — bounded description of why planning reconsideration is required
- `returned_at timestamptz not null default now()`
- `acknowledged_at timestamptz null` — optionally set when Project V acknowledges the return
- `notes text null`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- `execution_entry_id` must reference an entry belonging to the same `project_id`
- `return_reason` must be non-empty
- `acknowledged_at` must not precede `returned_at` if both are present

**Indexes:**
- index on `(project_id, execution_entry_id, returned_at desc, id)`
- index on `(project_id, returned_at desc, id)`

**Mutability:**
- `acknowledged_at`, `notes` may be updated
- `return_reason` and `returned_at` must not change after creation
- no delete in first pass

**Boundary note:** `ReturnToPlanning` records what V Forge returned and why.
It does not carry full execution state upstream. It does not transfer execution truth
ownership. V Forge remains the owner of execution history even after a return record exists.

---

### 22. `MaintenanceRecord`

**Purpose:** Records maintenance activity performed on a V Forge execution asset
(a surface, a page, or a release). Preserves maintenance history for execution
continuity.

**Fields:**

- `id uuid primary key`
- `project_id uuid not null references Project(id)`
- `maintenance_type text not null` — controlled vocabulary: `maintenance_type`
- `asset_type text not null` — the type of asset maintained; allowed values: `surface`, `page`, `release`
- `asset_id uuid not null` — ID of the maintained asset; must belong to the same `project_id`
- `performed_by text not null` — actor or agent identifier; free-text in first pass
- `performed_at timestamptz not null`
- `outcome_summary text null` — brief description of what was done and the result
- `execution_entry_id uuid null references ExecutionEntry(id)` — optional link to the execution entry this maintenance was performed under
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

**Constraints:**
- `maintenance_type` must use controlled vocabulary
- `asset_type` must be one of: `surface`, `page`, `release`
- `asset_id` is a polymorphic reference; the referenced record must belong to the same `project_id`; enforced at application layer
- if `execution_entry_id` is not null, it must reference an entry belonging to the same `project_id`
- `performed_by` must be non-empty

**Indexes:**
- index on `(project_id, asset_type, asset_id, performed_at desc, id)`
- index on `(project_id, maintenance_type, performed_at desc, id)`
- index on `(project_id, performed_at desc, id)`

**Mutability:**
- `outcome_summary` may be updated
- `performed_at`, `maintenance_type`, `asset_type`, `asset_id` must not change after creation
- no delete in first pass

---

## Cross-Family Relationship Rules

### 1. Same-project integrity rule
Where one V Forge record references another, both must belong to the same `project_id`.
There are no exceptions in first pass. Cross-project content graph connections are forbidden
per system invariant 8.

### 2. Surface-type compatibility rule
Record families that reference a `Surface` impose a surface type constraint on that reference:
- `Page.surface_id` must reference a `website` surface
- `Release.surface_id` must reference a `github_repo` surface
- `Video.surface_id` must reference a `youtube_channel` surface
- `SocialPost.surface_id` must reference a `social_profile` surface
- `NewsletterIssue.surface_id` must reference a `newsletter` surface
- `StorePublication.store_surface_id` must reference a `store_listing` surface

### 3. Content graph integrity rule
All content graph records (`Page`, `Topic`, `Entity`, `InternalLink`, `PageTopic`,
`PageEntity`, `ContentCluster`) must be project-scoped and must not connect across
projects. Junction records must only join records from the same project.

### 4. Execution continuity chain rule
`ExecutionFinding` records reference `ExecutionEntry` records.
`ReturnToPlanning` records reference `ExecutionEntry` records.
`ExecutionFinding.return_to_planning_id` references `ReturnToPlanning` where the finding
has been formally returned. All three record families must belong to the same `project_id`.

### 5. Polymorphic reference rule
Where a record carries a polymorphic `asset_id` or `source_content_id` field (i.e., a UUID
reference whose target type is identified by a companion type field), the application layer
must enforce that the referenced record belongs to the same `project_id`. Database-layer
enforcement of polymorphic references is out of scope for first pass but must be enforced
at the application layer.

### 6. Distribution action source validity rule
`DistributionAction.source_content_id` must reference a record that exists in V Forge schema
for the corresponding `source_content_type`. The valid source record families are:
- `source_content_type = 'page'` → `Page`
- `source_content_type = 'release'` → `Release`
- `source_content_type = 'video'` → `Video`
- `source_content_type = 'newsletter_issue'` → `NewsletterIssue`

---

## Transaction and Atomicity Notes

### 1. Status + timestamp atomicity
Where a status transition requires a timestamp (e.g., `ExecutionEntry` transitions to `active`
setting `execution_started_at`, or `StorePublication` transitions to `published` setting
`published_at`), the status change and timestamp must be written in the same transaction.

### 2. Finding + ReturnToPlanning atomicity
When an `ExecutionFinding` status transitions to `returned`, the `ReturnToPlanning` record
it references must already exist or be created in the same transaction. The `return_to_planning_id`
must be set atomically with the status transition. An `ExecutionFinding` in `returned` status
with a null `return_to_planning_id` is an integrity violation.

Required operation order within the transaction: `ReturnToPlanning` must be inserted
before the `ExecutionFinding` update is applied. Because `ExecutionFinding.return_to_planning_id`
is a foreign key to `ReturnToPlanning`, the referenced record must exist at constraint
evaluation time. Attempting to update `ExecutionFinding` before inserting `ReturnToPlanning`
within the same transaction will fail the FK constraint.

### 3. Snapshot immutability
`SurfaceSnapshot` and `PublicationEvent` records are immutable append-only records.
No update path is permitted for these families.

### 4. Release immutability posture
`Release` records represent versioned immutable artifacts. `version_tag` and `published_at`
must not change after creation. Corrections to `changelog_summary` and `release_name` are
permitted but should be treated with care.

---

## Extension Hooks

The following are named extension attachment points. They must not be pre-built into
first-pass schema as empty columns or speculative junction tables.

- **Engagement metrics per DistributionAction** — attach to `DistributionAction` when cross-surface performance tracking is scoped and the VEDA signal boundary is clearly designed
- **Deep YouTube metadata** — attach to `Video` via `youtube_video_id` as anchor; add tags, chapters, thumbnail URL, end screens when YouTube workflow modeling is scoped
- **Social engagement metrics** — attach to `SocialPost` when social analytics modeling is scoped
- **Newsletter subscriber management** — attach to newsletter `Surface` via new related record families when full email operations are scoped
- **Content scoring** — attach to `Page` with computed score fields when scoring methodology is defined
- **Experimentation / optimization** — attach to `Page` with experiment and variant references; explicitly deferred per `v-forge.md`
- **Advanced content graph features** — entity relationship modeling beyond page-entity junctions, deeper topic hierarchy; attach to existing `Topic` and `Entity` records
- **SaaS / runtime / commercial truth** — explicitly deferred; must not be designed into base schema

Extension hooks do not justify adding nullable columns or empty junction tables now.
The extension point is the existing record family. Future extension adds new records or columns
through governed schema expansion review.

---

## Anti-Drift Rules

V Forge schema has drifted from this specification if:

### 1. Planning truth appears
`Project` carries planning structure, readiness state, orchestration stage, or any Project V
planning field beyond the minimum identity anchor. `ExecutionEntry` replicates Project V
handoff content rather than referencing it by ID. `ExecutionFinding` becomes a shadow
planning record.

### 2. Observatory truth appears
Any record family stores raw SERP data, GA4 observations, Search Console data, keyword
intelligence, or VEDA observatory data as canonical V Forge truth.

### 3. Execution intelligence becomes stored observatory data
Results of crossing the content graph against VEDA signal are stored as a permanent record
family resembling VEDA observatory tables. Execution intelligence is a query-time computation,
not a stored first-pass record family.

### 4. Cross-project content graph connections appear
Any junction record (`PageTopic`, `PageEntity`, `InternalLink`, `ContentCluster`) connects
records from different projects. This is a structural integrity failure per system invariant 8.

### 5. Light-tracked surfaces become deeply modeled without governance
`Video`, `SocialPost`, or `NewsletterIssue` expand significantly beyond their minimal first-pass
shape without a governed schema expansion review.

### 6. Extension hooks are pre-built
Empty columns, nullable foreign keys to deferred entities, or speculative junction tables for
experimentation, SaaS/runtime, advanced engagement, or other deferred domains appear in
first-pass table definitions.

### 7. Playbook routing becomes a workflow engine
`Playbook` expands to carry step sequences, action nodes, condition branches, or execution
state tracking — turning V Forge's playbook routing into a workflow orchestration system.

### 8. Delete semantics are casually introduced
Table families with no delete semantics defined in this spec begin accepting delete operations
without a governed schema expansion review defining deletion semantics and hammer coverage.

---

## Final Rule

This schema specification is intentionally explicit and bounded.

If implementation pressure suggests broadening it casually, the correct response is
governance review, not improvisation.

This document is the concrete companion to `schema-authority.md`.
If future implementation wants to diverge from the first-pass table shape, fields,
constraints, or mutation posture defined here, the divergence must be reviewed explicitly
rather than introduced by migration convenience.

---

## Human-In-The-Loop Principle

Schema detail is implementation-shaping authority.

Human review is required where schema change would:

- broaden V Forge's ownership posture
- introduce new record families or domains
- weaken multi-project integrity enforcement
- promote a light-tracked surface to deeply modeled status
- add record families that resemble planning truth or observatory truth
- introduce delete semantics on families currently restricted

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- V Forge schema is explicitly bounded to execution truth
- the `Project` record is a thin local anchor — not a replication of Project V planning state
- the content graph is the most important schema domain; cross-project contamination is forbidden
- `PublicationEvent` and `SurfaceSnapshot` are immutable append-only records
- `DistributionAction` is the cross-surface link mechanism; it must not store analytics
- `Playbook` routes to playbook docs; it does not model workflow step sequences
- `ExecutionEntry` references a Project V handoff by external ID; it does not copy handoff content
- `ReturnToPlanning` must be created atomically with the `ExecutionFinding` status transition to `returned`
- extension hooks are named but must not be pre-built
- delete semantics are deferred for most families; exceptions are noted per family

If implementation uses this schema to widen V Forge toward planning truth, observatory truth,
cross-project execution, or deferred domain modeling, this specification is being violated.

---

## Usage

This document should be used:

- when writing migrations for first-pass V Forge schema
- when reviewing whether a proposed column or constraint belongs in first-pass authority
- when writing API family docs that depend on exact record shape
- when reviewing whether mutation behavior remains inside governed bounds
- when checking whether implementation assumptions match current shared-root authority
- when evaluating whether a proposed schema addition requires a governed expansion review

---

## Related Docs

- `schema-authority.md`
- `controlled-vocabularies.md`
- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `human-in-the-loop-doctrine.md`
- `reporting-and-approval-model.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `../ecosystem/decisions/ADR-007-docs-are-build-spec-db-owns-operational-state.md`
- `../ecosystem/decisions/ADR-009-no-direct-database-access.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/data-boundaries.md`
- `../project-v/schema-specification.md`
