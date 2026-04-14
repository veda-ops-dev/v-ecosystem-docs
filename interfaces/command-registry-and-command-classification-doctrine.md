# Command Registry and Command Classification Doctrine

## Purpose

This document defines the doctrine governing the command layer of the VedaOps
desktop application.

It exists to answer:

```text
What command classes exist, how do command types map to system ownership, what
kinds of commands are admissible in which system posture, what must never exist
in the wrong system posture, what doctrine must a future command registry obey,
and how does the command layer remain a bounded dispatch surface rather than
becoming a shadow architecture?
```

This is a Tier 1 ecosystem authority document for the desktop/runtime layer.

---

## Scope

This document governs:

- the identity and role of the command layer inside the VedaOps desktop
- the command class model and what each class means
- how command classes map to system ownership
- the rules governing command availability by current system, session scope,
  and gate posture
- the relationship between command entry and action class
- the doctrine a future command registry must follow
- forbidden command patterns that must not exist in any system posture
- how commands relate to delegated agents and plugins
- the shared interaction surface as a surface that remains system-scoped

This document builds on and assumes the active binding of:
- `desktop-interaction-surface-and-command-dispatch.md`
- `desktop-surface-architecture.md`
- `desktop-governance-and-gating-model.md`
- `desktop-llm-behavior-contract.md`
- `desktop-human-llm-interaction-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-state-and-context-model.md`
- `operator-surface-interfaces.md`
- `mcp-coordination-model.md`
- `../v-forge/content-execution-module.md`
- `../v-forge/bounded-analytical-tools-and-plugin-doctrine.md`
- `../governance/agent-operating-doctrine.md`

---

## Out of Scope

This document does not define:

- the specific command catalog or full command inventory — that belongs in the
  command registry document that this doctrine governs
- exact UI presentation or visual rendering of commands
- full machine-readable registry schema or implementation data model
- the specific MCP tools that back individual commands
- session initialization mechanics — those belong in `mcp-coordination-model.md`
- approval workflow mechanics beyond command-to-gate routing posture

---

## System

- interfaces

---

## Core Rule

Commands are operator-facing dispatch artifacts.

A command is a named operator intent that routes work within governed system
posture. Commands do not carry authority. They do not complete governance-sensitive
work. They do not cross system boundaries silently. They do not dissolve ownership.

Command fluency — typing fast, knowing the syntax, building habits — does not
expand what commands are permitted to do in a given system posture. The speed
or confidence of command entry does not change action class, widen scope, or
satisfy any governance gate.

The command layer must remain a surface that governs routing and dispatch.
It must not become a convenience layer that re-architects the ecosystem from
within the interaction surface.

---

## Identity

### What commands are

Commands inside the VedaOps desktop are:

- operator-facing dispatch invocations that route work within the current session
  scope and system posture
- bounded initiators that may start admitted work, navigate to review surfaces,
  set framing mode, or route toward governance gates
- system-scoped artifacts: each command belongs to a system and is available
  only when that system is active
- governed participants: their availability is conditional on session, scope,
  workflow posture, and gate state

### What commands are not

Commands are not:

- autonomous authorities that can approve, publish, or scope-expand on their own
- cross-system dispatch mechanisms that blend Project V, VEDA, VEDA Strategy,
  and V Forge into a single command vocabulary
- governance substitutes that complete Class B or Class C actions inline through
  the interaction surface
- scope-widening mechanisms that extend execution authority through command
  chaining or argument composition
- backdoors around the review-before-gate routing that the governance model requires

---

## Command Classes

The following command classes define how commands are grouped by role and
what each class may do. These classes are doctrine-level groupings. A future
command registry must classify every command against one of these classes.

### Class N — Navigation Commands

Commands that navigate the operator to a surface, record, or review area without
mutating any governed state.

Examples of what these commands do:
- open the detail view for a record in the center workspace
- navigate to a specific panel or surface within the current system
- open a review surface for a package, finding, or report

Rules:
- must produce no side effects
- must not initiate work
- must not change workflow stage or session scope
- available broadly within the current system posture, typically with fewer
  preconditions than other classes

### Class F — Framing and Mode-Setting Commands

Commands that set the LLM interaction mode or establish the framing context
for the current interaction without initiating execution or governance-sensitive
output production.

