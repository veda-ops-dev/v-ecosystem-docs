# Desktop Interaction Surface and Command Dispatch

## Purpose

This document defines the doctrine governing the operator interaction surface
inside the VedaOps desktop application, with specific attention to its
terminal/REPL-style character, slash command dispatch model, and the limits
that prevent it from becoming a governance surface or a substitute for the
rest of the application.

It exists to answer:

```text
What is the operator interaction surface, what may it initiate, what must it
never complete, how do slash commands work as bounded dispatch invocations,
how does the surface remain a support surface rather than the real system,
and how do terminal-style ergonomics interact with the governance posture
already established across the desktop doctrine?
```

This is a Tier 1 ecosystem authority document for the desktop/runtime layer.

---

## Scope

This document governs:

- the identity and bounded role of the operator interaction surface
- whether and how a terminal/REPL-style implementation relates to the existing
  interaction surface category defined in `desktop-surface-architecture.md`
- the slash command dispatch posture: what slash commands are, what governs
  their availability, what they may initiate, and what they must never complete
- the output posture of the interaction surface: what it may render and what
  must not appear here as authoritative
- the anti-affordance rules that prevent this surface from becoming an
  unrestricted shell or a governance bypass
- the REPL ergonomics doctrine: how terminal speed and directness interact
  with the existing gating and approval model
- the routing posture for delegated agents triggered through this surface
- the human-in-the-loop posture as it applies specifically to command-entry
  interaction

This document builds on and assumes the active binding of:
- `desktop-surface-architecture.md`
- `desktop-human-llm-interaction-model.md`
- `desktop-llm-behavior-contract.md`
- `desktop-governance-and-gating-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-state-and-context-model.md`
- `operator-surface-interfaces.md`
- `mcp-coordination-model.md`
- `../governance/agent-operating-doctrine.md`

---

## Out of Scope

This document does not define:

- the visual layout or component implementation of the interaction surface
- the specific command catalog or command inventory — those belong in a command
  registry document; this document defines the doctrine under which any command
  catalog must be written
- the exact approval routing for every action class — that belongs in
  `desktop-governance-and-gating-model.md`
- session compaction, memory, or continuity mechanics — those belong in
  continuity and memory docs
- MCP tool wire schemas — those belong in MCP surface and implementation docs
- the command palette overlay (defined in `session-21-command-palette.md`)
  — this document governs the persistent operator interaction surface, not
  the transient overlay palette

---

## System

- interfaces

---

## Core Rule

The operator interaction surface is a framing and dispatch surface.

It is where the operator directs work and receives bounded typed outputs.
It is not where governance happens, not where approval events are created,
not where canonical system truth becomes authoritative, and not where
Class B or Class C gates complete.

A command typed in this surface may initiate work. It does not complete
governance-sensitive work. The governance posture of any action initiated
from this surface is determined by the action's class, not by the surface
through which it was initiated.

Terminal ergonomics do not change governance posture.

---

## Surface Identity

### What this surface is

The operator interaction surface is:

- an operator framing and dispatch input surface
- a bounded typed-output display area
- a place where the operator directs work through text input and slash commands
- a surface where the LLM produces bounded typed outputs for operator review
- the primary conversational access point to the LLM within the desktop session

### What this surface is not

This surface is not:

- the canonical record browser — that is the left navigation panel and center
  workspace
- an approval or gate surface — that is the center workspace and modal gate
  layer
- the source of canonical system truth — truth lives in governed records,
  not in interaction output
- an unrestricted shell — slash command availability is governed by session
  scope, current system, and workflow posture
- permission to bypass center review surfaces or gate surfaces
- the real application — it supports the application; it does not replace it

---

## Relationship to the Existing Desktop Surface Architecture

### Surface category classification

`desktop-surface-architecture.md` defines six surface categories. Category 2,
Interaction Surfaces, is defined as:

