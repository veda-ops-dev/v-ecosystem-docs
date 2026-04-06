## Pass 4 Findings — Workflow Codability

Doc audited: `project-intake-workflow.md`
Date: 2025-04-05

### Files loaded
- `C:\dev\v-ecosystem-docs\workflows\project-intake-workflow.md`
- `C:\dev\v-ecosystem-docs\audit\pass-4\pass-4-workflow-codability.md`
- `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md`
- `C:\dev\v-ecosystem-docs\interfaces\veda-to-project-v-signal-interface.md`

### Files excluded
- `C:\dev\v-ecosystem-docs\governance\decision-continuity-doctrine.md` — referenced in Stage 6 boundary rule but not needed to judge stage and transition codability
- `C:\dev\v-ecosystem-docs\strategy\opportunity-scoring-model.md` — marked *(planned)* in Related Docs; does not exist
- `C:\dev\v-ecosystem-docs\workflows\handoff-workflow.md` — referenced as downstream; out of scope for this doc's workflow codability

---

### Checklist results

WF-1: PASS — Six stages are explicitly named: Signal Reaches Planning, Intake Framing, Planning Interpretation, Intake Evaluation, Intake Outcome, Post-Intake Direction.

WF-2: PASS — Each stage has a clear prose description of purpose. Stage 1 receives signal; Stage 2 frames the question; Stage 3 interprets; Stage 4 evaluates; Stage 5 produces outcome; Stage 6 routes post-outcome direction.

WF-3: FAIL — Entry conditions are not defined as testable guards per stage. The document defines workflow-level preconditions ("planning-relevant signal or evidence has reached Project V through the appropriate signal path") but does not specify what must be true to enter each individual stage. For example, Stage 3 — Planning Interpretation has no defined entry condition distinguishing it from Stage 2 completion. Stage 4 — Intake Evaluation has no defined entry condition stating what must be true about Stage 3 output before evaluation begins. A developer implementing stage transitions cannot determine when any individual stage is eligible to begin.

WF-4: FAIL — Exit conditions are not defined per stage. No stage specifies what must be true to leave it and move to the next. Stage 2 describes what Project V "frames" but not what constitutes a complete frame that permits exit. Stage 4 describes evaluation considerations ("whether there is enough bounded signal or justified planning input to act") but does not define the threshold or signal that closes evaluation and emits an outcome. The workflow cannot be encoded as a state machine without invented exit guards.

WF-5: PARTIAL — Transitions are implied by stage order but not explicitly defined as (from, on-condition, to) triples. Stage 6 is the only stage with explicit branching behavior: it names re-entry points ("Stage 2 if the intake framing question still needs work" / "Stage 3 if the intake framing question is already established"). All other transitions are implied by narrative sequence only.

WF-6: FAIL — Transition triggers are not defined. No stage specifies the event, completion signal, or condition that causes transition to the next stage. Stage 5 produces an outcome ("create project," "defer," etc.) but does not define what triggers exit from Stage 5 or entry into Stage 6. The difference between "evaluation not yet complete" and "evaluation complete with outcome" is not encoded. A developer must invent all triggers.

WF-7: FAIL — Invalid or blocked transitions are not addressed. There is no specification of what happens if Stage 2 cannot frame an intake question (not the same as "hold" — that is an outcome, not a framing failure), what happens if Stage 3 interpretation yields an internally contradictory result, or whether the workflow can be abandoned before Stage 5. The only partial coverage is the re-entry logic in Stage 6 (resume at Stage 2 or Stage 3 after additional evidence), but this does not cover forward-path blocking.

WF-8: PARTIAL — Cross-system interactions are identified at Stage 1 (VEDA provides signal to Project V via the VEDA-to-Project-V signal interface) and at Stage 6 ("VEDA may later supply more bounded signal if requested through the correct path"). However, Stage 4 references governance rules that "may affect what can be finalized" and references the approval model, but the cross-system interaction with the approval system is not identified as an explicit system call — only as a reference to a governance doc. No concrete interaction is specified for how Project V requests additional evidence from VEDA or how that request is structured.

