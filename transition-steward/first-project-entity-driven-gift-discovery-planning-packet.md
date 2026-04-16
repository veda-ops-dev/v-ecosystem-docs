# First Project Planning Packet — Entity-Driven Gift Discovery Site

> **Status at a glance:** Transition-support planning packet. **Not an admitted intake item.** No Project V intake event has been opened against this packet. Workflow-vocabulary references below describe what an intake event would look like *if and when* one is opened; they do not assert that intake has begun.

## Purpose

This document is a transition-support planning packet for the candidate first VedaOps proving-ground project: an entity-driven gift / product discovery affiliate site.

It exists to make the first-project shape operationally legible to Project V-style planning — thesis, constraints, success and kill conditions, open questions, and cross-system implications — without prematurely treating it as a Project V authority asset or as a finished intake outcome.

It is the planning-discipline counterpart to the project shape doc:

- shape: `first-project-entity-driven-gift-discovery-site.md`
- this packet: planning-side framing of that shape

---

## Status

Transition-support only.

This packet is **not an admitted Trigger Type B intake item** and is **not a governed intake outcome** under `workflows/project-intake-workflow.md`. No intake event has been opened against it. It is shaped to be usable as framing material for a future Trigger Type B intake — an operator-driven planning question with bounded framing attached — when first-project selection is ready to be tightened into a real intake event.

It is not Project V authority. It does not commit Project V to project creation. It does not bypass intake. Workflow-stage and approval-class language used elsewhere in this packet describes the intake event this packet *could later become input to*, not an intake event in progress.

It should be treated as a working planning packet while:

- first-project selection is being tightened
- the reusable archetype/pattern layer is not yet governed
- VedaOps planning and strategy-pattern surfaces are still maturing

---

## Project thesis

A small, branded, structured gift / product discovery site can be built and operated as a real monetizable first project while simultaneously serving as a deliberate proving ground for VedaOps planning, execution, observability, and review-gating.

The thesis depends on three claims standing together:

1. An entity-driven discovery model — canonical product records plus a small controlled classification layer plus genuine editorial curation — is structurally stronger than a generic affiliate blog or a programmatically generated taxonomy site.
2. Constrained v1 scope (small product set, narrow taxonomy, narrow indexable surface) is sufficient to validate the model and to expose VedaOps capability gaps without overwhelming maintenance.
3. The project's planning, execution, observability, and review-gating needs map cleanly onto the existing four-system ecosystem — Project V planning, V Forge execution, VEDA observation, VEDA Strategy derivation — without forcing any system to absorb work it does not own.

If any of those three claims fails in practice, the planning packet should be revisited before further commitment, not patched around.

---

## Why this is a strong first proving-ground project

- **Public-facing and monetizable** without the operational weight of SaaS, billing, or product-state management.
- **Failure cost is survivable.** A v1 that does not perform commercially is recoverable; a v1 that does not perform structurally still produces VedaOps learning.
- **Pressure-tests multiple VedaOps pipes at once:** intake framing, planning decomposition, handoff, execution under bounded doctrine, public publishing under review gates, content/asset continuity, and eventually observation and decay handling.
- **Constrainable.** The project shape allows v1 to be deliberately small without that smallness being a failure of ambition.
- **Has clear anti-patterns.** It is easy to identify what would make this project a generic affiliate blog instead of a structured discovery system, which gives planning a real check against drift.

The same characteristics that make it attractive also make it deceptively dangerous: traffic can look like success while revenue remains structurally weak, factual grounding failures are easy for an LLM to make and hard to catch late, and content and product records can decay silently. The kill/pivot section addresses these directly.

---

## Core project constraints

These are the constraints planning must preserve. They are derived from the project shape doc; this packet names them as planning-binding rather than aspirational.

- **Product is the only first-class durable object.** Categories, recipients, occasions, and interests are controlled vocabularies or governed classification objects, not equal peer entities.
- **Editorial curation is load-bearing**, not decoration. Every product carries a genuine human-written editorial note. Page-level featured/ranking decisions are editorial, not global product truth.
- **Page generation is not a function of taxonomy combinations.** Public indexable pages must earn their existence; combinatorial expansion is forbidden by default.
- **Public publishing is review-gated.** No public mutation occurs without governed review. Publishing is a governance-sensitive action, not an automation convenience.
- **Affiliate links are subordinate structured records attached to products**, not free-floating content fragments. Schema implications follow but are not solved here.
- **The site is the canonical branded layer.** Any future offsite branded reinforcement is reinforcement, not part of the same core ontology.

If a planning decision would weaken any of these, it is a planning failure and should be flagged before execution rather than absorbed silently.

---

## v1 boundaries

What v1 is allowed to do:

- carry roughly 50–75 manually curated products
- use a small controlled taxonomy (rough order: ~6–10 categories, ~7–10 recipients, ~5–6 occasions, ~8–10 optional interests)
- publish a constrained set of indexable surfaces (Product Detail, Recipient Guide, Occasion Guide, Category Browse, selected Recipient × Occasion pages, selected manual collections)
- accept practical near-term simplifications such as a single primary affiliate merchant, while not modeling that as the permanent shape

