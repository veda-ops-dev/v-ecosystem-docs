# First Project — Affiliate Link Record Posture Note

## 1. Purpose

This note closes the affiliate-link execution/schema seam exposed by the
first-project v1 execution packet exercise. The execution packet stated that
affiliate links are subordinate structured records attached to product records
and that merchant attachment belongs on the affiliate-link record — but did not
specify what that record posture actually requires at execution level.

This note defines the minimum execution-side record posture for affiliate links
in the first project: what the record shape must hold, how lifecycle states work,
how affiliate-link state relates to product state without collapsing the two, and
what is explicitly deferred.

It does not design the final schema. It makes the seam concrete enough that the
execution packet is no longer incomplete on this point and that later V Forge
doctrine or schema work has a working spec to build from.

---

## 2. Status

Transition-support spec note only.

This note is:
- concrete enough to close the named execution packet gap
- not final V Forge schema doctrine
- not a final record specification
- not implementation code
- subject to revision after the first project exercises the model

---

## 3. Problem Being Solved

The first-project planning materials establish the posture:

- affiliate links are subordinate structured records attached to products
- products are the primary durable objects
- affiliate links are not free-floating content fragments

But "subordinate structured record" is a posture statement, not a spec. At
execution time, V Forge needs to know concretely:

- what fields does an affiliate-link record hold?
- what lifecycle states does it support?
- how does a dead or stale link affect the product it is attached to?
- what happens when a merchant changes or a URL changes without the product
  changing?
- what does "single-merchant v1 simplification" mean structurally — does it
  change the record model or only the current population?

Without answers to these questions, a V Forge execution agent building or
maintaining product records and their affiliate links does not have a complete
execution model. The execution packet's posture statement is necessary but
not sufficient.

---

## 4. Proposed Record Posture

### Affiliate links are subordinate to products

An affiliate-link record has no independent existence outside its parent product
record. It exists only as an attachment to a product. Deleting or archiving a
product does not leave orphaned affiliate-link records — the links travel with
the product through its lifecycle.

The product is the unit of editorial and discovery truth. The affiliate-link
record is the unit of monetization attachment. These are distinct concerns that
must not be collapsed into a single flat record.

### Products remain primary

A product record is valid without any affiliate link attached. A product can
exist in discovery context — in editorial notes, in category pages, in recipient
guides — without being actively monetized. This is valid and should not trigger
lifecycle failure for the product.

A product with only dead or stale affiliate links remains a valid product.
The product's discovery and editorial value does not depend on its monetization
state. However, the absence of any active affiliate link is a signal that the
product should be reviewed — it may be appropriate to flag it but not to remove
it automatically.

### Merchant attachment belongs on the link record, not on the product

Merchant identity — which affiliate platform, which merchant, what tracking
parameters are used — is a property of the affiliate-link record, not a
property of the product itself. A product may have links from multiple merchants.
The product's canonical identity is independent of which merchants currently
carry it.

This is the key structural rule: the product does not know it is affiliated
through a specific merchant. The affiliate-link record knows which merchant it
came from.

### Affiliate links are not content fragments

An affiliate link record is a structured record with governed fields. It is not
a prose string embedded in product description text. It is not a URL embedded
in editorial copy. It is not a free-floating tracking pixel or referral code
divorced from the product record it serves. If affiliate link mechanics require
embedded URLs in rendered output, that embedding is derived from the structured
record at render time — the authoritative state lives in the record.

---

## 5. Minimum Structural Fields

The following field families represent the minimum execution-side record
structure for an affiliate-link record. These are semantic requirements, not
final schema field names.

**Identity**
A stable identifier for the affiliate-link record. Required to support linking
the record back to its parent product, tracking its lifecycle, and referencing
it from execution outputs.

**Parent product reference**
The canonical identifier of the product this link is attached to. Required.
A link without a parent product reference is an orphan and is invalid.

**Link target URL**
The actual URL used to send a visitor to the merchant's product page, including
any affiliate tracking parameters. Required for an active link.

**Merchant / source identity**
Which affiliate platform or merchant this link belongs to. Required. This is
the field that carries merchant attachment — it must not be a prose note but
a governed identifier (whether a formal enum or a controlled string depends on
implementation, but it must be structured and queryable).

**Link status / lifecycle state**
The current operational state of this link. Required. See Section 6 for the
proposed lifecycle states.

**Attribution identifier or tag**
The affiliate tracking tag, sub-ID, or similar attribution token that allows
revenue to be attributed to this site's referrals. Required for a monetizable
link. A link without an attribution identifier is a plain referral, not an
affiliate link, and should be distinguished.

**Created / added timestamp**
When this link record was created. Required for audit and freshness tracking.

