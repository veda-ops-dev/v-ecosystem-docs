# Audit Evaluation Rules

## Purpose

This document defines the first-pass BYDA audit rules for Project V.

It exists to answer:

```text
What audit types exist, what questions do they ask, what counts as pass/fail/warning/stale, what creates audit gaps, and what invalidates audit confidence later?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the audit execution model (how audits run, who sets the result)
- the first-pass audit types and what they ask
- the rule evaluation order
- the hard-failure conditions per audit type
- the warning conditions per audit type
- cross-artifact consistency check requirements
- ambiguity detection rules
- gap creation rules
- staleness and invalidation rules

---

## Out of Scope

This document does not define:

- the BYDA philosophy and ownership model (see `byda-in-project-v.md`)
- controlled vocabulary values (see `controlled-vocabularies.md`)
- how audit state couples to readiness (see `readiness-evaluation-rules.md`)
- schema field details (see `schema-authority.md`)
- audit-and-gap model shape (see `schema-authority.md` — AuditRun and AuditGap sections)

---

## System

- project-v

---

## Core Rule

BYDA in Project V must behave as a governed questioning and audit layer.

It must not ask random questions. It must ask explicit questions tied to:

- audit type
- lifecycle phase
- declared artifacts or governed expectations
- readiness and implementation consequences

If the system cannot explain what was asked and why the result was produced, the audit layer is too weak.

---

## Audit Execution Model

An audit may be operator-triggered, but the canonical audit result is server-computed from governed rules.

That means:

- an operator or workflow may request that an audit run
- the caller does not get to set the canonical `result`
- the server must execute the governed checks, compute the canonical result, and create gaps where required

If the server is not computing the result from governed checks, the audit model is too weak.

---

## First-Pass Audit Types

The first-pass BYDA core supports these audit types as real and implementable:

- `research`
- `planning`
- `implementation_readiness`
- `code_alignment`
- `handoff`
- `hygiene`

Not every project must use every audit type on day one. But the rule set must define what each type means.

---

## Rule Evaluation Order

Evaluate in this strict order for every audit run.

### Step 1 — Scope validity
If the target entity is missing, invalid, or out of project scope, fail the request rather than producing an audit result. Return `400 Bad Request` or `404 Not Found` as appropriate.

### Step 2 — Audit applicability
If the requested audit type does not apply to the target entity or lifecycle stage, fail the request rather than producing fake output. Return `422 Unprocessable Entity`.

### Step 3 — Required-basis validity
If the audit lacks the minimum required basis to ask its questions honestly, return `fail` and create gaps where appropriate.

### Step 4 — Hard-failure conditions
If one or more hard-failure rules are true, return `fail`.

### Step 5 — Warning conditions
If no hard-failure rule is true but one or more warning conditions are true, return `warning`.

### Step 6 — Pass condition
If no hard-failure rule or warning condition is true, return `pass`.

### Step 7 — Staleness
`stale` is not a normal first-run result. It is a later invalidation state applied when the original audit basis is no longer trustworthy. See Staleness / Invalidation Rules.

---

## Audit Questions and Rules By Type

---

### Audit Type: `research`

**Allowed targets:** `project`, `objective`, `initiative`, `work_item`

**Primary questions:**
- Is the project or target record scoped clearly enough to justify continued planning?
- Is there enough evidence or rationale to support the current direction?
- Are obvious blockers or dependencies visible rather than hidden?
- Is bounded ownership between Project V, VEDA, and V Forge still clear?

**Hard-failure examples:**
- Material evidence basis is missing
- Ownership is ambiguous
- The problem statement is too vague to plan against

**Warning examples:**
- Rationale exists but is still thin
- Dependency visibility is incomplete but not yet blocking
- Evidence is present but weak in one advisory area

**Typical gap severities:** `major`, `minor`, `advisory`

---

### Audit Type: `planning`

**Allowed targets:** `project`, `objective`, `initiative`, `work_item`

**Primary questions:**
- Is the planning stack structurally valid for the intended phase?
- Are key planning records, decisions, and dependencies explicit enough to govern work?
- Do governed docs agree on the current planning shape?

**Hard-failure examples:**
- Structurally required planning context is missing
- Key planning docs materially disagree
- Target system or scope remains materially unclear

**Warning examples:**
- Minor planning detail is incomplete
- One non-blocking doc inconsistency exists

**Typical gap severities:** `major`, `minor`, `advisory`

---

### Audit Type: `implementation_readiness`

**Allowed targets:** `initiative`, `work_item`, `handoff`

**Primary questions:**
- Is the target ready to move toward implementation or implementation tracking?
- Are blocking readiness and audit issues resolved?
- Is implementation linkage posture clear enough where required?
- Do governed contracts and planning docs agree enough to proceed?

**Hard-failure examples:**
- Required readiness gate is still failing
- Blocking audit gap remains open
- Implementation linkage posture is missing where required
- Cross-artifact contract disagreement is material

**Warning examples:**
- Non-blocking advisory gap remains open
- Implementation linkage is present but not yet as rich as preferred

**Typical gap severities:** `critical`, `major`, `minor`

---

### Audit Type: `code_alignment`

**Allowed targets:** `work_item`, `handoff`

**Primary questions:**
- Is there bounded GitHub or code-linked evidence for the target work?
- Does the linked code evidence appear to match the governed intent?
- Is obvious spec-to-code drift visible?
- Has the audit basis been invalidated by later linkage changes?

**Hard-failure examples:**
- Required GitHub or code linkage is missing
- Linked code evidence materially contradicts governed intent
- Material code drift is visible against governed contracts or docs

**Warning examples:**
- Linkage exists but is incomplete in one advisory area
- Evidence is present but still thin or partially summarized

**Typical gap severities:** `major`, `minor`, `advisory`

---

### Audit Type: `handoff`

**Allowed targets:** `handoff`, `work_item`

**Primary questions:**
- Is the handoff target explicit and bounded?
- Does the handoff basis align with readiness and audit state?
- Are unresolved issues still visible to the receiving boundary?

**Hard-failure examples:**
- Handoff target remains ambiguous
- Readiness and audit basis materially disagree
- Blocking gap remains unresolved

**Warning examples:**
- The handoff may proceed but still carries advisory caveats

**Typical gap severities:** `critical`, `major`, `minor`

---

### Audit Type: `hygiene`

**Allowed targets:** `project`, `objective`, `initiative`, `work_item`, `handoff`

**Primary questions:**
- Are the governed docs and records staying clean, explicit, and non-contradictory?
- Is ambiguity, TODO language, or drift accumulating?

**Hard-failure examples:**
- Material ambiguity prevents safe implementation or governance
- Stale contradictions remain unresolved across authority docs

**Warning examples:**
- Ambiguity exists but is still advisory rather than blocking
- Minor documentation debt is visible

**Typical gap severities:** `major`, `minor`, `advisory`

---

## Cross-Artifact Consistency Checks

BYDA becomes meaningfully useful only when it checks for contradictions across governed artifacts.

First-pass cross-artifact checks must include at least the following, bound to the audit types that apply them:

| Check | Applies To Audit Types |
|---|---|
| `schema-authority` ↔ `controlled-vocabularies` | `planning`, `implementation_readiness`, `hygiene` |
| `controlled-vocabularies` ↔ implementation | `planning`, `implementation_readiness`, `hygiene` |
| API contracts ↔ `schema-authority` | `implementation_readiness`, `code_alignment`, `hygiene` |
| `status-transitions` ↔ explicit status-route expectations | `planning`, `implementation_readiness`, `hygiene` |
| External linkage rules ↔ `implementation-traceability` rules | `code_alignment`, `handoff` |

### Applicability note on API contracts

API contract docs are deferred output in the documentation roadmap. Until they exist, the API contracts ↔ schema check cannot run. When running `implementation_readiness` or `code_alignment` audits before API docs exist, the audit must note the absence as an advisory gap rather than treating it as a blocking cross-artifact contradiction.

### Contradiction severity

If a material contradiction exists between two checked artifacts, the audit must return `fail`. If the contradiction is minor and non-blocking, it may return `warning`.

---

## Ambiguity Detection Rules

BYDA must explicitly detect implementation-dangerous ambiguity in governed docs.

First-pass ambiguity detection must flag terms such as:

- `appropriate`, `sufficient`, `reasonable`, `as needed`, `properly`
- `later`, `TBD`, `TODO`

Flagging a term triggers a classification decision.

### Material ambiguity — must fail the audit

Ambiguity is material when it affects any of the following:

- a field or rule that governs a hard-block readiness condition
- a status transition rule or allowed/forbidden classification
- a target-system or boundary classification
- a readiness or audit gate condition
- a constraint or validation rule that the hammer suite would probe

Examples:
- "set a **reasonable** timeout" in a schema spec → material; a timeout value is a hard rule, not a preference
- "use **appropriate** credentials" in a security doc → material; authentication rules are implementation gates
- "**TBD**: decide retry behavior" in an API contract → material; missing contract terms block safe implementation

### Advisory ambiguity — may produce a warning or minor gap

Ambiguity is advisory when it appears in:

- non-normative explanatory text that does not govern a rule
- prose rationale or context sections
- guidance that describes a recommendation rather than a requirement
- areas where the adjacent concrete rule makes the intent sufficiently recoverable

Examples:
- "this pattern is generally **sufficient** for most projects" in a rationale paragraph → advisory
- "**TODO**: add examples here" in an explanatory section that already has governing rules → advisory

### Ambiguity detection is a classification step, not a blanket pass/fail

Not every flagged term fails the audit. The audit must classify each finding as material or advisory before deciding result impact.

---

## Gap Creation Rules

An audit must create one or more `AuditGap` records when the audit exposes a concrete deficiency that must remain recoverable.

First-pass posture:

- hard-failure conditions must create at least one audit gap
- warning conditions may create advisory or minor gaps
- purely informational observations must not automatically become gaps

A good audit gap must preserve:

- what failed or weakened the audit
- why it matters
- what remediation direction exists
- whether it remains open, resolved, or invalidated

---

## Separation of Audit Gaps and Readiness Gaps

Audit gaps and readiness gaps are separate record families. They must not be silently collapsed.

- audit gaps preserve audit failures, contradictions, ambiguity findings, and stale-confidence issues
- readiness gaps preserve readiness deficiencies that block or weaken progression

They may relate to one another, but the separation must be maintained structurally.

---

## Staleness / Invalidation Rules

An audit result becomes `stale` when its original basis is materially invalidated.

First-pass triggers include:

- a superseding decision is recorded
- a material schema or contract change occurs after the audit
- a backward status rollback invalidates prior confidence
- implementation-linked evidence changes after the audit in a material way
- external linkage changes in a way that invalidates the audited basis

`stale` means the prior audit result must not be trusted as current. It does not convert the system into `pass` or `fail`. It means re-audit is required.

---

## Audit Output Minimum Requirements

A first-pass BYDA audit must preserve at least:

- audit type
- target entity
- result
- summary
- generated gaps (or explicit record that no gaps were found)
- enough basis to explain what was checked and why the result was produced

---

## Deferred Enhancements

The following remain intentionally deferred from the first-pass BYDA core:

- numerical scoring
- audit profiles
- temporal drift detection
- reverse-audit checks
- gap effort estimation
- dependency mapping between gaps
- richer audit layer hierarchies
- artifact-aware skip logic
- advanced code-diff intelligence
- historical trend views
- supersedence lineage
- audit weighting models

These should be promoted only when real use shows the first-pass core is still too weak.

---

## Hammer Expectations

The hammer suite must verify at least:

- invalid audit requests fail deterministically
- hard-failure conditions produce `fail`
- non-blocking conditions can produce `warning`
- gap creation is consistent
- cross-artifact contradictions are detected
- ambiguity detection behaves deterministically for governed patterns
- staleness triggers invalidate prior confidence correctly
- audit gaps and readiness gaps remain separate record families

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- audit results are server-owned and not caller-settable
- evaluation runs in a strict order: scope → applicability → basis → hard-fail → warning → pass
- `stale` is a later invalidation state, not a first-run result
- cross-artifact consistency checks are required for specific audit type combinations
- ambiguity detection classifies material vs advisory before deciding result impact
- audit gaps and readiness gaps must remain structurally separate

---

## Usage

This document should be used:

- when implementing BYDA audit evaluation logic
- when writing hammer tests for audit behavior
- when debugging an unexpected audit result
- as the authoritative rule source for BYDA in Project V

---

## Related Docs

- `byda-in-project-v.md`
- `readiness-evaluation-rules.md`
- `readiness-methodology.md`
- `controlled-vocabularies.md`
- `schema-authority.md`
- `implementation-traceability.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/testing-and-verification-doctrine.md`
