## Pass 4 Findings — Workflow Codability

Doc audited: `maintenance-and-replanning-workflow.md`
Date: 2025-04-05

### Files loaded
- `C:\dev\v-ecosystem-docs\workflows\maintenance-and-replanning-workflow.md`
- `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md` (loaded in prior session)
- `C:\dev\v-ecosystem-docs\governance\failure-and-recovery-doctrine.md` (loaded in prior session)
- `C:\dev\v-ecosystem-docs\interfaces\veda-to-project-v-signal-interface.md` (loaded in prior session)

### Files excluded
- `C:\dev\v-ecosystem-docs\interfaces\v-forge-to-project-v-return-to-planning-interface.md` — referenced for return input handling; downstream interface, not needed to judge this workflow's stage codability
- `C:\dev\v-ecosystem-docs\governance\decision-continuity-doctrine.md` — referenced for decision context handling; governs a referenced concern, not needed to judge stage/transition codability
- `C:\dev\v-ecosystem-docs\governance\invalidation-and-supersedence-doctrine.md` — referenced for Stage 5 action types; downstream governance, not needed to judge transition codability
- `C:\dev\v-ecosystem-docs\governance\evidence-continuity-model.md` — referenced for evidence trust posture; not needed to judge stage/transition codability

---

### Checklist results

WF-1: PASS — Six stages are explicitly named: Trigger Recognition and Classification, Return-to-Planning Input Handling, Prior Decision Context Retrieval, Replanning Scope Determination, Governed Replanning, Replanning Outcome Preservation.

WF-2: PASS — Each stage has a clear stated purpose. Stage 1 classifies the trigger; Stage 2 receives and assesses return-to-planning inputs; Stage 3 retrieves prior decision context; Stage 4 determines bounded replanning scope; Stage 5 performs replanning; Stage 6 preserves outcomes durably.

WF-3: PARTIAL — The Workflow Triggers section provides the strongest trigger enumeration in the Pass 4 set: six explicit conditions that trigger the workflow, plus four explicit non-triggers. This is meaningful partial entry structure at the workflow level. However, per-stage entry conditions are not defined. Stage 2 has no entry condition distinguishing it from Stage 1 completion — the doc notes Stage 2 applies "when V Forge has returned bounded execution findings" but this is not wired to Stage 1's output as a testable guard. Stage 3 has no entry condition specifying what Stage 1 or Stage 2 must have produced to begin prior decision retrieval. Stage 5 has no entry condition requiring Stage 4 scope determination to be complete before replanning begins.

WF-4: FAIL — Exit conditions are not defined per stage. Stage 1 describes what classification "must determine" but not the completion criterion — when is classification done enough to proceed to Stage 2? Stage 3 describes what must be "established" before replanning begins but not what constitutes established. Stage 4 lists what scope determination "includes" but not the exit condition — what result closes scope determination and permits Stage 5 entry? No stage provides a machine-testable closure criterion.

WF-5: PARTIAL — The workflow is the only one in the Pass 4 set that defines two distinct structural paths through the same doc: the "replanning path" (Stages 1–6) and the "maintenance activity model" (explicitly exempt from Stages 1–6). Stage 5 includes an explicit escalation branch: "when replanning scope cannot be bounded without reopening so many prior governing decisions that the reconsideration effectively becomes a new planning baseline, the correct response is escalation." This is the most specific branching condition in the Pass 4 set. However, forward transitions between Stages 1–6 are implied by narrative order only and are not defined as (from, on-condition, to) triples.

WF-6: FAIL — Transition triggers are not defined for any individual stage. The Workflow Triggers section defines what triggers the workflow as a whole but not what triggers each stage transition. The difference between "Stage 1 classification in progress" and "Stage 1 classification complete, proceed to Stage 2" is not encoded. Stage 2 applies conditionally ("when V Forge has returned bounded execution findings") but does not specify how that condition is evaluated or what closes Stage 1 in the absence of a V Forge return. A developer must invent all forward triggers.

WF-7: PARTIAL — Stage 5 explicitly addresses one blocked-forward-transition case: when replanning scope "cannot be bounded without reopening so many prior governing decisions," the correct response is escalation, not continuation. The Maintenance Activity Model explicitly defines what must not trigger the workflow (execution findings resolvable within scope, minor variations, operator preference without material basis). The Boundary Rule at Stage 4 names "scope creep disguised as governance" as a pattern that must not substitute for the bounded replanning path. These are meaningful structural guards. However, per-stage blocking conditions are not enumerated — what constitutes a blocked Stage 2 (return-to-planning input that cannot be assessed), or a blocked Stage 3 (prior decision context that cannot be retrieved), is not addressed.

