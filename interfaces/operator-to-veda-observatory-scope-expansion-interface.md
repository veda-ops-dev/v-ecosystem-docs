# Operator to VEDA Observatory Scope Expansion Interface

## Purpose

This document defines the governed interface by which an operator directs VEDA
to expand, narrow, adjust, retarget, or otherwise change its observatory scope.

It exists to answer:

```text
Who may initiate an observatory scope change, under what authority posture,
what must a valid scope change request contain, how does VEDA respond, what
external-action and cost constraints apply, and how does this interface stay
distinct from bounded evidence access and signal delivery paths?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- who may initiate an observatory scope change request to VEDA
- the authority and approval posture required before a request may be issued
- the minimum semantic contents of a valid scope change request
- the change categories this interface covers
- validity conditions for requests
- VEDA's response obligation
- degraded-mode and recovery behavior
- activity trail requirements
- cost and external-action posture
- the boundary between this interface and adjacent evidence and signal paths

---

## Out of Scope

This document does not define:

- VEDA internal observatory implementation, provider configuration, or ingestion mechanics
- the specific MCP tool schemas for request delivery
- provider-specific data formats or API contracts
- the bounded evidence request path from Project V to VEDA — that is governed by
  `project-v-to-veda-evidence-request-interface.md`
- V Forge's active evidence query path — that is governed by
  `v-forge-evidence-access-contract.md`
- VEDA's startup signal delivery to V Forge — that is governed by
  `veda-to-v-forge-signal-interface.md`
- V Forge's return-to-planning path — that is governed by
  `v-forge-to-project-v-return-to-planning-interface.md`
- the full approval mechanics model — that belongs in
  `../governance/approval-and-escalation-model.md` and
  `../governance/approval-mechanics-seam-model.md`

---

## System

- interfaces

---

## Core Rule

Observatory scope change is an operator-governed action. It is not a V Forge
command. It is not a Project V planning request. It is not an automatic consequence
of a signal gap finding.

**Only a human operator, or Project V acting through the governed operator-facing
surface with explicit human operator approval, may direct VEDA to change observatory
scope through this interface.**

V Forge never directly invokes this interface. V Forge surfaces signal gap needs
upstream through the governed return-to-planning path. Project V may carry those
needs into an operator review. The operator decides whether to authorize a scope
change. If authorized, Project V may route the request through this interface on
the operator's behalf — but only after the operator has approved the scope change.
The operator authority is not delegated away; Project V is a governed conduit
when acting in this capacity, not an independent authority.

Technical capability to expand observatory scope does not authorize it.
A V Forge execution finding that identifies a signal gap does not authorize it.
A planning determination by Project V that more signal would be useful does not
authorize it.

Only a governed operator decision authorizes observatory scope change.

---

## Access Model

**This interface uses operator-authorized request delivery to VEDA, with VEDA
as the implementing authority.**

### Who may initiate

Two initiation paths are valid:

**Path A — Direct operator initiation:**
A human operator issues the scope change request directly through the governed
operator surface. The operator is both the initiating actor and the approving
authority. No upstream system mediation is required.

**Path B — Project V-mediated with explicit operator approval:**
Project V routes a scope change request through this interface after a planning
review, replanning cycle, or return-to-planning processing has surfaced a
specific scope gap, and a human operator has reviewed and approved the scope
change. In this path:

- Project V is the proximate initiating actor on the interface
- the request must carry the operator approval reference that authorized it
- the operator approval must precede the request delivery — Project V must not
  pre-send the request and obtain approval later
- Project V does not hold independent authority to direct VEDA scope change; the
  operator approval is the governing authority
- the request records both Project V as the proximate initiator and the operator
  as the approving authority

**Who may NOT initiate:**

- V Forge may not initiate this interface under any conditions
- VEDA may not self-authorize scope changes through this interface
- system processes may not self-generate scope change requests without operator approval
- agents may not self-authorize scope change as a consequence of evidence gap detection

### Who receives

VEDA receives and processes the request. VEDA implements observatory scope changes
within its own authority domain. VEDA may accept, narrow, defer, or reject a request
based on its implementability and the boundedness of the requested change.

---

## Valid Use Conditions

This interface is appropriate when:

- a return-to-planning or execution finding reveals that VEDA is not currently
  observing a signal class or source that ongoing governance requires, and an
  operator has reviewed that finding and determined a scope change is warranted
- an operator independently determines that additional observatory coverage is
  needed for a project, portfolio, or governance concern
- a planning or replanning review determines that observatory scope must be expanded,
  narrowed, retargeted, or refreshed to support current planning reality
- a launch readiness or post-launch observation cycle identifies a coverage gap
  that VEDA is not currently addressing, and an operator determines that gap
  must be filled through governed observatory expansion

---

## Out-of-Bounds Uses

This interface must NOT be used:

- as a substitute for a bounded evidence request when the need is for specific
  existing evidence, not an ongoing observatory change
- as a way for V Forge to self-authorize broader evidence access by routing a
  request upstream and then consuming the resulting expansion
- as a casual instruction to "go watch more stuff" without a bounded scope definition
- to mutate VEDA's observatory internals in ways that go beyond the scope and
  change type authorized in the request
- to create ongoing unbounded observatory monitoring without a defined scope,
  project context, and review posture
- as a backdoor around the evidence access contract or signal delivery paths
- to authorize scope change after V Forge has already acted on the anticipated
  new signal — retrospective authorization is not valid

---

## Request Semantics

A valid scope change request must be interpretable as carrying at minimum the
following semantic fields.

### Required semantic fields

**Request identity**
A stable identifier for this scope change request. Required for activity trail
records, VEDA's de-duplication and processing, and linkage to any upstream
return-to-planning or review reference. Must remain stable across any re-send
attempts.

**Initiating actor and authority surface**
The actor issuing the request and through which surface. For Path A: the operator
identity and the operator surface. For Path B: Project V as proximate initiator,
plus the operator approval reference that governs the request authority.

**Operator approval reference**
A reference to the governed approval that authorizes this request. For Path A,
this is the operator's own decision record. For Path B, this is the external
approval record from the operator review. A request without a resolvable approval
reference is not valid.

**Originating context reference** (when applicable)
If the request originates from a return-to-planning finding, a planning review,
a launch readiness evaluation, or a post-launch observation gap finding: a reference
to that originating context. This ties the scope change to its governance trigger
and makes the trail auditable end-to-end.

**Reason for scope change**
A legible statement of why the scope change is being requested. This must be a
real governance rationale — a signal gap, a coverage need, a changed project scope,
a new portfolio concern — not a generic instruction. VEDA uses this to assess
whether the request is bounded and legitimate.

**Change type**
One of the change categories defined in the Change Categories section. The change
type must be explicit. A request that cannot be classified into a change category
is not bounded.

**Target scope definition**
The specific, bounded scope of what should change in VEDA's observatory. This must
identify at minimum one of:

- project or portfolio scope
- signal class or evidence class
- source class or provider scope
- topic or keyword scope
- observation target or URL scope

A request with no target scope is unbounded and invalid.

**Urgency and timing posture** (optional but strongly recommended)
Whether the scope change is blocking a time-sensitive governance need or can be
fulfilled in VEDA's normal observatory management cycle. This does not override
VEDA's implementation judgment but allows VEDA to prioritize appropriately.

**External-action and cost implication acknowledgment**
If the requested scope change involves adding new provider integrations, expanding
paid data coverage, or materially increasing retrieval volume or API cost, the
request must acknowledge that implication. A request that would trigger significant
external cost without acknowledging it does not satisfy the boundedness condition.

---

## Change Categories

This interface supports the following observatory change categories.

### Add new observation target
Add a new project, URL, domain, keyword set, or topic to VEDA's active observatory.
Must be bounded to a specific project or portfolio context.

### Expand signal or source coverage
Extend VEDA's coverage of an existing observation target to include additional
signal classes, source classes, or provider integrations not currently active.
Must identify which signal or source class to add and for which project scope.

### Narrow or retire obsolete scope
Remove an observation target, signal class, or source from active observatory
coverage. Appropriate when a project is archived, a signal class is no longer
relevant, or coverage is no longer cost-justified.

### Refresh or reclassify monitoring coverage
Update the depth, cadence, trust classification, or evidence class assignment for
an existing observation target without adding or removing coverage entirely.
Must identify what is being changed and why the current classification no longer
fits.

### Change cadence or depth
Increase or decrease the observation frequency or evidence depth for a specific
scope. Appropriate when governance needs or cost posture has changed. Must be
bounded to a specific scope and must carry the approval posture appropriate to
any cost increase.

Requests that cannot be classified into one of these categories must be treated
as unbounded and must not be processed.

---

## Validity Conditions

A scope change request is valid only when all of the following are true:

- the request carries a stable request identity
- the initiating actor is identified and falls within the allowed initiation paths
  (operator direct or Project V-mediated with documented operator approval)
- a resolvable operator approval reference is present and predates the request
- the reason for scope change is legible and constitutes a real governance rationale
- the change type is classifiable into a defined change category
- the target scope is explicitly bounded — project, signal class, source class,
  topic, or some combination
- the request does not attempt to transfer observatory ownership to another system
- the request does not act as a disguised evidence access escalation for V Forge
- if external-action or cost consequences are implied, the request acknowledges
  them and they fall within the approved posture
- the request has not been superseded by a materially changed governance context
  before VEDA acts on it

A request that fails any of these conditions must not be processed by VEDA.
VEDA must communicate the invalidity rather than proceeding on a deficient basis.

---

## Authority and Approval Rule

Observatory scope change is an approval-sensitive action.

The governed approval requirement exists because observatory scope change:

- may create new external retrieval activity and associated cost (Class E4 under
  `../governance/external-action-governance.md` for cases involving paid or
  spend-creating expansion)
- may expand VEDA's external surface in ways that have ongoing operational and
  cost consequences
- represents a material change to what the ecosystem observes and governs against

**Required approval posture:**

- for scope changes that involve new paid provider integrations, new billable API
  coverage, or material cost increase: explicit governed operator approval is
  required before the request is issued. Technical capability does not authorize
  it. An upstream signal gap finding does not authorize it. The approval must be
  documented and referenced in the request.

- for scope changes that involve narrowing, retiring, or reclassifying existing
  coverage without new cost implications: operator approval is still required, but
  the approval posture is lower-governance. The operator must still authorize the
  change; it cannot be self-initiated by any system.

- for scope changes initiated through Path B (Project V-mediated): the operator
  approval must be an explicit, documented decision — not an implied assent, not
  an informal preference, and not an automatic consequence of a planning review
  outcome. Project V routing the request without documented operator approval is
  a governance failure.

**What approval does not do:**

A prior approval for one scope change does not authorize a different or broader
change. Approval scope must remain bounded to what was specifically reviewed and
authorized.

---

## VEDA Response Obligation

VEDA receives the request and must respond through a governed response path.

VEDA may:

- **accept** the request and proceed with implementing the scope change within
  its own authority domain, with activity trail records for implementation start
  and completion
- **narrow** the request if the bounded scope exceeds what VEDA can implement
  cleanly or what the governance context supports, and communicate the narrowing
  explicitly
- **defer** the request if implementation is not currently feasible — for example
  because a required provider integration is not available, cost posture has changed,
  or a conflicting scope change is in progress — with an explicit deferral reason
  and re-entry posture
- **reject** the request if it fails validity conditions, exceeds approved scope,
  lacks a resolvable authority reference, or would require VEDA to absorb an
  unbounded observatory obligation

VEDA must not:

- silently process a request that fails validity conditions
- implement a scope change broader than what the approved request authorizes
- accumulate deferred requests silently without communicating status
- treat a stale request as current if the governance context has materially changed
  before implementation

VEDA remains the owner of all resulting observatory records and signal outputs
produced from the expanded or adjusted scope. Observatory scope change does not
transfer observatory ownership to the requesting system or to V Forge.

---

## Degraded-Mode Behavior

### Request is unbounded or missing required fields

VEDA must not process the request. VEDA must communicate the specific invalidity
to the initiating system. The request must be revised and resubmitted. The original
request identity should be preserved in the revised submission to maintain the
audit trail.

### Operator approval reference is missing or cannot be resolved

VEDA must not process the request. A scope change request without a resolvable
approval reference has no governed authority basis. The initiating system must
obtain the correct approval reference before resubmitting.

### Request scope conflicts with an active or pending scope change

VEDA must surface the conflict explicitly rather than silently merging requests.
The operator must resolve the conflict — either confirming the new request supersedes
the prior one, or withdrawing it. VEDA must not self-resolve scope conflicts.

### Requested scope exceeds approved external or cost posture

If implementing the requested scope change would trigger external cost or provider
activity beyond what the approval reference covers, VEDA must defer and communicate
the cost implication. The operator must issue a revised approval before VEDA proceeds.
VEDA must not self-approve cost escalation.

### Requested scope cannot currently be implemented

If the target scope change is technically not currently implementable — for example
because a required provider integration does not exist, a target URL is inaccessible,
or a required data class is not in VEDA's current observatory capability — VEDA
must communicate this as a deferral with a specific reason. The request should not
be silently discarded; the governance need it represents must remain visible.

### Request becomes stale before VEDA acts

If the governance context that triggered the request has materially changed before
VEDA implements the scope change — for example the originating project has been
archived, the planning direction has changed, or a broader replanning has superseded
the original scope gap — the initiating system must void the request before VEDA
proceeds. VEDA must not implement a scope change for a stale or voided request.

---

## Recovery Behavior

- A request that failed for resolvable reasons (missing fields, missing approval
  reference, conflict) may be corrected and resubmitted using the same request
  identity, provided the underlying governance rationale has not changed.

- If the governance rationale has materially changed, a new request must be issued
  with a new request identity. The original request identity should be referenced
  as superseded.

- A request that was deferred due to an external cost threshold may be resubmitted
  after a revised operator approval has been obtained. The revised approval reference
  must be included in the resubmission.

- A voided or superseded request must not be silently re-activated. Once voided,
  a new governed request is required.

- VEDA must not carry a stale deferred request forward without re-validating the
  governance context. Deferral does not mean indefinite hold without review.

---

## Activity Trail

Every scope change request event on this interface must produce activity trail records.

**Producing system:** Operator surface or Project V (for request initiation events);
VEDA (for receipt, processing, and implementation events)

The following events must each produce a record:

| Event | When it occurs |
|---|---|
| Request initiated | Operator or Project V (on operator's behalf) delivers the scope change request |
| Request received by VEDA | VEDA acknowledges receipt of the request |
| Request accepted | VEDA determines the request is valid and will proceed with implementation |
| Request narrowed | VEDA accepts a bounded subset of the request and communicates the narrowing |
| Request deferred | VEDA cannot currently implement; deferral reason recorded |
| Request rejected | VEDA rejects due to validity failure, authority gap, or out-of-bounds scope |
| Implementation started | VEDA begins observatory scope implementation |
| Implementation completed | VEDA confirms the scope change has been implemented |
| Request voided / superseded | Request is withdrawn or superseded before VEDA acts |

Each event record must carry, at minimum:

- the request identity
- the initiating actor and authority surface
- the operator approval reference
- the originating context reference, if applicable
- the change type and target scope summary
- the event outcome or status at the time of the record
- for implementation events: what specifically was changed in VEDA's observatory scope

**Activity trail canon status:**

The `observatory.scope_change.*` action type family (seven types) and the
`observatory_scope_change` entity type are canonical in
`../ecosystem/activity-trail-model.md`. The full mapping for this interface —
including producing systems, required entity references, and minimum additional
fields per event — is defined in integration map Section 11
(`../ecosystem/activity-trail-integration-map.md`).

Implementations must use the canonical action types and fields defined there.
Do not invent alternate action type names for this seam.

---

## Cost and External-Action Posture

Observatory scope expansion is potentially an external-action event under
`../governance/external-action-governance.md`.

Specifically:

- adding new paid provider integrations or expanding billable API coverage is a
  **Class E4** external action (paid or spend-creating external action) and requires
  explicit governed operator approval before it may proceed
- expanding observation targets that imply new ongoing external retrieval — even
  read-only — is a **Class E1** external action that may still carry cost, rate-limit,
  or source-trust governance sensitivity and must not be treated as automatically
  low-risk
- narrowing or retiring scope does not typically create new external cost, but
  must still follow the governed request path

The following must be explicit in all cases:

- technical capability to expand observatory scope does not authorize it
- a signal gap finding does not authorize scope expansion
- recommendation or planning determination that more signal would be useful does
  not authorize scope expansion
- only a governed operator approval satisfies the authorization requirement

Cost attribution for scope changes implemented through this interface is attributable
to the initiating project or portfolio context and must be traceable to the request
identity and operator approval reference in the activity trail.

---

## Boundary and Ownership Rule

This interface governs a change to what VEDA observes. It does not change who
owns the resulting observatory records.

After a valid scope change is implemented:

- VEDA remains the canonical owner of all observatory records, signal outputs,
  and evidence produced from the changed scope
- Project V remains the owner of planning and orchestration truth
- V Forge remains the owner of execution truth
- the requesting operator does not acquire a competing observatory authority by
  having directed the scope change

The scope change gives VEDA new or adjusted observatory obligations. It does not
create a VEDA-bypass path for any other system to access the new signal directly.
New signal produced from an expanded scope is delivered to other systems through
the existing governed signal interfaces — not through a special path created by
this request.

**V Forge cannot use a scope change request routed through Project V as a mechanism
to pre-authorize its own access to the resulting new signal.** The expansion may
ultimately result in VEDA delivering additional signal to V Forge through
`veda-to-v-forge-signal-interface.md`, but that delivery follows the standard
governed delivery path with its own validity and access rules.

---

## Distinction from Adjacent Interfaces

These distinctions must be kept sharp.

### vs. `project-v-to-veda-evidence-request-interface.md`

An evidence request is a bounded request for a specific evidence package to answer
a specific planning-side question. It does not change what VEDA observes going
forward. The evidence request path is governed by Project V's planning authority
and does not require operator approval.

This interface changes VEDA's ongoing observatory scope — what VEDA will observe
and produce going forward. It requires operator approval and has external-action
and cost implications. Do not use an evidence request as a substitute for this
interface when the real need is a persistent scope change.

### vs. `v-forge-evidence-access-contract.md`

The evidence access contract governs V Forge's active, bounded queries against
existing VEDA evidence during execution. V Forge queries what VEDA already has.
V Forge does not expand what VEDA tracks. The evidence access contract carries
no observatory scope change authority.

This interface changes what VEDA tracks. V Forge is not the initiating authority
and cannot invoke this interface. A V Forge evidence gap finding surfaces through
return-to-planning; the operator decides whether a scope change is warranted.

### vs. `veda-to-v-forge-signal-interface.md`

The VEDA to V Forge signal interface governs VEDA's delivery of a bounded baseline
startup signal package to V Forge at execution scope initialization. It does not
govern what VEDA observes — it governs delivery of what VEDA has already produced.

This interface governs what VEDA produces going forward by changing observatory
scope. These are separate concerns at separate lifecycle moments.

### vs. `v-forge-to-project-v-return-to-planning-interface.md`

The return-to-planning interface is how V Forge surfaces execution findings —
including signal gap findings — back to Project V for planning reconsideration.
This is the correct upstream path for V Forge when it identifies that VEDA is
not providing signal it needs.

The return-to-planning interface does not itself authorize a scope change.
It delivers the finding. The operator then decides whether to authorize a scope
change through this interface. These are two distinct steps in the governed
escalation chain.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- only an operator (or Project V acting with explicit operator approval) may
  initiate an observatory scope change through this interface
- V Forge never directly commands VEDA to expand observatory scope
- a signal gap finding, planning determination, or execution evidence gap does
  not self-authorize a scope change — operator approval is required
- the request must be bounded: change type, target scope, authority reference,
  and reason are all required
- VEDA may accept, narrow, defer, or reject — it is not obligated to implement
  every request in the form submitted
- observatory scope change may be an external-action event with cost consequences
  that require explicit approval
- VEDA remains the owner of all observatory records produced from the changed scope
- activity trail action types for this interface are canonical in the model;
  the full mapping is in integration map Section 11

If the interface is implemented as a direct V Forge command path, as an automatic
consequence of a signal gap finding, or as a path that bypasses operator approval,
the doctrine is wrong.

---

## Usage

This document should be used:

- when implementing the operator-facing observatory scope management surface for VEDA
- when implementing Project V's ability to route a governed scope change request
  on behalf of an operator following a planning review
- when evaluating whether an observatory scope change is properly authorized and bounded
- when reviewing whether a proposed V Forge evidence need should trigger a scope
  change request vs. an evidence request vs. an evidence access contract query
- when designing the activity logging pipeline for scope change events
- when confirming the activity trail action type mapping at integration map Section 11

---

## Related Docs

- `data-boundaries.md`
- `project-v-to-veda-evidence-request-interface.md`
- `v-forge-evidence-access-contract.md`
- `veda-to-v-forge-signal-interface.md`
- `v-forge-to-project-v-return-to-planning-interface.md`
- `../ecosystem/cross-system-access-governance.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/activity-trail-model.md`
- `../ecosystem/activity-trail-integration-map.md`
- `../governance/external-action-governance.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`
- `../veda/veda.md`
- `../veda/system-invariants.md`
- `../veda/observability-and-signal-role.md`
- `../project-v/project-v.md`
- `../v-forge/v-forge.md`
