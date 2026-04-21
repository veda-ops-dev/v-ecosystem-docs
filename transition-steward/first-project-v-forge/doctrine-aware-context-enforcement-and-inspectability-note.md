# Doctrine-Aware Context Enforcement and Inspectability — Design Note

## 1. Purpose

This note designs the harness enforcement and inspectability layer that makes
the doctrine-aware context model operationally auditable.

It exists to answer:

> How should the harness enforce stage-aware, authority-aware context loading,
> and what minimum evidence should the runtime produce so that a later Loaf
> Audit or end-to-end workflow capability audit can verify the model was
> actually followed?

This is a bounded transition-support design note. It is downstream of and
subordinate to the tightened design pass in
`doctrine-aware-context-model-design-pass.md`. It does not rewrite that model.
It adds the operational layer the model declared open.

---

## 2. Status

Transition-support only.

This note is:
- concrete enough to guide harness implementation direction
- not yet promoted into authority docs
- not a schema design, storage design, or UI design
- not final doctrine

The enforcement and inspectability mechanisms described here are proposed
postures. They may be revised as first-project work exposes gaps.

---

## 3. Problem Being Solved

The tightened context model defines what should load at each stage and why.
It does not define how the harness ensures that actually happens, nor how a
reviewer could verify it did.

Without an enforcement layer, the model is a policy document. Context loading
remains behavioral (the LLM is told what to load) rather than structural (the
harness enforces what can load). Without an inspectability layer, the model
cannot support a Loaf Audit because there is no evidence trail to audit.

The gap is specifically:

- admission enforcement: what prevents wrong-class context from loading?
- stage transition behavior: what happens to active context when stages change?
- load record production: what evidence exists that the model was followed?
- exclusion visibility: how does the operator know what was excluded?
- validation independence: how is it structurally enforced, not just declared?

This note proposes bounded answers to each of these. Where the answer is
genuinely open, it says so.

---

## 4. Enforcement Posture

### The admission gate concept

Context admission should be treated as a gate, not a convenience. A candidate
piece of context is not in scope for the active session until it has been
admitted. Retrieval hits, transition-support notes, prior continuity artifacts,
and planning packets are all candidates until admitted.

Admission is the moment when a context candidate becomes active session basis.
That moment should be structurally distinct from retrieval and from context
assembly start.

The harness enforces admission by checking each candidate against two things:

1. **Class check:** does this candidate's class match the classes allowed
   for the current stage, per the stage loading posture in Section 6 of the
   design pass?

2. **Stage check:** is the current workflow stage one where this class is
   mandatory, selective, or excluded?

A candidate that fails either check is not admitted. It may be retained as
an excluded candidate for inspectability purposes (see Section 7), but it does
not enter the active context basis.

### What must be checked before admission

Before a context candidate is admitted, the harness should verify:

- **Source class:** which of the eight classes does this candidate belong to?
  (Canonical Authority, Referenced Authority, Derived Intelligence, Planning
  Packet/Framing, Execution Packet, Transition-Support, Continuity Artifact,
  Inert Model Output)
- **Derivation basis visibility:** if the candidate is Derived Intelligence,
  is its derivation basis present and intact? A VEDA Strategy signal without
  its derivation basis is not admissible as Derived Intelligence — it would
  function as an unsourced claim.
- **Stage eligibility:** is this class in the mandatory or selective set for
  the current stage? Or is it in the exclude list?
- **Freshness:** if this is a Continuity Artifact, has it been superseded by
  canonical state loaded in this session? A stale continuity artifact that
  conflicts with freshly loaded canonical state must not be admitted as though
  it is current.
- **Scope:** does this candidate belong to the current project scope? Cross-
  project context bleed is a class-level violation regardless of stage.

### How retrieval results remain candidates

Qdrant retrieval hits must never be directly admitted to active session basis.
They enter as retrieval candidates. The admission check above is what converts
a candidate into admitted context.

The practical consequence is that retrieval results should be held in a
candidate pool separate from the admitted context basis until the harness runs
the class + stage check against each one. Results that pass become admitted.
Results that fail become excluded candidates (visible but inactive).

This separation is what gives the anchor principle operational meaning:
Qdrant finds; VedaOps decides.

### Authority ranking within admitted context

