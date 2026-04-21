# Execution-Scoped Planning Digest — Spec Note

## 1. Purpose

This note specifies the execution-scoped planning digest: what it is, what it
may contain, what it must not contain, when it should exist, and how it fits
the doctrine-aware context-loading model without becoming a loophole for
planning packet bleed into execution.

It exists because the context-model design pass and the enforcement /
inspectability note both named this artifact as an open gap. Without a bounded
spec, the execution stage either:

- loads the planning packet under a softer label, defeating the exclusion rule
- operates without distilled planning-side constraints that genuinely must
  survive handoff, which produces a different kind of execution error

This note defines the narrow middle ground between those two failure modes.

---

## 2. Status

Transition-support spec note only.

This note is:
- concrete enough to close the named open gap in the context-model work
- not final doctrine
- not a new canonical artifact class
- not a replacement for the planning packet, execution packet, or continuity
  model
- subject to revision after the first project exercises the model

---

## 3. Problem Being Solved

The context-model design pass establishes that the planning packet must not be
admitted to execution-stage context. The rationale is clear: planning packets
contain strategic rationale, open questions, provisional alternatives, and
intent framing — material that would bias execution toward re-litigating
planning rather than executing the decided outcome.

But planning also produces binding decisions and constraints that execution
must know. Some planning-side decisions are not strategic framing — they are
resolved outcomes that constrain what execution may and may not do. Encoding
those into the execution packet at handoff creation is the right path and
remains the primary path. The handoff interface (`project-v-to-v-forge-handoff-
interface.md`) already requires execution constraints and boundaries as a
mandatory semantic field of every handoff package. Where a small number of
specific, resolved planning-side constraints require an explicit carry-forward
beyond what the execution packet alone expresses — particularly constraints
that are not yet promoted to Canonical Authority docs — the digest provides
a narrow, governed path for that carry-forward.

The risk without a digest: specific resolved planning-side constraints that
are not yet in Canonical Authority docs get re-derived from scratch at execution
or the planning packet gets loaded anyway (planning bleed).

The risk with a poorly defined digest: it becomes "the planning packet with
a new label," encoding the same strategic breadth and bias under the softer
claim that it was "scoped for execution."

The spec must prevent both.

---

## 4. Definition

The execution-scoped planning digest is:

> A deliberately prepared, execution-safe carry-forward of specific planning
> decisions and binding constraints that (a) were resolved during planning,
> (b) directly govern what execution may or may not do, (c) are not yet
> promoted to Canonical Authority docs, and (d) require explicit statement
> beyond what the execution packet alone expresses.

**The execution packet remains the primary carrier of execution truth.** The
digest is subordinate and supplementary. A constraint that should be in the
execution packet belongs in the execution packet. The digest is not where
unenconded execution substance lives by default — it is a narrow, temporary
carry-forward for planning-settled constraints that are not yet in Canonical
Authority and that are auxiliary to an already-adequate execution packet.

It is not a summary of the planning packet. It is not planning memory. It is
a bounded list of resolved, execution-relevant constraints and approved
decision outcomes.

Key properties:

- **Resolved only.** It contains outcomes, not open questions, alternatives,
  or strategic rationale.
- **Execution-relevant only.** It contains only what execution needs in order
  to proceed correctly. If a constraint does not affect execution decisions,
  it does not belong in the digest.
- **Deliberately prepared.** It is not auto-generated from the planning packet.
  It is explicitly authored as a governance act at handoff creation, by the
  agent or operator responsible for handoff.
- **Bounded.** It is expected to be short. If it is long, it is probably doing
  the planning packet's job, not its own.
- **Single-direction.** It flows into execution context. It does not return
  to planning, does not feed validation, and does not become a continuity
  artifact for later stages.

---

## 5. When the Digest Should Exist

### It is produced at handoff creation

The digest is produced during handoff creation, not before and not at execution
start. It is part of the handoff package — a companion to the execution packet,
not a substitute for it.

Handoff creation is the right stage because:
- planning decisions are settled by then
- the execution packet is being assembled at the same time, so gaps can be
  addressed directly before execution begins
