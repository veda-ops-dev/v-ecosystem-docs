# First Project — V Forge Record Families Spec Note

## 1. Purpose

This note translates the settled transition-support decisions about product
records and affiliate-link records into a schema-facing working spec. It exists
so that later V Forge schema work does not have to re-derive the conceptual
model from scratch by reading a chain of posture and placement notes.

It makes the record families, their join posture, their lifecycle separation,
and their minimum integrity rules concrete enough to serve as a schema starting
point. It does not write final tables or migrations.

---

## 2. Status

Transition-support spec note only.

This note is:
- schema-facing at working-spec level
- not final V Forge schema doctrine
- not a migration plan
- not implementation code
- not a substitute for `v-forge/schema-specification.md` when that doc is
  authored
- subject to revision after the first project exercises the model

---

## 3. Problem Being Solved

The prior notes established:

- Product is the primary durable object; affiliate links are subordinate
- Affiliate-link records are a distinct record family, separate from the
  content graph, linked to products by product identifier
- Link lifecycle is independent of product lifecycle
- Merchant attachment belongs on the link record, not the product

What these notes do not yet provide is a schema-facing statement of:

- what the product record family minimally owns
- what the affiliate-link record family minimally owns
- how the join relationship works in schema/spec terms
- what "subordinate but separate" means as a concrete record relationship
- what minimum integrity rules must hold

Without this, "product record family" and "affiliate-link record family" remain
conceptual labels. A V Forge schema author arriving at this work still has to
invent the structure. This note closes that gap.

---

## 4. Proposed Record Families

Two primary record families are needed for the first-project V Forge slice
covering products and monetization:

**Family 1: Product record family**
Covers product identity, editorial state, classification relationships, and
lifecycle. This is the primary durable record family.

**Family 2: Affiliate-link record family**
Covers monetization attachment to products — link targets, merchant identity,
attribution, and link lifecycle state. This is the subordinate record family.

**Supporting implication: Link review / activity records**
The lifecycle posture implies that link state transitions (dead, replaced,
stale, merchant-changed) should be inspectable. Whether this requires a
separate link-activity or link-history record family, or whether the link
record's own state plus timestamps is sufficient, is an open question (see
Section 12). For v1, the link record's own state fields may be sufficient.
No third family is being introduced here as required.

**What is not a separate record family here:**

Classification terms (Category, Recipient, Occasion, Interest) are controlled
vocabulary objects. They are not full peer record families to Product — they
are governed classification objects. Their schema representation is simpler
than Product (identifier, label, slug, status) and is noted here only to
clarify they are not peer entities to Product despite being stored records.

---

## 5. Product Record Posture

The product record is the primary durable object for the first project. It
owns editorial and discovery truth about a product independently of its
monetization state.

**What the product record family owns:**

- Canonical product identity: stable identifier, slug, canonical URL target
- Title and editorial description
- Human-authored editorial note (required; see integrity rules)
- Brand / maker as a product property
- Images (reference or embedded, depending on storage model)
- Classification relationships: Category (required), Recipient (required),
  Occasion (optional), Interest (optional)
- Lifecycle / status for the product itself (see Section 8)
- Created and last-reviewed timestamps for the editorial record

**What the product record family does not own:**

- Merchant identity (belongs on affiliate-link records)
- Affiliate link URLs or tracking parameters
- Price as a stored first-class field with merchant provenance (price signal
  may be stored as a product property for display purposes, but it is not
  a monetization join and not a merchant attribute)
- Link lifecycle state (belongs on affiliate-link records)
- Revenue or attribution analytics (belongs in VEDA if anywhere)

**Primary vs. constructed fields:**

The product record stores what is true about the product editorially and
structurally. Price bands, "similar products," and other derived or computed
properties are not first-class stored fields on the product record — they
are derived at query or render time from product properties and classification
relationships.

---

## 6. Affiliate-Link Record Posture

The affiliate-link record is a subordinate execution record attached to a
product by product identifier. It owns everything about the monetization
attachment that should not be on the product record.

**What the affiliate-link record family owns:**

- Stable identifier for the link record itself
- Parent product identifier (foreign key / join reference to the product
  record; required; must not be null)
- Link target URL (the URL sent to the merchant, including tracking parameters;
  required for active links)
- Merchant / source identity (which affiliate platform or merchant this link
  belongs to; required; structured identifier, not a prose note)
- Attribution identifier or tag (the tracking tag or sub-ID that enables
  attribution; required for monetizable links)
- Link lifecycle state (see Section 8; required)
- Primary / secondary role flag (whether this is the primary link for this
  product in rendered output; defaults to primary for v1 single-link products)
- Created timestamp (when this link record was created; required)
- Last-verified timestamp (when this link was last confirmed live and accurate;
  required for operational freshness tracking)
- Optional notes field (brief human-authored note about this specific link;
  not a prose dump)

**What the affiliate-link record family does not own:**

- Product editorial state, identity, or description
- Content graph node or edge identity
- Product lifecycle state
- Merchant platform analytics or attribution metrics (these are VEDA
  observability data, not V Forge execution truth)

