# Audit Pass 3 — Interface Completeness

## Purpose

Verify that every interface doc (cross-system access contract) is complete enough to be implemented without guesswork.

An interface doc that omits query mechanics, error handling, or cost accounting forces implementers to invent behavior. That invented behavior becomes tribal knowledge and a future bug source.

---

## Scope

Per interface doc. One session per doc.

Target folder: `C:\dev\v-ecosystem-docs\interfaces\`

Also check: any interface contracts embedded in system-specific folders (e.g., `veda\`, `v-forge\`).

---

## Setup

For each session:

1. Load the interface doc under audit (full content)
2. Load the activity trail model: `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
3. Load the cross-system boundaries doc if it exists: `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
4. Load any doc referenced in the interface doc's `## Related Docs` section

---

## Checklist

Run every item against the interface doc. Mark each: **PASS**, **PARTIAL**, or **FAIL**.

### Query mechanics

- [ ] **QM-1**: Is the query entry point defined? (which system calls, which system answers)
- [ ] **QM-2**: Are the input parameters defined? (what fields, what types, what are valid values)
- [ ] **QM-3**: Is the response structure defined? (what fields are returned, what types)
- [ ] **QM-4**: Is pagination or result limits defined, if applicable?
- [ ] **QM-5**: Are filter options documented?

### Freshness and staleness

- [ ] **FR-1**: Is there a freshness contract? (how current is the data the caller receives)
- [ ] **FR-2**: Is there a staleness threshold defined? (when is data considered too old to use)
- [ ] **FR-3**: Does the response include a `last_updated` or equivalent timestamp field?

### Activity logging

- [ ] **AL-1**: Does the doc specify that this interface produces an activity trail record?
- [ ] **AL-2**: Is the `action` field value specified? (the dot-namespaced action type, e.g., `evidence.query`)
- [ ] **AL-3**: Are the required activity record fields covered — actor, target, cost fields if applicable?

### Degraded mode

- [ ] **DG-1**: Is degraded mode defined? (what happens when the target system is unavailable)
- [ ] **DG-2**: Is the caller's required behavior defined during degraded mode? (fail fast, use cache, block)
- [ ] **DG-3**: Is there a recovery path defined?

### Cost accounting

- [ ] **CA-1**: Does the doc state whether this interface incurs token cost or API cost?
- [ ] **CA-2**: If cost is incurred, is the cost model described? (per-call, per-token, etc.)
- [ ] **CA-3**: Is there a reference to budget enforcement for this interface?

### Structured records

- [ ] **SR-1**: Are response records structured (typed fields), not free-form text blobs?
- [ ] **SR-2**: Is the structure stable enough to write parsing code against?

### Approval references

- [ ] **AP-1**: Does this interface require any approval before access? If so, is that documented?
- [ ] **AP-2**: Are there governance gates referenced that apply to this interface?

---

## Output format

```
## Pass 3 Findings — Interface Completeness
Doc audited: [filename]
Date: [date]

### Checklist results
QM-1: [PASS/PARTIAL/FAIL] — [note if not PASS]
QM-2: [PASS/PARTIAL/FAIL] — [note]
QM-3: [PASS/PARTIAL/FAIL] — [note]
QM-4: [PASS/PARTIAL/FAIL] — [note]
QM-5: [PASS/PARTIAL/FAIL] — [note]
FR-1: [PASS/PARTIAL/FAIL] — [note]
FR-2: [PASS/PARTIAL/FAIL] — [note]
FR-3: [PASS/PARTIAL/FAIL] — [note]
AL-1: [PASS/PARTIAL/FAIL] — [note]
AL-2: [PASS/PARTIAL/FAIL] — [note]
AL-3: [PASS/PARTIAL/FAIL] — [note]
DG-1: [PASS/PARTIAL/FAIL] — [note]
DG-2: [PASS/PARTIAL/FAIL] — [note]
DG-3: [PASS/PARTIAL/FAIL] — [note]
CA-1: [PASS/PARTIAL/FAIL] — [note]
CA-2: [PASS/PARTIAL/FAIL] — [note]
CA-3: [PASS/PARTIAL/FAIL] — [note]
SR-1: [PASS/PARTIAL/FAIL] — [note]
SR-2: [PASS/PARTIAL/FAIL] — [note]
AP-1: [PASS/PARTIAL/FAIL] — [note]
AP-2: [PASS/PARTIAL/FAIL] — [note]

### Score
[X of 21 PASS] — [X PARTIAL] — [X FAIL]

### Critical gaps (FAIL items only)
[For each FAIL: what is missing and what risk does it create]

### Summary
[2–3 sentences: implementability verdict, most urgent gaps]
```

Save findings to: `C:\dev\v-ecosystem-docs\audit\findings-pass-3-[doc-shortname].md`

---

## Do not fix

This pass produces findings only. Do not rewrite interface docs during this pass.

If a required interface doc does not exist at all, flag that as a finding.
