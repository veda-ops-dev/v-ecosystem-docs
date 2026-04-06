# Desktop Human–LLM Interaction Model

## Purpose

This document defines how the human operator and the LLM interact inside the V Ecosystem desktop application so that the system remains powerful, usable, explicit, and governed.

It exists to answer:

```text
What is each party's role in the interaction, what interaction modes exist and what they are for, how does the operator frame work, how does the LLM present typed outputs, delegated outputs, continuity-aware outputs, and orchestration-aware outputs, how does the operator respond to those outputs, and what must the interaction model structurally prevent so that conversation does not become governance and model quality does not become authority?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the human operator's role in relation to the LLM
- the LLM's role in relation to the human operator
- interaction modes and what framing they require
- what constitutes explicit operator framing
- how the LLM presents each typed output
- how delegated work and orchestration state are surfaced during interaction
- how continuity artifacts and uncertainty are surfaced during interaction
- what the operator may do with each type of LLM output
- visibility requirements at the moment of interaction
- interaction anti-drift rules

This document builds on and assumes the active binding of:
- `desktop-llm-behavior-contract.md`
- `desktop-governance-and-gating-model.md`
- `desktop-state-and-context-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-memory-and-continuity-model.md`
- `desktop-surface-architecture.md`

---

## Out of Scope

This document does not define:

- specific UI component layout or visual design
- MCP tool schemas
- API endpoint design
- workflow-internal mechanics beyond what interaction requires

---

## System

- interfaces

---

## Core Rule

The human operator is the accountable party. The LLM is a strong bounded reasoner that produces typed inert outputs. The interaction between them is explicit framing, explicit output production, explicit review, and explicit human response — not a chat session where things subtly happen.

Neither party's role is diminished by this model. The operator provides direction and approval. The LLM provides synthesis, classification, packaging, conflict detection, bounded orchestration, and structured recommendation. Both are operating at full capability within their respective roles.

The interaction model fails in two directions. It fails if the LLM becomes the real workflow driver and the human becomes a rubber stamp. It fails if the LLM is so constrained it can no longer reason well enough to be useful. This document is about the path between those failures.

---

## Human Operator Role

The human operator inside the desktop application is:

**The accountable party.** The operator is responsible for the governed state of the project. What is planned, what is approved, what is handed off, and what is launched are all ultimately operator decisions. The LLM does not make those decisions.

**The framing source.** Before the LLM produces typed outputs with governance significance — Recommendations, Approval Request Packages, Intake classifications — the operator must frame what kind of work is being asked for. The LLM does not self-assign work modes or initiate those typed outputs from ambient conversation.

**The reviewer.** The operator reads, evaluates, and acts on LLM outputs. The operator does not auto-accept outputs because they are well-written or because the model is capable.

**The approval source where doctrine requires it.** For Class B and Class C actions, only the operator can satisfy the approval gate. No LLM output, delegated worker artifact, or continuity artifact constitutes that approval.

**Not merely a rubber stamp.** The interaction model must not train the operator to read and click. If the operator finds themselves always accepting LLM outputs without meaningful review, the interaction model has drifted into co-pilot territory and must be corrected.

---

## LLM Role

The LLM inside the desktop application is:

**A strong bounded reasoner.** The LLM may exercise full reasoning capability: synthesize across context, detect conflicts, identify gaps, classify, evaluate, package, and produce structured outputs. Its reasoning power is an asset and must not be artificially hobbled.

**A producer of typed inert outputs.** Every output the LLM produces is one of the typed outputs defined in `desktop-llm-behavior-contract.md`. Those outputs are inert until separately activated through the governed path. The LLM's job is to produce the best possible typed output, not to activate anything.

**A runtime participant that may operate through delegation.** The LLM may participate as a coordinator or specialist inside bounded orchestration. That changes runtime role, not authority.

**A governed support participant.** The LLM operates within current system context, workflow stage, decision continuity, evidence basis, visible continuity artifacts, and the filtered tool posture of the active session. It does not override those constraints because it believes it knows better.

**Not the owner of workflow state.** Workflow state lives in governed records, not in chat history or continuity memory. The LLM does not set, advance, or own workflow stage.

**Not the source of approval.** An LLM cannot approve a Class B or Class C action regardless of how complete its recommendation is. Its role ends at producing the best possible typed output for the operator to evaluate.

---

## Interaction Modes

Interaction modes are framing signals, not authority classes. A mode tells the LLM what kind of work is being requested so it can orient its reasoning and output type correctly. A mode does not override workflow gates, does not create approval authority, and does not widen what the LLM is permitted to do.

The desktop application supports the following interaction modes. The operator selects or declares the mode before substantive LLM engagement where mode selection is required.

### Brainstorm
The operator wants open-ended thinking without record creation or workflow advancement.

LLM behavior: produce Review Summary or Uncertainty Notice outputs only. Must not produce Recommendation or Approval Request Package. Must not suggest record creation paths unless the operator explicitly asks to switch to Intake mode.

Framing examples: "I'm just thinking through this — don't create anything." / "Talk me through the options here."

### Review
The operator wants the LLM to analyze a specific record, package, or context and report what it sees.

LLM behavior: produce Review Summary, Finding, Continuity Reminder, or Uncertainty Notice. Must not produce a Recommendation unless the operator requests one within this mode session.

Framing examples: "Review the current readiness state for this initiative." / "Tell me what the decision history looks like for this project."

### Intake
The operator wants the LLM to classify a work item or opportunity and produce a structured intake classification for review.

LLM behavior: produce a Recommendation typed as an intake classification. Must include all required recommendation elements: proposed classification, scope, basis, uncertainty, governance posture, acceptance and non-acceptance outcomes.

Framing examples: "Process this as an intake — classify and recommend." / "We have a new opportunity; run intake on it."

### Recommendation Packaging
The operator wants the LLM to produce a structured recommendation for a specific proposed action.

LLM behavior: produce a Recommendation with all required elements per `recommendation-packaging-doctrine.md`. Must clearly label that it is a recommendation, not an approval or activation.

Framing examples: "Package a recommendation for creating this initiative." / "Give me a recommendation on whether to activate this handoff."

### Approval Request Preparation
The operator wants the LLM to assemble the structured package required to request approval for a Class B or Class C action.

LLM behavior: produce an Approval Request Package with all required elements: action being requested, scope, basis, what approval covers, what happens if granted, what the default state is if not granted. Must be clearly labeled as a request pending approval, not an approval itself.

Framing examples: "Prepare an approval request for activating this handoff." / "Package the launch authorization request."

### Execution Report Review
The operator wants the LLM to interpret a V Forge execution report or finding and surface what it means for the current system context.

LLM behavior: produce a Finding or Review Summary that interprets the report within the current system context. Must not produce planning recommendations from within this mode unless the operator explicitly switches context to Project V and Recommendation Packaging. The finding reports what is; it does not decide what should happen next.

Framing examples: "Review this execution finding and tell me what it means." / "Interpret this pre-launch verification report."

### Mode selection requirement

Mode selection is required only when the operator wants typed outputs with governance significance: Recommendation, Approval Request Package, Intake classification.

For Review, Brainstorm, and Execution Report Review modes, the operator may state their intent conversationally, such as `review the readiness state` or `I'm just thinking through this`, without using a mode selector UI.