---

## 7. Join Posture

### The join is by product identifier

Each affiliate-link record carries a reference to its parent product by the
product's stable identifier. This is an explicit foreign-key-style relationship:
the affiliate-link record depends on the product, not the reverse.

### Products do not carry link identifiers

Product records do not store references to their affiliate-link records. The
join is one-directional: to retrieve a product's affiliate links, query the
affiliate-link family filtered by product identifier. To retrieve a product
given one of its links, join through the link's parent product identifier.

This is intentional. It means:
- adding, removing, or replacing affiliate links does not mutate the product
  record
- querying all links for a product is a join query, not a field access on the
  product record
- multiple affiliate links per product (multi-merchant) is structurally
  supported without schema change

### "Subordinate but separate" in schema/spec terms

"Subordinate" means: an affiliate-link record without a valid parent product
identifier is an invalid record. Links depend on products; products do not
depend on links.

"Separate" means: the affiliate-link record is not an embedded sub-document,
sub-row, or array field on the product record. It is a distinct record in its
own family with its own lifecycle, its own timestamps, and its own integrity
rules.

### Link records survive merchant churn without mutating product identity

When a merchant changes a URL, discontinues a product, or changes affiliate
program terms, the affiliate-link record is updated or replaced (its lifecycle
state transitions to replaced or dead). The parent product record does not
change. A new affiliate-link record may be created for the same product with
a different merchant or URL — it carries the same parent product identifier.

Product identity is stable across merchant churn. This is the structural
guarantee the join posture must preserve.

---

## 8. Lifecycle / Status Posture

### Product lifecycle states

Product lifecycle state governs whether a product is available for discovery,
editorial use, and publication. It is independent of whether the product
currently has live affiliate links.

Proposed minimum product lifecycle states (derived from planning materials):

- **active** — editorially valid, eligible for publication, in active use
- **flagged-for-review** — something about the product warrants human review
  before the next publication cycle (may be triggered by link decay, editorial
  staleness, or operator flag)
- **unavailable** — product is temporarily out of stock or otherwise not
  purchasable; may remain discoverable but should not be presented as
  immediately purchasable
- **discontinued** — product is no longer manufactured or available; should
  be transitioned out of active publication
- **archived** — product has been removed from active use; retained for
  record integrity

These states control publication eligibility. A product in `discontinued` or
`archived` state is not eligible for publication regardless of link state.

### Affiliate-link lifecycle states

Affiliate-link lifecycle state governs whether a specific monetization
attachment is operational. These are already specified in the posture note:

- **active** — live, recently verified, expected to produce valid referrals
- **needs-review** — not recently verified or flagged for review
- **dead** — URL does not resolve or does not represent the intended product
- **replaced** — superseded by a newer link record; retained for audit
- **stale** — resolves but linked page no longer accurately represents the
  product
- **merchant-changed** — merchant relationship has changed (program discontinued,
  merchant left network, etc.)

### Separation rule

These two state dimensions must not be conflated:

- Product lifecycle state answers: is this product editorially valid and
  eligible for publication?
- Link lifecycle state answers: is this specific monetization attachment
  currently operational?

A `dead` link does not automatically set the product to `unavailable`. A
product with all `dead` links should be `flagged-for-review` — the flag
triggers human review — but the product's own editorial validity is preserved
pending review. The transition between link state and product state is a
governed operational decision, not an automatic cascade.

---

## 9. Minimum Integrity / Completeness Rules

These are the minimum record-level integrity rules this first-project slice
requires. They are derived from the planning materials and the posture / placement
notes.

**R1. Affiliate-link record requires a valid parent product.**
An affiliate-link record without a parent product identifier referencing a
valid product record is invalid. Orphaned link records are not permitted.

**R2. Product identity does not require a live affiliate link.**
A product record is valid and may exist without any affiliate-link records or
with only non-active link records. Product identity and editorial validity are
independent of monetization state.

**R3. Dead or replaced affiliate links do not automatically invalidate the product.**
A product whose affiliate links are all dead or replaced should be
`flagged-for-review` at the product level, not automatically set to
`discontinued` or `archived`. The transition to a lower lifecycle state
requires human review.

**R4. A product eligible for publication and for active monetization requires
at least one affiliate-link record in `active` state.**
A product in `active` product lifecycle state that is intended to be
monetizable must have at least one affiliated link in `active` state for it
to function as a monetizable surface. A product with no active links may still
be published for discovery purposes if editorially warranted, but it should be
flagged to indicate the absent monetization state.

**R5. A product record must carry a human-authored editorial note before it
is eligible for publication.**
An absent, placeholder, or generated editorial note does not satisfy the
record completeness requirement for publication. This rule is stated in the
execution packet; it belongs here as a record integrity rule.

**R6. Merchant identity on the affiliate-link record is a structured identifier,
not a prose attribute.**
The merchant field on an affiliate-link record must be structured and queryable.
It is not a freeform text note. This is required for multi-merchant queries
and for merchant-change lifecycle management.

