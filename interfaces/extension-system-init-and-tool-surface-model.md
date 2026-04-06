# Extension System Init and Tool Surface Model

## Status
Superseded by `desktop-system-init-and-tool-surface-model.md`

This document reflects the legacy VS Code extension host model.
The Tauri 2 desktop application defined in ADR-011 is now the primary operator host.
Use `desktop-system-init-and-tool-surface-model.md` for active doctrine.

## Purpose

This document defines how the V Ecosystem VS Code extension constructs the system init message and assembles the session tool surface.

It exists to answer:

```text
What context must be assembled at session start, what must the LLM be told about its role and constraints, how is the active tool surface built and filtered for the session, and how does the extension expose only the context and tools the runtime is currently entitled to use?
```

This is a Tier 1 ecosystem authority document for the extension/runtime layer.

---

## Scope

This document governs:

- system init message assembly posture
- session-start context assembly
- the relationship between canonical loaded state and runtime distillation
- session refresh posture
- session tool-surface assembly
- tool filtering by current system, scope, and action posture
- referenced-system read posture in the active session
- absent-affordance enforcement at runtime
- visibility rules for loaded context and active tools
- anti-drift rules that prevent the runtime from exposing tools or context it should not expose

This document assumes the active binding of:
- `extension-llm-behavior-contract.md`
- `extension-governance-and-gating-model.md`
- `extension-state-and-context-model.md`
- `extension-agent-orchestration-model.md`
- `extension-memory-and-continuity-model.md`
- `../ecosystem/decisions/ADR-004-mcp-tools-are-thin-wrappers.md`
- `../ecosystem/decisions/ADR-005-session-token-model-for-project-scope.md`
- `../ecosystem/decisions/ADR-009-no-direct-database-access.md`

---

## Out of Scope

This document does not define:

- exact MCP tool schemas for each system
- exact backend API route contracts
- exact prompt wording templates
- exact webview UI rendering details
- exact implementation classes or storage engines
- system-specific tool lists beyond posture rules

Those belong in implementation docs or system-specific MCP docs.

---

## System

- interfaces

---

## Core Rule

The LLM must only receive the context and tool surface it is currently entitled to use.

The runtime must assemble the session basis deliberately.
It must not rely on ad-hoc prompt stuffing, topic drift, or convenience exposure of tools that happen to exist.

If the extension gives the LLM the wrong context or the wrong tools, every later governance rule is already weakened.

---

## System Init Message Definition

The system init message is the structured runtime context assembled at session start or session refresh to communicate the active session basis to the LLM.

It is not just a static system prompt.
It is a runtime assembly product that reflects:
- active project scope
- current system posture
- current workflow context where applicable
- admitted loaded context
- admitted continuity artifacts allowed to participate
- current tool surface
- behavior and governance constraints relevant to the session

The init message is where doctrine becomes runtime behavior.
If it is assembled casually, the rest of the extension cannot be trusted to behave consistently.

The mechanical ordered assembly, filtering, publication, and refresh of the active tool surface are defined in `extension-tool-surface-implementation-design.md`.
That companion operationalizes the posture defined here.

---

## Session Init Assembly Rule

At session start, the extension must construct the runtime basis in a deliberate sequence.

At minimum, the sequence must establish:

1. **Project scope**
   The session must be bound to the selected project through the governed session-token model.

2. **Current system posture**
   The runtime must know whether the active activity is governed by Project V, VEDA, or V Forge.

3. **Workflow and gating context where applicable**
   Relevant workflow stage, active approval state, and blocking conditions must be known before higher-order behavior is exposed.

4. **Decision and evidence basis where applicable**
   Required continuity and evidence context must be loaded or explicitly marked absent.

5. **Admitted continuity artifacts**
   Only continuity artifacts admitted under the memory and continuity doctrine may be brought forward.
   Admission is not automatic just because an artifact exists.

6. **Session tool surface**
   The runtime must assemble the filtered set of MCP tools and related capabilities that the LLM may actually use.

7. **Behavior and constraint distillation**
   The LLM must receive the role, limits, and current session basis in a compact but explicit form.

This sequence may be refreshed when session conditions change.
It must not be reconstructed from chat drift alone.

---

## Canonical Load vs Runtime Distillation Rule

The runtime may distill loaded canonical state into a compact init message representation.

