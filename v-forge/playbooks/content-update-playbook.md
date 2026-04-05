# V Forge Content Update Playbook

## Purpose

This playbook gives operators and synced LLM sessions a practical operating sequence for bounded updates to existing owned content inside V Forge.

It exists to answer:

```text
How should an operator or LLM handle a bounded update to existing content already inside execution scope, preserve execution truth and graph truth, decide whether publication is part of the work, and know when the update must stop, clarify, or return to planning?
```

This is a Tier 2 V Forge operator support document.

---

## Scope

This playbook governs:

- bounded updates to existing owned content assets
- execution-local update work already admitted into V Forge scope
- graph updates caused by content changes
- publication-sensitive update posture where applicable
- maintenance-style content correction and refresh work
- stop / clarify / return decisions for content update work

---

## Out of Scope

This playbook does not govern:

- brand-new strategy or opportunity selection
- open-ended market or signal exploration
- unbounded new content creation outside admitted scope
- release-package workflows not centered on content asset updates
- future experimentation or optimization programs

Those belong in Project V, VEDA, the release workflow, or later V Forge playbooks.

---

## System

- v-forge

---

## Core Rule

A content update playbook starts from an already admitted execution scope and preserves truth at every step.

The goal is not merely to “get the update done.”
The goal is to:
- update the correct asset
- stay inside approved or admitted execution scope
- preserve honest execution state
- preserve honest content graph state
- preserve honest publication continuity where relevant
- stop when the update has become a planning problem instead of an execution problem

---

## When To Use This Playbook

Use this playbook when all of the following are true:
- the work concerns an existing owned content asset
- the work is already inside admitted V Forge execution scope
- the work is bounded enough to describe clearly
- the task is an update, correction, refresh, or maintenance-style improvement rather than open-ended new strategy creation

Examples:
- revise an existing page already inside approved execution scope
- correct or expand a section of an existing page inside maintenance scope
- update internal links on an existing asset after legitimate execution change
- correct schema usage on an existing asset
- refresh existing content based on bounded execution-local need

---

## Do Not Use This Playbook When

Do not use this playbook when:
- the work is actually a new content initiative with no admitted execution basis
- the work depends on deciding whether a new topic should be pursued
- the work requires open-ended VEDA-style signal gathering first
- the work would materially redefine planning direction
- the work is really a release-package problem more than a content-asset update problem

In those cases:
- Project V may need to decide scope
- VEDA may need to provide bounded signal
- the release playbook may be the correct path
- return-to-planning may be required

---

## Inputs You Should Have Before Starting

Before beginning, you should have:
- project scope clarity
- the content asset identity
- the admitted execution basis for the update
- enough current-state visibility to know what currently exists
- any bounded constraints that matter to the update

Helpful inputs may include:
- the handoff or execution authorization basis
- current graph relationships for the asset
- recent execution findings related to the asset
- publication continuity if the asset is already live
- execution intelligence outputs if they are already admitted and relevant

If those inputs do not exist in usable form, do not bluff past it.
Clarify or stop.

---

## Default Operating Sequence

## Step 1 — Confirm the work is truly an update

Ask:
- is there already an existing asset?
- is this really a bounded modification to that asset?
- is the scope already admitted into execution?

If the answer to any of those is unclear, stop and classify before acting.

### Good signs
- exact asset is known
- update target is specific
- the update basis already exists in execution scope

### Bad signs
- the operator or LLM is drifting into “we should probably also make three more pages”
- the update target is only loosely defined
- the real ask sounds like planning, not execution

---

## Step 2 — Inspect current execution truth

Before changing anything, inspect what V Forge already says is true.

Check:
- current asset state
- current content graph relationships for that asset
- existing maintenance or blocker state
- current publication continuity if the asset is live

Do not update blind.
A large share of content drift starts when someone edits from memory instead of current truth.

---

## Step 3 — Restate the bounded update scope

Restate the exact update in bounded terms.

Examples:
- update section X on page Y
- correct schema markup on asset Z
- improve internal links for an already-built topic cluster in current scope
- refresh existing page copy inside maintenance scope

The restated scope should make clear:
- what asset is affected
- what kind of change is allowed
- what is explicitly not included

If you cannot restate the update cleanly, you are not ready to proceed.

---

## Step 4 — Decide whether this is execution-local or planning-relevant

Ask:
- does this update remain a bounded execution correction or refresh?
- or is the update revealing a broader content gap, structural contradiction, or new planning need?

### Execution-local examples
- fix incorrect internal links
- correct schema usage
- refresh outdated section copy within current asset scope
- improve already-admitted asset completeness

### Planning-relevant examples
- update reveals the asset no longer matches current planning direction
- update requires adding materially new scope beyond admitted work
- update reveals a broader cluster/topic decision that V Forge should not make alone

If planning relevance appears, do not force it into “maintenance.”
That is exactly how V Forge grows shadow strategy.

---

## Step 5 — Perform the bounded content update

Once scope is clear, perform only the in-scope update.

