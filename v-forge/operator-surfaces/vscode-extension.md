# V Forge VS Code Extension Operator Surface

## Purpose

This document defines how V Forge should appear and behave inside the unified VS Code extension operator surface.

It exists to answer:

```text
What V Forge surfaces should the operator see in the VS Code extension, what actions belong there, how should V Forge execution state, release state, graph state, findings, and return-to-planning posture be exposed, and how does the extension keep V Forge usable without letting the surface drift into planning ownership, observability ownership, or hidden governance?
```

This is a Tier 2 V Forge operator-surface authority document.

---

## Scope

This document governs:

- the operator-facing extension surfaces for V Forge
- what categories of V Forge information should be visible in the extension
- what actions are appropriate in V Forge operator surfaces
- how V Forge status, lifecycle, graph, release, and finding information should be exposed
- how V Forge surfaces should interact with the unified extension runtime without losing system boundaries
- how absent-affordance and governance rules apply to V Forge extension surfaces

---

## Out of Scope

This document does not define:

- the full extension architecture for all systems
- the exact TypeScript component tree
- the exact MCP wire schema for V Forge tools
- the full approval matrix for every action class
- future experimentation or commercial execution surfaces

Those belong in extension-wide docs, implementation docs, MCP docs, or later V Forge expansions.

---

## System

- v-forge

---

## Core Rule

The V Forge extension surface exists to make execution truth visible, operable, and governable.

It must help the operator:
- see the current execution state clearly
- act inside bounded execution scope
- understand content and release lifecycle posture
- inspect content graph truth
- review findings and return-to-planning conditions
- distinguish routine execution from authorization-sensitive execution

It must not:
- make V Forge look like Project V
- make V Forge look like VEDA
- hide governance-sensitive transitions behind convenient buttons
- let the chat panel become the real execution app

The operator surface should make execution easier without making boundaries weaker.

---

## Surface Role in the Unified Extension

Inside the unified extension, V Forge is one current-system posture among the three ecosystem systems.

That means:
- V Forge surfaces are visible when the current system or referenced context makes them relevant
- V Forge remains visually and operationally distinct from Project V and VEDA
- the extension must not flatten system boundaries just because all systems live inside one extension shell

The operator should be able to tell:
- when they are in V Forge
- what execution truth they are looking at
- what actions are local to V Forge
- when something must go back through governance or return-to-planning

This surface must stay aligned with the first-pass V Forge scope locked in `v-forge.md` and `schema-authority.md`:
- deeply modeled surfaces: website and GitHub/release
- lightly tracked surfaces: YouTube, social, newsletter, store listings
- deferred domains must not quietly appear as first-class surface commitments

---

## Surface Design Principles

### 1. Execution-first visibility
The first thing V Forge surfaces should show is execution truth, not prose chatter.

### 2. State-before-action
Operators should be able to inspect current execution state before mutating it.

### 3. Bounded action posture
Only actions that belong to the current V Forge surface posture should be present.

### 4. Explicit lifecycle visibility
Content, release, blocked, failed, partial, and return-required states should be visible as first-class execution posture.

### 5. No hidden governance
Approval-sensitive or authorization-sensitive execution must not be disguised as ordinary action.

### 6. Return is first-class
Return-to-planning conditions should be visible and operable, not treated like embarrassing edge cases.

---

## Primary V Forge Extension Surfaces

V Forge should expose a small set of clear operator surfaces inside the unified extension.

## 1. Execution Overview Surface

### Purpose
To give the operator a clear current-state view of V Forge execution for the active project.

### Should show
- active execution work units
- work-unit status summary
- blocked / failed / partial / return-required counts where relevant
- recent release activity summary
- recent findings summary
- high-level graph health or graph-related attention items where relevant

### Should allow
- opening a specific work unit
- opening blocked or failed items
- opening return-required items
- opening release or graph detail surfaces

### Should not allow
- direct stealth planning mutation
- hidden release action from a passive overview card

### Rule
The overview should feel like an execution operations board, not a planning dashboard.

---

## 2. Work Unit Detail Surface

### Purpose
To let the operator inspect and act on one bounded execution work unit.

### Should show
- work-unit identity
- current lifecycle state
- admitted execution basis or origin reference
- current execution notes or bounded findings
- current blockers or failure posture
- whether graph update or publication continuity is relevant
- whether return-to-planning posture is active

### Should allow
- bounded state transitions that belong inside V Forge execution posture
- opening related graph, release, or findings detail
- triggering bounded report or return packaging where legitimately allowed

