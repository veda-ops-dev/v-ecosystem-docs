# V Forge Execution Intelligence Operations

## Purpose

This document defines how V Forge produces, maintains, and uses execution intelligence inside the V Ecosystem.

It exists to answer:

```text
How does V Forge derive execution intelligence from the content graph and bounded VEDA signal, how is that intelligence operated without absorbing signal ownership or planning ownership, and how should execution intelligence produce bounded execution-side outputs that remain honest, reviewable, and governance-safe?
```

This is a Tier 2 V Forge implementation-build-spec authority document.

---

## Scope

This document governs:

- the operational role of execution intelligence inside V Forge
- the inputs execution intelligence may consume
- the kinds of execution intelligence outputs V Forge may produce
- how execution intelligence relates to the content graph, VEDA signal, and execution work
- how execution intelligence findings remain bounded and non-authoritative
- when execution intelligence should stay execution-local and when it must return to planning
- anti-drift rules that keep execution intelligence from becoming shadow planning or shadow observability

---

## Out of Scope

This document does not define:

- the full schema for every execution intelligence artifact
- the raw observatory provider integrations owned by VEDA
- the full planning opportunity model owned by Project V
- experimentation or optimization doctrine
- future commercial/runtime intelligence layers

Those belong in VEDA docs, Project V docs, strategy docs, or later V Forge expansions.

---

## System

- v-forge

---

## Core Rule

Execution intelligence is the bounded analytical layer V Forge produces by crossing execution truth against bounded VEDA signal.

It exists to help V Forge understand how what was built is performing, where execution-side gaps exist, and what execution-local issues or planning-relevant findings should be surfaced.

Execution intelligence must not become:
- raw signal ownership
- open-ended market research
- a planning replacement
- an automatic mutation engine for content graph or planning state

If execution intelligence starts behaving like VEDA or Project V, it is wrong.

---

## Execution Intelligence Definition

Execution intelligence is the execution-side analysis created when V Forge compares what exists in the project’s execution truth against bounded external signal provided through governed VEDA interfaces.

At minimum, execution intelligence may consider:
- content graph structure
- release and publication continuity
- execution history
- bounded VEDA signal relevant to built assets
- bounded execution-local validation outcomes

Execution intelligence is not raw signal.
Execution intelligence is not planning intelligence.
It is the execution-layer interpretation of how built structure and owned execution surfaces are behaving relative to bounded observed signal.

---

## Ownership Principle

V Forge owns execution intelligence because V Forge owns the execution truth and content graph the analysis is about.

VEDA owns the raw signal and observatory truth used as bounded input.
Project V owns planning intelligence and planning interpretation about what should be pursued next.

This means:
- V Forge may derive execution intelligence from bounded VEDA signal
- V Forge must not claim ownership over the raw signal itself
- V Forge must not treat execution intelligence as planning truth
- execution intelligence outputs remain execution-side analytical products unless and until governed workflows elevate their findings appropriately

---

## Operational Goals

Execution intelligence operations should achieve all of the following:

1. help V Forge understand how built assets are performing structurally and operationally
2. expose execution-side gaps or mismatches honestly
3. support execution-local maintenance, correction, and bounded review
4. surface planning-relevant findings without mutating planning truth directly
5. preserve clean ownership boundaries between execution, planning, and observability

An execution intelligence operation that is analytically interesting but ownership-blurring is a bad operation.

---

## Allowed Inputs

Execution intelligence may consume only bounded inputs that are legitimate for execution-side analysis.

### 1. Content graph inputs
Examples:
- page inventory
- topic coverage as actually built
- entity coverage as actually built
- internal link structure
- archetype footprint
- schema usage footprint

### 2. Execution continuity inputs
Examples:
- release records
- publication continuity
- execution reports
- bounded findings
- maintenance history

### 3. Bounded VEDA signal inputs
Examples:
- keyword or SERP signal already governed through the VEDA-to-V Forge interface
- bounded search performance indicators
- bounded observatory evidence relevant to built assets

### 4. Execution-local validation inputs
Examples:
- release-local checks
- bounded execution-side validation outcomes
- owned-surface operational confirmations inside admitted scope

### Rule
Execution intelligence must not pull in unlimited external inputs merely because more data seems useful.
The input set must remain bounded and justified by execution purpose.

---

## Forbidden Input Patterns

Execution intelligence must not be built from:
- open-ended observatory crawling owned by V Forge
- raw provider ingestion that should belong to VEDA
- speculative planning ideas treated as execution facts
- cross-project graph or signal contamination
- unlimited archival signal hoarding inside V Forge for convenience