Examples of what these commands do:
- set the LLM to Brainstorm, Review, Recommendation Packaging, or Approval
  Request Preparation mode per `desktop-human-llm-interaction-model.md`
- establish context framing for an upcoming typed output request
- switch the operator's focus to a specific record or package as framing context
  without opening a full detail view

Rules:
- must not initiate execution, record creation, or workflow transitions
- must not produce Recommendations or Approval Request Packages by themselves
- framing is a precondition for some typed outputs; it is not itself a typed output

### Class A — Bounded Analysis Commands

Commands that initiate bounded analytical work on already-admitted execution scope,
existing records, or loaded context, and return typed bounded findings or summaries.

Examples of what these commands do:
- run an analytical tool on a built content asset within admitted V Forge scope
- request a review summary of a specific record's current state
- invoke a bounded quality, structure, or coverage analysis on in-scope material
- run a readiness check in read-only mode

Rules:
- operate within current system and session scope
- may invoke bounded analytical tools and specialist agents per
  `../v-forge/bounded-analytical-tools-and-plugin-doctrine.md`
- return typed analytical findings — not approvals, not scope changes
- must not conduct open-ended research or discover new content targets
- tool and helper invocations triggered by Class A commands remain bounded
  and non-authoritative per the plugin doctrine
- correspond to Class A actions in the governance and gating model — no gate required

### Class X — Bounded Execution Commands

Commands that initiate approved execution work within admitted V Forge execution
scope, handed off through the governed path.

Examples of what these commands do:
- initiate creation of a content asset where the execution scope has been
  admitted through the governed handoff
- initiate an update to an already-built asset within admitted scope
- run an execution playbook step for an admitted work unit

Rules:
- require an active admitted execution scope from a valid governed handoff
  per `project-v-to-v-forge-handoff-interface.md`
- must confirm handoff sufficiency before proceeding per
  `../v-forge/content-execution-module.md`
- do not conduct open-ended research or discover content targets
- publication actions initiated through execution commands route to the
  Class C gate; commands do not complete publication inline
- scope is inherited from the active handoff; commands do not widen it
- available only in V Forge system posture

### Class E — Evidence and Signal Access Commands

Commands that request bounded evidence or signal from VEDA through the governed
interface, or that surface already-loaded VEDA signal context for review.

Examples of what these commands do:
- surface the currently loaded startup signal package for the active execution scope
- request mid-execution bounded evidence through the governed active query path
- open a signal package review in the center workspace
- surface available observatory records for the active project scope

Rules:
- must operate through the governed signal interface, not through direct provider
  access — V Forge commands in this class route through the interface defined in
  `veda-to-v-forge-signal-interface.md`; Project V commands route through
  the appropriate VEDA-to-Project-V interface
- must not acquire signal ownership; consuming delivered signal is not owning it
- must not conduct open-ended observatory sweeps
- signal surfaced through these commands remains VEDA-owned with attribution intact
- available only in the system posture for which the signal is relevant

### Class P — Packaging and Review-Routing Commands

Commands that prepare, package, or route work toward operator review surfaces
without completing approval or activation.

Examples of what these commands do:
- package an Approval Request Package for a pending Class B or Class C action
- prepare a return-to-planning finding package for operator review and routing
- package an execution report for delivery through the governed reporting path
- route a finding or recommendation to the appropriate center workspace review surface

Rules:
- produce typed outputs (Approval Request Package, Finding, Execution Report,
  Recommendation) per `desktop-llm-behavior-contract.md` — these outputs are inert
- must not complete the gate; they route toward the gate surface
- must not bundle a packaging action with silent record creation
- a command that packages a handoff proposal routes to the center workspace
  review surface; the operator completes the approval gate there

### Class G — Gate-Routing Commands

Commands that route the operator from a prepared package or review context
toward the appropriate approval gate surface.

Examples of what these commands do:
- navigate the operator from an Approval Request Package output to the
  Class B gate widget in the center workspace
- initiate the launch authorization gate surface after pre-launch verification
  is complete
- surface the confirmation path for an approval-gated action

Rules:
- do not complete Class B or Class C gates themselves
- route the operator to the gate surface in the center workspace or modal
  as defined in `desktop-surface-architecture.md`
