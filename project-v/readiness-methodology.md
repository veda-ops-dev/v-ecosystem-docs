# Readiness Methodology

## Purpose

This document defines how Project V evaluates readiness.

It exists to answer:

```text
What does Project V mean by readiness, how is readiness evaluated, and what rules prevent readiness from becoming vague theater?
```

Project V treats readiness as a first-class planning concern. Readiness is not a vibe. It is an inspectable judgment based on explicit criteria.

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- what readiness means inside Project V
- what can be evaluated for readiness
- what the evaluation must produce
- the core dimensions the methodology covers
- how readiness relates to BYDA audit and to state changes
- explainability and reproducibility requirements

---

## Out of Scope

This document does not define:

- the exact rule-by-rule evaluation logic (see `readiness-evaluation-rules.md`)
- the controlled vocabulary values for results and severities (see `controlled-vocabularies.md`)
- schema field details (see `schema-authority.md`)
- status transition rules (see `status-transitions.md`)

---

## System

- project-v

---

## Core Rule

A Project V record is ready only when the system can explain:

- what was evaluated
- what criteria were used
- what passed
- what failed
- what gaps remain
- what action becomes valid because of the result

If that basis is not recoverable, the readiness claim is weak and must not be trusted.

---

## What Readiness Is

Readiness is a bounded evaluation of whether a Project V record can legitimately move to the next planning or orchestration stage.

Readiness belongs to Project V because it is:

- planning truth
- gating truth
- orchestration truth

Readiness is not:

- observatory truth
- execution truth
- a substitute for implementation outcomes

---

## What Can Be Evaluated

Project V may evaluate readiness for:

- objectives
- initiatives
- work items
- handoffs
- planning packages where governed

The exact set may expand later through governed schema changes, but the methodology should remain stable.

---

## Evaluation Outputs

Every readiness evaluation must produce at minimum:

- evaluated entity reference
- evaluation type
- result (server-owned — callers may not set this)
- rule package or methodology reference
- summary
- created timestamp

Where conditions fail, the evaluation must also produce explicit `ReadinessGap` records.

---

## Core Evaluation Dimensions

The first-pass readiness methodology evaluates these dimensions where applicable.

### 1. Goal clarity

Can the system explain what outcome is being pursued?

Questions:
- Is the target outcome explicit?
- Is the scope bounded?
- Is the record specific enough to act on?

### 2. Structural completeness

Does the record have the required planning structure?

Questions:
- Are required fields present?
- Are required linked records present?
- Is the planning package structurally complete?

### 3. Dependency visibility

Are blocking dependencies visible and classified?

Questions:
- Are dependencies known?
- Are blockers explicit?
- Is hidden dependency risk still high?

### 4. Evidence support

Is there enough support for the planning claim being made?

Questions:
- Is supporting evidence linked where needed?
- Is the decision basis recoverable?
- Are key assumptions unsupported?

### 5. Boundary correctness

Is the work correctly classified as Project V, VEDA, or V Forge work?

Questions:
- Does the record stay inside Project V ownership?
- Is the target-system classification explicit where needed?
- Is the handoff boundary clear?

### 6. Execution-handoff readiness

If the work is intended to move toward execution, is the handoff basis actually sufficient?

Questions:
- Is the next target system known?
- Is the required package complete enough for handoff?
- Are unresolved blockers still present?

---

## Result Vocabulary

The first-pass readiness result vocabulary must remain small and explicit. Allowed values are defined in `controlled-vocabularies.md`:

- `ready`
- `not_ready`
- `ready_with_warnings`
- `deferred`

---

## Gap Vocabulary

Readiness gaps preserve concrete deficiencies found during evaluation. Required fields include:

- severity (see `controlled-vocabularies.md` for allowed values and rank order)
- description
- remediation guidance
- resolved state

---

## Explainability Rule

Every readiness result must be explainable. A reviewer must be able to answer:

- why this result happened
- which rule package was used
- what evidence or structure was missing
- what must change for the result to improve

Opaque pass/fail magic is not acceptable.

---

## Reproducibility Rule

If the same readiness evaluation is run against the same underlying state and the same rules, the result must be the same unless intentional nondeterminism is explicitly documented.

Readiness must favor reproducibility over cleverness.

---

## Advisory Rule

A readiness evaluation may produce advisory findings, warnings, or suggestions.

Those outputs must not silently mutate canonical planning truth.

Explicit action is still required for meaningful state change.

---

## Work Item Readiness State Sync Rule

`WorkItem.readinessState` is a server-managed summary field.

When a new readiness evaluation is created for a work item, the work item's `readinessState` must be updated in the same transaction to reflect the evaluation result.

The latest non-superseded readiness evaluation for that work item is the governing basis for the summary field.

If the current readiness basis is invalidated (because a required audit becomes stale or another material basis change occurs), the work item's `readinessState` must be reset to `unevaluated` until re-evaluation occurs.

This field exists as a summary for navigation and filtering. It must not replace the canonical readiness evaluation records.

---

## Relationship to State Changes

Readiness does not automatically equal a state transition.

A readiness result may justify a transition, but the transition itself must remain explicit where the domain requires it. Project V must not implement hidden behavior such as:

- evaluate and silently mark as approved
- evaluate and silently create handoff state
- evaluate and silently rewrite planning fields

---

## Archived-Parent Rule

Archived parents must freeze normal forward planning growth beneath them in the first pass.

That means:
- do not create new child objectives, initiatives, or work items under an archived parent record
- do not re-parent active child records under an archived parent
- status-history or governance-side actions may still occur where explicitly allowed

---

## Relationship to Handoffs

Handoff readiness is a special case.

A handoff should not be considered ready unless:
- the target system is explicit
- the work package is bounded
- critical gaps are visible
- the basis for transfer is recoverable

Project V may judge a handoff ready. It does not thereby become the owner of the execution truth that follows.

---

## Relationship to BYDA Audit

Readiness and BYDA audit are related but separate:

- readiness asks: can this move forward?
- BYDA asks: what was checked, what failed, what is ambiguous, what became stale?

Where a lifecycle stage requires audit, readiness must not ignore audit state. The specific coupling rules live in `readiness-evaluation-rules.md`.

Audit and readiness records must remain separate. They must not be silently collapsed into one undifferentiated family.

---

## Invalidation Rule

A readiness result may become stale when its governing basis changes materially.

Examples:
- a superseding decision changes scope or sequencing materially
- a required audit becomes stale
- a required audit changes from `warning` to `fail`
- evidence changes in a way that undermines the original basis

The first-pass system may represent invalidation by requiring re-evaluation rather than mutating readiness results into a separate stale status, but the invalidation behavior must remain explicit.

---

## Human-In-The-Loop Principle

Readiness that produces `ready_with_warnings` and requires operator approval to proceed must have that approval recorded explicitly. The mechanism for recording operator approval is defined in `readiness-evaluation-rules.md`.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- readiness is an inspectable, explicit judgment — not a vibe or a convention
- results are server-owned and must be explainable through recoverable fields
- audit and readiness are related but structurally separate
- a readiness result does not automatically trigger a state transition
- invalidation must be explicit when the governing basis changes materially

---

## Usage

This document should be used:

- as the methodology reference when implementing readiness evaluation logic
- when reviewing whether a readiness claim is sufficiently grounded
- when writing hammer tests for readiness behavior
- when writing more specific evaluation rule docs

---

## Related Docs

- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `byda-in-project-v.md`
- `schema-authority.md`
- `controlled-vocabularies.md`
- `status-transitions.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/testing-and-verification-doctrine.md`
