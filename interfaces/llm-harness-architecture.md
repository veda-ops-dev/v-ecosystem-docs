# LLM Harness Architecture

## Purpose

This document names and connects the existing doctrine that, taken together, constitutes the LLM harness of the V Ecosystem.

It exists to answer:

```text
What is the LLM harness in the V Ecosystem, what disciplines compose it, where does each discipline already live in governed doctrine, what does VedaOps mean by context engineering and harness engineering, and how do these pieces fit together so that the LLM can reason broadly while only acting through governed system pathways?
```

This is a Tier 1 ecosystem authority document. It is an architecture and index document. It does not introduce new behavioral rules, new state categories, new memory classes, new compaction mechanics, new command classes, new MCP coordination posture, new approval classes, or new agent posture. Each of those already lives in a governing doc and remains the authority for its area.

---

## Scope

This document governs:

- the VedaOps definitions of context engineering and harness engineering
- the identification of the LLM harness as a coherent assembly composed of existing doctrine
- the mapping between harness disciplines and the docs that already govern them
- the relationship between the harness and the four-system ecosystem model
- the explicit framing of mental alignment between LLM working belief and canonical system state

---

## Out of Scope

This document does not relocate authority from the component docs it indexes. If it conflicts with any of them, this document is wrong.

---

## System

- interfaces

---

## Core Rule

The LLM harness exists to make the V Ecosystem's system boundaries structurally enforced rather than behaviorally trusted.

The LLM may reason broadly, but may only act through governed system pathways.

The context window is not a truth store. Canonical truth remains owned by the proper system of record — Project V, VEDA, VEDA Strategy, or V Forge — under the schema and ownership posture defined in `../ecosystem/db-posture.md` and `../ecosystem/cross-system-boundaries.md`.

---

## VedaOps Definitions

### Context Engineering

Context engineering in VedaOps is the discipline of deciding, per session and per turn, what governed state, evidence, decisions, derived intelligence, and continuity artifacts the LLM is allowed to see, in what form, with what freshness, and with what authority weight, such that no reasoning step rests on hidden, inferred, stale, or non-canonical context.

It is not transcript management. It is not chat-history summarization.

The authority for this discipline is `desktop-state-and-context-model.md`, with freshness and refresh behavior governed by `desktop-invalidation-and-refresh-matrix.md` and `../governance/invalidation-and-supersedence-doctrine.md`, and continuity-context posture governed by `desktop-memory-and-continuity-model.md`.

### Harness Engineering

Harness engineering in VedaOps is the discipline of designing the runtime control layer around the LLM — system init, tool surfaces, command dispatch, context assembly, memory and continuity behavior, gate routing, approval mechanics, and execution constraints — such that the LLM can reason fully but cannot mutate state, cross system boundaries, or commit governed actions except through structurally enforced governed paths.

It is distinct from:

- **prompt engineering**, which concerns only the text sent on a single turn
- **architecture doctrine**, which defines what truths exist and who owns them
- **workflow design**, which defines stage sequences and approval gates as authority-level rules

Harness engineering takes architecture and workflow as given and builds the runtime that respects them.

---

## Harness Components

The harness in VedaOps is a single discipline composed of the following component areas, each governed by an existing doc.

| Component area | Authority |
|---|---|
| LLM posture and reasoning-vs-authority distinction | `desktop-llm-behavior-contract.md` |
| Agent operating posture across the ecosystem | `../governance/agent-operating-doctrine.md` |
| Session initialization and tool-surface exposure | `desktop-system-init-and-tool-surface-model.md` |
| Operator interaction surface and slash-command dispatch | `desktop-interaction-surface-and-command-dispatch.md` |
| Command classes and command-to-system mapping | `command-registry-and-command-classification-doctrine.md` |
| MCP tool surface and cross-system coordination | `mcp-coordination-model.md` |
| Delegated runtime roles and specialist participation | `desktop-agent-orchestration-model.md` |
| Context categories, visibility, freshness | `desktop-state-and-context-model.md` |
| Memory classes and continuity-non-authority posture | `desktop-memory-and-continuity-model.md` |
| Compaction mechanics under continuity doctrine | `desktop-compaction-implementation-design.md` |
| Gate routing and gate enforcement | `desktop-governance-and-gating-model.md` |
| Approval classes, escalation, and seam mechanics | `../governance/approval-and-escalation-model.md`, `../governance/approval-mechanics-seam-model.md` |
| Decision continuity and supersedence | `../governance/decision-continuity-doctrine.md`, `../governance/invalidation-and-supersedence-doctrine.md` |

