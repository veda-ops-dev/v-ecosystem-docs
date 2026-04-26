# Product Record Graph Posture — Spec Note

## 1. Purpose

This note resolves the graph-posture ambiguity identified as the last major
open question in the first-project V Forge record families spec note: whether
product records themselves are content graph nodes, or whether only their
page/content representations participate in the content graph while product
records remain adjacent execution records.

The answer affects how product durability relates to page churn, how graph
operations interact with product records, how affiliate-link adjacency connects
to the graph boundary, and whether the content graph remains page/content-
centered or becomes a broader record-covering structure.

---

## 2. Status

Transition-support spec note only.

This note is:
- a bounded graph-posture recommendation at working-spec level
- not final V Forge schema doctrine
- not a content graph redesign
- subject to revision after the first project exercises the model

---

## 3. Problem Being Solved

The content execution module defines the content graph as covering: pages,
topics, entities, internal links, and cluster structure — the execution truth
of what was built on owned surfaces and how it connects.

Product records are durable editorial objects. Product Detail Pages are page
representations built on top of product records. The question is whether those
two things — the durable editorial record and the built page — are the same
kind of graph citizen, or different kinds of things with a defined relationship
between them.

The ambiguity matters because:

- If product records are graph nodes, then graph operations (registration,
  update, maintenance, integrity checks) apply to product records directly —
  meaning that editing an editorial note, changing a classification, or
  retiring a product are graph operations.
- If only page representations are graph nodes, then the product record is
  stable editorial truth that the graph references rather than contains, and
  graph operations apply to the page layer without touching product durability.
- The affiliate-link placement note positioned affiliate links as
  "content-graph-adjacent" — meaning they join to products by product
  identifier while remaining outside the graph. If products are themselves
  graph nodes, affiliate links are one join away from a graph node. If products
  are outside the graph, affiliate links are two conceptual steps from the graph.
  The first is cleaner; the second is worth knowing explicitly.

---

## 4. Candidate Posture Options

### Option A — Product records are content graph nodes

Product records are first-class nodes in the V Forge content graph, alongside
pages, topics, entities, and internal links. Graph operations apply to product
records: creating a product record registers a graph node; updating editorial
content mutates a graph node; retiring a product is a graph deletion or
deactivation.

**In this model:**
- Product Detail Pages are page-layer realizations of product graph nodes
- The graph contains both the product node and the page node, with a graph
  edge connecting them
- Classification objects (Category, Recipient, Occasion) may also be graph
  nodes if they have page representations
- Affiliate-link records are adjacent to graph nodes (products)

**Strengths:**
- A single graph query can reach both the editorial record and the built page
- Classification relationships become graph edges, enabling traversal across
  the discovery structure

**Weaknesses:**
- Editorial operations on product records (update an editorial note, change a
  classification) become graph mutations — the graph changes every time editorial
  work happens
- Product record durability is coupled to graph integrity: a graph consistency
  check that fails could affect product record validity
- Graph operations are designed for content publishing structure; applying them
  to editorial records mixes two concerns
- When a product has no page yet (pre-publication state), it is a dangling
  graph node — the graph contains a node with no page realization, which is
  an awkward state for a graph meant to represent what was built

### Option B — Only page/content representations are graph nodes; product records remain adjacent execution records

Product records are V Forge execution records in `v_forge.*` — primary and
durable, but not graph nodes. Product Detail Pages are content graph nodes.
The page node carries a reference to the product record it represents. The
graph covers the page layer; the product record is what the page is built from.

**In this model:**
- Creating a Product Detail Page registers a graph node (the page)
- The page node carries a product identifier as a reference back to its
  source product record
- Updating editorial content on the product record does not mutate the graph;
  it mutates the product record, and the page node's reference to that record
  picks up the change at render or query time
- Product records can exist without any graph presence (pre-publication products,
  retired products)
- Affiliate-link records join to product records by product identifier;
  product records are adjacent to the graph through the page reference

**Strengths:**
- Product record durability is independent of graph state — editing, retiring,
  or restructuring product records does not trigger graph operations
- The content graph remains page/content-centered — it represents what was built
  and is publicly accessible, not the full editorial record set
- Pre-publication products exist cleanly outside the graph without creating
  dangling nodes
- Graph operations (registration, maintenance, integrity) remain scoped to
  built content without touching editorial operations
- The separation between "what exists as a product" and "what is live as a page"
  is explicit and inspectable

**Weaknesses:**
- To traverse from a page in the graph to its affiliate links requires two
  steps: page node → product identifier → affiliate-link records
- The graph does not natively contain product metadata — a graph query for
  "products featuring in Recipient Guide Pages" requires a join from page nodes
  to product records, not a pure graph traversal

### Option C — Hybrid: product records are lightweight graph reference nodes

Product records are represented in the graph as lightweight reference nodes
that contain the product identifier but not the full editorial record. The
full editorial record lives in the product record family. The graph node is a
thin graph anchor that enables graph traversal to and from pages without
making the full product record a graph citizen.

