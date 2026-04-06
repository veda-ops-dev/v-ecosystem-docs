# Audit Pass 4 — Workflow Codability

## Purpose

Verify that every workflow doc is specific enough to be implemented as a state machine or automated process.

A workflow doc that describes intent but not states, transitions, and failure paths cannot be implemented without invention. Invented workflow logic becomes inconsistent across agents and systems.

---

## Scope

Per workflow doc. One session per doc.

Target folder: `C:\dev\v-ecosystem-docs\workflows\`

Also check: any workflow descriptions embedded in governance or system-specific docs that are detailed enough to be implemented.

---

## Setup

For each session:

1. Load the workflow doc under audit (full content)
2. Load any interface docs referenced by this workflow
3. Load the approval and escalation model if this workflow involves approvals: `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md`
4. Load the activity trail model: `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`

---

## Checklist

Run every item against the workflow doc. Mark each: **PASS**, **PARTIAL**, or **FAIL**.

### Stage definition

- [ ] **SD-1**: Are all stages of the workflow explicitly named?
- [ ] **SD-2**: Does each stage have a defined entry condition? (what must be true to enter this stage)
- [ ] **SD-3**: Does each stage have a defined exit condition? (what must be true to leave this stage)
- [ ] **SD-4**: Is the start state defined?
- [ ] **SD-5**: Is the end state (or states) defined?

### Transitions

- [ ] **TR-1**: Are all transitions between stages defined? (from stage X, on condition Y, go to stage Z)
- [ ] **TR-2**: Are transition triggers explicit? (event, timer, approval, threshold — not vague "when ready")
- [ ] **TR-3**: Are parallel or branching paths documented where they exist?

### Cross-system calls

- [ ] **CS-1**: Are all cross-system calls within this workflow identified? (e.g., "V Forge queries VEDA evidence at this stage")
- [ ] **CS-2**: Is each cross-system call mapped to a specific interface doc?
- [ ] **CS-3**: Is the sequence of cross-system calls unambiguous?

### Failure states

- [ ] **FS-1**: Are failure states defined for each stage? (what happens if a stage cannot complete)
- [ ] **FS-2**: Are recovery paths defined from failure states?
- [ ] **FS-3**: Is there a defined behavior for timeout or no-response conditions?
- [ ] **FS-4**: Is there a defined behavior for budget exhaustion mid-workflow?

### Human touchpoints

- [ ] **HT-1**: Are all human approval points identified?
- [ ] **HT-2**: Is the escalation path defined when human approval is not received within expected time?
- [ ] **HT-3**: Are human review outputs (approve / reject / revision) mapped to workflow transitions?

### Activity trail coverage

- [ ] **AT-1**: Does the workflow specify which stages produce activity trail records?
- [ ] **AT-2**: Are the action types (dot-namespaced) identified for each activity record?

---

## Codability verdict

After completing the checklist, assess:

> Could a capable developer write a working state machine implementation of this workflow from this doc alone, without asking clarifying questions?

Score as:
- **Codable**: 18+ PASS, no FAIL on SD or TR items
- **Partially codable**: Can implement core path but failure/edge cases require invention
- **Not codable**: Core path is ambiguous or stage definitions are missing

---

## Output format

```
## Pass 4 Findings — Workflow Codability
Doc audited: [filename]
Date: [date]

### Checklist results
SD-1: [PASS/PARTIAL/FAIL] — [note if not PASS]
SD-2: [PASS/PARTIAL/FAIL] — [note]
SD-3: [PASS/PARTIAL/FAIL] — [note]
SD-4: [PASS/PARTIAL/FAIL] — [note]
SD-5: [PASS/PARTIAL/FAIL] — [note]
TR-1: [PASS/PARTIAL/FAIL] — [note]
TR-2: [PASS/PARTIAL/FAIL] — [note]
TR-3: [PASS/PARTIAL/FAIL] — [note]
CS-1: [PASS/PARTIAL/FAIL] — [note]
CS-2: [PASS/PARTIAL/FAIL] — [note]
CS-3: [PASS/PARTIAL/FAIL] — [note]
FS-1: [PASS/PARTIAL/FAIL] — [note]
FS-2: [PASS/PARTIAL/FAIL] — [note]
FS-3: [PASS/PARTIAL/FAIL] — [note]
FS-4: [PASS/PARTIAL/FAIL] — [note]
HT-1: [PASS/PARTIAL/FAIL] — [note]
HT-2: [PASS/PARTIAL/FAIL] — [note]
HT-3: [PASS/PARTIAL/FAIL] — [note]
AT-1: [PASS/PARTIAL/FAIL] — [note]
AT-2: [PASS/PARTIAL/FAIL] — [note]

### Score
[X of 20 PASS] — [X PARTIAL] — [X FAIL]

### Codability verdict
[Codable / Partially codable / Not codable]

### Critical gaps
[For each FAIL: what is missing, what a developer would have to invent, and what risk that creates]

### Summary
[2–3 sentences: implementability verdict, recommended priority fixes]
```

Save findings to: `C:\dev\v-ecosystem-docs\audit\findings-pass-4-[doc-shortname].md`

---

## Do not fix

This pass produces findings only. Do not rewrite workflow docs during this pass.
