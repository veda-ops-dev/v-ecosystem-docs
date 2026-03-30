# Paid Data Pull Governance

## Purpose

This document defines how paid external data retrieval is governed inside
the V Ecosystem.

It exists to answer:

```text
When may the ecosystem pull paid external data, what must be true before a
paid data pull occurs, how is spend authorized and bounded, and what rules
prevent paid data access from becoming ungoverned, unbounded, or operationally
invisible?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what constitutes a paid data pull inside the V Ecosystem
- what preconditions must be satisfied before a paid data pull occurs
- how spend authorization is established and bounded
- how paid data pull scope is prevented from widening silently
- how paid data pull outcomes must be reported and preserved
- the anti-drift rules operators and LLMs must preserve when evaluating
  whether a paid data pull is authorized

---

## Out of Scope

This document does not define:

- vendor-specific API credentials or authentication mechanics
- implementation-specific rate limiting or retry logic per provider
- detailed contract terms with individual data vendors
- post-admission data storage design for imported evidence

Those belong in implementation, vendor-specific, and project-local docs.

---

## System

- governance

---

## Core Rule

A paid data pull must not occur unless it is explicitly authorized, bounded
by approved scope and spend, attributable to a governed actor, and reportable
through the governed reporting path.

A paid data pull is not authorized because:

- the data would be useful
- a similar pull was done before
- the budget generally allows for it
- an agent believes the pull is warranted
- implementation convenience suggests it

Authorization must be explicit, bounded, and current for the specific pull.

---

## Paid Data Pull Definition

A paid data pull is any external data retrieval action that:

- incurs direct financial cost per call, per record, or per volume
- consumes a billable quota against a vendor account
- triggers spend against a paid subscription or usage-based service
- uses a paid API key, paid credential, or paid access tier

Examples include:

- paid SERP data provider calls
- paid search intelligence platform queries
- paid content intelligence or SEO data pulls
- paid citation or backlink data retrieval
- paid social or audience intelligence queries
- any external data retrieval billed by usage rather than covered by a
  flat subscription already explicitly pre-authorized for unbounded use

A flat subscription does not automatically authorize unbounded paid calls.
Pre-authorization for a subscription covers the subscription itself.
Individual pull volume, scope, and frequency still require explicit bounded approval
unless a specific unbounded pull posture has been explicitly governed.

---

## Relationship to External Action Governance

Paid data pulls are a specific subset of Class E4 external actions as defined
in `external-action-governance.md`.

The baseline E4 rules apply:

- explicit governed approval is required before execution
- informal direction does not substitute for governed approval
- scope must be bounded before the pull occurs
- actor legitimacy must be confirmed
- the pull must be reportable through the governed reporting path

This document refines those baseline rules specifically for the paid data
pull context, including spend authorization, vendor classification,
pull-scope bounding, and outcome reporting.

Where this document is silent, the baseline E4 rules from
`external-action-governance.md` apply.

---

## Pull Authorization Rule

A paid data pull is authorized only when all of the following are confirmed
before the pull occurs:

- the pull is explicitly approved for the specific query, scope, and vendor
- the spend level is within the explicitly approved budget for this pull
- the actor performing the pull has the required authority for this action class
- the pull is tied to a specific governed planning, observatory, or operational need
- the pull remains inside the approved scope and has not widened since authorization

If any of those conditions is missing or unclear, the pull must not proceed.

An agent must not self-authorize a paid data pull.
A human operator expressing interest in data is not the same as governing approval
for a specific paid pull.

Time sensitivity does not relax authorization requirements.
If a pull opportunity appears time-sensitive and authorization conditions cannot be
confirmed before the window closes, the correct response is to either obtain fast-track
governed authorization through the approval-and-escalation-model or forgo the pull.
An unverified authorization rationalized by timing is not a governed authorization.
Missed data opportunities are recoverable.
Ungoverned spend and ungoverned data imports are governance failures.

---

## Spend Authorization Rule

Spend authorization must be explicit and bounded.

This means:

- a specific spend ceiling must be identified before the pull occurs
- the spend ceiling must cover the specific pull being made, not just
  the general category of pulls
- if the actual cost of the pull is unknown before execution, the actor
  must confirm a ceiling is in place that covers the worst-case cost
- spend authorization does not roll over from a prior pull unless
  explicitly governed as a standing authorization

### Standing Authorization
A standing paid data pull authorization — one that covers recurring pulls
over time — must be explicitly established through a governed approval event.
It must name:

- the vendor or provider class covered
- the pull type covered
- the frequency or volume ceiling
- the spend ceiling per period
- the conditions under which the standing authorization expires or requires renewal

A standing authorization that is silent on any of those dimensions is not
a complete standing authorization for that dimension.

---

## Pull Scope Bounding Rule

Each paid data pull must have a defined scope before execution.

Scope includes at minimum:

- what query, target, or data class is being retrieved
- what vendor or provider is being used
- what volume or record ceiling applies
- what project or planning need the pull serves

Scope must not silently widen after authorization.

Examples of forbidden scope widening:

- authorizing a single domain query and pulling a full competitive set
- authorizing a keyword-level pull and pulling category-level intelligence
- authorizing a one-time pull and initiating a recurring series without
  additional authorization
- authorizing a bounded volume and triggering an unlimited-depth crawl

When a pull would naturally exceed its authorized scope to be useful,
the correct response is to return to the authorization step with the
revised scope — not to proceed and report scope excess afterward.

---

## Source Trust Classification Rule

Before a paid data pull is used for planning, observatory, or operational
purposes, the source must be classified by trust posture.

Trust posture classification must establish at minimum:

- what the vendor provides and how it is produced
- what data quality, freshness, and reliability expectations apply
- what limitations, biases, or coverage gaps are known
- whether the data is suitable for the specific planning or observatory
  use being made of it

### Rule
Paid data that has not been trust-classified must not be treated as clean
evidence in planning or observatory contexts.
The fact that data was paid for does not make it trustworthy.
Source trust is established through classification, not through cost.

---

## Vendor Classification Rule

Vendors used for paid data pulls must be classifiable.

A vendor is classifiable when the ecosystem can establish:

- what data class the vendor provides
- what authorization model the vendor uses
- what spend model applies
- what data quality and freshness commitments the vendor makes

An unclassifiable vendor must not be used for paid data pulls that affect
planning or observatory truth without explicit governance review.

---

## Agent Authorization Prohibition

Agents must not self-authorize paid data pulls.

This applies regardless of:

- how useful the pull appears
- how confident the agent is in the need
- whether a similar pull was previously authorized
- whether the agent believes the operator would approve

When an agent determines that a paid data pull may be warranted, the correct
response is to package a recommendation for human review and wait for explicit
governed approval before proceeding.

The recommendation package should include:

- what data is sought and why
- which vendor or provider would be used
- what the estimated or ceiling cost is
- what planning or observatory need the pull serves
- what the pull scope would be

This package supports human review without substituting for it.

---

## Pull Outcome Reporting Rule

Every paid data pull that occurs must produce a reportable outcome.

The outcome record must preserve at minimum:

- what pull was performed
- which vendor was used
- what the actual scope was
- what was returned or what failure occurred
- what the cost was or is estimated to be
- what governing need the pull served
- what trust posture applies to the returned data

Pull outcomes must not be silently discarded, even when the data is not
immediately useful.
A paid pull that returned nothing useful is still a governance event.

Pull outcome records must be preserved through the governed reporting path defined
in `report-structure-and-required-fields.md`.
A pull outcome that exists only in session context or informal notes is not a governed
outcome record and does not satisfy the reporting requirement.
Where the pull result feeds into VEDA observatory truth, the evidence and source
provenance standards in `../veda/evidence-and-source-provenance.md` also apply
to the ingested data.

---

## Partial and Failed Pull Rule

When a paid data pull partially succeeds, fails, or returns ambiguous data:

- the partial or failed outcome must be preserved explicitly
- the cost of the partial or failed pull must still be reported
- the partial data must not be reported as complete data
- return-to-planning or escalation may be required if the pull failure
  affects a governing planning or observatory need

A failed paid pull is not simply discarded.
It is a governance event with cost and continuity implications.

---

## Forbidden Paid Data Pull Patterns

The following are forbidden:

- pulling paid data without explicit governed approval for the specific pull
- self-authorizing a paid pull because the data seems warranted
- widening pull scope beyond what was authorized without re-authorization
- treating a prior authorization as covering a different pull, vendor, or scope
- concealing the cost or scope of a pull in reporting
- treating paid data as clean evidence without source trust classification
- using a standing authorization to cover pulls outside its explicitly stated scope
- initiating recurring pulls under a one-time authorization
- pulling paid data for exploratory convenience without a tied governing need

---

## Human-In-The-Loop Principle

Paid data pulls are governance-sensitive because they create direct financial
consequences and produce data that may influence planning and observatory truth.

Human review is required before:

- any paid data pull not covered by an explicit standing authorization
- any pull that would exceed a previously authorized spend ceiling
- any pull from a new vendor not previously classified
- any standing authorization is established or renewed
- any pull whose scope has widened beyond the original authorization

An agent expressing that a pull is warranted is a recommendation.
It is not authorization.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- paid data pulls require explicit governed approval before execution
- agent confidence in the need is not authorization
- scope must be bounded before the pull occurs, not after
- paid data is not automatically trustworthy because it was paid for
- every paid pull produces a reportable governance event regardless of outcome
- a prior authorization does not cover a different pull, vendor, or scope

If an LLM treats a useful-seeming data need as sufficient justification
to initiate a paid pull, this doctrine is failing.

---

## Usage

This document should be used:

- when evaluating whether a proposed paid data pull is authorized
- when packaging a recommendation for human review of a proposed pull
- when establishing or reviewing a standing paid data pull authorization
- when classifying a data vendor for paid pull eligibility
- when reviewing whether a pull outcome has been adequately reported
- when deciding whether a pull scope requires re-authorization before expansion

---

## Related Docs

- `external-action-governance.md`
- `approval-and-escalation-model.md`
- `auth-and-actor-model.md`
- `allowed-agent-actions-matrix.md`
- `report-structure-and-required-fields.md`
- `recommendation-packaging-doctrine.md`
- `failure-and-recovery-doctrine.md`
- `../veda/veda.md`
- `../veda/evidence-and-source-provenance.md`
- `../ecosystem/cross-system-boundaries.md`