- the operator responsible for handoff can review and authorize both the
  execution packet and the digest as a paired governance act

The digest must not be assembled retroactively after execution has started. If
execution begins without a needed digest, the right response is to pause,
assemble the digest through handoff creation discipline, and then continue —
not to load the planning packet as a fallback.

### It is conditional, not mandatory

The digest is only needed when specific resolved planning-side constraints are
not yet encoded in Canonical Authority docs and are not fully expressed in the
execution packet. If the execution packet is complete and self-contained, no
digest is needed and none should be produced.

The digest is not a compensating mechanism for a weak execution packet.
If a constraint matters to execution correctness, the primary response is
to encode it in the execution packet, not to carry it in a digest. The digest
may carry a small number of not-yet-promoted constraints that are genuinely
auxiliary to an already-adequate execution packet. It must not compensate
for a materially incomplete handoff.

### When it is not needed

- When the execution packet explicitly encodes all binding planning constraints
- When execution work is purely mechanical and requires no planning-context
  constraints (rare, but possible for isolated tasks)
- When the planning-side constraints are already encoded in Canonical Authority
  docs that execution will load independently

In these cases, producing a digest is unnecessary overhead and introduces a
risk that it drifts from the actual execution packet content.

---

## 6. Relationship to Adjacent Artifacts

This section matters. The digest only works if it stays sharply distinct from
the things it is not.

### vs. Planning Packet

The planning packet is the full planning-side record: thesis, constraints,
success conditions, open questions, kill conditions, cross-system implications,
and strategic framing. It is rich, contextual, and intentionally broad.

The digest is none of those things. It contains only resolved outcomes
and binding constraints. It excludes thesis material, strategic framing, open
questions, rationale, and anything that did not produce a binding decision.

The test: if removing a sentence from the digest would mean execution could
not operate correctly, it belongs. If removing it would only mean execution
had less context or framing, it does not belong.

### vs. Execution Packet

The execution packet is the primary execution-stage truth carrier. It is
assembled by the handoff process, governed by V Forge, and defines the scope,
target, approved work, and execution constraints for the execution stage. Per
the handoff interface doc (`project-v-to-v-forge-handoff-interface.md`),
execution constraints and boundaries are a required semantic field of every
valid handoff package. The execution packet is the authority artifact for what
execution does and what constrains it.

The digest is strictly subordinate to and supplementary to the execution packet.
It does not define scope. It does not authorize new work. It does not carry
constraints that belong in the execution packet. It carries a narrow set of
planning-settled constraints that are not yet in Canonical Authority docs and
that are auxiliary to — not replacements for — the execution packet's own
content.

**The digest must not become where real execution instructions live.** If the
content in the digest is load-bearing for execution correctness, that content
belongs in the execution packet. A digest carrying primary execution instruction
is a shadow execution packet, and that failure mode is explicitly named in
Section 12.

If the execution packet already encodes the constraint, the digest must not
repeat it.

### vs. Continuity Artifact

Continuity artifacts are runtime memory products — session notes, working
hypotheses, compact-boundary products. They are produced during session work
and are non-authoritative.

The digest is not produced during session work. It is produced as a governed
act at handoff creation. It is explicitly authorized, not assembled from
session memory. It carries more weight than a continuity artifact because it
was deliberately prepared and reviewed as part of the handoff — but that weight
is strictly bounded to the execution stage.

The digest must not be confused with or stored as a continuity artifact. They
have different production paths, different authority postures, and different
validity scopes.

### vs. Inert Model Output

Inert model output is uncommitted LLM output that has not been admitted to a
canonical system. A draft, a brainstorm, an unapproved recommendation.

The digest is not inert. It is explicitly authorized as part of a governed
handoff. However, it is also not canonical system truth — it is an execution-
stage support artifact, explicitly temporary and bounded to that stage.

### vs. Transition-Support Notes

Transition-support notes are advisory working material — notes, inventories,
working hypotheses, background framing. They do not carry binding authority
and are never mandatory context for any stage.

The digest carries binding constraints. That is the core difference. A
transition-support note says "here is useful background." The digest says
"this constraint was decided in planning and must govern execution."

