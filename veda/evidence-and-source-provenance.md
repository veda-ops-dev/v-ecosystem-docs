# VEDA Evidence and Source Provenance

## Purpose

This document defines how VEDA preserves evidence, provenance, source trust, and uncertainty as part of its observability role.

It exists to answer:

```text
How does VEDA keep evidence traceable, source context intact, trust posture visible, and later interpretation grounded without letting summaries, signal, or convenience erase provenance?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- how evidence is preserved inside VEDA
- what provenance must remain attached to evidence and signal
- how source trust and uncertainty should be represented
- how raw evidence, structured observations, and derived interpretation must remain distinct
- what provenance drift patterns are forbidden

---

## Out of Scope

This document does not define:

- the full schema of every observatory model
- the detailed payload structure of every signal package
- the detailed operator-surface rendering of provenance
- the exact provider-specific reliability model for every source family
- the full workflow for Project V intake or planning decisions

Those belong in more specific VEDA, interface, or governance docs.

---

## System

- veda

---

## Core Rule

VEDA must preserve evidence as evidence.

It must not allow source context, trust posture, uncertainty, capture time, or derivation boundaries to disappear merely because a later summary, signal, or operator-facing surface is easier to use when provenance is hidden.

If evidence becomes detached from provenance, VEDA stops being trustworthy observability and becomes decorative confidence theater.

---

## Evidence Definition

Inside VEDA, evidence is any captured or recorded material that contributes to observatory truth.

Evidence may include:

- source items and captured external material
- raw provider payloads
- structured observation records
- evented observatory state transitions
- structural observability records
- derived outputs only when they remain explicitly identified as derived from canonical observatory records

Evidence is not defined by format alone.
It is defined by its role in supporting traceable observatory truth.

---

## Provenance Definition

Provenance is the traceable context that allows a later reader, operator, or capable LLM to understand:

- what the evidence is
- where it came from
- when it entered or was captured by the system
- how it was obtained
- what project or scope it belongs to
- what trust posture applies
- whether the current representation is raw, structured, summarized, or derived

Provenance is part of evidence integrity.
It is not optional annotation.

---

## Evidence Preservation Rule

VEDA must preserve enough evidence context that later interpretation remains reviewable and challengeable.

This means:

- captured material remains distinguishable from summaries about it
- raw provider payloads remain distinguishable from structured extracted fields
- structured observations remain distinguishable from derived interpretations
- evidence remains linked to project scope, time context, and source context

VEDA should make evidence usable.
It must not make evidence origin disappear.

---

## Source Capture Rule

Nothing important should enter durable observatory use without explicit capture or equivalent governed intake recording.

This means:

- important external material should not live only in memory, chat residue, or ad hoc notes
- capture should preserve enough identifying context to support later review
- captured material should remain tied to source type, intake time, and operator or system context where relevant

Where capture context is incomplete, disputed, or unverifiable at intake time, the captured material must not be treated as fully provenanced evidence.
The incomplete provenance must be explicitly marked as such.
VEDA must not use presentation normalization to make partially provenanced material appear fully grounded.
Provenance gaps must be flagged, not smoothed over.

Source capture exists to stop provenance decay before it starts.

---

## Minimum Provenance Rule

At minimum, evidence inside VEDA should preserve enough context to answer:

- what is this?
- where did it come from?
- when was it captured or recorded?
- what project does it belong to?
- who or what introduced it into the system?
- is this raw evidence, a structured observation, a summary, or a derived output?

If those questions cannot be answered, provenance is too weak.

---

## Source Trust Rule

VEDA must preserve source-trust posture as part of evidence handling.

This means VEDA should preserve, where relevant:

- whether the source is direct or indirect
- whether the source is provider-originated, operator-captured, system-derived, or externally referenced
- whether the source is well-grounded, weakly grounded, ambiguous, or unverified
- whether important trust-relevant uncertainty remains unresolved

VEDA must not present low-trust, weakly grounded, or ambiguous source material as though it were clean observatory truth without surfacing the relevant uncertainty.

Trust posture belongs with evidence, not only with later interpretation.

---

## Uncertainty Visibility Rule

Where evidence or interpretation carries meaningful uncertainty, that uncertainty must remain visible.

This means:

- uncertainty should not be erased during summarization
- operator-facing clarity must not come from false certainty
- signal packaging should preserve important confidence limits
- provisional interpretation must remain provisional

A cleaner presentation is not a valid reason to hide uncertainty that materially affects downstream judgment.

---

## Raw vs Structured vs Derived Rule

VEDA must preserve a clear distinction between:

### 1. Raw Evidence
Unprocessed or minimally processed captured material, such as provider payloads or source artifacts.

### 2. Structured Observation
Canonical observatory records extracted or modeled from evidence in bounded schema.

### 3. Derived Interpretation
Diagnostics, summaries, classifications, or signal derived from canonical observatory records.

These three layers must not be collapsed into one convenience blob.

A later reader must be able to tell whether they are looking at:

- original evidence
- normalized observatory truth
- or a derived view layered on top

---

## Derivation Honesty Rule

When VEDA derives summaries, diagnostics, or signals from evidence, the derivation must remain honest about its basis.

This means derived outputs should preserve, at the level required by context:

- what evidence or observatory records they depend on
- what time range or record window they depend on
- whether the output is direct or inferred
- whether important uncertainty remains

Where a derived output is itself used as input to produce a further derived output, each step in the derivation chain must remain traceable.
Multi-step derivation must not produce an output that appears directly observatory-grounded when it is several steps removed from canonical evidence.
The derivation distance from source evidence is part of the output’s provenance.

Derived output must not masquerade as raw observed reality.

---

## Time Context Rule

Evidence and provenance must preserve time context where it matters.

This includes, as appropriate:

- capture time
- valid time
- record time
- event time
- derivation window or comparison window

A timeless evidence record is usually weak evidence handling.

Time context must remain explicit enough that later readers can distinguish current, historical, and replayed or delayed material where relevant.

---

## Actor and Capture Context Rule

Where evidence enters VEDA through human, LLM, or system action, that capture context should remain attributable where relevant.

This means later review should be able to determine whether evidence or a state change was introduced by:

- a human operator
- an LLM acting through a governed path
- a system process
- an external provider or external artifact being recorded

Where evidence is captured or recorded by an LLM acting through a governed path, the LLM’s interpretive framing must remain distinguishable from the source material being captured.
LLM-introduced capture notes, summaries, or classifications must not be stored in a way that blurs them with the original source evidence.
The LLM is an actor in capture, not a source of evidence.

Attribution helps preserve trust, debugging quality, and governance reviewability.

---

## JSON and Payload Rule

Raw payload storage is allowed when it preserves supporting evidence that would otherwise be lost.

But:

- raw payloads must remain supporting evidence, not the only place where hot-path meaning lives
- fields required for querying, validation, filtering, or stable logic should be promoted into explicit structure
- payload blobs must not become a hiding place for unclassified planning or execution truth

Where raw provider payloads are archived or dropped after a defined retention period, that decision must be explicit and governed rather than implicit.
Dropping a raw payload while retaining promoted fields is acceptable only when the promoted fields preserve enough evidence context that later review of the original observation remains meaningful.
Silent payload expiry that erases traceability without a documented retention policy is provenance drift.

JSON is useful evidence support.
It is not provenance discipline by itself.

---

## Event Provenance Rule

Where canonical event logs are used, event provenance must remain meaningful.

This means event records should preserve:

- the event type
- the entity type
- the entity identity
- project scope
- actor attribution
- event time
- bounded structured details where needed

Event logs must remain append-only historical truth.
They must not be rewritten to manufacture cleaner history.

---

## Source-to-Signal Continuity Rule

When VEDA packages signal from evidence, continuity between source and signal must remain reconstructible.

A later reader should be able to determine, at the level required by context:

- what source or observatory evidence fed the signal
- whether the signal is direct or heavily derived
- what trust posture applied to that evidence
- what uncertainty remained when the signal was produced

Signal that cannot be traced back to an evidence basis is not strong VEDA behavior.

---

## Summarization Rule

VEDA may summarize evidence to make it more usable.

Summarization must not:

- erase provenance
- erase uncertainty
- blur summary into source truth
- convert weak evidence into stronger-seeming evidence through presentation polish

A summary is an aid layered on top of evidence.
It is not a replacement for source traceability.

---

## Cross-System Packaging Rule

When VEDA packages evidence or signal for Project V or another governed consumer, provenance must remain strong enough that downstream reasoning does not operate on provenance-stripped output.

This means packaging should preserve, where relevant:

- source identity or source locator
- capture or observation timing
- trust posture
- derivation posture
- project scope
- uncertainty markers

When the downstream consumer cannot directly access VEDA’s underlying evidence records, the package must be self-sufficient for governance review.
That means the package must contain enough provenance context that a reviewer can assess the evidence basis, trust posture, and uncertainty without requiring access to VEDA’s internal records.
Provenance references that require VEDA database access to verify are insufficient for cross-system packaging where independent review is required.

Cross-system usefulness must not come from provenance collapse.

---

## Forbidden Provenance Drift Patterns

VEDA evidence and provenance handling has drifted if it begins to:

- treat summaries as though they were source evidence
- present low-trust material as clean truth without uncertainty markers
- allow important source material to exist only in transient conversation or memory
- hide hot-path meaning only inside raw payload blobs
- package signal without enough source continuity to reconstruct its basis
- erase actor, time, or project context from observatory material
- use polished presentation to hide weak provenance

These are evidence failures, not presentation wins.

---

## Human-In-The-Loop Principle

Human review remains especially important when evidence or provenance handling involves:

- ambiguous source trust
- conflicting or weak evidence
- high-impact signal packaging
- provenance gaps
- uncertain or derived conclusions that may materially influence planning or execution review

VEDA should make evidence more reviewable, not more mysterious.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- evidence must remain traceable to source context
- provenance is part of evidence integrity
- source trust and uncertainty must stay visible
- raw evidence, structured observation, and derived interpretation are distinct layers
- summaries and signals must remain reconstructible against evidence
- cleaner output is not permission to erase provenance

If an LLM could use this doc to justify packaging provenance-stripped signal because it seems easier for downstream consumption, this document is failing.

---

## Usage

This document should be used:

- when designing VEDA evidence handling or source-capture behavior
- when reviewing whether provenance is strong enough for downstream signal use
- when writing more specific docs about operator surfaces, signal interfaces, or search-intelligence packaging
- when checking whether summarization or payload handling is eroding evidence integrity
- when evaluating whether source-trust posture is visible enough for governed downstream use

---

## Related Docs

- `veda.md`
- `system-invariants.md`
- `observability-and-signal-role.md`
- `operator-surfaces.md` *(planned)*
- `data-boundaries.md`
- `mcp-surface.md` *(planned)*
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../ecosystem/cross-system-boundaries.md`
- `../governance/auth-and-actor-model.md`
- `../governance/failure-and-recovery-doctrine.md`
