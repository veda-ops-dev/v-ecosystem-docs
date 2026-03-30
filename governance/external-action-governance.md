# External Action Governance

## Purpose

This document defines how external actions are governed inside the V Ecosystem.

It exists to answer:

```text
When may the ecosystem take action outside its internal boundary, what makes an external action governance-sensitive, what controls must apply before it occurs, and how should external actions be bounded, approved, attributed, and reported?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what counts as an external action
- when external actions are governance-sensitive
- what conditions must be satisfied before external action may occur
- how external actions relate to approval, actor authority, reporting, and system boundaries
- what external actions must and must not be treated as permissible by default
- the baseline external-action posture shared across the ecosystem

---

## Out of Scope

This document does not define:

- provider-specific API details
- implementation-specific credential handling
- detailed paid data pull rules for every vendor
- detailed publication workflow mechanics
- every project-specific external action variant

Those belong in more specific governance, workflow, interface, implementation, or provider-specific docs.

---

## System

- governance

---

## Core Rule

An external action must not occur unless it is classifiable, bounded, attributable, authorized, and approved at the level required by its risk, scope, and effect.

External action is governance-sensitive by default.

Technical capability to perform an external action does not authorize it.
Recommendation to perform an external action does not authorize it.
Human permissiveness stated informally does not automatically authorize it.

---

## External Action Definition

An external action is any action that reaches outside the internal governed boundary of the V Ecosystem and may affect an external system, external audience, external account, external vendor, external dataset, external spend, or external real-world state.

Examples include:

- publishing or sending information externally
- making changes through third-party platforms or services
- triggering paid requests, spend, or billable usage
- mutating external accounts, listings, repositories, or services
- initiating outbound communication
- causing launch-visible or public-visible changes

The external-action governance doctrine exists so that the ecosystem does not treat outside-the-boundary mutation as casual continuation of internal work.

---

## External Action Principle

External action is not the same as internal preparation.

The fact that the ecosystem has internally decided, recommended, prepared, or simulated an action does not make the external action itself active or authorized.

Before an external action occurs, the ecosystem must preserve a clear distinction between:

- internal interpretation
- internal recommendation
- internal approval posture
- external action readiness
- external action execution

If those stages blur, external risk increases and governance weakens.

---

## External Action Classes

At the baseline level, external actions should be understood through the following classes.

### Class E1 — External Read-Only Retrieval
Examples:

- bounded external data fetches
- bounded read-only API queries
- bounded retrieval of public or authorized external information

### Rule
These actions may still be governance-sensitive depending on cost, source trust, rate limits, or approval posture.
Read-only does not automatically mean low-risk.
Where E1 actions involve cost, billable usage, rate-sensitive resources, source trust uncertainty, or approval posture requirements, they must be treated with the same governance care as higher-class external actions for those specific dimensions.
Boundedness and approval posture must be verified before proceeding in those cases.
E1 classification does not grant automatic clearance.

---

### Class E2 — External Communication or Submission
Examples:

- sending outbound messages
- submitting forms
- posting updates to external services
- creating tickets or requests in external systems

### Rule
These actions are governance-sensitive because they create outward-facing state or communication.
They must not proceed as though internal intent is enough.

---

### Class E3 — External Mutation
Examples:

- modifying external accounts or service configuration
- changing public-facing content
- publishing, deploying, launching, or altering externally visible artifacts
- mutating third-party platform state

### Rule
These actions are high-governance sensitivity by default.
They require explicit approval posture and actor legitimacy before execution.

---

### Class E4 — Paid or Spend-Creating External Action
Examples:

- paid data pulls
- paid API usage beyond pre-approved bounded scope
- ad spend changes
- paid service activation
- any external action that creates billable or financial consequences

### Rule
These actions require explicit governed approval before they become active.
Informal direction does not substitute for governed approval.
Paid data pull governance is a specific subset of E4 external actions.
More detailed rules for paid data pulls, including vendor-specific constraints, bounded approval posture, and source trust requirements, are defined in `paid-data-pull-governance.md`.
This doc’s E4 rules are the baseline; that doc refines them for the paid-data-pull use case.

---

## Governance-Sensitive Nature of External Action

External action is governance-sensitive because it may:

- create irreversible or hard-to-reverse consequences
- create external visibility
- create financial impact
- create reputational impact
- create legal, contractual, or compliance consequences
- move the ecosystem from internal readiness into outward effect

For this reason, the default posture is not "act unless forbidden."
The default posture is "do not execute until the action is clearly authorized and approved."

---

## Preconditions for External Action

An external action may proceed only when all of the following are true:

- the action is clearly classifiable
- the action scope is bounded
- the actor is identifiable and attributable
- the actor has the required authority for the action
- the required approval posture has been satisfied
- the action remains inside the relevant system and workflow boundaries
- the action has been reported or is reportable through the governed reporting path
- material uncertainty affecting safety, correctness, or authorization has been preserved and resolved at the level required for action

If any of these conditions is missing, the external action must not be treated as ready to execute.

---

## Internal Preparation Is Not External Authorization

The following do not by themselves authorize an external action:

- internal planning readiness
- recommendation packaging
- handoff preparation
- report generation
- simulated success
- technical tool access
- informal operator statements or expressed preferences that have not been recorded as governed approval

External authorization requires the specific governance posture appropriate to the action class and risk.

---

## Approval Rule for External Action

External actions must follow the approval model defined in `approval-and-escalation-model.md`.

At minimum:

- approval-sensitive external action must not proceed without explicit governed approval where required
- paid or spend-creating external action requires explicit governed approval
- high-impact or launch-sensitive external mutation requires explicit governed approval
- unclear approval posture is not permission
- stale approval must not be reused casually for changed external action scope

A prior approval for one external action does not automatically authorize:

- a broader action
- a later action
- a different external target
- a different account
- a different spend level
- a changed publication or launch scope

Approval scope must remain bounded.

---

## Actor Authority Rule for External Action

Not every actor who can technically perform an external action is allowed to do so.

Before external action occurs, the ecosystem must be able to determine:

- who or what is acting
- what actor class is involved
- whether that actor is permitted to execute the relevant external action class
- whether the actor is acting within the correct system and workflow role

Agents must not self-authorize external action.
System processes must not self-expand into external mutation authority.
A human operator does not automatically have authority for all external action classes merely by being human.

The relevant actor doctrine is defined in `auth-and-actor-model.md`.

---

## Bounded Scope Rule

An external action must be bounded before execution.

This means the action must make clear:

- what exact external effect is intended
- what target system, platform, audience, account, or vendor is involved
- what specific scope is approved
- what is outside scope
- what financial, publication, launch, or mutation boundaries apply

An external action must not silently widen from:

- one message to a broader campaign
- one content change to multiple public changes
- one bounded query to ongoing external retrieval
- one account change to broader platform mutation
- one approved spend to open-ended spend

Scope widening invalidates casual reuse of approval.

---

## External Readiness Rule

External action readiness is a specific governance state.

External readiness requires more than internal preparation.
It requires that:

- the action is clearly defined
- the required approvals are satisfied
- the actor legitimacy is clear
- the current scope still matches the approved scope
- any required review, reporting, and follow-up posture is in place

External readiness must not be self-certified by the acting agent.
The actor’s confidence that conditions are satisfied is not equivalent to verified external readiness.
Readiness determination must remain reviewable and consistent with the approval and attribution requirements defined in `approval-and-escalation-model.md` and `auth-and-actor-model.md`.

An action may be internally prepared without being externally ready.
That distinction must remain visible.

---

## Uncertainty and Withholding Rule

If material uncertainty affects whether an external action is safe, correct, authorized, or within scope, the action must be withheld until the uncertainty is resolved at the level required by the action class.

Examples include:

- unclear actor authority
- unclear approval status
- unclear target account or audience
- unclear spend consequence
- unclear launch sensitivity
- unclear publication consequence
- unclear legal or policy constraint

When material uncertainty cannot be resolved within the time available for the action, the correct behavior is to withhold the action, escalate the uncertainty explicitly through the governed escalation path, and preserve the external no-action outcome.
Delay does not constitute implicit authorization.
An unresolved uncertainty that blocks an external action must escalate rather than expire quietly.

External action must not be pushed through because delay is inconvenient.

---

## Execution Halt Rule

When governance conditions change materially during external action execution, the action must halt at the earliest safe stopping point.

Examples include:

- approval is revoked during execution
- scope widening is discovered after initiation
- unauthorized external effect is detected
- material uncertainty emerges after the action has begun
- actor legitimacy or target legitimacy becomes questionable mid-execution

In those cases, the ecosystem must:

- halt execution at the earliest safe stopping point
- preserve the current execution state
- report the situation through the governed escalation and reporting path
- not proceed further unless the required governance posture has been re-established

Completing a questionable external action because stopping is inconvenient is not acceptable governance behavior.

---

## External Action vs Recommendation Rule

A recommendation to perform an external action is still a recommendation.
It does not constitute external authorization or external execution.

Recommendation packaging may support approval review.
It must not be used to smuggle external action across the governance boundary.

If immediate external action is required rather than merely proposed, the approval and reporting requirements still apply.

---

## External Action vs Report Rule

A report may describe an external action, a proposed external action, a blocked external action, or an external no-action outcome.

The report must preserve which of these is true.

A report must not:

- describe a proposed external action as though it already occurred
- describe a blocked external action as though it is clear to proceed
- describe internal preparation as external execution
- hide that the action was withheld due to governance or uncertainty

A report preserves governed state.
It does not grant authority by wording.

---

## External No-Action Rule

Sometimes the correct governance outcome is not to perform the external action.

When external action is withheld, blocked, rejected, or deferred for governance-sensitive reasons, that outcome should be preserved through the governed reporting path when continuity, review, or later reconsideration depends on it.

Examples include:

- no external action taken because approval was missing
- no external action taken because actor authority was unclear
- no external action taken because scope widened beyond approval
- no external action taken because launch sensitivity required review
- no external action taken because cost impact was not yet approved

External non-action is often governance-relevant and must not be silently lost.

---

## Cross-System Boundary Rule

External action does not erase internal ownership boundaries.

This means:

- Project V may govern planning and readiness related to external action, but it does not become the execution ledger for external mutation
- V Forge may execute approved external action within scope, but it does not gain planning or approval authority by doing so
- VEDA may surface signal relevant to external action, but it does not authorize the external action by surfacing that signal

External execution must still preserve ecosystem system roles.

---

## Durability and Reporting Rule

External actions and external-action non-actions that matter to governance must be attributable and durably reportable.

The ecosystem must be able to determine, after the fact:

- what external action was proposed, approved, executed, withheld, or rejected
- who or what acted
- what approval posture applied
- what scope applied
- what outcome occurred
- what follow-up or continuity state remained

If that cannot be determined, external-action governance is weak.

The reporting structure is defined in `report-structure-and-required-fields.md`.
Daily recurring visibility is further governed by `daily-report-doctrine.md`.

---

## Insufficient External Action Patterns

External-action handling is insufficient when:

- internal readiness is treated as external authorization
- recommendation is treated as permission to execute
- tool capability is treated as authorization
- approval scope is widened silently
- a blocked or withheld external action is reported as though it is ready
- paid external action occurs without explicit governed approval
- actor legitimacy is assumed instead of verified
- public-facing mutation occurs without clear approval and attribution
- external action is taken without durable reporting where continuity depends on it

These are governance failures, not acceptable shortcuts.

---

## Human-In-The-Loop Principle

External action is one of the main places where human-in-the-loop control must remain real.

If external actions are allowed to proceed on ambiguous authority, unclear approval, or weak reporting:

- external risk increases
- approvals become less meaningful
- accountability weakens
- launch and publication mistakes become easier
- financial and reputational consequences become harder to govern

External action governance is not optional ceremony.
It is one of the main safety boundaries of the ecosystem.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- external action is governance-sensitive by default
- internal preparation does not authorize external execution
- recommendation does not authorize external execution
- approval scope must remain bounded
- actor legitimacy must be verified before external action occurs
- unclear authority or approval means withhold the action
- external non-action may be governance-relevant and reportable

If an LLM treats technical ability or internal confidence as enough to cross the external boundary, the doctrine is wrong.

---

## Usage

This document should be used:

- when deciding whether an external action may proceed
- when reviewing whether an external action is properly bounded and approved
- when evaluating whether an external action should be withheld, escalated, or rejected
- when tightening workflow rules for launch-sensitive, public-facing, or spend-creating actions
- when reviewing whether external execution is being confused with internal preparation

---

## Related Docs

- `approval-and-escalation-model.md`
- `auth-and-actor-model.md`
- `report-structure-and-required-fields.md`
- `daily-report-doctrine.md`
- `recommendation-packaging-doctrine.md`
- `paid-data-pull-governance.md`
- `failure-and-recovery-doctrine.md`
- `../ecosystem/cross-system-boundaries.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
