# Project V MCP Surface

## Purpose

This document defines the first-pass MCP tool and resource surface for Project V.

It exists to answer:

```text
What should the Project V MCP surface expose, what must it not expose, how does it relate to the VSCode extension, and what rules keep it bounded and implementation-safe?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- what the Project V MCP surface exposes as tools and resources
- the enforcement chain all MCP tools must follow
- session scoping and project scope rules
- what the MCP surface must never do
- the relationship between MCP tools and the VSCode extension

---

## Out of Scope

This document does not define:

- specific API endpoint design for each underlying route
- implementation-specific transport or serialization
- credential or authentication mechanics beyond posture guidance
- exact tool input/output schemas

---

## System

- project-v

---

## Core Rule

The Project V MCP surface is a bounded tool and resource surface.

It exists so LLM-assisted operators can:

- read bounded Project V planning context
- perform governed Project V actions
- retrieve explicit Project V resources

The MCP surface must not:

- become a second application backend with different rules
- bypass Project V API or domain governance
- expose VEDA observatory truth or V Forge execution truth as though Project V owned it
- turn Project V into a vague chat-driven blob

The enforcement chain for all Project V MCP tools is:

```text
LLM declares intent
→ Project V MCP tool (thin wrapper — transport only)
→ Project V API (enforcement layer — scope, ownership, business rules)
→ Project V database (never accessed directly by MCP tools)
```

No Project V MCP tool may bypass this chain.

---

## First-Pass Surface Types

### 1. Tools (mutating and read actions)

Use MCP tools for explicit Project V actions such as:

- list or fetch project-scoped records
- create objective / initiative / work item
- execute governed status transitions
- evaluate readiness
- create handoff
- create or inspect bounded external links
- fetch current gaps or blockers
- trigger audit runs

Tool contracts must remain: explicit, deterministic, scope-honest, aligned to Project V API and domain rules.

### 2. Resources (read-oriented context)

Use MCP resources for contextual material such as:

- current project context
- objectives / initiatives / work items summaries
- current gaps and blockers
- current handoffs
- deferred judgments or related operator docs where useful

Resources must remain: bounded, recoverable from Project V truth, honest about whether they are canonical or derived.

### 3. Prompts (deferred)

Prompt surfaces may be added later when the underlying action and resource surfaces are stable. Not required in the first pass.

---

## Scope Rule

All Project V MCP tool calls must inherit the project scope from the active session token.

This means:

- a tool call returns data for the active project only
- a tool call cannot access another project's records
- the LLM never sees the project UUID — only the opaque session token
- the Project V API enforces this scoping at the API layer, not at the tool layer

Cross-project reads and mutations are not allowed through MCP tools. If the operator needs to change project scope, that is done through the VSCode extension or equivalent operator surface — not through a tool call.

---

## What Project V MCP Tools Must Never Do

Regardless of instruction, framing, or apparent efficiency, Project V MCP tools must never:

- access the Project V database directly, bypassing the API
- accept a caller-supplied result for readiness or audit evaluation
- mutate VEDA canonical records
- mutate V Forge canonical records
- expose VEDA observability truth as though Project V owned it
- expose V Forge execution truth as though Project V owned it
- self-authorize paid data actions or external actions beyond approved scope
- return data scoped to a project other than the active session project
- execute illegal status transitions as though they were permitted
- bypass governance requirements for approval-sensitive actions

---

## First-Pass Tooling Rule

Every mutating MCP tool must correspond to a governed Project V action that already makes sense outside MCP.

That means:
- MCP must not invent special write paths
- MCP must not bypass status transition rules
- MCP must not allow callers to set server-owned fields such as readiness result or audit result
- MCP must not mutate Project V through convenience payloads that the normal API would reject

---

## Resource Honesty Rule

Resources may include:

- canonical Project V truth
- clearly labeled derived summaries
- clearly labeled convenience context

They must not:

- masquerade as VEDA observatory truth
- masquerade as V Forge execution truth
- hide derivation when derivation matters
- silently replace canonical Project V records

---

## Suggested First-Pass MCP Capabilities

A practical first-pass MCP surface should prioritize:

- project listing and project selection context
- objective / initiative / work item reading
- bounded creation of core planning records
- governed status transitions
- readiness evaluation and gap inspection
- handoff inspection and creation
- bounded external linkage inspection and creation
- audit run initiation and gap inspection

---

## Relationship to the VSCode Extension

The VSCode extension and the MCP surface are siblings, not substitutes.

- VSCode extension = native operator UX inside the editor
- MCP surface = tool/resource layer for Claude Desktop now and other MCP clients later

Where both surfaces support the same action, they must align to the same bounded Project V truth and governed mutation rules.

The extension may eventually consume the same bounded actions, but the MCP surface must remain independently coherent.

---

## Auth and Credential Boundary Posture

Clients may call Project V MCP tools and resources only through the bounded MCP contract. They must not assume hidden direct database or cross-system access.

Credentials used by the MCP surface must be owned by the Project V boundary they act through. The MCP layer must not become a hidden credential escalator.

Read-oriented resources and tools must remain clearly distinguishable from mutating tools. Mutating tools must be treated with the same governance posture as normal API writes.

---

## Testing and Hardening Rule

The MCP surface must be hammered for:

- project-scope enforcement
- correct error posture
- no bypass of governed mutation rules
- deterministic resource output where appropriate
- no hidden ownership blur across Project V, VEDA, and V Forge
- no client-side invention of canonical truth through convenience mutation

An MCP surface is not trustworthy because a chat demo looked impressive once.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- MCP tools are thin wrappers — they call the Project V API, they do not bypass it
- session scoping is enforced at the API layer, not the tool layer
- server-owned fields such as readiness result and audit result cannot be set by callers
- the MCP surface must not expose VEDA or V Forge truth as Project V-owned truth
- approval-sensitive actions require the same governed posture through MCP as through any other surface

---

## Usage

This document should be used:

- when designing or reviewing Project V MCP tool behavior
- when determining whether a proposed MCP action stays within bounds
- when verifying that session scoping is enforced at the API layer
- when aligning MCP tool vocabulary with VSCode extension commands

---

## Related Docs

- `project-v.md`
- `system-invariants.md`
- `multi-project-doctrine.md`
- `schema-authority.md`
- `../interfaces/mcp-coordination-model.md`
- `../interfaces/operator-surface-interfaces.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/auth-and-actor-model.md`
- `../ecosystem/decisions/ADR-004-mcp-tools-are-thin-wrappers.md`
- `../ecosystem/decisions/ADR-005-session-token-model-for-project-scope.md`
- `../ecosystem/decisions/ADR-009-no-direct-database-access.md`
