# First Project — Draft Execution-Scoped Planning Digest (Exercise)

## 1. Purpose

This file is a proving-case exercise for the execution-scoped planning digest
concept. It derives a plausible draft digest from the gift discovery first-
project planning materials and tests whether the digest spec is workable
against actual planning content.

It exists to:
- produce a concrete candidate digest for the first execution pass
- test each included item against the spec's admission criteria
- identify items that are too load-bearing for the digest (belong in the
  execution packet) or too broad (belong in Canonical Authority later)
- expose whether the digest concept adds real value for this project or is
  barely needed

This is not a governed handoff artifact.
It is not approved for use in a real handoff.
It is a transition-support exercise only.

---

## 2. Status

Transition-support exercise only.

This file is:
- grounded in the current first-project planning materials
- produced for spec validation, not operational use
- not an admitted planning packet, execution packet, or Canonical Authority doc
- subject to revision after the first project is formally taken through intake

---

## 3. Draft Execution-Scoped Planning Digest

> **For:** Entity-driven gift discovery site — v1 execution pass
> **Produced at:** Handoff creation (simulated for exercise purposes)
> **Status:** Draft exercise — not a governed artifact

---

### D1. Page-type allowlist

The following page types are the only types approved for v1 public indexable
publication:

- Product Detail Page
- Recipient Guide Page
- Occasion Guide Page
- Category Browse Page
- Recipient × Occasion pages — only where the pair has adequate product depth,
  real editorial framing, and explicit per-page approval
- Manually curated collection pages — only where explicitly approved

No other page type may be published as a public indexable URL by default.
Specifically excluded from v1 indexable surfaces by default: Interest-only
pages, Price-only pages, Recipient × Interest pages, Category × Recipient
pages, three-way intersection pages, filter-state pages.

---

### D2. Anti-page-explosion rule

Not every taxonomy relationship or filter state may be published as a durable
public page. A public page requires explicit editorial justification. Execution
must not treat "the combination is technically possible" as sufficient reason
to create a public URL.

Combinatorial page generation is forbidden. Each indexable page must be
individually approved, not derived from a taxonomy matrix.

---

### D3. Editorial-note requirement

Every product record must carry a human-written editorial note. Generated prose
is not a substitute. Execution must not produce or publish a product record
whose editorial note is absent, placeholder, or LLM-generated without human
review.

This requirement is not decorative. It is a structural rule for v1.

---

### D4. Product relationship requirements

The following product → classification relationships are required for v1:

- Product → Category: required for every product
- Product → Recipient: required for every product

The following are optional:

- Product → Occasion: optional
- Product → Interest: optional

Price band is a derived filter facet, not a primary stored relationship and
not a page-generation engine. It must not be modeled as a peer classification
object or used to generate standalone indexable pages.

---

### D5. Product is the only first-class durable object

Categories, Recipients, Occasions, and Interests are controlled vocabularies
or governed classification objects. They are not equal peer entities to Product
and must not be modeled or executed as such. Execution must not treat a
taxonomy term as a first-class content object that independently demands its
own page, record set, or execution workflow equivalent to a Product.

---

## 4. Included Items and Why They Pass

### D1 — Page-type allowlist

**Resolved?** Yes. The planning packet explicitly enumerates allowed and
excluded page types for v1. This is not aspirational — it is a stated
decision with explicit named exclusions.

**Execution-relevant?** Yes. Without this constraint, execution could
reasonably generate pages for Interest-only combinations, Recipient × Interest
intersections, or filter-state URLs. The allowlist directly constrains what
execution may produce.

**Not yet in Canonical Authority?** Correct. The allowlist lives in the
transition-support planning materials, not in a Canonical Authority doc.

**Auxiliary to an adequate execution packet?** Yes, if the execution packet
names the scope as "gift discovery site v1 page generation." The allowlist
supplements that scope without replacing it. An execution agent reading a
well-formed execution packet would still need the allowlist to know which pages
are in scope.

**Verdict: passes digest criteria.** This item is a strong candidate.

---