- must show the action class badge before the operator initiates routing
- available only when the preconditions for the relevant gate are satisfied:
  active project, correct system posture, required review completed

---

## System Ownership Mapping

Commands are system-scoped. Each command belongs to one system. It is available
when that system is the current active system. It is unavailable otherwise.

The shared interaction surface does not flatten system ownership. The same
terminal/REPL-style surface may host commands from any system — but which commands
are available at any moment is determined entirely by which system is active.

### Project V command ownership

Project V owns commands whose primary function is:

- planning record creation and status transitions
- handoff preparation and packaging
- intake framing, evaluation, and outcome routing
- decision record creation and review
- return-trigger review and routing
- readiness evaluation initiation
- approval request packaging for planning-side actions

Classes principally represented: N, F, P, G; limited A for read-only planning
analysis; limited E for consuming VEDA signal in planning context through the
governed path.

**Project V must not own commands that initiate execution work, configure
observatory scope, or access signal outside the governed VEDA-to-Project-V path.**

### VEDA command ownership

VEDA owns commands whose primary function is:

- observatory scope configuration within governed operator bounds
- signal package review and surfacing
- evidence record access and freshness review
- paid data pull approval request initiation
- observatory event log review

Classes principally represented: N, F, E, P, G for spend-sensitive pull requests.

**VEDA must not own commands that create planning records, initiate execution,
or make strategic interpretations of observatory signal. VEDA commands surface
signal. They do not own what the signal means.**

### VEDA Strategy command ownership

VEDA Strategy owns commands whose primary function is:

- strategic signal package inspection for signals relevant to the current project
- surfacing VEDA Strategy findings for operator review
- packaging strategic signals for delivery through the governed interface to
  Project V or V Forge
- reviewing derived strategic intelligence outputs relevant to the current project scope

Classes principally represented: N, F, E (for strategic signal delivery), P.

**VEDA Strategy must not own commands that initiate execution work, create planning
records, or conduct raw observatory signal gathering. VEDA Strategy commands
surface derived intelligence. They do not own planning decisions or execution scope.**

### V Forge command ownership

V Forge owns commands whose primary function is:

- bounded execution work initiation within admitted scope
- content graph review and execution state surfacing
- bounded analytical tool and plugin invocation on in-scope material
- pre-launch verification initiation
- execution report packaging and routing
- return-to-planning finding packaging from execution findings
- launch authorization gate routing

Classes principally represented: N, F, A, X, E (for consuming VEDA signal
through the governed V Forge interface), P, G.

**V Forge must not own commands that conduct open-ended research, discover
content targets, configure observatory scope, or initiate planning decisions.
V Forge commands operate on what was built and on admitted execution scope.**

---

## Command Availability Rules

Command availability is conditional. A command may exist in the registry but
be unavailable in the current context. The interaction surface must show
unavailable commands as unavailable, not hide them entirely, per
`desktop-interaction-surface-and-command-dispatch.md`.

### Conditions that govern availability

**Active project**
No execution, planning, or analysis command is available without an active
project bound to the current session through the session token model per
`mcp-coordination-model.md`. Navigation and framing commands may be available
in limited form before project selection.

**Current system**
Commands are available only when the system they belong to is the current
active system. A V Forge execution command is unavailable in Project V posture.
A Project V planning command is unavailable in V Forge posture. System mismatch
must be surfaced to the operator:
`Switch to [system] to use this command.`
Commands must not self-resolve a system mismatch by implicitly switching systems.

**Session and workflow posture**
Some commands require a specific workflow stage, an active handoff, or a
specific gate posture. A gate-routing command for a Class C launch action is
unavailable if pre-launch verification has not been completed. An execution
command requiring an admitted handoff scope is unavailable if no valid handoff
is active for the current project.

**Gate posture**
When an approval is actively in-flight, commands that would mutate the basis of
that approval must be either unavailable or surfaced with a warning before they
execute. Commands that would widen scope, change context, or mutate the basis of
a pending gate must be treated with caution per `desktop-agent-orchestration-model.md`.

---

## Command Posture vs Action Class

Command entry does not change action class.

