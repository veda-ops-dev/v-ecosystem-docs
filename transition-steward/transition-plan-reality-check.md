# Transition Plan Reality Check

## 1. Purpose

This note audits `transition-steward/transition-plan.md` against actual current repo state
to identify what the plan still gets right, where it now lags, what remains genuinely open,
and what the actual next control-step is.

It does not rewrite the transition plan. It is a bounded correction note.

---

## 2. What the Plan Still Gets Right

**The four-system architecture is correctly settled and stable.** The plan's core
architecture direction — one Postgres database, four schemas, strict logical separation,
VEDA as observatory-only, VEDA Strategy as derived intelligence, V Forge as execution
truth, Project V as planning truth — is reflected consistently in the landed authority
docs. No drift on this.

**Batch H partial posture is correctly described.** The plan accurately characterizes
Firecrawl as admitted and its `/crawl` and `/map` surfaces as doc-confirmed for schema
design purposes. The plan also correctly identifies the DataForSEO AI-surface family
work as unfinished. The `batch-h-waiting-on-provider-credits.md` note confirms the pause
is intentional and correctly scoped.

**The transition-support cluster hierarchy is correctly drawn.** The plan's description
of the `transition-steward/first-project-v-forge/` cluster as "transition-support side
work, not settled authority" remains accurate. The cluster README confirms this
classification. The plan correctly says this cluster should not be treated as a
replacement for the authority correction spine.

**Batch I (Qdrant doctrine) remains correctly blocked.** The plan says Batch I is
blocked pending external research review. Nothing in the current repo changes that.

**Batch K (VEDA Strategy interface full contracts) remains correctly deferred.** Both
VEDA Strategy signal interface docs are stubs with explicit Batch K deferral. No change.

**The "no VEDA Brain" and "no cross-schema convenience" rules are correctly landed.**
These are reflected in `veda/schema-reference.md`, `ecosystem/db-posture.md`, and the
V Forge system invariants. Stable.

---

## 3. What the Plan Now Lags or Overstates

**The plan does not reflect the new implementation-support doc set.** Six
transition-steward documents now exist that were not present when the plan was last
updated:
- `activity-trail-implementation-spec.md`
- `packet-schema-drafting-basis.md`
- `invariant-enforcement-plan.md`
- `minimum-codable-first-slice.md`
- `first-slice-implementation-task-breakdown.md`
- `coding-readiness-classification.md`

These represent a completed coding-readiness pass for the V Forge/handoff/approval-gate
first slice. The plan's "Immediate Next Control-Step" section calls for this pass as a
future item. It has been completed.

**The plan's "before coding proceeds" sequence is partially outdated.** The plan states:
> "A bounded coding-readiness classification pass must first classify what in the cluster
> is safe implementation guidance versus derivation history only."

This pass is now done and documented in `coding-readiness-classification.md`. The 13-file
coding packet for the first slice is defined. The first slice task breakdown is complete
to acceptance-criteria level. The specific "before coding proceeds" precondition the plan
named is satisfied for the first slice.

**The plan still frames Batch H as the primary remaining unfinished work without
distinguishing Firecrawl from DataForSEO.** The Firecrawl portion of Batch H has a
substantially completed design pass (`batch-h-veda-family-design-pass.md`) covering
nine canonical family definitions across Firecrawl and AI-surface domains. This design
pass is extensive and ready for authority-doc promotion review, but is still
transition-support only. The plan does not reflect that the design work is largely done
and what remains is the authority-promotion step (for Firecrawl) and the credits-gated
step (for DataForSEO AI-surface sampling).

**The plan's listed "actual next transition-control step" is now three steps behind.**
The plan's "Immediate Next Control-Step" reads:
1. Human reviews landed authority-correction work
2. Remaining Batch H doctrine work completed
3. A bounded coding-readiness classification pass is run
4. Only after that should coding proceed

Steps 3 and materially step 2 (for the first slice context) are now done. The
sequencing implied by the plan no longer matches where the repo actually is.

---

## 4. What Remains Genuinely Open

### Open because of missing doctrine/control work

**VEDA Batch H authority-doc promotion — Firecrawl families.** The nine canonical
family definitions in `batch-h-veda-family-design-pass.md` (four Firecrawl families,
five AI-surface families, `ObservatoryScope`, `TopicMonitor`) are transition-support
design work. They have not been promoted into `veda/schema-reference.md`. The
"Deferred Owned Domains" section of `veda/schema-reference.md` still shows these
domains as deferred. Promotion requires human review of the design pass for accuracy
and then a governed authority-doc update. Open questions in the design pass (Section 12)
must be resolved or explicitly deferred before promotion.

**`KeywordTarget` → `TopicMonitor` association mechanism.** Noted as open in the design
pass (question 12.3). Must be resolved before `TopicMonitor` is promoted to schema
authority.

**`ObservatoryScope` ↔ `TopicMonitor` cardinality.** Open question 12.2. Whether
`TopicMonitor` requires `ObservatoryScope` or may stand alone.

**Batch I (Qdrant doctrine).** Blocked on external research review. No doc in the repo
has changed this status.

**Batch K (VEDA Strategy full interface contracts).** Still deferred. Both stub
interfaces noted as Batch K pending.

### Open because of pending human review/acceptance

