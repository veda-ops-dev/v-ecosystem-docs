# VEDA to V Forge Signal Interface

## Purpose

This document defines the interface by which VEDA delivers a bounded baseline
execution-startup signal package to V Forge at the initialization of an active
execution scope.

It exists to answer:

```text
What does the VEDA-initiated startup signal delivery layer provide to V Forge,
what must the baseline package carry, when does delivery occur, what makes it
valid, how is receipt confirmed, and how does this layer stay distinct from the
active evidence-query layer?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the access model for VEDA-initiated startup signal delivery to V Forge
- what triggers this delivery and when it occurs in the execution lifecycle
- the minimum semantic contents of a valid baseline startup signal package
- receipt confirmation requirements
- what this delivery layer does and does not provide
- the explicit distinction from the active evidence-query layer
- degraded-mode and recovery behavior
- activity trail requirements for startup delivery events
- cost and accounting posture

---

## Out of Scope

This document does not define:

- V Forge-initiated active evidence queries during execution — that is governed by
  `v-forge-evidence-access-contract.md`
- VEDA internal signal production or observatory workflow
- V Forge internal execution intelligence workflow
- full approval policy — that belongs in governance docs
- the forward handoff transfer — that is `project-v-to-v-forge-handoff-interface.md`
- return-to-planning when execution findings require planning reconsideration —
  that is `v-forge-to-project-v-return-to-planning-interface.md`
- transport-layer implementation details or API schemas

---

## System

- interfaces

---

## Core Rule

VEDA delivers a bounded baseline execution-startup signal package to V Forge at the
initialization of a specific handed-off execution scope. Delivery is VEDA-initiated
and requires V Forge receipt confirmation.

This delivery establishes V Forge's baseline execution intelligence context for the
scope. It does not transfer observability ownership to V Forge. It does not authorize
arbitrary ongoing evidence access. It does not replace the active evidence-query layer
for mid-execution evidence needs.

---

## Access Model

**This interface uses VEDA-initiated push delivery with V Forge receipt confirmation.**

VEDA initiates this delivery. V Forge does not poll or query this interface. Delivery
is not complete until V Forge confirms receipt.

This interface is **tied to a specific handoff scope and a specific execution lifecycle
moment**: the initialization of V Forge's execution intelligence context after a
Project V handoff has been confirmed. This is not a general-purpose signal streaming
channel. It is not an arbitrary evidence access path. It fires once per execution
scope initialization.

This interface is **not** the active evidence-query layer. V Forge active queries
during execution are governed by `v-forge-evidence-access-contract.md`. See the
Distinction from Active Query Layer section below.

---

## When Delivery Occurs

Delivery on this interface is triggered at execution scope initialization — the point
at which:

- a Project V → V Forge handoff has been confirmed (through
  `project-v-to-v-forge-handoff-interface.md`)
- V Forge is about to begin execution work on the handed-off scope
- V Forge needs baseline execution intelligence context to operate effectively

VEDA delivers the bounded startup package at this moment. The delivery is scoped
to the same project and execution context as the confirmed handoff.

This is a defined lifecycle moment, not a vague "startup" phase. If the execution
scope is reinitiated after a return-to-planning and new handoff cycle, a new startup
signal delivery applies for the new scope.

---

## Startup Signal Package Semantics

A valid VEDA → V Forge startup signal package must be interpretable as carrying
at minimum the following semantic fields.

### Required semantic fields

**Package / delivery identity**
A stable identifier for this startup signal delivery event. Required for activity
trail records, receipt confirmation, de-duplication, and re-delivery handling.
Must remain stable across re-delivery attempts unless the package is regenerated
due to a materially changed basis.

**Originating handoff / execution scope reference**
A reference to the confirmed Project V → V Forge handoff that triggered this
delivery. This ties the startup package to a specific governed execution context
and prevents out-of-scope or orphaned signal deliveries.

**Bounded signal scope**
What class or domain of signal this package represents — the specific signal
classes relevant to this execution scope (e.g., search performance signal, keyword
signal, content structure signal). This is bounded to what is relevant to the
handed-off execution scope, not VEDA's full observatory.

**Execution-startup relevance statement**
Why this package applies now — a bounded statement of what execution intelligence
context this package is intended to establish. This makes the curation rationale
explicit and prevents the package from being treated as an all-purpose signal dump.

**Observation or capture timestamps**
When the underlying evidence or signal was gathered or observed. Distinct from the
delivery timestamp. Both must be present so V Forge can assess how current the
signal context is.

**Delivery timestamp**
When VEDA initiated this delivery.

**Freshness classification**
VEDA's assessment of the signal freshness for this package — fresh, aging, stale,
or uncertain. V Forge must not assume all startup signal is equally current. VEDA
must not deliver a package it knows to be expired without flagging the freshness state.

**Trust and provenance metadata**
The source or provider origin of the evidence, VEDA's trust classification for each
signal class included, and any known limitations or uncertainty. V Forge must not
treat all included signal as equally trustworthy.

**Bounded signal findings or evidence references**
The actual signal content relevant to this execution scope — bounded to what V Forge
needs to initialize its execution intelligence context. This is not a dump of all
available VEDA evidence for the project. VEDA is responsible for curating what is
execution-startup relevant.

**Known execution-facing caveats, limits, or uncertainty markers**
Any known gaps, provisional classifications, or areas where signal confidence is
limited. V Forge should not proceed as though the startup context is complete and
authoritative in areas where VEDA has flagged uncertainty.

**Package revision posture** (when applicable)
Whether this package is the original startup delivery or a revision. If a revision,
the prior delivery identity should be referenced. Revisions may occur if the
execution scope is re-initiated after a recall or replanning cycle.

### What the package must not contain

A startup signal package must not contain:

- VEDA's full observatory state or unrestricted evidence archives
- planning decisions or instructions about what V Forge should build
- signal from a different project scope than the delivery is tied to
- fabricated or provenance-anonymous evidence presented as clean signal
- authorization for V Forge to mirror VEDA's observatory records locally as canonical truth
- an answer to arbitrary future execution evidence questions — this is the startup
  context only

---

## Validity Conditions

A startup signal package is valid only when all of the following are true:

- the package is tied to a confirmed handoff or execution scope, identified by the
  originating handoff / execution scope reference
- the package is bounded to execution-startup relevance — it is curated for what
  V Forge needs to initialize its execution intelligence context, not a general
  VEDA state dump
- all required semantic fields are present
- freshness and provenance metadata are present and honest
- the signal included is not materially stale or superseded at delivery time
- the package does not represent itself as answering arbitrary future evidence
  needs during execution — those remain in the active query layer
- the package is not fabricated, contextless, or orphaned from a real handoff

A package that fails any of these conditions must not be treated as a valid startup
signal delivery. V Forge must not use an invalid package to initialize execution
intelligence context.

---

## Boundary and Authority Rule

After a valid startup signal delivery and receipt confirmation:

- VEDA remains the owner of signal, evidence, and observability truth
- V Forge owns execution truth and execution intelligence derived from this context
- Project V retains planning truth

**Receipt of the startup signal package does not transfer observability ownership
to V Forge.**

V Forge may use the delivered signal to initialize its execution intelligence context
and to inform execution work within the approved scope. V Forge must not:

- treat the delivered package as a local canonical mirror of VEDA's observatory
- accumulate the delivered signal as a growing evidence archive within V Forge
- use the delivered package as justification for acquiring new observatory responsibilities
- present the delivered signal to Project V as though V Forge originated it

VEDA curates and delivers. V Forge uses the context to execute. The delivered signal
remains VEDA-originated evidence with VEDA's trust and provenance classification.

---

## Distinction from the Active Evidence-Query Layer

This interface and `v-forge-evidence-access-contract.md` are complementary layers
governing different interaction classes on the same seam. They must not be conflated.

| Dimension | This interface (startup layer) | Evidence access contract (query layer) |
|---|---|---|
| Initiating system | VEDA | V Forge |
| Delivery model | VEDA-initiated push | V Forge-initiated active query |
| When it applies | Execution scope initialization, tied to a confirmed handoff | During active execution, when V Forge has a specific evidence need |
| Scope | Bounded baseline context for the handed-off execution scope | On-demand bounded evidence for specific execution-time needs |
| Curation | VEDA curates what is execution-startup relevant | V Forge specifies what it needs via query type and parameters |
| Receipt | Receipt confirmation required | Query response returned immediately |
| Purpose | Establish V Forge's baseline execution intelligence context | Supplement execution with current bounded evidence as needed |

**This interface must not be used for:**
- arbitrary mid-execution evidence lookup — that is the active query layer
- replacement of V Forge active queries during execution
- repeated per-task signal provision throughout the execution lifecycle

**The active evidence-query contract must not be used as a substitute for:**
- the baseline startup context that this interface provides
- VEDA curating a coherent execution-startup signal set for the handed-off scope

Both layers are required. Neither is a substitute for the other.

---

## What This Signal Delivery Does Not Provide

A startup signal delivery through this interface does not provide:

- arbitrary execution-time evidence lookup — that is the active query layer
- open-ended observatory access during execution
- planning truth or planning direction
- execution authority beyond the approved handed-off scope
- a full local mirror of VEDA's observatory state that V Forge may treat as canonical
- a substitute for return-to-planning when execution findings require planning
  reconsideration
- a substitute for the active evidence-query contract during execution
- signal for a different project scope than the delivery is tied to

---

## Receipt Confirmation

Startup signal delivery is not complete until V Forge confirms receipt.

**What receipt confirmation means:**
V Forge acknowledges that the startup signal package has arrived and is available
for use in initializing execution intelligence context. Receipt confirmation does
not mean V Forge has processed the signal or begun execution.

**What VEDA must do if receipt confirmation is not returned:**
VEDA must not treat the delivery as complete. VEDA must retain the package for
re-delivery using the same package identity. VEDA must not silently assume the
startup context has been established.

**What V Forge must not assume:**
V Forge must not assume a startup signal delivery has occurred if it has not
confirmed receipt. If V Forge receives a delivery it has already confirmed (e.g.,
due to retry), it must handle the duplicate gracefully using the package identity.

---

## Degraded-Mode Behavior

### V Forge unavailable at delivery time

If V Forge cannot receive the delivery, VEDA must:

- not treat the delivery as confirmed
- retain the package for re-delivery using the same package identity
- record the delivery attempt and failure in the activity trail

V Forge must not assume startup context has been established without confirmed receipt.

### Receipt confirmation not returned within expected window

VEDA must treat delivery as incomplete. Same behavior as "V Forge unavailable" applies.

### Package invalid or incomplete

If V Forge receives a startup signal package that is missing required semantic fields
or fails validity conditions, V Forge must not use it to initialize execution
intelligence context. V Forge must surface the insufficiency through the governed
interruption path.

### Package becomes stale or superseded before confirmation

If the package has been delivered but not yet confirmed, and the underlying signal
has changed materially — conditions shifted, evidence invalidated, handoff scope
revised — VEDA must assess whether the package still honestly represents the
startup context.

If the basis change is material:
- VEDA should produce an updated package rather than allowing V Forge to confirm
  and use a stale startup context
- The updated package carries a new delivery identity and references the prior
  package identity as superseded
- VEDA must not silently allow a materially stale startup context to become the
  basis for execution

### Duplicate delivery / retry case

If V Forge receives a delivery it has already confirmed, V Forge must handle it
gracefully using the package identity. It must not re-initialize its execution
intelligence context as if new startup signal had arrived.

---

## Recovery Behavior

After degraded mode clears or a delivery failure is resolved:

- VEDA may re-deliver the same package using the same package identity, provided
  the signal basis has not materially changed
- If the signal basis has materially changed during the delay, a new package must
  be generated and the old package identity referenced as the prior version
- Receipt confirmation of the re-delivered package completes the startup delivery event
- VEDA must not assume a prior delivery attempt subsequently succeeded without
  confirmed receipt

---

## Activity Trail

Every startup signal delivery event on this interface must produce activity trail
records.

**Producing system:** VEDA
**Target system:** V Forge

The following events must each produce a record:

| Event | When it occurs |
|---|---|
| Delivery initiated | VEDA initiates the push delivery |
| Receipt confirmed | V Forge confirms receipt |
| Delivery failed / unconfirmed | Delivery attempt produced no confirmation |
| Re-delivery initiated | VEDA re-delivers a previously unconfirmed package |
| Package superseded / voided | Signal basis changed materially; package invalidated before confirmation |

Each event record must carry, at minimum:

- the package / delivery identity
- the originating handoff / execution scope reference
- the signal scope (what signal classes are included)
- the freshness classification of the delivered signal
- the trust / provenance classification where applicable
- the receipt confirmation status
- whether delivery is original or a retry
- whether the package has been superseded or voided, and by what

The exact canonical action type names must align with the activity trail model
(`../ecosystem/activity-trail-model.md`) and the activity trail integration map
(`../ecosystem/activity-trail-integration-map.md`). The mapping for this interface
is defined in integration map Section 4.

Startup signal deliveries that produce no activity trail records are not governed
deliveries.

---

## Cost and Accounting Posture

Startup signal packaging and delivery are governed system activity. The costs
associated with curating and delivering the startup signal package are attributable
to VEDA as the producing and initiating system.

Cost attribution must be:

- reviewable after the fact
- associated with the package identity and the originating execution scope
- captured in the activity trail where applicable

Re-delivery costs are attributed to the same startup delivery event chain, traceable
through the package identity.

---

## Signal Ownership Rule After Delivery

After a valid startup signal delivery and confirmed receipt:

- VEDA remains the canonical owner of all observatory records used to produce the package
- V Forge owns the execution intelligence it derives by crossing the delivered signal
  against the content graph
- V Forge's local representation of the delivered signal is a derivative reference,
  not a competing canonical observatory record
- V Forge must not accumulate or extend the delivered signal into a growing
  observatory archive

VEDA's delivery is the source. V Forge's execution intelligence is the derived product.
These are not the same thing.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- VEDA initiates startup signal delivery; V Forge does not poll for it
- delivery is tied to a specific confirmed handoff and a defined execution-startup moment
- the startup package establishes baseline context, not arbitrary evidence access
- receipt confirmation is required; delivery is not complete without it
- the active query layer (evidence access contract) is separate and distinct —
  this interface is not a substitute for it and the query contract is not a
  substitute for this
- V Forge does not acquire observability ownership by receiving this package
- activity trail records are required for every startup delivery event

If the interface is implemented as an arbitrary evidence streaming channel, as a
substitute for the active evidence-query contract, or as a delivery that requires
no confirmation, the doctrine is wrong.

---

## Usage

This document should be used:

- when implementing VEDA's execution-startup signal delivery to V Forge
- when implementing V Forge's startup signal receipt and confirmation
- when reviewing whether a proposed startup package is too broad, too weak, or
  missing required fields
- when evaluating whether a signal access need belongs at the startup layer or
  the active query layer
- when writing VEDA and V Forge workflow docs that involve execution-startup context

---

## Related Docs

- `v-forge-evidence-access-contract.md` *(companion active query layer — read together with this doc)*
- `project-v-to-v-forge-handoff-interface.md`
- `v-forge-to-project-v-return-to-planning-interface.md`
- `../veda/veda.md`
- `../veda/system-invariants.md`
- `../veda/observability-and-signal-role.md`
- `../v-forge/v-forge.md`
- `../v-forge/system-invariants.md`
- `../interfaces/mcp-coordination-model.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/cross-system-access-governance.md`
- `../ecosystem/activity-trail-model.md`
- `../governance/testing-and-verification-doctrine.md`
