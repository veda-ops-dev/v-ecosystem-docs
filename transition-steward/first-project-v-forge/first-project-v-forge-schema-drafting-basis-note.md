# First Project — V Forge Schema Drafting Basis Note

## 1. Purpose

This note consolidates the settled first-project V Forge structural decisions
into a schema-facing drafting basis. It exists so that a later schema author
can begin drafting `v-forge/schema-specification.md` sections for this slice
without having to re-derive the conceptual model from a chain of transition-
support notes.

It is the terminal consolidation of the first-project structural cluster. The
notes behind it are the derivation record; this note is the usable starting
point.

---

## 2. Status

Transition-support schema-facing note only.

This note is:
- a concrete drafting basis, not a final schema
- not SQL, not migration design, not implementation code
- not V Forge schema doctrine until promoted
- subject to revision after the first project exercises the model
- the appropriate starting point for `v-forge/schema-specification.md` sections
  covering products, affiliate links, and page/content representations for this
  project type

---

## 3. Settled Structural Decisions Carried Forward

These are treated as settled inputs. They must not be reopened in schema
drafting without a documented reason that the repo contradicts them.

1. **Product is the primary durable object.** Product records are stable
   editorial/execution truth. Their identity does not change due to merchant
   churn, page publication, or link decay.

2. **Affiliate-link records are subordinate, separate execution records.**
   They attach to products by product identifier. They are not product sub-
   fields and are not embedded in product records.

3. **Merchant attachment belongs on affiliate-link records, not product records.**
   Product identity does not depend on or include merchant identity.

4. **Affiliate-link records are content-graph-adjacent but not graph nodes.**
   They join to product records; product records are adjacent to the graph via
   page references; affiliate-link records are outside both.

5. **Product records are not content graph nodes.** They are execution records
   in `v_forge.*` that exist independently of whether they have page
   representations.

6. **Page/content representations are the content graph participants.** Page
   nodes carry product identifier references back to product records. The
   direction is one-way: page → product, not product → page.

7. **Product identity is stable across merchant churn.** Adding, replacing, or
   removing affiliate links does not mutate product records.

8. **Link lifecycle and product lifecycle are independent dimensions.** A dead
   link does not automatically invalidate the product; a discontinued product
   does not automatically invalidate its links (though both signal review).

9. **Classification terms (Category, Recipient, Occasion, Interest) are
   controlled vocabulary objects, not peer entities to Product.** They are
   simpler record types than Product and are not equal peer schema citizens.

10. **Single-merchant v1 simplification is a population decision, not a
    structural constraint.** The schema must support multiple affiliate-link
    records per product from the start.

---

## 4. Proposed Schema-Facing Families

The following record families are implied for this first-project V Forge slice:

**F1 — Product record family**
Primary durable execution records for editorial and structural product truth.

**F2 — Affiliate-link record family**
Subordinate monetization attachment records, separate from the product family,
joining to products by product identifier.

**F3 — Page/content representation family**
Content graph nodes representing built published surfaces. This includes Product
Detail Pages, Recipient Guide Pages, Occasion Guide Pages, Category Browse Pages,
and other approved v1 page types. These are graph participants; F1 and F2 are not.

**F4 — Classification term records**
Controlled vocabulary objects for Category, Recipient, Occasion, and Interest.
These are simpler records than products — identifier, label, slug, status — and
are governed classification objects, not peer entities.

**Potential F5 — Page-to-product association records**
Whether multi-product pages (guide pages, browse pages, collections) use a
dedicated association record family or a structured field on the page record is
a still-open schema design choice. This is named as a potential family, not a
committed one. See Section 8.

No other new families are introduced. Lifecycle activity / history records for
affiliate links are deferred beyond v1.

---

## 5. Product Family Draft Shape

**What the product family must own:**

- Stable product identifier (primary key; must not change)
- Slug / canonical URL segment
- Title
- Short factual description
- Human-authored editorial note (required before publication; cannot be absent
  or generated)