WF-9: PARTIAL — Responsible actors are named per stage (Project V owns Stages 2–6; VEDA owns Stage 1 signal truth). However, the approval and governance actors are not concretely named. Stage 4 states "governance review or human review may be required" but does not identify which system or actor performs that review or how the review result is communicated back into the workflow.

WF-10: FAIL — Handoffs between systems and humans are not explicit. The Human-In-The-Loop section states that human review "may be required" but does not specify at which stage the workflow pauses, what form the approval request takes, who receives it, what the workflow state is while awaiting review, or how the review result re-enters the workflow. The approval model reference (Class B / Class C) provides classification but not handoff mechanics. A developer cannot implement the human approval interaction from this doc.

WF-11: PARTIAL — Failure states are partially addressed. Stage 4 permits "request additional bounded evidence" as an intake outcome, and Stage 6 defines re-entry points for that case. However, there is no defined failure state for: signal that cannot be framed at Stage 2, interpretation that yields no usable planning meaning at Stage 3, evaluation that cannot resolve within a defined period, or a human approval request that is not responded to.

WF-12: FAIL — Retry, rollback, and re-entry paths are not defined except for the one case in Stage 6 (re-entry at Stage 2 or Stage 3 after additional evidence is returned). No retry path is defined for evaluation timeout, failed framing, or rejected approval. Rollback is not addressed at any stage.

WF-13: FAIL — Escalation paths are not defined within the workflow. The approval model doc defines escalation principles but the workflow doc does not specify when escalation is triggered during intake, who receives the escalation, or what the workflow state becomes during escalation. "Escalation" is not mentioned in the workflow doc body at all.

WF-14: PARTIAL — Human approval points are identified in the Human-In-The-Loop section and Stage 4 boundary rule ("Governance review or human review may be required before an intake outcome becomes active"). However, the specific stage at which the workflow pauses for human review is not defined. The section lists triggering conditions (project creation significance, strategic importance, uncertainty, cost implications, material priority change) but these are not encoded as testable guards that would tell an implementation when to halt and request human input.

WF-15: FAIL — Required human action is not defined. The Human-In-The-Loop section references the approval-and-escalation model but does not specify what the human must do (approve, reject, revise, request more evidence) or in what form. The workflow doc defers entirely to the governance doc for this, and the governance doc defines approval principles but not the mechanics of human action within the intake workflow.

WF-16: FAIL — The effect of human approval or rejection on the intake workflow state is not defined. If a human approves a Class B intake outcome (e.g., project creation), the workflow does not specify what changes. If a human rejects, the workflow does not specify whether the result is a "reject" intake outcome, a return to Stage 3, or something else. The governance doc covers rejection semantics at a principle level but the workflow does not wire those principles into its own stage transitions.

WF-17: FAIL — The workflow does not specify what records or trail artifacts must be produced at any stage. The Intake Outcome Semantics section defines what an intake outcome "should be interpretable as" (what was considered, what signal mattered, what outcome was produced), but this is stated as semantic guidance, not as a required artifact specification. No stage specifies a record that must be written, stored, or made available.

WF-18: FAIL — Traceability across stages is not addressed. There is no specification of how the intake framing from Stage 2 is carried into Stage 3, how the interpretation from Stage 3 is available to Stage 4, or how any stage's outputs are preserved to support later review or re-entry. The doc states what each stage "may consider" but not what it must output in a traceable form.

WF-19: FAIL — State changes are not defined as observable or auditable events. The Retention Principle and Intake Outcome Semantics sections address what outcomes mean, but no stage specifies that a state change must be recorded, emitted, or made visible. "These semantics may later be represented through specific records or workflow structures, but the semantic contract comes first" explicitly defers observable structure to later design.

WF-20: PARTIAL — The happy-path narrative is coherent enough to understand the intended flow and ownership responsibilities. A developer could write a rough skeleton of the workflow. However, the workflow cannot be encoded as a complete state machine because entry/exit conditions, transition triggers, failure states, human touchpoint mechanics, and traceability requirements are all absent or deferred.