What v1 is **not** trying to do:

- prove every taxonomy combination
- prove full-scale site growth
- prove maximal traffic coverage
- exercise every offsite channel at once
- exercise every monetization pattern at once
- demonstrate broad automation autonomy

What v1 is allowed to be bad at, deliberately:

- traffic volume
- breadth of coverage
- merchant diversity
- offsite distribution
- automation surface area

These are not the v1 evaluation criteria.

---

## Structural rules planning must preserve

Carried forward as planning-binding, not restated in detail:

- **Product / classification / editorial / page separation.** Four distinct layers; planning must not let one absorb another.
- **Anti-page-explosion rule.** Not every relationship or filter state deserves a durable public page. Three-way intersections, interest-only pages, price-only pages, and filter-state URLs are not v1 indexable surfaces by default.
- **Curation as load-bearing.** The editorial layer is not metadata. Planning must not allow curation to be flattened into structured fields or generated prose.
- **Review-gated publishing.** Public mutation requires governed review. The harness rules in `../interfaces/llm-harness-architecture.md` apply: governance-sensitive actions complete through gate surfaces, not inline through any LLM tool call or chat phrasing.
- **Decay is a real systems concern.** Planning must treat product, link, and price decay as in-scope operational realities, not deferrable polish.

---

## Monetization posture

Affiliate links on relevant products and collections are the primary monetization mechanism. Recipient and occasion pages are the likely commercial/discovery hubs. Product pages are support/conversion endpoints rather than the only money pages.

Planning must avoid: traffic without buyer intent, novelty products that entertain but rarely monetize, unstructured dumping of products from one merchant, price-band spam pages, page sprawl without conversion logic.

For v1, dependence on a single affiliate merchant is an acceptable simplification but is not the permanent model. Planning should hold that distinction explicitly so it is not silently re-baselined as the architecture.

---

## Branded network posture

The site is the canonical branded money-site layer.

A later offsite branded reinforcement network — X, Pinterest, YouTube shorts/videos, Medium or article surfaces, other branded distribution assets — is anticipated but **explicitly out of v1 execution scope** unless separately admitted. Offsite assets, when they exist, act as reinforcement, distribution, and semantic support; they map back to canonical site objects but are not modeled as part of the same core ontology.

Planning must not let offsite-network ambition pull v1 scope outward.

---

## Operational realities

Planning must treat these as in-scope, not as later cleanup:

- **Product decay** — products go out of stock, get discontinued, become low-trust, or stop being meaningfully giftable. The site's lifecycle posture must support active / flagged / unavailable / discontinued / archived.
- **Affiliate link rot** — links go dead. Planning must include a recurring check cadence and a removal/replacement posture, not a hope that links stay live.
- **Stale pricing** — displayed prices drift from actual prices. Planning must decide what trust posture the site presents around price (live signal, "as of" stamp, deliberately omitted).
- **Editorial drift** — editorial notes age. Planning must decide when an editorial note needs review.
- **Maintenance load** — a 50–75 product v1 is small enough that operational load can be absorbed; the maintenance posture decided at v1 must scale to whatever growth is later authorized, or growth must be re-evaluated.

Operational realities that are not planned for at v1 will produce silent decay rather than visible failure, which is the worse failure mode.

---

## Success conditions

Early success is not "did pages get published." It is structural and operational:

- the entity-driven model stays structurally coherent under real product depth
- public page count grows only through earned existence, not through programmatic generation
- products remain maintained enough that the site does not visibly rot
- recipient and occasion discovery pages feel useful rather than synthetic
- affiliate monetization surfaces actually function and produce attributable revenue
- VedaOps handles intake, planning, handoff, execution, and review-gating cleanly for this project type
- the project surfaces real VedaOps capability gaps without collapsing into chaos
- editorial curation is doing visible work — the site reads like it was curated, not generated

Commercial success is desired but not the binary success criterion at v1.

---

## Kill / pivot conditions

The project should be paused, pivoted, or closed — not patched indefinitely — if any of the following hold after a fair v1 attempt:

- **Structural collapse.** The four-layer separation cannot be preserved in practice; categories, recipients, occasions, and interests collapse into each other or into Product properties; editorial decisions get absorbed into metadata.
- **Page sprawl.** Page generation policy fails in operation; combinatorial pages start appearing despite the rule; the indexable surface grows faster than editorial framing can support.
- **Editorial decay.** Editorial notes degrade into generated filler; per-page curation collapses into global product blurbs; the page-level featured/ranking distinction disappears.
- **Maintenance failure.** Product decay outpaces review cadence; dead affiliate links accumulate; the site starts presenting stale prices or out-of-stock products as live recommendations.
- **Monetization-structure conflict.** Pursuing revenue requires page patterns or merchant patterns that violate the structural rules; the only way to make money is to do the things v1 explicitly forbids.
- **VedaOps incompatibility.** The project cannot run cleanly under VedaOps planning, execution, and review-gating without the harness, intake, or workflow doctrine being repeatedly bent — which would mean either the doctrine or the project type is wrong for first-project use.
- **Proving-ground failure.** The project produces no useful VedaOps capability signal, either because it is too easy (no real gaps surfaced) or because the doctrine cannot bear the project's weight (gaps surface but cannot be addressed within bounded scope).