**R7. Classification relationships on the product record follow required / optional
rules.**
Product → Category and Product → Recipient are required for every product record.
Product → Occasion and Product → Interest are optional. A product record missing
a required classification relationship is incomplete.

---

## 10. First-Project V1 Implications

### What v1 minimally requires

- Product record family with the fields described in Section 5, including
  required classification relationships and human-authored editorial note
- Affiliate-link record family with the fields described in Section 6,
  at minimum: parent product identifier, link target URL, merchant identity,
  attribution identifier, lifecycle state, created timestamp, last-verified
  timestamp
- Product lifecycle states: at minimum active, flagged-for-review, discontinued,
  archived (unavailable is useful for v1 but could be deferred to first review
  cycle)
- Affiliate-link lifecycle states: at minimum active, needs-review, dead,
  replaced (stale and merchant-changed are useful but could be introduced at
  first review cycle)
- Integrity rules R1–R7 in effect from the start

### What can remain simplified for v1

- One affiliate-link record per product (single-merchant simplification affects
  population only, not structure)
- Primary / secondary link role flag defaults to primary for all v1 links;
  multi-link management logic is not operationally required
- Link verification is manual; no automated dead-link detection required
- Link-activity or link-history records are not required for v1; link record
  state plus timestamps is sufficient

### Single-merchant simplification

Structurally, the single-merchant v1 simplification means every product will
have zero or one affiliate-link records. The record model supports multiple
links per product from the start. Adding a second merchant requires creating
new link records — no schema change.

---

## 11. Boundary / Ownership Posture

**V Forge owns both record families as execution truth in `v_forge.*`.**

Product records are V Forge execution truth for what was built and what is
currently in the project's content execution footprint. Affiliate-link records
are V Forge execution truth for the current monetization attachment state of
those products.

**Project V owns the decisions that led to this execution state.**
Which products to include, what editorial standards to require, which affiliate
merchants to use, when to change monetization strategy — these are planning
decisions. They arrive at V Forge through the governed handoff. V Forge executes
and records them. V Forge does not make these decisions.

**VEDA owns any external performance or signal data.**
Click data, conversion rates, affiliate platform analytics, search performance —
if any of this is relevant to ecosystem decisions, it belongs in VEDA as
observatory records. V Forge affiliate-link records carry operational state
(is this link live?), not performance analytics.

**Merchant platform data is not canonical truth.**
A merchant's product page, pricing, and URL structure are external operational
data. They inform the affiliate-link record fields but do not define the
product's canonical identity or editorial state. The product record is the
canonical identity. The link record is the monetization attachment. Neither is
derived from merchant platform truth.

---

## 12. Open Questions

**Whether product records are content graph nodes**
The placement note identified this as an open seam. If Product Detail Pages
are content graph nodes but product records are a separate record family that
pages reference, the relationship between the product record family and the
content graph is through the page layer, not directly. If product records
themselves are content graph nodes, they participate in graph operations. This
has implications for how the product record family is registered and how graph
integrity checks apply to it. Not settled here; must be resolved at schema
specification time.

**Link-activity or link-history records**
For audit and operational visibility, knowing how a link's lifecycle state
changed over time may be useful. Whether this requires a separate link-activity
record family or whether the link record's own state plus timestamps is
sufficient for v1 is not settled. For v1, the link record approach is adequate.
Revisit after the first review cycle.

**Exact field types and constraint specifications**
Column types, constraint definitions, index strategy, and migration sequencing
are not addressed here. These belong in `v-forge/schema-specification.md`.

**Publication and content graph registration timing for product records**
When is a product record considered "published"? When its Product Detail Page
goes live? When the record is created? The publication state for the product
record as an entity (versus the publication state of its associated page) is
not fully specified here and should be addressed at schema time.

---

## 13. Recommended Next Move

1. Use this note as the starting spec for the `v-forge/schema-specification.md`
   section covering product records and affiliate-link records. The field
   families (Sections 5–6), join posture (Section 7), lifecycle states
   (Section 8), and integrity rules (Section 9) are the minimum spec a schema
   author needs to begin.

2. Resolve the "are product records content graph nodes?" question at schema
   specification time before finalizing the product record schema. The answer
   changes whether products participate in graph registration operations.

3. Update the first-project v1 execution packet draft to reference this note
   as the governing spec for product record completeness and affiliate-link
   record requirements. The integrity rules (Section 9) should be added as
   execution constraints in the packet.

4. Do not treat this note as final doctrine. It is a working spec. First-project
   exercise will validate or challenge it.

---

## 14. Related Files

- `first-project-affiliate-link-record-posture-note.md`
- `affiliate-link-placement-in-v-forge-note.md`
- `first-project-v1-execution-packet-draft.md`
- `../first-project-entity-driven-gift-discovery-site.md`
- `../first-project-entity-driven-gift-discovery-planning-packet.md`
- `../../v-forge/v-forge.md`
- `../../v-forge/content-execution-module.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../../project-v/project-v.md`