**Last reviewed / verified timestamp**
When this link was last confirmed as live and accurate. Required to support
decay detection. A link with no reviewed timestamp should be treated as
unverified.

**Primary vs. secondary role flag** (conditional)
Where a product has multiple links — multiple merchants — one link may be
designated as the primary link for rendering purposes. This is optional for
v1 (single-merchant simplification means only one link per product initially)
but the record model should support it structurally from the start so that
multi-merchant support does not require a schema change later.

**Notes / remarks** (optional)
A governed optional field for brief human-authored notes about this specific
link — for example, why it was replaced, what the previous link pointed to,
or why a regional variation exists. This is not a prose-dump field. It is
a bounded human note for operational clarity.

---

## 6. Lifecycle / Decay Posture

Affiliate links decay. This is explicit in the planning materials. The site
should not silently accumulate dead links, broken monetization surfaces, or
stale affiliate URLs.

The following lifecycle states are proposed for v1:

**active**
The link is live, has been recently verified, and is expected to produce valid
referrals. This is the default operational state for a link in good standing.

**needs-review**
The link has not been verified within a reasonable cadence, or something has
triggered a review flag (e.g., a verification check failed, the product was
flagged for review, or a scheduled review interval has elapsed). The link is
still carried but should be verified before the next publication cycle or
review gate.

**dead**
The link target URL no longer resolves, returns an error, or leads to a page
that does not represent the intended product. Dead links must not be served
to users. A product with only dead links should be flagged for review at the
product level.

**replaced**
The link was previously active but has been superseded by a newer link record
(new URL, new merchant, or updated attribution). Replaced links should be
retained for audit purposes but must not be served as active links. The
replacement link record carries the active state.

**stale**
The link resolves but the linked page no longer accurately represents the
product — for example, the product is out of stock at the merchant, the price
is significantly different from what was current at editorial time, or the
merchant page has been substantially changed. Stale links may still function
mechanically but carry reduced trust. They should be reviewed and either
updated or moved to dead.

**merchant-changed**
A specific transition state for when the merchant relationship itself has
changed rather than just the URL — for example, an affiliate program was
discontinued, a merchant left the affiliate network, or the site has switched
to a different platform for this product. This is distinct from a dead link
because the product itself may still be purchasable elsewhere.

These states form a working lifecycle model. They are not exhaustive but cover
the cases the planning materials explicitly name (out of stock, dead links,
stale pricing, discontinued products, affiliate link rot).

---

## 7. Relationship to Product Lifecycle

Affiliate-link lifecycle and product lifecycle are related but distinct. They
must not be collapsed.

**A product can be active while its links are dead or stale.**
The product's editorial validity (is it a real, giftable product with a genuine
editorial note?) is separate from its monetization state (are its affiliate
links currently live?). A product that has temporarily lost all live links should
not be automatically removed from the site — it should be flagged for link review
while remaining editorially valid.

**A product can be discontinued while its links are technically live.**
A merchant might still carry a product page even after the product is no longer
manufactured. In this case, the product lifecycle state (discontinued) is the
driving factor, not the link state. The product should be transitioned out of
active publication regardless of link state.

**The product lifecycle controls publication eligibility.**
A product whose lifecycle state is discontinued, unavailable, or archived should
not be in active publication regardless of affiliate link state. The link states
are subordinate to the product's own editorial and lifecycle state.

**Multiple links per product is a supported model, even if v1 starts simple.**
A product may have links from multiple merchants. One may be dead while another
is active. The product should be considered monetizable as long as at least one
affiliate link is in active state. Link-level decay does not necessarily
mean product-level decay.

**Proposed separation rule:**
- Product lifecycle state governs whether the product should be published and
  discoverable.
- Affiliate-link lifecycle state governs whether the product is currently
  monetizable and through which merchant.
- Neither state drives the other automatically. A review process connects them.

---

## 8. First-Project V1 Posture

### What v1 requires

For the first project's v1 execution pass, the affiliate link model should be:

- **one primary affiliate link per product, from a single primary merchant**
  (single-merchant simplification is acceptable for v1)
- **all required fields populated**: link target URL, merchant identity,
  attribution identifier, lifecycle state, created timestamp, last-reviewed
  timestamp
- **lifecycle states in use from the start**: active and needs-review at
  minimum; dead and replaced as operational states for the first review cycle

### What can stay simplified for v1

- The primary / secondary role flag can default to primary for all v1 links
  since there is only one link per product initially
- Regional variants or source-specific notes are not required for v1
- Multi-merchant link management is not required for v1 but the record model
  must not assume single-merchant as permanent (see below)

### Single-merchant simplification: structural implications

