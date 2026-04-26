# First-Slice V Forge Implementation Workbench

## Purpose

This folder collects the transition-steward implementation-support documents for the first codable V Forge slice.

The slice is handoff acceptance + approval gate + activity trail, with no content execution.

---

## Status

Transition-steward workbench folder.

Not a permanent core spec folder.
Not authority doctrine by location.
Not implementation code.

These documents are drafting bases and implementation-support material. Durable, settled content should be promoted into the proper core spec locations before being treated as long-term authority.

---

## Why this folder exists

The broader `transition-steward/` folder began as a transition work area for moving the ecosystem specification from the prior multi-database framing to the current one physical Postgres database / four strict logical schemas model.

Later work added transition-control notes, provider pauses, first-project side work, and implementation-support planning. Some of those documents are now useful enough to guide implementation, but they should not remain scattered in the transition folder or be mistaken for permanent authority docs.

This folder keeps the first-slice implementation-support set together until its durable content is promoted into the appropriate core spec locations.

---

## Included documents

- `activity-trail-implementation-spec.md`
- `packet-schema-drafting-basis.md`
- `invariant-enforcement-plan.md`
- `minimum-codable-first-slice.md`
- `first-slice-implementation-task-breakdown.md`
- `coding-readiness-classification.md`

---

## Promotion posture

Do not move these documents wholesale into authority folders.

Promote by extracting settled, durable content into the correct spec homes:

| Workbench document | Likely core destination |
|---|---|
| `activity-trail-implementation-spec.md` | `ecosystem/`, adjacent to activity trail authority |
| `packet-schema-drafting-basis.md` | `interfaces/` and possibly shared governance packet/report schema docs |
| `invariant-enforcement-plan.md` | Split across `ecosystem/`, `v-forge/`, `interfaces/`, and `governance/` according to ownership |
| `minimum-codable-first-slice.md` | V Forge implementation planning / playbook or Project V implementation document |
| `first-slice-implementation-task-breakdown.md` | V Forge implementation planning / playbook or Project V implementation document |
| `coding-readiness-classification.md` | Transition/control note, then superseded once promoted specs and implementation docs exist |

---

## Anti-drift rules

- Do not treat `transition-steward/` as a core spec namespace.
- Do not treat this folder as permanent authority.
- Do not feed unrelated transition notes into first-slice coding.
- Do not broaden the first slice into content graph, archetypes, providers, VEDA, VEDA Strategy, or return-to-planning delivery.
- Do not promote transition-support language into authority docs unchanged.
- Do not delete the transition copies until references have been updated or a supersession note is added.

---

## First-slice boundary reminder

In scope:

- handoff packet validation
- persisted approval record check
- fail-closed `handoff.confirmed` activity trail write
- minimal V Forge handoff context
- minimal task lifecycle through synthetic halt
- minimal execution report
- schema credential isolation verification

Out of scope:

- content graph tables
- archetype implementation
- product, page, internal-link, or affiliate-link schemas
- Firecrawl or DataForSEO work
- VEDA signal ingestion
- VEDA Strategy interfaces
- return-to-planning delivery
- real Project V service
- desktop approval UI

---

## Use during implementation

Use these docs to produce small, intent-separated core spec promotions and implementation plans.

Once the durable content has been promoted, mark this workbench as superseded rather than letting it become a shadow authority folder.
