# Agent Orchestration Design Note

## Purpose

This document explains the practical agent-orchestration pattern observed in the external `coordinatorMode.ts` reference and translates the useful parts into V Forge terms.

It exists to answer:

```text
What useful orchestration pattern does the external coordinator-mode implementation demonstrate, how does it work at a code level, what supporting runtime pieces does it require, and how should V Forge interpret it without drifting into planning ownership, signal ownership, or uncontrolled autonomy?
```

This is a V Forge design note.
It is implementation-shaping input for the V Forge operability wave.
It is not core identity doctrine and it does not override V Forge invariants.

---

## Scope

This document covers:

- the orchestration pattern shown in the external `coordinatorMode.ts` reference
- the main code-level mechanisms that make that pattern work
- the runtime dependencies and surrounding primitives required for the pattern to function
- the parts of the pattern that appear useful for V Forge
- the parts of the pattern that would require adaptation or stronger governance in V Forge
- the recommended interpretation posture for future V Forge MCP and operator-surface work

---

## Out of Scope

This document does not define:

- the canonical V Forge MCP tool surface
- final V Forge operator-surface behavior
- final executor task taxonomy
- final approval matrices for orchestrated execution
- final temporary-workspace rules
- final task-state schema
- final notification transport format

Those belong in later V Forge implementation-build-spec docs.

---

## System

- v-forge

---

## Status

External-reference interpretation note.

This document exists so useful external implementation patterns can be preserved in the shared root without being silently treated as authority.

---

## Core Rule

Agent orchestration may be useful inside V Forge because V Forge is an execution operating environment with bounded execution-side research, verification, publication, content-graph maintenance, and execution intelligence responsibilities.

But any orchestration pattern adopted by V Forge must remain subordinate to V Forge's invariants:

- V Forge remains the execution system of record
- V Forge does not become the planning system of record
- V Forge does not become the signal or observability system of record
- execution remains bounded by approved scope
- human-in-the-loop requirements remain real where governance requires them

An orchestration runtime is useful only if it strengthens bounded execution operability without weakening ownership boundaries or governance.

---

## External Reference

The immediate external reference for this design note is the uploaded `coordinatorMode.ts` implementation example.

That file demonstrates a concrete coordinator/worker pattern with:

- coordinator-mode detection
- session mode matching
- dynamic worker-context injection
- worker tool filtering
- optional scratchpad/shared-workspace injection
- a detailed coordinator system prompt
- worker task launch / continuation / stop behavior
- structured worker completion notifications

This design note preserves the parts of that reference that appear useful for V Forge while translating them into V Forge-safe interpretation.

---

## Why This Matters For V Forge

V Forge is not just a single-action executor.
It is the owned execution operating environment for a project.

That means V Forge must eventually support execution behavior such as:

- implementation work
- bounded execution-side research
- verification
- release and publication operations
- content-graph maintenance
- execution intelligence work
- operator playbooks and repeatable surface-operation guidance

A single flat agent with every tool and every responsibility may be workable for small actions, but it becomes weaker when V Forge needs:

- parallel research across multiple execution concerns
- independent verification of recent work
- bounded subtask decomposition
- clearer operator visibility into task progress
- explicit stop / continue / retry control for execution tasks

This is why an orchestrator/executor pattern is relevant to the V Forge operability wave.

---

## High-Level Pattern

The external reference uses a hierarchical pattern:

- one top-level coordinator handles the user, planning of execution steps, synthesis, and task control
- one or more workers perform bounded tasks
- worker results come back as structured task notifications
- the coordinator decides whether to continue a worker, stop it, or launch a fresh worker

Translated into V Forge terms, the useful pattern is:

- a top-level V Forge operator-facing agent retains responsibility for execution orchestration, synthesis, reporting, and escalation
- bounded V Forge executors perform specific execution-side tasks
- task results return in a structured format
- the top-level V Forge agent remains accountable for understanding the results before directing further work

The key value is not "more agents" by itself.
The key value is maintaining responsibility at the orchestrator layer while using bounded executors to increase operability.

---