> The LLM interaction surface where the operator frames work and the LLM
> produces typed bounded outputs. Supports the system. Does not replace it.

The operator interaction surface governed by this document is an implementation
of Category 2, the Interaction Surface. It is the right context and interaction
panel, implemented in a terminal/REPL style where the operator interacts via
text input rather than exclusively through structured form elements.

This document does not introduce a seventh desktop surface category.

If a future implementation requires the interaction surface to become
substantially different from the Category 2 definition in `desktop-surface-
architecture.md` — for example, if it acquires primary navigation authority,
canonical state display, or approval gate mechanics — that change constitutes
a surface architecture revision and must be governed explicitly through that doc,
not assumed through this one.

### What this document adds

`desktop-surface-architecture.md` defines the surface category, its role, its
required content, and its anti-affordance rules. It describes the right panel as
"not a general chat box" and establishes that the panel "supports the system"
and "does not become the real app."

This document fills the gap that architecture doc leaves open: it defines
what it means for the interaction surface to operate as a terminal/REPL-style
surface with slash command dispatch, and what governance constraints apply
to that implementation style specifically.

This document is subordinate to `desktop-surface-architecture.md`. Where the
two conflict, the surface architecture document governs.

---

## Slash Command Posture

### What slash commands are

Slash commands are bounded operator-directed invocations. They are not a
shell command language and they are not a governance bypass mechanism.

At doctrine level, a slash command is:

- a named operator intent expressed as `/command-name [optional-argument]`
  entered through the interaction surface input
- a dispatch invocation that routes to a defined action, navigation target,
  framing operation, or governed execution path
- a scoped invocation that inherits the current session scope, project scope,
  current system, and workflow posture — it does not widen any of these

Slash commands are defined by what they route to, not by their syntax.
The syntax is ergonomics. The routing is doctrine.

### What slash commands may do

A slash command may:

- initiate bounded execution work within admitted execution scope
- open a center workspace detail view for a record, package, or review surface
- set the LLM interaction mode (brainstorm, recommend, review, approval-request
  preparation)
- request a specific typed output from the LLM within current scope
- route toward a gate surface (without completing the gate action)
- initiate a delegated specialist agent within current session scope
- perform a navigation action that does not mutate governed state
- refresh context categories that are stale or incomplete
- package a bounded finding or report for operator review

### What slash commands must never do

A slash command must never:

- complete a Class B or Class C approval event inside the interaction surface
- substitute conversational confirmation for a persisted approval record
- activate a governance-sensitive action without the required gate being
  satisfied in the appropriate center workspace or modal surface
- widen the current session scope, project scope, or system scope
- create canonical system records as a side effect of the command entry alone,
  without the governed record creation path being completed
- bypass the center review-before-gate routing that the governance model requires
  for approval-gated actions
- treat command availability as governance permission

### Command scope inheritance

A slash command operates within the scope of the current session.

This means the command inherits:
- the active project, enforced by the session token
- the current system posture (Project V, VEDA, or V Forge)
- the current workflow stage and its constraints
- the current approval and gating posture

A slash command does not override any of these. It does not widen project scope.
It does not switch the current system. It does not alter the workflow stage.

If a command requires a different current system than the one currently active,
the command is unavailable in the current context. The operator must explicitly
switch the current system through the governed path before the command becomes
available.

### System-scoping of slash commands

Commands are system-scoped by their domain. A V Forge content execution command
such as `/write` or `/update` operates within V Forge posture. A Project V
planning command operates within Project V posture.

When the current system does not match the command's domain:
- the command is shown as unavailable in the interaction surface with a brief
  explanation: `Switch to [system] to use this command`
- the command must not execute silently against the wrong system
- the command must not self-resolve the system mismatch by implicitly switching
  systems

A command that appears to work across system boundaries must still respect the
ownership model. V Forge commands operate on V Forge truth. Project V commands
operate on Project V truth. Commands must not blur that by executing in the
wrong system context because the operator typed them while the wrong system was
active.