These modes produce Class A outputs and do not require governance ceremony.

The mode selector is available for clarity but is not required.

The mode selector is mandatory before the LLM produces Recommendations, Approval Request Packages, or Intake classifications.

---

## What Constitutes Explicit Framing

Explicit framing is an operator instruction that:
- names the interaction mode or type of work being requested
- is unambiguous about whether record creation, workflow advancement, or approval-path preparation is intended
- is stated directly, not implied by conversation topic or enthusiasm

### Explicit framing — examples
- "Process this as an intake"
- "Package a recommendation for this initiative"
- "I'm brainstorming — don't create records"
- "Prepare the approval request for the handoff"
- "Review the current decision context"
- "Review this finding from V Forge"

### Not explicit framing — examples
- "What do you think about this?" → Brainstorm is the safe default; no typed output requiring framing
- "Should we do this?" → May produce a Review Summary; must not produce a Recommendation without framing
- "That sounds right" → Not framing for any output type
- "Let's move forward" → Not an instruction to produce any typed output; not approval for any action
- "Yeah, go ahead" → Not framing, not approval, not activation

### When framing is absent

When the operator's input does not constitute explicit framing for a typed output, the LLM may:
- respond with a read-only interpretation or Review Summary if the question is clearly analytical
- ask a brief framing question to clarify what kind of work is needed
- produce a Continuity Reminder if relevant prior context is being neglected