That distillation is allowed only if:
- the underlying canonical records were actually loaded
- the distillation remains faithful to the loaded state
- the runtime can show the operator what was loaded
- the distillation does not replace the governing record

The init message may summarize.
It must not invent or imply canonical facts that were never loaded.

---

## Required Init Message Categories

The system init message must communicate, in a bounded form, the categories needed for correct runtime behavior.

At minimum, these categories are required where applicable:

### 1. Role and posture
What kind of participant the LLM is in this session and what authority limits apply.

### 2. Scope and current system
The active project scope and the system governing the current activity.

### 3. Workflow and gating posture
What stage the active work is in, what approvals are active or required, and whether blocking conditions exist.

### 4. Decision and evidence context summary
A bounded summary of loaded decision continuity and evidence basis relevant to the current work.

### 5. Continuity artifacts admitted to the session
The admitted memory/continuity items allowed to participate, with the non-authority boundary preserved.

### 6. Tool surface summary
What tools are available, in what posture, and what kinds of actions are not admitted.

### 7. Runtime warnings or protected-context notes
Any conditions the LLM must not ignore, such as stale evidence basis, unresolved approval state, or continuity caveats.

---

## Session Tool Surface Definition

The session tool surface is the governed set of tools and runtime capabilities the LLM may access in the current session.

It is assembled from admitted MCP surfaces and filtered according to:
- project scope
- current system posture
- governance and action-class rules
- referenced-system read posture where allowed
- runtime mode or flow constraints where admitted

The session tool surface must be treated as a deliberate assembly product.
It must not simply mirror every tool the runtime could theoretically access.

The mechanical registry, filtering stages, delegated narrowing model, execution gate, and refresh mechanics for the active surface are defined in `extension-tool-surface-implementation-design.md`.

---

## Tool Surface Assembly Rule

The runtime must assemble the session tool surface through explicit filtering rather than by convenience exposure.

At minimum, the assembly logic must consider:

### 1. Project scope binding
Every project-scoped tool must operate under the active session token and its bound project scope.

### 2. Current system relevance
Tools belonging to the current governing system are primary candidates for admission.

### 3. Referenced-system posture
Where cross-system reading is doctrinally allowed, referenced-system tools may be admitted in bounded read posture only.

### 4. Action-class posture
Mutation-capable tools must remain subordinate to the existing governance and gating model.

### 5. Runtime task posture
Delegated workers or bounded flows may receive narrower tool surfaces than the parent session.

If the runtime cannot explain why a tool is available in the session, that tool should not be in the session tool surface.

The implementation must enforce these filters structurally before the LLM reasons over the active surface, not merely at the moment of tool execution.

---

## Current System Tool Priority Rule

The current system governs the primary tool posture.

That means:
- the current system's admitted tools are the primary working surface
- referenced-system tools, where admitted, remain secondary and bounded
- non-relevant system tools should not be casually exposed just because they exist

The LLM should not be forced to infer the correct working surface from an over-broad tool list.
The runtime should make the correct working surface obvious by construction.

---

## Referenced-System Read Rule

Cross-system reading is not forbidden when doctrine already allows it.
But referenced-system reading does not transfer ownership.

When the current system requires bounded context from another system, the runtime may admit a narrow referenced-system read posture.

Examples:
- Project V session reading bounded VEDA signal package context
- V Forge session reading bounded VEDA signal relevant to execution intelligence
- V Forge session reading bounded Project V handoff context relevant to active execution

Referenced-system read posture must remain:
- bounded
- visible
- non-owning
- non-mutating unless an explicit ecosystem interface doc and separately governed path authorize more than reading

Referenced-system read posture must not become an implementation excuse for casual cross-system mutation.

The tool-surface implementation companion must enforce referenced-system posture as a narrower runtime exposure state rather than as equal membership in the active current-system surface.

---

## Absent-Affordance Runtime Rule

The extension must enforce absent affordances not just in the visible UI, but in the runtime tool surface presented to the LLM.

If the LLM should not perform or even propose a direct tool path in the current session posture, the runtime should avoid exposing that path as casually available.

This means the wrong tools must be absent from the LLM's effective tool surface, not just hidden behind a nicer interface.

A runtime that exposes too many tools and relies on the LLM to choose well is not actually bounded.

Structural filtering in `extension-tool-surface-implementation-design.md` exists specifically to make this rule enforceable rather than aspirational.