---

## Command Availability Rules

Command availability is conditional, not universal.

Commands are available or unavailable based on:

- whether an active project is selected (session scope established)
- which system is currently active
- the current workflow stage
- the current approval and gating posture
- whether required context categories are loaded and current

Unavailable commands must be shown as unavailable with a brief explanation —
they must not be hidden entirely. The operator should be able to see what
commands exist even when they cannot execute them in the current context.

### Commands and the approval model

No slash command is Class A merely because it is entered through the interaction
surface. A command's action class is determined by what it does, not by where
it is invoked.

If a command initiates a Class C action — for example, initiating a content
publication sequence — the Class C gate applies. The command routes toward the
gate surface. The gate completes in the center workspace or modal, not in the
interaction surface.

Typing a command faster does not reduce its action class. Terminal speed does
not reduce governance requirements.

---

## Output Posture

### What the interaction surface may render

The interaction surface may render:

- bounded typed output cards as defined in `desktop-llm-behavior-contract.md`
  and `desktop-human-llm-interaction-model.md`, including: Finding, Recommendation,
  Review Summary, Approval Request Package, Execution Report, Uncertainty Notice,
  Continuity Reminder
- execution status updates for delegated work in progress
- slash command acknowledgment or error messages
- navigation prompts that open center workspace detail views
- bounded execution progress output for admitted content execution work
- streaming LLM output rendered with appropriate type labeling

### What the interaction surface must not render as authoritative

The interaction surface must not:

- render a persisted approval event as though it completed in the interaction
  flow — approval events complete in center workspace gate widgets and are
  persisted to the database; the interaction surface may show the outcome
  after the fact as an acknowledgment, but the completion happened elsewhere
- render canonical record creation as though the typed output itself is the
  record — records are created through the governed API path; interaction output
  is not the record
- render an ambiguous "done" state for governance-sensitive work that has not
  actually been completed through the governed path
- present streaming execution output as canonical execution truth before the
  execution has completed and been properly recorded
- present LLM reasoning as canonical system state

### Output type labeling

Every typed output rendered in this surface must carry its type label.

The operator must never need to infer from context whether they are looking at
a Recommendation, a Finding, a Review Summary, or an Approval Request Package.
The type label is not optional decoration. It is the mechanism by which the
operator knows what governance significance the output has and what response
options apply.

This requirement holds regardless of implementation style. A terminal-rendered
output carries the same type label as a card-rendered output. Brevity of display
does not reduce the labeling requirement.

---

## REPL and Terminal-Style Ergonomics

### Terminal style is an admissible implementation posture

The operator interaction surface may be implemented as a terminal/REPL-style
surface — an input area that accepts text and slash commands, with streaming
output displayed sequentially in a scrollable output area.

This implementation style is compatible with the interaction surface category
defined in `desktop-surface-architecture.md`. It is not a new surface category.

Terminal-style rendering — streaming text, sequential output, keyboard-first
interaction — is an ergonomic choice. It is not an architecture change.

### Terminal speed does not weaken governance

The speed of typing `/publish` followed by Enter is the same as clicking a
publish button. The action class is the same. The gate requirement is the same.
The approval posture is the same.

An operator accustomed to terminal environments may experience slash commands
as more direct than GUI controls. That experience is valid and useful. It must
not, however, be translated into a belief that the governance posture differs
for terminal-entered commands.

The desktop application must structurally prevent this confusion by:
- showing the action class badge on commands that carry Class B or C implications
  before the operator executes them
- routing Class B and C invocations to the appropriate gate surface rather than
  completing them inline
- confirming routing clearly in the output area: `Routing to [gate surface] for
  approval — this action requires explicit authorization.`

### REPL pattern and session continuity

A REPL-style interaction surface operates within a session. Session rules apply:

- the session scope is set at session start by the operator's project selection
- commands operate within that scope for the duration of the session
- session expiry invalidates the interaction surface — commands cannot execute
  in an expired session
