# Audit Pass 5 — Cross-System Consistency

## Purpose

Verify that the docs for each system pair are consistent with each other — that access rules, activity trail coverage, interface contracts, and role boundaries do not contradict across system boundaries.

Internal doc quality within each system does not guarantee cross-system coherence. This pass checks the seams.

---

## Scope

Per system pair. 2–3 sessions:

- Session A: Project V ↔ VEDA
- Session B: V Forge ↔ VEDA
- Session C: Project V ↔ V Forge (plus ecosystem-level consistency)

---

## Setup

For each session, load:

1. The cross-system boundaries doc: `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
2. The activity trail model: `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
3. All interface docs relevant to this system pair (from `C:\dev\v-ecosystem-docs\interfaces\`)
4. The governance folder: `C:\dev\v-ecosystem-docs\governance\`
5. The system-level docs for both systems in the pair (top-level system doc / README if present)

---

## Checks

### 1. Interface coverage

For this system pair, identify every cross-system interaction that should exist based on system roles.

Expected interactions for reference:
- Project V → VEDA: reads signal for planning input
- V Forge → VEDA: queries evidence during execution
- Project V → V Forge: reads execution results; sends tasks/handoffs
- V Forge → Project V: reports execution state; requests approvals

For each expected interaction, check:
- [ ] Does an interface doc exist for it?
- [ ] Does the interface doc define both directions (caller behavior AND responder behavior)?
- [ ] Do the two systems' own docs agree on who calls whom?

Flag any interaction that is expected but has no interface doc. Flag any direction mismatch.

### 2. Access rule consistency

For each interface between this pair, compare:
- What the interface doc says the caller is allowed to access
- What the target system's own docs say is accessible externally

Flag any case where the interface doc grants access that the target system's docs do not acknowledge, or vice versa.

### 3. Activity trail action type coverage

For each cross-system action between this pair, check:
- Is there a corresponding action type in the activity trail model's action vocabulary?
- Does each system's doc agree on which system is responsible for producing the activity record?

Flag any cross-system action that has no corresponding activity trail action type. Flag any ownership ambiguity (both systems claim to produce the record, or neither does).

### 4. Role boundary contradictions

Check for any case where one system's docs describe it doing something that belongs to another system's role.

Examples of violations to look for:
- Project V described as executing tasks directly (V Forge role)
- VEDA described as making planning decisions (Project V role)
- V Forge described as storing canonical evidence (VEDA role)
- Any system described as the authority for a domain it does not own

Flag each role boundary violation with the specific doc and passage.

### 5. Approval and governance gate consistency

For each approval or governance gate that spans this system pair:
- Does the approval model doc describe it?
- Does each system's doc agree on who initiates the approval request and who processes the decision?
- Is the handoff of control between systems after approval consistent across docs?

Flag any approval flow where the two systems' docs describe incompatible behavior.

### 6. Contradictions between docs

Do a direct contradiction check: are there any statements in System A's docs that directly contradict statements in System B's docs about the same topic?

Flag each contradiction with both the source statement and the contradicting statement.

---

## Output format

```
## Pass 5 Findings — Cross-System Consistency
Session: [A / B / C]
System pair: [System A] ↔ [System B]
Date: [date]

### Interface coverage
[For each expected interaction: EXISTS / MISSING / DIRECTION MISMATCH]

### Access rule consistency
[List mismatches or "None found"]

### Activity trail action type coverage
[List missing action types or ownership ambiguities, or "None found"]

### Role boundary contradictions
[List each violation: doc, passage, which boundary it crosses]

### Approval/governance gate consistency
[List mismatches or "None found"]

### Direct contradictions
[List each pair: statement in Doc A vs statement in Doc B]

### Summary
[3–4 sentences: cross-system health for this pair, most critical inconsistencies, recommended resolution priority]
```

Save findings to: `C:\dev\v-ecosystem-docs\audit\findings-pass-5-[session-letter].md`

---

## Do not fix

This pass produces findings only. Do not edit docs during this pass.

Where contradictions are found and resolution requires a judgment call about which doc is correct, flag it for human decision. Do not resolve authority questions unilaterally.
