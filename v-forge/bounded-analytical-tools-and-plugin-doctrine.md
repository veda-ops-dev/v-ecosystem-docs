# Bounded Analytical Tools and Plugin Doctrine

## Purpose

This document defines the doctrine governing bounded analytical tools, scoring
modules, specialist agents, subprocess helpers, and plugin-style aids inside
V Forge.

It exists to answer:

```text
What are bounded analytical tools and plugins inside V Forge, what may they
consume, what may they output, what must they never do, how do specialist agents
remain bounded by parent scope, and how do their findings route without turning
into unauthorized new work?
```

This is a Tier 2 V Forge capability authority document.

---

## Scope

This document governs:

- the identity and role of bounded analytical tools and plugin-style helpers
  inside V Forge
- what inputs these tools and helpers may consume
- what inputs and postures are forbidden
- what outputs they may produce
- why tool and plugin output is not authority
- how specialist agents and delegated plugins remain bounded by parent scope
- how findings from these tools are classified and routed
- the boundary between these tools and VEDA, VEDA Strategy, and the approval model
- the classification of SEO Machine-pattern helpers at doctrine level

---

## Out of Scope

This document does not define:

- the runtime mechanism by which plugins or tools execute — subprocess,
  MCP tool, embedded worker, or otherwise; implementation mechanics belong
  in later technical docs
- the specific command catalog that invokes these tools — that belongs in
  the command registry
- the schema for tool output records — that belongs in the schema specification
- the full approval matrix for all execution action classes — that belongs in
  `../governance/approval-and-escalation-model.md`
- VEDA internal operations or VEDA Strategy internal operations
- Project V internal planning workflow

---

## System

- v-forge

---

## Core Rule

Bounded analytical tools and plugins inside V Forge are execution-support aids.

They assist with the work of carrying out, validating, or reviewing approved
execution. They do not carry authority. Their outputs are bounded analytical
findings that inform execution intelligence or operator review — not approvals,
not scope changes, not planning directives.

These tools are delegated bounded actors. They inherit parent execution scope.
They do not create new authority by virtue of their analysis.

A tool that can score content, identify a gap, or recommend a fix has produced
a bounded analytical finding. It has not authorized new work.

---

## Identity

### What bounded analytical tools and plugins are

Bounded analytical tools and plugins inside V Forge are:

- execution-support aids that assist with validating, reviewing, or improving
  already-approved execution work
- bounded analytical helpers that produce typed findings within their admitted scope
- specialist delegated aids that fire within a parent execution session and
  remain subordinate to it
- execution-time quality and structure reviewers operating on what was built
  or what the admitted scope describes

They are tools, not systems. They are helpers, not authorities. They are
bounded participants in execution, not independent actors with their own scope.

### What bounded analytical tools and plugins are not

These tools are not:

- independent systems with their own truth domain
- planners, observatories, or strategy engines
- scope-authorizing actors
- approval-issuing agents
- substitutes for VEDA's observatory function
- substitutes for VEDA Strategy's derived intelligence function
- substitutes for Project V's planning function
- agents that can independently decide what work to initiate next

---

## Admitted Inputs

A bounded analytical tool or plugin inside V Forge may consume only inputs from
these admitted categories:

**Admitted execution scope and handoff context**
The approved scope, constraints, and planning context delivered through the
governed handoff. This is the primary grounding for any analytical work.

**Built execution truth**
What V Forge has actually built — the content graph, publication continuity
records, execution history, and other execution truth owned by V Forge and
scoped to the active project.

**Built content graph truth**
The structural record of what was built — pages, topics, entities, internal
links, archetypes, and schema usage — project-scoped per `system-invariants.md`
invariant 8.

**Bounded VEDA signal delivered through the governed interface**
Signal delivered at execution-scope startup through `veda-to-v-forge-signal-interface.md`
or through the active evidence-query contract. These tools consume what V Forge
already holds through the governed path. They do not independently query VEDA.

**Bounded VEDA Strategy signal delivered through the governed interface**
Strategic signal packages delivered to V Forge through
`veda-strategy-to-v-forge-signal-interface.md`. These tools consume what V Forge
already holds. They do not independently query VEDA Strategy.

**Operator-provided execution framing where explicitly admitted**
Constraints, objectives, or conditions the operator has provided as admitted
execution context for the current session scope.

---

## Forbidden Inputs and Posture

The following inputs and postures are forbidden inside bounded analytical tools
and plugins:

**Direct provider signal ownership**
A tool or plugin must not independently ingest from SERP providers, GA4,
DataForSEO, Search Console, YouTube, or any equivalent external provider.
Signal ownership belongs to VEDA. These tools use signal that VEDA has already
delivered. They do not become independent signal sources.