The harness is the assembly. A change that affects more than one of these areas is a harness-level change and should be designed against this assembly view, not against one component in isolation.

---

## Context Engineering in VedaOps

Context engineering in VedaOps proceeds from the rules already established in `desktop-state-and-context-model.md`, `desktop-memory-and-continuity-model.md`, and `desktop-invalidation-and-refresh-matrix.md`. This document adds no rules; it states only the assembly-level posture.

### Reading aid: context source classes

As a reading aid for harness work, every entry in the LLM's working window can be read as belonging to one of these classes. This is an assembly-level lens, not new doctrine; the binding rules for each kind of source live in the docs cited above.

- **Canonical** — a record owned by one of the four systems under its schema (`project_v.*`, `veda.*`, `veda_strategy.*`, `v_forge.*`)
- **Referenced** — a canonical record from another system, loaded read-only through a governed interface
- **Derived** — a VEDA Strategy output, loaded with its derivation basis intact
- **Continuity** — a runtime continuity artifact, explicitly non-authority per `desktop-memory-and-continuity-model.md`
- **Operator** — input or framing supplied by the operator in the current session
- **Inert LLM output** — a typed output the LLM has produced this session that has not yet been admitted to a canonical system

Anything that would not fit one of these readings is a sign the harness is loading something it should not.

### Assembly-level posture

- Context loading is a governance act, not a convenience act. Cross-system boundary rules from `../ecosystem/cross-system-boundaries.md` apply to context as strictly as to data.
- Cross-system referenced context is loaded as referenced, never as owned.
- Stale, uncertain, or incomplete context is surfaced as such per `desktop-state-and-context-model.md`, never silently dropped.
- Before any approval-sensitive turn, context is refreshed against canonical state under the rules in `desktop-state-and-context-model.md` and `desktop-invalidation-and-refresh-matrix.md`. Continuity is never sufficient by itself for a governed transition.

---

## Relationship to the Four-System Model

The harness does not own truth. The four systems own truth. The harness mediates the LLM's interaction with all four:

- **Project V** — planning truth in `project_v.*`. Planning-affecting actions route through Project V's governed surfaces, never inline.
- **VEDA** — observatory truth in `veda.*`. Records are presented with provenance and timestamp intact; the harness does not allow paraphrasing that erases source attribution.
- **VEDA Strategy** — derived strategic intelligence in `veda_strategy.*`. The harness preserves derivation basis as protected context per `desktop-memory-and-continuity-model.md`. A strategic signal whose derivation basis has been compacted away is no longer a signal.
- **V Forge** — execution truth in `v_forge.*`, including the content graph. Execution-affecting actions route through V Forge's governed surfaces; execution-side research remains bounded to approved-handoff support per `../v-forge/v-forge.md`.

There is no fifth zone owned by the harness or the LLM. There is no agent memory layer that escapes the four-system map. Anything that would be a fifth zone is shadow ownership and is refused at the harness level.

The harness is also not a peer system. Per `../ecosystem/v-ecosystem-overview.md`, the desktop application — the primary instantiation of the harness — is an operator-facing governance and runtime layer, not a peer to the four core systems.

---

## Mental Alignment and Canonical State

Mental alignment is the explicit framing that the LLM's working belief is itself a thing the harness keeps current, not a side effect of context loading.

For VedaOps, mental alignment means:

- the LLM's belief about the current state of any governed concept must, at every turn that influences a governed output, match the canonical record from the system that owns that truth
- when the LLM cannot verify alignment, it says so explicitly per the uncertainty-handling rules in `desktop-llm-behavior-contract.md` rather than reason from assumption
- alignment is re-established at compact boundaries and before approval-sensitive turns, not only at session start
- decision continuity per `../governance/decision-continuity-doctrine.md` and ADR supersedence per `../governance/invalidation-and-supersedence-doctrine.md` are part of what must be re-checked, not assumed-stable across a long session

