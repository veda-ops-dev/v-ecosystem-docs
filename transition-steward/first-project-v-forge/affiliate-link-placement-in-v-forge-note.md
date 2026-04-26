# Affiliate Link Placement in V Forge — Spec Note

## 1. Purpose

This note resolves the placement ambiguity named at the end of the affiliate-
link record posture note: where affiliate-link records belong in the V Forge
execution model, and what record-family posture best serves product primacy,
merchant/link separation, lifecycle independence, and future multi-merchant
viability.

It does not write schema. It decides the conceptual placement that later schema
and doctrine work should build from.

---

## 2. Status

Transition-support spec note only.

This note is:
- a bounded placement decision at working-spec level
- not final V Forge schema doctrine
- not a content graph redesign
- subject to revision after the first project exercises the model

---

## 3. Problem Being Solved

The affiliate-link posture note established:

- affiliate links are subordinate structured records attached to products
- merchant attachment belongs on the link record, not on the product
- link lifecycle and product lifecycle are distinct
- the single-merchant v1 simplification is a population decision, not a
  structural constraint

What it left open is the conceptual placement question:

> In V Forge terms, are affiliate-link records product sub-records, content
> graph records, content-graph-adjacent records, or a distinct execution record
> family?

This matters because the content execution module doc defines the content graph
as covering pages, topics, entities, internal links, and cluster structure —
all of which are discovery/publishing concerns. Affiliate links are monetization
concerns. Conflating them creates a content graph that mixes editorial and
commercial substructure, which has ongoing maintenance and clarity costs.

The placement decision affects:
- how execution completeness is evaluated in execution packets
- whether the content graph can stay focused on discovery/publishing truth
- how decay and lifecycle handling attaches without contaminating graph integrity
- whether V Forge schema work starts from a clean separation

---

## 4. Candidate Placement Options

### Option A — Affiliate links as product sub-records

Affiliate-link records are a subordinate field family on the product record.
They live inside the product record in the same way that price or image
references do — as structured sub-fields rather than as separate first-class
records in their own right.

**Characteristics:**
- affiliate-link state is directly coupled to product state
- querying all affiliate links for a product means querying inside the product
  record
- lifecycle transitions on a link require updating the product record
- multiple links per product require either an array/JSON column or a joined
  sub-table that is conceptually part of the product row

**Problems:**
- link lifecycle changes (a single link goes dead) require touching the product
  record, which should be stable editorial truth
- querying across all links — e.g., "find all dead links across all products" —
  requires traversing product records rather than querying a link record set
- the product record becomes a mixed editorial/commercial artifact
- this posture makes merchant churn visible at the product record level, which
  violates the separation rule

### Option B — Affiliate links as content graph records

Affiliate-link records are treated as part of the V Forge content graph — edges
or nodes in the same graph structure that holds pages, topics, internal links,
and entities.

**Characteristics:**
- affiliate links become graph citizens alongside editorial/discovery nodes
- the content graph becomes responsible for lifecycle and decay of commerce
  records as well as editorial records
- graph operations (registration, update, maintenance) apply to affiliate links
  the same way they apply to page nodes

**Problems:**
- the content graph is defined in the content execution module as covering
  discovery and publishing truth: pages, topics, entities, internal links,
  cluster structure. Commerce substructure is a different concern.
- overloading the content graph with affiliate link records means that graph
  integrity checks, graph maintenance operations, and graph traversal all
  involve monetization state — which is not what those operations are designed
  for
- this makes the content graph harder to reason about and harder to maintain
  cleanly
- it couples editorial/discovery truth to commercial/monetization truth in
  the same data structure

This option is the weakest. The content graph should not absorb commerce
substructure.

### Option C — Affiliate links as content-graph-adjacent records

Affiliate-link records are V Forge execution truth, stored separately from the
content graph but linked to product records that may themselves be part of the
content graph. They are adjacent to the graph — aware of it, linked to product
identities that exist in it — but not graph citizens themselves.

**Characteristics:**
- affiliate links live in a distinct record family within `v_forge.*`
- they reference product records by product identifier
- the content graph does not contain affiliate-link nodes or edges
- lifecycle management operates on the affiliate-link record family
  independently of graph operations
- querying all dead links across all products is a query against the
  affiliate-link record family, not a graph traversal

**Strengths:**
- product records remain stable editorial/discovery artifacts
- the content graph remains focused on discovery/publishing structure
- link lifecycle transitions do not touch product records
- multi-merchant expansion is straightforward (add more link records referencing
  the same product)
- decay handling (link verification, stale detection) operates on its own record
  family with its own operational cadence

**Weaknesses:**
- introduces a record family outside the content graph that still references
  graph-adjacent product records — requires clear documentation that this is
  intentional, not an oversight