If the input pattern makes V Forge look like the observatory, the pattern is wrong.

---

## Primary Execution Intelligence Operations

Execution intelligence operations should be understood through bounded categories.

## 1. Graph-versus-signal comparison

This operation compares what the content graph says exists against bounded VEDA signal.

Examples:
- compare built topic coverage against relevant observed query space
- compare built page footprint against bounded signal clusters
- compare schema usage or structural patterns against observed execution-side outcomes

### Rule
The result is an execution intelligence view, not a planning decision.

---

## 2. Built-asset performance interpretation

This operation interprets how a built asset or asset group appears to be performing relative to bounded signal.

Examples:
- page cluster appears under-covered relative to observed signal pattern
- built asset exists but appears structurally weak in execution context
- released asset seems mismatched to observed execution-side opportunities

### Rule
Interpretation must remain bounded to execution-side meaning.
It must not silently become strategy ownership.

---

## 3. Execution-side gap detection

This operation identifies gaps between built structure and bounded observed signal that may matter for execution.

Examples:
- content graph lacks structural support for a topic area already partly in scope
- internal link support appears weak relative to current built footprint
- schema usage is missing where execution-local correction may matter

### Rule
A detected gap is a bounded analytical output.
It is not automatic authorization to build more assets or expand scope.

---

## 4. Execution-local maintenance insight

This operation identifies issues that may be resolved inside V Forge maintenance scope.

Examples:
- structural correction opportunity on already-built assets
- bounded refresh need on an owned asset already in maintenance scope
- release-follow-up correction inside admitted execution authority

### Rule
Only execution-local correction may remain local.
If the insight would widen scope or alter planning direction, it must not stay purely inside V Forge.

---

## 5. Return-worthy finding generation

This operation identifies execution intelligence findings that should be packaged for Project V reconsideration.

Examples:
- execution-side mismatch reveals a planning-level contradiction
- current built footprint exposes a materially different next-step problem than planning assumed
- execution-side outcomes suggest the planning basis of future work may need revision

### Rule
Return-worthy findings must flow through the governed return-to-planning path.
They do not mutate planning truth directly.

---

## Output Classes

Execution intelligence should produce bounded outputs, not vague analytical fog.

At minimum, output classes should include:
- execution-local observation
- execution-local maintenance candidate
- bounded execution-side gap
- bounded uncertainty notice
- return-to-planning candidate finding

Output classes should be explicit enough that operators and LLMs can tell:
- what kind of output they are looking at
- whether the output stays inside execution
- whether the output needs review or return-to-planning

---

## Execution-Local vs Planning-Relevant Rule

Execution intelligence must distinguish between:

### Execution-local outputs
These are outputs that can legitimately support maintenance, correction, or bounded review inside current execution scope.

### Planning-relevant outputs
These are outputs that materially affect what planning should do next, whether current planning assumptions still hold, or whether future execution scope should change.

Execution-local outputs may remain in V Forge handling.
Planning-relevant outputs must be surfaced through the governed return-to-planning path.

Execution intelligence must not blur those two classes.

---

## Non-Authority Rule

Execution intelligence is influential.
It is not authoritative by itself.

This means:
- it does not mutate the content graph automatically
- it does not mutate Project V planning truth automatically
- it does not self-authorize new execution work automatically
- it does not reclassify raw signal ownership

Execution intelligence may justify:
- a maintenance candidate
- a bounded correction review
- a return-to-planning finding
- a no-action result with preserved uncertainty

It must not justify silent autonomous expansion.

---

## Graph Mutation Rule

Execution intelligence must not automatically mutate graph truth.

If execution intelligence suggests a graph issue, V Forge must distinguish between:
- actual graph-truth error
- execution-local maintenance issue
- planning-level structural issue

Only bounded graph correction grounded in execution truth may change the graph.
Signal mismatch alone is not enough to mutate the graph automatically.

---

## Signal Ownership Rule

Execution intelligence may use bounded VEDA signal.
It must not absorb that signal into V Forge as canonical observatory truth.

This means:
- raw signal ownership remains in VEDA
- V Forge may preserve bounded references to the signal used for an execution intelligence view
- V Forge must not turn execution intelligence storage into a shadow VEDA archive
- execution intelligence summaries are not a substitute for VEDA evidence continuity

Using signal is not owning signal.

---

## Timing Rule

