# First-Slice V Forge Spec Promotion Map

## Purpose

This document maps the first-slice V Forge implementation workbench documents to their proper long-term spec destinations.

It exists to prevent `transition-steward/` from becoming a shadow authority namespace and to keep promotion of durable implementation content small, intentional, and reviewable.

---

## Status

Transition-steward control note.

Not authority doctrine.
Not implementation code.
Not a permanent core spec document.

Use this document to guide promotion work. Once the mapped content has been promoted and references have been updated, this document may be marked superseded.

---

## Source Workbench

Current workbench folder:

`transition-steward/first-slice-v-forge-implementation/`

The workbench contains implementation-support and drafting-basis documents for the first codable V Forge slice:

- handoff acceptance
- approval gate
- activity trail
- minimal V Forge handoff context
- minimal task lifecycle
- minimal execution report
- schema credential isolation verification

The workbench documents are useful, but their folder location does not make them authoritative.

---

## Promotion Principles

1. Promote durable content into the owning spec area.
2. Do not move transition-support docs wholesale into authority folders.
3. Preserve authority boundaries: `ecosystem/`, `interfaces/`, `governance/`, `v-forge/`, `project-v/`, `veda/`, and `veda-strategy/` each own only their proper scope.
4. Keep implementation playbooks distinct from authority doctrine.
5. Keep commits separated by intent.
6. Leave workbench docs in place until references are updated or supersession notes are added.

---

## Promotion Map

| Workbench document | Long-term target | Treatment | Status |
|---|---|---|---|
| `activity-trail-implementation-spec.md` | `ecosystem/activity-trail-implementation.md` | Extract durable activity trail storage, write-helper, fail-open/fail-closed, DLQ, first-pass scope, and `ecosystem_trail_writer` rules. | **Complete** — landed at `ecosystem/activity-trail-implementation.md`. ADR-013 and `db-posture.md` amendment are in place. Workbench source is now derivation history. |
| `packet-schema-drafting-basis.md` | 'interfaces/packet-schema-reference.md' or targeted updates to interface/governance docs | Extract mature structural packet constraints for handoff, return-to-planning, approval requests, and governed reports. Keep semantic sufficiency warnings intact. | Pending |
| `invariant-enforcement-plan.md` | Split across `ecosystem/`, `v-forge/`, `interfaces/`, and `governance/` | Extract only settled enforcement mappings into the owning docs. Do not promote human-governance-only commentary as mechanical guarantees. | Pending |
| `minimum-codable-first-slice.md` | 'v-forge/playbooks/first-slice-governance-proving-slice.md' | Convert into a V Forge implementation playbook. Preserve slice boundary and out-of-scope list. Do not make it authority doctrine. | Pending |
| `first-slice-implementation-task-breakdown.md` | 'v-forge/playbooks/first-slice-task-breakdown.md' | Convert into an engineering task plan/playbook. Preserve task order, dependencies, acceptance criteria, and test plan. | Pending |
| `coding-readiness-classification.md` | Remain in workbench until superseded | Keep as transition-control/readiness classification. Supersede after promoted specs and playbooks exist. | Pending |

---

## Recommended Promotion Order

### 1. Activity trail implementation

Promote first because it is concrete, foundational, and shared by the first slice.

Target:

'ecosystem/activity-trail-implementation.md'

Extract:

- event granularity rules
- service-layer write rule
- fail-open versus fail-closed behavior
- fail-closed event set: `approval.request`, `approval.decide`, `handoff.confirmed`
- minimal `ecosystem.activity_trail` table
- required indexes
- minimal `ecosystem.activity_trail_dlq` table
- `ecosystem_trail_writer` role boundary
- first-pass exclusions: no compaction table, no event bus, no live subscription

### 2. Packet schema reference

Promote after activity trail implementation because packet validators depend on durable packet-shape rules.

Likely target:

'interfaces/packet-schema-reference.md'

Alternative: targeted updates to the specific interface/governance docs if review determines a shared packet reference would duplicate too much authority.

### 3. V Forge first-slice playbook

Promote implementation planning into `v-forge/playbooks/` after the shared ecosystem/interface pieces exist.

Targets:

- 'v-forge/playbooks/first-slice-governance-proving-slice.md'
- 'v-forge/playbooks/first-slice-task-breakdown.md'

### 4. Enforcement mapping cleanup

Promote selected enforcement mappings into owning docs only after the concrete specs are in place.

Potential destinations:

- `ecosystem/db-posture.md`
- 'ecosystem/activity-trail-implementation.md'
- 'interfaces/packet-schema-reference.md'
- `governance/approval-mechanics-seam-model.md`
- `interfaces/desktop-governance-and-gating-model.md`
- `v-forge/system-invariants.md`

### 5. Supersession cleanup

After durable content is promoted:

- update references from old workbench paths to promoted locations
- add supersession notes to workbench docs where appropriate
- update `../transition-plan.md` only if the control spine changes
- leave derivation history available until it is no longer useful

---

## Non-Promotion Rules

Do not promote the following into core authority as part of first-slice work:

- content graph tables
- archetype implementation
- product/page/internal-link/affiliate-link schemas
- Firecrawl or DataForSEO provider work
- VEDA signal ingestion
- VEDA Strategy contracts
- return-to-planning delivery
- real Project V service behavior
- desktop approval UI behavior
- autonomous agent behavior beyond synthetic halt

These are later slices or separate workstreams.

---

## Current Next Step

Promote `activity-trail-implementation-spec.md` into an ecosystem-owned implementation spec:

'ecosystem/activity-trail-implementation.md'

This should be a focused extraction, not a rewrite of the full activity trail doctrine.