### D2 — Anti-page-explosion rule

**Resolved?** Yes. The planning packet states the rule explicitly and names
it as an anti-slop protection.

**Execution-relevant?** Yes. This rule prevents automatic page generation
from taxonomy combinations. Without it, an execution agent has no structural
constraint against combinatorial expansion.

**Not yet in Canonical Authority?** Correct. It lives in planning materials.

**Auxiliary?** This is the borderline case. The rule is short and concrete,
but it is *also* exactly the kind of structural constraint that should be in
the execution packet's "execution constraints and boundaries" field. An
execution packet for v1 page generation that does not state this rule is
arguably incomplete. If the execution packet is properly formed, D2 is
redundant in the digest.

**Verdict: passes digest criteria — but borderline.** This item should be
in the execution packet. It appears here as auxiliary carry-forward only
because the execution packet has not yet been written. If the execution packet
is written well, D2 drops out. See Section 7.

---

### D3 — Editorial-note requirement

**Resolved?** Yes. The planning packet calls this out as explicit and
structural: "every product carries a genuine human-written editorial note."

**Execution-relevant?** Yes. This directly constrains how product records
are produced and what the harness or execution agent must ensure before
a product record is considered complete.

**Not yet in Canonical Authority?** Correct.

**Auxiliary?** Like D2, this is a constraint that belongs in the execution
packet's constraints field for a content execution scope. But it is concrete
enough and specific enough to a first-project decision (as opposed to a
general ecosystem rule) that it could legitimately appear in the digest as
a temporary carry-forward while Canonical Authority docs are absent.

**Verdict: passes digest criteria — borderline, same as D2.** Should
eventually move to the execution packet or Canonical Authority. Not planning
bleed. Defensible as a digest item for the first project exercise.

---

### D4 — Product relationship requirements

**Resolved?** Yes. The planning packet specifies required vs. optional
relationships clearly.

**Execution-relevant?** Yes. An execution agent building product records
needs to know which relationships are required before a record is considered
valid.

**Not yet in Canonical Authority?** Correct.

**Auxiliary?** This is the cleanest digest item. It is a narrow, specific,
resolved constraint list that supplements scope without replacing it. An
execution packet saying "build product records for v1" does not by itself
tell the execution agent which relationships are required.

**Verdict: passes digest criteria cleanly.** Genuinely auxiliary. Good
digest material.

---

### D5 — Product is the only first-class durable object

**Resolved?** Yes. The planning packet is explicit: categories, recipients,
occasions, and interests are controlled vocabularies, not peer entities.

**Execution-relevant?** Yes, but this is the most abstract item in the
digest. The constraint matters when execution is modeling the data layer or
deciding how to structure page generation logic. It is less directly
constraining on a per-task basis than D1–D4.

**Not yet in Canonical Authority?** Correct.

**Auxiliary?** This is a structural modeling rule. It would be better placed
in an execution packet that explicitly defines the entity model for v1 than
in a digest that supplements an already-defined scope. Without an execution
packet that defines the entity model, D5 is load-bearing, not auxiliary.

**Verdict: borderline — may belong in execution packet rather than digest.**
If the execution packet defines the entity model (which it should for a
content execution scope of this complexity), D5 is redundant in the digest.
If the execution packet omits the entity model, D5 is plugging a gap in the
execution packet, which is precisely what the digest must not do. See
Section 7.

---

## 5. Deliberately Excluded Items and Why

### Project thesis and strategic rationale
Why entity-driven discovery was chosen over generic affiliate blogging, why
the project is the first proving ground, the claims the project must validate.
**Excluded:** This is planning context, not execution constraint. No
execution decision depends on knowing the strategic rationale.

### Kill / pivot conditions
The conditions under which the project should be paused, pivoted, or closed.
**Excluded:** These are planning governance rules, not execution constraints.
Execution does not need to know kill conditions to execute correctly. Loading
kill conditions into execution context would be planning framing smuggled in.

