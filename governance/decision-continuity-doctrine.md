# Decision Continuity Doctrine

## Purpose

This document defines how decisions are preserved, referenced, revisited, and evolved across the V Ecosystem.

It exists to answer:

```text
How does the ecosystem ensure that decisions remain consistent, traceable, and govern future behavior without being silently lost, duplicated, or contradicted?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- how decisions persist across workflows and systems
- how decisions are referenced during planning, execution, and replanning
- how prior decisions constrain future behavior
- how decision continuity is preserved during return-to-planning
- how decisions are revisited, superseded, or invalidated
- how decision continuity relates to approval posture
- how decision continuity differs from runtime continuity artifacts

---

## Out of Scope

This document does not define:

- the approval process for decisions
- the full structure of ADR documents
- evidence validation rules
- detailed execution reporting structure
- implementation-specific storage or record schemas

Those belong in governance, interface, workflow, and project-specific docs.

---

## System

- governance

---

## Core Rule

A decision, once made and governed with the required approval posture, remains part of the active governing context until it is explicitly superseded or invalidated.

Decisions must not disappear, drift, or be silently overridden.

A proposed decision, draft decision, or informally discussed direction is not automatically a governing decision.
Runtime continuity artifacts are not governing decisions.

---

## Decision Continuity Definition

Decision continuity is the requirement that:

- governing decisions persist as active context
- future actions remain consistent with prior governing decisions unless explicitly changed
- decision history is preserved and interpretable
- replanning does not reset or ignore prior governing decisions without justification
- approval-sensitive decisions are not treated as continuity-binding before the required approval posture exists

---

## Decision Continuity vs Runtime Continuity

Decision continuity is not the same as runtime continuity.

### Decision continuity
Decision continuity concerns governing decisions that have continuity-binding force because they were properly approved, recorded, and remain active unless superseded or invalidated.

### Runtime continuity
Runtime continuity concerns session-support artifacts such as:
- working memory
- durable memory
- transcript artifacts
- compaction products
- retained worker findings

Runtime continuity artifacts may support usefulness and operator recall.
They do not become governing decision state by existing, by being remembered, or by surviving compaction.

---

## Decision Classes for Continuity Purposes

For continuity purposes, decisions should be understood at minimum through the following states:

- proposed decision
- approved governing decision
- rejected decision outcome
- superseded decision
- invalidated decision

### Rule

Only an approved governing decision has active continuity-binding force.

A proposed decision may inform review or planning preparation.
It does not constrain future behavior as governing doctrine or active project truth unless the required approval posture has been satisfied.

A rejected decision outcome must also be preserved where relevant, because rejected paths affect future reconsideration and prevent repeated rediscovery.

---

## Governing Decision Rule

A decision becomes continuity-binding only when:

- it is explicit enough to be reviewable
- it is attached to a bounded scope
- it has the approval posture required for its action class, workflow stage, and risk level
- it has not expired, been revoked, been superseded, or been invalidated

If those conditions are not met, the ecosystem must not treat the decision as stable governing context.

A decision is not continuity-binding until its governing state is reviewable.
Where approval has occurred but the decision record has not yet been created, the decision exists in an approved-but-unrecorded state and must not be treated as fully continuity-binding until the record is established.
Agents must not defer record creation to justify acting on unrecorded governing state.

---

## Decision Persistence Rule

Approved governing decisions must persist as part of the ecosystem’s active governing context.

This means:

- decisions remain visible to future planning and execution
- decisions must be referenceable during:
  - planning
  - handoff creation
  - execution interpretation
  - return-to-planning
  - approval-sensitive reconsideration
- decisions must not be implicitly dropped due to workflow transitions, system transitions, or context packaging

---

## Decision Binding Principle

Approved governing decisions constrain future behavior.

This means:

- planning must respect prior governing decisions unless explicitly revisited
- execution must operate within the bounds of governing decisions relevant to the handed-off work
- interfaces must not reinterpret governing decisions beyond their defined scope
- governance-sensitive follow-on actions must not claim continuity force from decisions that were never properly approved

A decision is not a suggestion.
But a proposed decision is also not a decision with binding force.

---

## Approval Relationship

Decision continuity depends on approval posture where doctrine requires approval.

This means:

- readiness is not the same as an approved decision
- recommendation is not the same as an approved decision
- draft planning language is not the same as an approved decision
- handoff preparation is not the same as an approved handoff decision
- return-to-planning findings are not the same as an approved decision to replan or mutate planning state

When approval is required, lack of explicit approval means the decision does not yet have governing continuity force.

The approval and escalation model defines when approval is required and how unclear approval posture must be handled.
This document defines what continuity means once decision state is interpreted.

---

## Ungoverned Decision Rule

The ecosystem must distinguish clearly between:

- a candidate decision under consideration
- an informally expressed preference or direction
- an approved governing decision

Agents must not:

- treat discussion as decision
- treat informal direction as governed decision state
- treat a drafted recommendation as continuity-binding
- carry unapproved decision language forward as if it were settled governing context
- treat transcript or memory artifacts as substitute decision records

If approval-sensitive decision state is unclear, the decision must not be treated as continuity-binding.

---

## Decision Reference Requirement

When performing planning, handoff creation, execution interpretation, or replanning:

- relevant prior governing decisions must be considered
- conflicting actions must trigger explicit decision review
- absence of decision reference where one exists is a continuity failure
- reused decision authority must remain within its approved scope

When an agent detects that a relevant governing decision has not been referenced where it should have been, it must not proceed as though the decision context is absent.
The agent must surface the gap, reference the prior governing decision where possible, and escalate if the missing decision context materially affects correctness.

Decision reference does not require repeating the full history every time.
It requires preserving and using the governing decision context that still applies.

---

## Approval Scope Reuse Rule

A governing decision remains continuity-binding only within the scope actually covered by its approval and decision context.

This means agents must not silently widen a decision across:

- workflow stages
- materially changed project conditions
- expanded mutation scope
- different projects
- broader external action classes
- new handoff packages that exceed the originally governed scope

If the scope changed materially, the ecosystem must not assume the prior governing decision still applies unchanged.

---

## Stale Approval and Changed Context Rule

A prior governing decision may lose active continuity force if the conditions that supported its approval have materially changed.

Examples include:

- materially changed evidence
- materially changed execution findings
- materially changed risk posture
- materially changed scope
- materially changed workflow stage
- materially changed external constraints

A change is material when it would have been decision-relevant at the time the governing decision was made.
A change that would likely have altered the decision, changed the approval posture, or triggered re-evaluation should be treated as material for continuity purposes.
When materiality is uncertain, the default is to treat the change as potentially material and apply this rule cautiously.

In those cases, the decision should not be treated as automatically reusable without determining whether revalidation, supersedence, or invalidation is required.

This does not mean every new fact resets decision continuity.
It means materially changed governing context must not be ignored.

---

## Replanning Continuity Rule

Return-to-planning must preserve decision continuity.

When execution findings, changed conditions, or revised evidence trigger replanning:

- prior governing decisions remain active unless explicitly challenged
- new findings may:
  - reinforce prior decisions
  - expose invalid assumptions
  - justify revision
  - justify supersedence
  - justify invalidation

But replanning must not:

- reset decision context
- ignore prior governing decisions
- create parallel contradictory governing decisions without resolution
- treat the existence of new findings as automatic approval to change prior decisions

Replanning preserves continuity unless and until a governed change occurs.

---

## Decision Conflict Rule

If a proposed action, proposed decision, or current workflow path conflicts with an existing governing decision:

- the conflict must be made explicit
- one of the following must occur:
  - decision reaffirmation
  - decision revision
  - decision supersedence
  - decision invalidation
  - escalation for conflict resolution

Silent conflict is not allowed.

---

## Conflicting Approval Rule

A decision with conflicting approval signals must not be treated as stable governing context until the conflict is resolved through the governed approval path.

This includes situations where:

- one actor appears to approve and another rejects
- one approval applies only conditionally and those conditions are unclear
- later direction appears to contradict earlier approval without explicit supersedence or revocation
- the reviewable approval record does not support a single stable interpretation

In those cases, continuity requires explicit resolution rather than optimistic interpretation.

---

## Rejection Continuity Rule

A rejection is part of decision continuity where the rejected path affects future behavior.

When a proposal, handoff, mutation, or other approval-sensitive decision is rejected, continuity should preserve:

- what was rejected
- why it was rejected, if known
- what scope the rejection applied to
- what conditions would need to change before reconsideration, if known

A rejected path must not be repeatedly rediscovered as if no prior decision existed.
Rejection records must be preserved in a form accessible to future planning sessions.
Ephemeral conversation-level notes do not satisfy rejection continuity.

Rejection continuity supports intake rejection continuity, replanning continuity, and approval-history integrity.

---

## Supersedence Requirement

A governing decision may only be replaced through explicit supersedence.

Supersedence must:

- reference the prior governing decision
- explain why the prior decision is no longer sufficient, no longer correct, or no longer the active governing choice
- establish the new governing decision
- satisfy the approval posture required for the new decision’s scope and impact

Supersedence must be initiated by the system or actor that owns the relevant governing context, or through a governed escalation path.
V Forge must not unilaterally supersede governing planning decisions.
Actor authority is defined in `auth-and-actor-model.md`.

After supersedence:

- the prior decision remains part of history
- the new decision becomes the active governing constraint
- agents must not treat the old and new decisions as co-equal active authority

---

## Invalidation Rule

A governing decision may be invalidated when:

- underlying assumptions are proven false
- required conditions no longer exist
- governing context has materially changed
- later evidence or findings remove the basis for continued validity

Invalidation must be:

- explicit
- justified
- reviewable
- handled with the approval posture required by the affected decision class and impact level

Invalidation must be initiated by the system or actor that owns the relevant governing context, or through a governed escalation path.
V Forge must not unilaterally invalidate governing planning decisions.
Actor authority is defined in `auth-and-actor-model.md`.

Invalidated decisions remain part of history but must not continue to constrain active behavior.

---

## Cross-System Decision Integrity

Decision continuity must hold across system boundaries.

This means:

- Project V must preserve planning decisions and planning-side decision continuity
- V Forge must execute within governing decision bounds relevant to handed-off work
- V Forge must not reinterpret or override planning decisions casually
- VEDA must not redefine decisions through signal transfer
- signal, findings, and execution outcomes may challenge decisions only through the governed return, review, and replanning path

No system may silently mutate decision meaning.

---

## Decision vs Signal vs Findings vs Runtime Continuity

To prevent drift:

- **Decision** = a governing choice that becomes continuity-binding when properly approved
- **Signal** = evidence or observation that may inform or challenge a decision
- **Findings** = bounded execution outputs that may inform or challenge a decision
- **Runtime continuity artifact** = a non-canonical memory, transcript, compaction, or worker-derived artifact that may support session continuity without becoming governing state

Rules:

- signal does not become decision automatically
- findings do not override decisions automatically
- proposed decisions do not become governing decisions automatically
- runtime continuity artifacts do not become decision records automatically
- decisions must be explicitly reviewed, revised, superseded, invalidated, or reaffirmed when signal or findings require it

This distinction is one of the main anti-drift controls in the ecosystem.

---

## Failure Modes (Explicitly Forbidden)

The following are continuity failures:

- decisions disappearing across workflow transitions
- draft or proposed decisions being treated as approved governing decisions
- duplicate conflicting governing decisions without resolution
- execution ignoring governing planning decisions
- replanning that resets decision context
- stale approval being treated as automatically reusable
- conflicting approvals being treated as stable decision authority
- signal being treated as implicit decision
- findings being treated as automatic decision override
- informal direction being carried forward as if it were governed decision state
- runtime continuity artifacts being treated as decision records

---

## Human-In-The-Loop Principle

Decision continuity is governance-critical.

Human review may be required when:

- a decision becomes approval-sensitive
- high-impact decisions are revised
- conflicting decision or approval states emerge
- invalidation or supersedence occurs
- strategic direction changes
- changed context may have made prior approval stale

Human involvement here is not paperwork theater.
It is how the ecosystem prevents silent drift dressed up as momentum.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- only approved governing decisions have continuity-binding force
- decisions must be referenced, not rediscovered
- replanning does not reset decision state
- changed evidence or findings do not automatically mutate decisions
- stale or conflicting approval posture weakens decision continuity and may require revalidation or escalation
- runtime continuity artifacts are useful but non-authoritative
- changes to governing decisions must be explicit and justified

If an LLM can treat drafts, informal direction, stale approvals, or runtime continuity artifacts as binding decisions without consequence, the doctrine is failing.

---

## Usage

This document should be used:

- when determining whether a decision is continuity-binding
- when reviewing whether prior decision context still applies
- when deciding whether replanning may reuse prior decision authority
- when resolving conflicts between prior decisions and current proposals
- when deciding whether supersedence, invalidation, reaffirmation, or escalation is required
- when designing decision records and continuity checks in workflows

---

## Related Docs

- `approval-and-escalation-model.md`
- `agent-operating-doctrine.md`
- `auth-and-actor-model.md`
- `invalidation-and-supersedence-doctrine.md`
- `evidence-continuity-model.md`
- `report-structure-and-required-fields.md`
- `../interfaces/extension-memory-and-continuity-model.md`
- `../ecosystem/cross-system-boundaries.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../workflows/project-intake-workflow.md`
