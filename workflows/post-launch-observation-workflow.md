# Post-Launch Observation Workflow

## Purpose

This document defines the governed cross-system workflow by which the V Ecosystem
observes, classifies, and responds to post-launch reality.

It exists to answer:

```text
How does post-launch observation start, what does each system do, when is signal
actionable vs immature vs noise, when does the workflow cycle back into observation,
and when does it route into maintenance, return-to-planning, or escalation?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the concrete stage sequence from post-launch entry through observatory
  activation, signal capture, classification, reconsideration assessment,
  and governed outcome routing
- entry conditions and repeat-cycle posture
- what constitutes actionable signal vs immature signal vs noise
- transition triggers for continue-observation, maintenance, return-to-planning,
  and escalation outcomes
- degraded-mode and interruption handling
- activity-trail obligations for governed observation events
- re-entry after a maintenance or replanning cycle

---

## Out of Scope

This document does not define:

- the VEDA → Project V or VEDA → V Forge signal interface data contracts — those
  belong in `interfaces/veda-to-project-v-signal-interface.md` and
  `interfaces/veda-to-v-forge-signal-interface.md`
- the maintenance and replanning workflow stages — those belong in
  `workflows/maintenance-and-replanning-workflow.md`
- detailed VEDA provider or ingest mechanics for specific signal sources
- post-launch campaign, paid media, or distribution management
- project intake for new opportunities discovered during post-launch observation —
  that is a separate intake workflow trigger, not part of this workflow

---

## System

- workflows

---

## Relationship to Governing Docs

- `workflows/launch-readiness-workflow.md` — this workflow begins from Stage 11
  (post-launch state) of the launch-readiness workflow.
- `workflows/maintenance-and-replanning-workflow.md` — when this workflow routes
  to return-to-planning, it enters that workflow at its entry condition. This
  workflow ends at the handoff point; maintenance and replanning sequencing is
  governed separately.
- `interfaces/veda-to-project-v-signal-interface.md` — signal delivery to Project V
  at Stages 3 and 5 of this workflow follows this interface's delivery and receipt model.
- `ecosystem/activity-trail-integration-map.md` — canonical action type mapping for
  signal delivery events referenced in this workflow's activity trail section.

---

## Core Rule

VEDA observes and records. Project V and V Forge classify and interpret.
Classification does not equal action authorization.

Three phases are distinct and must not be conflated:
- **Observation** — VEDA captures what the external world is doing relative to
  the launched scope
- **Classification** — Project V and V Forge interpret what the signal means in
  planning and execution terms
- **Action routing** — the ecosystem activates the correct governed path based
  on classification

Signal does not authorize action. Classification does not authorize action.
A governed path activation is required before any replanning, maintenance, or
escalation begins.

---

## Entry Conditions

### Primary entry

This workflow begins from Stage 11 (post-launch state) of
`workflows/launch-readiness-workflow.md`. That state requires:

- V Forge has completed launch-sensitive execution within the confirmed scope
- V Forge execution truth includes the launched scope
- VEDA's observatory role has resumed for the launched scope
- Project V retains planning truth for the launched work
- no active replanning or mid-launch interruption has returned the ecosystem
  to the maintenance and replanning workflow

### Re-entry after a maintenance or replanning cycle

This workflow may be re-entered after a governed maintenance or replanning cycle
has completed and the launched scope has returned to a stable observed state:
- governed replanning or maintenance has concluded
- execution (if any) has completed within the revised scope
- VEDA's observatory role is active for the (potentially revised) launched scope

Re-entry begins at Stage 2 (signal capture) rather than Stage 1 (observatory scope
activation) if VEDA's observatory scope is already established for the scope.

---

## Workflow Stages

### Stage 1 — Observatory Scope Activation

**Entry event:** Post-launch state established; VEDA activates or confirms its
observatory scope for the launched project.

**What happens:**
VEDA establishes or confirms what it is watching for the live scope:
- search performance signals for the launched content
- indexation and crawl state from Search Console
- keyword ranking behavior relevant to the launched scope
- traffic and engagement signals from GA4
- SERP volatility or intent drift for the target topic cluster
- any platform signals relevant to the launched scope

The operator or Project V may direct VEDA to prioritize specific signal types or
monitoring targets within governed observatory scope bounds.

**Exit condition → Stage 2:** Observatory scope is active; initial signal capture
can begin.
**Exit condition → Stage 6 (degraded):** Observatory scope cannot be established
for part or all of the launched scope — missing coverage gap must be surfaced.

**Boundary rule:** Observatory scope activation does not give VEDA planning
authority. VEDA establishes what to watch. It does not determine what the
observations mean or what to do next.

---

### Stage 2 — Signal Capture

**Entry event:** Stage 1 complete (or re-entry from a completed maintenance /
replanning cycle with observatory scope already active).

**What happens:**
VEDA captures post-launch signal for the launched scope and packages it for
ecosystem consumption through the governed signal interfaces:
- initial indexation signals — whether launched content is being found and crawled
- early search performance signals — impressions, clicks, position where meaningful
- traffic behavior from GA4 where applicable
- SERP context for the target topic cluster

The initial post-launch capture window is the period shortly after launch where
indexation state, crawl behavior, and early performance signals provide the first
honest read on launch health. This window is signal-type dependent — search
performance signals typically require weeks to stabilize to a reliably interpretable
state.

Ongoing: after the initial window, signal capture continues at governed intervals.

**Exit condition → Stage 3:** A signal delivery package has been produced and is
available for classification.
**Exit condition → Stage 6 (degraded):** Signal is too immature to classify
meaningfully (see Signal Patience rule below); capture continues until the maturity
threshold is met.

**Boundary rule:** Captured signal is VEDA-owned evidence. It is not yet an
interpretation or a finding. Low initial signal does not automatically mean the
launch failed. Strong initial signal does not automatically confirm long-term success.

---

### Stage 3 — Signal Delivery to Project V and V Forge

**Entry event:** Signal package ready for delivery.

**What happens:**
VEDA delivers bounded signal packages to Project V and V Forge through the
governed signal interfaces:
- `interfaces/veda-to-project-v-signal-interface.md` — push delivery to Project V
  with receipt confirmation
- `interfaces/veda-to-v-forge-signal-interface.md` — push delivery of relevant
  execution-intelligence signal to V Forge (startup/initialization layer where
  applicable; ongoing signal feeds the V Forge active-query layer via
  `interfaces/v-forge-evidence-access-contract.md`)

Both deliveries follow their respective interface contract models (AD-01 / AD-02
layered model for V Forge).

**Activity trail:** `signal.delivery.confirmed` records produced by the receiving
systems on receipt, per `ecosystem/activity-trail-integration-map.md` Section 1 and
Section 4.

**Exit condition → Stage 4:** Signal delivered and receipt confirmed; classification
can begin.
**Exit condition → Stage 6 (degraded):** Delivery failure, package validity failure,
or freshness/provenance concerns — per the degraded-mode handling in each interface contract.

---

### Stage 4 — Classification and Interpretation

**Entry event:** Signal received at Stage 3.

**What happens:**
Project V and V Forge independently classify what the signal means:

**Project V classifies for planning implications:**
- does the signal confirm, question, or contradict the planning basis?
- does the signal suggest a trend that would affect readiness for follow-on work?
- is the signal strong and reliable enough to support a reconsideration conclusion?
- does the signal require more observation time before it can be meaningfully
  interpreted (signal maturity assessment)?

**V Forge classifies for execution implications:**
- does the signal indicate an execution-side condition requiring attention?
- are there findings that affect ongoing V Forge execution within scope?
- does the signal suggest a condition that V Forge can address within existing scope
  (maintenance candidate) or one that requires planning reconsideration (return-to-planning candidate)?

**Signal maturity assessment:** At this stage, if the signal has not yet matured to a
reliably interpretable state — because insufficient time has passed since launch for
the signal type — the classification outcome is "continue observation" and the workflow
cycles back to Stage 2. Acting on pre-maturity signal produces governance noise.

**Exit condition → Stage 5:** Classification complete; either a potential action
trigger has been identified or classification concludes the signal does not yet meet
the action threshold.
**Exit condition → Stage 2 (continue-observation cycle):** Signal is immature; return
to capture and wait for maturity window.
**Exit condition → Stage 6 (degraded):** Signal is contradictory, low-trust, or
provenance is insufficient to classify reliably.

**Boundary rule:** Classification is not replanning. Classifying that a signal
looks concerning is not authorization to replan. Classification produces a bounded
interpretation that feeds Stage 5 assessment.

---

### Stage 5 — Reconsideration Assessment

**Entry event:** Stage 4 classification complete; a potential action trigger
identified or a structured review interval has been reached.

**What happens:**
Project V and V Forge conduct a structured assessment of whether the classified
signal meets the threshold to activate a governed action path.

Assessment criteria:
- Is the signal material — strong enough, consistent enough, and from a sufficiently
  trustworthy source to support a reconsideration conclusion?
- Is the signal within the expected range of post-launch variation for this signal
  type and maturity window? (If yes → continue observation)
- Is the finding addressable within existing approved scope by V Forge, without
  changing the planning basis? (If yes → maintenance candidate)
- Does the finding materially affect the planning basis — blocking execution,
  invalidating assumptions, or requiring Project V reconsideration? (If yes →
  return-to-planning candidate)
- Is the signal significant enough or uncertain enough that classification cannot
  be safely resolved without human review? (If yes → escalation candidate)

The assessment must produce one of the four outcomes in the Outcome Routing section.

**Threshold guidance:**
- A single data point rarely meets the material signal threshold
- A sustained trend across multiple capture cycles may
- Noise accumulation alone does not cross the threshold — volume is not materiality
- When the boundary between noise and material signal is genuinely uncertain,
  escalation is the correct outcome, not a forced classification

**Exit condition → Stage 6a (continue-observation):** No action threshold met;
cycle continues.
**Exit condition → Stage 6b (maintenance):** Finding addressable within existing scope.
**Exit condition → Stage 6c (return-to-planning):** Finding affects planning basis.
**Exit condition → Stage 6d (escalation):** Signal is governance-sensitive, ambiguous,
or significant enough to require human review.
**Exit condition → Stage 6 (degraded):** Assessment cannot be completed due to
signal quality issues.

**Boundary rule:** The assessment determines which governed path is appropriate.
It does not itself constitute a replanning decision, a maintenance authorization,
or an execution instruction. Each path activation follows its own governed workflow.

---

### Stage 6a — Continue Observation (Repeat Cycle)

**Entry event:** Stage 5 assessment concludes no action threshold is met.

**What happens:**
The assessment outcome is recorded. The current interpretation of post-launch signal
is preserved. The workflow cycles back into ongoing observation.

**Repeat cycle:** Return to Stage 2 (signal capture). The next capture / delivery /
classification / assessment cycle runs at the next governed interval, or is triggered
earlier if a materially significant signal event occurs.

**Governed intervals:** The cadence for repeat cycles should be defined per launched
scope based on signal type maturity windows and observatory configuration. A defined
interval prevents the observation phase from becoming either a background noise
accumulator or an ad hoc event-triggered-only loop.

**Activity trail:** The classification outcome must be durably recorded using the
`observation.classify` action type per `ecosystem/activity-trail-integration-map.md`
Section 10. This prevents classification history from existing only in session memory.

---

### Stage 6b — Maintenance Activation

**Entry event:** Stage 5 assessment concludes a finding is addressable within existing
approved scope without changing the planning basis.

**What happens:**
Maintenance work proceeds within the existing approved handoff scope per the
maintenance activity model in `workflows/maintenance-and-replanning-workflow.md`.

This is maintenance — not replanning. No return-to-planning event is triggered.
No new handoff is required unless the maintenance work subsequently reveals a
finding that does require planning reconsideration.

**Exit condition:** Maintenance work completes. The workflow re-enters at Stage 2
(signal capture) to resume the observation cycle for the maintained scope.

**Boundary rule:** Maintenance within approved scope does not require re-entering
the handoff workflow or the replanning workflow. If maintenance work produces findings
that change the planning basis, those route to Stage 6c (return-to-planning) from
within the maintenance cycle.

---

### Stage 6c — Return-to-Planning Activation

**Entry event:** Stage 5 assessment concludes a finding materially affects the
planning basis.

**What happens:**
V Forge surfaces the relevant execution findings through the governed return-to-planning
interface (`interfaces/v-forge-to-project-v-return-to-planning-interface.md`). The
return-to-planning / replanning workflow begins at its entry condition in
`workflows/maintenance-and-replanning-workflow.md`.

**Activity trail:** `execution.return` record produced by V Forge on delivery;
`execution.return.confirmed` record produced by Project V on receipt, per
`ecosystem/activity-trail-integration-map.md` Section 3.

**Exit condition:** The replanning cycle completes and the launched scope returns to
a stable observed state. The post-launch observation workflow re-enters at Stage 2
(or Stage 1 if the replanning cycle changed the observatory scope).

**Boundary rule:** Activating return-to-planning does not skip the maintenance and
replanning workflow. The full return-to-planning / replanning stage sequence applies.

---

### Stage 6d — Escalation

**Entry event:** Stage 5 assessment concludes the signal is governance-sensitive,
ambiguous, or significant enough to require human review before the correct path
can be determined.

**What happens:**
The situation is surfaced through the governed escalation path per
`governance/approval-and-escalation-model.md`. No action path is activated before
the escalation resolves. The observation phase pauses for the affected scope.

**Exit condition:** Escalation resolves with a governed outcome. The workflow routes
to the appropriate outcome stage (6a, 6b, or 6c) based on the escalation resolution.

---

### Stage 6 — Degraded / Insufficient Signal

**Entry event:** Signal too immature at Stage 2; contradictory or low-trust signal
at Stage 4; signal quality prevents assessment completion at Stage 5; or observatory
coverage gap at Stage 1.

**What happens:**
The specific degraded condition is identified and handled:

| Condition | Handling |
|---|---|
| Signal too immature (pre-maturity window) | Continue observation; cycle back to Stage 2; do not classify or assess |
| Contradictory signal | Surface contradiction explicitly; route to escalation (6d) or await additional capture cycles |
| Low-trust / low-provenance signal | Do not produce an assessment on low-trust signal; flag in trail; await higher-trust capture |
| Observatory coverage gap | Surface the gap; operator may direct VEDA to expand scope; do not treat missing coverage as clean signal |
| Material post-launch failure | Do not treat as noise; route directly to return-to-planning (6c) or escalation (6d) with urgency |
| Repeated noise without threshold met | Preserve noise history but do not elevate to material signal through volume; continue observation |

**Exit condition:** Specific degraded condition resolves (route to appropriate stage)
or is durably recorded and the observation cycle continues.

**Boundary rule:** A degraded observation must not be resolved by forcing a
classification on insufficient signal. Preserving an honest inconclusive state
is better governance than a false assessment.

---

## Transition Summary Table

| From | Event | To |
|---|---|---|
| Post-launch state (launch-readiness Stage 11) | — | Stage 1 |
| Re-entry after maintenance / replanning cycle | Observatory scope active | Stage 2 |
| Stage 1 | Observatory scope active | Stage 2 |
| Stage 1 | Coverage gap | Stage 6 (degraded) |
| Stage 2 | Signal package ready | Stage 3 |
| Stage 2 | Signal too immature | Stage 6 (degraded / wait) |
| Stage 3 | Delivery confirmed | Stage 4 |
| Stage 3 | Delivery failure / validity failure | Stage 6 (degraded) |
| Stage 4 | Classification complete | Stage 5 |
| Stage 4 | Signal immature; not classifiable | Stage 2 (continue-observation cycle) |
| Stage 4 | Contradictory / low-trust signal | Stage 6 (degraded) |
| Stage 5 | No action threshold met | Stage 6a (continue observation) |
| Stage 5 | Finding addressable within scope | Stage 6b (maintenance) |
| Stage 5 | Finding affects planning basis | Stage 6c (return-to-planning) |
| Stage 5 | Governance-sensitive / ambiguous | Stage 6d (escalation) |
| Stage 5 | Assessment cannot complete | Stage 6 (degraded) |
| Stage 6a | — | Stage 2 (next cycle) |
| Stage 6b | Maintenance complete | Stage 2 (resume observation) |
| Stage 6c | Replanning cycle complete; scope stable | Stage 1 or Stage 2 |
| Stage 6d | Escalation resolved | Stage 6a, 6b, or 6c |
| Stage 6 (degraded) | Condition resolved | Appropriate stage |

---

## Outcome Routing

### Continue Observation (→ Stage 6a)

Use when: Current signal does not meet the material action threshold — it is either
within expected post-launch variation, too immature to classify, or is noise without
a sustained trend.

The assessment is recorded. Observation continues. The next cycle begins at Stage 2.

### Maintenance (→ Stage 6b)

Use when: A finding is real but addressable within the existing approved execution
scope without changing the planning basis.

V Forge addresses the finding within scope. Observation continues after maintenance
completes. Does not require return-to-planning or a new handoff.

If maintenance work subsequently produces findings that do affect the planning basis,
those escalate to return-to-planning from within the maintenance cycle.

### Return-to-Planning (→ Stage 6c)

Use when: A finding materially affects the planning basis — blocking execution,
invalidating assumptions underpinning the launched scope, or requiring Project V
to reconsider direction.

V Forge surfaces findings through `interfaces/v-forge-to-project-v-return-to-planning-interface.md`.
The full maintenance and replanning workflow applies.

The post-launch observation workflow resumes after the replanning cycle concludes.

### Escalation (→ Stage 6d)

Use when: The signal is significant enough, ambiguous enough, or governance-sensitive
enough that the correct path cannot be safely determined without human review.

No action path is activated before escalation resolves. The observation phase pauses
for the affected scope while escalation is active.

### Distinguishing Maintenance from Return-to-Planning

The distinction matters and must be explicit at Stage 5:

| Maintenance | Return-to-planning |
|---|---|
| Finding addressable within existing approved scope | Finding requires changing what the planning basis approves |
| V Forge can resolve without Project V reconsideration | Project V must reconsider planning decisions |
| No new handoff required | May require a new or revised handoff |
| Planning basis remains valid | Planning basis is challenged or invalidated |

When uncertain, default to return-to-planning rather than treating an ambiguous
finding as maintenance-only. The cost of an unnecessary reconsideration assessment
is lower than the cost of executing on a changed reality without planning reconsideration.

---

## Signal Maturity Rule

Many post-launch signals require time to stabilize before they can be meaningfully
classified:

- Search performance signals (impressions, clicks, position) typically require
  weeks to reflect steady-state response to launched content
- Indexation and crawl state signals may stabilize in days; ranking signals take longer
- Traffic and engagement signals depend on content type and distribution context

The workflow must account for maturity windows at Stage 2 and Stage 4:
- if the signal type has not yet had sufficient time to mature, the Stage 4
  classification outcome must be "continue observation" regardless of current signal value
- early strong or weak signal does not override the maturity window
- acting on pre-maturity signal produces governance noise

**When signal has not matured:** return to Stage 2; do not classify; do not produce
an assessment. Record that the observation cycle ran and signal was immature.

---

## Noise vs Material Signal Rule

Not every post-launch fluctuation is actionable:

- **Material signal** — a trend, event, or pattern strong enough and consistent
  enough across multiple capture cycles to support a governed reconsideration conclusion
- **Noise** — natural variation in signal that does not reflect a meaningful change
  in external conditions

An observation is noise until there is enough evidence to classify it otherwise.
Noise must not be treated as a return-to-planning trigger.
Accumulating noise does not become material signal through volume alone.

When the boundary between noise and material signal is genuinely uncertain, escalation
(Stage 6d) is the correct governed outcome — not a forced classification.

---

## Observation Continuity Rule

Post-launch observations must be preserved so that later reconsideration,
review, and reconstruction are possible:

- observatory event records must remain traceable with provenance and timestamp
  even when they do not immediately trigger action
- signal assessed as "continue observation" must remain accessible as context
  when a later signal event triggers reconsideration
- assessment outcomes for each cycle must be recorded durably, not left only
  in session memory
- an observation that is inconclusive today may become part of the evidence
  basis for a governing decision six weeks later; its provenance must be preserved

See `governance/evidence-continuity-model.md`.

---

## Activity Trail Requirements

Activity trail coverage for post-launch observation events:

| Workflow event | Action type | Producing system |
|---|---|---|
| Signal delivery confirmed (Stage 3, Project V) | `signal.delivery.confirmed` | Project V |
| Signal delivery confirmed (Stage 3, V Forge) | `signal.delivery.confirmed` | V Forge |
| Classification produced (Stage 4) | `observation.classify` | Project V and/or V Forge |
| Assessment completed (Stage 5) | `observation.assess` | Project V |
| Observation cycle completed (Stage 6a) | `observation.cycle` | Project V |
| Return-to-planning delivery initiated (Stage 6c) | `execution.return` | V Forge |
| Return-to-planning receipt confirmed (Stage 6c) | `execution.return.confirmed` | Project V |
| Escalation initiated (Stage 6d) | `approval.escalate` | Project V |

Per `ecosystem/activity-trail-integration-map.md` Sections 1, 3, 4, and 10.

For the full field-level mapping detail for observation events — including required
entity references, minimum additional fields, and cycle identity guidance — see
integration map Section 10.

Activity records must be produced durably. An assessment that exists only in session
memory is not a governed record.

---

## Human-In-The-Loop Principle

Post-launch observation is governance-sensitive because its findings may affect
ongoing planning, execution scope, and resource allocation.

Human review may be required when:

- a signal event is significant enough to suggest a major replanning event is warranted
- the reconsideration assessment concludes that escalation (Stage 6d) is appropriate
- signal quality or trust posture is too uncertain to support a classification
  conclusion without human review
- a maintenance or return-to-planning activation involves significant scope or
  spend implications
- post-launch findings affect other projects in the portfolio

An agent may support signal classification and reconsideration assessment at Stages 4–5.
An agent must not self-authorize replanning, scope changes, or external action based
on post-launch signal alone.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- post-launch observation has eight distinct named stages with concrete transitions
- VEDA observes and records; Project V and V Forge classify and interpret; action
  requires a governed path activation — these three phases must not be conflated
- signal maturity must be assessed before classification; pre-maturity signal cycles
  back to Stage 2, not to assessment
- "continue observation" is a valid, governed, frequently correct outcome — not a
  failure or a stall
- noise accumulation alone does not become material signal
- each action route (maintenance, return-to-planning, escalation) activates its own
  governed workflow — this workflow ends at the handoff point
- project intake for new opportunities is a separate workflow, not part of this one
- activity trail records are required for governed events; observation cycle events
  use `observation.classify`, `observation.assess`, and `observation.cycle` canonical
  action types per integration map Section 10

If post-launch observation is implemented as a passive quiet period where signal
informally accumulates until someone decides to replan, or as a loop where any
signal triggers immediate action, the doctrine is wrong.

---

## Usage

This document should be used:

- when establishing the observatory scope for a newly launched project scope
- when implementing post-launch observation stage transitions and repeat cycles
- when evaluating whether classified signal meets the material action threshold
- when determining whether maintenance, return-to-planning, or escalation is
  the correct governed route
- when auditing whether observation cycle outcomes are durably recorded
- when distinguishing maintenance from return-to-planning for a given finding

---

## Related Docs

- `launch-readiness-workflow.md`
- `maintenance-and-replanning-workflow.md`
- `project-intake-workflow.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/v-forge-evidence-access-contract.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/evidence-continuity-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../ecosystem/activity-trail-model.md`
- `../ecosystem/activity-trail-integration-map.md`
- `../ecosystem/cross-system-boundaries.md`
- `../veda/veda.md`
- `../veda/system-invariants.md`
- `../project-v/project-v.md`
- `../v-forge/v-forge.md`