### Open questions from the planning packet
Single vs. multi-merchant, whether VEDA observation starts at v1, editorial
capacity confirmation, decay-handling cadence.
**Excluded:** These are unresolved planning questions. By definition they
must not appear in the digest (a core spec rule: unresolved items are
forbidden). If any of these must be resolved before execution begins, the
handoff is not ready.

### v1 success conditions
What "early success" looks like, the proving-ground success posture.
**Excluded:** Success framing is planning evaluation context. Execution does
not need to know what success looks like to execute correctly. This would
bias execution toward optimizing for success criteria rather than executing
against structural rules.

### Branded-network and offsite distribution posture
The site as canonical branded layer, future offsite reinforcement.
**Excluded:** Explicitly deferred from v1 execution scope. Even if relevant
to the project shape, it is not an execution constraint for the current pass.

### Monetization posture and anti-patterns
Affiliate link mechanics, anti-patterns to avoid.
**Excluded:** Monetization posture is planning and product framing. The
structural constraint (affiliate links are subordinate structured records,
not free-floating content fragments) is closer to a legitimate digest item,
but it is better placed in the execution packet's scope definition for
affiliate link handling. It is not a standalone carry-forward constraint.

### Editorial philosophy and curation framing
Why curation matters, what good editorial judgment looks like, why the site
must not become affiliate sludge.
**Excluded:** This is exactly the planning framing that the digest spec says
must not appear. The rule (D3 — every product requires a human-written
editorial note) is in the digest. The framing behind the rule is not.

### Product lifecycle and decay posture
Operational lifecycle states, review cadence, decay as a systems concern.
**Excluded:** Lifecycle states and decay posture are operational planning
and execution design questions that belong in the execution packet or in
V Forge execution doctrine, not in a carry-forward digest. If execution
needs to know the lifecycle model, that model belongs in the execution scope
definition.

---

## 6. Judgment on Draft Viability

The draft digest is viable but thinner than the planning materials might
suggest. Five items were identified. Of those:

- **D4** (product relationship requirements) passes cleanly as a genuine
  auxiliary digest item.
- **D1** (page-type allowlist) passes with confidence as a strong digest item.
- **D2** (anti-page-explosion rule) and **D3** (editorial-note requirement)
  pass the criteria but are borderline — both should be in the execution
  packet's constraint fields, and will drop out of the digest once the
  execution packet is properly formed.
- **D5** (product as only first-class durable object) is the most suspect
  item. It is a structural modeling rule that is load-bearing if the
  execution packet does not define the entity model. If D5 is in the
  digest because the execution packet omits the entity model, D5 is
  compensating for a weak execution packet, not supplementing a strong one.

**The exercise reveals a useful signal:** most of the digest's contents are
items that should be in the execution packet. The digest is functioning here
as a placeholder for an execution packet that has not yet been written. That
is a normal first-pass result, but it confirms the spec's warning: repeated
digest dependence signals an underspecified execution packet.

The draft is not planning bleed. No forbidden content was included. The
excluded items section is much longer than the included items section, which
is the expected shape for a well-governed digest.

---

## 7. What May Belong in the Execution Packet Instead

The following digest items are strong candidates for execution packet
relocation once the execution packet for v1 is formally drafted:

**D2 — Anti-page-explosion rule**
This is a structural execution constraint that belongs in the execution
packet's "execution constraints and boundaries" field. An execution packet
for v1 page generation that omits this rule is incomplete. When the execution
packet is written, D2 should move there and be removed from the digest.

**D3 — Editorial-note requirement**
Same reasoning as D2. A content execution scope for v1 product records should
explicitly require a human-written editorial note as part of the product
record definition. When the execution packet defines that record shape, D3
moves there.

**D5 — Product as only first-class durable object**
If the execution packet defines the entity model for v1 (which it should for
a content execution scope of this complexity), D5 is redundant in the digest.
If it does not define the entity model, that is the gap to close — the right
response is to fix the execution packet, not to keep D5 in the digest.

**Conclusion:** A well-formed execution packet for v1 would absorb D2, D3,
and D5. The digest for a well-formed handoff would contain only D1 and D4 —
the page-type allowlist and the product relationship requirements. That is a
very short digest, which is the expected result of a strong execution packet.

