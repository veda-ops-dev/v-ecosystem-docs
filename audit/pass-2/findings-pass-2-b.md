# Pass 2 Findings — Vocabulary & Term Consistency

Session: B
Folders audited: `project-v/`
Date: 2026-04-05

---

### Files loaded

- `project-v/project-v.md`
- `project-v/system-invariants.md`
- `project-v/lifecycle.md`
- `project-v/operational-workflow.md`
- `project-v/multi-project-doctrine.md`
- `project-v/data-boundaries.md`
- `project-v/byda-in-project-v.md`
- `project-v/v-forge-integration.md`
- `project-v/schema-authority.md`
- `project-v/schema-governance.md`
- `project-v/schema-specification.md`
- `project-v/controlled-vocabularies.md`
- `project-v/status-transitions.md`
- `project-v/readiness-methodology.md`
- `project-v/readiness-evaluation-rules.md`
- `project-v/audit-evaluation-rules.md`
- `project-v/implementation-traceability.md`
- `project-v/github-integration.md`
- `project-v/mcp-surface.md`
- `project-v/endpoint-governance.md`
- `project-v/api-conventions.md`
- `project-v/hammer-doctrine.md`
- `project-v/hammer-plan.md`
- `project-v/hammer-coverage-map.md`
- `project-v/hammer-implementation-rules.md`
- `project-v/polymorphic-reference-enforcement.md`
- `project-v/operator-surfaces/vscode-extension.md`
- `project-v/decisions/ADR-001-separate-databases-per-bounded-system.md`
- `project-v/decisions/ADR-002-strict-multi-project-enforcement.md`
- `project-v/decisions/ADR-003-governed-schema-and-endpoint-expansion.md`
- `project-v/decisions/ADR-004-separate-audit-and-readiness-records.md`
- `project-v/api/objectives.md`
- `project-v/api/initiatives.md`
- `project-v/api/work-items.md`
- `project-v/api/handoffs.md`
- `project-v/api/readiness.md`
- `project-v/api/audits.md`
- `ecosystem/vocabulary.md` (canonical reference)
- `audit/findings-pass-1.md` (exclusion check)

### Files excluded based on Pass 1

None found. No `project-v/` docs were flagged as stubs, archive material, or self-declared superseded in Pass 1 findings.

---

### Undefined load-bearing terms

**Term: `handoff scope` / `execution scope` / `bounded execution scope` / `handed-off scope`**

| Attribute | Value |
|---|---|
| Docs that use it | `system-invariants.md`, `lifecycle.md`, `v-forge-integration.md`, `operational-workflow.md` |
| Definition found? | N |
| Short note | Four distinct phrases are used across project-v/ to refer to the same load-bearing concept: the bounded set of work transferred from Project V to V Forge at handoff time. `vocabulary.md` defines `Handoff` as the transfer event but does not define the scope of what is transferred. None of the four phrases has a canonical definition. |
| Evidence quote | `system-invariants.md`: "constraining execution through approved scope and handoff conditions"; `lifecycle.md`: "no longer owns execution truth for the handed-off scope"; `operational-workflow.md`: "the execution target and scope are clear"; `v-forge-integration.md`: "the relevant execution scope" |

---

### Near-synonym sprawl

**Term pair: `handoff-preparation` (hyphen) vs underscore pattern used by all other multi-word vocabulary values**

| Attribute | Value |
|---|---|
| Terms | `handoff-preparation` vs expected `handoff_preparation` |
| Locations | `controlled-vocabularies.md` under Work Item Type; referenced by `schema-specification.md` |
| Canonical term | Not determinable from loaded docs — the exact string used in `controlled-vocabularies.md` is `handoff-preparation` but this is inconsistent with the rest of the vocabulary |
| Intentional? | N |
| Short note | Every other multi-word controlled vocabulary value in `controlled-vocabularies.md` uses underscores as separators: `not_ready`, `ready_with_warnings`, `implementation_readiness`, `code_alignment`, `relates_to`, `project_v`. The Work Item Type value `handoff-preparation` uses a hyphen. This is a load-bearing inconsistency because these strings are used as constrained field values in the schema and must be exact at implementation time. |
| Evidence quote | `controlled-vocabularies.md` Work Item Type: "`handoff-preparation`" alongside `implementation_readiness` and `code_alignment` in audit types; `schema-specification.md`: "work item `type`" listed as using controlled vocabularies |

