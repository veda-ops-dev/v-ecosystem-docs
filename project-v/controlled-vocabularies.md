# Controlled Vocabularies

## Purpose

This document defines the canonical first-pass controlled vocabularies for Project V.

It exists to answer:

```text
What enum-like values are officially allowed across Project V schema, APIs, workflow, hammer expectations, and BYDA evaluation?
```

This is the canonical registry for first-pass controlled vocabularies.

If another doc lists values that conflict with this registry, this registry wins until the conflict is resolved explicitly through a governed architecture decision.

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- all controlled vocabulary values across Project V schema, API contracts, workflow, and BYDA evaluation
- the single source of truth for any field that uses an enum or restricted value set
- the rules for extending or changing vocabulary values

---

## Out of Scope

This document does not define:

- exact column types or SQL representations
- API request/response shape beyond vocabulary values
- readiness evaluation logic or BYDA rules (those belong in their respective docs)

---

## System

- project-v

---

## Core Rule

Controlled vocabulary values must not drift across docs, routes, schema, and implementation.

A developer or LLM must not need to reconstruct canonical values by reading multiple files.

This file is the single source of truth for first-pass vocabulary values.

Adding, removing, or renaming a value is a governed architecture event — not a local implementation convenience. Follow the Vocabulary Change Rule at the end of this document.

---

## Project Status

Allowed values:

- `active`
- `deferred`
- `archived`

---

## Objective Status

Allowed values:

- `proposed`
- `active`
- `blocked`
- `completed`
- `archived`

---

## Initiative Status

Allowed values:

- `proposed`
- `active`
- `blocked`
- `completed`
- `archived`

---

## Work Item Status

Allowed values:

- `proposed`
- `active`
- `blocked`
- `completed`
- `archived`

---

## Work Item Type

Allowed values:

- `analysis`
- `planning`
- `specification`
- `handoff_preparation`
- `governance`

---

## Work Item Readiness State

Allowed values:

- `unevaluated`
- `not_ready`
- `ready_with_warnings`
- `ready`
- `deferred`

This field is server-managed. It reflects the outcome of the latest governing readiness evaluation. It must not be set directly by callers. The sync rule is defined in `readiness-evaluation-rules.md`.

---

## Initiative Target System

Allowed values:

- `project_v`
- `veda`
- `v_forge`

---

## Work Item Target System

Allowed values:

- `project_v`
- `veda`
- `v_forge`

---

## Priority

The `priority` field on `Objective` and `Initiative` uses a governed numeric range.

Allowed range: `1..1000`

Default value: `100`

Semantic: lower values represent higher priority. Priority `1` is highest; priority `1000` is lowest. List surfaces ordered by `priority asc` show highest-priority records first.

An out-of-range value supplied at creation or update must fail with `422 Unprocessable Entity`.

---

## Dependency Type

Allowed values:

- `blocks`
- `requires`
- `relates_to`

---

## Dependency Status

Allowed values:

- `active`
- `resolved`

---

## Dependency Entity Type

Allowed values:

- `objective`
- `initiative`
- `work_item`
- `handoff`

---

## Decision Record Entity Type

Allowed values:

- `objective`
- `initiative`
- `work_item`
- `handoff`

---

## Decision Record Status

Allowed values:

- `recorded`
- `superseded`

---

## Research Doc Source Type

Allowed values:

- `manual`
- `imported`
- `veda_reference`
- `external_reference`

---

## Research Doc Status

Allowed values:

- `active`
- `archived`

---

## Evidence Link Source Entity Type

Allowed values:

- `objective`
- `initiative`
- `work_item`
- `handoff`
- `decision_record`
- `research_doc`

---

## Evidence Link Type

Allowed values:

- `document`
- `observation`
- `decision_basis`
- `external_reference`

---

## Readiness Entity Type

Allowed values:

- `objective`
- `initiative`
- `work_item`
- `handoff`

---

## Readiness Evaluation Type

Allowed values:

- `research`
- `planning`
- `handoff`
- `hygiene`

First-pass readiness evaluation types intentionally exclude deeper execution-shaped concepts such as rich code-alignment modeling. Adding a new evaluation type requires explicit governance.

---

## Readiness Evaluation Result

Allowed values:

- `ready`
- `not_ready`
- `ready_with_warnings`
- `deferred`

Results are server-owned. Callers may not supply or override the result. See `readiness-evaluation-rules.md`.

---

## Readiness Gap Severity

Allowed values:

- `critical`
- `major`
- `minor`
- `advisory`

### Severity rank for ordering

When list surfaces order by severity, use numeric rank rather than raw text sort.

