# First Project — Draft V1 Execution Packet (Exercise)

## 1. Purpose

This file is a proving-case exercise for the execution packet concept as applied
to the gift discovery first project v1 scope. It drafts what the execution packet
would need to contain so that:

- execution can proceed without loading the planning packet
- the digest can stay genuinely auxiliary (not compensatory)
- planning packet bleed is structurally unnecessary
- validation independence remains intact at the next stage

It exists to close the gap identified in the draft digest exercise: most of
the digest's items were structurally load-bearing content that belonged in the
execution packet, not in a supplementary carry-forward artifact.

This is not a governed handoff artifact.
It is not approved for use in a real handoff.
It is a transition-support exercise only.

---

## 2. Status

Transition-support exercise only.

This file is:
- grounded in the current first-project planning materials and the handoff
  interface semantic requirements
- produced for spec validation, not operational use
- not an admitted planning packet or governed execution record
- subject to revision after the first project is formally taken through intake
  and the execution packet is authored as part of a real handoff

---

## 3. Draft First-Project V1 Execution Packet

> **Handoff identity:** [to be assigned at real handoff creation]
> **Originating planning entity:** gift discovery site — v1 planning record
> **Target system:** V Forge
> **Package status:** Draft exercise — not a governed artifact

---

### EP1. Execution Purpose and Task Shape

V Forge is being asked to build the v1 content and page layer of a branded,
entity-driven gift discovery affiliate site.

The work is: produce a structured, curated, review-gate-eligible set of product
records, classification records, and public-facing pages for the v1 scope defined
below. The site must function as a structured discovery system, not as a generated
affiliate content dump.

This is a content execution scope, not a research scope and not a strategy scope.
V Forge must execute within the scope defined here. If execution discovers a
planning problem, the governed path is return-to-planning, not unilateral scope
redefinition.

---

### EP2. Approved Execution Scope

**In scope for this execution pass:**

- Product records: a manually curated set of approximately 50–75 products
  meeting the curation rules defined in EP5
- Classification records: a small controlled set per dimension:
  - Category: approximately 6–10 top-level terms
  - Recipient: approximately 7–10 terms
  - Occasion: approximately 5–6 terms
  - Interest / Theme: approximately 8–10 optional terms (secondary use only)
- Required product relationships: Product → Category (required), Product →
  Recipient (required); Product → Occasion and Product → Interest (optional)
- Public indexable pages: the allowed types defined in EP3, each requiring
  individual editorial justification before publication
- Human-authored editorial notes: one per product record, required for every
  product before that record is eligible for publication

**Out of scope for this execution pass:**

- Offsite branded reinforcement network (X, Pinterest, YouTube, Medium, etc.)
- Autonomous publishing without review gate
- Three-way taxonomy intersection pages
- Interest-only pages, Price-only pages, filter-state URLs
- Subcategory expansion beyond the approved top-level taxonomy
- VEDA observation setup or integration
- VEDA Strategy analysis
- Full merchant diversification (single primary merchant is acceptable for v1)
- Advanced product lifecycle automation

---

### EP3. Page-Type Constraint

The following page types are the only types approved for v1 public indexable
publication:

- Product Detail Page
- Recipient Guide Page
- Occasion Guide Page
- Category Browse Page
- Recipient × Occasion pages — only where the pair has adequate product depth,
  real editorial framing, and explicit per-page review approval
- Manually curated collection pages — only where explicitly approved

No other page type may be created as a public indexable URL in this execution
pass. Specifically excluded: Interest-only pages, Price-only pages, Recipient ×
Interest pages, Category × Recipient pages, any three-way intersection pages,
filter-state pages.

Each public page must be individually justified. Existence of a taxonomy
combination does not constitute justification for a page.

---

### EP4. Required Structural Constraints

**Product is the only first-class durable object.**
Categories, Recipients, Occasions, and Interests are controlled vocabularies
or governed classification objects. They are not equal peer entities to Product.
V Forge must not model or execute them as peer objects that independently demand
equivalent record infrastructure or page-generation workflows.

**Anti-page-explosion rule.**
Combinatorial page generation is forbidden. A public page requires positive
editorial justification — not just the technical possibility of a taxonomy
intersection. V Forge must not generate pages from a taxonomy matrix. Each
published page is a deliberate individual decision.

**Affiliate links are subordinate structured records.**
Affiliate links attach to product records as structured subordinate records.
They are not free-floating content fragments and must not be modeled or executed
as such.