- the product-to-affiliate-link join is explicit rather than structural — a
  query must reference product identity to retrieve its links

### Option D — Affiliate links as a distinct V Forge execution record family,
fully independent of the content graph

Affiliate-link records are a wholly separate execution record family in
`v_forge.*` that references products by identifier but has no structural
relationship to the content graph at all. They are execution truth about
monetization, treated as a parallel record concern to the content graph
rather than adjacent to it.

**Characteristics:**
- same as Option C but more explicitly separated — "adjacent" is replaced
  with "parallel and independent"
- product identifier is the join key; the relationship is explicit but loose
- graph operations never touch affiliate records; affiliate record operations
  never touch the graph

**Compared to Option C:** The practical difference between C and D is mainly
conceptual framing. Option D emphasizes full independence; Option C acknowledges
adjacency through shared product identity. For a project where products are
content graph nodes (pages, entities), Option C's "adjacent" framing is more
accurate. For a project where product records are execution records that may
or may not have content graph representations, the distinction collapses.

---

## 5. Evaluation Criteria

The recommended placement posture should:

1. **Preserve Product as primary durable object.** Product records should not
   need to change when affiliate links are added, removed, or cycled.

2. **Keep merchant attachment on the link record.** No merchant identity should
   appear as a product property.

3. **Support link lifecycle independently from product lifecycle.** A single
   link going dead should not require a product record update.

4. **Avoid overloading the content graph.** The content graph covers
   discovery/publishing structure. Commerce substructure is a different concern
   and should not be mixed into it.

5. **Support v1 single-merchant simplification without hard-coding it.** The
   structural model must accommodate multiple links per product from the start.

6. **Align with current V Forge doctrine.** The content execution module defines
   execution truth as covering what was built on owned surfaces. Affiliate links
   are part of what was built — they are the monetization attachment to content
   execution work. They belong in V Forge execution truth. The question is only
   which record family classification is cleanest.

7. **Support cross-link operational queries.** Finding all dead links, all
   links from a given merchant, all links not reviewed within a cadence, should
   be possible as queries against the affiliate-link record family without
   requiring product-level traversal.

---

## 6. Recommended Placement Posture

**Option C — content-graph-adjacent execution record family.**

Affiliate-link records are a distinct record family within `v_forge.*`, separate
from the content graph, linked to product records by product identifier, and
governed by their own lifecycle and operational posture.

They are not product sub-records (Option A) because link lifecycle must remain
independent of product record state.

They are not content graph records (Option B) because the content graph should
not absorb commerce substructure.

Option D (fully independent) and Option C differ mainly in framing. Option C is
preferred because "adjacent" more accurately describes the relationship: affiliate-
link records reference products that may themselves have content graph
representations. Calling them "adjacent" keeps the relationship legible without
implying they are graph nodes.

**The recommended posture in plain terms:**

> Affiliate-link records are a distinct V Forge execution record family, separate
> from but adjacent to the content graph. They reference product records by
> product identifier. They are owned by V Forge execution truth in `v_forge.*`.
> They have their own lifecycle posture. The content graph does not contain
> affiliate-link nodes. Product records do not contain affiliate-link sub-fields.
> Affiliate links join to products; products do not carry their links as embedded
> properties.

**Why the rejected options are weaker:**

Option A (sub-records) couples link lifecycle to product record stability. Every
link change touches the product record. This is wrong: editorial product truth
should not change because a merchant link died.

Option B (graph records) overloads the content graph with commerce concerns. The
content graph is defined as covering discovery/publishing structure. Putting
monetization records in it violates that scope.

Option D (fully independent) is nearly identical to Option C but unnecessarily
implies no relationship. Products and their affiliate links have a real join
relationship; "adjacent" captures this better than "fully independent."

---

## 7. Relationship to the Content Graph

Affiliate-link records are **outside the content graph proper**.

The content graph — as defined by the content execution module — covers:
pages, topics, entities, internal links, cluster structure, and content graph
relationships used for discovery and publishing. It represents what was built
and how it connects editorially.

Affiliate links represent monetization attachment. They are execution truth
about how content connects to purchase paths, not about how content connects
to other content. They do not belong in the same record structure as page nodes,
topic clusters, or internal link edges.

**The join relationship:**

A product record that has a content graph representation (for example, a Product
Detail Page) connects to the affiliate-link record family through the product
identifier. The content graph node references the product; the product identifier
is the key that retrieves the product's affiliate links. The graph does not
traverse into affiliate links. Affiliate link operations do not traverse the graph.

**When a product has no content graph representation** (a product record that
exists but whose page has not yet been published), the affiliate-link records
still exist and are valid. This confirms that affiliate links are not graph-
dependent — they are product-dependent. The graph representation is one possible
surface for a product; the affiliate-link record is a monetization attachment
to the product regardless of its graph state.