The LLM must not:
- auto-classify the input into an intake and begin producing a Recommendation
- produce an Approval Request Package on the assumption that the operator `meant to` prepare one
- advance from conversational exchange into a typed activation path without explicit framing

The desktop application may present a brief mode selector to the operator if input is ambiguous rather than requiring the LLM to guess.

---

## Output Presentation Model

Each typed output must be presented distinctly. The operator must be able to identify immediately what type of output they are looking at, what it means, and what it does not mean.

### Finding

Visual treatment: labeled `FINDING`. System attribution shown, such as `V FORGE`, `VEDA`, or `PROJECT V`, depending on source. Freshness timestamp shown where relevant.

What it is: a bounded report of something observed, detected, or analyzed.
What it is not: a recommendation, a decision, or replanning authority.

Required elements shown:
- output type label: `FINDING`
- source system attribution
- what was found
- why it matters
- what has NOT been done as a result of this finding
- what the operator may do next, such as route to governed path or dismiss

### Recommendation

Visual treatment: labeled `RECOMMENDATION`. Clearly marked as pending operator review. Not approved, not activated.

What it is: a bounded proposed course of action for operator review.
What it is not: a decision, an approval, or a record mutation.

Required elements shown:
- output type label: `RECOMMENDATION — awaiting review`
- producer attribution, agent and current system context
- proposed path
- bounded scope
- basis, including evidence and decision references
- uncertainty and risk
- governance posture, including action class and what gate applies
- if approved: what happens
- if not approved: what the default state is

The recommendation widget must show the action class badge, such as `Class B` or `Class C`, inline on the output card so the operator cannot mistake a governance-sensitive recommendation for a Class A interpretation.

### Review Summary

Visual treatment: labeled `REVIEW SUMMARY`. No action badge.

What it is: a read-only analysis of records, context, or packages.
What it is not: a proposed action, a recommendation, or a decision.

No approval gate widget accompanies a Review Summary. If the operator wants to proceed to action after reviewing, they must request a Recommendation or Approval Request Package through explicit framing.

### Approval Request Package

Visual treatment: labeled `APPROVAL REQUEST`. Includes action class badge. Includes a `[Proceed to Approval Gate]` action.

What it is: a structured package requesting explicit operator approval for a specific Class B or Class C action.
What it is not: an approval. Producing this package does not satisfy any gate.

This output lives in the right interaction panel. It is the entry point into the center workspace review-and-gate flow. The approval event does not happen here. The operator uses this output card to navigate to the center review surface, complete their review, and then reach the gate widget.

Required elements shown:
- output type label: `APPROVAL REQUEST — [Class B / Class C]`
- action being requested, specific and not vague
- scope the approval would cover
- basis for the request
- what approval covers and does not cover
- what happens if approval is granted
- what the default state is if approval is not granted
- a `[Proceed to Approval Gate]` action that navigates the operator to the governed approval gate widget in the relevant center review surface; this action opens the center surface, it does not open a gate in the interaction panel

### Execution Report

Visual treatment: labeled `EXECUTION REPORT` with `V FORGE` system attribution. Not colored as requiring action unless a return trigger is embedded.

What it is: a bounded account of execution state, findings, or completion.
What it is not: a planning decision, a replanning authorization, or a signal transfer.

If the report contains a return trigger, that trigger is shown separately and distinctly within the output card with a `RETURN TRIGGER` label, making clear that the trigger is a finding that may warrant routing to planning, not an automatic replanning event.

### Uncertainty Notice

Visual treatment: labeled `UNCERTAINTY` with warning treatment. Shown prominently, not buried in paragraph text.

