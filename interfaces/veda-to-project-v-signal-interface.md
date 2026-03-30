# VEDA to Project V Signal Interface

## Purpose

This document defines the interface by which VEDA provides bounded signal and evidence outputs to Project V for planning use.

It exists to answer:

```text
What crosses from VEDA into Project V as planning-relevant signal, what does that transfer mean, and what does it not mean?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the meaning of a VEDA to Project V signal transfer
- what kinds of information may cross through the signal interface
- what role that signal plays in planning
- what is explicitly not transferred through the signal interface
- the boundary posture operators and LLMs should use when interpreting planning-relevant signal behavior

---

## Out of Scope

This document does not define:

- VEDA internal evidence-gathering workflow
- Project V internal planning workflow
- detailed source trust policy
- detailed approval policy
- detailed transport or implementation format

Those belong in VEDA docs, Project V docs, governance docs, workflow docs, and implementation-specific docs.

---

## System

- interfaces

---

## Core Rule

The VEDA to Project V signal interface transfers bounded planning-relevant signal and evidence from VEDA into Project V for planning interpretation.

A signal transfer does not transfer planning ownership to VEDA.
A signal transfer does not transfer signal-system ownership to Project V.
A signal transfer does not turn signal into decision automatically.

---

## Interface Definition

The VEDA to Project V signal interface is the bounded mechanism by which VEDA provides Project V with planning-relevant signal and evidence outputs.

The signal interface exists so that:

- VEDA can remain the signal, evidence, and observability system of record
- Project V can interpret relevant signal for planning and orchestration
- signal can influence planning without collapsing the distinction between evidence, recommendation, decision, and handoff

---

## Signal Transfer Validity Conditions

A signal transfer is valid only when:

- VEDA has produced bounded signal or evidence outputs relevant to planning
- the transfer is limited to planning-relevant signal rather than open-ended observability state
- the minimum signal-interface semantics required by this interface are present

Signal with significant source-trust concerns or high provenance uncertainty should not be treated as planning-ready signal without clearly flagging that uncertainty in the transfer and following the source-trust governance path.

This document does not define the full source-trust or approval model.
But a signal transfer must not be treated as valid if these conditions are not met.

---

## Signal Retention Principle

Not all signal or evidence collected by VEDA should be transferred into Project V.

Signal that does not affect planning, prioritization, readiness, project creation, handoff readiness, or planning reconsideration should remain inside VEDA's observability and evidence domain.

Signal transfer to Project V is warranted when the signal:

- affects what planning should consider
- affects project creation, prioritization, or readiness
- affects whether an existing plan remains valid
- affects whether a handoff should be prepared, revised, delayed, or withheld
- affects what Project V should reconsider at a planning level

---

## What a Signal Transfer Provides

A valid signal transfer provides:

- bounded planning-relevant signal or evidence
- bounded description of what was observed or inferred
- bounded reason the signal matters for planning
- bounded references, provenance, or evidence pointers needed for interpretation
- bounded indication of what planning concern the signal is relevant to

### Explanation
A signal transfer is not a dump of VEDA's full evidence state.
It is the bounded planning-relevant subset of signal and evidence needed for Project V to interpret what may matter.
VEDA is responsible for determining what signal is included in the transfer and for ensuring that only planning-relevant outputs cross the interface.
Where signal is inferred rather than directly observed, the inference basis must be included as part of the bounded provenance reference.

---

## What a Signal Transfer Does Not Provide

A signal transfer does not provide:

- planning truth
- orchestration truth
- readiness truth as a decision already made
- handoff truth
- execution truth
- permission for VEDA to decide what Project V must do next
- full observability state as a planning payload (i.e. VEDA's complete internal evidence and monitoring record)

### Explanation
After a signal transfer:

- VEDA remains the system of record for signal, evidence, and observability truth
- Project V remains the system of record for planning and orchestration truth
- V Forge remains the system of record for execution truth

The signal interface changes what Project V may consider, not who owns planning.

---

## Minimum Interface Semantics

A signal transfer should be interpretable as carrying at least the following semantic elements:

- what signal, evidence, or observation is being surfaced
- what bounded evidence or provenance supports it
- why it matters for planning
- what planning concern it affects
- what Project V should consider or reconsider
- what boundaries or uncertainties apply to the signal

These semantics may later be represented through specific data structures, but the semantic contract comes first.

---

## Ownership After Signal Transfer

After a valid signal transfer:

- VEDA remains the owner of signal, evidence, and observability truth
- Project V remains the owner of planning truth
- Project V may interpret the signal for planning purposes
- V Forge remains the owner of execution truth

No signal transfer changes the owner of those truth domains.

---

## Allowed Use of Signal Inputs by Project V

Project V may use signal-transfer inputs to:

- reconsider planning assumptions
- create or reject potential projects
- reconsider prioritization or readiness
- determine whether further bounded evidence is needed through the proper ecosystem path
- determine whether planning, reprioritization, or handoff preparation should change

---

## Forbidden Interpretations of Signal Transfer

A signal transfer must not be interpreted as:

- permission for VEDA to define planning decisions directly
- permission for Project V to absorb VEDA's signal-system role
- permission to treat signal as already-approved planning action
- permission to collapse the distinction between evidence, recommendation, and decision
- permission for Project V to treat all observability state as planning payload
- permission for Project V to treat received signal as validated planning-ready truth without independent interpretation

If a signal transfer is interpreted that way, the interface model is being used incorrectly.

---

## Relationship to Planning

The signal interface informs planning.
It does not replace planning.

Project V may use signal transfer inputs to create, revise, defer, reject, or reprioritize planning work, but those outcomes belong to Project V's planning truth, not to VEDA.
Receiving signal through this interface does not validate that signal for planning action. Project V is responsible for interpreting signal appropriately before acting on it.

This interface is unidirectional.
It defines what crosses from VEDA into Project V.
Any path from Project V back to VEDA is a separate interface and is not defined here.

This document does not define Project V's internal planning workflow.
That belongs in Project V and workflow docs.

---

## Human-In-The-Loop Principle

A signal transfer can influence high-impact planning decisions.

Human review or approval may be required depending on:

- strategic importance
- uncertainty or source-trust concerns
- external paid data implications
- project creation implications
- reprioritization or launch sensitivity

The governance and approval model for these decisions is defined in `../governance/approval-and-escalation-model.md`.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- signal transfer is a bounded interface
- Project V receives planning-relevant signal, not planning ownership from VEDA
- VEDA remains the signal and evidence system of record after the transfer
- signal does not automatically become recommendation, decision, or handoff
- the signal interface is one of the main places where evidence-to-decision drift must be prevented

If the interface is implemented as an unbounded observability dump or as automatic planning instruction, the doctrine is wrong.

---

## Usage

This document should be used:

- when defining planning-relevant signal packages or transfers
- when deciding what VEDA outputs may cross into Project V
- when reviewing whether a proposed signal transfer is too broad or too weak
- when writing VEDA and Project V workflow docs
- when evaluating whether a signal should remain inside VEDA or move into planning consideration

---

## Related Docs

- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../project-v/project-v.md`
- `../veda/veda.md`
- `project-v-to-v-forge-handoff-interface.md`
- `../workflows/project-intake-workflow.md` *(planned)*
- `../governance/approval-and-escalation-model.md` *(planned)*
- `../governance/source-trust-and-evidence-quality-doctrine.md` *(planned)*
