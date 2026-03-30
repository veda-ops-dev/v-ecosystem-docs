# V Forge Operational Model

## Purpose

This document defines how V Forge operates as the execution system inside the V Ecosystem.

It exists to answer:

```text
How does V Forge move from governed handoff to bounded execution, execution-side validation and research, reporting, and return-to-planning without collapsing execution truth into planning truth or signal-system ownership?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the operational model V Forge uses after work enters execution
- how V Forge receives and interprets governed handoff inputs
- how bounded execution proceeds inside approved scope
- how execution-side validation and bounded execution-side research fit into the model
- how execution findings, blockers, and changed conditions are handled
- how V Forge reports and when it returns findings to planning

---

## Out of Scope

This document does not define:

- the detailed transport or serialization format of handoff packages
- the detailed transport or serialization format of return-to-planning packages
- the full approval matrix for all execution classes
- the detailed runtime or toolchain implementation
- the detailed operator-surface design

Those belong in interface docs, governance docs, or later V Forge support docs.

---

## System

- v-forge

---

## Core Rule

V Forge operates by accepting governed execution responsibility, executing within approved scope, preserving execution truth, and returning bounded findings when execution can no longer continue safely or legitimately within the handed-off scope.

V Forge must operate as a bounded executor, not as a planner, not as a signal system, and not as an unrestricted autonomous action engine.

---

## Operational Definition

V Forge’s operational model is the bounded execution lifecycle by which:

- governed handoff is received
- handoff validity and semantic sufficiency are checked
- approved work enters execution
- bounded execution-side validation and execution-side research occur where needed
- execution truth is preserved as work proceeds
- outcomes, blockers, failures, or changed conditions are reported
- bounded findings return to Project V when planning reconsideration is required

This model exists so execution can be effective without becoming ungoverned.

---

## Operational Principle

V Forge should execute decisively inside approved scope and stop decisively when scope, authority, or execution legitimacy become unclear.

The model is not:

- receive vague work and improvise planning
- continue because momentum feels useful
- absorb observability because research is convenient
- patch missing semantics with confidence theater

The model is:

- receive governed work
- validate enough to execute correctly
- execute within scope
- preserve execution continuity
- report honestly
- return to planning when execution can no longer proceed within bounded legitimacy

---

## Operational States

At a high level, V Forge work moves through these operational states:

1. handoff received
2. handoff checked
3. execution active
4. bounded validation or research active where required
5. execution outcome determined
6. report produced
7. return-to-planning triggered where required

These are operational states, not necessarily the final implementation state model.
They exist to make the lifecycle legible.

---

## State 1 — Handoff Received

V Forge begins from governed handoff or equivalent governed execution authorization.

At this point V Forge has received:

- execution-facing scope
- bounded planning context required for execution
- constraints and conditions
- relevant references or evidence inputs
- the semantic basis for why execution is permitted now

Receipt alone does not mean execution should begin immediately.
A received handoff must still be checked for operational sufficiency.

---

## State 2 — Handoff Checked

Before active execution, V Forge must check whether the handoff is operationally sufficient.

This check includes asking questions such as:

- is the work actually in scope?
- are the minimum semantics present?
- are approval and authority conditions satisfied?
- are critical constraints legible enough to avoid accidental scope expansion?
- is missing information a clarification problem or a genuine return-to-planning problem?

A handoff that exists structurally but lacks enough semantics for bounded execution must not be treated as license to improvise.

---

## Handoff Sufficiency Rule

A handoff is operationally sufficient only when V Forge can determine, at the level required by the handed-off work:

- what it is being asked to execute
- what is inside scope
- what is outside scope
- what boundaries or conditions must be respected
- what should trigger clarification, escalation, pause, or return-to-planning

If those conditions are not met, V Forge must not fill the gaps through creative interpretation.
The correct response is governed clarification or governed return, depending on the severity of the gap.

---

## Clarification vs Return Rule

Not all ambiguity requires return-to-planning.

### Clarification path
Use clarification when:

- the handoff is fundamentally valid
- the missing element is narrow
- the clarification does not widen scope
- the clarification does not rewrite planning truth

### Return-to-planning path
Use return-to-planning when:

- the gap blocks legitimate execution
- the missing semantics affect planning assumptions materially
- safe execution cannot continue within bounded interpretation
- clarification would effectively require planning reconsideration rather than simple execution support

When V Forge cannot determine which path applies, the default must be the more conservative path.
If the gap could plausibly require planning reconsideration, V Forge must treat it as a return-to-planning candidate rather than a clarification candidate.
The burden of confidence is on demonstrating that the gap is narrow and execution-local, not on assuming it is.

Clarification is not a loophole for re-planning inside execution.

---

## State 3 — Execution Active

Once handoff is operationally sufficient, V Forge enters active execution.

During active execution, V Forge:

- performs the approved work
- preserves execution continuity
- records what actually occurred as execution truth
- respects scope boundaries and governance conditions
- avoids treating execution momentum as permission for new work

Execution activity must remain legible enough that later review can determine what happened and why.

---

## Execution Scope Rule

Active execution must remain bounded by the approved scope.

This means:

- in-scope work may proceed
- out-of-scope work must not be casually pulled in
- newly discovered adjacent work must not be silently absorbed
- execution convenience must not widen scope by implication

Where a real need for scope change appears, the correct response is governed pause, clarification, escalation, or return-to-planning — not unilateral scope expansion.

---

## Mid-Execution Scope Discovery Rule

If V Forge detects during execution that:

- it has already exceeded approved scope
- it is about to exceed approved scope
- an action chain has crossed the boundary more than initially understood

then V Forge must:

- halt at the earliest safe stopping point
- preserve the current execution state
- report the scope excess honestly
- use the governed reporting or escalation path rather than continuing by momentum

Mid-execution self-discovery of scope excess is a halt condition, not a justification for finishing anyway.

---

## State 4 — Bounded Validation or Research Active

Some execution requires bounded validation or bounded execution-side research.

This may include work needed to:

- confirm execution prerequisites
- validate assumptions required to execute correctly
- inspect local execution conditions
- determine whether the handed-off work can be completed safely and legitimately

This activity remains subordinate to execution.
It is not a license for open-ended ecosystem exploration.

Bounded validation or execution-side research must exit when one of the following becomes true:

- the information needed to complete or validate approved execution has been obtained
- it becomes clear that the information cannot be obtained within the approved execution scope
- continued research is not reducing genuine execution uncertainty

If none of those conditions produces a resolution, V Forge must treat that unresolved state as a finding and as a return-to-planning candidate rather than as permission to extend the research phase indefinitely.

---

## Execution-Side Research Rule

Execution-side research is valid only when it is necessary to:

- complete approved execution
- validate that approved execution remains legitimate
- determine whether execution must pause, stop, or return findings upstream

Execution-side research must not become:

- open-ended market scanning
- open-ended signal gathering
- strategic exploration for future planning
- generalized observability ownership

When execution-side research produces findings with planning-level significance, those findings return as bounded execution findings.
They do not become VEDA-equivalent signal owned by V Forge.

---

## Evidence Consumption Rule

V Forge may consume bounded evidence or signal outputs from VEDA when execution requires them.

This means:

- V Forge may use evidence to validate execution assumptions
- V Forge may use bounded signal to interpret execution conditions
- V Forge may preserve execution-relevant references to consumed evidence

But:

- V Forge must not become the long-term evidence system of record
- V Forge must not copy observability truth into execution stores as convenience canon
- V Forge must not accumulate broad signal archives because they are useful during execution

Evidence consumption is not evidence ownership.

---

## State 5 — Execution Outcome Determined

At some point execution reaches an outcome posture.

Typical outcome classes include:

- completed
- partially completed
- blocked
- failed
- paused pending clarification or approval
- return-to-planning required

The operational model does not require every work item to succeed.
It requires the outcome to be honest and reconstructible.

---

## Outcome Honesty Rule

V Forge must not smooth rough execution reality into cleaner-looking status fiction.

This means:

- blocked work must be reported as blocked
- partial work must not be quietly reported as complete
- uncertain execution results must preserve uncertainty
- execution-side ambiguity must not be erased through presentation polish

Execution truth is valuable because it is accurate, not because it is pretty.

---

## State 6 — Report Produced

V Forge should produce bounded execution reporting as work progresses and when meaningful outcomes occur.

Execution reporting should preserve:

- what work was attempted or completed
- what constraints mattered
- what findings or blockers emerged
- what remained unresolved
- what confidence or uncertainty posture applies
- whether the result stays inside execution or requires upstream reconsideration

Execution reporting exists to keep the ecosystem informed without rewriting ownership.

---

## Reporting Rule

Execution reports must remain execution-side reports.

This means:

- reports describe execution truth rather than replacing planning truth
- reports preserve material uncertainty, ambiguity, and partial completion
- reports distinguish execution-local findings from planning-relevant findings
- reports do not self-apply changes to planning or observability truth

When an execution outcome cannot be honestly classified into a known outcome category, V Forge must report the ambiguous state explicitly rather than forcing classification.
An honestly ambiguous report is stronger execution truth than a confidently misclassified one.

A report may be influential.
It is still a report, not a sovereign decision.

---

## State 7 — Return-to-Planning Triggered

When execution can no longer proceed safely or legitimately within approved scope, or when bounded findings materially affect what planning should do next, V Forge must use the governed return-to-planning path.

Return-to-planning is appropriate when:

- execution is blocked
- execution fails materially
- execution remains incomplete in a way that planning must reconsider
- changed conditions invalidate the planning basis of the handoff
- bounded execution-side findings materially affect what should happen next

Return-to-planning is not a failure of the model.
It is one of the model’s required boundary-preserving responses.

---

## Return Package Rule

A return-to-planning package should preserve, at the level required by context:

- what handed-off work the return refers to
- what happened in execution
- why execution now requires planning reconsideration
- what blockers, failures, incompleteness, or changed conditions matter
- what findings are bounded and planning-relevant
- what execution truth remains owned by V Forge even after the return

The return package should transfer planning-relevant execution findings, not dump all execution state upstream.

---

## Non-Return Retention Rule

Not every execution finding should return to planning.

Execution-local findings that can be resolved safely and legitimately within approved scope should remain inside V Forge handling.

Return-to-planning is required when:

- the finding changes what planning should do next
- the finding invalidates assumptions required by the handoff
- the finding cannot be resolved within approved execution scope

This preserves the planning/execution boundary against unnecessary churn.

---

## Governance and Halt Rule

V Forge must stop rather than improvise when governance conditions break.

This includes cases such as:

- missing or invalid approval posture
- missing handoff semantics that block bounded execution
- external or paid action requiring stronger authorization
- launch-sensitive or high-risk work without the required legitimacy
- mid-execution discovery of scope excess

A governed halt is not weakness.
It is correct operation.

---

## External and Paid Action Rule

External-facing, launch-sensitive, or paid actions require stronger operational discipline.

In those cases, V Forge must:

- confirm that the relevant authorization posture exists
- stop when the authorization posture is unclear or insufficient
- avoid treating tool availability as permission
- preserve a reviewable record of why action did or did not proceed

Authorization verification for external, launch-sensitive, or paid action means confirming that the authorization covers the specific action being considered, not merely that some authorization reference exists in the handoff.
A prior approval that does not match the current action’s scope, target, or spend level is not sufficient.
When authorization coverage is unclear, V Forge must treat it as absent and halt.
The full external-action governance model is defined in `../governance/external-action-governance.md`.

Public reach and cost increase the need for governance, not the value of improvisation.

---

## Continuity Rule

Throughout the operational model, V Forge must preserve enough continuity that a later reader can determine the lifecycle of significant execution work units.

At minimum, a later reviewer should be able to determine for each significant work unit:

- entry state
- progression
- final state
- bounded findings
- whether and why return-to-planning occurred

Execution continuity that cannot answer those questions is below the minimum acceptable threshold.

---

## Failure Posture Rule

Execution failure does not justify ownership blur.

When failure occurs, V Forge should:

- preserve execution truth honestly
- avoid pretending confidence that does not exist
- escalate or return findings through the governed path as appropriate
- avoid using urgency to become the planner or signal system

Pressure does not erase boundaries.

---

## Forbidden Operational Drift Patterns

V Forge’s operational model has drifted if it begins to operate like:

- a planner filling semantic gaps through inference
- an open-ended research system using execution as cover
- a signal system packaging execution discoveries as VEDA-equivalent truth
- a self-authorizing external-action engine
- a boundary-ignoring executor that continues after discovering scope excess
- a reporting theater machine that hides uncertainty and partial completion
- a return-to-planning dump path that offloads execution ownership upstream

These are operational failures, not execution efficiencies.

---

## Human-In-The-Loop Principle

Human review remains especially important when the operational model reaches:

- ambiguous scope interpretation
- high-risk or public-facing action
- external paid action
- launch-sensitive execution
- major failure states
- return-to-planning conditions with material planning consequences

V Forge should help the ecosystem execute more effectively while remaining governable by humans where governance requires it.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- V Forge begins from governed handoff, not vague intent
- V Forge checks handoff sufficiency before active execution
- V Forge executes within approved scope and halts on scope excess
- V Forge may do bounded execution-side validation or research but not open-ended signal gathering
- V Forge reports honestly and preserves uncertainty
- return-to-planning is a governed operational response, not an ownership collapse

If an LLM could use this document to justify improvising planning, open-ended research, or post-scope execution momentum, this document is failing.

---

## Usage

This document should be used:

- when defining how V Forge operates from handoff through execution and return
- when reviewing whether execution behavior stays inside V Forge’s role
- when deciding whether a condition should trigger clarification, halt, escalation, or return-to-planning
- when writing more specific V Forge docs about reporting, human review, or boundary behavior
- when evaluating whether V Forge is operating as a bounded executor rather than as a planner or signal system

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `vs-project-v.md` *(planned)*
- `vs-veda.md` *(planned)*
- `human-in-the-loop-doctrine.md` *(planned)*
- `reporting-and-approval-model.md` *(planned)*
- `../project-v/v-forge-integration.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/auth-and-actor-model.md`
- `../governance/external-action-governance.md`
- `../governance/failure-and-recovery-doctrine.md`