That difference is also why the digest must be produced deliberately, not
accumulated organically from session notes.

---

## 7. Allowed Contents

The following categories of content may appear in the execution-scoped planning
digest:

**Resolved binding constraints on execution scope or method**
Decisions made in planning that explicitly limit what execution may do or how
it may proceed. For example: constraints on which content patterns are
permitted, which output types are authorized, which publication targets are
in scope.

**Approved decision outcomes that execution must honor**
Specific choices that were made in planning and that execution must treat as
settled. Not the rationale for those choices — just the outcome. For example:
a decision about the canonical page structure, a decision about required
editorial note presence, a decision about anti-explosion rules.

**Not-yet-promoted structural rules that supplement the execution packet**
Rules that (a) were explicitly resolved in planning, (b) are not yet encoded
in Canonical Authority docs, and (c) are not already stated in the execution
packet. All three conditions must be true. Rules that belong in Canonical
Authority or that the execution packet already covers must not appear here.
These contents are temporary candidates for Canonical Authority promotion,
not a permanent supplement layer.

**Narrow execution packet disambiguation**
Where the execution packet is genuinely ambiguous about a specific scope
boundary, a brief statement from planning that resolves that specific ambiguity.
The ambiguity must be real and identified, not a general sense that more
context would help. This is not a license for additional framing or context—
it is a narrow clarification of a stated execution packet term.

**What is explicitly not allowed here:** see Section 8.

---

## 8. Forbidden Contents

The following must not appear in the execution-scoped planning digest:

**Open planning questions**
If a question was not resolved in planning, it does not belong in the digest.
Loading an unresolved question into execution context is planning work smuggled
into execution. If a question must be resolved before execution, the handoff
is not ready.

**Strategic rationale or thesis material**
Why the project exists, why a particular approach was chosen, what the project
hopes to prove — none of this belongs in the digest. Execution does not need
to understand the strategy; it needs to know what was decided.

**Speculative alternatives or hedge language**
"We considered X but decided Y" is a planning discussion, not an execution
constraint. The digest carries the decision (Y), not the deliberation.

**Planning-packet breadth in any compressed form**
A condensed version of the full planning packet is still a planning packet.
If the content reads like "here is what the planning packet said, but shorter,"
it is not a digest — it is a violation of the exclusion rule in a different
container.

**Anything that was not resolved and approved during planning**
If it is provisional, under discussion, or operator-preference-only, it does
not belong. The digest carries settled governance decisions, not working
assumptions.

**Validation-relevant framing**
Anything that would bias a validator's assessment of execution outputs toward
what was intended rather than what was produced against canonical rules must
not appear. Framing like "the intent was to produce X style of output"
is the kind of planning intent that the validation-independence rule exists
to prevent.

**Material already encoded in Canonical Authority**
If the constraint is already stated in a Canonical Authority doc that execution
will load independently, restating it in the digest is redundant and creates
a risk that the digest version drifts from the authoritative version.

---

## 9. Authority and Class Posture

### What class does the digest belong to?

The digest does not fit cleanly into any single existing class without
qualification. The most honest classification is a constrained sub-type of
the Execution Packet class — it is a companion input to the execution packet,
produced under handoff creation discipline, carrying execution-stage binding
authority, but not itself the primary scope and authorization record.

If the class model must place it precisely: it is admitted to the execution
stage as a **selective** Execution Packet companion, below the execution
packet itself in authority, above transition-support notes, and explicitly
excluded from all other stages.

It is not Canonical Authority. If constraints in the digest are important
enough to become ecosystem-wide rules, they should be promoted to the
appropriate Canonical Authority doc — not left in the digest permanently.

### Authority weight

Within the execution stage:
- Canonical Authority outranks the digest
- The execution packet outranks the digest
- The digest outranks transition-support notes
- The digest outranks continuity artifacts

The digest does not override Canonical Authority. If a digest constraint
conflicts with a Canonical Authority rule, the Canonical Authority rule wins
and the digest constraint should be flagged as inconsistent at the point of
discovery, not silently absorbed.

### Is it part of the execution packet?