- Brand / maker as a product property (not a separate entity for v1)
- Price signal (stored as a product property for display; not a merchant
  attribute and not a first-class join target)
- Availability / lifecycle state (see lifecycle states below)
- Created timestamp
- Last-reviewed timestamp

**Classification relationship fields on product:**
- Category (required; foreign reference to F4 classification term)
- Recipient (required; foreign reference to F4 classification term)
- Occasion (optional; foreign reference to F4 classification term)
- Interest (optional; foreign reference to F4 classification term)

**What the product family must not own:**
- Merchant identity (belongs in F2)
- Affiliate link URLs or tracking parameters (belongs in F2)
- Link lifecycle state (belongs in F2)
- Revenue or attribution data (belongs in VEDA if anywhere)
- Content graph node identifiers (the join is page → product, not product → page)
- Price band as a first-class field (derived from price signal at query/render time)

**Product lifecycle states (minimum):**
- `active` — editorially valid, eligible for publication
- `flagged-for-review` — requires human review before next publication cycle
- `unavailable` — temporarily not purchasable; may remain discoverable
- `discontinued` — no longer manufactured or available; should transition out
  of active publication
- `archived` — removed from active use; retained for record integrity

---

## 6. Affiliate-Link Family Draft Shape

**What the affiliate-link family must own:**

- Stable affiliate-link record identifier (primary key)
- Parent product identifier (required; foreign reference to F1; must not be null)
- Link target URL (required for active links; the full URL including tracking
  parameters sent to the merchant)
- Merchant / source identity (required; structured identifier, not prose;
  must be queryable)
- Attribution identifier / tag (required for monetizable links; the tracking
  tag or sub-ID for attribution)
- Link lifecycle state (required; see below)
- Primary / secondary role flag (defaults to primary; supports multi-link
  products when needed)
- Created timestamp (required)
- Last-verified timestamp (required; supports freshness tracking and cadence
  review)
- Optional notes field (bounded; human-authored; not a prose dump)

**What the affiliate-link family must not own:**
- Product editorial content (title, description, editorial note)
- Product lifecycle state
- Merchant platform analytics, conversion data, or revenue metrics
- Content graph node identity

**Affiliate-link lifecycle states (minimum):**
- `active` — live, recently verified, expected to produce valid referrals
- `needs-review` — not recently verified or flagged for review
- `dead` — URL does not resolve or does not represent the intended product
- `replaced` — superseded by a newer link record; retained for audit
- `stale` — resolves but linked page no longer accurately represents the product
- `merchant-changed` — merchant relationship has changed structurally

---

## 7. Page/Content Representation Posture

### Page nodes are the content graph participants

Page records / nodes are registered in the content graph at publication time.
They represent what was built and published on the owned surface. Product records
exist before and independently of page publication.

### Product Detail Pages

A Product Detail Page node carries:
- a stable page identifier
- a product identifier reference (required; foreign reference to F1)
- page lifecycle/publication state
- content graph registration metadata (when registered, publication event
  reference)
- standard page content fields (not specified in detail here; belong in the
  page schema section)

The product identifier on the page node is the join key that connects built
content back to the editorial source record. Querying a page's product gives
access to the product's editorial content, classification, and affiliate links.

### Guide, Browse, and Collection Pages

Recipient Guide Pages, Occasion Guide Pages, Category Browse Pages, and
manual collection pages reference multiple products. The mechanism for this
reference is an open schema design choice (see Section 8). In all cases:

- the page node exists in the content graph
- product records referenced by the page are in F1 (outside the graph)
- the page node carries or joins to product identifier references
- the page is the graph citizen; the products are the execution records being
  referenced

### One-directional reference posture

The reference direction is always: page → product identifier → product record.
Product records do not carry page identifiers or graph node references.