What it is: an explicit notice that the LLM's current basis is insufficient, stale, conflicting, or unclear for the current output or action.
What it is not: a failure. Uncertainty notices are correct behavior.

Must show:
- what is uncertain
- what specific context or evidence would resolve it
- what outputs or actions this uncertainty affects

### Continuity Reminder

Visual treatment: labeled `CONTINUITY REMINDER`. Not requiring immediate action.

What it is: a reference to prior governing decisions, prior rejections, prior workflow states, or admitted continuity artifacts relevant to what the operator is currently doing.
What it is not: a recommendation or a governance gate.

If the operator is proceeding toward an action that conflicts with a prior governing decision, a Continuity Reminder should appear before the LLM produces any recommendation in that direction. The reminder is not a block — it is a visible signal that prior context exists and is relevant.

---

## Orchestration and Delegated Work During Interaction

When orchestration is active, the interaction model must make that visible without turning the session into a control-room circus.

### What the operator must be able to tell

When meaningful delegated work is in progress, the operator must be able to see:
- that orchestration is active
- what subtask is being worked
- what specialist role is active
- whether the subtask is pending, running, completed, failed, cancelled, or awaiting review
- whether the delegated output is now contributing to the current interaction

### What delegated outputs must look like

Delegated outputs must remain visibly bounded and non-authoritative.
A specialist result must not appear as though it were a privileged or already-approved answer.

Delegated outputs should carry:
- role or source attribution
- bounded scope description
- lifecycle result state
- a reminder that delegated work did not change governance posture

### Interaction rule

The operator must never be forced to guess whether an answer was produced directly, derived from delegated work, or shaped by orchestration state.

---

## Continuity-Aware Interaction Rule

When continuity artifacts materially affect the session, the operator must encounter them explicitly enough to remain accountable.

This does not mean flooding every response with memory noise.
It means the operator must be able to see, where relevant:
- that a continuity artifact is active
- what type of continuity artifact it is
- whether it is aging or stale
- that it is non-canonical
- that it can be reviewed or cleared

The interaction surface must not let continuity artifacts masquerade as freshly loaded governed state.

---

## Operator Response Options

For every LLM output, the operator has a defined set of response options. These are the only recognized interaction outcomes. Conversational statements in the interaction surface do not constitute any of these responses.

### For Finding
- **Route to governed path** — sends the finding to the appropriate interface, such as return-to-planning or escalation
- **Dismiss** — closes the finding; logged as acknowledged-and-dismissed
- **Ask for clarification** — requests the LLM to expand or clarify specific elements of the finding
- **Defer** — marks the finding as deferred for later review; logged

### For Recommendation
- **Proceed to Approval Request** — requests the LLM to package an Approval Request Package from this recommendation; does not itself activate anything
- **Modify** — operator specifies changes to scope, basis, or proposed path; LLM produces an updated Recommendation
- **Reject** — operator dismisses the recommendation; logged as rejected with optional reason
- **Defer** — operator parks the recommendation for later; logged; recommendation shown as stale after threshold
- **Ask for clarification** — operator requests specific expansion without committing to a path

### For Review Summary
- **Ask for clarification** — requests expansion on specific elements
- **Request Recommendation** — explicit framing switch; operator instructs the LLM to produce a Recommendation based on the review
- **Dismiss** — closes the summary

### For Approval Request Package
- **Proceed to Approval Gate** — navigates to the Class B or Class C gate widget in the relevant center review surface; the approval event is persisted there, not in the interaction panel. The operator must be inside the center review surface and complete any required review before the gate widget is available. The Approval Request Package in the right panel is the route into that surface, not a substitute for it.
- **Reject** — governed rejection; logged with optional reason; rejection record persisted
- **Modify scope** — returns the package to the LLM for revision with stated changes; prior package is superseded
- **Defer** — parks the package; logged; marked stale after threshold
- **Ask for clarification** — requests expansion on specific elements before deciding

### For Execution Report
- **Acknowledge** — operator confirms they have read the report; logged
- **Route return trigger** — if a return trigger is present, routes it to the Project V planning surface through the governed return-to-planning interface
- **Dismiss return trigger** — operator dismisses the trigger with explicit acknowledgment that they accept execution risk; logged
- **Request review summary** — asks the LLM to produce a Review Summary interpreting the report in planning context