No. It is a companion artifact. The execution packet defines scope and
authorized work. The digest carries distilled planning constraints that
support the execution packet's use. They are related but distinct.

Treating the digest as part of the execution packet would blur the question
of what governs execution scope (the execution packet) and what constrains
execution method (a combination of Canonical Authority, execution packet,
and digest). The distinction is worth preserving.

---

## 10. Admission and Loading Posture

### When execution may load it

The digest is admitted to execution-stage context as a selective item, only
when it was deliberately produced at handoff creation and explicitly included
in the handoff package. An execution stage that finds no digest in the handoff
package does not go looking for one. Absence of a digest is not a problem to
solve by loading the planning packet.

### Mandatory or selective?

Selective. Not every execution stage needs a digest. It is loaded when present
and when the execution agent needs the distilled planning constraints it carries.

### What must be true before it is admitted

- It was produced during handoff creation, not retroactively
- It has been reviewed as part of the handoff package — it is not a
  self-generated artifact
- It does not contain any of the forbidden contents defined in Section 8
  (this is a check the harness or handoff preparation process should run)
- It is scoped to the current execution task — a digest produced for a prior
  execution scope is not automatically valid for a different scope

### Exclusion from validation

The digest must be explicitly excluded from the validation stage. It is an
execution-stage artifact that carries planning-side framing, even in its
constrained form. That framing, however carefully scoped, would bias a
validator toward what was intended rather than what must be evaluated against
canonical rules.

The load record for the validation stage should show the digest in the excluded
set with the exclusion reason: `validation-independence`.

### Appearance in load records

In the execution-stage load record, the digest should appear in the admitted
set with:
- class: `execution-packet-companion` (or the closest available class label)
- admission-basis: `selective`
- carried-from-prior-stage: `no` (it was produced at handoff creation; it
  does not carry forward from execution into later stages)

In the validation-stage load record, the digest should appear in the excluded
set with exclusion-reason: `validation-independence`.

It should not appear in planning-stage, observation-return, or
publication-stage load records.

---

## 11. First-Project Proving-Case Mapping

### Does the gift discovery first project need a digest?

Probably yes, for a narrow set of constraints. The planning materials for the
first project contain several explicit structural rules that are binding on
execution but are stated in planning-side framing docs rather than in Canonical
Authority docs:

- the anti-page-explosion rule (not every taxonomy combination deserves a
  public page)
- the editorial-curation-is-load-bearing rule (every product carries a genuine
  human-written editorial note; curation must not collapse into metadata)
- the page-type allowlist for v1 (which page types are in-scope for indexable
  publication)
- the product-first-class-object rule (categories, recipients, occasions are
  controlled vocabularies, not equal peer entities)

These were decided in planning, are explicitly binding on execution, and are
exactly the kind of constraint that execution needs to know without needing
the full planning packet context.

### What would legitimately belong in the digest for this project

A digest for the gift discovery project's first execution pass might contain:

- the explicit v1 page-type allowlist (Product Detail, Recipient Guide,
  Occasion Guide, Category Browse, selected Recipient × Occasion with
  justification, selected manual collections — no others by default)
- the anti-explosion rule stated as a constraint: combinatorial pages are
  forbidden; each public page requires explicit editorial justification
- the editorial-note requirement: every product record requires a human-written
  editorial note; generated prose is not a substitute
- the product relationship requirements: Product → Category required;
  Product → Recipient required; others optional

These are resolved decisions from planning. They directly constrain what
execution may do. They are not present in the current Canonical Authority docs
(they live in transition-support planning materials). They are exactly the
category the digest is designed to carry temporarily.

### What must stay only in planning materials

- Why an entity-driven discovery model was chosen over a generic affiliate blog
- The kill/pivot conditions
- The open questions (single vs. multi-merchant, VEDA observation timing)
- The project thesis claims
- The strategic rationale for keeping v1 small
- The branded-network posture and offsite distribution plans

None of these affect execution decisions. They are planning context, not
execution constraints. They must stay in the planning packet.

### Where planning bleed risk is highest for this project

