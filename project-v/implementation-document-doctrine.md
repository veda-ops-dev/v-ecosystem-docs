# Implementation Document Doctrine

## Purpose

This document defines what an implementation document is inside Project V,
what it must contain, and how it fits between planning truth and execution truth.

It exists to answer:

```text
What is an implementation document in this system, what must it contain to be
execution-ready rather than planning prose, who owns it, and what makes one
invalid, stale, or non-buildable?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the definition and ownership of implementation documents in Project V
- the minimum semantic contract an implementation document must satisfy
- the relationship between implementation documents and handoff, ETR, decisions,
  readiness, audit, and traceability
- what makes an implementation document invalid, stale, or non-buildable
- the boundary between an implementation document and related artifacts

---

## Out of Scope

This document does not define:

- the handoff package record and its required semantic fields
  (those belong in `../interfaces/project-v-to-v-forge-handoff-interface.md`)
- V Forge internal execution workflow
- detailed schema or field specifications
- ETR record posture and freshness requirements
  (those belong in `external-technology-research-doctrine.md`)
- decision continuity and approval requirements
  (those belong in `../governance/decision-continuity-doctrine.md`)

---

## System

- project-v

---

## Core Rule

An implementation document is a Project V-owned, execution-ready planning artifact
that translates approved planning truth into bounded build direction for V Forge.

It must be specific enough that V Forge can determine what to build, what not to
build, what constitutes a complete output, and what should trigger clarification or
return-to-planning — without needing to interpret vague scope or absorb unresolved
planning ambiguity.

If an implementation document cannot meet that bar, it is not execution-ready. It
is still planning prose.

---

## Definition

An implementation document is the execution-ready artifact that Project V produces —
as part of or referenced by a governed handoff package — to carry the approved
execution scope, constraints, evidence basis, and decision rationale into V Forge in
actionable form.

It is a specification of bounded execution intent. It is not a full technical API or
schema specification, but it is not a loose summary either. It specifies what V Forge
is to execute, within what constraints, on what basis, and under what conditions it
should return to planning rather than proceed.

---

## What an Implementation Document Is Not

An implementation document is not:

- a planning narrative — planning narratives explain why decisions were made;
  implementation documents carry what was decided in execution-ready form
- a `ResearchDoc` or ETR record — it may reference them; it does not duplicate them
- a `DecisionRecord` — it references governing decisions; it is not a decision itself
- a V Forge execution record — V Forge owns what was actually built; the
  implementation document carries what was approved to build
- a handoff package — the handoff package is a governed record with structured
  fields; the implementation document is the artifact carried or referenced by it
- a free-floating markdown file — a markdown file with no linkage to planning
  records, decisions, and governed handoff context is not an implementation
  document; it is ungoverned prose

---

## Ownership

An implementation document is:

- **owned by Project V** — it is produced under Project V's planning authority as
  part of the planning-to-handoff process
- **consumed by V Forge** — V Forge reads it to understand what was approved, what
  constraints apply, and what should trigger clarification or return-to-planning
- **referenced by the handoff package** — the handoff record's structured fields
  summarize or reference the implementation document's content; the document does
  not replace the structured fields

Ownership does not transfer when V Forge reads the document. The document remains
Project V planning truth after receipt. V Forge's execution outputs — what was
actually built — are V Forge-owned execution truth. Those are not the same thing.

---

## Minimum Semantic Contract

A valid implementation document must carry enough to answer all of the following.
If any of these cannot be answered from the document, the document is incomplete.

### 1. Bounded objective and approved scope

What work is being approved, for what surface or system, and at what explicit
boundaries.

The scope must be specific enough that V Forge can determine what is in scope
and what is not. Open-ended scope descriptions are not valid. Execution does not
interpret ambiguous scope — it returns to planning or blocks.

This maps to the handoff package's **Approved execution scope** field.

### 2. Linked planning records

Which Project V planning records — objective, initiative, work item — this
document traces to.

A document with no planning record linkage is untraceable. It cannot be audited
and should not support a valid handoff.

### 3. Linked decision basis

Which `DecisionRecord` entries govern the scope, technology choices, constraints,
and structural rules the document carries.

A document that asserts execution direction without recoverable `DecisionRecord`
linkage cannot be reviewed or superseded cleanly. Per
`../governance/decision-continuity-doctrine.md`: a governing decision must be
reviewable to be continuity-binding. An implementation document whose direction
cannot be traced to a governing decision is carrying assertions, not governed truth.

### 4. ETR references where technology assumptions are carried

Any claim that depends on external technology behavior — what database version,
what framework, what API contract, what platform constraint — must reference a
governed ETR record with version, source attribution, and freshness classification.

This is not optional when technology assumptions are present. Per
`external-technology-research-doctrine.md` Anti-Drift Rules:
"handoff or implementation docs paraphrasing unsupported technology claims as
though they were grounded" is a forbidden pattern.

A document that says "use PostgreSQL 16" without a linked `ResearchDoc` in ETR
posture is carrying a claim with no recoverable basis.

### 5. Execution constraints and explicit non-goals

What constraints apply to execution — cost bounds, external action limits, launch
conditions, dependency conditions, structural rules — and what is explicitly out
of scope.

Without explicit non-goals, V Forge has no basis for refusing scope expansion.

This maps to the handoff package's **Execution constraints and boundaries** field.

### 6. Expected outcomes and deliverable shape

What done looks like — the specific deliverable or output V Forge should produce
within the approved scope.

This must be concrete enough to support a completion determination, not a
restatement of intent.

This maps to the handoff package's **Expected outcomes or intended execution
objective** field.

### 7. Return-to-planning triggers

What execution conditions should cause V Forge to return findings to planning
rather than proceeding.

Per `../interfaces/project-v-to-v-forge-handoff-interface.md`: "conditions that
should trigger return-to-planning" is a mandatory semantic field. A document
without explicit triggers leaves every return decision to V Forge's unilateral
judgment, which defeats the governed path.

### 8. Readiness basis and freshness posture

Why this document is valid now — what readiness determination supports it, and
whether any ETR or evidence it references has been validated against current
freshness requirements.

Per ETR Freshness and Re-Validation Rule: "handoff is being prepared significantly
later than the original research" is a re-validation trigger. An implementation
document authored at one point and activated significantly later must carry
explicit freshness posture on its ETR references.

This maps to the handoff package's **Readiness basis** field.

### 9. Traceable inputs

The document must carry explicit references to the planning records, decisions,
and ETR that support its claims — not paraphrases disconnected from those records.

Per `implementation-traceability.md` Minimum Traceability Semantics: the planning
basis must be recoverable through record linkages, not reconstructed from prose.
A document whose claims cannot be traced to governed records is a documentation
artifact, not a traceable planning artifact.

### 10. Buildability threshold

The document must pass this test: can V Forge act within it without loading the
planning packet? Can V Forge determine what is in scope, what is out of scope,
what constitutes completion, and what should trigger clarification or return?

If the answer is no — if V Forge would need to consult planning materials to
fill gaps in the document — the document has not reached the buildability
threshold. It is still planning-phase work.

---

## Invalid, Stale, and Non-Buildable Conditions

The following conditions make an implementation document invalid, stale,
or non-buildable.

### Missing decision basis

A document that carries execution direction without linking to the governing
`DecisionRecord` entries that authorized that direction is incomplete. The basis
is asserted but not recoverable. It cannot be audited, superseded, or reviewed.

### Missing or stale ETR for technology assumptions

A document that names specific external technologies without linked ETR records
carrying version, source, and freshness classification is non-buildable against
those assumptions. Execution proceeds on unverified planning-time beliefs. If the
ETR exists but is classified `stale` or `unknown`, the document's technology
basis is no longer trustworthy until re-validation occurs.

### Open-ended scope

A scope description that requires V Forge to interpret what is in scope is not
execution-ready. Per handoff interface Validity Conditions: "the execution scope
is bounded — it is specific enough for V Forge to act within without requiring
unilateral scope interpretation." A document whose scope description is planning
framing rather than execution definition is still a planning document.

### Planning ambiguity carried forward

Unresolved decisions, open questions, or TBD items in the document are
execution-time ambiguities. Per `audit-evaluation-rules.md` Ambiguity Detection
Rules: material ambiguity affecting a constraint, a scope boundary, or a
structural rule fails audit. An implementation document with unresolved material
ambiguity will either block execution or cause V Forge to resolve the ambiguity
silently through scope interpretation — neither outcome is acceptable.

### Unresolved boundary ownership

A document that carries responsibilities spanning Project V, V Forge, and VEDA
without explicit system-ownership classification creates execution confusion. V Forge
must not be left to infer where its authority ends and planning or observatory
authority begins.

### Technology assumptions not grounded in current research

An implementation document may have been valid when authored. If it is activated
significantly later and its ETR references have become stale — due to elapsed time
or a relevant version release — the document's technology basis is no longer current.
Re-validation is required before the document can support a valid handoff activation.

### Free-floating markdown with no traceability

A markdown document with execution-sounding content but no linkage to planning
records, no `DecisionRecord` references, no ETR records, and no handoff package
reference is not a governed implementation document. It may reflect real planning
intent but has no traceability and cannot be audited.

### Return-to-planning triggers absent

A document without explicit return triggers leaves V Forge no governed path for
blocking conditions. This is a mandatory semantic field per the handoff interface.
Its absence is a validity failure.

### Fabricated readiness claims

A document that asserts execution readiness without a traceable readiness basis —
a reference to an actual Project V readiness evaluation — is carrying an
unsupportable claim. Per handoff interface What the Package Must Not Contain:
"fabricated readiness claims — the readiness basis must be traceable to actual
Project V readiness evaluation" is explicitly forbidden. This applies equally to
the implementation document.

---

## Relationship to Handoff

An implementation document is not the handoff package. The handoff package is a
governed Project V record with structured required fields. The implementation
document is the artifact the handoff package carries or references to provide
the narrative and bounded-execution-intent depth behind those structured fields.

The structured fields of the handoff package must be independently satisfiable.
The implementation document provides the executable detail that makes those
fields meaningful.

A valid handoff package without a linked implementation document may carry
sufficient structured fields to be technically valid under the interface contract.
But for non-trivial execution scope, the implementation document is what V Forge
will actually work from. An approved handoff that references only structured
metadata and no execution-ready implementation document is weak at the point
that matters most: what V Forge reads when execution begins.

---

## Relationship to ETR

ETR records are the evidence basis for technology assumptions an implementation
document carries. The document references ETR; it does not duplicate it.

Where the document carries a technology assumption, the reader must be able to
follow the reference to the ETR record and confirm: what version, what source,
when captured, and whether the freshness classification still supports the claim.

A document that summarizes ETR findings in-line without the reference breaks
the traceability chain. The summary may be accurate at the time of writing and
wrong by the time of activation. The reference is what allows freshness to be
evaluated.

---

## Relationship to Audit

The `implementation_readiness` audit type asks whether a target is ready to move
toward implementation. For that audit to produce a meaningful result, the
implementation document associated with the target must exist and satisfy the
minimum semantic contract.

Specific audit hard-failures that apply to implementation documents:

- **Missing implementation document where one is required for a non-trivial
  execution scope** is an implementation linkage posture failure per
  `audit-evaluation-rules.md`
- **ETR-backed technology assumptions in the document that are stale, unknown,
  or insufficiently attributed** trigger the `implementation_readiness` hard-failure
  condition for stale ETR
- **Ambiguous scope or unresolved TBD items** in the document trigger the
  material ambiguity hard-failure
- **Missing decision basis** for execution direction in the document surfaces as
  a cross-artifact consistency failure between the document and the
  `DecisionRecord` entries it should reference

The `hygiene` audit type may also surface implementation document drift — for
example, a document whose ETR references have aged into `stale` classification
without the document having been updated or the handoff having been re-validated.

---

## Relationship to Readiness

The Evidence Sufficiency Block in `readiness-evaluation-rules.md` is the
readiness gate most directly affected by implementation document quality.

When a work item or handoff is evaluated for readiness and the evaluation
depends on implementation-target assumptions:

- a missing implementation document where one is required for execution-target
  work is a hard-block condition
- an implementation document whose ETR references are materially stale or
  insufficiently attributed is a hard-block condition per the Evidence
  Sufficiency Block

A work item cannot be `ready` for handoff when its implementation document
fails the minimum semantic contract. The readiness system enforces this through
the Evidence Sufficiency Block, the ETR re-evaluation triggers, and the Audit
Gate Block when the relevant audits have been run.

---

## Relationship to Traceability

An implementation document is one of the key artifacts in the Project V
traceability chain.

Per `implementation-traceability.md` Traceability Chain Principle, a valid
traceability chain should preserve linkage across decisions, work items, ETR
references, handoff records, and audit results. The implementation document
is where those linkages are assembled into execution-ready form.

A document that breaks any link in that chain — missing decision references,
missing ETR references, no planning record linkage — creates invisible traceability
gaps. Those gaps may not be apparent until audit runs, until a return-to-planning
event requires reconstructing planning intent, or until a handoff is recalled and
the basis for the original scope cannot be recovered.

---

## Anti-Drift Rules

The following are forbidden drift patterns for implementation documents:

- an implementation document that has no linked planning records, decisions,
  or ETR records is not a governed implementation document regardless of its
  content
- a document that asserts technology assumptions without ETR references is
  carrying ungoverned claims
- a document that was valid at the time of authoring but is activated
  significantly later without re-validating ETR freshness is carrying
  potentially stale technology assumptions
- a document whose scope description requires V Forge to determine what is
  in scope has not reached the buildability threshold
- using an implementation document as a substitute for the governed handoff
  package record and its required structured fields is a boundary failure
- summarizing ETR findings in-line rather than referencing the ETR record
  breaks the traceability chain and prevents freshness evaluation
- drafting an implementation document before the underlying `DecisionRecord`
  entries exist produces a document that specifies direction that is not yet
  formally authorized
- a document stored only in a markdown file outside Project V's governed record
  structure, with no handoff package reference, is ungoverned prose

---

## Human-In-The-Loop Principle

Implementation documents are governance-sensitive because they define what V Forge
will build and are the artifact V Forge executes from.

Human review is especially important when:

- the execution scope is novel, large, or high-consequence
- the document carries significant technology assumptions requiring current ETR
- there is ambiguity about return-to-planning trigger conditions
- the document is being activated significantly later than it was authored, requiring
  ETR re-validation
- the document will form the basis of a Class B or Class C handoff approval

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- an implementation document is execution-ready planning truth, not prose about
  what planning intended
- it is owned by Project V and consumed by V Forge; ownership does not transfer
  when V Forge reads it
- it must carry linked planning records, decisions, ETR references, explicit
  scope, constraints, outcomes, and return triggers
- a document without these linkages is not a valid implementation document
  regardless of how complete its prose is
- technology assumptions without ETR references are ungoverned and must not be
  treated as grounded planning basis
- the buildability test is: can V Forge act from this document without loading
  the planning packet?

If an LLM produces or approves an implementation document that carries technology
assumptions without ETR linkages, scope descriptions that require V Forge
interpretation, or execution direction without `DecisionRecord` references, this
doctrine is failing.

---

## Usage

This document should be used:

- when authoring an implementation document to understand what it must contain
  before the handoff can be valid
- when reviewing an existing implementation document against the minimum
  semantic contract
- when running an `implementation_readiness` audit and determining what
  constitutes a hard-failure in the implementation document
- when evaluating whether an implementation document has reached the
  buildability threshold or is still planning prose
- when assessing whether ETR freshness in a document requires re-validation
  before handoff activation

---

## Related Docs

- `project-v.md`
- `data-boundaries.md`
- `implementation-traceability.md`
- `external-technology-research-doctrine.md`
- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `schema-authority.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../ecosystem/cross-system-boundaries.md`