**Open-ended external research**
A tool or plugin must not conduct open-ended searches, SERP analyses, or
competitive intelligence sweeps on its own. Research that discovers what
should exist belongs upstream in Project V, VEDA, and VEDA Strategy — not
inside a V Forge plugin.

**Unconstrained topic or opportunity discovery**
A tool or plugin must not identify new content opportunities, new keyword
targets, or new strategic directions as a primary function. That is VEDA
Strategy's derived intelligence role, not an execution plugin's role.

**Speculative planning context beyond admitted scope**
A tool or plugin must not import or construct planning-level context that
was not delivered through the governed handoff. Analytical work does not
expand the admitted scope by inferring what planning probably intended.

**Hidden cross-project data consumption**
A tool or plugin must not consume execution truth, content graph records,
or signal from a different project than the active session's project scope.
Cross-project contamination is forbidden per `system-invariants.md` invariant 8.

**Plugin-private shadow stores of canonical truth**
A tool or plugin must not maintain its own local archive of VEDA signal,
VEDA Strategy intelligence, execution records, or content graph data that
functions as a private canonical truth store. Bounded reference is admissible.
Private canonical accumulation is not.

---

## Admitted Outputs

A bounded analytical tool or plugin inside V Forge may produce outputs in these
categories:

**Bounded analytical findings**
A typed, scoped summary of what the tool observed or assessed — for example,
a readability finding, a structure observation, or a keyword density result —
within the admitted execution scope.

**Execution-time scores or classifications**
A numeric or categorical result that describes a characteristic of an
already-built or in-progress execution asset — for example, a content quality
score, a readability grade, or a schema completeness classification.

**Structure or quality recommendations**
A bounded recommendation addressing a specific characteristic of the execution
asset — for example, a heading structure improvement, an internal link gap
within the active project, or a sentence length adjustment — where the
recommendation is local to the admitted execution scope.

**Local correction candidates**
Specific bounded candidates for execution-local corrections — fixes to
what was built that remain within the admitted scope and do not require
planning reconsideration.

**Specialist summaries**
A bounded summary produced by a specialist agent to assist the parent execution
flow — for example, a consistency review across a set of admitted execution
assets, or a packaging of bounded VEDA signal for use in execution intelligence.

**Bounded return-to-planning findings**
A classified finding that the parent execution flow has identified as
potentially requiring planning reconsideration, packaged for routing through
the governed return-to-planning path. The tool surfaces the finding; the
routing happens through the governed interface, not through the tool.

**Operator review candidates**
A typed finding that the tool recommends be reviewed by the operator before
the parent execution continues — for example, a mid-execution signal that
a produced asset may conflict with existing content graph truth.

---

## Non-Authority of Outputs

This section carries equal weight to the admitted inputs section.

**Tool and plugin output is not authority.**

The following rules apply without exception:

**Scores are not approval**
A content quality score of any value — high or low — does not authorize
publication, scope expansion, or any other governed action. Scores are
observations. They are not gates.

**Recommendations are not scope expansion**
A recommendation from an analytical tool or specialist agent does not
authorize new assets, expanded topics, or additional execution work. A
recommendation that implies new work beyond the admitted scope is a
finding candidate for return-to-planning, not a self-executing instruction.

**Gap findings do not self-authorize new assets**
If an analytical tool identifies a gap — a missing internal link, a topic
not yet covered, a structural shortfall — that finding does not authorize
V Forge to fill the gap. Whether the gap is addressed, and how, is a
governed decision. The tool found it. The ecosystem decides what to do
with it through the governed path.

**Analytical outputs must not silently mutate planning or execution scope**
A tool or plugin output must not cause a silent change to what execution is
pursuing. If an output would change the execution scope, it must be surfaced
to the operator and routed appropriately. Scope changes require the governed
planning path through Project V.

**No tool output creates a canonical record by itself**
An analytical finding, score, or recommendation produced by a bounded tool
does not create a canonical content graph record, an execution truth record,
or a planning record. Records are created through the governed record creation
path, not through tool output.

---

## Delegation and Specialist Agents

### Plugins and specialist agents are delegated bounded actors

Plugins, specialist agents, and analytical helpers inside V Forge are
delegated bounded actors. This means:

- they are subordinate to the parent execution session and scope
- they inherit the parent session's project scope, system posture, and
  approved execution scope
- they do not acquire independent authority by virtue of being delegated or
  by virtue of the specialization they perform

### They inherit parent scope

A specialist agent fired within a V Forge execution session for content
analysis, link review, quality scoring, or equivalent work operates within
the same project scope as the parent session. It does not receive a broader
scope. It does not gain access to other projects. It does not widen the
execution target.