**Publication is review-gated.**
No public mutation — no page publication, no product record publication — occurs
without governed review. Publication is a governance-sensitive action. V Forge
must route all publication decisions through the review gate, not execute them
inline.

---

### EP5. Product and Editorial Curation Rules

**Every product record requires:**
- canonical identity and slug
- title and short factual description
- current price or price signal
- availability / lifecycle state indicator
- brand / maker as a product property
- at least one affiliate link as a subordinate structured record with merchant
  attribution
- image reference
- date added
- a human-authored editorial note — this is required; generated prose is not
  a substitute and does not satisfy this requirement

**Products must not be included if:**
- they are stale, discontinued, persistently out of stock, or low-trust
- they do not have meaningful giftable use for at least one real recipient case
- they are padding for page depth without curation value

**Ranking and featured picks are page-level editorial decisions, not global
product truth.** A product may be featured differently across pages. Execution
must preserve this flexibility — it must not flatten page-level curation into
a global ranking field on the product record.

---

### EP6. Deliverable Shape

At the end of this execution pass, V Forge should have produced:

- a set of product records meeting EP5 requirements, within the 50–75 product
  scope
- a controlled classification record set per EP2
- a set of public-facing pages of the approved types per EP3, each individually
  reviewed and approved before publication
- execution findings surfaced through the governed return path where relevant

Execution is not complete until the review gate has been passed for each
published page and product record. Draft production is not publication.

---

### EP7. Forbidden Execution Patterns

V Forge must not, during this execution pass:

- generate pages from taxonomy combinations without individual editorial
  justification
- publish any page or record without a completed review gate
- substitute generated prose for a human-authored editorial note on any product
  record
- expand scope beyond the product volume, classification scope, or page types
  defined in EP2 and EP3 without a scope update through the governed path
- treat the handoff as authorization for open-ended content research or strategy
  work
- model classification objects (categories, recipients, occasions, interests) as
  peer entities to Product with equivalent record infrastructure
- create affiliate links as free-floating content fragments rather than
  subordinate structured records attached to product records
- treat a draft production state as a published state for any record or page

---

### EP8. Return-to-Planning Triggers

V Forge should return bounded findings to planning rather than proceeding if:

- the approved product scope cannot be satisfied with products meeting the
  curation rules (e.g., insufficient qualifying products exist for a required
  recipient or occasion page)
- the page-type allowlist cannot produce a coherent site structure within v1
  scope (e.g., too few products exist to support a planned Recipient Guide Page
  meaningfully)
- an execution-blocking finding requires a planning decision that is not covered
  by the execution scope defined here
- a curation constraint conflict arises that cannot be resolved within the
  defined rules

V Forge must not silently absorb these conditions or resolve them through
unilateral scope interpretation.

---

### EP9. Conditions That Would Make This Package Invalid

Per the handoff interface requirements, this package would be invalid if:

- the execution scope is too open-ended for V Forge to determine what is in
  scope (not the case here — scope is bounded)
- the planning basis is materially stale or superseded at activation time
- a prior handoff for the same scope is still active and unresolved

V Forge must not begin execution on a package that fails validity conditions.

---

## 4. Why Each Major Section Belongs in the Packet

**EP1 (Execution purpose):** Required by the handoff interface as "expected
outcomes / intended execution objective." Execution needs to know what it is
building.

**EP2 (Approved scope):** Required by the handoff interface as "approved
execution scope" — must be specific enough for V Forge to determine what is
in and out of scope. This section is a core required field.

**EP3 (Page-type constraint):** Belongs in the execution packet's "execution
constraints and boundaries" field. This is a direct execution constraint, not
planning framing. Without it, execution has no basis for refusing a page request.

**EP4 (Structural constraints):** These are the constraints identified in the
digest exercise as borderline-but-better-in-the-packet items. Anti-page-explosion,
product-as-first-class-object, affiliate-link model, and publication-gating all
belong here as structural execution constraints, not in a supplementary carry-
forward artifact.

**EP5 (Curation rules):** Execution needs to know what makes a valid product
record. The editorial-note requirement belongs here as a record completeness rule,
not in the digest. This is the clearest case of a digest item that should move to
the packet.

**EP6 (Deliverable shape):** Required by the handoff interface as "expected
outcomes." Execution needs to know what "done" looks like.

