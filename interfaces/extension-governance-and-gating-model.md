# Extension Governance and Gating Model

## Purpose

This document defines how governance-sensitive actions, approvals, gating, activation, blocking, and persisted approval state work inside the V Ecosystem VS Code extension.

It exists to answer:

```text
What kinds of extension-side actions exist, how are they classified for gating, what must happen before a governance-sensitive action becomes active, what must be persisted, what invalidates a pending approval, what happens when context changes between recommendation and activation, and what must be enforced structurally rather than trusted to operator or model behavior?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the extension-side action classification model
- the gating rules that apply to each action class
- the definitions of review, recommendation, approval request package, activation event, and execution
- what must happen before Class B and Class C actions become active
- what must be persisted for governed actions to be reviewable
- what invalidates a pending or prior approval
- how rejection and non-acceptance must be handled
- how stale approval, stale recommendations, and changed context are handled
- how conflict in approval state or between bounded model outputs is handled
- structural enforcement requirements

This document builds on `extension-llm-behavior-contract.md`, which defines the LLM's bounded operating posture. That posture is active and binding here. This document defines the governance mechanics that enforce it.

---

## Out of Scope

This document does not define:

- the visual design of the extension UI beyond what governance requires
- specific MCP tool schemas
- detailed workflow-stage mechanics beyond what gating requires
- credential or authentication mechanics
- implementation-specific storage formats

---

## System

- interfaces

---

## Core Rule

An extension-side action becomes active only when every required governance condition for its class has been explicitly satisfied and persisted.

A prepared action is not an active action.
A reviewed action is not an approved action.
An approved action is not an activated action unless activation has occurred through the governed path.
Conversational statements, model confidence, and operator presence are not governance conditions.

---

## Extension Action Classes

Every interaction inside the extension falls into one of the following classes. Classification determines what gate, if any, must be satisfied before the action may proceed.

### Class A — Read-Only, Non-Mutating, In-Bounds Support

Examples:
- loading and displaying planning context, signal summaries, execution state
- interpreting or summarizing records without proposing next steps
- producing finding reports, review summaries, continuity reminders, and uncertainty notices
- running readiness checks in read-only mode
- displaying evidence and decision context
- searching records, browsing planning trees, reviewing gaps

**Gate:** No gate required.

**Rule:** Class A actions may proceed within current doctrine, session scope, and system boundaries without additional approval. Class A actions must not produce side effects or silent state mutations. A read action that produces a side effect is misclassified.

---

### Class B — Bounded, Reviewable Mutation or Governed Transition

Examples:
- creating a new project, objective, initiative, or work item
- executing a governed status transition (e.g., `proposed → active`, `active → completed`)
- activating an intake outcome that changes planning status
- creating a decision record
- preparing or activating a handoff
- returning execution findings into a planning-affecting path
- creating or marking audit runs
- evaluating and recording readiness outcomes
- creating or resolving readiness or audit gaps

**Gate:** Persisted operator approval required before the action becomes active.

**Rule:** Class B actions require an explicit operator approval event persisted to the database before the downstream API call is permitted. Conversational approval does not satisfy this gate. Operator presence in the session does not satisfy this gate. A recommendation package covering the action does not satisfy this gate. The gate is satisfied only when the approval record exists.

**Doubt-default rule:** When an action's class is ambiguous between A and B, treat it as B and require the gate.

---

### Class C — External, Paid, Launch-Sensitive, High-Impact, or Irreversible Action

Examples:
- launch activation for any public-facing or externally visible execution
- paid data pull authorization
- external publication, distribution, or outbound communication actions
- scope expansion beyond the approved handoff bounds
- actions that create financial, legal, or reputational consequence
- return-to-planning activation that materially affects planning direction
- handoff activation with high external risk

**Gate:** Persisted operator approval required, plus typed confirmation for irreversible actions.

**Rule:** Class C actions require all of the following before proceeding:
- a persisted approval record
- the approving actor is identifiable and has the required authority
- the approval covers the current specific scope, not a general category
- no material change has occurred since the approval basis was established
- for irreversible actions, typed operator confirmation (not a single-click) is required as an additional gate

Class C approval is not generic. Approval of one Class C action does not cover another, even if they appear similar.

---

### Class D — Doctrine-Unclear, Boundary-Exceeding, or Exception Action

Examples:
- actions that appear to require doctrine exceptions or overrides
- actions that route around normal interface or approval paths
- actions that depend on ambiguous authority
- requests to merge system roles or collapse system ownership
- actions where the class cannot be confidently determined

**Gate:** Escalation required. Must not proceed as normal work.

**Rule:** Class D actions must surface the conflict or ambiguity explicitly, withhold the action, and escalate through the governed path. The extension must make the escalation visible to the operator and preserve the reason. Class D is not a failure state — it is the correct response to situations the current governance posture cannot safely resolve.

---

## Gating Model

The gating model defines what kind of confirmation is required before an action in each class may proceed.

| Class | Gate Type | Persistence Required | Conversational Approval Accepted |
|---|---|---|---|
| A | None | No | N/A — no gate |
| B | Operator approval event | Yes — approval record | No |
| C | Operator approval event + typed confirmation for irreversible actions | Yes — approval record, confirmation log | No |
| D | Escalation | Yes — escalation record | No |

No row in this table says yes to conversational approval. That column exists to make the answer explicit. Conversational approval is not a gate mechanism for any class.

---

## Distinction: Review, Recommendation, Approval Request Package, Approval Event, Activation

These are not the same thing. The extension must treat them as distinct at every layer.

### Review
An operator or LLM examines a record, package, finding, or context without initiating any state change. Review is Class A. The record examined does not change as a result. No persisted approval event occurs. A button labeled "Review" must not silently write state.

### Recommendation
A bounded proposed course of action produced by the LLM and packaged per `recommendation-packaging-doctrine.md`. A recommendation is inert. It exists as a structured output in the extension. It does not become a database record, a state change, or an approval merely by being produced or displayed. An operator reading a recommendation and feeling that it is correct does not activate it.

### Approval Request Package
A structured artifact produced by the LLM — or assembled by the extension — that requests operator approval for a specific Class B or Class C action. The Approval Request Package contains the action being requested, the scope, the basis, what approval covers, and what the default state is if approval is not granted. An Approval Request Package is not itself an approval. It is the input to the governed approval event.

### Approval Event
An explicit operator action — through the extension's governed approval gate — that creates a persisted approval record in the database. The approval event is what satisfies the governance gate. It is:
- explicit (requires deliberate operator action, not conversational statement)
- persisted (written to the database before the downstream action is permitted)
- bounded (covers the specific action and scope identified in the approval request package)
- attributable (actor identity is preserved with the record)
- reviewable (a later reviewer can determine what was approved, by whom, and when)

An approval event that cannot satisfy all five conditions is not a valid governed approval.

### Activation
The governed API call that makes a previously approved action active. Activation occurs only after a valid approval event has been persisted. The API enforces this — not the UI, not the model, not a soft check. The extension's activation path must call the API only after confirming the approval record exists. If the API rejects the activation because the approval record is missing or invalid, that is the correct behavior. The UI must surface that rejection explicitly, not retry or route around it.

### Execution
The downstream system behavior that follows activation. Execution is V Forge's domain for execution-class work. Activation is the last step the extension owns. What follows is V Forge execution truth.

---

## Persisted State Requirements

The following must be persisted for governed actions to remain reviewable.

### For every Class B action:
- approval record: action identified, scope bounded, actor identified, timestamp, approval granted or denied
- if denied: reason preserved, continuity state updated (see Rejection section)
- if granted: downstream activation may proceed when the approval record is confirmed

### For every Class C action:
- all Class B requirements plus:
- typed confirmation log for irreversible actions
- evidence basis at time of approval (what signal and decisions informed the approval)
- explicit scope of what the approval covers

### For every Class D escalation:
- escalation record: what triggered it, what action was withheld, what authority or doctrine question was unclear, what the expected resolution path is

### For approval events generally:
The persisted approval record must be sufficient to answer, after the fact:
- what action or transition was approved
- who approved it
- what scope the approval covered
- what conditions or limits applied
- whether the approval is still active, expired, revoked, or superseded

If those questions cannot be answered from the persisted record, the approval record is insufficient.

---

## What Must Be Blocked

The extension must block, not merely warn, when:

- a Class B or Class C action is attempted without a persisted approval record
- a Class D condition is detected and escalation has not been initiated
- an approval scope is being widened beyond what was persisted
- an activation is attempted for an action whose approval has expired, been revoked, or become stale
- a button or command in the wrong system surface is invoked (e.g., "Create Planning Record" from V Forge, "Configure Observatory" from Project V)
- an action attempts to advance past a blocked state that has not been cleared through the governed path

"Block" means the action cannot complete. A warning that can be dismissed without satisfying the gate is not a block. A confirmation dialog followed by an API call that accepts the action regardless of approval record state is not a block. A real block is one where the action fails if the governance condition is not met.

---

## Approval Invalidation: What Makes a Pending or Prior Approval No Longer Valid

An approval is no longer valid when any of the following are true:

### Scope changed materially
The action being approved has grown, contracted, or changed from what the approval covered. The original approval does not cover the new scope. A new approval is required.

### Planning basis changed materially
A governing decision was superseded, invalidated, or created after the approval was granted, in a way that is relevant to the approved action. The prior approval was made under different governing context and must not be treated as still applying.

### Evidence changed materially
The signal or evidence that supported the approval basis has become stale or has been contradicted by new signal. For Class C actions especially, approval granted under a particular evidence state cannot be reused when that evidence has materially changed. The Evidence Currency Principle from the launch readiness workflow applies.

### Workflow stage changed
The ecosystem has moved to a different workflow stage since the approval was granted. An approval that was valid at a prior stage does not automatically carry forward to a later or changed stage.

### Approval explicitly revoked
The operator has explicitly revoked the prior approval through the governed path. Revocation must be persisted. It is not enough for the operator to say "never mind" in conversation.

### Time has passed beyond a reasonable horizon for the action type
An approval that was granted but never activated within a reasonable horizon for the relevant action type should be treated as requiring reconfirmation before activation proceeds. The extension should surface an expiry warning and require explicit reconfirmation rather than silently reusing a stale approval.

### Rule
When any of the above conditions is detected, the extension must:
- surface the invalidation condition explicitly to the operator
- block activation until the invalidation is addressed
- not treat the original approval as still applying
- not allow the LLM to reason around the invalidation

---

## Changed Context Between Recommendation and Activation

There is always some gap between when a recommendation is produced and when the operator acts on it. Context can change in that gap. The extension must handle this explicitly.

### Detection
Before presenting the approval gate for a Class B or Class C action, the extension checks whether context has changed materially since the recommendation was produced. Relevant changes include:
- a new or superseded governing decision
- a readiness state change
- new gaps opened at blocking or critical severity
- a significant change in VEDA signal for the scope being approved
- workflow stage change

### Behavior when change is detected
The extension presents the operator with a visible notice before the approval gate:

```
CONTEXT HAS CHANGED SINCE THIS RECOMMENDATION WAS PRODUCED
Changed: [what changed]
Basis of recommendation may be affected.
Review the updated context before approving.
```

The approval gate remains available but the operator sees this notice first. The recommendation is not automatically invalidated — the operator decides whether the change is material. But the extension does not silently proceed as if nothing changed.

### Behavior when change is severe
If the change is severe enough to make the recommendation basis clearly invalid (e.g., a governing decision was superseded that the recommendation depended on), the approval gate must be blocked until the recommendation is re-evaluated and a new recommendation is produced reflecting the current context.

---

## Rejection and Non-Acceptance

Rejection is a governed outcome, not a null event. The extension must treat it accordingly.

### When a recommendation is rejected
The operator explicitly dismisses or rejects the recommendation. The extension must:
- remove the inert recommendation from the active panel
- create a bounded rejection record if the rejection is continuity-relevant (e.g., the same recommendation has been surfaced before or the rejection affects future planning)
- surface a brief reason prompt — optional for the operator but logged if provided
- not re-surface the same recommendation in the same session unless the operator explicitly requests reprocessing

### When an approval request is rejected
The operator denies the approval request at the approval gate. The extension must:
- write a persisted rejection record (what was denied, by whom, when, and why if provided)
- block the downstream action
- surface a continuation options panel: revise and resubmit, defer, escalate, or take no action
- not treat the rejected action as informally proceeding — rejection is not soft non-approval

### When a Class C activation is denied at the typed confirmation step
The operator does not complete the typed confirmation. The extension must:
- treat this as a denial
- not log it as an approval event
- not activate the action
- preserve the approval request package as still pending if the operator may want to return to it
- or explicitly close the approval request if the operator signals they are done

### Rejection continuity
Where a rejection is relevant to future planning or future sessions, the rejection must be findable. A rejected handoff, a denied launch authorization, or a rejected intake outcome must appear in the relevant record's history. Future sessions should be able to see "this was proposed and rejected" without having to reconstruct it from conversation.

---

## Stale Recommendation Handling

A recommendation that sat in the extension panel for a significant period without operator action may no longer reflect current context. The extension handles this as follows:

### Staleness detection
The extension tracks when each recommendation was produced. After a configurable threshold relevant to the action type, the recommendation is marked stale.

### Stale behavior
A stale recommendation:
- remains visible but displays a staleness indicator
- cannot proceed directly to approval — the operator must first acknowledge the staleness
- prompts the LLM to re-evaluate before proceeding if the operator wants to continue

### Rule
Stale recommendations do not auto-close. The operator must explicitly dismiss or reactivate them. Silent expiry of recommendations would create continuity failures — the operator would not know whether a recommendation was acted on, deferred, or simply forgotten.

---

## Conflict Handling

### Recommendation conflicts with prior governing decision
When the LLM produces a recommendation that conflicts with an active governing decision, the extension surfaces a conflict notice before the approval gate:

```
GOVERNING DECISION CONFLICT DETECTED
Recommendation may conflict with: [decision ID and title]
Review this decision before approving.
[View Decision] [Acknowledge and Proceed to Approval] [Cancel]
```

"Acknowledge and Proceed" requires the operator to explicitly confirm they have reviewed the conflict. Their acknowledgment is logged. This does not override the approval gate — the operator still goes through the full approval event.

### Conflicting or unclear approval state
When approval state is ambiguous — for example, a prior approval appears to apply but scope may have changed, or two approval events seem to conflict — the extension must:
- surface the ambiguity explicitly
- block activation
- require the operator to resolve the conflict through the governed path (confirm one approval, revoke another, or produce a new approval)
- not attempt to resolve approval conflict by defaulting to the more permissive interpretation

### Multiple model outputs in conflict
When multiple LLM sessions or multiple models have produced recommendations that conflict with each other, the extension treats each as an independent inert recommendation. One model's recommendation does not override or invalidate another's. The operator evaluates them independently. No model output is privileged. If both cannot be activated simultaneously, the operator resolves the conflict. The extension does not merge them or silently choose one.

---

## Multi-Model Governance Neutrality

All of the following apply regardless of which model produced an output:

- a more capable model's recommendation is still an inert recommendation
- a more confident model's approval request package is still an approval request — not an approval
- one model's output is not another model's approval
- model identity does not change the action class of any output
- model identity does not relax any gate
- the extension applies the same gating rules regardless of which model produced the relevant output

The extension does not record model identity as a governance factor. Model identity may be logged for audit and debugging purposes, but it does not affect whether the governance gate is required or how it must be satisfied.

---

## Structural Enforcement Requirements

The following must be enforced by API, data model, and extension architecture — not trusted to operator discipline or model behavior.

### 1. API must reject activation without persisted approval record
The API must return an error when a Class B or Class C activation is attempted without a valid persisted approval record for the specific action and scope. The extension surfaces this error. There is no silent fallback.

### 2. Approval records must be written before activation calls are made
The extension's activation path must: (a) write the approval record, (b) confirm the write succeeded, (c) then call the activation API. If the write fails, activation must not proceed.

### 3. Cross-project scope must be enforced at the API layer
The session token enforces project scope at the API. The extension cannot activate a Class B or C action in a project other than the one bound to the current session token. This is not a UI-level check — it is an API enforcement requirement.

### 4. System surface restrictions must be enforced by UI construction
The V Forge panel must not contain buttons or commands that initiate planning-level state changes. The Project V panel must not contain buttons or commands that configure observatory scope. The VEDA panel must not contain buttons or commands that initiate execution or planning decisions. These restrictions are enforced by which commands exist in which surfaces, not by a warning that appears when the operator clicks the wrong thing.

### 5. Typed confirmation must be a separate UI input
For irreversible Class C actions, typed confirmation must be a distinct input element (text field requiring a specific phrase) rendered after the approval gate has been satisfied. It must not be a checkbox. It must not be pre-populated. It must not be dismissible without completing the input.

### 6. Stale approval detection must run before the approval gate is presented
The extension checks the approval request package against current context before presenting the approval gate widget. If staleness is detected, the staleness notice is displayed before the gate. The operator cannot see the approval gate without first seeing the staleness notice.

### 7. Rejection records must be persisted, not conversational
When an operator rejects an approval request, the rejection is written to the database with the same persistence requirements as an approval event. Rejection is not a UI-only interaction.

### 8. Escalation records must be persisted when Class D conditions are detected
When the extension identifies a Class D condition and blocks the action, the escalation event is persisted. The operator must be able to find, in a later session, that a specific action was blocked and escalated rather than discovering it by noticing missing state.

---

## Safe Usefulness Principle

Governance gates must not make the extension useless. The extension must remain a powerful operating surface for the operator and the LLM.

The gates apply specifically to actions that change governed state or cross governance thresholds. They do not apply to reasoning, analysis, synthesis, conflict detection, evidence interpretation, continuity surfacing, or any Class A activity.

The LLM must remain able to:
- produce detailed analysis of planning state, evidence, and execution findings
- detect and surface decision conflicts before the operator acts
- package complete and honest approval request packages and recommendations
- surface stale context, gap conditions, and approval posture questions
- produce continuity reminders that improve operator decision quality

None of that requires removing governance gates from Class B and C actions. The goal is a powerful bounded participant, not a weak one. The gates are what preserve the boundary between helpfulness and authority.

---

## Human-In-The-Loop Principle

Human approval remains real because the gates make it real.

If the gates can be satisfied conversationally, approval becomes theater. If the gates require persisted approval events that cannot be produced by conversational statements or model confidence alone, approval remains a meaningful governance mechanism.

The extension's job is to make it easy for operators to provide real governed approval when it is warranted, and structurally impossible for approval to be inferred from anything other than a deliberate governed approval event.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- every action in the extension has a class and a gate that matches that class
- Class B and C actions require persisted approval records — not conversational agreement
- reviewing a package, recommendation, or record does not activate it
- an approval request package is not an approval
- an approval event is distinct from activation
- activation is distinct from execution
- context that changed between recommendation and approval must be surfaced before the gate is presented
- rejection must be persisted, not silently absorbed
- stale approvals must be detected and surfaced, not silently reused
- conflicting approval state must block activation, not default to the more permissive interpretation
- model identity does not affect any gate or any action class
- structural enforcement exists and is not circumventable through conversational framing

If a model treats operator presence or session context as sufficient to activate a Class B or C action, this governance model is being violated.

---

## Usage

This document should be used:

- when designing extension UI interactions to identify which gate applies to each interaction
- when designing the API to enforce approval record requirements before activation
- when reviewing whether a proposed UX flow correctly distinguishes review from approval from activation
- when evaluating whether a rejection, stale approval, or changed-context condition is being handled correctly
- when designing the persisted state model for approval events and rejection records
- when auditing extension sessions for governance drift
- as the governance spine for later detailed interaction-model docs

---

## Related Docs

- `extension-llm-behavior-contract.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/auth-and-actor-model.md`
- `../governance/recommendation-packaging-doctrine.md`
- `../governance/report-structure-and-required-fields.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/external-action-governance.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/testing-and-verification-doctrine.md`
- `mcp-coordination-model.md`
- `operator-surface-interfaces.md`
- `../workflows/handoff-workflow.md`
- `../workflows/launch-readiness-workflow.md`
- `../workflows/maintenance-and-replanning-workflow.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
