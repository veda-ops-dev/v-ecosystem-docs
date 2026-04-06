# Project V to V Forge Scope Update Interface

## Purpose

This document defines the interface by which Project V notifies V Forge of
scope or constraint changes that result from governed replanning, after a
handoff is already active.

It exists to answer:

```text
How does Project V communicate scope or constraint changes to V Forge after
replanning, without issuing a full new handoff, without triggering return-to-planning,
and without granting V Forge authority to reinterpret planning intent beyond
the bounded update?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the meaning of a post-replanning scope update from Project V to V Forge
- when a scope update is appropriate vs when a new handoff or return-to-planning
  is required
- what may cross through this interface and what may not
- the boundary posture that prevents a scope update from becoming an informal
  planning transfer or an open-ended execution re-authorization

---

## Out of Scope

This document does not define:

- detailed transport or implementation format
- approval mechanics beyond the boundary note below
- field-level schemas
- Project V internal replanning workflow
- V Forge internal execution adaptation workflow

Those belong in workflow, governance, and implementation-specific docs.

---

## System

- interfaces

---

## Interface Direction

**Project V → V Forge**

Project V initiates. V Forge receives the updated scope or constraint notice
and adjusts execution accordingly within the bounds of the update.

---

## Governing Systems

- **Initiator:** Project V (planning truth owner)
- **Receiver:** V Forge (execution truth owner)

---

## Core Rule

A scope update delivers the planning-side output of governed replanning to V Forge
so that V Forge's active execution reflects the revised scope or constraints.

A scope update is not:

- a new handoff (which would re-initiate the full handoff readiness and approval path)
- a return-to-planning substitute
- permission for V Forge to reinterpret planning intent beyond the bounded update
- an open-ended re-authorization of execution scope
- a mechanism for Project V to issue informal planning changes outside the
  governed replanning path

If the replanning outcome requires a fundamentally different execution scope or
target, a new handoff through `project-v-to-v-forge-handoff-interface.md` is the
correct path, not a scope update through this interface.

---

## Applicability Condition

This interface applies when:

- a governed replanning event (through `../workflows/maintenance-and-replanning-workflow.md`)
  has produced revised scope or constraints
- the revision is bounded enough to be applied to the existing active execution
  relationship without requiring a full new handoff
- V Forge has an active execution scope that the update applies to

---

## Minimum Semantic Elements

A valid scope update must be interpretable as carrying at minimum:

- which active handoff or execution scope the update applies to
- what specific scope or constraint elements have changed
- what the updated scope or constraints are
- that this update is the product of governed replanning, not informal planning mutation
- what V Forge may and may not do differently as a result of the update
- whether any current in-progress execution work is affected and what the
  disposition of that work is under the updated scope

---

## Boundary and Ownership Rule

After a valid scope update:

- V Forge remains the owner of execution truth for the active scope
- Project V remains the owner of planning and orchestration truth
- V Forge must not treat the scope update as authorization to expand execution
  beyond what the update explicitly describes
- the scope update must not be used to widen scope incrementally in ways that
  individually seem bounded but collectively exceed what governed replanning authorized
- if the scope update is ambiguous about what V Forge may now do, V Forge must
  surface that ambiguity through the execution clarification interface rather
  than resolving it by assumption

---

## Activity Trail

Activity trail integration is required for this interface.

The exact canonical action type mapping and required fields will be defined in
the activity trail integration map (`../ecosystem/activity-trail-integration-map.md`)
once that document is completed.

This stub does not finalize the activity trail action vocabulary for this interface.
Implementations must not proceed without that mapping in place.

---

## Usage

This document should be used:

- when governed replanning has produced revised scope or constraints that must
  be communicated to V Forge for an active execution scope
- when reviewing whether a proposed post-replanning communication should route
  through this interface or through a new handoff
- when verifying that V Forge has received and is executing within the updated
  scope rather than the prior scope

---

## Related Docs

- `project-v-to-v-forge-handoff-interface.md`
- `v-forge-to-project-v-return-to-planning-interface.md`
- `project-v-to-v-forge-execution-clarification-interface.md`
- `../workflows/maintenance-and-replanning-workflow.md`
- `../project-v/v-forge-integration.md`
- `../ecosystem/cross-system-boundaries.md`
- `../governance/approval-and-escalation-model.md`