**In this model:**
- The graph contains a thin product reference node (identifier only, or
  identifier plus minimal graph-relevant fields like slug and status)
- The Product Detail Page node links to this thin product graph node
- Affiliate links remain adjacent to product records, not graph nodes
- Full editorial content queries go to the product record family; graph
  traversal uses the thin product node

**Strengths:**
- Enables single-hop graph traversal from page to product reference
- Keeps full editorial operations off the graph

**Weaknesses:**
- Introduces a dual representation: a thin graph node and a separate full
  editorial record for the same product — keeping them in sync is operational
  overhead
- The thin node must be updated when product identity changes (slug, status),
  creating a coupling between graph state and product record state that Option B
  avoids
- The benefit over Option B is modest: Option B's two-step traversal
  (page → product identifier → product record) is a join operation, not
  meaningfully harder than Option C's one-step traversal to a thin node

---

## 5. Evaluation Criteria

The recommended posture should:

1. **Preserve product durability independent of graph/page churn.** Product
   records should be valid and stable whether or not they have a live page
   representation. Editorial operations should not trigger graph mutations.

2. **Keep the content graph page/content-centered.** The content execution
   module defines the graph as what was built and how it connects. Product
   editorial records are what things are; pages are what was built. These are
   different concerns.

3. **Support clean pre-publication states.** Products that exist editorially
   but have not been published yet should not be awkward graph states.

4. **Support multiple page representations per product.** A product referenced
   on a Product Detail Page, a Recipient Guide Page, and a manual collection
   page has multiple graph representations. The product record is the stable
   identity behind all of them.

5. **Align cleanly with affiliate-link placement.** Affiliate links are
   adjacent to product records. The posture should not require re-deriving
   affiliate link placement.

6. **Stay coherent with current V Forge doctrine.** The content graph in the
   content execution module is built from execution — it records what was
   actually built. Product records exist before building; pages are the built
   artifacts.

---

## 6. Recommended Posture

**Option B — only page/content representations are content graph nodes;
product records remain adjacent execution records.**

Product records are V Forge execution records in `v_forge.*` — primary,
durable, not graph nodes. Product Detail Pages and other page representations
are content graph nodes that carry a reference back to the product record they
represent.

**Why Option B is best:**

The content execution module is explicit that the content graph records what
was actually built. A product record is not built — it is the editorial source
from which built content is derived. A Product Detail Page is built. That
distinction should be structural, not blurred by including product records as
graph citizens.

Option B preserves product durability most cleanly: editorial operations
(updating notes, changing classifications, retiring products) are product record
operations, not graph mutations. The graph reflects what is published; the
product record reflects what exists editorially. These are different dimensions
and should remain separate.

**Why Option A is weaker:**

The graph becomes responsible for editorial record integrity if product records
are graph nodes. Pre-publication products create dangling graph nodes. Every
editorial change to a product record becomes a graph mutation — which is wrong
for a graph designed to represent built/published structure.

**Why Option C is weaker than Option B:**

