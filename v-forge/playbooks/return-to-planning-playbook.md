# V Forge Return-to-Planning Playbook

## Purpose

This playbook gives operators and synced LLM sessions a practical operating sequence for returning bounded execution findings from V Forge back to Project V when execution should not continue locally.

It exists to answer:

```text
How should an operator or LLM recognize that V Forge has reached a real planning boundary, stop execution cleanly, package bounded findings honestly, preserve what V Forge still owns, and return the right information to Project V without collapsing execution truth into planning truth or dumping undigested execution noise upstream?
```

This is a Tier 2 V Forge operator support document.

---

## Scope

This playbook governs:

- return-to-planning posture for V Forge work
- how to recognize when execution should stop and planning should reconsider
- what bounded findings should be packaged for Project V
- what execution truth remains owned by V Forge after the return
- how to preserve honesty, uncertainty, and boundaries during the return

---

## Out of Scope

This playbook does not govern:

- Project V planning behavior after the return arrives
- VEDA-owned observatory packaging behavior
- broad operator-surface UI design
- the full schema of return-package transport payloads

Those belong in Project V docs, VEDA docs, interface docs, or operator-surface docs.

---

## System

- v-forge

---

## Core Rule

Return-to-planning is the correct governed outcome when V Forge reaches a real planning boundary.

The goal is not to prove execution failed.
The goal is to:
- stop execution at the right boundary
- preserve what V Forge actually learned
- preserve what V Forge actually did
- package only the bounded findings that planning needs
- avoid silent planning inside V Forge
- avoid dumping raw execution clutter into Project V

Return is a boundary-preserving act, not a defeat state.

---

## When To Use This Playbook

Use this playbook when all of the following are true:
- execution work is already inside V Forge
- a real boundary has been reached that V Forge should not resolve locally
- the outcome or finding materially affects what planning should do next
- continuing inside V Forge would require stealth planning, stealth scope expansion, or unauthorized interpretation

Examples:
- a content update reveals a planning contradiction
- a new content work unit turns out to require materially broader scope than admitted
- a release cannot proceed because the real authorization or planning basis is no longer adequate
- execution intelligence reveals a planning-relevant mismatch rather than an execution-local fix
- maintenance work uncovers a future-direction issue rather than a bounded correction

---

## Do Not Use This Playbook When

Do not use this playbook when:
- the issue is still clearly execution-local and solvable inside current scope
- the blocker is merely a narrow clarification that does not widen scope or alter planning meaning
- the finding is trivial and does not materially affect planning
- the work can still complete honestly inside current execution bounds

In those cases:
- continue bounded execution
- clarify locally if legitimate
- record a bounded finding if useful
- do not escalate prematurely just to feel safe

---

## First Recognition Question

Before triggering a return, ask:

**“Has this become a planning problem, or is it still honestly an execution problem?”**

That question prevents both forms of drift:
- stealth planning inside V Forge
- over-escalating ordinary execution work back to Project V

### Signs it is now a planning problem
- the admitted scope no longer makes sense
- the real next step depends on deciding what should be done, not just doing it
- broader strategy or asset-scope decisions are now required
- execution intelligence outputs materially affect future planning direction
- the work now depends on unresolved planning assumptions rather than execution-local conditions

### Signs it is still an execution problem
- the target remains clear
- the fix stays inside admitted scope
- the issue is structural or operational rather than strategic
- no planning ownership decision is actually required

---

## Inputs You Should Have Before Returning

Before returning to planning, gather:
- project scope clarity
- the current work unit identity
- the admitted execution basis that brought the work into V Forge
- the bounded finding or contradiction that triggered the return
- the current execution state of the work unit
- what remains uncertain

Helpful supporting context may include:
- graph state relevant to the finding
- release/publication continuity if release was involved
- execution intelligence outputs relevant to the return
- blocked / failed / partial state truth
- any prior related findings that materially affect interpretation

Do not wait for perfect certainty.
But do not return with vague vibes either.

---

## Default Operating Sequence

## Step 1 — Stop the local drift early

Once a real planning boundary is recognized, stop pretending this is still ordinary execution.

Do not keep pushing work forward “just a little more” if:
- the scope has clearly widened
- the meaning of the work has changed materially
- authorization depends on planning reconsideration
- execution is now making decisions about what should exist next

The earlier the boundary is recognized, the cleaner the return will be.

---

## Step 2 — Classify the trigger honestly

Classify why return-to-planning is happening.

Common trigger classes:
- scope insufficiency
- planning contradiction
- release authorization/planning mismatch
- execution intelligence planning-relevant finding
- maintenance discovering strategy-level issue
- surrounding work required beyond admitted unit

Use the smallest honest class.
Do not use vague “complexity increased” language if the real issue is scope or strategy.

---

## Step 3 — Freeze the current execution truth

Before packaging the return, make sure execution truth is stable enough to describe honestly.

Capture:
- what work actually happened
- what state the work unit is now in
- whether the outcome is partial, blocked, failed, rollback-active, or otherwise incomplete
- what V Forge still owns as execution truth after the return

Do not let the return erase execution truth.
Project V needs the finding, but V Forge still owns the execution-side reality that led to it.

---

## Step 4 — Separate facts from interpretation

Before sending anything upstream, separate:

### Execution facts
What V Forge knows from execution truth.

Examples:
- asset X was updated partially
- graph relationship Y is now inconsistent with actual built state
- release Z was validated but not authorized to proceed legitimately
- bounded execution intelligence found mismatch A using admitted inputs B

