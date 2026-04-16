# BYDA Spec Audit Findings — Adjudicated

## Purpose

This document records an adjudicated read of the first BYDA-style spec audit
report against the VedaOps spec corpus.

It exists to preserve the useful findings from the first audit pass while
correcting overstatements, downgrading weak claims, and distinguishing between:

- true contradiction
- real seam incompleteness
- controlled deferral
- transition-support overhang
- local repo state observations that are not themselves spec findings

This is a transition-support findings note.
It is not authority doctrine.
It is not the final word on the corpus.
It is the cleaned result of the first audit pass.

---

## Adjudication summary

The first BYDA-style audit was directionally useful.

It correctly identified:

- actor identity as a real implementation-critical gap
- VEDA Strategy interface seams as still underdefined
- transition-support notes as beginning to carry meaningful planning truth
- archetype / intake structure as a real near-term blind spot

It overstated or blurred:

- the DB read / ownership issue as a hard contradiction
- the transition-plan / branch-state relationship as straightforward plan lag
- the difference between temporary local repo state and durable corpus issues

The corpus is therefore best described as:

> structurally strong at architecture and ownership boundaries,
> but still incomplete at several implementation-critical seams

That is a stronger and more accurate conclusion than either:

- “the corpus is inconsistent”
- or
- “the corpus is ready with no real gaps”

---

## Confirmed findings

### ADJ-BYDA-001

**Severity:** Blocking  
**Type:** underdefined implementation-critical behavior  
**Location:**
- `ecosystem/ecosystem-schema-spine.md`

**Issue:**
The actor identity / `actor_id` model remains explicitly unresolved while the
activity trail posture depends on it for cross-system traceability.

**Why it matters:**
The activity trail is one of the most load-bearing cross-system contracts in the
repo. If actor identity is invented ad hoc during implementation, traceability,
consistency, and audit integrity will diverge immediately.

**Failure risk:**
- inconsistent actor identity formats across systems
- broken traceability in the activity trail
- impossible or unreliable cross-system reconstruction of responsibility

**Action timing:**
Before any real activity-trail implementation work begins.

---

### ADJ-BYDA-002

**Severity:** High  
**Type:** incomplete handoff seam  
**Location:**
- `interfaces/veda-strategy-to-project-v-signal-interface.md`
- `interfaces/veda-strategy-to-v-forge-signal-interface.md`
- `project-v/project-v.md`
- `workflows/project-intake-workflow.md`

**Issue:**
VEDA Strategy is already positioned as a real upstream signal source, but its
interfaces remain stub-level.

**Why it matters:**
The core signal path exists conceptually, but the seam where those signals take
usable governed form is still thin. That creates room for ad hoc semantics,
signal shape drift, and LLM invention if real workflows begin before the seam is
clarified.

**Failure risk:**
- signal-shape drift
- invented intake semantics
- inconsistent downstream handling of strategic signals

**Action timing:**
Before real signal-driven workflows are implemented.

---

### ADJ-BYDA-003

**Severity:** High  
**Type:** transition-support overhang  
**Location:**
- `transition-steward/hammer-upgrade-plan.md`
- `transition-steward/first-archetype-affiliate-content-site-note.md`
- `transition-steward/byda-spec-audit.md`

**Issue:**
Several transition-support notes now carry meaningful planning and
implementation-shaping truth, while still correctly labeled as non-authority.

**Why it matters:**
The problem is not that these notes exist. The problem is that the promotion path
for their truths is not yet explicit enough. Over time this can create shadow
planning doctrine even without anyone intending it.

**Failure risk:**
- transition-support notes treated as quasi-authority by future readers
- planning truths living too long outside their proper long-term home
- LLM drift toward “this note looks real enough, so I’ll treat it as settled”

**Action timing:**
Soon, but not necessarily through immediate promotion of every note.
A clearer promotion / retirement rule is the important next step.

---

### ADJ-BYDA-004

**Severity:** High  
**Type:** archetype / intake blind spot  
**Location:**
- `project-v/byda-in-project-v.md`
- `workflows/project-intake-workflow.md`
- `transition-steward/first-archetype-affiliate-content-site-note.md`

**Issue:**
A meaningful first-archetype candidate assessment now exists, but the intake and
readiness posture has not yet formally absorbed that structure.

**Why it matters:**
If the first real project is selected before intake/readiness can ask the right
questions, VedaOps may choose a “good-looking” first project that is actually a
poor proving ground.

**Failure risk:**
- poor first-project selection
- false early success signals
- under-scaffolded intake for the first live archetype

**Action timing:**
Before first real project selection / first-archetype commitment.

---

## Downgraded findings

### ADJ-BYDA-005

**Severity:** Medium  
**Type:** wording-risk / implementation-interpretation risk  
**Location:**
- `ecosystem/db-posture.md`
- `ecosystem/cross-system-boundaries.md`
- `ecosystem/ecosystem-schema-spine.md`

**Issue:**
The first audit framed the DB read posture as a hard contradiction.
That is too strong.

