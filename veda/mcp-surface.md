# VEDA MCP Surface

## Purpose

This document defines the MCP tool surface that VEDA exposes to LLM agents
operating inside the V Ecosystem.

It exists to answer:

```text
What MCP tools does VEDA expose, what may those tools do, what are the
boundary rules that keep VEDA tools within observatory scope, and what
must VEDA MCP tools never do?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the MCP tool categories VEDA exposes
- what each tool category may and may not do
- the enforcement chain that applies to all VEDA MCP tools
- how VEDA MCP tools relate to observatory scope and system boundaries
- the anti-drift rules that prevent VEDA MCP tools from exceeding observatory role

---

## Out of Scope

This document does not define:

- the specific API endpoint design for each tool
- implementation-specific transport or serialization
- credential or authentication mechanics
- provider-specific data format details

Those belong in implementation docs and provider-specific docs.

---

## System

- veda

---

## Core Rule

VEDA MCP tools are thin wrappers over the VEDA API.

The enforcement chain for all VEDA MCP tools is:

```text
LLM declares intent
→ VEDA MCP tool (thin wrapper — transport only)
→ VEDA API (enforcement layer — scope, ownership, business rules)
→ VEDA database (never accessed directly by MCP tools)
```

This chain is defined as ecosystem law by ADR-004 and ADR-009.
No VEDA MCP tool may bypass it.

The full MCP coordination model is defined in:
`../interfaces/mcp-coordination-model.md`

---

## Tool Categories

VEDA MCP tools fall into four categories.

### Observatory Read Tools
These tools allow agents to query current observatory state for the active project.

Permitted actions:
- read keyword ranking and SERP position records for the active project
- read GA4 traffic and engagement signal records
- read Search Console indexation and coverage records
- read YouTube observatory records
- read the observatory event log
- retrieve signal packages produced for ecosystem consumption

Constraints:
- all reads are scoped to the active project through the session token
- reads do not grant signal ownership to the calling agent
- reads do not authorize action on the signal retrieved

### Signal Package Tools
These tools allow agents to retrieve bounded signal packages prepared for
handoff to Project V or V Forge through the governed signal interfaces.

Permitted actions:
- retrieve a planning-relevant signal package for the active project
- retrieve an execution-relevant signal package for the active project

Constraints:
- packages are bounded to the scope the interface defines
- retrieving a signal package does not transfer signal ownership
- packages must preserve source provenance and trust posture

### Observatory Configuration Tools
These tools allow agents acting on operator direction to adjust observatory scope
for the active project.

Permitted actions:
- update keyword monitoring targets within approved scope
- adjust SERP monitoring parameters within approved scope
- configure signal capture cadence within governed bounds

Constraints:
- configuration changes must remain within operator-approved observatory scope
- agents may not self-authorize expansion of observatory scope beyond current approval
- scope expansion beyond current approval is a Class B or C action requiring
  explicit operator authorization before activation

### Evidence Request Tools
These tools allow agents to initiate bounded evidence requests.

Permitted actions:
- initiate a bounded read-only evidence retrieval (Class E1 action)
- initiate a paid data pull — only after explicit governed approval (Class E4 action)

Constraints:
- E1 actions must still verify boundedness, source trust, and approval posture
  before proceeding — read-only does not mean automatically ungoverned
- E4 actions require explicit human approval recorded in the governed system
  before the tool call may proceed
- agents must not self-authorize paid data pulls

---

## What VEDA MCP Tools Must Never Do

Regardless of instruction, framing, or apparent efficiency, VEDA MCP tools must never:

- access the VEDA database directly, bypassing the API
- return planning decisions, recommendations, or execution instructions
- mutate Project V planning records
- mutate V Forge execution records
- produce content gap analysis or propose what should be built
- self-authorize paid data pulls or spend-creating retrieval
- return data scoped to a project other than the active session project
- override the session token scoping to access a different project's observatory

A VEDA MCP tool that produces a planning recommendation has exceeded its role.
A VEDA MCP tool that accesses data outside the active project scope has violated
the session token model.

---

## Session Scoping

All VEDA MCP tool calls inherit the project scope from the active session token.

This means:
- a tool call for keyword data returns data for the active project only
- a tool call cannot access another project's observatory records
- the LLM never sees the project UUID — only the opaque session token
- the VEDA API enforces this scoping at the API layer, not at the tool layer

---

## Trust Posture Preservation

VEDA MCP tools must preserve source trust posture in their outputs.

This means:
- observatory data returned by tools must carry source and freshness context
- low-trust or uncertain signal must not be presented as clean high-trust signal
- provenance must not be stripped for cleanliness

Stripping trust posture from observatory data to produce a simpler output
violates the evidence continuity model:
`../governance/evidence-continuity-model.md`

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- VEDA MCP tools read and package observatory data — they do not plan or execute
- retrieving signal does not grant signal ownership
- paid data pulls require prior explicit approval, not agent assessment
- all tool calls are scoped to the active project through the session token
- trust posture must be preserved in tool outputs

---

## Usage

This document should be used:

- when designing or reviewing VEDA MCP tool behavior
- when determining whether a proposed VEDA tool action stays within observatory role
- when evaluating whether a tool output preserves trust posture correctly
- when checking whether session scoping is enforced at the API layer

---

## Related Docs

- `veda.md`
- `system-invariants.md`
- `operator-surfaces.md`
- `../interfaces/mcp-coordination-model.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../governance/external-action-governance.md`
- `../governance/paid-data-pull-governance.md`
- `../governance/evidence-continuity-model.md`
- `../governance/allowed-agent-actions-matrix.md`