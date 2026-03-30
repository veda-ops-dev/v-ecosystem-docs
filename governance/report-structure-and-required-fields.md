# Report Structure and Required Fields

## Purpose

This document defines the minimum structure and required fields for governed reports inside the V Ecosystem.

It exists to answer:

```text
What must a governed report contain so actions, findings, approvals, escalations, and continuity-relevant outcomes remain reviewable, interpretable, and durable across the V Ecosystem?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the minimum structure of governed reports
- the minimum required fields needed for reviewability and continuity
- what information must be present when agents report actions, findings, requests, outcomes, or escalations
- the baseline reporting posture shared across systems
- what makes a report insufficient for governed ecosystem use

---

## Out of Scope

This document does not define:

- every project-specific report variant
- implementation-specific storage schemas
- detailed UI or transport formats
- full decision-record structure
- full ADR structure
- detailed source-provenance structure

Those belong in more specific governance, workflow, interface, or project docs.

---

## System

- governance

---

## Core Rule

A governed action, finding, request, transition, or continuity-relevant outcome must be reported in a reviewable structure.

If a report does not make the action or outcome understandable after the fact, it is not sufficient governed reporting.

A report must preserve enough structure that a capable human or LLM can determine:

- what happened
- why it happened
- what scope it affected
- what did not happen
- what remains uncertain
- what requires follow-up, approval, or escalation

---

## Report Definition

A governed report is the bounded, reviewable record by which an agent or operator communicates an action, result, request, finding, transition, or no-action outcome inside the V Ecosystem.

The report structure exists so that:

- reporting is externalized rather than implicit
- governance-sensitive behavior is reviewable
- approval and escalation behavior can be interpreted correctly
- continuity-relevant outcomes are preserved
- future sessions do not have to rediscover what already happened

This document defines the baseline report shape.
More specific docs may define additional fields for specific workflows or systems.

---

## Reporting Principle

A report must describe reality, not posture.

This means a report must not substitute tone, confidence, or implication for the actual record of what happened.

A governed report must be:

- explicit rather than implied
- bounded rather than sprawling
- reviewable rather than conversationally fuzzy
- continuity-supporting rather than ephemeral
- faithful to the current system, workflow, and approval posture

---

## When a Governed Report Is Required

A governed report is required whenever an agent or operator performs, attempts, recommends, rejects, escalates, or returns a meaningful ecosystem action or outcome that affects governance, continuity, workflow state, or cross-system understanding.

This includes at minimum:

- approval requests
- approval outcomes where they must be preserved
- escalation outputs
- handoff-related reporting
- return-to-planning reporting
- execution findings returned for planning use
- intake outcomes that materially affect planning
- continuity-relevant rejections
- significant no-action outcomes where governance or correctness depends on preserving why no action occurred

Class A low-risk non-mutating support actions do not require a full governed report when the output is fully visible in the current session, produces no continuity-affecting state, and requires no follow-up approval, escalation, or cross-session continuity.
When in doubt whether these conditions are met, produce a governed report.
The burden of confidence is on the absence of governance impact, not on inference.

---

## Minimum Report Structure

A governed report must be interpretable as containing the following sections or semantic equivalents:

- report type
- context
- subject
- action or outcome
- basis
- current status
- constraints or uncertainties
- required next step

These sections may later be represented through different storage or transport mechanisms, but the semantic structure is mandatory.

---

## Required Fields

Every governed report must contain, at minimum, fields that answer the following questions.

## 1. Report Type

The report must identify what kind of report it is.

Examples include:

- action report
- finding report
- approval request
- approval outcome report
- escalation report
- handoff report
- return-to-planning report
- intake outcome report
- rejection report
- no-action report

### Rule
If the report type is unclear, the report is not safely classifiable.
An unclassifiable report is weak governance output.

---

## 2. System Context

The report must identify which system the report belongs to.

Examples:

- Project V
- VEDA
- V Forge
- ecosystem governance layer

### Rule
A report must not blur which system owns the action, finding, or outcome being described.

---

## 3. Actor Context

The report must identify who or what produced the report.

Examples:

- operator
- agent session
- Project V planning agent
- V Forge execution agent
- governance review actor

### Rule
Attribution must be specific enough that later review can determine who or what produced the report and, where relevant, who performed the action or issued the outcome.
Where actor authority matters, this attribution must be specific enough to be verified.
The full actor authority model is defined in `auth-and-actor-model.md`.

---

## 4. Workflow or Interface Context

The report must identify the relevant workflow stage, interface, or governance path when one exists.

Examples:

- project intake
- handoff
- return-to-planning
- approval review
- escalation path

### Rule
A report that omits its workflow or interface context when that context matters is harder to interpret and easier to misuse later.

---

## 5. Subject

The report must identify what the report is about.

Examples:

- the relevant project
- intake candidate
- handoff package
- execution work item
- finding set
- approval-sensitive action
- rejected proposal

### Rule
The subject must be specific enough that later readers do not have to guess what work or context the report refers to.

---

## 6. Action, Outcome, or Finding

The report must state what happened, what was produced, what was requested, or what outcome was reached.

Examples:

- approval requested
- handoff prepared
- execution blocked
- intake rejected
- no action taken
- escalation required

### Rule
A report must state the outcome directly.
It must not force the reader to infer the real result from surrounding prose.

---

## 7. Basis

The report must state the bounded basis for the action, outcome, or recommendation.

Examples include:

- relevant signal
- relevant findings
- relevant planning context
- governing decision context
- approval posture
- blocking condition
- source or evidence references where needed

### Rule
The basis must be sufficient to explain why the reported action or outcome is appropriate, not merely why the report was generated.
A basis that describes the situation without justifying the action or outcome is not sufficient.
A report without basis is not reviewable.

---

## 8. Approval or Governance Posture

Where governance matters, the report must identify the relevant approval, rejection, escalation, or no-action posture.

Examples:

- approval not required
- approval requested
- approval pending
- approved
- rejected
- escalated
- no action due to unclear authority

### Rule
A report must not imply governed permission if the approval posture is still unresolved.

---

## 9. Status

The report must identify the current actionable status of the subject.

Examples:

- pending review
- approved to proceed
- blocked
- returned to planning
- deferred
- rejected
- complete
- no action taken

### Rule
Status must describe what is true now, not what might be true later.

---

## 10. Constraints, Risks, or Uncertainties

The report must identify material constraints, risks, or uncertainties that affect correctness, approval, execution, or interpretation.

Examples:

- unclear authority
- weak source confidence
- missing evidence
- blocked dependency
- unclear approval scope
- unresolved conflict

### Rule
If uncertainty materially affects correctness, the report must preserve it explicitly.
Confidence theater is not valid reporting.

---

## 11. Required Next Step

The report must identify what needs to happen next, if anything.

Examples:

- human review required
- approval required
- escalation required
- additional evidence requested
- return to planning complete; await planning decision
- no next step

### Rule
A report should not leave follow-up state ambiguous when the ecosystem depends on that next step.

---

## Minimum Report Semantics by Use Case

The baseline fields above apply to all governed reports.
The following use cases require extra clarity.

## Approval Request Reports

An approval request report must make clear:

- what action is being requested
- why approval is needed
- what scope the approval would cover
- what happens if approval is granted
- what happens if approval is denied

Approval requests must not hide the real action inside vague wording.

---

## Approval Outcome Reports

An approval outcome report must make clear:

- what was approved or rejected
- what scope the outcome applies to
- what conditions, limits, or expiry concerns exist where relevant
- whether follow-up action is now permitted, denied, or still pending

Approval outcome reporting must not widen the actual approval scope.

---

## Escalation Reports

An escalation report must make clear:

- what issue requires escalation
- why it cannot be resolved safely within current doctrine, workflow, or approval posture
- what action is blocked or withheld pending resolution
- what decision, clarification, or approval is needed

Escalation is not complete unless the blocked condition is made reviewable.

---

## Finding Reports

A finding report must make clear:

- what was found
- in what bounded context it was found
- why it matters
- whether it changes planning, execution, approval, or continuity posture
- whether the finding remains inside the current scope or requires return-to-planning, escalation, or additional evidence handling

Findings must not be reported as though they are already decisions.
A finding report must not present findings as VEDA signal or as governing planning decisions from Project V.
Findings are execution-side outputs, and their system context must be explicit.
A finding report does not constitute signal transfer through the VEDA to Project V interface, and it does not constitute a governing decision.

---

## Rejection Reports

A rejection report must make clear:

- what was rejected
- why it was rejected, if known
- what scope the rejection applies to
- whether reconsideration is expected later
- what conditions would need to change before reconsideration, if known

A rejection that cannot be interpreted later is weak continuity support.

---

## No-Action Reports

A no-action report is required when the reason for not acting matters to governance, continuity, or future correctness.

A no-action report must make clear:

- what was not done
- why it was not done
- whether the blocker is approval-related, authority-related, evidence-related, boundary-related, or workflow-related
- whether a later retry, escalation, or review is expected

These blocker type categories also apply to escalation reports.
No-action reporting prevents future sessions from mistaking deliberate non-action for omission.

---

## Reporting Boundaries

A report must not:

- collapse signal into decision
- collapse recommendation into approval
- collapse findings into automatic planning changes
- blur planning truth with execution truth
- blur one system’s report into another system’s authority
- pretend uncertainty has been resolved when it has not

A report describes governed state.
It does not create authority by wording alone.

---

## Durability Principle

A governed report must be preserved in a form that remains accessible to future relevant sessions.

Ephemeral conversational output is not sufficient when the report affects:

- approvals
- rejections
- continuity
- handoffs
- return-to-planning
- escalation history
- execution findings that planning may need later

This document does not define where all reports are stored.
But durability is required where governance or continuity depends on later access.

---

## Insufficient Report Patterns

A report is insufficient if it:

- does not identify what happened
- does not identify what system or workflow it belongs to
- does not identify the subject clearly
- hides the real outcome in vague prose
- omits material uncertainty
- implies approval that does not exist
- fails to preserve what follow-up is required
- cannot be understood without the original live conversation

An insufficient report should not be treated as full governed reporting.

---

## Human-In-The-Loop Principle

Reports are one of the main ways human review remains real inside the ecosystem.

If reports are vague, incomplete, or stylistic instead of reviewable:

- approvals become unreliable
- escalations become noisy
- continuity weakens
- cross-system accountability blurs
- LLM behavior becomes harder to govern

Good reporting is not admin overhead.
It is part of how governed action stays governed.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- reporting must be structured and reviewable
- report type, system context, actor context, subject, outcome, basis, status, uncertainty, and next step are not optional decoration
- a report must preserve governance state, not just summarize activity
- reporting does not create approval, authority, or decisions by implication
- future sessions should be able to use governed reports without reconstructing hidden context

If a report reads well but does not preserve decisionally relevant state, the doctrine is being used incorrectly.

---

## Usage

This document should be used:

- when designing governed report formats
- when reviewing whether an agent output is sufficient for approval, escalation, or continuity use
- when defining workflow-specific report variants
- when deciding whether a no-action or rejection must be preserved durably
- when tightening report outputs that are too conversational or too vague

---

## Related Docs

- `agent-operating-doctrine.md`
- `approval-and-escalation-model.md`
- `decision-continuity-doctrine.md`
- `daily-report-doctrine.md`
- `recommendation-packaging-doctrine.md`
- `auth-and-actor-model.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../workflows/project-intake-workflow.md`