The more accurate concern is that the wording around:

- no conceptual merger
- no convenience coupling
- governed read access
- ownership boundaries

may still benefit from clarification so a literal implementer does not confuse:

- forbidden domain absorption
with
- governed cross-system read access

**Why it matters:**
This is not obviously a contradiction in doctrine.
It is a place where wording could still be interpreted badly by an implementer
or LLM if not read carefully.

**Failure risk:**
- over-restrictive implementation that blocks needed governed reads
- under-restrictive implementation that treats governed reads as permission for
  convenience coupling

**Action timing:**
Clarify before implementation, but this should not be treated as proof that the
corpus is internally contradictory.

---

### ADJ-BYDA-006

**Severity:** Medium  
**Type:** control-flow discoverability gap  
**Location:**
- `transition-steward/transition-plan.md`

**Issue:**
The first audit described the transition plan as behind branch reality.
That is overstated.

The transition plan already distinguishes between:

- landed
- partial
- pending human review
- deferred
- transition-support only

The more accurate issue is that as more transition-support notes accumulate,
discoverability and control-flow references may need occasional tightening so
future readers know which supporting notes matter for upcoming work.

**Why it matters:**
This is more about keeping control truth discoverable than about the plan being
materially inaccurate.

**Failure risk:**
- future work missing an important transition-support note
- readers treating side notes as optional when they are practically relevant

**Action timing:**
As part of ongoing transition-plan maintenance, not as an emergency correction.

---

### ADJ-BYDA-007

**Severity:** Medium  
**Type:** hidden assumption  
**Location:**
- multiple system and interface docs

**Issue:**
The corpus still assumes certain enforcement mechanisms will exist around
service boundaries, governed access paths, and implementation posture without
fully specifying those implementation mechanics yet.

**Why it matters:**
This is normal in a staged doctrine corpus, but it still means implementers could
introduce “temporary” shortcuts if they do not feel the missing mechanism
pressure explicitly enough.

**Failure risk:**
- accidental direct DB coupling
- convenience shortcuts during early runtime work
- boundary doctrine weakened by implementation improvisation

**Action timing:**
Before multi-system runtime implementation deepens, but not necessarily as a
standalone doctrine emergency today.

---

## Rejected or overstated findings

### REJ-BYDA-001

**Original claim shape:**
The corpus has a blocking contradiction between “no direct reads” and “reads are
required.”

**Adjudication:**
Rejected in that form.

The doctrine appears to distinguish between:

- ownership
- governed read access
- forbidden convenience coupling
- conceptual merger

That may still need wording clarification, but it is not automatically a true
blocking contradiction.

---

### REJ-BYDA-002

**Original claim shape:**
The transition plan is plainly behind branch reality because Batch L and other
materials are already landed.

**Adjudication:**
Rejected in that form.

The transition plan already records landed-but-unaccepted work and does not
pretend all landed material is already ratified truth. The more accurate issue
is note discoverability and transition-support overhang, not simple plan lag.

---

## Non-findings worth preserving

The first audit was correct to note that several areas looked risky but are
actually holding together well.

### Strong non-findings

- four-system ownership boundaries are unusually clear and consistent
- single-Postgres / four-schema posture is well defended and no longer muddled
- VEDA “observatory only / no brain” posture is reinforced consistently
- schema-spine rigor is high even where some seams remain unresolved
- deferred-but-owned language is often used correctly to prevent ad hoc doctrine
  invention rather than pretending unsettled work is already finished

These strengths matter because they show the corpus is not failing broadly.
The real issues are concentrated at seams, not spread everywhere.

---

## Local repo state note

The original audit included current working-tree observations:

- modified `transition-steward/transition-plan.md`
- untracked transition-support files

Those observations are operationally useful, but they should not be confused
with durable corpus findings.

They reflect local repo state at audit time, not permanent spec defects.

---

## Prioritized implementation-critical gaps

If the goal is to reduce near-term implementation and planning drift, the
highest-priority gaps now appear to be:

1. **Actor identity spec**
2. **Minimum viable VEDA Strategy signal contract**
3. **Archetype / intake structure for first real project selection**
4. **Clearer promotion / retirement rule for transition-support planning notes**
5. **Optional wording clarification around governed cross-system reads**

This ordering preserves the signal from the audit without overstating the
corpus’s weaknesses.

---

## Recommended next move

The smallest sensible next move is not another broad audit pass.

It is to use this adjudicated findings note as the cleaner baseline for the next
Claude-run audit comparison later, while proceeding with a narrow seam-
clarification focus on:

- actor identity
- Strategy signal seam
- first-archetype / intake seam

That preserves momentum while avoiding audit theater.

---

## Related files

- `byda-spec-audit.md`
- `transition-plan.md`
- `hammer-upgrade-plan.md`
- `first-archetype-affiliate-content-site-note.md`
- `../project-v/byda-in-project-v.md`
- `../workflows/project-intake-workflow.md`
- `../ecosystem/db-posture.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/ecosystem-schema-spine.md`