## Code-Level Mechanisms Shown In The External Reference

## 1. Mode Detection

The reference includes an explicit mode switch.

Illustrative snippet:

```ts
export function isCoordinatorMode(): boolean {
  if (feature('COORDINATOR_MODE')) {
    return isEnvTruthy(process.env.VFORGE_COORDINATOR_MODE)
  }
  return false
}
```

### What this means

The orchestration posture is not treated as always active.
It is gated by:

- a build/runtime feature flag
- an environment variable that actually turns the mode on

### Why this matters for V Forge

This suggests that if V Forge adopts orchestration, it should probably do so through an explicit bounded mode such as:

- operator-selected orchestration mode
- task-class-specific orchestration enablement
- gated rollout during operability-wave implementation

That is safer than silently assuming that every V Forge session should become multi-agent.

---

## 2. Session Resume Mode Matching

The reference also includes a session-resume correction path.

Illustrative snippet:

```ts
export function matchSessionMode(
  sessionMode: 'coordinator' | 'normal' | undefined,
): string | undefined {
  if (!sessionMode) {
    return undefined
  }

  const currentIsCoordinator = isCoordinatorMode()
  const sessionIsCoordinator = sessionMode === 'coordinator'

  if (currentIsCoordinator === sessionIsCoordinator) {
    return undefined
  }

  if (sessionIsCoordinator) {
    process.env.VFORGE_COORDINATOR_MODE = '1'
  } else {
    delete process.env.VFORGE_COORDINATOR_MODE
  }

  return sessionIsCoordinator
    ? 'Entered coordinator mode to match resumed session.'
    : 'Exited coordinator mode to match resumed session.'
}
```

### What this means

The runtime tries to preserve session continuity.
A resumed session should restore the same mode it previously used rather than silently changing behavior.

### Why this matters for V Forge

If V Forge later supports orchestrated sessions, it probably needs explicit continuity around:

- whether the session is orchestrated or not
- what tasks are still active
- what temporary task context remains live
- whether resumed execution can safely continue

That continuity concern fits V Forge's execution-continuity posture well.

---

## 3. Dynamic Worker Context Injection

The external reference injects tool and environment context into the coordinator/user context.

Illustrative snippet:

```ts
export function getCoordinatorUserContext(
  mcpClients: ReadonlyArray<{ name: string }>,
  scratchpadDir?: string,
): { [k: string]: string } {
  if (!isCoordinatorMode()) {
    return {}
  }

  const workerTools = isEnvTruthy(process.env.VFORGE_SIMPLE)
    ? [BASH_TOOL_NAME, FILE_READ_TOOL_NAME, FILE_EDIT_TOOL_NAME]
        .sort()
        .join(', ')
    : Array.from(ASYNC_AGENT_ALLOWED_TOOLS)
        .filter(name => !INTERNAL_WORKER_TOOLS.has(name))
        .sort()
        .join(', ')

  let content = `Workers spawned via the ${AGENT_TOOL_NAME} tool have access to these tools: ${workerTools}`

  if (mcpClients.length > 0) {
    const serverNames = mcpClients.map(c => c.name).join(', ')
    content += `\n\nWorkers also have access to MCP tools from connected MCP servers: ${serverNames}`
  }

  if (scratchpadDir && isScratchpadGateEnabled()) {
    content += `\n\nScratchpad directory: ${scratchpadDir}\nWorkers can read and write here without permission prompts.`
  }

  return { workerToolsContext: content }
}
```

### What this means

The orchestrator is informed about:

- what tools workers have
- what MCP servers are available
- whether a shared workspace exists

This reduces hidden assumptions and makes orchestration more explicit.

### Why this matters for V Forge

This is probably one of the strongest implementation ideas for V Forge.
If V Forge uses bounded executors, the top-level agent should know:

- which execution tools are available to executors
- which MCP servers or tool surfaces are connected
- whether a temporary cross-task workspace exists
- what executor classes are permitted for the current session or task class

That would improve LLM behavior and operator clarity.

---

## 4. Internal Tool Blacklist For Workers

The reference explicitly excludes some tools from worker access.