The single-merchant v1 simplification changes the **current population** of
the affiliate link records, not the **record model**. Every product has one
link and it comes from one merchant — but the model should support multiple
links per product with different merchant identities from the start. Adding a
second merchant later should not require a schema change.

This is the key structural commitment: model for multiple merchants even if
v1 only uses one. The planning packet is explicit that the site should not
depend on a single merchant forever.

### What should be explicitly deferred

- Automated link verification / dead-link detection (can be manual for v1;
  the lifecycle state model supports it, but automation is not required)
- Cross-merchant comparison or pricing comparison logic
- Affiliate commission tracking or revenue attribution at record level
  (attribution identity supports this eventually; the analytics layer is
  not required for v1)
- Regional or locale-specific link variants

---

## 9. Boundary / Ownership Posture

### This is V Forge execution truth

Affiliate-link records are execution truth owned by V Forge under `v_forge.*`.
They are part of the content graph for the project — specifically, they are
subordinate monetization attachments to product records that are part of the
project's content execution footprint.

### Not Project V planning truth

Decisions about which merchants to affiliate with, whether to expand to new
affiliate networks, or when to pivot monetization strategy are planning decisions
that belong in Project V. The affiliate-link record carries what was decided and
what currently exists. It does not carry why.

A planning decision to change affiliate strategy returns to Project V through
planning discussion. It is not a V Forge execution-side authority decision.

### Not VEDA observability truth

External affiliate platform behavior — click counts, commission amounts, merchant
performance signals — is external signal that, if relevant to ecosystem decisions,
belongs in VEDA as observatory records. V Forge does not accumulate affiliate
platform analytics as canonical truth. A dead link is detected by operational
verification, not by importing affiliate platform analytics into V Forge records.

### External affiliate platform URLs are not canonical product truth

A merchant URL and its associated tracking parameters are not canonical truth
about the product. The product's canonical identity, description, and editorial
note do not derive from the merchant's product page. The affiliate link record
is an operational attachment — it connects the product to a purchase path.
Changes in that purchase path (new URL, different merchant, tracking parameter
update) do not change the product's canonical identity.

This is the structural rule that prevents affiliate link decay from corrupting
product truth: the product is what it is; the link only connects to where it
can be purchased.

---

## 10. Open Questions

**Verification cadence**
What review interval triggers a link moving from active to needs-review? This
is an operational policy decision — probably determined by product volume and
operational capacity, not by a universal rule. Not settled here.

**Dead-link detection mechanism**
For v1, manual verification is acceptable. Eventually, automated link-check
tooling would be useful. How that tooling integrates with the lifecycle state
model (who sets the state, how automatically vs. manually) is not specified here.

**Multi-merchant transition path**
When the site moves from single-merchant to multi-merchant operation, the record
model supports it but the operational process — how links from a new merchant
are added, how primary-link designation is managed, whether new merchants require
a planning decision or are an execution-side record addition — is not settled here.

**Revenue attribution record shape**
The attribution identifier supports external attribution tracking. Whether V Forge
maintains any revenue attribution records internally (for operational visibility,
not as analytics) is not settled. If it does, those records are V Forge execution
truth, not planning truth and not VEDA observability truth.

**Affiliate link record as part of the content graph**
The content execution module doc treats the content graph as containing pages,
topics, entities, and internal links. Where affiliate-link records sit relative
to that model — as content graph edges, as product sub-records, or as a distinct
record family within V Forge schema — is not specified in the content execution
module doc. This seam needs to be resolved when the V Forge schema specification
is authored.

---

## 11. Recommended Next Move

1. Treat this note as the working spec for affiliate-link record posture in the
   first project. The execution packet can reference this note as the governing
   spec for the affiliate-link seam until V Forge schema doctrine is written.

2. Flag the anti-page-explosion rule, publication-gating rule, and editorial-note
   requirement (already identified as doctrine candidates in the closure note)
   alongside the affiliate-link record posture as V Forge content execution
   doctrine candidates. The affiliate-link posture defined here — subordinate
   records, merchant attachment on the link record, lifecycle states — should
   eventually move into V Forge schema specification and content execution doctrine.

3. Resolve the "where do affiliate-link records sit in the content graph model"
   seam when the V Forge schema specification is being drafted. That is the most
   significant structural question this note leaves open.

4. Do not treat this note as final doctrine. First-project exercise will reveal
   whether the lifecycle states and field families are sufficient or need
   refinement.

---

## 12. Related Files

- `first-project-v1-execution-packet-draft.md`
- `../first-project-entity-driven-gift-discovery-site.md`
- `../first-project-entity-driven-gift-discovery-planning-packet.md`
- `first-project-digest-against-execution-packet-closure-note.md`
- `../../v-forge/v-forge.md`
- `../../v-forge/content-execution-module.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../../project-v/project-v.md`
