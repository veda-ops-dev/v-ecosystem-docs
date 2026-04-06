# Audit 04 — Project V Authority + Build-Spec Audit Prompt

Use this prompt for the fourth Claude audit pass.

---

You are performing a **Project V Authority + Build-Spec Audit** of the V Ecosystem docs.

Use the audit posture below and follow it strictly.

[PASTE THE FULL CONTENTS OF `audit-posture.md` HERE]

---

## Audit goal

I want you to audit whether **Project V** is documented strongly enough and coherently enough to function as:
- the planning and orchestration system of record
- a bounded multi-project planning system
- a governed handoff/readiness/audit system
- an implementation-build-spec layer that a competent engineer or LLM could build from without reconstructing the model from legacy repos

This is the first **system-specific deep audit**.

Stay focused on:
- Project V identity and role fidelity
- internal coherence across lifecycle, schema, readiness, audit, hammer, operator surface, and API docs
- whether Project V docs actually obey ecosystem law and governance law
- whether Project V build-spec sufficiency is real or overstated
- whether there are any misleading seams between doctrine and implementation-facing docs

This is **not** the VEDA audit.
This is **not** the V Forge audit.
This is **not** the runtime audit.

Do not drift into redesigning the whole product.
Do not treat implementation detail as a flaw unless it creates doctrine/build-spec confusion.

---

## Audit target

Review the Project V cluster together as one system authority + build-spec spine.

### Core identity / system docs
- `project-v/project-v.md`
- `project-v/system-invariants.md`
- `project-v/multi-project-doctrine.md`
- `project-v/lifecycle.md`
- `project-v/operational-workflow.md`
- `project-v/data-boundaries.md`
- `project-v/v-forge-integration.md`
- `project-v/byda-in-project-v.md`

### Schema / authority / implementation docs
- `project-v/schema-authority.md`
- `project-v/schema-specification.md`
- `project-v/schema-governance.md`
- `project-v/polymorphic-reference-enforcement.md`
- `project-v/implementation-traceability.md`
- `project-v/api-conventions.md`
- `project-v/endpoint-governance.md`
- `project-v/github-integration.md`

### Planning / readiness / audit docs
- `project-v/controlled-vocabularies.md`
- `project-v/status-transitions.md`
- `project-v/readiness-methodology.md`
- `project-v/readiness-evaluation-rules.md`
- `project-v/audit-evaluation-rules.md`

### Hammer / operator / interface docs
- `project-v/hammer-doctrine.md`
- `project-v/hammer-plan.md`
- `project-v/hammer-coverage-map.md`
- `project-v/hammer-implementation-rules.md`
- `project-v/mcp-surface.md`
- `project-v/operator-surfaces/vscode-extension.md`

### API family docs
- `project-v/api/objectives.md`
- `project-v/api/initiatives.md`
- `project-v/api/work-items.md`
- `project-v/api/dependencies.md`
- `project-v/api/handoffs.md`
- `project-v/api/readiness.md`
- `project-v/api/audits.md`
- `project-v/api/evidence-links.md`
- `project-v/api/external-links.md`
- `project-v/api/research-docs.md`
- `project-v/api/decision-records.md`
- `project-v/api/status-history.md`

You are auditing whether this cluster works as one coherent Project V authority and build-spec system.

---

## Core questions

Answer these with specifics:

1. Does Project V consistently behave like the planning and orchestration system of record, or are there places where it drifts toward execution or observability ownership?
2. Are the core Project V docs mutually consistent in lifecycle, multi-project posture, readiness, audit, schema, handoff, and operator posture?
3. Is the build-spec layer strong enough that a competent implementer could build Project V without reconstructing key models from old repos?
4. Are any important Project V concepts underdefined, multiply defined, or used inconsistently?
5. Do the readiness and audit systems remain properly distinct, or is there conceptual drift between them?
6. Does the schema/API/operator/hammer stack align, or are there hidden contradictions between what Project V says it is and what its implementation docs imply?
7. Are any Project V docs underperforming their role, overreaching their role, or carrying stale assumptions?
8. Is there any Project V doctrine/build-spec gap that would materially confuse implementation or later system audits?

---

## What I want from you

Organize your answer exactly like this:

# 1. Direct judgment

Give a blunt judgment on the Project V cluster.
Examples:
- strong and implementation-usable
- mostly coherent with bounded cleanup needed
- conceptually strong but build-spec patchy
- or whatever you think is accurate

Explain briefly.

# 2. Project V identity / authority audit

Assess whether Project V consistently behaves like:
- planning system of record
- orchestration system of record
- bounded multi-project system
- governed handoff/readiness/audit system

Call out strongest and weakest identity docs.

# 3. Lifecycle / readiness / audit coherence audit

Audit how the Project V cluster handles:
- lifecycle
- workflow
- status transitions
- readiness methodology
- readiness evaluation rules
- audit evaluation rules
- BYDA posture

I want to know whether these areas form one coherent planning-governance model or whether there are seams.

# 4. Schema / API / implementation-spec audit

Audit how the Project V cluster handles:
- schema authority
- schema specification
- schema governance
- polymorphic references
- API conventions
- endpoint governance
- API family docs

Tell me whether this build-spec layer is real, coherent, and implementation-usable.

# 5. Hammer / operator / interface audit

Audit how Project V handles:
- hammer doctrine and plan
- hammer coverage and implementation rules
- MCP surface
- VS Code operator surface
- relationship to V Forge handoff/return boundaries

I want to know whether verification and operator posture actually reinforce Project V doctrine.

# 6. Vocabulary / term-discipline audit

Call out any Project V terms that are:
- underdefined
- multiply defined
- used inconsistently
- likely to confuse an LLM or implementer

Only call out real issues.

# 7. Bounded fixes

Split into:

## Fix now
Real Project V issues worth correcting immediately.

## Fix later
Real but lower-priority improvements.

## Leave alone
Things that may look imperfect but are functioning correctly.

# 8. Final verdict

End by answering:

> Is the Project V cluster strong enough for implementation-oriented work and for the later VEDA / V Forge / runtime audits to proceed cleanly?

Then answer:
- yes
- yes, with small cleanup first
- no

And explain why in a short final paragraph.

---

## Important constraints

- This is not the VEDA audit.
- This is not the V Forge audit.
- This is not the runtime audit.
- Do not ask for giant rewrites.
- Do not collapse doctrine docs and build-spec docs into one blur.
- Do not invent implementation gaps unless they are real and consequential.
- Prefer bounded fixes over churn.

I want a sharp Project V authority + build-spec audit, not a summary.