Delegation may increase analytical specialization.
It must not increase authority or scope.

This is consistent with `desktop-agent-orchestration-model.md` — delegation
does not increase power.

### They must remain visible enough for accountability

A specialist agent or plugin must not operate as an anonymous background
process when its work is meaningful — when it produces outputs the operator
will review, when it affects what execution can now say or recommend, or when
it introduces a finding that may affect the execution lifecycle.

Meaningful delegated analytical work must be operator-visible as a delegated
step. It must not silently chain into subsequent actions without the operator
being aware of what was produced.

This is consistent with the cascade-without-visibility prohibition in
`content-execution-module.md`.

### They do not cascade into unbounded execution chains

A plugin producing a finding does not trigger the next plugin automatically
without scoped confirmation. Analytical tools must not chain in a way that
progressively expands what is being assessed, built, or changed beyond the
admitted execution unit.

Each delegated analytical step operates within the scope that was active
when it was triggered. The output of one step does not automatically widen
the scope for the next.

---

## Finding Classification and Routing

Tool and plugin outputs that require follow-up must be classified before
routing. The classification governs how the output is handled.

### Local bounded correction

A finding is a local bounded correction candidate when:

- the issue can be resolved within the admitted execution scope
- the correction does not change what planning assumed about the content target
- the correction does not widen execution scope
- addressing it does not require planning reconsideration

Local bounded corrections may be handled inside V Forge handling without
returning to planning. Examples: correcting a broken internal link, updating
schema markup on an already-built page, fixing a heading structure within
the admitted asset.

### Operator review candidate

A finding is an operator review candidate when:

- the finding affects a decision the operator should make before execution
  continues
- the finding introduces an ambiguity about execution direction that the
  operator should resolve
- the finding involves a result that is outside the expected range and should
  be confirmed before proceeding

Operator review candidates must be surfaced as typed findings with their
review significance stated. They must not be silently acted on.

### Return-to-planning

A finding must be classified as a return-to-planning candidate when:

- it reveals that the real execution need is materially larger than the
  admitted scope and proceeding would amount to silent scope expansion
- it reveals a planning-level contradiction — for example, the content
  structure conflicts with what planning intended in the cluster architecture
- it reveals a gap or mismatch with planning-level significance — meaning
  it would materially change what Project V should plan next, not merely
  what maintenance should fix locally
- it reveals a changed condition that invalidates the planning basis of
  the handoff

Return-to-planning findings from analytical tools are surfaced to the
operator and packaged for routing through
`../interfaces/v-forge-to-project-v-return-to-planning-interface.md`.
The tool identifies the finding. The governed interface routes it. The tool
does not self-route to planning.

### Blocked or unresolved

A finding is blocked or unresolved when:

- the tool cannot produce a reliable result due to missing or insufficient
  inputs
- the finding falls into a category where classification is genuinely unclear
  and the tool should not guess

Blocked or unresolved findings must be surfaced explicitly. A tool that
cannot classify a finding reliably must not silently drop it or force it
into the nearest available category.

---

## Boundary with VEDA and VEDA Strategy

### Tools and plugins consume delivered signal; they do not become signal owners

A bounded analytical tool inside V Forge may use VEDA signal that has
already been delivered to V Forge through the governed startup interface or
active query contract. Using signal through V Forge's governed posture does
not make the tool an observatory.

The tool is consuming V Forge's execution-side reference to bounded VEDA
signal. It is not operating as a VEDA provider, a VEDA substitute, or an
independent observatory.

### Tools and plugins do not become VEDA Strategy

An analytical tool inside V Forge that produces scores, gap findings, or
quality classifications is producing execution-time bounded analysis.
It is not producing strategic intelligence, even if the outputs superficially
resemble strategic intelligence.

Competitive analysis, opportunity scoring, and content gap detection at the
strategic level belong to VEDA Strategy. Execution-time quality scoring,
structure analysis, and local content gap detection within admitted execution
scope are V Forge execution intelligence. The distinction is ownership,
scope, and purpose — not merely the name of the output.

**A tool or plugin inside V Forge must not perform competitive analysis,
opportunity scoring, or strategic planning discovery.**

Those functions are not admissible inside a V Forge execution plugin,
regardless of whether the tool is technically capable of performing them.

### The seam is not fully settled for all borderline analyzers

For some analytical functions, the question of whether they belong inside
V Forge or upstream in VEDA Strategy is not fully settled.

The conservative rule: if an analyzer's primary function is to identify
what should be built next, prioritize new content targets, or score opportunities
at a market or competitive level, it does not belong inside V Forge execution.
It belongs upstream.