Adding a new page that references a product does not mutate the product record.
Retiring a product does not automatically remove page nodes from the graph — it
triggers a review workflow for affected pages, which is a separate governed
action.

---

## 8. Minimal Association / Reference Options Still Open

### Multi-product page references: foreign key list vs. association table

For pages that reference multiple products (Recipient Guide, Occasion Guide,
Category Browse, collection pages), two options remain open:

**Option M1 — Structured list field on the page record**
The page record carries a structured list of product identifiers with optional
ordering/position metadata. Simple for v1 query volumes; harder to query across
("which pages reference product X?" requires scanning list fields).

**Option M2 — Dedicated association record family (page_product_reference)**
A join table / association family with records carrying: page identifier,
product identifier, position/rank, context label (e.g., "featured", "included").
Supports clean bidirectional queries ("which pages feature product X?",
"which products appear on guide Y?") and is the better long-term choice for
a site where this traversal is operationally useful.

**Recommendation without full commitment:** Option M2 is likely the stronger
choice for a content site where guide-page-to-product traversal is a real
operational query (maintenance, editorial review, decay detection). However,
the schema author should confirm whether v1 query volumes actually require this
or whether a list field is sufficient for the initial build.

### Whether guide pages need dedicated association records

Related to the above. If Option M2 is chosen, the association record family
may be shared across all multi-product page types (guide, browse, collection)
with a page type or context field distinguishing them. If Option M1 is chosen,
guide pages use a list field. This choice should be made at schema specification
time, not deferred further.

### Link activity / history records

Deferred beyond v1. The affiliate-link record's own state fields plus
timestamps are sufficient for v1 operational needs. Whether a link-activity
or link-state-history family is warranted for later audit needs is an open
question to revisit after the first review cycle.

---

## 9. Integrity / Completeness Rules Carried Forward

These rules constrain later schema work and should be reflected in schema
constraints, validation logic, or documented completion criteria.

**R1.** Affiliate-link record requires a valid parent product identifier. Orphan
link records are invalid.

**R2.** Product identity does not require a live affiliate link. Product records
are valid without any affiliated links.

**R3.** Dead or replaced affiliate links do not automatically invalidate the
product. They trigger `flagged-for-review` at the product level; the transition
to a lower lifecycle state requires human review.

**R4.** A product in `active` lifecycle state that is intended to be monetizable
should have at least one affiliate-link record in `active` state. A product with
no active links may remain published for discovery purposes but should be flagged
to indicate absent monetization state.

**R5.** A product record must carry a human-authored editorial note before it is
eligible for publication. Absent, placeholder, or generated editorial notes do
not satisfy this requirement.

**R6.** Merchant identity on the affiliate-link record is a structured identifier,
not a prose attribute.

**R7.** Product → Category and Product → Recipient classification relationships
are required for every product record. Product → Occasion and Product → Interest
are optional.

**R8.** Page nodes carry product identifier references; product records do not
carry page node identifiers or graph references. This one-directional posture
must be preserved in schema design.

---

## 10. First-Project V1 Drafting Implications

### What is concrete enough to proceed

A schema author can begin drafting F1 (product), F2 (affiliate-link), and F4
(classification terms) immediately from this note. The field families, lifecycle
states, integrity rules, and ownership posture are all settled at working-spec
level.

F3 (page/content representations) can begin with Product Detail Pages, where
the schema is straightforward (page node + product identifier reference). The
association mechanism for multi-product pages (M1 vs. M2) should be decided
before drafting guide/browse page schema.

### What still needs a schema author decision

- The multi-product page reference mechanism (M1 vs. M2 from Section 8)
- Exact field types, column names, and constraint specifics
- Whether product lifecycle state transitions produce activity trail records
  (likely yes per the activity trail model, but not specified in this slice)
- Whether the price signal field is a first-class column or a structured
  JSON/JSONB field on the product record

### What remains intentionally deferred