A command that initiates a Class C action remains Class C regardless of how it
was invoked — through a slash command, a command palette entry, a button click,
or any other mechanism. The action class is determined by what the action does,
not by how it was initiated.

The rules from `desktop-governance-and-gating-model.md` apply fully:

- commands may initiate Class A work directly
- commands may initiate or route Class B work; completion requires a persisted
  approval event in the center workspace gate surface
- commands may initiate or route toward Class C work; completion requires a
  persisted approval event plus typed confirmation where irreversible
- commands that surface Class D conditions must escalate, not proceed

A command entry acknowledging Class B or C work routes the operator to the
appropriate gate surface. The command does not complete the gate. The operator
completes the gate in the center workspace or modal.

Typing a command faster does not reduce the gate requirement.
Terminal ergonomics do not change governance posture.

---

## Command Registry Doctrine

A future command registry must be written under this doctrine. This section
defines what the registry must track at a minimum.

The registry is the catalog that implements this doctrine. It obeys this doc.
It does not supersede it.

### What the registry must record per command

**Command identifier**
A stable machine-readable name for the command.

**Command class**
One of: N, F, A, X, E, P, G as defined above.

**Owning system**
One of: Project V, VEDA, VEDA Strategy, V Forge.
A command has exactly one owning system. No cross-system commands.

**Required current-system posture**
Which system must be active for this command to be available. In most cases
this matches the owning system directly.

**Required scope or gate preconditions**
The preconditions that must be true for this command to be available, such as:
active project, active handoff with admitted scope, specific workflow stage,
gate posture requirements, or review completion requirements.

**Action class implications**
The action class or classes implicated by this command. A command that routes
toward a Class C gate must be labeled as implicating Class C. This is not the
command's own class — it is the governance class of the work it initiates or routes.

**Invocation role**
One of: navigation-only, framing-only, analysis-only, execution-only,
evidence-access, packaging, gate-routing, or combination where a command
may initiate multiple roles. Combinations must be explicit, not implied.

**Delegated-work implications**
Whether invoking this command may trigger delegated analytical tools, specialist
agents, or plugin invocations, and under what bounded conditions. This must be
visible in the registry so command design does not hide delegation.

**Availability behavior when unavailable**
How the command should be presented to the operator when preconditions are not
met: shown as unavailable with explanation, hidden entirely (only in cases where
the command should never be discoverable from the current system), or surfaced
with a conditional warning.

### What the registry must not do

- invent system ownership that does not follow from this doctrine
- create commands that mix planning and execution authority
- create commands whose action class implications are unstated
- create commands that widen scope through argument composition without explicit
  scope confirmation at each step
- register commands as Class A that actually implicate Class B or C work

---

## Forbidden Command Patterns

These patterns must not exist in the command registry or be implemented in the
interaction surface. They represent the most important anti-drift rules for the
command layer.

### Silent cross-system dispatch

A command that belongs to one system must not silently route to another system's
operations. A V Forge command must not silently write a Project V planning record.
A Project V command must not silently trigger observatory ingestion. Cross-system
dispatch must always be explicit, visible to the operator, and governed by the
appropriate interface.

### Mixed planning and execution authority in one command

A command must not combine planning-level decisions with execution-level actions
in a single invocation. Commands that appear to "create and publish" or "plan and
execute" in one step are blurring the handoff boundary between Project V and
V Forge. That boundary must remain explicit and traversed through the governed
handoff interface.

### Open-ended research inside V Forge

Commands inside V Forge must not conduct open-ended keyword research, competitive
SERP analysis, content opportunity discovery, or any equivalent activity that
belongs upstream in VEDA or VEDA Strategy. The `/research`-pattern prohibition
from `../v-forge/content-execution-module.md` applies at the command layer: a V
Forge command that begins from a free-form topic and discovers what to build is
not an execution command, regardless of how it is named.

### Implied inline approval completion

A command must not be designed or described in a way that implies a Class B or C
approval completes inline through the command entry. A command may route toward
a gate. It may not be the gate. Command naming and descriptions must not use
language like `directly publishes`, `immediately activates`, or `confirms and
deploys` when in fact the action routes to a gate surface.

### Scope widening through chained convenience

