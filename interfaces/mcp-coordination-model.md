# MCP Coordination Model

## Purpose

This document defines how MCP tools are structured, scoped, and enforced across the V Ecosystem.

It exists to answer:

```text
How are MCP tools organized, how is project scope enforced so an LLM cannot touch the wrong project, what is the session token model, and what rules must every MCP tool follow to preserve system boundaries and prevent cross-project contamination?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the role of MCP tools in the ecosystem
- the API-first enforcement model
- the session token model for project scoping
- cross-project contamination prevention
- MCP tool design rules
- what MCP tools may and may not do
- the relationship between the VSCode extension and MCP session initialization

---

## Out of Scope

This document does not define:

- the specific list of MCP tools for each system
- provider-specific API details
- credential or secrets management beyond the scope model
- UI design for the VSCode extension beyond the scope selector
- transport-level MCP protocol mechanics

Those belong in system-specific operator surface docs, interface docs, or implementation docs.

---

## System

- ecosystem

---

## Core Rule

MCP tools are thin wrappers.

The enforcement chain is always:

```text
LLM declares intent
→ MCP tool (thin wrapper — transport only)
→ API call (enforcement layer — business rules, scope, ownership)
→ Database (never accessed directly by MCP tools)
```

No MCP tool may bypass this chain.
No MCP tool may access the database directly.
No MCP tool may enforce business rules that belong to the API.
The API is the enforcement layer.

---

## MCP Role Definition

MCP tools exist to let an LLM interact with V Ecosystem systems in a bounded, governed way.

MCP tools are good for:

- reading bounded system state relevant to the current session
- triggering governed API actions within approved scope
- surfacing observatory data, planning state, and execution state to the LLM
- helping the LLM understand current project state without asking the human operator

MCP tools are not:

- a source of truth — they read and write through APIs that own the truth
- a shortcut around governance — every action through MCP follows the same rules as any other API call
- a direct database client — database access is never direct, always through the API
- an authority escalation mechanism — MCP tool availability does not grant permission

---

## The API-First Enforcement Model

All MCP tool calls route through system APIs.

The API is responsible for:

- enforcing project scope
- enforcing system ownership boundaries
- enforcing authorization and actor rules
- validating all inputs
- emitting canonical event log entries where required
- returning clean, bounded responses

The MCP tool is responsible for:

- formatting the request to the API
- passing the session-scoped project context as a header
- returning the API response to the LLM in a usable form
- not adding business logic of its own

If a capability is not safe or coherent through the API, MCP must not work around it.
The fix belongs in the underlying API, not in a clever MCP tool implementation.

---

## The Session Token Model

### Why session tokens instead of project ID headers

The most obvious approach — having the LLM pass a project ID in each tool call — is insufficient. The LLM controls what it passes. That means the LLM could, accidentally or through drift, pass the wrong project ID and contaminate another project's data.

The correct model moves project scope out of LLM control entirely.

### How session initialization works

The human operator selects the active project in the VSCode extension.
The extension calls the MCP server's session initialization endpoint with the project UUID selected by the operator.
The project UUID comes from the project list the extension loaded through the API — not from direct database access.
The MCP server creates a session record bound to that project UUID server-side.
The MCP server returns an opaque session token to the extension.
The extension stores the session token for the duration of the session.
Every subsequent MCP tool call includes the session token automatically — not the project ID.
The MCP server resolves the project scope from the token server-side before forwarding the request to the API.
The LLM never sees the project ID. The LLM only sees the session token.

### What the LLM cannot do

The LLM cannot:

- change the active project during a session
- pass a different project ID to a tool call
- infer the project ID from the session token
- access another project's data even if it tries

### How project switching works

Project switching is a deliberate human action.
The operator selects a different project in the extension.
The extension initializes a new session with the new project UUID.
A new session token is issued.
The prior session token is invalidated.
The new session is bound to the new project.

### What happens when a session token is invalid or expired

If the MCP server receives a tool call with an invalid, expired, or unrecognized session token, it must:

- reject the tool call with a governed error response — not silently proceed
- not attempt to infer a project scope from other context
- not fall back to a default project
- surface the error clearly so the extension or operator can reinitialize the session

An expired or invalid session token is not a degraded permission level. It is an absent session. The correct response is rejection and re-initialization, not best-effort continuation.

---

## The VSCode Extension as Governance Layer

The extension is not just a display surface.
It is an active governance layer for project scope.

The extension:

- presents the active project selector to the human operator
- initializes sessions with the MCP server when the operator selects a project
- stores the session token for the active session
- passes the session token automatically on every tool call
- displays the active project name visibly at all times in the status bar
- invalidates the prior session when the operator switches projects

The operator glances at the status bar and always knows which project the LLM is operating on.
If it ever looks wrong, the operator can correct it before any tool call happens.

---

## Cross-Project Contamination Prevention

Cross-project contamination — an LLM reading or writing another project's data — is a hard failure, not a minor hygiene concern.

The following layers prevent it:

### Layer 1 — Human project selection
The operator selects the active project. The LLM does not.

### Layer 2 — Session token binding
The session token is bound to the selected project server-side. The LLM cannot change this binding.

### Layer 3 — Project ID not exposed to LLM
The LLM sees only the session token, not the project ID. It cannot pass the wrong project ID because it never has the project ID.

### Layer 4 — API scope enforcement
The API resolves project scope from the session token and enforces it on every request. Reads filter by project. Writes require explicit project context. UUID lookup alone is not sufficient — the record must belong to the active project.

### Layer 5 — Cross-project non-disclosure
If a record exists but belongs to a different project, the API returns 404 as if it does not exist. Not 403. Not an error that reveals existence. 404.

### Layer 6 — Hammer verification
The hammer test suite for each system includes explicit cross-project violation probes. Any attempt to access another project's data must fail. This is not optional. Cross-project isolation must be verified, not merely declared.

No single layer is sufficient alone.
All six layers together make cross-project contamination structurally impossible rather than merely discouraged.

---

## MCP Tool Design Rules

Every MCP tool in the V Ecosystem must follow these rules:

### Rule 1 — API-only access
No tool may query the database directly.
No tool may use an ORM, Prisma, or any other database client directly.
Every tool calls an HTTP API endpoint.

### Rule 2 — Project scope is automatic, not LLM-controlled
Tools do not accept project ID as a parameter from the LLM.
Project scope is resolved from the session token server-side.
Global tools (such as list projects) explicitly suppress project scope headers.

### Rule 3 — Write tools must be explicit
Write tools must be clearly identified in their description.
Write tools must call mutating API routes only where the mutation is explicitly documented.
Write tools must never disguise a mutation as a read.

### Rule 4 — No silent mutation
Read tools must not produce side effects.
No tool may silently mutate canonical state as a side effect of a read operation.

### Rule 5 — Tool descriptions must not overclaim
A tool's description must accurately describe what it does, what it reads or writes, and what scope it operates in.
A tool must not imply ownership, authority, or capability it does not have.

### Rule 6 — Deterministic outputs where possible
Tool responses must use stable field names, clear ordering, and explicit nullability.
Tool responses must not return shapeless or ambiguous data.

### Rule 7 — Owned by the system whose API it calls
A tool that calls a VEDA API endpoint is VEDA-owned.
A tool that calls a Project V API endpoint is Project V-owned.
A tool that calls a V Forge API endpoint is V Forge-owned.
MCP does not own system truth. It exposes capabilities owned by the systems it wraps.

---

## Session Initialization Contract

The session initialization endpoint must:

- accept the project UUID from the extension
- validate that the project exists and is active
- create a server-side session record binding the token to the project UUID
- return an opaque session token
- set a session expiration policy appropriate to operational use

The session token must:

- be opaque — no information about the project ID can be derived from it
- be bound to exactly one project
- be revocable server-side instantly
- expire according to the session expiration policy or when the operator switches projects

The session expiration policy is an implementation decision. This doc does not specify a duration. What matters is that expired tokens are rejected cleanly, not silently extended.

---

## Global vs Project-Scoped Tools

Most tools are project-scoped. A small number are intentionally global.

### Project-scoped tools
- send the session token as a header on every request
- are automatically scoped to the active project by the API
- cannot access data from other projects

### Global tools
- do not send project scope headers
- operate across all projects
- must be explicitly designed as global and documented as such
- examples: list projects, get project by ID, create project

Global tools must not be used as a workaround for project scoping.
The fact that a tool is global must be documented in the tool description.

---

## Write Tool Governance

Write tools require stronger discipline because they change canonical state.

Every write tool must:

- be labeled as a write tool in its description
- call a mutating API route that enforces the appropriate governance rules
- preserve the governed Propose → Review → Apply posture where required
- never self-authorize mutations that require human approval

Where a write requires explicit human approval before execution, the MCP tool must surface the recommendation for review rather than executing immediately. The tool is not the approval. The governed approval path is the approval.

---

## Verification Expectation

Every MCP tool surface must be verifiable.

Verification must confirm:

- project scope is correctly enforced
- cross-project data is not accessible
- read tools produce no side effects
- write tools mutate only what they document
- API responses align with tool descriptions
- session token binding holds correctly
- expired or invalid session tokens are rejected, not silently continued

This verification is part of each system's hammer responsibility.

---

## Forbidden MCP Patterns

The following are forbidden:

- any tool that queries the database directly
- any tool that accepts project ID from the LLM as a parameter for scoped operations
- any tool whose description implies ownership or authority it does not have
- any read tool that silently mutates state
- any tool that bypasses API validation or authorization
- any tool that self-authorizes a mutation requiring human approval
- any global tool used as a workaround for scope enforcement
- any tool whose purpose is to let the LLM switch the active project
- any behavior that silently continues on an expired or invalid session token

---

## Human-In-The-Loop Principle

The session token model keeps the human in control of project scope at all times.

The human selects the project.
The human switches the project.
The LLM operates within the scope the human set.

No LLM action through MCP can change which project is active.
That control belongs exclusively to the human operator through the extension.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- MCP tools are thin wrappers around API calls
- the database is never accessed directly through MCP
- project scope is determined by the session token, not by the LLM
- the LLM cannot switch projects or access other projects' data
- write tools require explicit labels and follow governed approval posture
- cross-project contamination is prevented by six structural layers, not by LLM good behavior
- an expired or invalid session token must cause rejection and re-initialization, not silent continuation

If an LLM believes it controls project scope through MCP tool parameters, or that a session can continue silently after token expiry, this doctrine is failing.

---

## Usage

This document should be used:

- when building any MCP tool for any V Ecosystem system
- when designing the session initialization endpoint
- when reviewing whether an MCP tool follows the required structure
- when evaluating whether cross-project contamination prevention is structurally sound
- when building the VSCode extension's project scope selector and session management

---

## Related Docs

- `../ecosystem/doctrine-vs-operational-state.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/auth-and-actor-model.md`
- `../governance/external-action-governance.md`
- `../governance/testing-and-verification-doctrine.md`
- `../veda/mcp-surface.md` *(planned)*