WF-21: FAIL — Multiple hidden assumptions block implementation. (1) The doc assumes an operative definition of "planning-relevant signal" that determines Stage 1 validity but does not define this concretely. (2) The doc assumes "governance review or human review may be required" can be evaluated at Stage 4, but does not define the evaluation logic that determines when it is required. (3) The doc assumes that "request additional bounded evidence" as an intake outcome triggers a path back to VEDA, but does not define how that request is formed or routed. (4) The doc assumes the approval model governs approval mechanics without integrating those mechanics into the workflow stages.

---

### Score
3 of 21 PASS — 5 PARTIAL — 13 FAIL

---

### Critical codability gaps

**WF-3 (entry conditions):** No per-stage entry conditions are defined. A developer cannot determine when any stage is eligible to begin. Each stage has a "Description" and "Responsibility" section but no "Entry Condition" field or equivalent.

**WF-4 (exit conditions):** No per-stage exit conditions are defined. Stage 4 lists evaluation considerations including "whether there is enough bounded signal or justified planning input to act" but provides no threshold or completion signal that closes the stage.

**WF-6 (transition triggers):** No event or condition triggers stage transitions. The workflow reads as a sequence of named stages with no mechanism connecting them.

**WF-7 (invalid/blocked transitions):** Forward-path blocking (e.g., framing fails at Stage 2, interpretation yields nothing at Stage 3, evaluation cannot resolve) is entirely absent from the doc.

**WF-10 (handoffs):** Human approval handoff mechanics are unspecified. The workflow cannot pause at a defined point, form a reviewable approval request, or receive and process a human review result.

**WF-12 (retry/rollback):** Only one re-entry path is defined (Stage 6 back to Stage 2 or 3 on additional evidence). No retry or rollback behavior exists for any other failure or blocking condition.

**WF-13 (escalation):** Escalation is not mentioned in the workflow body. The governance doc defines escalation principles, but the workflow does not wire them to any stage or condition.

**WF-15 (required human action):** What the human must do at the approval point — approve, reject, revise, request evidence — and in what form, is not specified in the workflow doc.

**WF-16 (effect of human approval/rejection):** How approval or rejection re-enters the workflow and affects stage state or transition is not defined. The governance doc covers rejection principles; the workflow does not connect them to its own stage model.

**WF-17 (records/trail artifacts):** No stage specifies a required output record. Intake outcome semantics are explicitly deferred: "These semantics may later be represented through specific records or workflow structures, but the semantic contract comes first."

**WF-18 (traceability across stages):** Stage outputs are not defined. How Stage 2 framing is passed to Stage 3, or how Stage 3 interpretation is available to Stage 4, is unspecified.

**WF-19 (observable/auditable state changes):** No state change is defined as an observable or auditable event. The doc explicitly defers this structure to later design.

**WF-21 (hidden assumptions):** At least four implementation-blocking assumptions are embedded without resolution: operative definition of "planning-relevant signal" as a Stage 1 guard; evaluation logic for when human review is required at Stage 4; mechanics for requesting additional evidence from VEDA; integration of approval model mechanics into stage transitions.

---

### Codability verdict
Not codable without major clarification

---

### Summary
The project-intake-workflow doc establishes a coherent ownership narrative and a correct high-level role split (VEDA supplies signal, Project V owns all intake stages, V Forge is excluded). However, it is not codable as written: it defines no per-stage entry or exit conditions, no transition triggers, no human approval handoff mechanics, no required output records, and no observable state change specification. The workflow can inform a developer's conceptual understanding of intake but cannot be implemented as a state machine without substantial invention of guards, triggers, and traceability structure.

---

### Out-of-scope observations not included in findings
The `opportunity-scoring-model.md` referenced in Related Docs is marked *(planned)* and does not exist. Stage 4 depends on planning, governance, and strategy posture for evaluation, but the scoring model that would make evaluation concrete is absent. This is a cross-system consistency issue, not a workflow codability issue, and belongs in Pass 5.