- re-initialization is required before commands resume

The session token model defined in `mcp-coordination-model.md` applies fully
to commands entered through the interaction surface. Commands do not bypass
the session token. They do not gain cross-project access. The REPL is inside
the session boundary, not outside it.

---

## Delegated Agents Triggered Through This Surface

### Commands may trigger delegated specialists

Some slash commands may trigger delegated specialist agents within the current
session scope. For example, a content execution command within V Forge may
trigger a bounded analysis agent to inspect the content graph before proceeding,
or a specialist to validate execution prerequisites.

This is admissible. It is governed by `desktop-agent-orchestration-model.md`.

### Delegation constraints from this surface

When a slash command triggers delegated work:

- the delegated work inherits the current session scope — it does not widen it
- the delegated work does not gain additional authority by being triggered
  through a command entry rather than through the operator UI
- delegated outputs must be visible to the operator as delegated work in
  progress — they must not collapse into an anonymous processing state
- delegated completion must produce a bounded typed output that the operator
  reviews, not a silent state change

### Delegated work does not complete governance gates

A delegated specialist triggered by a command does not have authority to complete
a Class B or Class C gate on behalf of the operator. Delegation is a runtime
capability enhancement. It is not a governance bypass.

If delegated work produces a finding or recommendation that requires a gate
to be satisfied, the output routes through the same operator review and gate
path as any other finding or recommendation. The operator completes the gate.
The delegation prepared the package. It did not authorize the action.

---

## Anti-Affordance Rules

The following must be absent from this surface.

### No Class B or Class C completion inline

No command, no conversational statement, and no LLM output in the interaction
surface constitutes a completed Class B or Class C approval event. The surface
must not expose affordances that create the appearance of inline governance
completion.

This means:
- no "Confirm and proceed" button embedded in a command output card that writes
  a Class B approval record and activates the action in one step
- no command sequence that chains through Class B or C completion without the
  operator navigating to the center workspace gate
- no approval-request output in this surface that carries a gate widget — the
  Approval Request Package output may carry a `[Proceed to Approval Gate]`
  routing action, but the gate itself lives in the center workspace

### No prose confirmation as approval

No statement the operator makes through the interaction surface text input
constitutes governed approval for any action class. Typing "yes", "confirm",
"approved", or any equivalent phrase in the input area does not satisfy any
gate.

The desktop application must not attach governance significance to conversational
statements in this surface. This is structural, not behavioral: the interaction
surface input must not be a path through which approval records are created.

### No silent scope expansion through command chaining

Slash commands must not chain in a way that expands execution scope beyond the
admitted session scope without the operator being aware of the expansion and
confirming it through the governed path.

A command sequence like `/write [topic]` followed by auto-chained commands that
create additional assets, expand research scope, or widen the execution target
beyond the admitted handoff is not admitted. Each command operates within the
current admitted scope. Chaining does not authorize cumulative scope expansion.

### No affordances that make the surface look like unrestricted shell authority

The interaction surface must not present itself visually or behaviorally as a
shell with unrestricted execution authority. This means:

- no command prompt styling that implies root or unrestricted access
- no output that presents Class C actions as executed without showing the
  routing-to-gate path
- no command descriptions that use language like "directly publishes" or
  "immediately executes" for Class C operations, when in fact they route to
  a gate
- no "power user" affordances that visually or behaviorally imply that
  typing commands bypasses the governance requirements that apply to GUI
  interactions

### No governance through the interaction surface becoming the real system

The interaction surface becomes the real system when the operator can do
everything that matters entirely within the interaction surface without ever
navigating to the left panel, center workspace, or gate surfaces.

That must not be permitted to happen organically.

The gate must not come to the surface. The surface must route to the gate.
Record review must not happen inline in output cards. Navigation to the record
detail must remain the review path. Approval must not happen via an inline
widget appended to a slash command result.

