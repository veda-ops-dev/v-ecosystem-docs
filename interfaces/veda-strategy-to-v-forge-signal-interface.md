# VEDA Strategy to V Forge Signal Interface

## Purpose

This document defines the governed interface stub for how VEDA Strategy delivers
bounded execution-relevant strategic signals to V Forge.

It exists to answer at a governance level:

```text
What is the governed path by which VEDA Strategy delivers execution-relevant
strategic signal to V Forge, what does ownership look like across this interface,
and what does this interface explicitly not provide?
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
- explicit statements on execution system authority

This document does not yet govern:

- detailed delivery package field specifications
- transport mechanics, queue semantics, or retry behavior
- activity trail action type mappings for this interface
- approval workflow mechanics specific to this interface
- degraded-mode and recovery behavior details
- cost and accounting posture
- the relationship between this interface and V Forge's active evidence-query layer

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
**Destination system:** V Forge (`v_forge`)

---

## What Crosses This Interface

VEDA Strategy delivers bounded execution-relevant strategic signal packages to
V Forge through this interface.

A strategic signal package on this interface carries VEDA Strategy's derived
intelligence outputs that are relevant to in-scope execution — such as strategic-level
gap signals, competitive analysis conclusions, and opportunity signals pertaining
to work already within the project's execution scope.

The package contains VEDA Strategy's canonical derived records. It does not
contain raw VEDA observatory truth. VEDA Strategy derives intelligence from VEDA's
observatory records; it does not forward those records to V Forge through this
interface.

This interface carries signals relevant to execution intelligence within scope.
It does not carry planning directives, scope expansion instructions, or signals
that would alter what V Forge is approved to execute.

---

## Access Model

This interface uses VEDA Strategy-initiated delivery.

VEDA Strategy determines when a strategic signal package is relevant to V Forge's
execution intelligence and initiates delivery through this governed path.

V Forge receives the package through this interface. It does not query VEDA
Strategy directly for arbitrary strategic intelligence on demand.

The specific mechanics of delivery initiation, receipt confirmation, and
re-delivery are deferred to the full contract specification in Batch K.

---

## Signal Ownership Rule

VEDA Strategy owns the strategic signal package it delivers through this interface.

Delivery of a strategic signal package to V Forge does not transfer ownership
of VEDA Strategy's derived records to V Forge. V Forge receives a bounded
package for use in execution intelligence. It does not acquire canonical ownership
of the underlying VEDA Strategy records.

V Forge's local use of or reference to a delivered strategic signal package
is an execution-side reference — not a duplicate of VEDA Strategy's canonical
derived output.

VEDA Strategy's derived intelligence remains in `veda_strategy.*`.
V Forge's execution intelligence derived from that input remains in `v_forge.*`.
These are distinct canonical records in distinct schemas.

---

## What This Interface Does Not Provide

This interface does not provide:

- raw VEDA observatory records — those remain in `veda.*` and are owned by VEDA
- execution decisions — V Forge makes its own execution decisions after evaluating
  the delivered signal
- authorization to expand execution scope beyond what Project V has approved
- execution commands or directives of any kind
- planning instructions or planning-level decisions
- VEDA Strategy's full derivation history or all records in `veda_strategy.*`
- a mechanism for V Forge to query VEDA Strategy's internal state directly

---

## Boundary and Authority Rule

After a valid strategic signal delivery through this interface:

- VEDA Strategy remains the owner of the strategic signal package and the
  derived records it contains
- V Forge remains the execution system of record
- V Forge evaluates the delivered signal as one input to its execution intelligence
  and makes its own execution determination
- VEDA Strategy does not make execution decisions and does not authorize scope
  changes through signal delivery

Strategic signals from VEDA Strategy inform V Forge's execution intelligence.
They do not replace it. A strategic signal does not constitute an execution
command, a scope change, or an approval.

V Forge remains the governed authority for what gets executed within the
approved scope. Changes to execution scope require the governed planning path
through Project V, not a strategic signal from VEDA Strategy.

---

## Related Docs

- `../veda-strategy/veda-strategy.md`
- `../veda-strategy/data-boundaries.md`
- `../veda-strategy/schema-authority.md`
- `../ecosystem/cross-system-boundaries.md`
- `../interfaces/data-boundaries.md`
- `../v-forge/v-forge.md`
- `veda-strategy-to-project-v-signal-interface.md`
- `veda-to-v-forge-signal-interface.md`