### Should not allow
- direct planning mutation
- casual approval bypass
- system-ownership crossover actions

### Rule
The work-unit detail surface is where bounded execution becomes inspectable and actionable.
It must not become a universal do-anything panel.

---

## 3. Content Graph Inspection Surface

### Purpose
To let the operator inspect the content graph as execution truth.

### Should show
- asset nodes relevant to the active project
- relationships between assets, topics, entities, archetypes, schema usage, and internal links
- graph-local drift or correction cues where relevant
- graph completeness or inconsistency indicators where relevant

### Should allow
- bounded inspection of graph neighborhoods
- opening graph-related correction or work-unit context
- viewing where newly created or updated assets changed graph truth

### Should not allow
- speculative graph planning
- future-state graph modeling
- cross-project graph views

### Rule
The graph surface is an execution-truth inspection surface, not a strategy canvas.

---

## 4. Release Surface

### Purpose
To let the operator inspect and act on bounded release work.

### Should show
- release work units
- release readiness / validation / authorization-sensitive posture
- release continuity history
- blocked / failed / rollback-active release states
- post-release verification posture where relevant

### Should allow
- opening release detail
- reviewing release prerequisites and verification state
- executing release actions only when governance posture and runtime posture admit them
- initiating rollback only when rollback is truly in-bounds

### Should not allow
- treating release readiness as release authorization
- casual ship-it buttons without clear discipline cues

### Rule
The release surface should make authorization-sensitive work feel more explicit, not more magical.
It should remain strongest for the deeply modeled GitHub/release surface posture already admitted in first pass, while lighter surfaces should not be made to look equally deep unless scope changes are governed explicitly.

---

## 5. Findings and Return Surface

### Purpose
To make bounded findings and return-to-planning posture visible and operable.

### Should show
- execution findings
- planning-relevant findings
- return-required items
- uncertainty markers where relevant
- whether a return package is draft, prepared, sent, or awaiting planning response if that posture exists in implementation

### Should allow
- reviewing bounded findings
- packaging or opening return-to-planning material through the governed interface path
- differentiating execution-local findings from planning-relevant findings

### Should not allow
- converting findings directly into planning truth
- pretending that a chat explanation is the governing return artifact

### Rule
This surface exists because return-to-planning is a first-class part of V Forge governance, not an afterthought.

---

## 6. Execution Intelligence Inspection Surface

### Purpose
To let the operator inspect execution intelligence outputs without turning V Forge into VEDA or Project V.

### Should show
- graph-versus-signal analytical outputs
- execution-local maintenance candidates
- planning-relevant findings candidates
- uncertainty posture and basis cues where relevant

### Should allow
- reviewing bounded execution intelligence outputs
- opening linked execution work or findings context
- promoting a planning-relevant execution finding into return-to-planning packaging through the governed path

### Should not allow
- direct strategy mutation
- treating analytics as permission
- presenting raw VEDA ownership surfaces as if V Forge owns them

### Rule
Execution intelligence is inspection and interpretation support, not sovereign decision authority.

---

## Relationship to the Chat Surface

The chat panel may assist V Forge work.
It must not replace the V Forge operator surfaces as the real execution UI.

### Chat is good for
- bounded explanation
- reviewing next-step options
- preparing a bounded finding or report draft
- helping the operator navigate current V Forge truth

### Chat is not the right place for
- hidden execution state mutation
- hidden release action
- canonical graph inspection
- the only place where blocked/failed/return-required truth exists
- governance-sensitive action without surface-level visibility

### Rule
If a critical V Forge action or state only exists in chat, the extension surface is incomplete.

---

## Current-System and Referenced-System Posture

When V Forge is the current system:
- V Forge surfaces should be primary
- Project V or VEDA context may appear only in bounded referenced posture where doctrinally admitted

When V Forge is only referenced:
- V Forge context should appear as secondary or linked inspection context
- the surface must not imply that V Forge has become the current governing system by accident

The operator must not lose track of which system is primary.

---

## Surface-Level Action Classes

V Forge extension surfaces should expose actions according to bounded classes.

## Class 1 — Inspection actions
Examples:
- open work unit
- inspect graph neighborhood
- inspect release continuity
- inspect findings
- inspect execution intelligence output

### Posture
These are broadly safe and should be easy to reach.

---

## Class 2 — Bounded execution actions
Examples:
- mark execution state where admitted
- record bounded finding
- update graph truth through bounded correction path
- prepare a return package

