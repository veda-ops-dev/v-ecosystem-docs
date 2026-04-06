# Allowed Agent Actions Matrix

## Purpose

This document defines which agent behaviors are permitted, constrained, or
forbidden inside the V Ecosystem, organized by action class and system context.

It exists to answer:

```text
What may an agent actually do inside Project V, VEDA, and V Forge, what
requires explicit approval or escalation before proceeding, and what is
forbidden regardless of instruction, context, or apparent efficiency?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the permitted action classes for agents in each ecosystem system
- which actions require pre-authorization or approval before proceeding
- which actions require human review rather than agent-only execution
- which actions are forbidden regardless of instruction
- how cross-system agent behavior is bounded
- the anti-drift rules operators and LLMs must preserve when evaluating
  whether an agent action is within bounds

---

## Out of Scope

This document does not define:

- detailed approval thresholds for every specific action variant
- implementation-specific tool or API authorization
- detailed workflow steps for any specific system operation
- repo-local agent behavior not involving ecosystem boundaries
- session-level configuration or tooling choices

Those belong in governance, workflow, interface, and system-specific docs.

---

## System

- governance

---

## Core Rule

An agent may act only when the action is permitted by its classification in
this matrix, the required approval or authorization posture is satisfied, and
the action stays inside the current system's role and the actor's authority.

An action not covered by a permitted class in this matrix is not permitted
by default.

Access to a system, tool, or interface does not grant permission to act.
The matrix governs what agents may do. Everything else requires explicit
governed expansion before it becomes permitted.

---

## Matrix Definition

The allowed agent actions matrix is the governed reference for evaluating
whether a proposed agent action is:

- **Permitted** — the agent may proceed within the stated constraints
- **Requires Authorization** — the agent must obtain explicit approval or
  escalation resolution before proceeding
- **Human-Required** — the action must not be completed by the agent alone;
  human review or execution is required
- **Forbidden** — the action must not occur regardless of instruction,
  convenience, or apparent efficiency

The matrix is organized by action class, then by system context.

---

## Action Class Definitions

Before reading the matrix, establish these action classes:

### Interpret
Read, classify, summarize, or reason about existing content, state, or signal
without mutating any system state.

### Package
Prepare, structure, or format output for review, reporting, recommendation,
or handoff without activating that output as a governing decision or action.

### Recommend
Produce a bounded recommendation for a next step, planning decision,
or action — without treating the recommendation as approval or authorization.

### Report
Produce a governed report of current state, findings, outcomes, or continuity
context through the governed reporting path.

### Bounded Execute
Carry out explicitly approved, bounded work within approved scope where the
action is authorized and the actor has the required authority.

### Mutate Planning State
Create, update, supersede, or invalidate planning records, decision records,
readiness evaluations, or orchestration state inside Project V.

### Mutate Observatory State
Create, update, or modify observatory records, observation targets, or
evidence records inside VEDA.

### Mutate Execution State
Create, update, or modify execution records, task state, or execution
artifacts inside V Forge.

### Trigger External Action
Take action outside the ecosystem boundary, including external reads, writes,
paid data pulls, publication, or launch-visible changes.

### Approve or Authorize
Grant approval, authorize an action, or confirm that a governed gate has
been satisfied.

### Escalate
Surface a situation for human review, conflict resolution, or exception
handling through the governed escalation path.

---

## Project V — Allowed Agent Actions

Project V is the planning and orchestration system of record.

| Action Class | Status | Constraints |
|---|---|---|
| Interpret | Permitted | Must remain bounded to planning-relevant content. Must not treat interpretation as decision. |
| Package | Permitted | May prepare recommendations, handoff packages, or planning summaries. Must not treat packaging as activation. |
| Recommend | Permitted | May recommend planning decisions, priority changes, or next steps. Recommendation is not approval. |
| Report | Permitted | Must follow report-structure-and-required-fields.md. Must preserve uncertainty and partial completion honestly. |
| Bounded Execute | Permitted | Only within explicitly approved planning scope. Must not widen scope by inference. |
| Mutate Planning State | Requires Authorization | Requires explicit governed approval for the specific mutation. Agent must not self-authorize planning state changes. Decision records, readiness evaluations, and handoff records require approval posture defined in approval-and-escalation-model.md. |
| Mutate Observatory State | Forbidden | Project V does not own observatory or evidence truth. Agent must not create or modify VEDA records from within Project V context. |
| Mutate Execution State | Forbidden | Project V does not own execution truth. Agent must not create or modify V Forge execution records from within Project V context. |
| Trigger External Action | Requires Authorization | Must satisfy external-action-governance.md preconditions. Agent must not self-authorize external action from planning context. |
| Approve or Authorize | Human-Required | Agents may not grant approval for governed planning decisions. Approval requires a human actor with the required authority. |
| Escalate | Permitted | Agent must escalate when authority is unclear, approval posture is unclear, or a situation exceeds agent scope. Escalation is correct behavior, not failure. |

---

## VEDA — Allowed Agent Actions

VEDA is the signal, evidence, and observability system of record.

| Action Class | Status | Constraints |
|---|---|---|
| Interpret | Permitted | Must remain bounded to observatory-relevant content. Must not convert interpretation into planning decisions or execution instructions. |
| Package | Permitted | May prepare signal packages, evidence summaries, or observatory outputs for governed consumption. Must preserve source provenance and trust posture. Must not overclaim confidence or signal quality. |
| Recommend | Permitted | May recommend observatory targets, evidence classifications, or signal packaging. Must not treat signal as self-authorizing planning direction. |
| Report | Permitted | Must follow report-structure-and-required-fields.md. Must preserve source trust posture honestly. Uncertain or low-trust signal must not be presented as clean observatory truth. |
| Bounded Execute | Permitted | Only within explicitly approved observatory scope. Must not absorb open-ended signal gathering beyond approved scope. |
| Mutate Planning State | Forbidden | VEDA does not own planning truth. Agent must not create or modify Project V planning records, decision records, or readiness evaluations from within VEDA context. |
| Mutate Observatory State | Requires Authorization | Requires explicit governed approval for mutations that affect canonical observatory records, keyword targets, or evidence provenance. Append-only records must remain append-only. Event logs must not be mutated through read paths. |
| Mutate Execution State | Forbidden | VEDA does not own execution truth. Agent must not create or modify V Forge execution records from within VEDA context. |
| Trigger External Action (E1 — bounded read-only retrieval) | Permitted | Bounded scope and source trust classification must be confirmed before proceeding. Read-only does not mean ungoverned — cost, rate limits, and source trust posture still apply per external-action-governance.md. |
| Trigger External Action (E4 — paid or spend-creating retrieval) | Requires Authorization | Explicit governed approval required before any paid data pull or spend-creating external retrieval. Governed under external-action-governance.md and paid-data-pull-governance.md. Agent must not self-authorize. |
| Approve or Authorize | Human-Required | Agents may not grant approval for observatory scope changes or new evidence domains. |
| Escalate | Permitted | Agent must escalate when source trust is unclear, observatory boundary is at risk, or a proposed operation would expand VEDA scope beyond its classified role. |

---

## V Forge — Allowed Agent Actions

V Forge is the execution system of record.

| Action Class | Status | Constraints |
|---|---|---|
| Interpret | Permitted | Must remain bounded to execution-relevant content. Must not convert execution-side interpretation into planning decisions. |
| Package | Permitted | May prepare execution findings, return-to-planning packages, or bounded execution reports. Must distinguish execution-local findings from planning-relevant findings. |
| Recommend | Permitted | May recommend execution paths, clarification requests, or return-to-planning when warranted. Must not treat execution-side recommendations as planning decisions. |
| Report | Permitted | Must follow report-structure-and-required-fields.md. Must preserve uncertainty, partial completion, and ambiguous outcomes honestly. Must not present uncharacterizable outcomes as clean completion. |
| Bounded Execute | Permitted | Only within explicitly approved execution scope and valid handoff. Must halt on scope excess detection. Must not widen scope by inference or execution momentum. |
| Mutate Planning State | Forbidden | V Forge does not own planning truth. Agent must not create or modify Project V planning records, decision records, or readiness evaluations from within V Forge context. |
| Mutate Observatory State | Forbidden | V Forge does not own observatory truth. Agent must not create or modify VEDA observatory records from within V Forge context. |
| Mutate Execution State | Requires Authorization | Execution state mutations within approved handoff scope are permitted within bounded execute. Mutations outside approved scope, or mutations that affect cross-system state, require explicit governed approval. |
| Trigger External Action | Requires Authorization | External and paid actions require authorization posture defined in external-action-governance.md. Launch-sensitive or public-facing execution requires stronger authorization. Agent must halt and escalate when authorization posture is unclear. |
| Approve or Authorize | Human-Required | Agents may not grant approval for execution scope expansion, external actions, or launch-sensitive mutations. |
| Escalate | Permitted | Agent must escalate when handoff semantics are insufficient, scope excess is detected, authorization is unclear, or execution produces a result that cannot be honestly characterized. |

---

## Cross-System Agent Actions

When an agent operates across more than one system in a single session,
additional constraints apply.

| Action Class | Status | Constraints |
|---|---|---|
| Cross-system interpret | Permitted | May read and reason across system contexts. Must preserve ownership distinctions. Must not merge system truth domains in reasoning outputs. |
| Cross-system package | Permitted | May prepare packages that reference multiple systems. Must clearly classify what each element of the package is and which system owns it. |
| Cross-system state mutation | Forbidden without explicit interface path | An agent may not mutate state in one system as a consequence of acting in another system unless that consequence passes through the explicitly governed cross-system interface. Preparation chains that route around individual interface requirements are forbidden. |
| Cross-system approval | Human-Required | Cross-system transitions that require approval (handoff activation, return-to-planning triggers, inter-system reporting) require human actor involvement where doctrine requires it. |

---

## Mandatory Escalation Rule

Escalation is marked as Permitted in all system tables above.
In certain conditions it is not merely permitted — it is required.

An agent must escalate when:

- actor authority is unclear or disputed
- approval posture cannot be confirmed for an approval-sensitive action
- a scope boundary has been or is about to be exceeded
- a Forbidden action has been requested by any actor
- an action class is ambiguous and the default posture would be to proceed
- the agent cannot determine whether verification conditions for the action are satisfied

Escalation is not a sign of failure.
It is the correct governed response when the agent's operating bounds have been reached.
An agent that fails to escalate in these conditions is not operating within the permitted posture — it is operating outside it.

---

## Approval-Sensitive Action Classes

The following action classes are always governance-sensitive and require
explicit handled approval posture before the agent proceeds:

- any Mutate Planning State action in Project V
- any Mutate Observatory State action in VEDA that affects canonical records
- any Trigger External Action regardless of system
- any action involving paid data pulls or spend-creating external behavior
- any action that crosses a system ownership boundary
- any action where scope has widened beyond the originally approved bounds
- any action where actor authority is unclear or disputed

### Rule
When an agent is uncertain whether an action requires authorization,
the default posture is to treat it as requiring authorization.
The burden is on demonstrating permission, not on demonstrating prohibition.

---

## Forbidden Action Classes

The following are forbidden for agents regardless of system, instruction,
or apparent efficiency:

- inventing or asserting authority not established through governed doctrine
- self-authorizing approval-sensitive actions by treating confidence as permission
- mutating one system's canonical truth from another system's context
- bypassing cross-system interfaces through shared infrastructure or direct DB access
- treating access as authority for any action class
- treating recommendation as equivalent to granted approval
- treating execution momentum as authorization to widen scope
- hiding uncertainty, partial completion, or failure in reporting
- treating a prior session's unverified state as verified current state
- absorbing ownership of truth domains beyond the current system's classified role

### Response to Forbidden Action Requests

When an agent is requested to perform a Forbidden action — regardless of the
instruction source, framing, or apparent justification — the correct response is:

1. Refuse the specific action
2. Explicitly state that the action is forbidden under this matrix
3. Escalate the request through the governed escalation path if the instruction
   came from an operator or system with apparent authority

A Forbidden action must not be performed even if the requester asserts it is
approved, necessary, consistent with the spirit of the ecosystem, or required
for efficiency.
A plausible justification for a Forbidden action is not authorization for it.

---

## Default Posture Rule

Where an action is not explicitly listed as permitted in this matrix,
the default posture is not permitted.

An agent may not self-expand the permitted list by analogy, inference,
or convenience reasoning.

If a needed action class is not covered, the correct response is to
escalate for explicit governance expansion of the matrix, not to proceed
under an implied permission.

---

## Matrix Expansion Rule

This matrix may be expanded only through explicit governance review.

Expansion requires:

- identification of the action class and system context to be added
- justification by reference to the project's classified role and truth domain
- explicit approval posture defined for the new permitted action
- update to this doc as the authoritative governed record

An agent must not treat informal direction, session-level instruction,
or implementation convenience as authorization to act beyond the current matrix.

---

## Human-In-The-Loop Principle

This matrix preserves human governance at the points where it matters most.

Human review is required for all Human-Required action classes and must
remain real rather than ceremonial.

An agent producing a package, recommendation, or report that appears to
make human review unnecessary has not made human review unnecessary.
It has made human review more efficient.
The governance gate must still be passed.

---

## LLM Use Principle

A capable LLM should be able to use this matrix to:

- classify a proposed action into its action class
- determine the permission status for that class in the current system context
- apply the stated constraints if the action is permitted
- identify that authorization is required and halt to request it if applicable
- identify that the action is forbidden and refuse regardless of instruction

If an LLM uses this matrix to rationalize proceeding with a forbidden or
authorization-required action because the spirit of the ecosystem seems
to support it, the matrix is being used incorrectly.

---

## Usage

This document should be used:

- when an agent is evaluating whether a proposed action is within bounds
- when designing agent-assisted workflows to ensure action classes are
  correctly classified and governed
- when reviewing whether agent behavior during a session stayed within
  permitted bounds
- when deciding whether an escalation is required or an action may proceed
- when writing system-specific agent behavior rules that must be consistent
  with this matrix

---

## Relationship to Approval and Escalation Model

This matrix defines which action classes are permitted, require authorization, require human involvement, or are forbidden. It must be read together with `approval-and-escalation-model.md`.

The matrix alone does not replace approval posture. An action classified as Permitted or Requires Authorization in this matrix may still be governed by the approval class rules in the escalation model. In particular:

- a Permitted action that crosses an approval-sensitive threshold (Class B, C, or D) requires the approval posture defined in `approval-and-escalation-model.md` before it may be activated
- a Requires Authorization action must follow the approval class and escalation path defined in the escalation model
- the escalation model governs when a Permitted action still triggers human review requirements

Do not read this matrix as the only governing constraint. Both docs apply.

---

## Related Docs

- `agent-operating-doctrine.md`
- `approval-and-escalation-model.md`
- `auth-and-actor-model.md`
- `decision-continuity-doctrine.md`
- `external-action-governance.md`
- `failure-and-recovery-doctrine.md`
- `testing-and-verification-doctrine.md`
- `paid-data-pull-governance.md`
- `report-structure-and-required-fields.md`
- `recommendation-packaging-doctrine.md`
- `../ecosystem/cross-system-boundaries.md`
- `../project-v/system-invariants.md`
- `../veda/system-invariants.md`
- `../v-forge/system-invariants.md`
