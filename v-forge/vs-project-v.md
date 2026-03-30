# V Forge vs Project V

## Purpose

This document defines the distinction between V Forge and Project V, and the
rules that preserve that distinction during planning, handoff, execution, and
return-to-planning.

It exists to answer:

```text
What is the difference between what V Forge does and what Project V does,
where does one system end and the other begin, and what drift patterns must
be prevented to keep those roles clean?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the fundamental distinction between V Forge's role and Project V's role
- what V Forge may accept from Project V and what it must not absorb
- what Project V retains after handoff and what it must not absorb back
- the boundary posture during handoff, execution, and return-to-planning
- the drift patterns that blur the line between the two systems

---

## Out of Scope

This document does not define:

- the detailed handoff payload format
- the detailed return-to-planning payload format
- internal planning workflow steps
- internal execution workflow steps

Those belong in the interface docs, workflow docs, and system operational docs.

---

## System

- v-forge

---

## Core Rule

Project V owns planning truth. V Forge owns execution truth.

These are not the same truth and must not be treated as such even when they
concern the same project at the same moment.

A project being handed off to V Forge has both planning truth (in Project V)
and beginning execution truth (in V Forge). They coexist without merging.

---

## The Fundamental Distinction

Project V answers: what should be done, why, and when?
V Forge answers: what was done, how, and what happened?

Project V operates in the planning domain:
- what work exists
- whether work is ready
- what scope is approved
- what should move next
- what planning changes are required

V Forge operates in the execution domain:
- what execution was performed
- what was built
- what the content graph looks like now
- what execution findings emerged
- what happened during bounded execution

These domains overlap in time but must not merge in ownership.

---

## What V Forge Accepts from Project V

V Forge accepts through the governed handoff interface:

- the approved execution scope
- the execution objective and constraints
- relevant planning context needed to execute correctly
- evidence references that matter for execution
- conditions that should trigger return-to-planning

V Forge does not accept:
- planning authority over future work
- the right to replan based on execution findings without the return-to-planning interface
- the right to create new projects
- ownership of Project V's decision records

---

## What Project V Retains After Handoff

After handoff, Project V retains:

- planning truth for the handed-off work
- the governing decisions that shaped the handoff
- handoff truth — what was handed off, why, and under what constraints
- the right to receive return-to-planning findings and evaluate them
- the right to replan if return-to-planning findings warrant it

Project V does not absorb back:
- execution records from V Forge
- canonical content graph state
- execution findings as though they are planning decisions

---

## How V Forge Informs Project V Without Owning Planning

V Forge may produce findings that affect planning. It does so through the
return-to-planning interface, not through direct planning mutation.

The pattern is:
1. V Forge identifies a finding during execution that affects the planning basis
2. V Forge packages the finding through the return-to-planning interface
3. Project V receives the finding and evaluates it
4. Project V decides what planning response is appropriate
5. If replanning is needed, Project V performs it

V Forge does not decide that replanning is needed.
V Forge identifies that a finding may warrant reconsideration and returns it.
The planning decision belongs to Project V.

Return-to-planning interface: `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`

---

## Drift Patterns to Prevent

### V Forge drift toward planning
V Forge has drifted when it:
- makes planning decisions based on execution findings without the return-to-planning path
- creates new project direction or scope independently
- treats execution momentum as planning authority
- stores planning records as execution records to bypass Project V
- proposes replanning and then self-executes on the proposal without Project V evaluation

### Project V drift toward execution
Project V has drifted when it:
- stores rich execution lifecycle state as though it were canonical execution truth
- acts as the execution ledger rather than V Forge
- monitors V Forge execution at a granularity that substitutes for V Forge's own records
- overrides V Forge's bounded execution decisions from the planning side without a governed path

Both directions of drift are governance failures.
Neither system should envy or absorb the other's truth domain.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- planning truth and execution truth coexist without merging
- V Forge accepts a handoff but not planning authority
- Project V retains planning truth but not execution ownership
- execution findings reach Project V through a governed interface, not by direct mutation
- drift in either direction — V Forge acting as planner, Project V acting as executor — is wrong

If an LLM treats execution findings as automatic planning decisions, or treats
Project V planning records as V Forge's execution specification, this doctrine is failing.

---

## Usage

This document should be used:

- when evaluating whether a proposed action belongs in V Forge or Project V
- when reviewing whether execution findings are crossing the boundary correctly
- when writing V Forge or Project V docs that involve the handoff or return boundary
- when evaluating whether either system has drifted into the other's domain

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `vs-veda.md`
- `../project-v/project-v.md`
- `../project-v/v-forge-integration.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../workflows/handoff-workflow.md`
- `../workflows/maintenance-and-replanning-workflow.md`
