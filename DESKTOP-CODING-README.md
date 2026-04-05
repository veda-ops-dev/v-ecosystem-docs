# Desktop Coding Readme

## Purpose

This file tells developers what they must read before writing code for the V Ecosystem desktop application.

The desktop application is not a normal chat wrapper.
It is a governed operator surface for a multi-system ecosystem with real boundaries, real approval semantics, real anti-drift constraints, and a Tauri 2 desktop host.

If you code before reading the required docs, you will almost certainly build the wrong thing.

---

## Core Rule

Before coding, understand this:

- the LLM is powerful but bounded
- recommendation is not approval
- approval is not activation
- activation is not execution
- chat is not governance
- the right interaction panel is not the real app
- Project V, VEDA, and V Forge must remain visibly distinct
- doctrine is enforced partly by what the desktop application does **not** allow

If your implementation weakens any of those, stop and reread the docs.

---

## Must-Read Order Before Coding

Read these in order.
Do not skip ahead.

### 1. Ecosystem grounding

1. `C:\dev\v-ecosystem-docs\README.md`
2. `C:\dev\v-ecosystem-docs\ecosystem\v-ecosystem-overview.md`
3. `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
4. `C:\dev\v-ecosystem-docs\ecosystem\vocabulary.md`
5. `C:\dev\v-ecosystem-docs\ecosystem\decisions\ADR-011-tauri-2-desktop-is-the-operator-host.md`

These define what the ecosystem is, what the systems are, what words mean, and what the current operator host is.

---

### 2. Governance spine

6. `C:\dev\v-ecosystem-docs\governance\agent-operating-doctrine.md`
7. `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md`
8. `C:\dev\v-ecosystem-docs\governance\auth-and-actor-model.md`
9. `C:\dev\v-ecosystem-docs\governance\recommendation-packaging-doctrine.md`
10. `C:\dev\v-ecosystem-docs\governance\decision-continuity-doctrine.md`
11. `C:\dev\v-ecosystem-docs\governance\report-structure-and-required-fields.md`
12. `C:\dev\v-ecosystem-docs\governance\external-action-governance.md`

These define what governance means in this ecosystem.
If you do not understand these, you will mistake chat smoothness for permission.

---

### 3. Workflow spine

13. `C:\dev\v-ecosystem-docs\workflows\project-intake-workflow.md`
14. `C:\dev\v-ecosystem-docs\workflows\handoff-workflow.md`
15. `C:\dev\v-ecosystem-docs\workflows\maintenance-and-replanning-workflow.md`
16. `C:\dev\v-ecosystem-docs\workflows\launch-readiness-workflow.md`

These define when things are allowed to move and what transitions actually mean.

---

### 4. Core interfaces

17. `C:\dev\v-ecosystem-docs\interfaces\veda-to-project-v-signal-interface.md`
18. `C:\dev\v-ecosystem-docs\interfaces\project-v-to-v-forge-handoff-interface.md`
19. `C:\dev\v-ecosystem-docs\interfaces\v-forge-to-project-v-return-to-planning-interface.md`
20. `C:\dev\v-ecosystem-docs\interfaces\mcp-coordination-model.md`
21. `C:\dev\v-ecosystem-docs\interfaces\operator-surface-interfaces.md`

These define what crosses boundaries and what operator surfaces are supposed to do.

---

### 5. Desktop doctrine sequence (required before desktop code)

22. `C:\dev\v-ecosystem-docs\interfaces\runtime-sidecar-and-nerve-model.md`
23. `C:\dev\v-ecosystem-docs\interfaces\local-first-architecture.md`
24. `C:\dev\v-ecosystem-docs\interfaces\desktop-surface-architecture.md`
25. `C:\dev\v-ecosystem-docs\interfaces\desktop-implementation-architecture.md`
26. `C:\dev\v-ecosystem-docs\interfaces\desktop-llm-behavior-contract.md`
27. `C:\dev\v-ecosystem-docs\interfaces\desktop-governance-and-gating-model.md`
28. `C:\dev\v-ecosystem-docs\interfaces\desktop-state-and-context-model.md`
29. `C:\dev\v-ecosystem-docs\interfaces\desktop-human-llm-interaction-model.md`
30. `C:\dev\v-ecosystem-docs\interfaces\desktop-agent-orchestration-model.md`
31. `C:\dev\v-ecosystem-docs\interfaces\desktop-memory-and-continuity-model.md`
32. `C:\dev\v-ecosystem-docs\interfaces\desktop-system-init-and-tool-surface-model.md`
33. `C:\dev\v-ecosystem-docs\interfaces\desktop-tool-surface-implementation-design.md`
34. `C:\dev\v-ecosystem-docs\interfaces\desktop-transcript-persistence-design.md`
35. `C:\dev\v-ecosystem-docs\interfaces\desktop-task-lifecycle-implementation-design.md`

These desktop docs are the active desktop doctrine and implementation-companion spine.
Do not code the desktop application until you understand the active doctrine set.

---

## If You Are Working On Specific Areas

### If you are working on LLM interaction
Re-read:
- `desktop-llm-behavior-contract.md`
- `desktop-human-llm-interaction-model.md`
- `recommendation-packaging-doctrine.md`

### If you are working on approvals / gates / activation
Re-read:
- `desktop-governance-and-gating-model.md`
- `approval-and-escalation-model.md`
- `auth-and-actor-model.md`
- `launch-readiness-workflow.md`

### If you are working on state, context, or synchronization
Re-read:
- `desktop-state-and-context-model.md`
- `decision-continuity-doctrine.md`
- `report-structure-and-required-fields.md`

### If you are working on surfaces, panes, routing, and shell behavior
Re-read:
- `desktop-surface-architecture.md`
- `desktop-implementation-architecture.md`
- `operator-surface-interfaces.md`

### If you are working on orchestration or delegated runtime work
Re-read:
- `desktop-agent-orchestration-model.md`
- `desktop-governance-and-gating-model.md`
- `agent-operating-doctrine.md`

### If you are working on memory, continuity, compaction, or transcript handling
Re-read:
- `desktop-memory-and-continuity-model.md`
- `desktop-state-and-context-model.md`
- `desktop-transcript-persistence-design.md`
- `decision-continuity-doctrine.md`

### If you are working on session bootstrap, init prompts, or tool-surface assembly
Re-read:
- `desktop-system-init-and-tool-surface-model.md`
- `desktop-tool-surface-implementation-design.md`
- `desktop-llm-behavior-contract.md`
- `mcp-coordination-model.md`

### If you are working on cross-system reads or tool flows
Re-read:
- `cross-system-boundaries.md`
- `mcp-coordination-model.md`
- the three workflow docs above
- the three core interface docs above

---

## Non-Negotiable Coding Rules

### 1. Do not make the right interaction panel the real app
The interaction panel is a support surface.
Canonical state lives in governed surfaces, explicit stores, and canonical backend records.

### 2. Do not let chat prose become governance
No conversational approval.
No `looks good` shortcuts.
No hidden activation from LLM cards.

### 3. Do not let recommendations mutate state
Recommendations are inert.
Approval Request Packages are inert.
Approval must be persisted.
Activation must be separate.

### 4. Do not put the wrong actions in the wrong surfaces
If a control should not exist in a surface, do not add it temporarily.
Temporary shortcuts become permanent doctrine leaks.

### 5. Do not infer too much from user intent
`The model knows what I meant` is not a system rule.
Explicit framing matters.
Current system matters.
Workflow stage matters.
Class A conversational framing does not change the current system. Only an explicit operator system switch does that.

### 6. Do not build around convenience if it weakens boundaries
If the easiest implementation path collapses governance, the easy path is wrong.

### 7. Do not duplicate gate logic everywhere
Approval and activation logic must be centralized.
Do not let multiple surfaces or commands each invent their own gate rules.

### 8. Do not let orchestration become hidden governance
Delegation does not create permission.
A coordinator is not an approval source.
A specialist worker must not become a secret mutation path.

### 9. Do not let memory become fake authority
Working memory, durable memory, transcripts, compaction products, and worker findings are continuity artifacts.
They are not canonical decisions, approval records, evidence records, or system truth.

### 10. Do not let compaction hide protected context
If compaction drops current-system posture, approval state, decision continuity context, evidence basis markers, or other protected context, the runtime is wrong even if it still feels smooth.

### 11. Do not let local SQLite become truth
SQLite is a support-state layer.
It is not the canonical source of Project V, VEDA, or V Forge truth.
If the local layer becomes easier to trust than the backend systems, stop and fix the architecture.

### 12. Do not blur frontend, sidecar, and backend responsibilities
The frontend is not the hidden runtime engine.
The sidecar is not the system of record.
The backend is not a UI state store.
If responsibilities start bleeding together, stop and resolve the boundary intentionally.

---

## First Implementation Priority

Build in this order:

1. project/session scope
2. state/context spine
3. system init and session tool-surface assembly
4. typed output validation and rendering
5. center review/detail surfaces
6. approval pipeline
7. memory and continuity safeguards
8. workflow-specific flows
9. orchestration and delegated runtime features

Do not start with pretty UI.
Do not start with clever agent behavior.
Build the spine first.

---

## Stop-and-Check Conditions

Stop coding and go back to the docs if you find yourself wanting to:

- add an Approve button directly to an LLM output card
- let a tree item call a mutating API directly
- store governance state in chat history
- infer mode from conversation topic without explicit framing
- make VEDA create planning records
- make Project V execute work
- make V Forge alter planning decisions
- skip persisted approval because the operator is right there
- merge review, approval, and activation because it feels smoother
- let memory records behave like decisions or approvals
- treat transcripts as canonical state
- let compaction silently remove protected context
- let SQLite become the easier truth source
- let a delegated worker mutate governed state without the existing gate path
- hide orchestration state because the UI feels cleaner without it
- bypass the sidecar/runtime boundary because IPC feels annoying

If any of those feel tempting, you are drifting.

---

## Practical Reminder

The desktop application is supposed to be:

- powerful
- explicit
- bounded
- governed
- usable

Not:

- magical
- chat-first
- shortcut-heavy
- co-pilot theater
- governance by vibes

Code accordingly.