Command chaining — invoking a sequence of commands that collectively accomplish
more than any single command is permitted to do alone — must not be used to
widen execution scope beyond the admitted handoff without explicit scope confirmation.
A command chain that starts from a valid execution scope and progressively expands
into new assets, new topics, or new research without operator confirmation at each
step is a scope-widening failure. Each command in a chain operates within the
scope that was active when it was invoked.

### Making VEDA behave like a strategy engine

VEDA commands must not be designed to produce competitive analysis conclusions,
opportunity scoring, or content gap recommendations. Those are VEDA Strategy
functions. A command that surfaces VEDA signal is an evidence-access command.
A command that interprets that signal into strategic conclusions is not a VEDA
command. It is, at best, a VEDA Strategy command — and the interpretation must
route through VEDA Strategy's governed role, not be embedded in VEDA command output.

### Systemless shell behavior

The shared interaction surface must not be designed or described as a systemless
shell where the operator can type any command and have it resolve against any
system without knowing the current system posture. Commands are system-scoped.
The shared surface hosts commands from any system — but which commands are active
at any moment is determined entirely by which system is active. The surface must
never feel like ownership has been dissolved into a single undifferentiated CLI.

### Provenance deception commands

No command that removes authorship markers, scrubs content watermarks, or
misrepresents the origin of execution outputs may exist in any system posture.
This prohibition is absolute and is not relaxable through framing, context, or
operator preference.

---

## Commands and Delegated Agents or Plugins

Some commands trigger delegated helpers: analytical tools, specialist agents,
or plugin-style workers per `../v-forge/bounded-analytical-tools-and-plugin-doctrine.md`
and `desktop-agent-orchestration-model.md`.

The following rules apply when commands trigger delegation:

**Command ownership does not transfer to the helper**
A V Forge analysis command that triggers a specialist agent is a V Forge command
invocation. The specialist agent operates within V Forge's scope and posture.
The agent does not acquire separate system authority by being invoked through
a command.

**Helper invocation stays bounded by the command's system and scope posture**
The delegated helper inherits the session scope and system posture of the command
that triggered it. It does not gain broader scope. It does not access other
systems' truth as though it owns it.

**Command registry design must not hide delegated-work implications**
If a command may trigger a specialist agent, analytical module, or plugin
invocation, the registry must document that delegation. Delegation must not be
hidden in command descriptions in a way that makes commands appear simpler than
they are.

**Delegated outputs remain bounded and non-authoritative**
A finding, score, or recommendation produced by a delegated helper triggered
through a command is a bounded analytical output. It is not authority. It does
not self-authorize scope expansion or publication. The non-authority rules from
`../v-forge/bounded-analytical-tools-and-plugin-doctrine.md` apply fully.

---

## Shared Surface, Different System Posture

The VedaOps desktop uses a single shared terminal/REPL-style interaction surface
across all systems. This is an ergonomic choice, not a system design choice.

The following is explicitly true:

- Project V, VEDA, VEDA Strategy, and V Forge all use the same interaction surface
- the same slash-command syntax, input field, and output rendering apply in all systems
- operators do not enter a different product when they switch systems

The following must remain equally true:

- commands are system-scoped; the active system determines what commands are available
- switching the active system changes which commands are reachable, what framing modes
  apply, and what action classes the surface routes toward
- the interaction surface does not become an equalizing layer that makes all systems
  feel like one blob; the current system shown in the context strip is not cosmetic
- the LLM's output posture is governed by the current system, not by conversation topic

The practical enforcement mechanism is the current-system indicator in the topbar
and context strip, the command availability rules defined above, and the system-scoped
routing described in `desktop-interaction-surface-and-command-dispatch.md`. These
together ensure the shared surface remains system-aware without requiring the
operator to use a different interface for each system.

---

## Doctrine Examples

The following examples illustrate how this doctrine applies. These are
representative command examples, not catalog entries.

### Project V planning command example

A command that prepares a handoff package for operator review belongs to
Project V, class P (Packaging). It is available only in Project V posture with an
active project. Invoking it does not activate the handoff — it produces an
Approval Request Package typed output that routes the operator to the center
workspace review surface and then to the Class B or C gate. The command's action
class implication is Class B or C depending on scope and launch sensitivity.
The registry entry must document this routing explicitly so operators understand
that typing the command initiates the packaging process, not the approval.