The editorial layer is the highest risk. The planning materials contain
nuanced framing about curation quality, the editorial voice the site should
have, and why the editorial layer is load-bearing. That framing is useful
for planning. At execution, it risks producing a situation where the
executing agent is trying to match planning's editorial *intent* rather than
executing against the editorial *rules*.

The digest should carry the rule (every product requires a human-written
editorial note; generated prose is not a substitute) without carrying the
framing (here is what good editorial judgment looks like, here is why
curation matters, here is the risk if we become affiliate sludge).

The rule constrains execution. The framing is planning context. Only the rule
belongs in the digest.

---

## 12. Failure Modes Prevented

### Planning packet bleed under a softer label
The most direct failure. The digest spec prevents this by requiring that content
be resolved, execution-relevant, and deliberately prepared — not compiled by
summarizing planning narrative. The forbidden-contents list is the primary
enforcement mechanism for this failure mode.

### Execution blindness due to missing distilled decisions
The complement failure. Without the digest concept, the only choices are
"load the planning packet" or "execution infers from the execution packet
alone." The digest provides a third path: explicitly distilled binding
constraints that close the gap in the execution packet without opening
the planning packet.

### Pseudo-digest that is really a compressed planning packet
A digest that contains strategic rationale, open questions, thesis material,
and general project framing, just in a shorter form. The allowed-contents
and forbidden-contents sections directly address this. The "test" from Section 6
(does removing this sentence break execution, or only reduce context?) is the
practical check.

### Digest reused in validation
Addressed directly in the admission and loading posture. The digest must
appear in the excluded set at validation with the `validation-independence`
exclusion reason. If it appears in the admitted set at validation, that is
a validation-contamination event detectable in the load record.

### Digest becoming shadow doctrine
This failure mode occurs when constraints in the digest are never promoted to
Canonical Authority, remain in the digest indefinitely, drift from the actual
execution intent, and start to be treated as stable doctrine. The spec prevents
this by: (a) explicitly calling digest contents candidates for Canonical
Authority promotion, (b) bounding the digest to a single execution-stage scope,
and (c) noting that a digest produced for a prior execution scope is not
automatically valid for a different scope.

### Digest assembled retroactively or from session memory
This would convert a carefully governed artifact into a continuity artifact
in everything but name. The spec prevents this by requiring production at
handoff creation, as a governed act, with operator review as part of the
handoff package.

### Digest becoming a shadow execution packet
This failure mode occurs when the digest carries primary execution instructions
that should be in the execution packet — scope interpretation, core task
specification, output requirements — and the execution packet becomes a
nominal container while the digest does the real work. The spec prevents this
by: (a) defining the digest as supplementary only, (b) requiring that
primary constraints belong in the execution packet, (c) stating that digest
contents load-bearing for execution correctness signal a handoff quality
failure, not a reason to use the digest, and (d) limiting digest contents
to not-yet-promoted auxiliary constraints and narrow execution packet
disambiguation only.

---

## 13. Open Questions

**Governance of the production process**
This spec names handoff creation as the production stage and requires operator
review, but does not define the exact governance path. What workflow step in
handoff creation produces the digest? Does it require a specific BYDA audit
type? Does it require the operator to explicitly sign off as part of the
handoff package approval? These are open and should be addressed in the
handoff interface docs or a future workflow refinement.

**Alignment with the handoff interface — partial, no contradiction**
This spec note was checked against `interfaces/project-v-to-v-forge-handoff-
interface.md`. Summary of findings:

- **No contradiction found.** The handoff interface does not forbid the digest
  concept. Its requirement that the package must not contain "planning state
  beyond what execution requires" is consistent with the digest's definition,
  which explicitly limits contents to what execution requires.
- **The digest is unaccounted for in the handoff interface's package model.**
  The interface defines required semantic fields for the handoff package but
  has no concept of a companion artifact. The digest is neither named as a
  required field nor prohibited as excess planning state. It sits in a gap.
- **Approval scope is ambiguous.** The handoff interface treats activation
  approval as applying to the handoff package as a whole. It does not address
  whether a companion artifact like the digest falls within or outside
  activation approval scope. If the digest is included in the handoff package
  for delivery, activation approval plausibly covers it. If it is a separate
  artifact delivered alongside the package, its approval status is undefined.
  This should be resolved before the digest is used in a governed handoff.