Canonical rank:

- `critical` = 4
- `major` = 3
- `minor` = 2
- `advisory` = 1

---

## Handoff Source Entity Type

Allowed values:

- `objective`
- `initiative`
- `work_item`

---

## Handoff Target System

Allowed values:

- `project_v`
- `veda`
- `v_forge`

---

## Handoff Type

Allowed values:

- `execution`
- `analysis`
- `governance`
- `review`

---

## Handoff Status

Allowed values:

- `proposed`
- `ready`
- `handed_off`
- `accepted`
- `closed`

---

## Audit Type

Allowed values:

- `research`
- `planning`
- `implementation_readiness`
- `code_alignment`
- `handoff`
- `hygiene`

Adding a new audit type is a schema and doctrine governance event. See `byda-in-project-v.md` for what each type asks. Richer execution-side audit types must not be normalized inside Project V until receiving-boundary doctrine is clearer.

---

## Audit Result

Allowed values:

- `pass`
- `fail`
- `warning`
- `stale`

Results are server-owned. Callers may not supply or override the result. See `audit-evaluation-rules.md`.

`stale` is not a normal first-run result. It is a later invalidation state applied when the original audit basis is no longer trustworthy.

---

## Audit Gap Severity

Allowed values:

- `critical`
- `major`
- `minor`
- `advisory`

---

## Audit Gap Status

Allowed values:

- `open`
- `resolved`
- `invalidated`

---

## External Link Source Entity Type

Allowed values:

- `objective`
- `initiative`
- `work_item`
- `handoff`
- `decision_record`
- `research_doc`
- `audit_run`

`audit_run` is allowed as a planning-side source entity for bounded external reference. These links must remain thin and non-authoritative. This is not permission to turn audit records into execution-state carriers.

---

## External Link Target System

Allowed values:

- `github`
- `v_forge`
- `veda`
- `external`

---

## External Link Type

Allowed values:

- `repository`
- `issue`
- `pull_request`
- `reference`

These are thin bounded link categories, not a rich execution taxonomy.

---

## Status History Entity Type

Allowed values:

- `project`
- `objective`
- `initiative`
- `work_item`
- `handoff`
- `decision_record`
- `audit_run`

---

## Rule Package Vocabulary

The `rulePackage` field on `ReadinessEvaluation` identifies the set of evaluation rules applied.

First-pass canonical rule packages map one-to-one with evaluation types:

- `evaluationType = research` → default `rulePackage = standard_research_v1`
- `evaluationType = planning` → default `rulePackage = standard_planning_v1`
- `evaluationType = handoff` → default `rulePackage = standard_handoff_v1`
- `evaluationType = hygiene` → default `rulePackage = standard_hygiene_v1`

A caller may supply an explicit `rulePackage` to override the default for a given `evaluationType`. If an unknown or incompatible value is supplied, the request must fail with `422 Unprocessable Entity`.

---

## Key Format Rule

Project V keys must use one governed format.

First-pass key format:

- lowercase ASCII letters and digits only
- internal separators: single hyphens only
- no spaces, no underscores, no leading hyphen, no trailing hyphen
- length: 3 to 64 characters

Regex: `^[a-z0-9]+(?:-[a-z0-9]+)*$`

This rule applies to: `Project.key`, `Objective.key`, `Initiative.key`, `WorkItem.key`.

---

## Actor / Origin Guidance

Actor-like fields remain free text in the first pass but should follow a stable convention where practical.

Recommended shapes:

- human operator identifier
- system identifier
- workflow identifier

This is guidance, not yet a controlled vocabulary.

---

## Vocabulary Change Rule

A controlled vocabulary change is a governed architectural change.

When a value is added, removed, or renamed:

1. Update this registry first
2. Update `schema-authority.md` if the affected field is listed there
3. Update `schema-governance.md` change gate
4. Update API contract docs if affected
5. Update workflow and readiness docs if affected
6. Update hammer expectations if affected

Do not silently extend controlled values in implementation first.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- this file is the canonical single source for all allowed values
- values not listed here are not allowed without a governed change
- adding a value silently in implementation is a vocabulary failure
- result fields such as readiness result and audit result are server-owned and not caller-settable

---

## Usage

This document should be used:

- as the first reference when setting any field that accepts restricted values
- when implementing schema, API contracts, or validation logic
- when writing hammer expectations for vocabulary-governed fields
- when proposing a vocabulary change through the governed change path

---

## Related Docs

- `schema-authority.md`
- `schema-governance.md`
- `status-transitions.md`
- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `byda-in-project-v.md`
