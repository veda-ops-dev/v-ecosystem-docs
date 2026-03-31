# V Forge

## Purpose

This document defines what V Forge is inside the V Ecosystem.

It exists to answer:

```text
What role does V Forge play in the V Ecosystem, what truth does it own, what
capability domains must it support, and how should V Forge be understood by
operators and LLMs as the owned execution operating environment for a project?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the identity of V Forge
- the role V Forge plays in the ecosystem
- the kinds of truth V Forge owns
- the high-level capability domains V Forge must support
- the high-level boundary between V Forge and other systems
- the default mental model used when classifying V Forge behavior

---

## Out of Scope

This document does not define:

- detailed V Forge workflows
- detailed execution tooling or runtime design
- detailed interface contracts
- detailed governance rules
- implementation details
- future extension layer design

Those belong in more specific V Forge, interface, workflow, or governance docs.

---

## System

- v-forge

---

## Core Rule

V Forge is the execution system of record and the owned execution operating environment
for a project inside the V Ecosystem.

V Forge exists to carry out approved work, preserve execution truth, own the content
graph of what was built, own the project's owned/branded execution footprint across
relevant surfaces, perform bounded execution-side research required to complete or
validate approved handoffs, and report bounded execution findings back into the
ecosystem.

Execution-side research is bounded to work required to complete or validate an
approved handoff. V Forge must not conduct open-ended signal gathering and must not
propose unsolicited changes to planning direction.

V Forge must not expand into planning ownership or signal-system ownership.

---

## V Forge Definition

V Forge is the system used to execute approved work after responsibility has been
handed off from planning.

More broadly, V Forge is where the project's owned execution footprint is built,
operated, maintained, and made legible to the LLM and operator over time.

It turns inputs such as approved handoffs, bounded evidence inputs, operator
direction, and prior findings into:

- execution truth
- implementation truth
- content graph truth for built projects
- release and publication continuity records
- owned/branded execution surface state across relevant project surfaces
- operator playbooks, checklists, and repeatable execution guidance
- bounded execution findings
- execution intelligence derived from crossing content graph against VEDA signal
- maintenance execution outputs
- execution-side reporting

V Forge is not the planner.
V Forge is not the signal/observability system of record.
V Forge is not the experimentation or optimization system by default.
V Forge is not the SaaS/runtime/commercial layer by default.

---

## Owns

V Forge owns:

- execution truth
- implementation truth
- the content graph of what was built — pages, topics, entities, internal links,
  archetypes, schema usage
- release and publication continuity — the structured record of what has been
  published, when, and at what state
- owned/branded execution surfaces relevant to a project — the surfaces V Forge
  operates, builds, and maintains as the project's execution footprint
- publication and engagement continuity where publication and engagement are part
  of the project's owned execution, not open-ended social listening
- operator playbooks, checklists, and execution guidance — the repeatable
  operational knowledge needed to build, operate, and maintain project surfaces
- execution-side tactic and application knowledge needed to operate project
  surfaces repeatably
- execution intelligence — the cross-referencing of the content graph against
  VEDA observatory signal
- bounded execution-side research
- execution-side maintenance truth
- execution-side reporting
- bounded execution findings produced during approved work

### Content Graph Ownership Explanation
The content graph is the structural model of what a project has built. It describes
pages, topics, entities, internal links, archetypes, and schema usage. This is
execution truth because it reflects what V Forge has built. It changes when V Forge
does work — when pages are created, when structure changes, when content is added.

The content graph does not belong in VEDA because VEDA is a pure observatory of
external reality. The content graph is not an observation of external reality. It
is a record of what was built.

### Execution Intelligence Explanation
V Forge owns the execution intelligence layer — the analysis of how what was built
is performing and where the gaps are. This is done by reading VEDA's observatory
signal through a governed interface and crossing it against the content graph.

Questions like "we have these pages but SERP data shows we are missing coverage
here" are V Forge execution intelligence questions, not VEDA questions. VEDA
provides the raw signal. V Forge does the cross-referencing against what was
actually built.

### Publication and Engagement Continuity Boundary
V Forge owns publication and engagement continuity only where those activities
are part of owned project execution — for example, publishing content to owned
surfaces, operating owned channels, or tracking the engagement outcomes of owned
publication work.

V Forge does not own open-ended social listening, raw signal ownership, or
broad market engagement monitoring. Those are VEDA observatory responsibilities.

---

## Capability Domains

V Forge must support these high-level capability domains:

- **Build / implementation** — carrying out approved work to produce built assets
  and implementation truth
- **Content graph / structure** — maintaining the structural model of what a
  project has built across all relevant dimensions
- **Owned/branded surface operations** — building, operating, and maintaining
  the project's owned execution surfaces
- **Release and publication continuity** — managing the structured lifecycle of
  what gets published, when, and in what state
- **Engagement continuity** — where publication and engagement are part of
  owned execution, tracking what was distributed and what it produced
- **Operator playbooks and checklists** — providing repeatable operational
  guidance so project surfaces can be operated consistently by operators and
  LLM-assisted workflows
- **Execution intelligence** — crossing the content graph against VEDA signal
  to assess performance and identify execution-side gaps

These are doctrinal capability domains, not a schema or data model.
Specific design for each domain belongs in more specific V Forge docs.

---

## Future Extensions

Some capability domains may exist later as bounded extensions or adjacent layers,
but are **not core V Forge by default**.

- **Experimentation / optimization layer** — capabilities focused on systematic
  testing, experimentation, and optimization of execution assets. This may be a
  bounded extension of V Forge or an adjacent system. It is not assumed to be
  part of base V Forge identity.

- **SaaS / runtime / commercial layer** — capabilities focused on operating
  software as a service, commercial runtimes, or paid commercial product surfaces.
  These are adjacent to execution but require their own bounded identity if they
  exist. They must not be silently assumed as already part of V Forge.

These future domains must not be designed into or assumed inside core V Forge
until explicitly governed and bounded as part of the ecosystem doctrine.

---

## Does Not Own

V Forge does not own:

- planning truth
- orchestration truth
- readiness truth
- handoff truth
- signal truth
- observability truth as a system of record
- project-creation authority
- raw SERP data, GA4 data, Search Console data, or YouTube observatory data
- open-ended social listening or raw market signal ownership
- generic strategy ownership
- future runtime/commercial truth by default
- experimentation/optimization layer truth by default

### Explanation
V Forge may consume handoffs from Project V.
V Forge may consume bounded signal outputs from VEDA through the governed interface.
V Forge may produce bounded execution findings that matter to Project V or VEDA.

V Forge must not become the canonical owner of planning structure, signal-system
truth, or open-ended market signal.
V Forge reads VEDA signal. It does not own it.

Project-creation authority belongs to Project V. V Forge executes work for
projects that already exist in the ecosystem. V Forge does not decide that a
project should exist, what it should be, or what its planning structure should be.

Publication and engagement continuity belong to V Forge only where they are
part of owned project execution. Open-ended social listening or raw signal
accumulation for market intelligence purposes belong to VEDA, not V Forge.

Generic strategy — decisions about what markets to enter, what opportunities
to pursue, or what the ecosystem should prioritize — belongs to Project V,
not V Forge.

---

## Main Ecosystem Relationships

### Relationship to Project V
Project V hands off approved work to V Forge.

V Forge executes that work and may return bounded execution findings (including
issues or changed conditions) back to Project V where planning reconsideration
is needed.

Project V remains the planning and orchestration system of record.
V Forge remains the execution system of record.

### Relationship to VEDA
V Forge consumes bounded observatory signal from VEDA through the governed
signal interface.

V Forge uses that signal to power its execution intelligence layer — understanding
how what was built is performing externally and where execution-side gaps exist.

VEDA remains the signal, evidence, and observability system of record.
V Forge must not absorb the signal-system role by accumulating open-ended
signal ownership.
V Forge reads what VEDA observed. V Forge does not replace VEDA as the observer.

The governed signal path is defined in
`../interfaces/veda-to-v-forge-signal-interface.md`.

---

## Responsibility Model

V Forge is responsible for:

- executing approved work
- preserving execution continuity
- owning and maintaining the content graph of what was built
- owning the project's owned/branded execution footprint across relevant surfaces
- managing release and publication continuity
- maintaining operator playbooks and checklists for repeatable surface operation
- performing bounded execution-side research in support of approved work
- crossing the content graph against VEDA signal to produce execution intelligence
- reporting execution outcomes and bounded execution findings
- supporting maintenance execution
- returning bounded execution findings back into the ecosystem where needed
- returning blocked, failed, or incomplete execution to planning through bounded
  reporting

V Forge is not responsible for:

- deciding project structure
- deciding what should be pursued in planning
- serving as the canonical observability system
- owning raw SERP, GA4, Search Console, or YouTube data
- replacing Project V's orchestration role
- replacing VEDA's signal and evidence role
- open-ended social listening or market signal gathering
- operating experimentation/optimization layers or SaaS/commercial surfaces
  unless explicitly bounded and governed as part of the ecosystem doctrine

---

## Human-In-The-Loop Principle

V Forge is a governed execution system.

Human review and direction remain especially important for:

- execution approvals where required
- external paid actions
- significant mutations
- publication and launch-sensitive execution
- doctrine changes affecting execution boundaries
- any expansion of V Forge's surface responsibilities

V Forge may be heavily LLM-assisted, but it is not an unrestricted autonomous
execution environment.

---

## LLM Use Principle

A capable LLM operating inside V Forge should understand that:

- V Forge is the owned execution operating environment for a project
- V Forge gives the LLM structured execution truth and operational continuity
  — content graph, publication state, playbooks, execution intelligence — so
  the LLM can help build, track, maintain, publish, and operate projects with
  a human in the loop
- V Forge is the executor, not the planner; the LLM operates in V Forge's
  bounded execution scope, not as the ecosystem's planning brain
- V Forge owns the content graph of what was built
- V Forge owns execution intelligence derived from content graph plus VEDA signal
- V Forge is not the signal system; it reads VEDA signal but does not own it
- V Forge does not create projects — it executes work for projects that
  Project V has planned
- surface ownership and publication continuity belong to V Forge, but open-ended
  signal gathering and strategic planning do not
- experimentation layers and commercial/SaaS layers are not assumed to be part
  of V Forge unless explicitly bounded in the ecosystem doctrine

If the docs allow V Forge to drift toward planning ownership, observability
ownership, raw signal accumulation, or unrestricted autonomous surface expansion,
the V Forge doctrine is wrong.

---

## Usage

This document should be used:

- as the first identity doc for V Forge in the shared root
- as the top-level V Forge role definition for operators and LLMs
- as a boundary reference when writing more specific V Forge docs
- as a check against future drift in V Forge design or implementation
- as the authority anchor for which capability domains belong to V Forge
  and which belong to adjacent or future layers

---

## Related Docs

- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `system-invariants.md`
- `operational-model.md`
- `vs-project-v.md`
- `vs-veda.md`
- `human-in-the-loop-doctrine.md`
- `reporting-and-approval-model.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