Once admitted, context follows the authority ranking from the design pass:
Canonical Authority outranks everything; retrieval-derived material, even if
admitted, does not outrank Canonical Authority. The harness should make this
ranking available to the LLM as part of the context assembly — not just as
a behavioral instruction, but as explicit metadata on each admitted item.

---

## 5. Stage-Transition Posture

Stage transitions are the moment when the enforcement posture is most likely
to fail silently. Context that was correct for the prior stage may be wrong
for the next stage, and drift happens when transitions are not treated as
explicit re-admission events.

### Proposed posture: explicit re-admission on stage transition

The harness should treat each stage transition as a context re-admission event.
This does not mean flushing everything. It means:

- the active context basis is re-evaluated against the new stage's class + stage
  rules
- items that are no longer eligible are withdrawn from active basis
- items that are now excluded are moved to excluded-candidate status
- items that were mandatory at the prior stage but not mandatory at the new
  stage are re-evaluated as selective
- new mandatory items for the incoming stage are loaded if not already present

This is pruning and re-evaluation, not wholesale flush. Full context flush would
destroy continuity that is legitimately carried forward (e.g., Canonical
Authority that is mandatory at every stage should not be dropped and reloaded on
every transition). The goal is selective re-evaluation, not clean-room restart.

### Key transitions and their enforcement implications

**Planning → Handoff Creation**

- Planning Packet remains mandatory (handoff is produced from plan)
- Execution Packet is not yet available; must not be fabricated from planning
  packet content at this stage
- Continuity artifacts from intake should be re-evaluated for admission
- Transition-Support remains advisory

**Handoff Creation → Execution**

- This is the highest-risk transition for context bleed
- Planning Packet must be explicitly withdrawn from active basis at this
  transition, except for any execution-scoped digest explicitly prepared and
  admitted under that class
- Execution Packet must be present as mandatory before execution begins;
  if it is absent, execution should be blocked pending its assembly
- Builder continuity artifacts from the planning stage must not carry forward
  silently — they must be evaluated and either explicitly withdrawn or
  explicitly retained as advisory-only with visible attribution
- This transition should require an explicit acknowledgment from the harness
  that the Planning Packet has been withdrawn and the Execution Packet is active

**Execution → Validation**