---

## Delegated Tool Surface Narrowing Rule

Delegated subtasks must receive a narrower tool surface than or equal to the parent session surface.

A delegated worker must not receive broader authority than the parent session.

Delegated tool surfaces should be filtered by:
- subtask objective
- current-system posture
- read/write posture needed for the subtask
- action-class restrictions
- explicit governance rules for delegated work

Delegation may reduce tool exposure.
It must not expand it.

The implementation companion must model delegated narrowing as an explicit filtering stage, not as a best-effort side effect.

---

## Visibility Rule

The operator must be able to determine, where relevant:
- what current system governs the session
- what major context categories were loaded
- whether continuity artifacts were brought forward
- whether referenced-system context is active
- what general tool posture is active
- when the session basis has been refreshed or changed materially

The runtime does not need to dump raw prompt internals constantly.
But the operator must not be left guessing what basis the model is currently operating on.

---

## Refresh Rule

The runtime must refresh the session basis when relevant conditions change materially.

Examples include:
- project scope change
- current-system change
- workflow-stage change that affects gating or context needs
- approval-state change
- evidence-basis refresh or invalidation
- meaningful continuity change after compaction or resume
- delegated work completion that changes the admitted continuity set

A stale init basis must not be allowed to linger just because the chat session is still open.

A material active-tool-surface rebuild counts as a session-basis change and may require bounded system-init re-assembly.

---

## Refresh Implementation Posture

A session refresh must be deliberate, not ad hoc.

The runtime may implement refresh through a bounded full re-init or a bounded delta-style refresh, but only if all of the following remain true:
- the resulting session basis is explicit and reviewable
- protected context remains preserved
- the operator can tell that a material refresh occurred
- stale prior basis does not continue to operate invisibly beside the refreshed basis

A refresh must not be implemented as casual hidden prompt injection that leaves the operator unable to tell what changed.

When a material refresh occurs, the runtime must:
- surface that the session basis changed
- identify the categories that changed
- ensure the active tool posture and admitted continuity posture are recomputed as needed

The implementation companion defines the rebuild and invalidation mechanics that support this refresh posture.

---

## Cross-System Session Start Posture

The default session start posture is one current system with optionally admitted referenced-system context.

When referenced-system context is active at session start:
- the current system must still remain primary and explicit
- referenced-system context must be labeled as referenced, not owned
- referenced-system tools must remain secondary and bounded in the session tool posture
- the init message must not present multi-system visibility as merged system ownership

A session may be cross-system aware.
It must not become cross-system indistinct.

---

## Anti-Drift Rules

### 1. No ad-hoc prompt stuffing rule
The init message must be deliberately assembled, not casually accumulated.

### 2. No tool overexposure rule
The runtime must not expose tools beyond the session's actual admitted posture just because the implementation can reach them.

### 3. No cross-system ownership blur rule
Referenced-system tools and context do not transfer ownership or make another system's truth local property.

### 4. No stale-basis confidence rule
The runtime must not behave as though an old session basis remains correct after a material context change.

### 5. No hidden continuity injection rule
Continuity artifacts brought into the session must remain within the memory doctrine and not be silently treated as canonical state.

### 6. No delegation-based privilege expansion rule
Delegated workers must not gain broader tool access than the parent session or broader authority than the active governance posture allows.

---

## Relationship to Other Extension Docs

This doc defines how the session basis and tool surface are assembled.

It relies on:
- `extension-llm-behavior-contract.md` for bounded model posture
- `extension-governance-and-gating-model.md` for action-class and approval rules
- `extension-state-and-context-model.md` for what must remain visible and current
- `extension-agent-orchestration-model.md` for delegated-runtime posture
- `extension-memory-and-continuity-model.md` for what continuity artifacts may participate
- `extension-tool-surface-implementation-design.md` for the mechanical filtering, publication, execution-gate, and refresh model that enforces the posture defined here

This doc must not be used to bury governance decisions in prompt engineering.
It exists to make the admitted runtime surface explicit and controlled.

---

## Implementation Direction

Implementation should make session assembly and tool exposure:
- deliberate
- bounded
- refreshable
- visible enough for review
- subordinate to canonical records and governance posture

A smart runtime is valuable.
A runtime that feels smart because it was given too much context and too many tools is not compatible with this ecosystem.