### VEDA evidence and signal command example

A command that surfaces the currently loaded VEDA startup signal package for the
active execution scope belongs to V Forge system posture, class E. It is available
only in V Forge posture with an active handoff. Invoking it produces a bounded
display of already-delivered signal. It does not initiate new observatory sweeps.
It does not make the signal V Forge-owned. The attribution label `SOURCE: VEDA`
remains visible in the output. If additional signal is needed that was not
delivered at startup, that need surfaces through the governed evidence-access
path — not through expanding the scope of this command.

### VEDA Strategy signal inspection command example

A command that surfaces a VEDA Strategy-derived signal package relevant to the
current project scope belongs to VEDA Strategy posture, class E. It is available
only when VEDA Strategy is the active system. Invoking it displays bounded derived
intelligence outputs — strategic gap signals, competitive conclusions, opportunity
signals — for the current project. It does not make these outputs Project V planning
decisions or V Forge execution authorizations. If the operator wants to act on a
signal, they route through the appropriate packaging command (class P) and then
through the governed planning or execution path. The command surfaces intelligence.
It does not turn intelligence into action.

### V Forge execution command example

A command that initiates production of a content asset belongs to V Forge, class X.
It is available only in V Forge posture with an active admitted execution scope from
a valid governed handoff. Invoking it confirms handoff sufficiency before proceeding.
It may trigger bounded analytical tools (a quality check, a structure review) as
delegated helpers, visible to the operator as delegated steps. It does not publish
without a Class C gate. A publication sub-command routes the operator to the launch
authorization gate surface, not through the interaction surface inline. The command's
action class implication includes Class C for any publication action.

---

## Human-In-The-Loop Principle

Command entry is one point in a larger governed flow. It is not the governing point.

The operator directs work by invoking commands. The commands route work toward
governed surfaces, review surfaces, and gate surfaces. The operator reviews and
approves at those surfaces. That sequence — initiation through command, review in
center workspace, approval at gate — is the correct use of the command layer.

Commands that collapse that sequence by completing governance-sensitive work at
the point of invocation are failures, not features. The command layer must make
it easy to initiate the right work and impossible to skip the review and gate
steps that governed work requires.

---

## LLM Use Principle

A capable LLM operating within the command layer should understand that:

- commands are dispatch artifacts, not authorities; invoking a command does not
  complete any governance-sensitive action
- a command's owning system determines where it may be used; the LLM must not
  suggest or invoke commands outside the current system posture
- Class B and C gate requirements are not reduced by the manner in which work
  was initiated through a command; they apply equally whether work was framed
  conversationally or through a slash command
- delegated helpers triggered by commands remain bounded and non-authoritative;
  their outputs are findings and recommendations, not approvals
- the shared interaction surface does not flatten system ownership; the LLM
  must not produce outputs or invoke commands as if it were operating in a
  systemless shell
- commands that would conduct open-ended research, mix planning and execution
  authority, or imply inline approval completion must be refused, not adapted
  to fit context

If an LLM treats command invocation as authority, uses commands to route around
system boundaries, or suggests commands that violate the forbidden patterns defined
above, this doctrine is being violated.

---

## Usage

This document should be used:

- as the governing doctrine when writing the command registry
- when designing any new command to verify its class, owning system,
  preconditions, and action class implications before it is registered
- when reviewing whether an existing command has drifted beyond its defined class
  or into a forbidden pattern
- when evaluating whether a command invocation is being used correctly during
  a desktop session
- when reviewing whether the interaction surface is surfacing command availability
  correctly by system posture
- when writing command descriptions in the registry to ensure they do not
  overclaim capability or obscure governance implications

---

## Related Docs

- `desktop-interaction-surface-and-command-dispatch.md`
- `desktop-surface-architecture.md`
- `desktop-governance-and-gating-model.md`
- `desktop-llm-behavior-contract.md`
- `desktop-human-llm-interaction-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-state-and-context-model.md`
- `operator-surface-interfaces.md`
- `mcp-coordination-model.md`
- `../v-forge/content-execution-module.md`
- `../v-forge/bounded-analytical-tools-and-plugin-doctrine.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/veda-strategy-to-v-forge-signal-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
