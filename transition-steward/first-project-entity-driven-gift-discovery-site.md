# First Project — Entity-Driven Gift Discovery Site

## Purpose

This document captures the working shape of the likely first VedaOps proving-ground project: an entity-driven gift / product discovery affiliate site.

It exists so the first project can be reasoned about deliberately rather than by defaulting to generic affiliate-blog assumptions, and so VedaOps planning, execution, observability, and review-gating can be exercised against a concrete first target.

---

## Status

Transition-support only.

Not a final archetype commitment. Not yet a Project V authority asset. To be treated as a working first-project specification candidate while:

- first-project selection is being tightened
- the reusable archetype/pattern layer is not yet governed
- the VedaOps planning and strategy-pattern surfaces are still maturing

---

## Why this project exists

This project is intended to do two things at once:

1. act as a real monetizable first project
2. act as a proving ground for VedaOps itself

The site existing is not the bar. The project must pressure-test Project V intake and planning, entity/taxonomy/editorial/page-layer separation, V Forge execution under bounded doctrine, review-gated public publishing, and continuity and traceability across the work. It is therefore a deliberately constrained first run, not a maximal niche-site build.

---

## Project type

A branded product-discovery site that helps users find gifts by recipient, occasion, category, and selected thematic interests, using canonical product records, editorial curation, and tightly governed page generation.

It is not a generic affiliate blog, a giant gift catalog, a page-factory for every taxonomy combination, a novelty-sharing site, or a listicle site with affiliate links bolted on. It must behave like a structured discovery system with curation, not like SEO sludge with products attached.

---

## Structural model

The first-project structure should be understood in four layers.

### 1. Product / data layer

The core durable structured object is the **Product**.

Each product should have:

- canonical identity
- slug / canonical URL
- title
- short factual description
- current price or price signal
- availability / lifecycle state
- brand / maker as product property
- one or more affiliate links with merchant attribution
- images
- date added / date reviewed
- human-written editorial note

Affiliate links should be treated as subordinate structured records attached to products, not as free-floating content fragments.

### 2. Classification / facet layer

A small controlled set of classification dimensions:

- **Category** — what kind of product this is
- **Recipient** — who the gift is for
- **Occasion** — when / why the gift is relevant
- **Interest / Theme** — a weaker optional thematic dimension
- **Price** — stored as a product property, with price bands treated as derived filter facets, not a primary page engine

These dimensions are not equivalent and should not be modeled as equal peer entities. For first-project purposes:

- Product is the only strongly modeled first-class durable object
- Category / Recipient / Occasion / Interest are controlled vocabularies or governed classification objects
- Price band is a derived facet for filtering, not a primary content object

### 3. Editorial / curation layer

This layer is load-bearing. The site must not pretend curation is just metadata.

It includes why a product is a good gift, why it fits a recipient or occasion, how products are ranked or selected on a page, top-pick / featured-pick logic, page-level curation framing, and manual collections and discovery paths.

This layer requires human judgment. It must not be reduced to generated filler around structured data.

### 4. Indexable page layer

Not every useful relationship or filter should create a public page. The project must explicitly separate:

- what exists in structured product/classification data
- what can be used internally for filtering or composition
- what deserves a durable public URL
- what deserves indexing

This separation is one of the main anti-slop protections for the project.

---

## v1 posture

The first version should be intentionally constrained.

**v1 should prove:** the entity-driven discovery model is workable, curation can remain strong under system support, VedaOps can plan and execute this cleanly, combinatorial page bloat is avoided, stale-product and broken-link maintenance does not collapse the site, and a small set of pages each earn their existence.

**v1 should not try to prove:** every taxonomy combination, full-scale site growth, maximal traffic coverage, every offsite channel at once, every monetization pattern at once, or broad automation autonomy.

---

## Recommended v1 scope

### Product volume

A small, manually curated product set in the working range of **50–75 products**. Enough to create meaningful pages; not enough to cause maintenance collapse.

### Classification scope

Practical v1 targets, not hard doctrine:

- **Category:** ~6–10 controlled top-level terms
- **Recipient:** ~7–10 strong terms
- **Occasion:** ~5–6 strong terms
- **Interest / Theme:** ~8–10 optional weaker terms, secondary use only

Actual counts should follow product depth and usability, not vanity taxonomy.

### Relationships

Store only the strongest useful relationships:

- Product → Category (required)
- Product → Recipient (required)
- Product → Occasion (optional)
- Product → Interest (optional)

Derive rather than manually store where possible: price band, similar products.

### Indexable page types for v1

Allowed by default:

- Product Detail Page
- Recipient Guide Page
- Occasion Guide Page
- Category Browse Page
- selected Recipient × Occasion pages, only when justified
- selected manual collections

Not default v1 indexable surfaces:

- Interest-only pages
- Price-only pages
- Recipient × Interest pages
- Category × Recipient pages
- any three-way intersection pages
- filter-state pages

These may exist internally as composition or filtering surfaces. They should not automatically become public indexable pages.

---

## Page-generation policy

Explicit anti-explosion rule:

> Not every relationship or filter state deserves a durable public page.