Mental alignment is not a new discipline. It is a name for what the existing context, memory, and invalidation docs already require when read together. Naming it makes the requirement legible to LLMs and operators who would otherwise treat session continuity as if it were canonical truth.

The supporting rule is short:

> The context window is not a truth store. Canonical truth remains owned by the proper system of record.

---

## Relationship to Compaction, Memory, and Continuity

Compaction, memory classes, transcript posture, and continuity-non-authority posture are governed by `desktop-memory-and-continuity-model.md`, with mechanics in `desktop-compaction-implementation-design.md`. This document adds no rules. The assembly-level consequence:

- A continuity artifact, including any compaction product, is never authority. The harness structurally prevents a compacted summary from being treated as a decision record, an approval record, an evidence record, or canonical system state.
- Protected-context categories under `desktop-memory-and-continuity-model.md` are the harness's primary defense against post-compaction drift. Whether the existing list is exhaustive for VEDA Strategy derivation basis, observation provenance, approval event references, and ADR supersedence status is a question for that doc, not this one.
- Continuity does not refresh canonical state. Canonical state is refreshed by reading canonical records through governed interfaces.

---

## Relationship to Command Dispatch, MCP, and Approval Gating

Command dispatch (`desktop-interaction-surface-and-command-dispatch.md`, `command-registry-and-command-classification-doctrine.md`), MCP tool surfaces (`mcp-coordination-model.md`), and gate enforcement (`desktop-governance-and-gating-model.md`) are the structural mechanisms by which harness rules become enforceable rather than aspirational.

The assembly-level posture:

- A governance-sensitive action — Class B and Class C events under `../governance/approval-mechanics-seam-model.md` — completes through the governed gate surfaces. The interaction surface, the command layer, and MCP tools are dispatch and access mechanisms; they are not approval surfaces.
- Tool availability is bounded by current system, session scope, and gate posture per the command classification doctrine. Reasoning about a tool is not the same as having access to it.
- Cross-system reach through MCP does not transfer ownership per cross-system Rule 5 in `../ecosystem/cross-system-boundaries.md`.
- Delegated runtime roles inherit the parent session's scope and approval posture per `desktop-agent-orchestration-model.md` and `../governance/agent-operating-doctrine.md`. Delegation is not a way to widen authority.

---

## Human-In-The-Loop Principle

The harness exists in service of human-in-the-loop governance, not in tension with it. Per `../ecosystem/v-ecosystem-overview.md` and every system identity doc, human review remains required for project creation, approvals, external paid actions, significant mutations, launch decisions, and ecosystem doctrine changes. The harness's job is to make those choke points structurally unavoidable, not advisory.

If it is easy for an LLM to bypass a gate by phrasing things differently, the harness is failing.

---

## Usage

This document should be used:

- as the orientation doc for any LLM session, contributor, or auditor approaching VedaOps's runtime posture as a whole
- as the index for which doc governs which harness component
- as the reference when proposing a change that touches more than one harness component
- as the boundary check when evaluating a proposed harness behavior against the four-system ecosystem model

It is not the place to look for binding rules in any component area. Those live in the component-area docs.

---

## Related Docs

- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/db-posture.md`
- `../project-v/project-v.md`
- `../veda/veda.md`
- `../veda-strategy/veda-strategy.md`
- `../v-forge/v-forge.md`
- `desktop-llm-behavior-contract.md`
- `desktop-state-and-context-model.md`
- `desktop-memory-and-continuity-model.md`
- `desktop-compaction-implementation-design.md`
- `desktop-system-init-and-tool-surface-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-governance-and-gating-model.md`
- `desktop-interaction-surface-and-command-dispatch.md`
- `desktop-invalidation-and-refresh-matrix.md`
- `command-registry-and-command-classification-doctrine.md`
- `mcp-coordination-model.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/invalidation-and-supersedence-doctrine.md`
- `../transition-steward/transition-plan.md`