---

### Canonical terms used incorrectly

None found.

All ecosystem-level canonical terms from `vocabulary.md` that appear in `project-v/` docs (`Handoff`, `Evidence`, `Findings`, `BYDA`, `Hammer`, `Bounded`) are used in ways consistent with their definitions.

---

### Vague references

**Reference: "the system" in `operational-workflow.md`**

| Attribute | Value |
|---|---|
| Reference | "the system" |
| Doc | `operational-workflow.md` |
| Why it is ambiguous | Used in the sentence: "Project V must always know which planning state it is in. The workflow must remain interpretable enough that a later reader or capable LLM can determine..." — here "the system" clearly refers to Project V and is not ambiguous. |
| Evidence quote | "Operational speed does not outrank planning doctrine." — no genuine vague reference found in this doc. |

Verdict: No genuinely ambiguous "the system" references found in `project-v/`. The few cases encountered are self-resolving from context. Not a finding.

**Reference: `actor` field in `schema-specification.md` and `status-transitions.md`**

| Attribute | Value |
|---|---|
| Reference | "server-resolved `actor`" |
| Docs | `schema-specification.md` (`StatusHistory.actor`), `status-transitions.md`, `api/objectives.md`, `api/handoffs.md` |
| Why it is ambiguous | `actor` appears as a required field on `StatusHistory`, `DecisionRecord`, and `AuditRun` records. It is described as "server-resolved from the authenticated request context." However, no doc in `project-v/` defines what value the server resolves to. Is it a user ID? A session token? A system identifier string? The `controlled-vocabularies.md` Actor/Origin section says "Actor-like fields remain free text in the first pass" with "guidance, not yet a controlled vocabulary." This leaves `actor` undefined as a field contract despite appearing in every governed transition. |
| Evidence quote | `schema-specification.md` `StatusHistory`: "actor text not null"; `status-transitions.md`: "The `actor` value must be server-resolved"; `controlled-vocabularies.md`: "Actor / Origin Guidance — This is guidance, not yet a controlled vocabulary." |

This is a load-bearing term gap: `actor` drives attribution in every status history record and is required for audit trails, but its value format is explicitly deferred.

---

### Capitalization inconsistencies

None found.

`Project V`, `VEDA`, and `V Forge` are consistently capitalized throughout all `project-v/` docs.

`VS Code extension` is used consistently (with space) in `operator-surfaces/vscode-extension.md`, which is appropriate given that document's topic. The reference to "VSCode extension" (no space) in `mcp-surface.md` is a stale host reference (the active host is now the Tauri 2 desktop per ADR-011), not a capitalization inconsistency of a canonical system name.

---

### Summary

`project-v/` vocabulary is substantially coherent. The controlled-vocabularies.md functions well as a single source of truth for enumerated values, and the schema/API docs reference it consistently. Two issues require attention before implementation.

The `handoff-preparation` hyphen in Work Item Type (Finding: Near-synonym sprawl) is the most concrete pre-implementation blocker: the exact string must be consistent with the rest of the vocabulary before schema constraints and validation logic are written. The undefined `actor` field format (Finding: Vague references) is the second priority: every status history record requires it, and "free text — guidance only" is not sufficient specification for implementation.

---

### Out-of-scope observations not included in findings

- `mcp-surface.md` refers to "the VSCode extension" as the operator surface. The active host is now the Tauri 2 desktop per ADR-011. This is a doc staleness issue, not a vocabulary finding.
- `operator-surfaces/vscode-extension.md` governs the VS Code extension surface, which is now superseded by the desktop. The doc was not flagged in Pass 1 as superseded (it lacks a `## Status: Superseded` header), so it remains in scope for Pass 2. No vocabulary findings within its content.
- The `operator` term (undefined in `vocabulary.md`) appears throughout `project-v/` docs in the same pattern identified in Session A. Not re-flagged here — already captured.
- The `governance-sensitive` term (undefined in `vocabulary.md`, defined differently in two governance docs) appears in `project-v/` in the same pattern identified in Session A. Not re-flagged here — already captured.