- **Who produces the digest is implied but unstated.** The handoff interface
  treats Project V as the producer and deliverer of the handoff package. Since
  the digest is produced at handoff creation (a Project V responsibility), it
  is implicitly a Project V output. But this is inferred, not stated in either
  doc. A future handoff interface refinement should name the digest explicitly
  if it is to be a governed optional component of the handoff package.
- **The strongest structural risk** is that the digest could be used to make
  a technically "complete" execution packet look complete while real execution
  constraints live in the digest. The handoff validity conditions require the
  package to be complete. The digest spec prevents this posturally but not
  structurally — there is no enforcement mechanism that prevents the pattern.
  This remains a judgment-based control until the handoff interface names
  the digest explicitly and scopes what it may carry.

Conclusion: The digest concept can proceed as transition-support without
conflicting with current handoff doctrine. It should not be promoted to
authority-level doctrine until the handoff interface is updated to account
for it explicitly, the approval scope is resolved, and the production
responsibility is stated rather than inferred.

**Promotion path for digest contents**
Some constraints in the digest should eventually be promoted to Canonical
Authority. Who initiates that promotion, through what process, and when?
Not defined here. A constraint that lives in digests indefinitely is a sign
that the authority layer is incomplete.

**Maximum useful length**
This note says the digest is "expected to be short" but does not define what
short means. A practical upper bound — either a line count or a constraint
category count — would help distinguish a legitimate digest from a disguised
planning packet. Not settled here; may be better addressed after the first
project produces an actual digest.

**Primary threshold between digest use and execution packet fix**
This spec says the digest must not compensate for a materially incomplete
execution packet. But the practical threshold — how to distinguish "narrow
auxiliary carry-forward" from "compensating for a weak package" — is not fully
defined here. A working test: if the digest contents are load-bearing for
execution correctness, they belong in the execution packet, and the handoff
is not ready. If the digest is absent and execution can still proceed correctly
from the execution packet alone, the digest is genuinely supplementary. The
practical evaluation of that boundary is a handoff discipline judgment that
should be governed in the handoff workflow docs, not in this spec note.

---

## 14. Recommended Next Move

1. The handoff interface alignment check has been completed (see Section 13).
   The digest concept is partially aligned — no contradiction, but unaccounted
   for in the interface's package model. Before the digest is used in a
   governed handoff, the approval scope ambiguity and production responsibility
   gap should be resolved. The handoff interface will need a refinement pass
   to name the digest explicitly as an optional companion component if it is
   to be a governed artifact. That work belongs in the handoff interface doc,
   not here.

2. Use the first-project proving case to produce an actual draft digest for
   the v1 execution pass. That exercise will test whether this spec holds up
   or requires revision. A draft digest produced against the forbidden-contents
   rules is a better test than abstract review.

3. Identify which digest contents (specifically the structural rules from Section 11)
   are candidates for promotion to Canonical Authority docs. The goal is to
   make the digest shorter over time — ideally unnecessary for most handoffs —
   not to normalize it as a permanent planning-to-execution conduit. Repeated
   digest dependence across handoffs is a signal that either the execution
   packet design is weak or Canonical Authority promotion is overdue. It should
   not be treated as a stable operating pattern.

4. Do not treat this spec note as final doctrine. It is a working spec that
   should be revised after first-project exercise.

---

## 15. Related Files

- `doctrine-aware-context-model-note.md`
- `doctrine-aware-context-model-design-pass.md`
- `doctrine-aware-context-enforcement-and-inspectability-note.md`
- `../first-project-entity-driven-gift-discovery-site.md`
- `../first-project-entity-driven-gift-discovery-planning-packet.md`
- `../transition-plan.md`
- `../../interfaces/llm-harness-architecture.md`
- `../../interfaces/desktop-memory-and-continuity-model.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md` (checked for
  alignment — partial, no contradiction; see Section 13 for findings)
- `../../project-v/project-v.md`
- `../../project-v/byda-in-project-v.md`
- `../../v-forge/v-forge.md`
- `../../governance/decision-continuity-doctrine.md`
