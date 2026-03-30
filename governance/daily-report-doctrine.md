# Daily Report Doctrine

## Purpose

This document defines when daily reporting is required inside the V Ecosystem, what daily reports are for, and how daily reporting should be interpreted.

It exists to answer:

```text
When should a daily report be produced, what must a daily report accomplish, and how does daily reporting support governance, continuity, and human review inside the V Ecosystem?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- when daily reporting is required
- what daily reporting is meant to accomplish
- how daily reports relate to governed reporting more generally
- what daily reports must and must not be used for
- the baseline daily reporting posture shared across systems

---

## Out of Scope

This document does not define:

- the full field structure of all governed reports
- every workflow-specific reporting variant
- implementation-specific scheduling or notification systems
- project-specific progress dashboards
- detailed actor attribution rules

Those belong in more specific governance, workflow, implementation, and actor-model docs.

---

## System

- governance

---

## Core Rule

Daily reporting is the recurring governance practice by which relevant ecosystem activity, non-activity, blockers, changes, and follow-up state are made reviewable across time.

A daily report is required when a system, workflow, or session has produced meaningful governed activity or meaningful governed non-activity that future review, continuity, approval, or human oversight depends on.

A daily report must not be treated as a substitute for real-time governed reporting when immediate reporting is required.

---

## Daily Report Definition

A daily report is a time-bounded governed summary of relevant ecosystem activity for a reporting period.

The daily report exists so that:

- human review remains practical across ongoing work
- continuity is preserved across sessions and days
- meaningful progress, blockers, approvals, rejections, and non-action are visible without reconstructing every low-level interaction
- recurring oversight does not depend on memory or live session presence alone

A daily report is not a replacement for the underlying governed records it summarizes.
It is the recurring review surface that makes those records usable over time.

---

## Reporting Period Rule

A reporting period is a bounded interval of ecosystem activity used for recurring review.

The default reporting period is one calendar day when relevant ecosystem activity, governed non-activity, or continuity-relevant state exists.
If a session or workflow spans multiple calendar days without a natural stopping point, the reporting period should still be treated as ending at each calendar day boundary for daily reporting purposes.
More specific workflows may refine the exact cadence, but they must not weaken the continuity and reviewability requirements defined here.

A reporting period that produces little or no relevant activity does not automatically eliminate the need for a daily report if governance, continuity, or oversight depends on preserving that non-activity.

---

## Daily Reporting Principle

Daily reporting exists to preserve operational truth across time, not to produce status theater.

A daily report must help a later reader determine:

- what changed during the reporting period
- what did not change but still matters
- what actions were taken
- what actions were withheld
- what blockers or uncertainties remain active
- what approvals, rejections, escalations, or continuity-relevant outcomes occurred
- what needs attention next

If a daily report creates the appearance of visibility without preserving actionable understanding, it is not doing its job.

---

## Relationship to Governed Reports

Daily reports depend on governed reporting but are not identical to every governed report.

The relationship is:

- governed reports preserve specific actions, outcomes, requests, findings, and transitions
- daily reports summarize the relevant state of those governed records for a reporting period

This means:

- a daily report must not invent events that were never reported
- a daily report must not replace the need for a governed report where one is required
- a daily report should reference or summarize relevant governed records rather than restating the entire ecosystem from scratch

When a daily report is the only durable artifact produced by a session, it must satisfy not only the daily report sufficiency requirements in this doc but also the minimum governed report structure defined in `report-structure-and-required-fields.md` for each action, outcome, or finding it covers.
A daily report that is the sole continuity anchor for session activity must be treated as a governed report, not merely as a summary.
Agents must not use the daily-report-as-summary framing to produce a weaker record than the activity requires.

The baseline field structure for governed reports is defined in `report-structure-and-required-fields.md`.

---

## When Daily Reporting Is Required

A daily report is required when, during the reporting period, one or more of the following are true:

- meaningful governed actions occurred
- meaningful approvals, rejections, or escalations occurred
- meaningful workflow transitions occurred
- meaningful execution findings, intake outcomes, handoff changes, or return-to-planning events occurred
- meaningful blockers, unresolved uncertainties, or no-action outcomes remained active
- continuity would be weakened if the day’s state were not summarized for later review

For these trigger conditions, meaningful is equivalent to material as defined in the Materiality Rule.
An action, transition, blocker, or non-action is meaningful for daily reporting purposes when it is material under that rule.

A daily report may also be required when little or no action occurred, if preserving that non-action is important to governance, continuity, or oversight.

---

## When Daily Reporting Is Not Required

A daily report is not required when all of the following are true:

- no meaningful governed action or governed non-action occurred during the reporting period
- no approvals, rejections, escalations, or workflow transitions require preservation
- no continuity-relevant blockers or uncertainties remained active
- omission of a daily report would not make later review materially harder
- continuity would not be weakened if the period’s state were not summarized

When in doubt, the default is to produce a daily report.
The burden of confidence is on the absence of meaningful governance or continuity impact.

---

## Required Daily Report Outcomes

A valid daily report must make clear, at minimum:

- what reporting period it covers
- who or what produced the report
- what systems, workflows, or workstreams it refers to
- what materially happened during the period
- what materially did not happen but still matters
- what remains blocked, pending, uncertain, or awaiting approval
- what requires follow-up in the next period

A daily report that cannot answer these questions is not sufficient for governed daily review.

---

## Minimum Daily Report Semantics

A daily report should be interpretable as containing, at minimum, the following semantic elements:

- reporting period
- producer attribution
- system or workstream scope
- material actions and outcomes
- material no-action or withheld-action outcomes
- active blockers, risks, or uncertainties
- approvals, rejections, escalations, or transitions that matter
- next required attention

These semantics may later be represented through more specific report formats, but the semantic contract comes first.

---

## Materiality Rule

Daily reports should preserve material state, not every possible detail.

For daily reporting purposes, something is material when it would change how a reasonable operator, reviewer, or later LLM session understands:

- current progress
- current risk or uncertainty
- current approval posture
- current workflow state
- what should happen next

Daily reporting must not become a dump of every low-level event.
But it also must not omit changes that would alter later interpretation of what state the ecosystem is in.

---

## No-Action and Withheld-Action Rule

Daily reports must preserve meaningful non-action where that non-action affects governance, continuity, or review.

Examples include:

- no action taken because approval was unclear
- no action taken because authority was unclear
- no action taken because evidence was insufficient
- no action taken because execution remained blocked
- no action taken because a required human review did not occur yet

A day with meaningful non-action is not the same as a day with nothing to report.

---

## Approval and Escalation Rule

Where approvals, rejections, or escalations occurred or remained active during the reporting period, the daily report must make that state visible.

This includes:

- approvals requested
- approvals granted
- approvals denied
- escalations raised
- escalations still unresolved
- stale or blocked approval-dependent work that remained inactive

Where approval posture is unclear at report-writing time, the daily report must preserve that uncertainty explicitly, including what is known, what is unclear, and what review is needed before approval-dependent work may proceed.
A daily report must not imply that approval-sensitive work is clear to proceed when approval posture remains unresolved, and it must not resolve approval ambiguity by implication.

---

## Continuity Rule

A daily report must support continuity across sessions and reporting periods.

This means a daily report should preserve enough state that a later reader can determine:

- what changed since the prior relevant report
- what remained open
- what decisions, rejections, findings, or blockers still govern current work
- what should be resumed, reviewed, escalated, or withheld next

A daily report that only describes the present moment without preserving carry-forward state is weak continuity support.

---

## Cross-System Rule

A daily report may summarize activity across more than one system, but it must not blur system ownership.

This means a daily report must not:

- present VEDA signal as Project V decision truth
- present Project V planning state as V Forge execution truth
- present V Forge findings as though they are VEDA signal
- hide which system owns which action, finding, decision, or blocker

Cross-system visibility is allowed.
Cross-system ownership blur is not.

---

## Daily Report Sufficiency Patterns

A daily report is sufficient when it allows a later reviewer to understand:

- what mattered during the day
- what changed
- what remained pending or blocked
- what approvals, rejections, or escalations matter now
- what follow-up is required next

A daily report is insufficient when it:

- reads like generic status language without governed state
- hides blocked or withheld work
- omits active uncertainty that affects correctness
- collapses multiple systems into one undifferentiated summary
- cannot be used without reading the entire live session history
- reports activity but not current actionable state

---

## Human-In-The-Loop Principle

Daily reporting is one of the main mechanisms that makes human oversight practical across ongoing ecosystem activity.

Without disciplined daily reporting:

- human review becomes dependent on live session access
- governance-sensitive drift becomes harder to detect
- continuity weakens across days and sessions
- blocked or stale work becomes easier to lose track of

Daily reporting is not performance reporting.
It is recurring governance visibility.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- daily reports summarize governed state across a reporting period
- daily reporting does not replace required governed reports
- meaningful non-action may be reportable and important
- materiality matters more than verbosity
- cross-system summaries must preserve ownership boundaries
- daily reporting exists to support continuity and review, not to sound productive

If daily reporting is implemented as vague status prose or as a substitute for required underlying records, the doctrine is wrong.

---

## Usage

This document should be used:

- when deciding whether a reporting period requires a daily report
- when designing daily report formats or recurring reporting workflows
- when reviewing whether a daily report is too vague, too broad, or too shallow
- when deciding whether meaningful non-action or blocked state must be carried forward
- when aligning recurring reporting behavior across systems

---

## Related Docs

- `report-structure-and-required-fields.md`
- `agent-operating-doctrine.md`
- `approval-and-escalation-model.md`
- `decision-continuity-doctrine.md`
- `recommendation-packaging-doctrine.md`
- `auth-and-actor-model.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../workflows/project-intake-workflow.md`