The dual-representation overhead (thin graph node + full editorial record) is
not worth the marginal traversal convenience. Option B's two-step traversal
(page node → product identifier via page's product reference → product record)
is a clean join with no meaningful operational cost. Option C's sync overhead
between graph node and product record is a persistent operational risk.

---

## 7. Relationship Between Product Record and Page/Content Graph

### The reference is on the page node, not the product record

When a Product Detail Page is built and registered in the content graph, the
page node carries a product identifier field that references the product record
it represents. The product record does not carry a graph node reference — it
does not know whether it has a page or not.

This is the same join-direction logic as affiliate links: the dependent artifact
(page, affiliate link) carries the reference to the primary artifact (product).
The primary artifact does not track its dependents in its own record.

### Multiple page contexts for one product

A product may appear in multiple graph contexts without the product record
being duplicated:

- Its Product Detail Page is one graph node, carrying the product identifier
- A Recipient Guide Page that features this product does not create a new
  product record; the guide page's graph node references the products it
  features through product identifier references
- A manual collection page similarly references products by identifier

In all cases, the product record is stable and singular. The graph contains
the pages; the pages reference products by identifier.

### Pre-publication products

A product record that exists but has no published Product Detail Page yet has
no content graph representation. It is a valid V Forge execution record — it
exists in `v_forge.*` — but it does not appear in the content graph. This is
the correct state: the graph represents what was built and published, not what
exists in editorial preparation.

When the Product Detail Page is published, the graph gains a new node. The
product record does not change. The graph registration is triggered by the
page publication event, not by the product record's creation.

### Affiliate-link adjacency in this posture

With Option B, the chain is:

```
Content graph node (Product Detail Page)
  → product identifier reference (on the page node)
    → Product record (in v_forge.*)
      → Affiliate-link records (in v_forge.*, by product identifier)
```

Affiliate links are two steps from the content graph — through the product
record. This is correct: affiliate links are not graph citizens and should not
be reachable through a single graph traversal. Monetization attachment is
a distinct concern from content graph structure.

### Graph integrity and product records

Graph integrity checks — ensuring that page nodes reference valid products,
that internal links resolve, that topic and entity references are coherent —
do not need to touch product record internals in Option B. A graph integrity
check can confirm that a page node's product identifier resolves to a valid,
active product record (by checking the product record's lifecycle state) without
those checks modifying the product record.

---

## 8. First-Project V1 Implications

### Product Detail Pages

Each published Product Detail Page is a content graph node that carries a
product identifier reference. The page node is registered in the graph at
publication time. The product record exists independently and is the stable
source of editorial truth for that page.

Publishing a Product Detail Page creates a graph node. Retiring a product
(setting it to discontinued or archived lifecycle state) does not automatically
remove the graph node — it flags the page for review or removal, which is a
separate governed action.

### Recipient Guide, Occasion Guide, and Category Browse Pages

These pages reference products but do not have a one-to-one relationship with
a single product. They are graph nodes that may carry lists of product
identifier references. The product records they reference are stable editorial
records; the guide page's content is assembled from those records at build or
render time.

In the graph, a Recipient Guide Page node references the products it features
through product identifier lists — these are not graph edges to product graph
nodes (since products are not graph nodes); they are data fields on the page
node that enable queries like "which pages feature product X?"

### Multi-context product reference

For v1, a product may appear on its own Product Detail Page and be referenced
from one or more guide or collection pages. The product record is stable across
all these contexts. The content graph contains multiple page nodes that each
carry references to the same product identifier, without any product graph node
being shared between them.

### What remains simplified for v1

- Each product has at most one Product Detail Page in v1 (no multi-variant or
  multi-region product pages)
- Guide pages reference products through product identifier lists; the graph
  structure for these references is simple for v1 scope
- The traversal pattern (page node → product identifier → product record) is
  functional without any optimization for v1 query volumes

---

## 9. Boundary / Ownership Posture

**V Forge owns both product records and the content graph as execution truth.**

Product records are V Forge execution records for what exists editorially.
Content graph nodes (pages) are V Forge execution records for what was built
and published. Both live in `v_forge.*`. The distinction is within V Forge's
execution truth domain, not across system boundaries.

**Project V plans what should exist.** The decision to create a product, the
decision to publish a Product Detail Page, the decision to structure the site
with Recipient Guides — these are planning decisions that arrive through the
governed handoff. V Forge executes them and records the results.

**VEDA observes what performs.** Search visibility, content signals, AI-surface
presence for products and pages — these belong in VEDA. V Forge's content graph
records what was built; it does not record how what was built is performing.

---

## 10. Open Questions

**How product identifier references on page nodes are stored**
The mechanism for a page node to carry product identifier references is not
specified here. Whether this is a foreign-key field (for single-product pages),
a join table (for multi-product pages), or a structured list field depends on
schema design decisions that belong in `v-forge/schema-specification.md`.

**Whether guide pages reference products through a dedicated join record**
For Recipient Guide Pages and similar multi-product pages, the relationship
between the page node and the product records it features may warrant a
dedicated association record (page_product_reference: page_id, product_id,
position/rank, context) rather than an array field on the page node. This is
a schema design choice that affects query patterns. Not settled here.

**Graph registration event for product-referencing pages**
When a Recipient Guide Page is registered in the graph, does it trigger a
scan to verify that all referenced product identifiers resolve to valid,
active product records? If so, when does that check run — at draft creation,
at publication, or on a scheduled cadence? Not settled here.

**Page retirement when product is discontinued**
When a product is set to `discontinued` or `archived`, what happens to pages
that reference it? A Product Detail Page with only a discontinued product
may need to be retired. A Recipient Guide Page that features one discontinued
product among many may only need its content updated. The governance of this
cascade is not specified here; it is a V Forge workflow concern.

---

## 11. Recommended Next Move

1. Treat Option B as the settled graph posture for the first-project V Forge
   slice. Product records are adjacent execution records; page representations
   are content graph nodes. Update the record families spec note to reflect
   this resolution of its open question.

2. When `v-forge/schema-specification.md` is authored, use this note's
   product-record-to-page-node relationship model as the starting point for
   the page node schema: page nodes carry product identifier references; product
   records do not carry graph node references.

3. Resolve the guide-page-to-product association design (join table vs. array
   field) at schema specification time. The choice affects query patterns for
   "which pages reference this product?" and "which products appear on this
   guide page?" — both of which are relevant to content maintenance operations.

4. Do not treat this note as final doctrine. First-project exercise will
   validate or challenge the Option B posture.

---

## 12. Related Files

- `first-project-v-forge-record-families-spec-note.md`
- `affiliate-link-placement-in-v-forge-note.md`
- `first-project-affiliate-link-record-posture-note.md`
- `first-project-v1-execution-packet-draft.md`
- `../first-project-entity-driven-gift-discovery-site.md`
- `../first-project-entity-driven-gift-discovery-planning-packet.md`
- `../../v-forge/v-forge.md`
- `../../v-forge/content-execution-module.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../../project-v/project-v.md`