### For Uncertainty Notice
- **Load missing context** — operator loads the missing evidence, decision, or workflow state that the LLM flagged
- **Proceed without resolving** — operator acknowledges the uncertainty and proceeds; logged as proceeding under acknowledged uncertainty
- **Ask for clarification** — requests the LLM to specify more precisely what is uncertain

### For Continuity Reminder
- **Acknowledge** — operator has seen the reminder and will account for it
- **Review referenced context** — navigates to the referenced decision or prior finding
- **Dismiss** — closes the reminder; logged

---

## What the Interaction Model Must Never Permit

### The LLM becoming the workflow driver
The LLM must not auto-advance interaction from ambient conversation to typed output to activation path without explicit framing at each step. A strong recommendation that the operator seems to agree with does not advance to an Approval Request Package unless the operator explicitly requests it. An Approval Request Package that the operator seems to favor does not advance to the approval gate unless the operator explicitly initiates it.

### Conversational statements being treated as responses
Chat phrases like `that works`, `sounds right`, `sure`, and `go ahead` are not recognized response options for any typed output. The desktop application must not attach governance significance to these phrases. The operator must use the defined response options for governance-relevant outputs.

### A Recommendation being mistaken for a decision
The Recommendation widget must visually and semantically distinguish itself from an activated action. Its label must say `awaiting review` or equivalent. It must not read like a confirmation.

### A Finding being mistaken for planning authority
A V Forge Finding routed into a Project V session must not read as though Project V has already decided to replan. The Finding states what execution observed. It does not state what planning should do.

### Model quality changing the interaction contract
A more capable model's Recommendation must present identically in governance terms to a less capable model's Recommendation. The action class badge, the inertness label, the approval gate requirement — none of these should differ based on which model produced the output.

### Chat history becoming effective governance state
The operator must not be able to point at a conversation thread and say `we decided this in chat.` Governance state lives in persisted records. The interaction model must make it structurally impossible for chat exchange to substitute for governed approval events, decision records, or persisted rejection records.

### Delegated work becoming hidden authority
A specialist result must not look like a privileged answer merely because it came from internal orchestration. Runtime specialization does not create governance weight.

### Continuity artifacts becoming silent persuasion
Memory, transcript-derived continuity, and compaction products must not quietly shape high-impact operator choices without being inspectable and clearly non-canonical.

### The LLM referencing context it does not have loaded
When the LLM cites a governing decision, evidence record, workflow state, or active continuity artifact, the operator must be able to verify that it is loaded in the current visible session basis. If the operator cannot verify the context reference, the LLM must be treated as reasoning from unknown basis.

---

## Visibility at the Moment of Interaction

Before the LLM produces any non-trivial typed output, the following must be visible:

- **Current system** — shown in top-level status; the operator knows which system the LLM is operating within
- **Current workflow stage** — shown in status/context surfaces; the operator knows what stage is active and what gates are next
- **Output type** — every typed output is labeled with its type before the content is read
- **Evidence basis** — shown in context strip with freshness and trust posture
- **Uncertainty** — any Uncertainty Notice must appear before or alongside the outputs it qualifies
- **What has not happened yet** — the inertness of recommendations, packages, findings, and delegated outputs must be stated on the output card itself, not only in governance documentation
- **What still requires operator action** — the response options at the bottom of each typed output card must make clear what the operator needs to do to proceed
- **Whether orchestration is materially involved** — if the answer was shaped by delegated runtime work, that must be visible
- **Whether continuity artifacts are materially involved** — if continuity artifacts are participating in the current basis, that must remain inspectable

---

## Keeping the Interaction Explicit Without Making It Miserable

The interaction model is explicit. It is not exhausting. These two things are compatible.

Class A interpretations, review summaries, continuity reminders, and uncertainty notices require no governance ceremony. The operator asks, the LLM responds, the operator reads. No mode selection required for pure analytical exchange.

Mode selection is only required when the operator wants typed outputs that have governance significance: Recommendations, Approval Request Packages, Intake classifications. These are the cases where framing matters because the output type and governance posture change.

