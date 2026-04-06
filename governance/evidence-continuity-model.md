# Evidence Continuity Model

## Purpose

This document defines how evidence continuity is preserved inside the
V Ecosystem.

It exists to answer:

```text
What makes evidence traceable across planning, observatory, and execution
contexts, how must evidence provenance be preserved so that governing
decisions can be understood and reviewed later, and what prevents evidence
from being silently lost, misattributed, or treated as stronger than it is?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what evidence continuity means inside the V Ecosystem
- how evidence provenance must be preserved across system boundaries
- how evidence quality and trust posture must remain visible
- how evidence relates to governing decisions and planning continuity
- how evidence staleness must be handled
- the anti-drift rules that prevent evidence from becoming anonymous,
  overclaimed, or invisible in governing contexts

---

## Out of Scope

This document does not define:

- the detailed VEDA schema for evidence records
- the detailed source capture and observatory intake mechanics
- the exact format of every evidence package
- implementation-specific storage design for evidence records

Those belong in VEDA-specific docs, schema docs, and interface docs.

---

## System

- governance

---

## Core Rule

Evidence that is used to inform, support, or justify a governing decision
must remain traceable to its source, honest about its quality and trust
posture, and preserved in a way that later reviewers can reconstruct
what was known, when it was known, and how confident the ecosystem
should have been in it.

Evidence that cannot be traced is not reliable governance support.
Evidence whose quality is not visible may produce false confidence.
Evidence that disappears after use cannot support later review or continuity.

---

## Relationship to Decision Continuity Doctrine

This document extends and complements the evidence-handling principles
in `decision-continuity-doctrine.md`.

The decision continuity doctrine establishes that:

- governing decisions must be referenced, not rediscovered
- changed evidence or findings do not automatically mutate decisions
- stale or materially changed evidence may require decision revalidation
- signal, findings, and decisions are distinct categories

This document defines how evidence itself must be preserved across its
lifecycle — so that when decision continuity doctrine requires reference
to prior evidence, that evidence is still traceable and interpretable.

Where this document is silent, the baseline rules from
`decision-continuity-doctrine.md` apply.

---

## Evidence Definition

Evidence is any input used to inform, support, or justify a governing
decision, planning record, observatory finding, or operational judgment
inside the V Ecosystem.

Evidence includes but is not limited to:

- VEDA signal and observatory outputs used for planning
- search observation records used to support readiness judgments
- execution findings returned from V Forge that affect planning
- external data retrieved through governed data pulls
- research artifacts used to support planning decisions
- source provenance records that establish where data originated

Evidence is not the same as a decision.
Evidence informs decisions.
It does not replace the need for governed decision-making.

---

## Evidence Continuity Definition

Evidence continuity is the requirement that evidence used in governing
contexts remains:

- **Traceable** — its origin, capture path, and provenance are preserved
- **Honest** — its quality, trust posture, and known limitations remain visible
- **Current or Honestly Stale** — its freshness state is preserved rather
  than assumed
- **Preserved** — it is not silently lost, overwritten, or made inaccessible
  after use

Evidence continuity is what allows later reviewers, sessions, and systems
to understand why governing decisions were made and on what basis.

---

## Evidence Provenance Rule

Evidence used in governing contexts must carry enough provenance to answer:

- where did this evidence originate?
- what system, provider, or source produced it?
- when was it captured or last confirmed?
- what method or pathway was used to obtain it?
- what trust posture applies to this source?

### Rule
Evidence without provenance is anonymous evidence.
Anonymous evidence must not be treated as reliable support for governing
decisions.
If provenance cannot be established for evidence that has already been
used in a governing context, the strength of that decision's evidence
basis must be treated as unknown.

---

## Evidence Trust Classification Rule

Evidence must be classified by trust posture before it is used to support
a governing decision.

Trust posture classification must establish at minimum:

- the reliability of the source for this type of evidence
- the freshness of the evidence at the time of use
- any known limitations, biases, gaps, or uncertainty
- whether the evidence is direct observation, derived interpretation,
  or secondary inference

### Rule
Evidence trust posture must remain visible throughout its use in governing
contexts.
Presenting evidence without its trust posture attached is a form of
overclaiming.
A governing decision that relies on low-trust evidence without flagging
that trust posture is not fully honest about its own basis.

---

## Evidence Freshness Rule

Evidence has a temporal dimension that must be preserved.

Evidence that was current when captured may become stale as conditions
change.

### Staleness Determination
Evidence is materially stale when:

- the conditions it described have changed enough that the evidence
  no longer accurately represents the current state
- the time elapsed since capture exceeds the typical validity window
  for this evidence type and use
- newer evidence contradicts or significantly updates the prior evidence
- the governing decision that relied on it would likely differ if based
  on current evidence

### Rule
Stale evidence must not be treated as current evidence.
Where evidence used in a prior governing decision has become materially
stale, the decision that relied on it should be reviewed for revalidation
under `invalidation-and-supersedence-doctrine.md`.
The staleness of evidence does not automatically invalidate the decision —
but it does create an obligation to assess whether the decision remains
valid on current evidence.

When new evidence arrives during active execution or planning that directly
contradicts the evidence basis of a governing decision currently being acted on,
that contradiction must be surfaced explicitly rather than resolved by continuing
under the prior evidence basis.
The actor must halt or pause at the earliest safe point, preserve the
contradiction, and return through the governed escalation or return-to-planning
path as appropriate.
An active approval does not override materially contradicting new evidence —
it creates an obligation to reassess before continuing.

---

## Evidence Integrity Rule

Evidence must not be altered, summarized, or reframed in a way that changes
its meaning without making that transformation explicit.

This means:

- raw evidence and derived interpretation must remain distinguishable
- a summary of evidence must not be presented as equivalent to the
  original evidence
- a planning-side interpretation of evidence must not displace the
  underlying observable record that VEDA owns
- evidence must not be selectively cited in a way that misrepresents
  the overall signal

### Rule
If evidence has been transformed — summarized, interpreted, or filtered —
the transformation must be visible.
A transformed representation of evidence is not the same as the evidence
itself.

---

## Cross-System Evidence Continuity Rule

Evidence originates in VEDA and is consumed by Project V and V Forge
through governed interfaces.

This creates a cross-system evidence continuity obligation:

- VEDA must preserve evidence provenance and trust posture in the
  records it owns
- Project V must preserve the evidence references and trust context
  when using evidence to support planning decisions
- V Forge must preserve the evidence references when they support
  execution rationale or findings
- no system may absorb evidence ownership from VEDA by storing a
  richer or more authoritative version of the same evidence locally

### Rule
Evidence ownership stays with VEDA.
Planning-side or execution-side references to evidence are references,
not ownership transfers.
A reference to a VEDA evidence record is not a substitute for the record.

---

## Evidence Reference Rule

When a governing decision, planning record, or operational judgment
references evidence, that reference must be sufficient to allow later
review to:

- identify what evidence was referenced
- locate or reconstruct the evidence record through the system that owns it
- understand the trust posture that applied at the time of reference
- determine whether the evidence has since become stale or been superseded

### Rule
A vague reference to evidence is not a governed reference.
"Based on available data" without specificity is not traceable evidence
reference.
A governing context that cannot identify what evidence it relied on cannot
be fully reviewed or audited later.

---

## Evidence Loss Rule

Evidence that was used in a governing context must not be lost,
made inaccessible, or silently discarded.

Evidence loss occurs when:

- the evidence record is deleted without a governed retention decision
- the source system that owned the evidence is decommissioned without
  migration of evidence continuity
- a session-level evidence reference exists but the underlying record
  is not preserved in a durable governed system
- evidence is stored only in transient context and cannot be retrieved
  by later sessions

### Rule
Evidence continuity requires durable preservation, not session-level memory.
If evidence that supported a governing decision cannot be retrieved later,
the decision's evidence basis has been silently degraded.

At minimum, durable preservation means the evidence record can be retrieved
by a later session or reviewer without relying on the memory of the session
that created it.
Evidence stored only in session context, only in ephemeral compute, or only
in a location not accessible through the governed system that owns it does
not satisfy the durability requirement.
Durable preservation is consistent with the doctrine-vs-operational-state split: evidence records are operational state and belong in the database, not in session context or doc files. See `../ecosystem/doctrine-vs-operational-state.md`.
Where VEDA owns the evidence, VEDA's storage is the authoritative preservation
location.
Evidence referenced by Project V or V Forge must remain retrievable through
VEDA, not only through the referencing system's local copy.

---

## Evidence and Agent Behavior Rule

Agents must preserve evidence continuity when working with evidence
in any governed context.

This means agents must:

- reference evidence by its traceable identity, not by summary or paraphrase
  alone when the specific evidence record matters
- preserve trust posture and freshness context when packaging evidence
  for consumption by other systems or operators
- not present derived interpretation as raw evidence
- not present low-trust evidence as high-trust evidence
- surface staleness or provenance gaps rather than proceeding as though
  evidence quality is established

Agents must not:

- invent evidence provenance where it is unknown
- discard evidence quality context to produce a cleaner-looking summary
- treat their own in-session reasoning as evidence for governing purposes
- absorb evidence ownership by storing richer local copies than VEDA owns

---

## Evidence Continuity Failure Modes

Evidence continuity has failed when:

- governing decisions reference evidence that can no longer be located
  or reconstructed
- evidence trust posture was not preserved and cannot be recovered
- raw evidence and planning-side interpretation have been conflated
  into one record with no distinguishing markers
- stale evidence was treated as current without staleness being flagged
- evidence provenance is anonymous or cannot be traced to a source
- an agent presented in-session reasoning as evidence for a governing decision
- a planning-side summary of VEDA evidence displaced the actual VEDA
  observable record as the governing reference
- evidence was silently lost when a system or session ended

---

## Relationship to VEDA

VEDA is the canonical evidence system of record inside the V Ecosystem.

Evidence continuity depends on VEDA fulfilling its role:

- VEDA preserves source provenance and trust posture for observatory records
- VEDA preserves append-friendly observation history where time matters
- VEDA does not silently overwrite historical observatory reality
- VEDA preserves event auditability for meaningful observatory state changes

This governance doc establishes the ecosystem-level obligation for
evidence continuity.
The VEDA-specific implementation of that obligation is defined in:

- `../veda/system-invariants.md`
- `../veda/evidence-and-source-provenance.md`
- `../veda/data-boundaries.md`

---

## Human-In-The-Loop Principle

Evidence continuity is governance-sensitive because governing decisions
made on evidence that cannot later be traced, qualified, or reviewed
produce accountability gaps.

Human review may be required when:

- evidence used in a governing decision has become materially stale
- evidence provenance cannot be established for evidence already in use
- evidence trust posture appears to have been overclaimed
- a governing decision's evidence basis is being reviewed for revalidation
- new evidence materially contradicts evidence that supported a prior
  governing decision

Evidence continuity exists to make human review meaningful.
If evidence cannot be traced, human review of the decisions it supported
is weakened.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- evidence must remain traceable to its source throughout its use
- trust posture and freshness must remain visible, not stripped for cleanliness
- raw evidence and derived interpretation are distinct and must stay distinct
- planning-side references to VEDA evidence are references, not ownership
- in-session reasoning is not evidence for governing purposes
- stale evidence creates a revalidation obligation, not automatic invalidation

If an LLM presents a planning-side summary as the authoritative evidence
record, or discards trust posture to produce a cleaner output, this
doctrine is failing.

---

## Usage

This document should be used:

- when evaluating whether evidence used in a governing context is
  adequately traceable and honest
- when reviewing whether evidence provenance and trust posture have
  been preserved through a cross-system workflow
- when determining whether stale evidence triggers a decision revalidation
  obligation
- when reviewing whether an agent has correctly preserved evidence
  continuity in packaging or reporting
- when writing evidence-handling rules in VEDA, Project V, or V Forge
  specific docs

---

## Related Docs

- `decision-continuity-doctrine.md`
- `invalidation-and-supersedence-doctrine.md`
- `approval-and-escalation-model.md`
- `agent-operating-doctrine.md`
- `allowed-agent-actions-matrix.md`
- `report-structure-and-required-fields.md`
- `paid-data-pull-governance.md`
- `../veda/veda.md`
- `../veda/system-invariants.md`
- `../veda/evidence-and-source-provenance.md`
- `../veda/data-boundaries.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../ecosystem/cross-system-boundaries.md`