---

## 8. What May Belong in Canonical Authority Later

These digest items are candidates for eventual promotion to Canonical Authority
docs, at which point they would be excluded from the digest entirely
(Canonical Authority content must not be restated in the digest):

**D2 — Anti-page-explosion rule (generalized)**
This rule — combinatorial page generation requires per-page editorial
justification — is not first-project-specific. It is a structural doctrine
for any content site operated under V Forge. It belongs in a V Forge content
execution doctrine doc or a cross-ecosystem content governance doc.

**D3 — Editorial-note requirement (generalized)**
The requirement that human-authored editorial content must accompany
structured product records is also a generalizable content execution rule.
It belongs in V Forge execution doctrine when that doctrine is formalized.

**D1 — Page-type allowlist (project-specific)**
The v1 page-type allowlist is specific to this project's v1 scope. It is not
a generalizable rule. It does not belong in Canonical Authority — it belongs
in the execution packet for this specific handoff scope. It is not a candidate
for promotion.

**D4 — Product relationship requirements (project-specific)**
Like D1, this is specific to the gift discovery site's data model. It is not
a generalizable rule for all projects. It belongs in the execution packet for
this specific handoff scope, not in Canonical Authority.

**D5 — Product as only first-class durable object (case-by-case)**
This is a first-project modeling decision. Whether it generalizes depends on
whether future V Forge execution doctrine addresses entity modeling for content
sites. It is a candidate for project-specific execution doctrine, not a clear
Canonical Authority item yet.

---

## 9. Open Cautions

**The draft digest was produced without a real execution packet.**
The exercise simulated the handoff creation stage, but no actual execution
packet exists for the first project. Several digest items (D2, D3, D5) would
drop out if the execution packet were properly formed. The digest's size is
partly an artifact of the missing execution packet, not evidence that the
digest concept is broadly needed.

**D5 carries load-bearing risk.**
If execution agents need the entity model to proceed correctly, D5 is not
auxiliary — it is a fundamental execution definition. That makes it either
an execution packet item or Canonical Authority material, not a digest item.
It was included here to surface this tension explicitly. If a real digest
is produced, D5 should be removed and placed in the execution packet.

**The anti-explosion rule and editorial-note requirement are structurally
important enough to warrant their own governing path.**
Both should be V Forge content execution doctrine. Their presence in a
transition-support digest is temporary and should not normalize the pattern
of carrying structural rules in digests indefinitely.

**The digest exercise confirms the spec warning:**
A well-formed execution packet would absorb most of what this draft digest
contains. The digest should be expected to shrink toward D1 and D4 only once
the execution packet is properly drafted.

---

## 10. Recommended Next Move

1. Draft the execution packet for the first project's v1 page generation
   scope. The natural test: if D2, D3, and D5 can be absorbed cleanly into
   the execution packet's constraint fields, the digest shrinks to D1 and D4.
   That is the correct outcome.

2. After the execution packet draft exists, re-run this digest exercise against
   it to confirm that the digest is genuinely auxiliary (supplements the packet)
   rather than compensating for it (plugging packet gaps).

3. Flag D2 (anti-explosion rule) and D3 (editorial-note requirement) as
   candidates for V Forge content execution doctrine. These are structural
   rules that should not require a project-specific carry-forward artifact
   once the doctrine exists.

4. Do not use this draft digest as a real handoff artifact. The approval scope
   ambiguity (noted in the digest spec's open questions) and the missing
   execution packet both mean this is not ready for a governed handoff.

---

## 11. Related Files

- `execution-scoped-planning-digest-spec-note.md`
- `../first-project-entity-driven-gift-discovery-site.md`
- `../first-project-entity-driven-gift-discovery-planning-packet.md`
- `doctrine-aware-context-model-design-pass.md`
- `doctrine-aware-context-enforcement-and-inspectability-note.md`
- `../../project-v/project-v.md`
- `../../v-forge/v-forge.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md`