Illustrative snippet:

```ts
const INTERNAL_WORKER_TOOLS = new Set([
  TEAM_CREATE_TOOL_NAME,
  TEAM_DELETE_TOOL_NAME,
  SEND_MESSAGE_TOOL_NAME,
  SYNTHETIC_OUTPUT_TOOL_NAME,
])
```

### What this means

Workers do not receive every tool.
Some coordination-sensitive tools remain reserved to the coordinator.

### Why this matters for V Forge

This is directly relevant.
If V Forge adopts executors, subordinate executors should probably not have unrestricted access to:

- orchestration control primitives
- approval-sensitive actions
- return-to-planning actions
- possibly some cross-system mutation paths
- any tool that could rewrite execution authority boundaries

This is one of the clearest governance-aligned lessons from the external reference.

---

## 5. Coordinator System Prompt As Behavioral Spine

The reference contains a long coordinator prompt that defines:

- role
- available tools
- worker behavior assumptions
- research → synthesis → implementation → verification workflow
- continue vs spawn guidance
- anti-lazy-delegation rules
- post-launch user messaging behavior

### What this means

The orchestration intelligence is not mostly hidden in code.
It is largely a governed prompt/runtime behavior pattern.

### Why this matters for V Forge

That fits the shared-root build-spec posture well.
If V Forge adopts orchestration, a first-pass V Forge orchestrator prompt or behavior contract would likely need to define things such as:

- orchestrator responsibilities
- executor responsibilities
- what bounded execution-side research means for executors
- when to continue vs restart execution tasks
- how verification differs from implementation
- when findings are execution-local vs return-to-planning relevant
- what halt conditions exist for scope or governance reasons

---

## 6. Structured Task Notifications

The reference uses an internal notification format.

Illustrative snippet:

```xml
<task-notification>
  <task-id>{agentId}</task-id>
  <status>completed|failed|killed</status>
  <summary>{human-readable status summary}</summary>
  <result>{agent's final text response}</result>
  <usage>
    <total_tokens>N</total_tokens>
    <tool_uses>N</tool_uses>
    <duration_ms>N</duration_ms>
  </usage>
</task-notification>
```

### What this means

Task lifecycle events are not mixed into normal chat as if they are ordinary user messages.
They are structured internal signals.

### Why this matters for V Forge

This is useful because V Forge likely needs explicit separation between:

- operator conversation
- internal task-state updates
- execution reporting
- final execution outcomes

A structured task-notification model could help future V Forge operator surfaces remain legible.

---

## 7. Continue / Stop / Relaunch Semantics

The reference defines three key runtime actions:

- launch a worker
- continue an existing worker
- stop a running worker

### What this means

The system recognizes that execution tasks have lifecycles.
They are not just one-shot tool invocations.

### Why this matters for V Forge

This is important for execution continuity.
V Forge often needs bounded, resumable, reviewable execution rather than stateless single-shot calls.

Useful V Forge-aligned interpretations include:

- continue the same executor when context overlap is high and the prior task context remains useful
- launch a fresh executor for independent verification or when earlier context is polluted by a wrong approach
- stop an executor when scope has changed or the task direction is no longer valid

That fits well with V Forge's halt / clarification / continue discipline.

---

## 8. No-Lazy-Delegation Synthesis Rule

One of the strongest rules in the reference is that the coordinator must synthesize research results before issuing follow-up work.

Illustrative anti-pattern from the reference:

```ts
// Bad
AGENT_TOOL({ prompt: "Based on your findings, fix the auth bug" })
```

Illustrative better pattern from the reference:

```ts
// Better
AGENT_TOOL({
  prompt: "Fix the null pointer in src/auth/validate.ts:42. Add a null check before user.id access. If user is null, return 401 with 'Session expired'."
})
```

### What this means

The top-level orchestrator remains responsible for understanding the work.
It does not outsource understanding to the next worker.

### Why this matters for V Forge

This is highly compatible with V Forge.
A V Forge orchestrator should remain responsible for:

- understanding execution findings
- deciding whether a finding is execution-local or planning-relevant
- deciding whether work remains in scope
- writing bounded executor instructions that are specific and reviewable

This prevents the orchestration layer from becoming empty ceremony.

---

## What Else This Pattern Needs To Work

The external file by itself is not enough.
The orchestration pattern shown there depends on a broader runtime environment.

## 1. Worker-Spawning Runtime Primitive

The pattern assumes a runtime can actually launch subordinate agents and track them.

Required capabilities include:

- spawn a new bounded executor
- assign it an ID
- preserve some task-local context
- receive structured completion or failure output
- continue or stop the task later

Without that runtime, the pattern is just prompt cosplay.

---

## 2. Tool Registry And Tool Access Control

The pattern assumes a tool registry that can:

- expose allowed tools to the orchestrator
- expose a filtered subset to executors
- hide internal coordination tools from executors
- mark tool concurrency posture where relevant
- perform permission checks before use

If V Forge adopts orchestration, this access-control layer is not optional.

---

## 3. MCP Integration Layer

The pattern assumes MCP clients can be discovered and their tools made available.

Required capabilities include:

- connected MCP server discovery
- stable server naming or identity
- tool exposure for executors where allowed
- context injection telling the orchestrator which MCP surfaces are live

This is directly relevant to `v-forge/mcp-surface.md`.

---

## 4. Task Lifecycle State Tracking

The pattern assumes tasks are not ephemeral mysteries.
There is enough lifecycle tracking to know:

- task id
- running / completed / failed / stopped status
- brief result summary
- full result payload if available
- usage / timing metadata if useful

V Forge would likely need some bounded first-pass task lifecycle model if orchestration becomes real.

---

## 5. Operator-Surface Support

The pattern assumes the operator can understand what is happening.

Required operator-surface abilities likely include:

- seeing what executors are active
- seeing what they were launched to do
- seeing whether they completed, failed, or were stopped
- resuming or redirecting work safely
- understanding when the orchestrator is waiting vs actively executing

Without this, orchestration becomes opaque and trust degrades.

---

## 6. Temporary Workspace Policy

The external reference includes a scratchpad/shared-workspace pattern.

That can be useful, but in V Forge it would need clear classification.
At minimum, V Forge would need rules distinguishing:

- temporary executor coordination state
- durable execution truth
- content-graph truth
- operator-facing reports
- return-to-planning findings

A shared workspace must not silently become shadow authority.

---

## 7. Governance And Halt Conditions

The external runtime pattern becomes unsafe if the orchestrator and executors lack explicit stop conditions.

For V Forge, an orchestration-capable runtime would need to respect halt conditions such as:

- scope ambiguity that crosses into planning reconsideration
- governance-sensitive external or paid action without sufficient authorization
- attempted cross-system ownership drift
- execution-side research expanding into open-ended observability behavior
- mid-execution discovery of scope excess

Without these guardrails, orchestration increases risk rather than useful capability.

---

## 8. Verification Posture

The external reference correctly treats verification as a distinct responsibility rather than a rubber stamp.

A useful V Forge implementation would likely need:

- explicit verification tasks or verifier executors
- separation between implementation and independent verification where appropriate
- real outcome recording rather than optimistic self-approval

This matters because V Forge owns execution truth, and execution truth becomes weak if verification is fake.

---

## What Appears Most Reusable For V Forge

The following parts of the external pattern appear highly reusable:

- explicit orchestrated-mode gating
- session continuity for orchestrated execution
- dynamic context injection listing executor tools and live MCP surfaces
- filtered executor tool access
- launch / continue / stop executor lifecycle
- structured task notifications
- no-lazy-delegation synthesis rule
- fresh-eye verification instead of self-verification only
- brief post-launch operator messaging that avoids fabricating results

These are useful operational patterns, not just implementation trivia.

---

## What Requires Stronger V Forge Adaptation

The following parts would need explicit V Forge-specific doctrine before being adopted:

## 1. Executor Task Taxonomy

The generic external pattern talks about workers in broad software-engineering terms.
V Forge likely needs a more bounded task taxonomy such as:

- implementation executor
- verification executor
- content executor
- release executor
- content-graph maintenance executor
- execution-intelligence analysis executor
- surface-operations executor

This does not need to become over-engineered immediately, but V Forge should not adopt a taxonomy-free worker blob.

---

## 2. Temporary State vs Execution Truth

The external pattern permits a scratchpad-like workspace.
V Forge must make clear what remains temporary and what becomes canonical execution truth.

Examples of likely distinctions:

- temporary workspace notes are not execution truth
- executor summaries are not automatically canonical reports
- content-graph changes become truth only through governed write paths
- return-to-planning findings are not equivalent to planning decisions

---

## 3. Cross-System Boundary Rules

The external reference does not know anything about Project V, VEDA, or V Forge.
V Forge must therefore add explicit rules for:

- when an execution finding stays local
- when a finding must return to Project V
- how VEDA signal may be read without becoming execution-owned signal canon
- what executor actions are forbidden because they would blur planning or observability boundaries

---

## 4. Governance-Sensitive Action Controls

The external pattern is runtime-centric.
V Forge must add governance-sensitive controls for:

- external paid actions
- launch-sensitive changes
- public-facing publication or mutation
- actions that require stronger human approval posture

Not every executor should be able to perform every action, even if the tool technically exists.

---

## 5. Execution-Side Research Limits

The generic research pattern in the external reference is useful, but V Forge must preserve bounded execution-side research.

That means executors may research only when the research is needed to:

- complete approved execution
- validate approved execution
- determine whether bounded execution must halt, clarify, or return findings upstream

Executors must not become general research agents or shadow observatories.

---

## Recommended Interpretation Posture

The correct way to use the external coordinator-mode reference inside the V Ecosystem is:

- do not treat it as doctrine
- do not treat it as authority over V Forge boundaries
- do treat it as a practical orchestration design input
- harvest the runtime and operator-surface ideas that strengthen V Forge operability
- translate those ideas into V Forge-specific governance, scope, and boundary rules before adoption

This is a design-input document, not a constitution.

---

## Implications For The Current V Forge Workstream

This design note strengthens the case that the future `v-forge/mcp-surface.md` doc should probably address more than flat tool lists.

It likely needs at least a bounded first-pass statement on whether V Forge supports:

- an operator-facing orchestrator posture
- bounded executor task delegation
- executor tool filtering
- task lifecycle visibility
- executor continuation / stopping behavior
- temporary coordination workspace posture
- notification or result-return behavior

That does not require over-designing a full orchestration platform immediately.
But ignoring orchestration entirely would likely underspecify how V Forge becomes practically operable for the LLM/operator seat.

---

## Recommended Next Questions

When the V Forge MCP surface is drafted, the following questions should be answered explicitly:

1. Does first-pass V Forge support orchestrator/executor task delegation at all?
2. If yes, what executor task classes are admitted in first pass?
3. What tool classes may executors use directly?
4. What tools remain orchestrator-only?
5. What temporary workspace, if any, is allowed?
6. What task-result shape is required?
7. What execution findings stay local versus return to Project V?
8. What VEDA-derived signal access is allowed for execution intelligence tasks?
9. What halt conditions stop executors or halt orchestration entirely?
10. What operator approvals are required for high-risk actions?

Those questions belong in future V Forge build-spec work, not in this note.

---

## Final Rule

The external coordinator-mode reference demonstrates that useful multi-agent execution orchestration is practical.

For V Forge, the value is not copying the pattern verbatim.
The value is using it to shape a governed V Forge execution-orchestration posture that:

- improves operability
- keeps responsibility visible
- preserves execution continuity
- supports bounded executor specialization
- remains compatible with V Forge invariants
- does not create a shadow planner or shadow observatory inside execution

If V Forge adopts orchestration, it must do so as better bounded execution — not as an excuse for architecture drift.

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `surface-execution-state-design-note.md`
- `human-in-the-loop-doctrine.md`
- `reporting-and-approval-model.md`
- `vs-project-v.md`
- `vs-veda.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../governance/external-action-governance.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/testing-and-verification-doctrine.md`