**EP7 (Forbidden patterns):** Belongs in "execution constraints and boundaries."
Stating what execution must not do is as important as stating what it must do.

**EP8 (Return-to-planning triggers):** Required by the handoff interface as
"conditions that should trigger return-to-planning." This is a mandatory semantic
field.

**EP9 (Invalidity conditions):** Reflects the handoff interface's validity
requirements. Included to make the packet self-aware of its own validity posture.

---

## 5. What Was Deliberately Kept Out

**Project thesis and strategic rationale**
Why the entity-driven model was chosen, what the project hopes to prove, why
the first project is the proving ground. This is planning context. Execution
does not need it and must not be influenced by it.

**Kill / pivot conditions**
Planning governance rules, not execution constraints. Excluded.

**Success conditions**
What early success looks like. This is evaluation framing. Execution must
not optimize against success criteria — it must execute against the structural
rules. Excluded.

**VEDA observation and VEDA Strategy scope**
Explicitly deferred from v1 scope. Not an execution constraint for this pass.

**Branded network and offsite distribution ambition**
Explicitly deferred. Excluded.

**Monetization philosophy**
Anti-patterns and channel strategy. The structural constraint (affiliate links
as subordinate records) is in EP4. The broader monetization philosophy is
planning context. Excluded.

**Detailed decay posture and lifecycle cadence**
The lifecycle state structure is implied by the curation rules (a product must
not be included if stale or out of stock). The full decay governance model is
an operational planning concern beyond this execution pass. Excluded.

**Open questions from planning**
Single vs. multi-merchant, VEDA timing, editorial capacity. These are
unresolved planning questions. Excluded. If any must be resolved before
execution, the handoff is not ready.

**Readiness and planning rationale**
Why this handoff is happening now, what the BYDA audit found, what the
planning progression looked like. This is planning continuity context.
Execution inherits the result (the approved scope), not the deliberation.
Excluded.

---

## 6. Interaction with the Draft Digest

The draft digest exercise identified five items: D1 (page-type allowlist),
D2 (anti-page-explosion rule), D3 (editorial-note requirement), D4 (product
relationship requirements), D5 (product-first-class-object rule).

**D2 — Anti-page-explosion rule → now in EP4.**
This is now explicitly in the execution packet as a required structural
constraint. It should be removed from any real digest produced against this
execution packet.

**D3 — Editorial-note requirement → now in EP5.**
Now in the packet as a product record completeness rule. Should be removed
from any real digest.

**D5 — Product-first-class-object rule → now in EP4.**
Now explicitly in the packet. Should be removed from any real digest.

**D1 — Page-type allowlist → remains in digest.**
EP3 states the page-type constraint in the packet, but in a form that defines
the rule without enumerating every excluded type in detail. The specific
enumeration (named excluded surfaces) is useful auxiliary detail that could
remain in the digest without duplicating the packet. However, EP3 is already
detailed enough that the digest entry is nearly redundant. If EP3 is considered
complete, D1 can also be dropped from the digest.

**D4 — Product relationship requirements → partially absorbed.**
EP2 states the required relationships (Product → Category required, Product →
Recipient required; others optional). The digest entry for D4 is now redundant
against the packet. D4 should be removed from any real digest.

**Result:** With this execution packet in place, the draft digest shrinks from
five items to either zero (if EP3 is treated as sufficiently covering the
page-type detail) or one very short item (if the explicit named-exclusions
list in D1 is retained as an auxiliary detail). The digest becomes optional
in the strong sense: an adequate execution packet makes it unnecessary for
this project.

---

## 7. Judgment on Packet Viability

The draft packet is viable and looks primary. It covers all required handoff
interface semantic fields:

- execution purpose / intended objective ✓ (EP1)
- approved execution scope ✓ (EP2)
- execution constraints and boundaries ✓ (EP3, EP4, EP5, EP7)
- target system ✓ (implicit throughout; stated in header)
- expected outcomes / deliverable ✓ (EP6)
- return-to-planning triggers ✓ (EP8)
- readiness basis — not included here, belongs in the actual handoff record
  at activation time, not in the scope definition

**What makes this packet strong:** It is specific enough that V Forge could
act within it without needing the planning packet. Scope, constraints, record
requirements, forbidden patterns, and return triggers are all stated. The
editorial-note rule is in the packet as a record definition requirement, not
an ambient cultural expectation.

**Where it remains incomplete:**
- No explicit handoff identity or activation timestamp (not appropriate for
  a draft exercise; would be assigned at real handoff creation)