WF-8: PARTIAL — Cross-system interactions are identified at a role level per stage: Stage 1 = V Forge surfaces via return-to-planning interface, VEDA surfaces via signal interface, operators via governed direction; Stage 2 = Project V receives from V Forge via governed return-to-planning interface; Stage 3 = Project V retrieves internal planning context; Stage 4–5 = Project V with operator direction; Stage 6 = V Forge is "informed of any scope or constraint changes through the governed interface." However, no stage specifies a concrete call structure. Stage 6's requirement to inform V Forge does not name the specific interface. Stage 1's reference to "governed return-to-planning interface" names the path but does not specify the interaction mechanics.

WF-9: PARTIAL — Responsible actors are named throughout and the split is clear: Project V owns Stages 1–6 planning work; V Forge surfaces findings via governed interface; VEDA surfaces signal via governed interface; operators surface triggers via governed direction. Stage 5 references "approval posture requirements" but the approving actor is not concretely identified within the workflow.

WF-10: FAIL — Human approval handoff mechanics are not defined. The Human-In-The-Loop Principle lists five conditions requiring human review. Stage 5 contains the escalation rule for when replanning effectively becomes a new planning baseline requiring "human review and governed approval." However, the workflow does not specify: at which stage the workflow pauses for human involvement, what form the approval request takes, who receives it, what workflow state is held while pending, or how the human result re-enters the workflow. As with all prior docs, the governance docs are referenced but not wired into stage mechanics.

WF-11: PARTIAL — The Failure and Interruption Principle addresses workflow interruption explicitly: "when the replanning workflow cannot legitimately progress — including when decision context cannot be established, when prior decisions are in conflict, or when required approval is not available — the interruption must remain explicit." Three specific interruption conditions are named. However, failure states are not defined per stage. What constitutes a failure at Stage 2 (return input cannot be assessed) vs Stage 3 (prior context unrecoverable) vs Stage 5 (replanning produces contradiction) is not specified. Failure handling is referenced to failure-and-recovery-doctrine.md but not integrated into the workflow.

WF-12: PARTIAL — The Stage 5 escalation branch provides a re-routing path for one specific condition (replanning scope unboundable). The doc explicitly notes that maintenance activity bypasses the workflow, implying a fast-path out. The Workflow Triggers section's non-trigger list defines conditions that must not re-enter the workflow. However, retry or re-entry paths for workflow interruptions (Stage 3 context unrecoverable, Stage 5 approval not available) are not defined within the workflow. These are referenced to failure-and-recovery-doctrine.md only.

WF-13: FAIL — Escalation is referenced in Stage 5 as the correct response when replanning scope exceeds bounded reconsideration, and in the Failure and Interruption Principle as an interruption case. However, no escalation path is defined within the workflow. Who receives the escalation, what the workflow state becomes during escalation, what closes escalation, and how the result re-enters Stage 5 or redirects to a new planning cycle are all unspecified.

WF-14: PARTIAL — The Human-In-The-Loop Principle lists five conditions requiring human review with more specificity than most prior workflow docs (superseding/invalidating prior governing decisions, significant scope change, revised handoff activation, cross-system interface effects, external paid action triggers). Stage 5 explicitly identifies the escalation-to-new-planning-baseline case as requiring "human review and governed approval before proceeding as such." These are the most concrete human-trigger conditions in the Pass 4 set. However, the specific stage at which the workflow pauses is not defined as a formal hold state, and the triggering conditions are not encoded as testable guards.

WF-15: FAIL — Required human action is not defined within the workflow. The Human-In-The-Loop Principle defers to approval-and-escalation-model.md. What the human must do — approve, reject, conditionally approve, specify replanning bounds — and in what form is not specified in the workflow.

WF-16: FAIL — The effect of human approval or rejection on workflow state is not defined. If a human approves a replanning scope at Stage 5, the workflow does not specify what state transition occurs. If a human rejects (or demands narrowing), the workflow does not specify whether the result is a return to Stage 4, Stage 1, or something else. The Stage 5 escalation-to-new-planning-cycle case names the required outcome ("new planning cycle") but does not specify how the workflow transitions into that state.

WF-17: PARTIAL — Stage 6 requires: revised or new governing decisions to be "recorded explicitly," prior decisions to be "marked as reaffirmed, revised, superseded, or invalidated," and the connection between trigger, reconsideration, and outcome to be "traceable." The Replanning Outcome Preservation stage has the most concrete artifact language in the Pass 4 set. The boundary rule at Stage 6 states: "A replanning event that leaves no durable trace has not produced governed continuity." However, no stage specifies a concrete record format, storage location, or which system must write what artifact. The traceability requirement is real but not operationally specified.