### Planning-relevant interpretation
Why those facts matter to what planning may need to do next.

Examples:
- current handoff scope may be too narrow
- future asset sequencing may need reconsideration
- release timing or packaging assumptions may no longer hold
- surrounding work may need planning review before execution continues

Do not collapse these into one blurry paragraph.
Planning needs both, but they are not the same thing.

---

## Step 5 — Package only bounded findings

The return package should include what planning needs, not every piece of execution noise.

At minimum, preserve:
- what work unit was being executed
- what triggered the return
- what execution facts matter
- what interpretation makes this planning-relevant
- what remains uncertain
- what execution work remains local to V Forge even after the return

Avoid:
- raw transcript dumping
- giant undigested logs as the main output
- speculative future strategy proposals from V Forge
- pretending the finding is more certain than it is

A good return package is bounded, reviewable, and relevant.

---

## Step 6 — Preserve uncertainty honestly

If uncertainty remains, say so.

Examples:
- whether the broader scope should actually be admitted is not decided here
- whether the mismatch warrants new work or re-sequencing is not decided here
- whether the release should be delayed, revised, or split is not decided here

Return-to-planning is not where V Forge crowns itself strategist.
It is where V Forge says:
- here is what happened
- here is why it matters
- here is what is not safe for me to decide locally

---

## Step 7 — Preserve ownership boundaries explicitly

When returning, keep ownership labels clear.

### V Forge still owns
- execution truth
- graph truth
- release continuity
- execution intelligence outputs as V Forge-owned analytical artifacts
- blocked / failed / partial state truth

### Project V will own next
- planning reconsideration
- decision about future scope
- decision about revised sequencing or new handoff posture
- any planning-side mutation of what should happen next

### VEDA still owns
- raw signal / observatory truth
- evidence continuity where VEDA is source of record

The return should transfer the finding, not erase ownership.

---

## Step 8 — Use the governed interface, not ad hoc chat logic

Return to planning through the governed interface posture.

That means:
- align with `interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- do not invent a shadow side channel because it is faster
- do not let a chat summary become the governing record by accident

Chat may explain the return.
It must not replace the governed return path.

---

## Step 9 — Classify the local outcome honestly after return

After the return is prepared or sent, classify the V Forge work unit honestly.

Common local states:
- `return_required`
- `blocked`
- `partial`
- `failed`
- `rollback_active`

Use the state that best reflects execution truth.
Do not mark work “completed” just because the return was successfully sent.
Sending the return is not the same as finishing the work unit.

---

## Step 10 — Wait for new governed direction before widening scope

After return-to-planning, do not quietly keep going on broader scope while waiting for planning.

Until new governed direction arrives:
- preserve current execution truth
- preserve the bounded finding
- avoid scope expansion
- avoid turning local notes into de facto approval

Return-to-planning means a boundary has been hit.
Respect the boundary.

---

## Fast Checks During Return Prep

Use these quick questions while preparing the return.

### Check 1
**Am I returning because this is truly planning-relevant, or just because I am nervous?**

### Check 2
**Have I clearly separated execution facts from planning interpretation?**

### Check 3
**Am I packaging bounded findings, or dumping raw clutter upstream?**

### Check 4
**Would an auditor later agree that V Forge stopped at the right boundary?**

If the answers are weak, tighten the package before sending.

---

## Stop Immediately Conditions

Stop and reset your return prep when:
- you are about to send raw execution clutter instead of a bounded package
- you are about to recommend strategy as though V Forge owns it
- you are hiding uncertainty because a stronger recommendation feels nicer
- you are about to classify the work as complete when it is only paused pending planning
- you are using the return as an excuse to avoid an execution-local fix you still actually own

The correct response is to tighten the return, not rush it.

---

## Good Use of This Playbook Looks Like

Good use looks like:
- early recognition of a real planning boundary
- clean stopping posture inside V Forge
- stable execution truth preserved before returning
- bounded findings, not noise dumping
- uncertainty preserved honestly
- explicit ownership boundaries
- governed interface use
- local work unit classified truthfully after return

Bad use looks like:
- stealth planning inside the return package
- raw logs treated as a useful handoff
- hiding what V Forge still owns
- pretending a sent return means the work unit completed
- punting ordinary execution work upstream out of caution theater

---

## LLM Sync Reminder

A synced LLM using this playbook should remember:
- return-to-planning is a correct bounded response, not embarrassment
- V Forge returns findings, not strategy ownership
- execution facts and planning interpretation must remain distinct
- uncertainty must be preserved honestly
- the governed interface matters more than a clever summary
- sending the return does not magically finish the underlying execution work

If the LLM starts sounding like a strategist or starts dumping execution clutter upstream, it is out of bounds.

---

## Usage

This playbook should be used:
- by operators preparing a V Forge return to Project V
- by synced LLM sessions that hit a real planning boundary inside execution
- when deciding whether to stop locally and package a bounded finding
- as the practical operator layer for disciplined return-to-planning behavior in V Forge

---

## Related Docs

- `../v-forge.md`
- `../operator-quickstart.md`
- `../execution-intelligence-operations.md`
- `../content-lifecycle-workflow.md`
- `../release-lifecycle-workflow.md`
- `../reporting-and-approval-model.md`
- `../../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../../governance/approval-and-escalation-model.md`
- `../../governance/decision-continuity-doctrine.md`