If an analyzer's primary function is to evaluate what was already built — its
quality, its structure, its coverage relative to the admitted execution scope —
it is a V Forge execution-intelligence function when bounded to that scope.

When the boundary is unclear, the correct posture is to surface the uncertainty
rather than to claim the function as V Forge capability.

---

## Boundary with the Approval Model

### Analytical tools and plugins do not complete approvals

A bounded analytical tool or plugin inside V Forge may prepare evidence and
findings that inform an approval decision. It may produce a pre-publication
checklist result. It may surface a quality review finding. It may identify
conditions that should be reviewed before a Class C action proceeds.

**It may not complete a Class B or Class C approval.**

Approvals complete through the governed approval and gating path, as
defined in `../governance/approval-and-escalation-model.md` and enforced
through the desktop gating model in `desktop-governance-and-gating-model.md`.
No analytical tool, scoring module, or specialist agent completes an approval
event by producing a favorable finding.

### Tools may prepare the ground for review; they do not replace review

An analytical tool that finds a content asset passes a quality threshold
has produced a finding that informs operator review. That finding is an
input to the review, not a replacement for it. The operator reviews the
finding. The operator completes the approval where approval is required.

A high score does not mean publication can proceed without the Class C gate.
A passed pre-publication check does not substitute for governed authorization.

---

## Classification of SEO Machine-Pattern Helpers

This section classifies tool types associated with SEO Machine-style workflows
at doctrine level. The classification governs whether and how these patterns
are admissible inside V Forge.

### Admissible with adaptation

**Readability scorers**
Admissible as bounded execution-time analytical tools when applied to
already-admitted execution assets within approved scope. Their output is
an execution intelligence finding, not an authorization. Scores do not
self-authorize corrections or rewrites.

**Content structure analyzers**
Admissible when applied to built or in-progress assets within admitted scope.
A structure analysis of a specific asset is execution-time analysis. A
structure analysis that proposes new structural directions for the project
has crossed into planning territory and is not admissible in that form.

**Internal-link analyzers and recommendation helpers**
Admissible when bounded to the active project's content graph and the
admitted execution scope. Recommendations are execution intelligence findings.
They do not self-authorize link additions or new page creation. Cross-project
link analysis is forbidden.

**Keyword density and content coverage analyzers**
Admissible when analyzing already-built content against the admitted execution
scope and bounded VEDA signal. Not admissible when used to conduct open-ended
keyword discovery. The test: is the tool analyzing what was built against what
VEDA delivered, or is it discovering new keyword targets? The former is
execution intelligence. The latter is not.

**Content quality raters**
Admissible as bounded analytical scoring tools when applied to assets within
admitted scope. Their output informs operator review and execution intelligence.
It does not complete review or authorize publication.

**Specialist agents (SEO optimizer, editor, link mapper, content analyzer)**
Admissible as bounded delegated aids per the delegation rules in this document.
Each specialist agent must remain within the parent session's project and
execution scope, produce a bounded typed output, remain visible to the operator
as a delegated step, and not self-authorize scope expansion based on its output.

### Not admissible inside V Forge

**Open-ended keyword research helpers**
Not admissible. Discovering what content targets should exist belongs upstream
in Project V and VEDA Strategy. By the time work enters V Forge, the content
scope is admitted. A tool that begins from a free-form topic and discovers
what to build is conducting planning-side work inside execution. This is
the `/research`-pattern classification from `content-execution-module.md`
applied to plugin form.

**Competitive SERP scanners operating as independent research engines**
Not admissible inside V Forge. Competitive SERP analysis at the level of
identifying new opportunities belongs to VEDA Strategy. A V Forge plugin
that conducts open-ended competitive scanning is absorbing VEDA Strategy's
function under the banner of execution support.

**Opportunity scorers at the strategic level**
Not admissible inside V Forge. Scoring new content opportunities or prioritizing
what to build next belongs to VEDA Strategy. An execution-time score of what
was built is admissible execution intelligence. A score of what should be built
next is VEDA Strategy's function. The distinction matters and must not be blurred.

**Competitor gap analyzers used for planning-side discovery**
Not admissible inside V Forge. Gap analysis that identifies what the project
should pursue next belongs upstream. Gap analysis that identifies how what
was built compares to VEDA signal within admitted scope is bounded execution
intelligence and is admissible with appropriate governance.

**Provenance deception helpers**
Not admissible under any form. Tools that remove AI authorship markers, scrub
content watermarks, or misrepresent the origin of execution outputs conflict
with V Forge's boundary-safe reporting invariant and the honest provenance rule
in `content-execution-module.md`. This is not an execution support function.

