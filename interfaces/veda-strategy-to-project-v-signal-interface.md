# VEDA Strategy to Project V Signal Interface

## Purpose

This document defines the governed interface stub for how VEDA Strategy delivers
bounded strategic signal packages to Project V for planning evaluation.

It exists to answer at a governance level:

```text
What is the governed path by which VEDA Strategy delivers strategic signal to
Project V, what does ownership look like across this interface, and what does
this interface explicitly not provide?
```

This is a governed interface stub.
Full interface contract specification is deferred to Batch K.

---

## Scope

This document governs at stub level:

- the source and destination systems for this interface
- the nature of what crosses this interface
- the access model at a high level
- the signal ownership rule
- the boundary and authority rule after delivery
- what this interface does not provide
- explicit statements on planning system authority

This document does not yet govern:

- detailed delivery package field specifications
- transport mechanics, queue semantics, or retry behavior
- activity trail action type mappings for this interface
- approval workflow mechanics specific to this interface
- degraded-mode and recovery behavior details
- cost and accounting posture

Those belong in the full interface contract to be specified in Batch K.

---

## System

- interfaces

---

## Stub Status

This interface is governed but not yet fully specified.

The governed path exists. The boundary and ownership rules are settled.
Implementations must not cross this boundary outside this governed interface.
Full specification of delivery mechanics, package contents, and activity trail
requirements is deferred to Batch K.

---

## Source and Destination

**Source system:** VEDA Strategy (`veda_strategy`)
**Destination system:** Project V (`project_v`)

---

## What Crosses This Interface

VEDA Strategy delivers bounded strategic signal packages to Project V through
this interface.

A strategic signal package on this interface carries VEDA Strategy's derived
intelligence outputs — such as scored opportunity candidates, strategic-level
gap signals, clustering outputs, and competitive analysis conclusions — packaged
for planning evaluation by Project V.

The package contains VEDA Strategy's canonical derived records. It does not
contain raw VEDA observatory truth. VEDA Strategy derives intelligence from VEDA's
observatory records; it does not forward those records to Project V through this
interface.

---

## Access Model

This interface uses VEDA Strategy-initiated delivery.

VEDA Strategy determines when a strategic signal package is ready and relevant
for Project V's planning evaluation, and initiates delivery through this
governed path.

Project V receives the package through this interface. It does not query VEDA
Strategy directly for arbitrary strategic intelligence on demand.

The specific mechanics of delivery initiation, receipt confirmation, and
re-delivery are deferred to the full contract specification in Batch K.

---

## Signal Ownership Rule

VEDA Strategy owns the strategic signal package it delivers through this interface.

Delivery of a strategic signal package to Project V does not transfer ownership
of VEDA Strategy's derived records to Project V. Project V receives a bounded
package for planning evaluation. It does not acquire canonical ownership of the
underlying VEDA Strategy records.

Project V's local copy or planning-side reference to a delivered strategic signal
package is a planning-side reference — not a duplicate of VEDA Strategy's
canonical derived output.

VEDA Strategy's derived intelligence remains in `veda_strategy.*`.
Project V's planning decisions informed by that intelligence remain in `project_v.*`.
These are distinct canonical records in distinct schemas.

---

## What This Interface Does Not Provide

This interface does not provide:

- raw VEDA observatory records — those remain in `veda.*` and are owned by VEDA
- planning decisions — Project V makes its own planning decisions after evaluating
  the delivered signal
- approval or authorization for any specific planning action
- execution instructions of any kind
- VEDA Strategy's full derivation history or all records in `veda_strategy.*`
- a mechanism for Project V to query VEDA Strategy's internal state directly

---

## Boundary and Authority Rule

After a valid strategic signal delivery through this interface:

- VEDA Strategy remains the owner of the strategic signal package and the
  derived records it contains
- Project V remains the planning system of record
- Project V evaluates the delivered signal and makes its own planning determination
- VEDA Strategy does not make planning decisions and does not constrain what
  planning determination Project V reaches

Strategic signals from VEDA Strategy inform Project V's planning evaluation.
They do not replace it. A strong strategic signal does not constitute a
planning decision, a project creation event, or an approval.

Project V remains the governed authority for what gets planned, prioritized,
approved, and handed off.

---

## Related Docs

- `../veda-strategy/veda-strategy.md`
- `../veda-strategy/data-boundaries.md`
- `../veda-strategy/schema-authority.md`
- `../ecosystem/cross-system-boundaries.md`
- `../interfaces/data-boundaries.md`
- `../project-v/project-v.md`
- `veda-strategy-to-v-forge-signal-interface.md`
- `veda-to-project-v-signal-interface.md`