Public pages should generally require real user/discovery value, enough product depth to avoid thinness, meaningful editorial framing, structural coherence, and a reason to exist beyond "the combination is technically possible."

Explicitly avoid programmatic generation of every recipient/occasion/theme combination, indexable filter-state URLs, low-depth pages created only to capture query permutations, price bands treated as standalone page engines, and treating every taxonomy term as a page that must exist.

**Recipient × Occasion pages** are the strongest likely intersection pages for v1, but should be created only where the pair is genuinely useful, product depth is adequate, editorial framing is real, and the page is intentionally approved rather than auto-generated.

---

## Curation rules

The project lives or dies on curation quality.

Products qualify when they are actually purchasable, current enough to trust, meaningfully giftable for at least one real recipient use case, not obvious junk padding, and not included only to inflate page counts.

Products should be rejected or flagged when they are stale, low-trust, persistently out of stock, disposable junk, poorly described, or generic commodity clutter that adds no discovery value.

Every product carries a genuine human-written editorial note. The editorial layer is part of the site's value and one of the main reasons it does not become thin-affiliate sludge.

Ranking and featured picks are page-level editorial decisions, not global product truth. A product may be featured on one recipient page, absent from another, and framed differently in different collection contexts. The system should support that, not flatten it.

---

## Product lifecycle / decay posture

Product decay is a real systems concern. VedaOps should eventually support awareness of out-of-stock state, discontinued products, stale pricing, dead affiliate links, and no-longer-worthy products.

Lifecycle states should eventually support: active, flagged for review, unavailable / out of stock, discontinued, archived / replaced.

**v1 operational posture (simple but explicit):** review active products regularly, check affiliate links on a recurring cadence, update or remove stale products rather than letting dead records linger, do not let broken monetization surfaces silently persist.

---

## Monetization posture

Monetized project, but monetization must not distort structure into junk.

Primary posture: affiliate links on relevant products and collections; recipient and occasion pages as likely commercial/discovery hubs; product pages as support/conversion endpoints rather than the only money pages.

Anti-patterns to avoid: traffic without buyer intent, novelty products that entertain but rarely monetize, unstructured dumping of products from one merchant, price-band spam pages, page sprawl without conversion logic.

The project should not depend on a single merchant forever, even if one merchant is easier early. v1 may accept that simplification; the structure must not assume one affiliate source is the permanent model.

---

## Branded network relationship

The site is the **canonical branded money-site layer**. It may later be supported by an offsite branded reinforcement network — X posts, Pinterest pins, YouTube shorts/videos, Medium or article surfaces, other branded distribution assets.

Those offsite assets must not be modeled as if they are part of the same core ontology as canonical site objects. The site remains canonical discovery structure; offsite assets act as reinforcement, distribution, and semantic support, mapping back to canonical products, guides, collections, recipients, occasions, or campaigns.

This relationship is expected, but not part of first-project v1 execution scope unless explicitly admitted later.

---

## VedaOps implications

This project is a proving ground, so it implies system needs.

**Project V should eventually support:** tighter first-project intake for this project type, entity/classification/editorial/page-layer separation in planning, explicit page-generation policy, explicit anti-explosion constraints, and project-level success / kill / pivot conditions.

**V Forge should eventually support:** product record execution flows, page and collection generation under bounded templates and rules, editorial support without flattening judgment into metadata, review-gated public publishing, and continuity and traceability for content / page / asset work.

**VEDA / VEDA Strategy should eventually support:** niche and opportunity observation, branded search / AI-surface / search-surface observation where relevant, performance and decay signals, opportunity and gap interpretation that does not collapse into planning truth.

**Harness / continuity posture should support:** context assembly for this project type, preservation of planning and decision continuity, review gates before public mutation or publication, and compaction that does not destroy load-bearing project constraints.

---

## What success would mean

Not judged only by "did pages get published." Early success looks like the model staying structurally coherent, page sprawl prevented, products maintained enough to trust, recipient and occasion discovery pages feeling useful rather than synthetic, monetization surfaces real and functioning, VedaOps handling planning/execution/review cleanly, and the project exposing real missing capabilities without collapsing into chaos.

This is a proving-ground success posture, not just a publishing posture.

---

## What should be explicitly deferred

To protect the first run, defer:

- full-scale taxonomy expansion
- deep subcategory trees
- three-way page intersections
- fully indexed interest page systems
- aggressive offsite branded network rollout
- autonomous publishing
- advanced merchant comparison logic
- giant novelty-product catalogs
- every possible automation loop at once

The first project should be allowed to stay small enough to remain legible.

---

## Recommended next move

1. Use this as the working first-project shape.
2. Derive a tighter Project V intake / planning packet for this project type.
3. Later extract the reusable structural pattern into a more general doc once first-project learning stabilizes.

Do not universalize the pattern before the first project proves the structure in practice.

---

## Related files

- `transition-plan.md`
- `first-archetype-affiliate-content-site-note.md`
- `byda-spec-audit-findings-adjudicated.md`
- `../project-v/project-v.md`
- `../project-v/byda-in-project-v.md`
- `../workflows/project-intake-workflow.md`
- `../v-forge/v-forge.md`
- `../interfaces/llm-harness-architecture.md`