### Admissible only upstream, outside V Forge

The following patterns are potentially admissible as capabilities in the
V Ecosystem, but belong upstream of V Forge, not inside it:

- strategic opportunity scoring as a planning input — VEDA Strategy
- content gap detection at strategic scope — VEDA Strategy
- competitive positioning analysis — VEDA Strategy
- keyword discovery and research — Project V / VEDA Strategy inputs

These capabilities may produce outputs that eventually reach V Forge as
part of a handoff package. They do not belong as tools running inside
V Forge execution.

---

## Anti-Drift Rules

### 1. No analysis-becomes-authority rule
Tool and plugin output does not authorize execution, scope change, publication,
or planning mutation. High scores, favorable assessments, and comprehensive
findings are inputs to human review and governed decisions — not replacements
for them.

### 2. No tool-becomes-observatory rule
Bounded analytical tools that use VEDA signal through V Forge's governed posture
do not become observatories. They consume delivered signal. They do not own it,
extend it, or conduct open-ended signal gathering independently.

### 3. No tool-becomes-VEDA-Strategy rule
Execution-time analytical scoring and structure analysis do not become strategic
intelligence functions. A quality score on a built asset is execution intelligence.
An opportunity score for what to build next is VEDA Strategy's function. The
purpose and scope distinguish them — not just the name.

### 4. No delegation-hides-scope-expansion rule
Specialist agents and plugins must not be used to quietly expand what the parent
execution session is doing. Delegation is a specialization convenience, not an
expansion path. Each delegated tool operates within the scope that existed when
it was triggered.

### 5. No cascade-without-visibility rule
Analytical tools and specialist agents must not automatically chain in ways that
are invisible to the operator. Meaningful delegated analytical work is visible as
a delegated step.

### 6. No convenient-research-as-execution rule
Reframing open-ended discovery work as "execution-time analysis" to admit it inside
V Forge is a boundary violation. The admission test is whether the activity validates
or improves what was already approved — not whether it can be described in
execution-adjacent language.

### 7. No shadow-planning-through-scoring rule
A tool that surfaces enough gap findings, low scores, and coverage shortfalls to
effectively reconstruct a new content plan inside V Forge is functioning as a
shadow planner. Scoring tools that return planning-level signals must route those
signals through the return-to-planning path, not accumulate them into an implicit
internal planning queue.

---

## Human-In-The-Loop Principle

Human review remains especially important in this area when:

- a tool or plugin produces findings that may require return-to-planning
- a scoring result is being used to inform a publication readiness determination
- a specialist agent has surfaced ambiguous findings that affect execution direction
- a tool has produced an output outside the expected analytical range that may
  warrant reconsideration before execution continues

Analytical tool and plugin outputs support operator review.
They do not replace it.

---

## LLM Use Principle

A capable LLM operating inside V Forge with access to bounded analytical tools
and plugins should understand that:

- these tools are execution-support aids, not authorities
- tool outputs — scores, findings, recommendations — inform execution intelligence
  and operator review; they do not authorize actions
- specialist agents remain bounded by parent session scope; delegation does not
  expand scope or authority
- signal used by these tools comes through V Forge's governed posture, not through
  independent provider access
- tools that could technically conduct competitive analysis, opportunity scoring,
  or keyword discovery must not do so inside V Forge; those functions belong upstream
- a gap finding from an analytical tool is a return-to-planning candidate if it
  has planning-level significance; it is a local correction candidate if it can
  be resolved within admitted scope; it does not self-authorize new work in either case
- provenance deception is not an admitted execution function in any form

If an LLM uses bounded analytical tools to conduct open-ended research, absorb
signal ownership, self-authorize scope expansion based on findings, or complete
approval gates based on scores, this document is failing.

---

## Usage

This document should be used:

- when determining whether a proposed analytical tool or plugin is admissible
  inside V Forge
- when classifying what a tool or plugin output means and how it should be routed
- when evaluating whether a specialist agent is remaining bounded by parent scope
- when reviewing whether a scoring or analytical module is crossing into
  VEDA Strategy territory
- when designing the classification posture for SEO Machine-style capabilities
  being considered for adaptation into the V Ecosystem
- when writing more specific playbook or execution module docs that reference
  analytical tool use

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `reporting-and-approval-model.md`
- `content-execution-module.md`
- `vs-project-v.md`
- `vs-veda.md`
- `../interfaces/desktop-interaction-surface-and-command-dispatch.md`
- `../interfaces/desktop-agent-orchestration-model.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/veda-strategy-to-v-forge-signal-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../veda-strategy/veda-strategy.md`