WF-18: PARTIAL — Stage 3 explicitly requires that prior governing decisions and approval basis must be retrieved before Stage 4 scope determination, establishing an inter-stage data dependency. The Decision Continuity Principle requires that "replanning events must reference prior governing decisions rather than treating them as absent." The Evidence Continuity Principle requires that "what signal or findings triggered reconsideration" must be preserved with trust posture. These are the strongest inter-stage continuity requirements in the Pass 4 set. However, how Stage 1 classification output is formally available to Stage 2, or how Stage 3 prior decision context is formally available to Stage 4 scope determination, is not specified as a concrete data contract.

WF-19: FAIL — State changes are not defined as observable or auditable events. Stage 6 requires durable preservation of replanning outcomes but does not specify that stage transitions within the replanning workflow must themselves be recorded or emitted as events. Whether trigger classification at Stage 1 produces an auditable record is unspecified. The requirement in Stage 6 applies to replanning outcomes, not to workflow progression events.

WF-20: PARTIAL — This is the most structurally complete workflow in the Pass 4 set alongside post-launch-observation. The Workflow Triggers section provides a concrete six-condition trigger list plus four non-triggers. The maintenance/replanning distinction provides an explicit fast-path bypass. The Stage 5 escalation branch defines a specific overflow condition. The Stage 6 artifact language is the most concrete in the set. The Stage 3 → Stage 4 data dependency is stated. A developer could write a more complete skeleton from this doc than from any other in the set. However, per-stage exit conditions, concrete transition triggers, human approval mechanics, per-stage failure states, escalation path mechanics, and observable state change specification are all absent, blocking full state machine implementation.

WF-21: FAIL — Multiple hidden assumptions block implementation. (1) The Workflow Triggers section defines six triggers but does not specify how each trigger arrives — which interface, in what form, requiring what to evaluate trigger materiality. (2) Stage 4 scope determination assumes a definition of "what the trigger actually requires reconsideration of" but does not provide an evaluation method. (3) Stage 5 escalation condition ("cannot be bounded without reopening so many prior governing decisions") has no defined threshold. (4) Stage 5 assumption that approval posture requirements can be evaluated during replanning depends on undefined cross-reference to governance docs not integrated into the stage. (5) Stage 6 "informing V Forge of scope or constraint changes through the governed interface" assumes a specific interface but does not name it — the return-to-planning interface is for V Forge → Project V, and the interface for Project V → V Forge scope updates is not identified in this doc.

---

### Score
2 of 21 PASS — 9 PARTIAL — 10 FAIL

---

### Critical codability gaps

**WF-4 (exit conditions):** No per-stage exit conditions defined. Stage 1 classification, Stage 3 context retrieval, and Stage 4 scope determination all lack closure criteria.

**WF-6 (transition triggers):** No forward transition triggers defined. Workflow-level triggers are enumerated but stage-level transition events are absent.

**WF-10 (handoffs):** Human approval handoff mechanics are unspecified. Stage 5 human review requirement and the escalation-to-new-planning-cycle case both lack concrete pause point, request form, pending state, and result re-entry mechanics.

**WF-13 (escalation):** Stage 5 identifies the escalation condition but defines no escalation path — no recipient, no workflow state during escalation, no closure condition, no re-entry logic.

**WF-15 (required human action):** Human action is not defined within the workflow. Deferred to governance docs without workflow-level integration.

**WF-16 (effect of human approval/rejection):** Approval and rejection outcomes are not wired to workflow stage transitions. The escalation-to-new-planning-cycle outcome names the destination state but not the transition mechanics.

**WF-19 (observable/auditable state changes):** Workflow stage transitions are not defined as observable or auditable events. Stage 6 artifact requirement covers replanning outcomes, not workflow progression.

**WF-21 (hidden assumptions):** Five implementation-blocking assumptions: undefined trigger arrival interface and materiality evaluation; undefined scope determination method; undefined escalation threshold for Stage 5; undefined approval posture evaluation during replanning; unnamed interface for Project V → V Forge scope change notification.

---

### Codability verdict
Not codable without major clarification

---

### Summary
The maintenance-and-replanning-workflow is tied with post-launch-observation as the most structurally mature doc in the Pass 4 set: it has the strongest workflow-level trigger definition (six triggers, four non-triggers), an explicit maintenance/replanning fast-path distinction, a concrete Stage 5 escalation branch condition, and the most specific artifact language at Stage 6. Despite these strengths, it shares the same blocking structural gaps as all prior workflow docs — no per-stage exit conditions, no stage-level transition triggers, no human approval mechanics wired into stage transitions, and no observable state change specification. The Stage 5 escalation overflow condition is notably specific but its path mechanics are as undefined as in every other workflow in the set.

---

### Out-of-scope observations not included in findings
Stage 6 requires informing V Forge of scope changes "through the governed interface" but does not name the interface. The Project V → V Forge path for post-replanning scope notifications appears to have no dedicated interface doc in the current set. This is a structural gap for Pass 5 cross-system consistency review.