---

## 8. First-Project V1 Implications

### Execution completeness

With the placement posture settled, the execution packet for v1 can be considered
complete for the affiliate-link seam. The packet states:

- affiliate links are subordinate structured records attached to products
- merchant attachment belongs on the link record

The placement note adds: affiliate-link records are a distinct record family in
`v_forge.*`, separate from the content graph, joining to products by product
identifier. An execution agent building product records for v1 knows where to
attach affiliate-link records and how to maintain them without touching product
editorial state.

### Single-merchant v1 simplification

The placement posture supports this cleanly. With one merchant, every product
has zero or one affiliate-link records in the link record family. Adding a second
merchant means adding additional link records referencing the same product
identifier — no structural change required.

The placement as a separate record family (not sub-records) is what makes this
work: multi-merchant is a record population concern, not a schema change.

### What remains simplified for v1

- All affiliate links reference a single merchant identifier (one merchant)
- Link verification is manual rather than automated
- No cross-merchant comparison or primary/secondary designation logic is
  operationally required (though the record model supports a primary flag
  from the start per the posture note)

---

## 9. Boundary / Ownership Posture

**V Forge owns affiliate-link records as execution truth.**

These records are in `v_forge.*`. They represent what was executed — which
products have which affiliate links, in what state, from which merchant. They
are not VEDA observability records. They are not Project V planning records.

**Project V plans the monetization strategy.** Decisions about which affiliate
platforms to use, when to diversify merchants, or when to retire a monetization
channel are planning decisions. They belong in Project V and arrive at V Forge
through the governed handoff. V Forge executes the resulting affiliate link
record changes.

**VEDA observes external affiliate performance.** If click data, conversion
data, or affiliate platform analytics are relevant to ecosystem decisions, they
belong in VEDA as observatory records — not in V Forge affiliate-link records.
V Forge's affiliate-link records are operational state (is this link live?), not
analytics (how is this link performing?).

**External affiliate platform URLs and tracking parameters are not canonical
truth.** The affiliate-link record carries these as operational data, but they
are mutable — merchants change URLs, affiliate programs change tracking
parameters. Changes to external URLs do not change the product's identity or
editorial state. V Forge affiliate-link records reflect the current operational
state of monetization attachments; they do not define product truth.

---

## 10. Open Questions

**Content graph registration for product records**
The placement posture says affiliate-link records are outside the content graph
but adjacent to product records that may have content graph representations.
Whether product records themselves are content graph nodes, or whether only
Product Detail Pages (the page layer) are content graph nodes, is not settled
in this note. If product records are not content graph nodes, the "adjacent to
the content graph" framing is slightly inaccurate — it would be more precise
to say "linked to products; products may or may not have graph representations."
This seam should be clarified when V Forge schema specification is written.

**Lifecycle event triggers and operational workflow**
Who runs link verification? What triggers a lifecycle state transition? How
does the operator or system initiate a review cycle? Not settled here — this
is an operational design question for V Forge workflow docs.

**Activity trail for affiliate-link record changes**
Whether affiliate-link lifecycle transitions produce activity trail records (per
the activity trail model) is not addressed here. Given that dead-link accumulation
is a real operational risk, some trail visibility seems appropriate, but the
exact event classification is deferred.

**Schema naming and field specifics**
The posture note proposes field families; this note confirms the record family
placement. Actual schema field names, column types, index strategy, and
constraint design belong in `v-forge/schema-specification.md` when that doc is
authored.

---

## 11. Recommended Next Move

1. Update the first-project v1 execution packet draft to reference this placement
   note as the governing spec for the affiliate-link seam. The packet can state:
   "affiliate-link records are a distinct V Forge execution record family,
   separate from the content graph, linked to product records by product
   identifier. See affiliate-link-placement-in-v-forge-note.md for posture."
   This closes the packet's remaining completeness gap.

2. When V Forge schema specification work begins, start the affiliate-link
   record section from the posture note (field families, lifecycle states) and
   this placement note (record family classification, content graph relationship).
   These two notes together are the working spec for that schema section.

3. Resolve the "are product records content graph nodes?" question at V Forge
   schema time. The answer affects whether "content-graph-adjacent" is precise
   or needs to be reframed as "product-linked."

4. Do not treat this note as final doctrine. It is a bounded placement decision
   at working-spec level. First-project exercise will validate or challenge it.

---

## 12. Related Files

- `first-project-affiliate-link-record-posture-note.md`
- `first-project-v1-execution-packet-draft.md`
- `../first-project-entity-driven-gift-discovery-site.md`
- `../first-project-entity-driven-gift-discovery-planning-packet.md`
- `../../v-forge/v-forge.md`
- `../../v-forge/content-execution-module.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../../project-v/project-v.md`