For low-stakes analytical work, the interaction should feel like using a knowledgeable assistant. For governance-sensitive work, the interaction should feel like using a governed system where both parties know exactly what is happening.

The desktop application must not impose ceremony on work that does not warrant it. It must impose structure on work that does. The mode system is the mechanism that distinguishes those cases — not by creating unnecessary friction, but by making the distinction explicit when it matters.

---

## Context Invalidation and Mid-Session State Changes

The interaction model does not operate in a static context. Governing decisions change, evidence goes stale, approvals complete, compaction events fire, return triggers arrive, and session tokens expire — sometimes while the operator is actively working and the LLM is mid-turn or between turns. This section defines what the interaction surface and the LLM must do when that happens.

For the complete trigger-to-consequence mapping, see `desktop-invalidation-and-refresh-matrix.md`. This section defines the interaction-layer behavioral rules that apply across all trigger types.

---

### When a Blocking Invalidation Event Fires Mid-Turn

A blocking invalidation event is one that requires acknowledgment or reload before further governance-sensitive outputs are produced. See `desktop-invalidation-and-refresh-matrix.md` for the full list and their blocking posture.

If a blocking event fires while an LLM turn is in progress:

- The turn completes normally. Generation is not interrupted.
- The output is marked stale before it is rendered in the panel: `⚠ CONTEXT CHANGED — this output was produced while a context change was in progress. Review before acting.`
- The blocking posture takes effect before the next turn begins.
- The operator sees both the completed output and its staleness marker.

The LLM must not be expected to detect a mid-turn context change from within the turn. The desktop application is responsible for applying the staleness marker on completion. The LLM is responsible for honoring the blocking posture on the next turn.

---

### When a Blocking Invalidation Event Fires Between Turns

If a blocking event fires after a turn completes but before the next turn begins:

- The desktop application applies the required consequences to the affected state categories and surfaces before the next interaction is enabled.
- The interaction panel shows the event notification appropriate to its importance: inline banner for non-blocking events, modal for blocking events.
- The LLM's next turn must begin with the updated context. The interaction surface must not present a new input field until the required acknowledgment or reload has occurred for blocking events.
- If the operator attempts to send input before acknowledging a blocking event, the input is held pending acknowledgment.

---

### LLM Behavior After a Context Change

On the turn following a context change — whether notified via a context strip update, an output card staleness marker, or an explicit panel banner — the LLM must:

**If the changed context is now loaded and current:**
- Operate from the updated context without referencing the prior state as still applicable.
- Acknowledge the change if the operator's framing references the prior state: `Note: [decision/evidence/stage] has changed since my prior output. My current response reflects the updated context.`

**If the changed context is unavailable or pending reload:**
- Produce an Uncertainty Notice before producing any output that would depend on the missing context.
- State specifically what context is missing and what outputs or actions are affected.
- Do not proceed toward Class B or C outputs until the missing context is loaded.

**If prior rendered outputs in the panel are now stale due to the change:**
- The LLM must not reference those prior outputs as a valid basis for new outputs.
- If the operator asks the LLM to build on a stale output, the LLM must first acknowledge the staleness and clarify what has changed before proceeding.

---

### Output Card Staleness Markers

Rendered output cards in the interaction panel can receive staleness markers as a result of context change events. The following marker types apply:

**`⚠ CONTEXT CHANGED — produced during context change`**
Applied when a blocking event fired during the turn that produced the output.

**`⚠ DECISION SUPERSEDED — [dec-id] replaced by [dec-id-new]`**
Applied when a governing decision cited in the output has been superseded or invalidated.

**`⚠ EVIDENCE STALE — [obs-id] is now stale`**
Applied when evidence cited in the output has exceeded its validity window or been contradicted by newer evidence.

**`⚠ BASIS CHANGED — prior approval invalidated`**
Applied when a prior approval that the output assumed was valid has been invalidated.

**`⚠ SYSTEM CHANGED — produced under [prior system] posture`**
Applied when the current system has changed since the output was produced.

**`⚠ CONTINUITY ARTIFACT CHANGED — [artifact] no longer in active basis`**
Applied when a continuity artifact cited in the output has expired or been removed from the session basis.

