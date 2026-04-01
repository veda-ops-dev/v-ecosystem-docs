# Extension Coding Readme

## Purpose

This file tells developers what they must read before writing code for the V Ecosystem VS Code extension.

The extension is not a normal chat wrapper.
It is a governed operator surface for a multi-system ecosystem with real boundaries, real approval semantics, and real anti-drift constraints.

If you code before reading the required docs, you will almost certainly build the wrong thing.

---

## Core Rule

Before coding, understand this:

- the LLM is powerful but bounded
- recommendation is not approval
- approval is not activation
- activation is not execution
- chat is not governance
- the LLM sidebar is not the real app
- Project V, VEDA, and V Forge must remain visibly distinct
- doctrine is enforced partly by what the extension does **not** allow

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

These define what the ecosystem is, what the systems are, and what words mean.

---

### 2. Governance spine

5. `C:\dev\v-ecosystem-docs\governance\agent-operating-doctrine.md`
6. `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md`
7. `C:\dev\v-ecosystem-docs\governance\auth-and-actor-model.md`
8. `C:\dev\v-ecosystem-docs\governance\recommendation-packaging-doctrine.md`
9. `C:\dev\v-ecosystem-docs\governance\decision-continuity-doctrine.md`
10. `C:\dev\v-ecosystem-docs\governance\report-structure-and-required-fields.md`
11. `C:\dev\v-ecosystem-docs\governance\external-action-governance.md`

These define what governance means in this ecosystem.
If you do not understand these, you will mistake chat smoothness for permission.

---

### 3. Workflow spine

12. `C:\dev\v-ecosystem-docs\workflows\project-intake-workflow.md`
13. `C:\dev\v-ecosystem-docs\workflows\handoff-workflow.md`
14. `C:\dev\v-ecosystem-docs\workflows\maintenance-and-replanning-workflow.md`
15. `C:\dev\v-ecosystem-docs\workflows\launch-readiness-workflow.md`

These define when things are allowed to move and what transitions actually mean.

---

### 4. Core interfaces

16. `C:\dev\v-ecosystem-docs\interfaces\veda-to-project-v-signal-interface.md`
17. `C:\dev\v-ecosystem-docs\interfaces\project-v-to-v-forge-handoff-interface.md`
18. `C:\dev\v-ecosystem-docs\interfaces\v-forge-to-project-v-return-to-planning-interface.md`
19. `C:\dev\v-ecosystem-docs\interfaces\mcp-coordination-model.md`
20. `C:\dev\v-ecosystem-docs\interfaces\operator-surface-interfaces.md`

These define what crosses boundaries and what operator surfaces are supposed to do.

---

### 5. Extension doctrine sequence (required before extension code)

21. `C:\dev\v-ecosystem-docs\interfaces\extension-llm-behavior-contract.md`
22. `C:\dev\v-ecosystem-docs\interfaces\extension-governance-and-gating-model.md`
23. `C:\dev\v-ecosystem-docs\interfaces\extension-state-and-context-model.md`
24. `C:\dev\v-ecosystem-docs\interfaces\extension-human-llm-interaction-model.md`
25. `C:\dev\v-ecosystem-docs\interfaces\extension-vscode-surface-architecture.md`
26. `C:\dev\v-ecosystem-docs\interfaces\extension-implementation-architecture.md`
27. `C:\dev\v-ecosystem-docs\interfaces\extension-agent-orchestration-model.md`
28. `C:\dev\v-ecosystem-docs\interfaces\extension-memory-and-continuity-model.md`
29. `C:\dev\v-ecosystem-docs\interfaces\extension-system-init-and-tool-surface-model.md`

These extension docs are the extension doctrine spine.
Do not code the extension until you understand the active doctrine set.

---

## If You Are Working On Specific Areas

### If you are working on LLM interaction
Re-read:
- `extension-llm-behavior-contract.md`
- `extension-human-llm-interaction-model.md`
- `recommendation-packaging-doctrine.md`

### If you are working on approvals / gates / activation
Re-read:
- `extension-governance-and-gating-model.md`
- `approval-and-escalation-model.md`
- `auth-and-actor-model.md`
- `launch-readiness-workflow.md`

### If you are working on state, context, or synchronization
Re-read:
- `extension-state-and-context-model.md`
- `decision-continuity-doctrine.md`
- `report-structure-and-required-fields.md`

### If you are working on panels, views, and commands
Re-read:
- `extension-vscode-surface-architecture.md`
- `extension-implementation-architecture.md`
- `operator-surface-interfaces.md`

### If you are working on orchestration or delegated runtime work
Re-read:
- `extension-agent-orchestration-model.md`
- `extension-governance-and-gating-model.md`
- `agent-operating-doctrine.md`

### If you are working on memory, continuity, or compaction
Re-read:
- `extension-memory-and-continuity-model.md`
- `extension-state-and-context-model.md`
- `decision-continuity-doctrine.md`

### If you are working on session bootstrap, init prompts, or tool-surface assembly
Re-read:
- `extension-system-init-and-tool-surface-model.md`
- `extension-llm-behavior-contract.md`
- `mcp-coordination-model.md`

### If you are working on cross-system reads or tool flows
Re-read:
- `cross-system-boundaries.md`
- `mcp-coordination-model.md`
- the three workflow docs above
- the three core interface docs above

---

## Non-Negotiable Coding Rules

### 1. Do not make the LLM panel the real app
The LLM sidebar is a support surface.
Canonical state lives in governed surfaces and explicit stores.

### 2. Do not let chat prose become governance
No conversational approval.
No “looks good” shortcuts.
No hidden activation from LLM cards.

### 3. Do not let recommendations mutate state
Recommendations are inert.
Approval Request Packages are inert.
Approval must be persisted.
Activation must be separate.

### 4. Do not put the wrong actions in the wrong surfaces
If a button should not exist in a surface, do not add it “temporarily.”
Temporary shortcuts become permanent doctrine leaks.

### 5. Do not infer too much from user intent
“The model knows what I meant” is not a system rule.
Explicit framing matters.
Current system matters.
Workflow stage matters.
Class A conversational framing does not change the current system. Only an explicit operator system switch does that.

### 6. Do not build around convenience if it weakens boundaries
If the easiest implementation path collapses governance, the easy path is wrong.

### 7. Do not duplicate gate logic everywhere
Approval and activation logic must be centralized.
Do not let multiple panels or commands each invent their own gate rules.

### 8. Do not let orchestration become hidden governance
Delegation does not create permission.
A coordinator is not an approval source.
A specialist worker must not become a secret mutation path.

### 9. Do not let memory become fake authority
Working memory, durable memory, transcripts, compaction products, and worker findings are continuity artifacts.
They are not canonical decisions, approval records, evidence records, or system truth.

### 10. Do not let compaction hide protected context
If compaction drops current-system posture, approval state, decision continuity context, evidence basis markers, or other protected context, the runtime is wrong even if it still feels smooth.

---

## First Implementation Priority

Build in this order:

1. project/session scope
2. state/context spine
3. system init and session tool-surface assembly
4. typed output validation and rendering
5. detail panels
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
- skip persisted approval because “the operator is right there”
- merge review, approval, and activation because it feels smoother
- let memory records behave like decisions or approvals
- treat transcripts as canonical state
- let compaction silently remove protected context
- let a delegated worker mutate governed state without the existing gate path
- hide orchestration state because the UI feels cleaner without it

If any of those feel tempting, you are drifting.

---

## Practical Reminder

The extension is supposed to be:

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