- Link activity / history records (beyond v1)
- Full page schema for guide, browse, and collection page types pending
  association mechanism decision
- Editorial revision history or versioning for product records (not specified
  here; defer unless the first project requires it)

---

## 11. Boundary / Ownership Posture

**V Forge owns all four record families as execution truth in `v_forge.*`.**

F1 (products), F2 (affiliate links), F3 (pages), and F4 (classification terms)
are all V Forge execution truth. They represent what was executed and built.

**Project V owns the planning decisions that produced this execution state.**
Which products to include, which pages to build, which merchants to affiliate
with — these are planning decisions that arrive through the governed handoff.
V Forge records the results; it does not make the decisions.

**VEDA owns any external performance or signal data.** Search performance,
affiliate platform analytics, AI-surface presence — these are observatory data.
They do not appear in V Forge execution records.

**Merchant platform data is not canonical truth.** Affiliate link URLs and
tracking parameters are operational fields on F2 records. They are not product
identity. They are not canonical even if sourced from a merchant's affiliate
program.

---

## 12. Open Questions

**Product records and the activity trail model**
Whether product lifecycle transitions (active → flagged-for-review → discontinued)
produce activity trail records per the ecosystem activity trail model is not
specified here. Given that product lifecycle changes are governed operational
events, activity trail records are likely warranted. This should be confirmed
when the V Forge schema section is drafted.

**Price signal field design**
Whether price is stored as a simple numeric/text field or as a structured
object (price value, currency, "as of" timestamp, source) affects both the
product schema and how the site presents price information. Not resolved here;
the planning materials are silent on schema specifics. The schema author should
decide based on the site's price presentation requirements.

**Content graph registration event posture for product-referencing pages**
When a guide or browse page is registered in the content graph, whether the
registration event validates that all referenced product identifiers resolve
to valid, active products is not specified. Likely advisable; not settled here.

**Classification term schema specifics**
F4 classification terms are noted as simpler records (identifier, label, slug,
status). Whether they carry additional metadata (description, parent-term for
potential subcategories, sort order) is not resolved here and should be decided
at schema time.

---

## 13. Recommended Next Move

1. **Begin V Forge schema specification drafting from this note.** The F1 and
   F2 families are ready to draft. F4 classification terms are straightforward.
   F3 page nodes for Product Detail Pages are ready. The multi-product page
   association mechanism (Section 8, M1 vs. M2) should be decided before
   drafting guide/browse page schema.

2. **Decide M1 vs. M2 for multi-product page references.** This is the single
   most consequential open schema design choice for this slice. Make the decision
   based on expected v1 query patterns (especially "which pages reference product
   X?" as a maintenance query) before drafting the guide/browse page schema.

3. **Confirm the activity trail integration for product lifecycle events.**
   Check `ecosystem/activity-trail-model.md` and `ecosystem/activity-trail-
   integration-map.md` before finalizing the product record schema to ensure
   lifecycle transitions are properly reflected in the trail.

4. **Treat this note as the definitive transition-support cluster close for the
   first-project V Forge structural seam.** The chain of notes (posture → placement
   → record families → graph posture → this drafting basis) is complete. Later
   schema work should cite this note as the primary transition-support input, not
   re-read the full chain.

---

## 14. Related Files

- `first-project-v-forge-record-families-spec-note.md`
- `first-project-affiliate-link-record-posture-note.md`
- `affiliate-link-placement-in-v-forge-note.md`
- `product-record-graph-posture-note.md`
- `first-project-v1-execution-packet-draft.md`
- `../first-project-entity-driven-gift-discovery-site.md`
- `../first-project-entity-driven-gift-discovery-planning-packet.md`
- `../../v-forge/v-forge.md`
- `../../v-forge/content-execution-module.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../../ecosystem/activity-trail-model.md` (should be checked before finalizing
  product lifecycle schema)
- `../../ecosystem/activity-trail-integration-map.md` (same)