A kill or pivot decision is itself a Project V intake-side reconsideration event and should preserve continuity per `../governance/decision-continuity-doctrine.md` (referenced for posture, not invoked as authority by this packet).

---

## Open questions

These are real open questions that planning will need to resolve. They are not blockers to using this packet as Trigger Type B framing material; they are flagged for visibility.

- **Single-merchant v1 vs. multi-merchant from the start.** Single-merchant is simpler; multi-merchant exercises affiliate-attribution structure earlier. The planning packet does not pick.
- **What "review-gated public publishing" looks like operationally for a content site** — what governance class applies to a page publication, what the review surface is, how batch publishing relates to per-page review.
- **Whether VEDA observation of the site itself starts at v1** — branded search observation, AI-surface observation, performance observation — or whether v1 launches without ecosystem observation and adds it later.
- **Whether VEDA Strategy is in play at v1** at all, or only enters once enough surface and signal exist to derive anything useful from. Likely the latter; this should be made explicit at intake.
- **Editorial workload reality.** A 50–75 product set with genuine human-written editorial notes is non-trivial sustained editorial work. Planning needs to confirm capacity before committing to scope.
- **Schema implications of subordinate affiliate-link records.** The shape doc states the posture; the schema work belongs in V Forge content-execution design, not here. Flagged so it does not get smuggled into intake.
- **Decay-handling cadence.** What review and link-check cadence v1 actually commits to, and who or what runs it.
- **Kill/pivot evaluation cadence.** When the kill/pivot conditions are formally evaluated, not just informally felt.

---

## Implications for Project V

The section below uses workflow-stage vocabulary from `../workflows/project-intake-workflow.md` to describe what an intake event opened against this packet would look like. It does not assert that such an intake event has been opened. As of this packet's status, no intake event exists.

If this packet is later admitted as Trigger Type B framing for an intake:

- The intake item is bounded enough to frame at Stage 2: "Should we create a project to build a constrained v1 of an entity-driven gift discovery affiliate site as the first VedaOps proving-ground project, with the constraints in this packet?"
- Stage 3 interpretation should treat this as a candidate first proving-ground project and weigh it against the Why-this-is-a-strong-first-proving-ground claims and the kill/pivot risks.
- Stage 4 evaluation should determine whether the basis is sufficient to produce a Create outcome, or whether bounded evidence (e.g., merchant feasibility check, editorial capacity confirmation) should be requested before outcome.
- A Create outcome here would be governance-sensitive and almost certainly require human review per `governance/approval-mechanics-seam-model.md` Section E (Governed Intake Outcome Review).
- BYDA, per `../project-v/byda-in-project-v.md`, applies as the planning-side audit and readiness layer for whatever project this becomes; this packet does not pre-decide BYDA audit framing.

This packet is intake input. Project V remains the planning system of record.

---

## Implications for V Forge

Planning should anticipate, but not solve, that V Forge will need to support:

- product record execution flows, with affiliate links as subordinate structured records
- page and collection generation under bounded templates and rules, not programmatic combinatorial generation
- editorial support that preserves human judgment rather than flattening it into metadata
- review-gated public publishing as a governance-sensitive action, not an automation convenience
- continuity and traceability for content and page work, including page-level featured/ranking decisions that differ across contexts
- product lifecycle and decay handling

These are flagged as needs, not specified here. Schema, template, and execution-engine design belong in V Forge docs.

---

## Implications for VEDA / VEDA Strategy

Anticipated, not committed:

- **VEDA** observation of niche conditions, branded search and AI-surface presence, search-surface performance, and content/product decay signals where applicable. Whether any of this starts at v1 is an open question.
- **VEDA Strategy** derivation of opportunity, gap, and competitive signal — only meaningful once the site has enough surface and observed signal to derive anything from. Likely deferred past v1 launch.

Planning must not let either system absorb planning truth or execution truth from this project. Per cross-system boundary doctrine, signal informs; it does not command.

---

## Recommended next move

1. Treat this packet as the working planning packet for the first-project candidate.
2. The packet is **not intake-ready as written.** Before it can be offered as Trigger Type B framing material, the highest-priority open questions — at minimum editorial capacity, single vs. multi merchant, and whether v1 launches with VEDA observation — must be resolved or explicitly scoped as bounded evidence requests to route during intake.
3. When those are resolved, use this packet as Trigger Type B framing material for a real intake event under `../workflows/project-intake-workflow.md`. Do not let it function as an intake outcome on its own.
4. Do not universalize this packet into a general first-project archetype framework before the first real project actually exercises the structure.

---

## Related files

- `first-project-entity-driven-gift-discovery-site.md`
- `first-archetype-affiliate-content-site-note.md`
- `byda-spec-audit-findings-adjudicated.md`
- `transition-plan.md`
- `../project-v/project-v.md`
- `../project-v/byda-in-project-v.md`
- `../workflows/project-intake-workflow.md`
- `../v-forge/v-forge.md`
- `../interfaces/llm-harness-architecture.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
