# V Ecosystem

## Purpose

This document defines what the V Ecosystem is.

It exists to answer:

```text
What systems make up the V Ecosystem, what role does each system play, and how should the ecosystem be understood as a whole?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the top-level identity of the V Ecosystem
- the role of each core system in the ecosystem
- the high-level separation of system responsibilities
- the ecosystem-wide mental model used by operators and LLMs

---

## Out of Scope

This document does not define:

- detailed cross-system interface contracts
- detailed workflow steps
- detailed governance rules
- project-specific internal doctrine
- implementation details

Those belong in more specific ecosystem, project, interface, workflow, or governance docs.

---

## System

- ecosystem

---

## Tier 1 Note

A Tier 1 ecosystem authority document defines top-level cross-system truth for the V Ecosystem.

Tier 1 docs should be:

- broadly stable
- low-ambiguity
- load-bearing for later docs
- limited to top-level ecosystem meaning and rules

---

## Core Rule

The V Ecosystem is a bounded multi-system environment.

Each system exists to own a different kind of truth.
The ecosystem is strongest when those ownership boundaries stay explicit.

No system should expand casually into another system’s truth domain.

---

## Ecosystem Definition

The V Ecosystem is the coordinated set of systems used to:

- observe reality
- interpret signal
- create and govern plans
- hand off work
- execute work
- report outcomes
- maintain and improve launched work over time

The ecosystem is not a single monolithic application.
It is a governed set of cooperating systems.

---

## Core Systems

## Project V

### Role
Project V is the planning and orchestration system of record.

### Owns
- planning truth
- orchestration truth
- project decomposition
- readiness truth
- decision truth
- handoff truth

### Does Not Own
- long-lived execution truth
- signal/observability truth
- raw external evidence as a canonical store

### Main Use
Project V exists to decide what should be pursued, how it should be structured, when it is ready, and when it should be handed off.

---

## VEDA

### Role
VEDA is the signal, evidence, and observability system of record.

### Owns
- signal truth
- evidence truth
- observability truth
- external reality inputs relevant to the ecosystem

### Does Not Own
- planning truth
- execution truth
- project orchestration truth

### Main Use
VEDA exists to observe, gather, organize, and preserve the external and internal signals that other systems may interpret.

---

## V Forge

### Role
V Forge is the execution system of record.

### Owns
- execution truth
- implementation truth
- bounded execution-side research
- maintenance execution
- execution-side reporting

### Does Not Own
- planning truth
- orchestration truth
- signal/observability truth as a system of record

### Main Use
V Forge exists to carry out approved work, perform bounded execution-side research, report what happened, and return execution findings back into the ecosystem where required.

---

## VEDA Strategy

### Role
VEDA Strategy is the derived strategic intelligence system of the V Ecosystem.

### Owns
- opportunity scoring
- content gap detection
- clustering
- competitive analysis
- strategic signals derived from observatory truth

### Does Not Own
- observatory truth — that belongs to VEDA
- planning truth — that belongs to Project V
- execution truth — that belongs to V Forge
- raw signal or evidence — VEDA Strategy reads from VEDA; it does not replace it
- planning decisions or execution decisions

### Main Use
VEDA Strategy reads VEDA observatory truth and derives bounded strategic intelligence.
It signals Project V when new project-worthy opportunities emerge.
It signals V Forge when in-scope optimization or execution-relevant conditions are identified.
It does not replace Project V's planning authority or V Forge's execution authority.

---

## High-Level Ecosystem Model

The ecosystem should be understood through this flow:

1. **VEDA** observes external reality and preserves signal, evidence, and observability truth
2. **VEDA Strategy** reads VEDA's observatory truth and derives scored opportunities, gap signals, and strategic intelligence
3. **Project V** receives strategic signals from VEDA Strategy, interprets what matters for planning, and creates structure, readiness, and handoff truth
4. **Human review and approval** occurs at meaningful choke points before execution where required
5. **V Forge** executes approved work within its bounded role
6. **V Forge** receives execution-relevant signals from VEDA Strategy to inform execution intelligence
7. **V Forge** reports outcomes, issues, and findings back into the ecosystem
8. **VEDA** continues to observe reality over time
9. **Project V** may re-prioritize, re-plan, or create new handoffs based on strategic signals and execution findings

This is a cooperation model, not shared ownership.

---

## Operator Access Layer

The V Ecosystem is primarily surfaced to operators through one unified Tauri 2 desktop application.

That desktop application is an operator-facing governance and runtime layer. It is not a peer ecosystem system alongside Project V, VEDA, VEDA Strategy, and V Forge.
It presents bounded access to the four core systems while preserving their separate truth domains.
The desktop runtime behavior, orchestration posture, and tool-surface rules are governed by the desktop doctrine docs under `../interfaces/`, not by this overview doc.

---

## Human-In-The-Loop Principle

The V Ecosystem is not designed around unrestricted autonomy.

Human review, direction, and approval remain important at meaningful choke points, especially around:

- project creation
- approvals
- external paid actions
- significant mutations
- launch decisions
- ecosystem doctrine changes

The ecosystem may be heavily LLM-assisted, but it remains governed.

---

## LLM Use Principle

The V Ecosystem docs are written LLM-first.

That means the ecosystem must be understandable by a capable LLM without relying on hidden tribal knowledge.

Each system must have:

- a clear role
- clear boundaries
- clear vocabulary
- clear interactions
- clear authority

If the docs are ambiguous, the ecosystem becomes easier for LLMs to drift while implementing or operating it.

---

## Future Growth Principle

The V Ecosystem currently has four core systems. It may grow further.

Any future system added to the ecosystem must:

- have a clear role
- have a bounded truth domain
- have clear access and interface rules
- have required doctrine and onboarding docs
- avoid collapsing existing system boundaries

Future growth is governed expansion, not casual accumulation.

---

## Usage

This document should be used:

- as the first identity/orientation doc for the ecosystem
- as the top-level system-role reference for operators
- as a first-stop authority doc for LLM sessions working from the shared docs root
- as a boundary reminder when writing more specific doctrine docs

---

## Related Docs

- `cross-system-boundaries.md`
- `vocabulary.md`
- `../project-v/project-v.md`
- `../veda/veda.md`
- `../v-forge/v-forge.md`
- `../interfaces/desktop-surface-architecture.md`
- `../interfaces/desktop-agent-orchestration-model.md`
- `../governance/agent-operating-doctrine.md`
