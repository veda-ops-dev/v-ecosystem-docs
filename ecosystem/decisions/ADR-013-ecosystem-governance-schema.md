# ADR-013: Ecosystem Governance Schema for Shared Activity Trail

## Status
Accepted

## Date
2026-04-26

## Context

ADR-012 established one physical PostgreSQL database with four schemas, one per bounded system:

- `project_v`
- `veda`
- `veda_strategy`
- `v_forge`

That decision remains correct for bounded-system canonical truth. Project V owns planning truth, VEDA owns observatory truth, VEDA Strategy owns derived strategic intelligence, and V Forge owns execution truth.

The ecosystem activity trail creates a different kind of persistence need. It is not planning truth, observatory truth, derived strategic intelligence, or execution truth. It is a shared governance artifact used to make cross-system actions, approvals, handoffs, delivery confirmations, budget stops, and lifecycle events auditable.

Assigning the ecosystem activity trail to any one bounded-system schema would blur ownership:

- `project_v.activity_trail` would make Project V appear to own ecosystem-wide governance records.
- `veda.activity_trail` would make the observatory appear to own non-observatory governance records.
- `veda_strategy.activity_trail` would put governance trail truth inside the derived-strategy system.
- `v_forge.activity_trail` would make execution appear to own approval, planning, and observatory governance events.

The activity trail therefore needs a persistence home that is shared for governance without becoming a fifth bounded system or a general-purpose shared data store.

## Decision

The V Ecosystem admits a fifth PostgreSQL schema named `ecosystem` as a constrained governance infrastructure schema.

The `ecosystem` schema is not a bounded-system schema. It does not own planning truth, observatory truth, derived strategic intelligence, or execution truth. It exists to hold shared ecosystem-governance artifacts that cannot be correctly owned by any one bounded system.

Initial permitted scope is limited to:

- `ecosystem.activity_trail`
- `ecosystem.activity_trail_dlq`

No other tables, views, or persistent stores may be added to the `ecosystem` schema without a later ADR or equivalent governed authority update.

## Role and Access Model

The shared trail write path is implemented through a dedicated role:

- `ecosystem_trail_writer`

That role may have:

- `INSERT` on `ecosystem.activity_trail`
- `INSERT` on `ecosystem.activity_trail_dlq`

That role must not have:

- `UPDATE` on ecosystem trail tables
- `DELETE` on ecosystem trail tables
- `SELECT` on the `ecosystem` schema
- write access to any bounded-system schema

The four bounded-system service roles may be granted `ecosystem_trail_writer` for the sole purpose of writing activity trail records.

### SELECT posture for bounded-system services

Bounded-system service roles must not receive SELECT grants on `ecosystem.activity_trail`
or `ecosystem.activity_trail_dlq` for general use.

Service-layer verification of trail record existence (for example, confirming that a
fail-closed write succeeded within the same transaction) must be achieved through the
write result or transaction outcome, not through a follow-up SELECT query. A service
that needs to confirm its own write must rely on the database's write acknowledgement,
not a read-back.

### Governance replay and audit reads

Governance replay and audit query access requires a separate read role:

- Suggested name: `ecosystem_governance_reader`
- Permitted: `SELECT` on `ecosystem.activity_trail`
- Must not have: `INSERT`, `UPDATE`, `DELETE`, or access to any bounded-system schema
- This role is not granted to bounded-system services

### DLQ draining, compaction, retention, and repair

Dead-letter draining, compaction, retention enforcement, and repair operations require
a separate maintenance role with elevated privileges:

- Suggested name: `ecosystem_governance_operator`
- Permitted: `SELECT`, `INSERT`, `UPDATE`, `DELETE` on `ecosystem.activity_trail` and
  `ecosystem.activity_trail_dlq` as needed for operational work
- Must not have: write access to any bounded-system schema
- This role is not granted to bounded-system services

The exact privileges for `ecosystem_governance_reader` and `ecosystem_governance_operator`
are an infrastructure concern to be established before governance replay or DLQ operations
go live. Neither role may be granted to bounded-system services under any circumstances.

## Migration Ownership

The `ecosystem` schema is not owned by Project V, VEDA, VEDA Strategy, or V Forge.

Migrations for the `ecosystem` schema are owned by the ecosystem infrastructure / operations layer. Bounded-system migration runners must not mutate the `ecosystem` schema unless explicitly operating under that infrastructure migration authority.

This preserves the migration ownership rule for bounded systems while acknowledging that shared governance infrastructure needs its own migration owner.

## Boundary Rules

The `ecosystem` schema is a governed exception to the normal bounded-system schema model.

This exception does not allow:

- casual cross-system reads
- shared canonical truth storage
- provider payload archives
- planning records
- observatory records
- strategic intelligence records
- execution records
- convenience tables that do not fit elsewhere

The `ecosystem` schema must remain narrow. Its existence must not weaken the four bounded-system ownership boundaries created by ADR-012.

## Consequences

- `ecosystem/db-posture.md` must be amended to describe four bounded-system schemas plus one constrained ecosystem governance schema.
- Activity trail implementation specs may use `ecosystem.activity_trail` and `ecosystem.activity_trail_dlq` after this ADR and the `../db-posture.md` amendment are in place.
- First-slice V Forge implementation planning may rely on the ecosystem activity trail as the shared governance trail, not as a system-specific operational log.
- Per-system operational logs or temporary per-system activity tables may exist only as system-internal logs. They do not replace the ecosystem activity trail as the cross-system governance surface.

## Non-Consequences

This decision does not create a fifth bounded system.

This decision does not allow systems to treat the `ecosystem` schema as a shared application database.

This decision does not allow a bounded-system service role to read from or mutate another bounded system's schema.

This decision does not change Qdrant's posture. Qdrant remains retrieval support only and is not canonical truth or activity trail storage.

This decision does not promote transition-steward workbench docs into authority by itself. Durable implementation content still must be promoted into the proper spec locations in separate, reviewable patches.

## Risks

The main risk is that the `ecosystem` schema becomes a dumping ground for cross-system convenience state.

The mitigation is strict scope:

- initial allowed objects are only the activity trail and DLQ tables
- no additional schema objects without a further governed decision
- no broad read grants to bounded-system services
- no update/delete grants for subsystem trail writers
- separate operational credentials for governance replay and repair work

Another risk is migration ownership ambiguity. This ADR resolves that by assigning `ecosystem` schema migrations to ecosystem infrastructure / operations rather than any bounded system.

## Related Docs

- `ADR-012-single-postgres-multi-schema.md`
- `../db-posture.md`
- `../activity-trail-model.md`
- `../activity-trail-integration-map.md`
- `../cross-system-boundaries.md`