The practical enforcement of this rule is that the center workspace, left
navigation, and gate surfaces must remain the authoritative surfaces for review
and governance. The interaction surface routes to them. It does not absorb them.

---

## Human-In-The-Loop Posture

Fast command entry does not reduce review requirements.

An operator who uses slash commands rapidly and efficiently still has the
same review obligations as an operator who uses the GUI. The speed at which
work is initiated does not compress the review that governance requires.

Where review is required before a gate, the review happens in the center
workspace. That requirement holds regardless of how quickly the command was
typed.

Where human approval is required for a Class C action, that approval requires
deliberate operator action through the gate widget. It does not happen because
the operator typed the initiating command quickly and confidently.

The interaction surface must make this distinction visible:
- commands with Class A routing execute immediately with appropriate feedback
- commands with Class B routing open the gate surface with a clear notice that
  the action requires approval before proceeding
- commands with Class C routing open the gate surface with a clear notice that
  the action is launch-sensitive or external-facing and requires explicit
  governed authorization

The operator must never be surprised that a command did not immediately execute
a Class B or C action. The routing behavior must be explicit and expected.

---

## Relationship to the Command Palette

The command palette (defined in the Session 21 UX specification) is a transient
overlay surface opened by `⌘K`. It is not the same surface as the persistent
operator interaction surface governed by this document.

The command palette is for discovery and keyboard-first navigation to commands
and records. It is a launcher. It closes after routing.

The persistent interaction surface is for framing work, entering slash commands
in flow, and receiving typed LLM output across a working session. It is a
workspace.

Both surfaces route through the same command availability rules, the same scope
inheritance model, and the same governance posture. They share doctrine. They
are distinct implementation surfaces.

---

## LLM Use Principle

A capable LLM operating within the interaction surface should understand that:

- this surface is a framing and dispatch surface, not a governance surface
- slash commands initiate work; they do not complete governance-sensitive work
- the LLM's outputs in this surface are typed inert outputs — they do not
  become authoritative merely because they were produced in response to a
  command
- an Approval Request Package produced in response to a command still routes
  the operator to the center workspace for the gate; it does not complete the
  gate inline
- the session scope is fixed by the session token; commands do not widen it
- terminal speed and command fluency do not change the action class of any
  operation
- delegated work triggered by a command is bounded, visible, and non-authoritative
- conversational confirmation in this surface is not governed approval for any
  action class

If an LLM produces outputs in this surface that imply Class B or C actions have
been completed, that canonical records have been created by the output alone,
or that conversational agreement in this surface constitutes governed approval,
this doctrine is being violated.

---

## Usage

This document should be used:

- when designing the persistent operator interaction surface in the VedaOps
  desktop application
- when designing the slash command dispatch model and command availability rules
- when evaluating whether a proposed command or interaction pattern stays within
  the surface's bounded role
- when reviewing whether a terminal/REPL-style implementation preserves the
  governance posture already established in the desktop doctrine
- when writing a command registry document, as the doctrinal foundation that
  governs what the registry may contain
- when evaluating whether the interaction surface is drifting toward becoming
  the real system

---

## Related Docs

- `desktop-surface-architecture.md`
- `desktop-human-llm-interaction-model.md`
- `desktop-llm-behavior-contract.md`
- `desktop-governance-and-gating-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-state-and-context-model.md`
- `desktop-system-init-and-tool-surface-model.md`
- `operator-surface-interfaces.md`
- `mcp-coordination-model.md`
- `runtime-sidecar-and-nerve-model.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/allowed-agent-actions-matrix.md`
- `../v-forge/content-execution-module.md`
- `../ecosystem/decisions/ADR-011-tauri-2-desktop-is-the-operator-host.md`
- `../ecosystem/decisions/ADR-005-session-token-model-for-project-scope.md`
- `../ecosystem/decisions/ADR-010-agent-orchestration-is-an-extension-runtime-capability.md`
