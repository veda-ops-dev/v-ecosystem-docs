# VEDA Operator Surfaces

## Purpose

This document defines what operator-facing surfaces VEDA exposes and how
operators interact with the observatory inside the V Ecosystem.

It exists to answer:

```text
What can an operator see and do through VEDA's surfaces, what observatory
configuration is operator-directed, and what must operators not attempt to
do through VEDA that would violate its pure observatory role?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- what VEDA exposes to operators through its surfaces
- what observatory configuration operators may direct
- what operators may trigger or approve through VEDA surfaces
- what operators must not attempt through VEDA that belongs elsewhere
- how VEDA's operator surface relates to the unified VSCode extension

---

## Out of Scope

This document does not define:

- implementation-specific UI layout or component design
- detailed MCP tool list for VEDA surfaces
- provider-specific configuration mechanics

Those belong in the MCP surface doc and implementation docs.

---

## System

- veda

---

## Core Rule

VEDA's operator surface is an observatory control surface, not a planning or
execution surface.

Operators use VEDA surfaces to direct what is observed, review what has been
observed, and authorize observatory-related spend.
They do not use VEDA surfaces to make planning decisions or direct execution.

---

## What Operators May Do Through VEDA Surfaces

### View observatory state
Operators may view current observatory records for active projects, including:
- keyword ranking and SERP position data
- GA4 traffic and engagement signals
- Search Console indexation and coverage data
- YouTube channel and search observatory data
- signal packages produced for ecosystem consumption
- the observatory event log for a project

### Configure observatory scope
Operators may direct VEDA to adjust what it watches for specific projects:
- adding or modifying keyword monitoring targets
- expanding or narrowing SERP monitoring scope
- adjusting signal capture cadence within governed bounds
- enabling or disabling specific observatory channels for a project

### Initiate bounded evidence requests
Operators may request specific bounded evidence pulls for planning or evaluation use,
subject to source trust classification and spend posture.

### Approve paid data pulls
Any observatory action that creates spend — paid data retrieval, premium API usage,
or billable external queries — requires explicit operator approval before activation.
This is a Class C action under the approval model.

Paid data pull governance is defined in:
`../governance/paid-data-pull-governance.md`

### Review and configure provider integrations
Operators may review active external provider integrations and their configuration
within governed bounds. Adding a new provider is an architectural event requiring
the governed path defined in:
`../ecosystem/external-provider-integration-doctrine.md`

---

## What Operators Must Not Attempt Through VEDA Surfaces

### Making planning decisions
VEDA surfaces show what the external world looks like.
Operators must not use VEDA signal directly to make planning decisions
outside the governed intake and planning workflow.
Planning interpretation belongs to Project V.

### Directing execution
VEDA surfaces must not be used to direct V Forge execution.
Signal observation and execution direction are separate governed activities.

### Mutating another system's records
Operators may not use VEDA surfaces to create or modify Project V planning records
or V Forge execution records.

### Storing non-observatory data in VEDA
Operators may not use VEDA configuration surfaces to store planning-side or
execution-side information inside VEDA's observatory records.

---

## VEDA Panel in the VSCode Extension

VEDA's primary operator surface is the VEDA panel inside the unified VSCode extension.

The VEDA panel is scoped to the active project through the session token model.
All VEDA observations, signal packages, and configuration visible in the panel
are bounded to the project the operator has selected.

The session token model is defined in:
`../interfaces/mcp-coordination-model.md`

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- VEDA operator surfaces are observatory control surfaces
- operators direct what is observed and approve observatory spend
- operators do not use VEDA surfaces to make planning or execution decisions
- paid data pulls require explicit operator approval regardless of context

---

## Usage

This document should be used:

- when designing the VEDA panel in the VSCode extension
- when deciding which operator actions are appropriate through VEDA surfaces
- when reviewing whether an operator interaction through VEDA stayed in bounds
- when writing the VEDA MCP surface doc

---

## Related Docs

- `veda.md`
- `system-invariants.md`
- `mcp-surface.md`
- `../interfaces/operator-surface-interfaces.md`
- `../interfaces/mcp-coordination-model.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/external-action-governance.md`
- `../governance/paid-data-pull-governance.md`
- `../ecosystem/external-provider-integration-doctrine.md`