**Batches A through G, J, L landed on branch but not human-reviewed.** The plan notes
these are pending human review. Nothing in the implementation-support pass changes that.
These landed authority-correction docs have not been marked as accepted.

**Batch H design pass not yet reviewed.** `batch-h-veda-family-design-pass.md` is a
substantial transition-support document ready for review but not yet promoted.

### Open because of provider-credit blockers

**DataForSEO AI-surface family authority promotion.** As documented in
`batch-h-waiting-on-provider-credits.md`: the DataForSEO AI-surface families in the
design pass were derived from docs-only coverage for the unsampled endpoints (LLM
mentions, aggregated metrics surfaces). Promoting these families to authority requires
pulling actual payloads from those endpoints, which requires provider credits. The
design pass exists and covers these families in structural detail, but it explicitly
flags this as unverified for unsampled surfaces (design pass open question 12.4 and
12.5). Promoting docs-only structures without payload verification would be
overclaiming.

---

## 5. Provider-Credit-Specific Blockers

### Blocked by credits

**DataForSEO AI-surface family authority promotion for unsampled endpoints.** Specifically:
- LLM Mentions endpoint surfaces
- Aggregated AI-surface metrics surfaces
- Possibly Bing Copilot, Gemini, and Perplexity platform-specific behavior

The design pass has structural recommendations for these, but notes they are based on
documentation review, not live payload samples. The `batch-h-waiting-on-provider-credits.md`
explicitly states the resume condition: credits available → pull real payloads → compare
against design pass → promote only what is now evidenced.

### Not blocked by credits

**Firecrawl family authority promotion.** The Firecrawl surface shapes are
doc-confirmed and sample-confirmed per the `firecrawl-crawl-map-surface-inventory.md`
and the scrape baseline sample. The four Firecrawl families (`CrawlJob`, `CrawledPage`,
`CrawlFailureRecord`, `DiscoveryObservation`) in the design pass do not depend on
unsampled payloads. Their promotion to `veda/schema-reference.md` is not blocked by
provider credits. It is blocked only by human review and the open questions in the
design pass (12.1–12.3) being resolved or explicitly deferred.

**`ObservatoryScope` and `TopicMonitor` promotion.** These do not require provider
data. Their promotion depends on resolving the cardinality and association mechanism
questions in the design pass, then human review. Not credit-blocked.

**First-slice V Forge coding.** Entirely unrelated to provider credits. The handoff
acceptance + approval gate + activity trail slice has no provider dependencies. It can
be built immediately from the existing coding packet.

**All Batches A through G, J, L human review.** These are authority corrections to the
four-system ecosystem map, database posture, VEDA Strategy introduction, and V Forge
execution doctrine. None of them require provider data.

---

## 6. Actual Current Next Control-Step

**Human reviews and accepts (or corrects) the Batch H Firecrawl family design pass
(`batch-h-veda-family-design-pass.md`) and promotes the non-credit-blocked families
into `veda/schema-reference.md`.**

Rationale: This is the highest-value unblocked control-spine action currently available.
The design work is complete. The four Firecrawl families and the `ObservatoryScope` /
`TopicMonitor` families are not credit-blocked. The open questions in Section 12 of the
design pass (12.1–12.3) can be resolved or explicitly deferred during review. Promoting
these into `veda/schema-reference.md` would complete the largest remaining piece of
Batch H and unblock VEDA schema implementation for the Firecrawl domain.

The DataForSEO AI-surface family promotion remains paused pending credits — that is
correct and should not be forced.

The first-slice V Forge coding can start in parallel. It does not depend on this step.

---

## 7. Recommended Bounded Update to `transition-plan.md`

The plan needs one targeted update, not a rewrite. The update should:

**Add a new "Coding-Readiness Pass Complete" note under Current Transition Status:**

Record that the coding-readiness classification pass (listed as a future item in the
original plan) has been completed. The following implementation-support docs now exist
and constitute the first-slice coding-readiness output:
- `activity-trail-implementation-spec.md`
- `packet-schema-drafting-basis.md`
- `invariant-enforcement-plan.md`
- `minimum-codable-first-slice.md`
- `first-slice-implementation-task-breakdown.md`
- `coding-readiness-classification.md`

The first-slice 13-file coding packet is defined. The first slice (handoff acceptance +
approval gate + activity trail) can start from this packet without further transition-support
preparation.

**Update the "Immediate Next Control-Step" section:**

Replace the current four-step sequence with the actual current state:
1. Human reviews and accepts (or corrects) the Batch H Firecrawl design pass and
   promotes non-credit-blocked families into `veda/schema-reference.md`
2. DataForSEO AI-surface family promotion remains paused pending provider credits
3. First-slice V Forge coding may proceed in parallel from the defined coding packet

No other rewriting of the plan is warranted. The batch sequence, the architecture
direction, and the anti-drift rules remain accurate.

---

## 8. Related Files

- `transition-steward/transition-plan.md` — the control spine audited here
- `transition-steward/batch-h-waiting-on-provider-credits.md` — credit-block status
- `transition-steward/batch-h-veda-family-design-pass.md` — Firecrawl + AI-surface design pass
- `transition-steward/coding-readiness-classification.md` — first-slice coding packet
- `transition-steward/first-slice-implementation-task-breakdown.md` — 14 tasks for first slice
- `veda/schema-reference.md` — authority target for Batch H promotion
- `transition-steward/first-project-v-forge/README.md` — cluster status reference