- No readiness basis statement (belongs in the activation-time record)
- No explicit cost or accounting posture (required by the handoff interface
  but not material to the scope definition exercise)
- Affiliate link schema implications are noted in EP4 and EP5 but not
  specified in detail — the planning packet flagged this as a V Forge design
  question that should not be smuggled into intake. The packet acknowledges
  the posture without solving the schema.

**Does it look like planning bleed?**
No. The packet does not contain thesis material, strategic rationale, kill
conditions, success framing, or open questions. The closest risk is EP5
(curation rules) — detailed curation guidance can read like editorial philosophy.
But EP5 is grounded in concrete record-completeness requirements (what fields
are required, what disqualifies a product from inclusion) rather than in the
"why curation matters" framing that belongs in the planning packet.

---

## 8. What May Belong in Canonical Authority Later

**Anti-page-explosion rule (EP4)**
This is not first-project-specific. It is a structural rule for any content
site operated under V Forge: each indexed page requires individual editorial
justification; combinatorial generation is forbidden. This belongs in V Forge
content execution doctrine when that doctrine is formalized.

**Publication-is-review-gated rule (EP4)**
Similarly generalizable. Any V Forge content execution scope that involves
public mutation should be subject to review gating. This is already implied
by the harness and approval doctrine, but it should be explicit in V Forge
content execution doctrine.

**Editorial-note-as-record-requirement (EP5)**
Whether every structured content record requires a human-authored editorial
component is a generalizable content execution rule for this class of site.
Belongs in V Forge content execution doctrine or in a governed content quality
doctrine.

**Project-specific items that do not generalize:**
EP2 (scope boundaries), EP3 (v1 page-type allowlist), EP5 product relationship
requirements — these are first-project decisions and should not be promoted
to Canonical Authority. They belong in the execution packet for this specific
handoff.

---

## 9. Open Cautions

**This packet was drafted without a real handoff being activated.**
The scope numbers (50–75 products, approximate taxonomy sizes) come from the
planning materials. In a real handoff, these would be reviewed for accuracy
at activation time. The planning basis may have changed since those numbers
were written.

**The affiliate link schema is flagged but not solved.**
EP4 and EP5 state the posture (subordinate structured records) without
specifying the schema. The planning packet correctly deferred this to V Forge
design. A real execution packet may need to reference a V Forge-owned schema
doc for this detail, or the activation may need to confirm the schema is
resolved before execution begins.

**Readiness basis is absent.**
A real execution packet needs to state why this handoff is valid now — what
BYDA audit or readiness determination supports it. That is not a scope
definition question; it is an activation-time question. Not included here
because the first project has not formally completed intake. In a real handoff,
it must be present.

**The open questions from planning are still open.**
Single vs. multi-merchant, VEDA observation timing, editorial capacity
confirmation are unresolved. If any of them must be resolved before execution
begins, the handoff is not yet ready. This packet assumes they have been
resolved or scoped as out-of-v1 at intake time.

---

## 10. Recommended Next Move

1. Use this draft packet alongside the draft digest to confirm the prediction
   in Section 6: with this packet in place, the digest becomes empty or
   near-empty. If that prediction holds, the digest concept is validated
   as a temporary carry-forward mechanism, not a permanent pattern.

2. Before a real handoff is activated, the open questions from the planning
   packet (Section 9 above) must be resolved. The packet as drafted assumes
   resolution.

3. Flag the anti-page-explosion rule, publication-gating rule, and editorial-
   note requirement as V Forge content execution doctrine candidates. These
   structural rules should not require packet-level restatement for every
   content site execution pass.

4. The affiliate link schema gap is the one material open item for execution
   packet completeness. It should be resolved in V Forge before the handoff
   is activated.

5. Do not use this draft packet as a real governed handoff artifact. The
   activation approval is not in place, the readiness basis is not stated,
   and the handoff identity is not assigned.

---

## 11. Related Files

- `first-project-draft-execution-scoped-planning-digest.md`
- `execution-scoped-planning-digest-spec-note.md`
- `../first-project-entity-driven-gift-discovery-site.md`
- `../first-project-entity-driven-gift-discovery-planning-packet.md`
- `doctrine-aware-context-model-design-pass.md`
- `doctrine-aware-context-enforcement-and-inspectability-note.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../../project-v/project-v.md`
- `../../v-forge/v-forge.md`