Execution intelligence may run at bounded points such as:
- after material content graph change
- after release or publication events
- during bounded maintenance review
- during execution-side validation where intelligence legitimately matters
- during explicit operator or LLM inspection requests inside V Forge scope

Execution intelligence must not become an always-on open-ended scanning engine by default.

---

## Honesty and Uncertainty Rule

Execution intelligence must preserve uncertainty honestly.

This means:
- weak signal remains weak
- ambiguous analytical result remains ambiguous
- mismatch hypotheses must not be presented as settled fact
- incomplete bounded inputs must be surfaced as incomplete

Execution intelligence that sounds decisive while resting on weak or incomplete basis is worse than a smaller but honest output.

---

## Cross-Project Integrity Rule

Execution intelligence must remain project-scoped.

This means:
- graph inputs are project-scoped
- execution continuity inputs are project-scoped
- bounded signal references are project-scoped to the active session where relevant
- no cross-project intelligence views may be built from contaminated inputs

Cross-project analytical contamination is a structural failure.

---

## Return-to-Planning Rule

When execution intelligence produces a planning-relevant finding, the correct path is bounded return-to-planning.

The return package should preserve, at the level required by context:
- what built or released execution reality was analyzed
- what bounded signal or execution inputs informed the view
- what the finding is
- why the finding may matter to planning
- what remains uncertain
- what execution truth V Forge still owns after the return

The return should transfer the finding, not collapse ownership.

---

## Maintenance Rule

Execution intelligence may support maintenance, but maintenance support remains bounded.

This means:
- execution-local maintenance candidates may remain inside V Forge when they do not widen scope
- a maintenance insight that effectively changes planning intent must not be handled as routine maintenance
- execution intelligence must not turn maintenance into stealth roadmap expansion

Maintenance is not a loophole for strategic drift.

---

## Governance and Halt Rule

Execution intelligence operations must halt or withhold action-driving outputs when:
- signal inputs are not legitimately admitted through the governed interface
- project scope is unclear
- the output would implicitly widen execution scope
- the output would be mistaken for planning authority unless explicitly reclassified and routed
- the basis is too weak or incomplete for the claimed output class

The correct fallback may be:
- uncertainty notice
- bounded no-action result
- return-to-planning candidate
- deferred analysis pending better inputs

Not every analytical impulse deserves an active outcome.

---

## Human-In-The-Loop Principle

Human review remains especially important when execution intelligence outputs:
- may trigger return-to-planning
- may justify substantial maintenance action
- reveal a planning-level contradiction
- sit on ambiguous or weak signal basis
- may be misread as permission for broader execution change

Execution intelligence should make execution more legible, not more autonomous by implication.

---

## Anti-Drift Rules

### 1. No shadow VEDA rule
Do not let execution intelligence absorb raw signal ownership or observatory behavior.

### 2. No shadow Project V rule
Do not let execution intelligence become planning intelligence or roadmap authority.

### 3. No analytics-equals-permission rule
Do not let a strong analytical output become automatic authorization for new execution work.

### 4. No graph-mutation-by-mismatch rule
Do not mutate the content graph automatically because signal and structure appear misaligned.

### 5. No open-ended scanning rule
Do not turn execution intelligence into an always-on broad market research engine.

### 6. No cross-project contamination rule
Do not build execution intelligence from cross-project mixed inputs.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:
- execution intelligence is derived from execution truth plus bounded signal, not raw signal ownership
- execution intelligence stays execution-side unless its findings are returned through the governed path
- analytical mismatch does not automatically authorize graph mutation or scope expansion
- execution-local maintenance candidates are different from planning-relevant findings
- uncertainty must be preserved honestly
- execution intelligence is powerful but non-sovereign

If an LLM could use this document to justify turning V Forge into a planning brain, a signal archive, or an autonomous action engine driven by analytics, this document is failing.

---

## Usage

This document should be used:
- when designing or reviewing V Forge execution intelligence tools and operations
- when deciding what inputs execution intelligence may consume
- when classifying outputs as execution-local or planning-relevant
- when checking whether an execution intelligence output should stay local, become maintenance, or return to planning
- when reviewing whether V Forge is drifting into shadow planning or shadow observability through its analytical layer

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `mcp-surface.md`
- `content-graph-operations.md`
- `content-lifecycle-workflow.md`
- `release-lifecycle-workflow.md`
- `data-boundaries.md`
- `reporting-and-approval-model.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/external-action-governance.md`