During update execution:
- stay inside the stated asset boundary
- preserve partial progress honestly if interrupted
- avoid absorbing adjacent ideas into the work unit
- treat newly discovered opportunities as findings, not permissions

The update should make the existing asset more truthful, usable, current, or structurally correct.
It should not turn into opportunistic roadmap expansion.

---

## Step 6 — Update content graph truth

If the content change materially affects structure, update graph truth accordingly.

Examples:
- internal link change
- topic relationship change caused by real execution truth
- entity relationship correction
- schema usage correction
- archetype classification change only if the asset actually changed materially enough to justify it

Graph updates must follow what the content update actually changed.
They must not lead it.

If the content changed materially and the graph was left stale, the work is not done.

---

## Step 7 — Decide whether publication continuity is affected

Ask:
- was this a live asset?
- did the update affect what is actually published or released?
- does publication continuity need to reflect a meaningful change?

If yes:
- update publication continuity honestly
- check whether stronger authorization posture matters for the specific surface or visibility level

If no:
- do not invent publication steps just to feel complete

Publication continuity matters when the real published state changed.
Not every internal correction is a publication event.

---

## Step 8 — Classify the outcome honestly

At the end of the update, classify the work truthfully.

Possible outcomes:
- completed
- partial
- blocked
- failed
- return_required

### Use completed when
- the bounded update finished
- graph truth is aligned
- publication continuity is aligned if relevant

### Use partial when
- some real progress happened
- but the full update did not complete

### Use blocked when
- the update cannot continue inside current scope because of a real execution blocker

### Use failed when
- the update attempt did not succeed

### Use return_required when
- the update revealed a planning-level problem or scope contradiction that V Forge should not decide locally

Do not classify for aesthetics.
Classify for truth.

---

## Step 9 — Record findings if they matter

If the update surfaced useful execution findings, record them.

Examples:
- asset was structurally weaker than expected
- graph drift was larger than expected
- publication constraints were more restrictive than assumed
- bounded execution intelligence raised a planning-relevant concern

A finding should remain bounded and honest.
It is not a stealth decision record.

---

## Step 10 — Return to planning if needed

Return-to-planning is required when the update crosses execution boundaries.

Common triggers:
- the admitted update scope no longer makes sense
- the real fix requires materially larger scope
- the content asset reveals a planning contradiction
- publication cannot continue legitimately without planning clarification
- execution intelligence or update findings materially affect future planning direction

When returning:
- preserve what was actually updated
- preserve what remains blocked or uncertain
- package bounded findings
- do not dump all execution ownership upstream

Return is not failure theater.
It is correct governance when execution should stop.

---

## Fast Checks During the Work

Use these quick questions during the update.

### Check 1
**Am I still editing the same asset, or am I silently expanding scope?**

### Check 2
**Did the content change require graph change, and did I actually update the graph?**

### Check 3
**Is this still execution-local, or am I now deciding what should exist next?**

### Check 4
**If audited later, would the update look like bounded execution or stealth planning?**

If the answers start drifting, stop.

---

## Stop Immediately Conditions

Stop and do not continue casually when:
- the target asset is no longer clearly identified
- the admitted scope is unclear
- the real update requires materially broader work than originally admitted
- the content graph implications are no longer execution-local
- publication-sensitive change now requires stronger authorization and that posture is unclear
- the work is starting to sound like “while we’re here, let’s also…”
- execution intelligence is being treated as permission instead of input

That is the point for:
- clarification
- halt
- bounded finding
- return-to-planning

Not improvisation.

---

## Good Use of This Playbook Looks Like

Good use looks like:
- clear asset identity
- clear update scope
- inspection before mutation
- update work that stays bounded
- graph truth updated after real content change
- publication continuity touched only when actually relevant
- honest final status
- clean return-to-planning when boundaries are crossed

Bad use looks like:
- editing from memory instead of current truth
- graph drift left behind after content change
- maintenance used as a loophole for new content creation
- publication done because capability exists, not because posture is clear
- broader strategy drift hidden inside “content update” language

---

## LLM Sync Reminder

A synced LLM using this playbook should remember:
- this is for existing assets already inside execution scope
- update work is bounded execution, not strategy expansion
- graph truth must follow real content change
- publication continuity matters only when real published state changed
- execution intelligence can inform but not authorize
- return-to-planning is the correct response when the update becomes a planning problem

If the LLM starts sounding like a strategist or opportunistic expansion engine, it is out of bounds.

---

## Usage

This playbook should be used:
- by operators updating existing content assets in V Forge
- by synced LLM sessions handling maintenance-style or bounded refresh work
- when deciding whether a content update stays local or must return to planning
- as the first practical playbook for routine content execution work in V Forge

---

## Related Docs

- `../v-forge.md`
- `../operator-quickstart.md`
- `../content-lifecycle-workflow.md`
- `../content-graph-operations.md`
- `../execution-intelligence-operations.md`
- `../mcp-surface.md`
- `../../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../../governance/approval-and-escalation-model.md`
- `../../governance/external-action-governance.md`