- This is the most important transition for independence enforcement
- Execution Packet is withdrawn from active basis (it was the builder's context)
- Planning Packet remains excluded
- Builder continuity artifacts must be explicitly cleared, not merely deprioritized
- Validation-side context assembly must begin fresh from Canonical Authority
  and execution outputs only
- The harness should produce an explicit validation-assembly marker indicating
  that context was assembled independently for this stage (see Section 8)

**Validation → Publication / External Mutation**

- Approved execution outputs become mandatory
- Canonical Authority remains mandatory
- Validation artifacts (the validation outputs themselves) should be present
  as evidence of passed validation, not as planning context
- Planning Packet and Execution Packet remain excluded

**Publication → Observation Return / Feedback**

- Active context narrows significantly
- Only VEDA canonical observation records and VEDA Strategy derived intelligence
  (with derivation basis) are relevant
- Prior planning and execution context must not be present; observation return
  should not be informed by what was planned or built, only by what was observed
- Any planning implication from observation data routes back through Project V
  intake — it does not re-enter here as planning context

### What must never silently carry forward across any transition

- Planning Packet context into execution or validation
- Builder continuity artifacts into validation
- Execution Packet context into validation
- Retrieval-only candidates that were never explicitly admitted
- Inert model output presented as though it graduated to a higher class during
  the transition

---

## 6. Inspectable Load Record Posture

### The minimum useful concept

An inspectable load record is the evidence that context loading happened as the
model requires. It does not need to be a full log of every token. It needs to be
sufficient for a later auditor to answer:

- what was loaded at each stage?
- what class was each loaded item assigned?
- why was it admitted (mandatory / selective / advisory)?
- what stage was it admitted for?
- what was explicitly excluded?
- was any context inherited from a prior stage, and was that inheritance
  authorized?
- was validation context assembled independently?

### Proposed load record structure (operational model level)

Each stage transition should produce a context load record with the following
logical fields:

```
stage: [intake | planning | handoff-creation | execution | validation |
        publication | observation-return]

admitted:
  - id or reference to the item
  - class: [canonical-authority | referenced-authority | derived-intelligence |
            planning-packet | execution-packet | transition-support |
            continuity-artifact | inert-model-output]
  - admission-basis: [mandatory | selective | advisory]
  - freshness-state: [current | aging | stale | superseded]
  - carried-from-prior-stage: [yes | no]
  - if carried: authorization-basis [explicitly-re-admitted | inherited-without-check]

excluded:
  - id or reference to the item
  - class
  - exclusion-reason: [wrong-class-for-stage | stale | scope-mismatch |
                       validation-independence | retrieval-candidate-not-admitted]

validation-assembly-marker:
  - present: [yes | no]
  - assembled-independently: [yes | no | unknown]
```

This is an operational model, not a schema. The implementation will need to
decide storage format, persistence, and retrieval. The fields above are the
minimum evidence requirements — if an implementation cannot produce this
evidence, the Loaf Audit cannot verify the model was followed.

### What the load record is not

The load record is not a canonical truth record. It is not a Project V planning
record or a VEDA evidence record. It is a runtime inspectability artifact —
akin to a continuity artifact in class, but with the specific purpose of
supporting audit rather than continuity. It lives in the harness / desktop
layer, not in any of the four system schemas.

---

## 7. Exclusion Visibility Posture

### The failure mode being prevented

Without explicit exclusion visibility, the harness produces a clean-looking
context basis with no indication of what was considered and rejected. An
auditor cannot tell whether planning context was properly excluded from
validation or simply never retrieved. An operator cannot tell whether their
transition-support note was advisory or simply invisible.

This creates fake independence: the system appears clean because excluded
material leaves no trace, not because it was properly evaluated and rejected.

### Proposed posture

Excluded context candidates should be retained as an explicit excluded set
alongside the admitted context basis. They are not active; they do not influence
LLM reasoning. But they exist as inspectable evidence that the admission check
ran and found them ineligible.

For each excluded item, the exclusion reason should be recorded (see the load
record above). The operator should be able to inspect the excluded set through
the appropriate surface — not by default in the interaction surface, but
available through a review surface when audit or investigation is needed.

### Practical constraint

Not every retrieval candidate that goes unselected needs to be a formal
excluded record. The concern is specifically about items that were evaluated
against the class + stage rules and rejected — not about the long tail of
retrieval results that are simply low-relevance. The excluded set should reflect
decisions made, not every candidate considered.

In practice, the distinction is:
- a retrieval hit that was never a plausible admission candidate → not a formal
  excluded record
- a planning packet that was present and evaluated at the execution stage, and
  rejected by the class + stage check → a formal excluded record

### Exclusion visibility at stage transitions

At each stage transition, the newly excluded items (items that were admitted
in the prior stage but are now excluded) should be explicitly recorded in the
transition's load record. This is the evidence that the transition's pruning
actually ran.

---

## 8. Validation-Independence Enforcement

### Why declaration is not enough

The design pass declares that validation must not inherit planning context.
A declaration is necessary but not sufficient. Without structural enforcement,
the LLM or harness could include planning context in the validation basis
while still technically honoring the declaration's letter — for instance, by
loading planning context as "advisory only" in validation, which the model
allows for transition-support but not for planning packets.

Structural enforcement means the harness makes it mechanically impossible, not
merely doctrinally wrong, to load Planning Packet or builder continuity artifacts
into the validation stage.

### Proposed enforcement approach

**1. Separate context assembly for validation**

Validation context should be assembled from scratch, not by pruning the
execution context. The execution-to-validation transition should be treated as
a context-reset event for everything except Canonical Authority. The new basis
starts from Canonical Authority and execution outputs; prior context is not
the starting point.

This is the difference between "prune planning context from execution basis"
(still starts with execution's view of the world) and "build validation basis
independently" (starts fresh from canonical records). The latter is structurally
stronger.

**2. The validation-assembly marker**

The load record should include an explicit validation-assembly marker: a flag
indicating whether the validation stage's context was assembled independently
or inherited from a prior stage. This marker is what would prove independence
to a Loaf Audit.

If the marker is absent or says "inherited-without-check", that is a
validation-contamination event. The audit can flag it.

**3. What counts as a validation-contamination event**

A validation-contamination event occurs when any of the following is present
in the admitted context basis at validation stage:

- Planning Packet in any form not classified as Canonical Authority
- Builder continuity artifacts from execution or planning stages
- Intermediate reasoning or working hypotheses tagged as prior-stage products
- Transition-support notes whose admitted basis was planning-intent framing
  rather than general advisory content

The load record's excluded set should show these were considered and rejected.
If they appear in the admitted set at validation, the contamination is
detectable by the audit.

---

## 9. First-Project Proving-Case Mapping

The entity-driven gift discovery first project provides a concrete surface for
testing this enforcement posture.

### Planning-stage admitted bundle (approximate)

**Admitted — Mandatory:**
- Project V doctrine (Canonical Authority)
- V Ecosystem cross-system boundaries (Canonical Authority)
- LLM harness architecture (Canonical Authority)
- Planning packet: `first-project-entity-driven-gift-discovery-planning-packet.md`
  (Planning Packet / Framing class — binding within planning only)

**Admitted — Selective:**
- First-project shape doc: `first-project-entity-driven-gift-discovery-site.md`
  (Planning Packet / Framing class or Transition-Support, depending on whether
  the intake event has been opened — this is a real classification judgment the
  harness would need to make)
- V Forge doctrine (Referenced Authority, read-only)
- Transition-support notes (advisory)

**Excluded at planning:**
- Any Execution Packet (not yet assembled)
- Prior continuity artifacts from unrelated work
- Retrieval hits not passing class + stage check

**Inspectability note:** The planning stage is where the planning packet's
"not yet an admitted intake item" status matters most for load record accuracy.
The load record should classify the planning packet at its current status
(transition-support framing material) rather than as a promoted authority asset.
Getting this classification right is a concrete test of the class-check.

---

### Execution-stage admitted bundle (approximate)

**Admitted — Mandatory:**
- V Forge doctrine (Canonical Authority)
- Execution Packet derived from the approved handoff
- Cross-system boundaries (Canonical Authority)

**Admitted — Selective:**
- Referenced Authority from Project V (project scope, constraints) — read-only,
  bounded, not the full planning packet
- V Forge content execution guidance (Canonical Authority)

**Excluded at execution:**
- Planning Packet (full form or any framing version not explicitly scoped as
  execution digest)
- Planning-stage builder continuity artifacts
- Validation artifacts (not yet produced)
- VEDA Strategy signals at this stage unless explicitly relevant to bounded
  execution-side research

**High-risk point:** The gift discovery project involves editorial judgment —
what makes a good gift, how to frame a recipient page, how to weight products.
The temptation at execution will be to pull the planning packet to "remind" the
LLM of product curation intent. This is the specific bleed the execution-stage
exclusion rule is designed to prevent. The planning intent should have been
encoded into the execution packet at handoff creation. If it was not, the
execution packet is incomplete — the right response is to fix the execution
packet, not to admit the planning packet.

---

### Validation-stage admitted bundle (approximate)

**Admitted — Mandatory:**
- Canonical Authority (structural rules, page generation policy, anti-explosion
  rule, curation-load-bearing rule — all from the Canonical Authority docs)
- Execution outputs: produced product records, page drafts, classification
  assignments, editorial notes

**Admitted — Selective:**
- Referenced Authority for validation rule set where needed

**Excluded at validation:**
- Planning packet (any form)
- Builder/execution continuity artifacts
- Transition-support notes with planning intent framing
- VEDA Strategy signals (not yet relevant)

**Validation-assembly marker:** must be present and set to
`assembled-independently: yes` to pass Loaf Audit check for this stage.

**Critical test for the first project:** The gift discovery site has an explicit
anti-page-explosion rule and an editorial-curation-is-load-bearing rule. Both
of these must validate against the executed output independently of what the
planning stage intended. If the validator knows "we planned to be strict about
page explosion," that knowledge could bias toward seeing non-existent compliance.
The validator should check against the rule, not against the plan.

---

### Where inspectability matters most in this project

1. **Execution-stage exclusion of the planning packet** — the most likely
   failure point given the editorial judgment required
2. **Validation-assembly marker** — the evidence that validation was
   independent matters for a project that has explicit structural rules
3. **Classification of the planning packet at planning stage** — it is
   transition-support framing, not a promoted authority asset; the load record
   should show that

---

## 10. How This Supports Later Loaf Audit

### What this enforcement design contributes

A Loaf Audit on the gift discovery first project using this enforcement design
could ask and get evidence-backed answers to:

- Was Canonical Authority (Project V, V Forge, ecosystem boundaries) present
  at every stage?
- Was the planning packet excluded from the execution and validation stages?
- Was validation context assembled independently?
- Were builder continuity artifacts cleared at the execution → validation
  transition?
- Were retrieval candidates held in candidate status until explicitly admitted?
- Did VEDA Strategy derived intelligence carry its derivation basis when present?
- Were any excluded items from planning-stage context recorded as excluded at
  validation, proving the check ran?

These are answerable from the load records this design would produce.

### What the audit could not verify from this design alone

- Whether the admitted Canonical Authority was actually current (freshness
  verification requires the invalidation and refresh layer from
  `desktop-invalidation-and-refresh-matrix.md`)
- Whether the execution packet actually encoded what the planning stage decided
  (that belongs to handoff quality, not context loading)
- Whether the LLM's reasoning actually respected the authority ranking of
  admitted context (load records show what was available; they don't audit
  how it was used)
- Whether validation outputs were correct (that is content validation, not
  context loading verification)

### Honest readiness assessment

This design makes the Loaf Audit feasible for context-loading claims.
It does not make the full Loaf Audit complete. The other audit dimensions —
harness enforcement of governance gates, authority boundary respect, workflow
stage fidelity — each have their own evidence requirements that are out of
scope for this note.

---

## 11. Open Questions

- **Load record persistence:** where load records live, who owns them, and
  how long they are retained. This is an implementation question but is not
  trivial — load records that exist only in session memory are not useful for
  a post-session Loaf Audit.

- **Candidate pool separation from active basis:** whether the retrieval
  candidate pool and the admitted context basis are structurally separate data
  structures (preferred) or logically separated by metadata flags within a
  single structure (lower structural guarantee). The former is more auditable.

- **Execution-scoped planning digest governance:** if a planning digest is
  legitimately prepared for execution use, who produces it, in what workflow
  step, and what governs its contents? This is the most under-specified part
  of the current model. Until it is answered, the execution-stage selective
  item is a claimed capability without a governing process.

- **Validation-assembly marker trust:** the validation-assembly marker is only
  meaningful if the harness sets it, not if the LLM sets it. If the LLM can
  write its own load record, the marker proves nothing. The marker must come
  from the harness layer, not from LLM self-report.

- **Stage transition initiation:** who or what triggers a stage transition?
  If stage transitions are operator-initiated, the re-admission event is clear.
  If stage transitions happen implicitly (e.g., because an execution packet was
  loaded), the trigger is fuzzy. This needs to be resolved in implementation.

- **Excluded-set retention scope:** how long excluded candidates are retained,
  and whether they are scoped to the session or persist for post-session audit.
  Session-scoped exclusion records are useful for operator inspection;
  post-session retention is needed for Loaf Audit.

---

## 12. Recommended Next Move

1. Use this note alongside the design pass to evaluate the first-project
   planning stage: can the harness produce a credible load record for that
   stage given the current state of the planning materials?

2. The execution-scoped planning digest open question (Section 11) is the
   highest-priority design gap to resolve before first-project execution begins.
   Without a governing process for that digest, the execution-stage admission
   rules are incomplete.

3. Resolve the load record persistence question before attempting a Loaf Audit.
   Session-only records cannot support post-session audit.

4. Do not promote this note into authority doctrine until the first project has
   exercised the model in practice and the open questions above have been
   addressed. The model may need revision based on what the first project
   exposes.

---

## 13. Related Files

- `doctrine-aware-context-model-note.md`
- `doctrine-aware-context-model-design-pass.md`
- `../first-project-entity-driven-gift-discovery-site.md`
- `../first-project-entity-driven-gift-discovery-planning-packet.md`
- `../transition-plan.md`
- `../../interfaces/llm-harness-architecture.md`
- `../../interfaces/desktop-memory-and-continuity-model.md`
- `../../interfaces/desktop-interaction-surface-and-command-dispatch.md`
- `../../interfaces/desktop-governance-and-gating-model.md`
- `../../interfaces/desktop-state-and-context-model.md`
- `../../interfaces/desktop-invalidation-and-refresh-matrix.md`
- `../../interfaces/desktop-compaction-implementation-design.md`
- `../../governance/approval-mechanics-seam-model.md`
- `../../governance/decision-continuity-doctrine.md`
- `../../ecosystem/cross-system-boundaries.md`