### Posture
These belong in V Forge surfaces when they remain inside admitted execution scope and governance posture.

---

## Class 3 — Authorization-sensitive actions
Examples:
- execute release action
- execute rollback when materially consequential
- other higher-discipline public-facing or irreversible actions

### Posture
These must be visibly differentiated from routine actions.
They must not appear like casual one-click convenience operations when the underlying discipline is stronger.

---

## Absent-Affordance Rules

The V Forge extension surface must preserve absent affordances.

### Must be absent
- direct Project V planning mutation controls inside V Forge panels
- VEDA ownership controls inside V Forge panels
- casual cross-system write controls
- generic “approve and continue” shortcuts that erase governance posture
- release actions presented as normal passive navigation buttons when they are authorization-sensitive
- first-class controls for deferred V Forge domains that are not yet admitted into first-pass scope

### Rule
If a button should not exist doctrinally, it should not exist visually.
Not even “temporarily.”

---

## Visibility Rules

The operator should be able to determine from the V Forge surfaces:
- what work units exist
- what state they are in
- which items are blocked, failed, partial, or return-required
- which items are release-sensitive
- when graph state is relevant
- when execution intelligence is only advisory
- when a finding is planning-relevant rather than execution-local

A surface that hides these distinctions is not a usable V Forge surface.

---

## Governance and Gating Rules in Surface Design

When an action depends on stronger discipline, the surface must show that posture.

This means:
- sensitive actions should be visibly differentiated
- states like blocked, awaiting authorization, rollback-active, or return-required should not be visually flattened into generic “pending” language
- the operator should not have to infer governance posture from tiny text hidden deep in a panel

The extension must not make unsafe action feel visually equivalent to ordinary inspection.

---

## Surface and Playbook Relationship

The V Forge extension surface should reinforce the playbook layer.

This means the operator surfaces should make it easy to follow:
- `playbooks/content-update-playbook.md`
- `playbooks/new-content-execution-playbook.md`
- `playbooks/release-execution-playbook.md`
- `playbooks/return-to-planning-playbook.md`

The operator surface should not force the operator into a workflow that contradicts the playbooks.
A playbook-compatible surface is stronger than a superficially slick but doctrine-breaking surface.

---

## Anti-Drift Rules

### 1. No planner-surface rule
Do not let V Forge extension surfaces act like planning dashboards.

### 2. No observatory-surface rule
Do not let V Forge extension surfaces impersonate VEDA ownership surfaces.

### 3. No chat-is-the-app rule
Do not make the chat panel the only real place where V Forge truth or action lives.

### 4. No hidden-governance rule
Do not present authorization-sensitive execution as casual routine action.

### 5. No graph-as-strategy-canvas rule
Do not let graph surfaces become speculative planning canvases.

### 6. No return-is-an-edge-case rule
Do not hide return-to-planning posture as though it were exceptional embarrassment.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:
- V Forge surfaces are execution surfaces, not planning surfaces
- the operator must see current truth before acting
- graph, release, findings, and return posture should be explicit
- authorization-sensitive actions need stronger visual and interaction discipline
- playbooks should align with the surface
- chat assists V Forge work but does not replace the real operator surfaces
- first-pass surface depth is intentionally uneven across surface types and that unevenness is part of the doctrine, not an omission

If an LLM could use this document to justify turning V Forge into a strategy board, a hidden release console, or a chat-only execution surface, this document is failing.

---

## Usage

This document should be used:
- when designing V Forge panels, views, and action locations inside the unified VS Code extension
- when deciding what V Forge information should be primary, secondary, or absent
- when checking whether a proposed V Forge surface weakens boundaries or governance posture
- when aligning extension implementation with the V Forge playbook layer

---

## Related Docs

- `../v-forge.md`
- `../schema-authority.md`
- `../operator-quickstart.md`
- `../operational-model.md`
- `../mcp-surface.md`
- `../content-lifecycle-workflow.md`
- `../release-lifecycle-workflow.md`
- `../content-graph-operations.md`
- `../execution-intelligence-operations.md`
- `../playbooks/content-update-playbook.md`
- `../playbooks/new-content-execution-playbook.md`
- `../playbooks/release-execution-playbook.md`
- `../playbooks/return-to-planning-playbook.md`
- `../../interfaces/extension-vscode-surface-architecture.md`
- `../../interfaces/operator-surface-interfaces.md`
- `../../interfaces/extension-governance-and-gating-model.md`
- `../../interfaces/extension-system-init-and-tool-surface-model.md`