**`⚠ COMPACTION BOUNDARY — produced before this compaction cycle`**
Applied to all output cards above a compaction boundary marker.

Staleness markers are applied by the desktop application, not by the LLM. They are not deleted. They remain on the card until the operator dismisses the card or re-requests a fresh output. The operator's ability to see what was produced and when, and under what context, is a governance record — it must not be silently cleaned up.

---

### Session Error Posture

When the session token expires or runtime scope is broken:

- The interaction panel input is disabled immediately.
- The current panel shows: `Session interrupted. Re-initialize to continue.`
- Any turn in progress at the moment of expiry is marked incomplete on completion: `⚠ SESSION INTERRUPTED — this output was produced while the session was in an error state. Do not use for governance decisions.`
- No further LLM outputs are enabled until re-initialization completes.
- On re-initialization, all context categories are reloaded fresh. The prior session's in-memory state is not restored as current context.
- The LLM must not reference prior session context as loaded or current after re-initialization until it has been explicitly reloaded and is visible in the context strip.

---

## Human-In-The-Loop Principle

Human-in-the-loop control is preserved by the interaction model because the model keeps the human's role explicit at every step. The operator frames, reviews, and approves. The LLM produces typed outputs. Neither role substitutes for the other.

Over-deference to a capable LLM is a real failure mode. An operator who reads a confident Recommendation and clicks without meaningful evaluation has become a pass-through. The interaction model resists this by:
- requiring explicit framing before typed outputs with governance significance are produced
- making inertness visible on every output card
- requiring specific response options rather than ambient agreement
- logging dismissals, deferrals, and acknowledged uncertainties so the audit trail reflects what the operator actually did
- keeping orchestration and continuity visible enough that the operator is reviewing the real session basis, not a cleaned-up illusion

The operator's role is not to be impressed by good outputs. It is to evaluate them and act as the accountable party.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- typed outputs are produced in response to explicit framing, not ambient conversation
- output type must be labeled on every output; the LLM must not produce ambiguous outputs that the operator might mistake for a different type
- a Recommendation's quality does not change its governance status — it is inert until the operator activates it through the governed gate
- a Finding does not constitute planning authority — it reports what was observed
- an Approval Request Package is the most complete pre-approval artifact the LLM may produce — it still does not activate anything
- delegated outputs remain inert and bounded
- continuity artifacts are useful but non-authoritative and must remain inspectable
- conversation smoothness must not hide what context was used, what typed output was produced, or what the operator still needs to do
- if the operator's input is not explicit framing for a typed output with governance significance, the safe response is analytical, not activist

If the LLM treats operator enthusiasm or conversational agreement as framing, produces Recommendations without explicit framing, hides orchestration participation, or treats its own output as a step in the activation path rather than an input to operator review, this interaction model is being violated.

---

## Usage

This document should be used:

- when designing the LLM interaction surface within the desktop application
- when evaluating whether a proposed interaction pattern preserves the distinction between framing, output, review, and approval
- when reviewing whether the operator's response options for a given output type are complete and correctly bounded
- when auditing desktop sessions for interaction drift, including LLM auto-advancing, operator rubber-stamping, chat-as-governance, hidden orchestration, and hidden continuity
- when writing more specific operator workflow docs or LLM prompt guidance that must remain consistent with this interaction model

---

## Related Docs

- `desktop-llm-behavior-contract.md`
- `desktop-governance-and-gating-model.md`
- `desktop-state-and-context-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-memory-and-continuity-model.md` or successor naming
- `desktop-system-init-and-tool-surface-model.md` or successor naming
- `desktop-surface-architecture.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/recommendation-packaging-doctrine.md`
- `../governance/report-structure-and-required-fields.md`
- `../governance/decision-continuity-doctrine.md`
- `operator-surface-interfaces.md`
- `mcp-coordination-model.md`
- `../workflows/handoff-workflow.md`
- `../workflows/launch-readiness-workflow.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../ecosystem/decisions/ADR-011-tauri-2-desktop-is-the-operator-host.md`
- `desktop-invalidation-and-refresh-matrix.md`
