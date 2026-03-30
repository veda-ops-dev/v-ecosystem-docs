# External Provider Integration Doctrine

## Purpose

This document defines how external data providers are integrated into the V Ecosystem.

It exists to answer:

```text
When a new external data provider needs to be added to any system in the V Ecosystem, what must be true before integration begins, how must the integration be structured, what governance applies, and how is it documented so a capable LLM can build it correctly?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what an external data provider is in the context of the V Ecosystem
- which system may own a given provider integration
- the required integration structure every provider must follow
- credential and authentication posture
- ingest path requirements
- trust classification of provider data
- paid usage governance
- hammer verification requirements
- documentation requirements for each integration

---

## Out of Scope

This document does not define:

- provider-specific API mechanics or endpoint details
- provider-specific schema design
- individual credential values or secrets
- UI or operator-surface design for specific providers
- the full list of currently approved providers

Those belong in provider-specific docs, implementation docs, or secrets management.

---

## System

- ecosystem

---

## Core Rule

Adding a new external data provider is a governed architecture event, not a casual implementation choice.

A provider must not be integrated merely because:

- it looks useful
- it is easy to call
- another project uses it
- an LLM suggests it would help

Integration must follow this doctrine completely.
Partial integration that skips classification, documentation, or governance is not a valid integration.

---

## What an External Data Provider Is

An external data provider is any external service, API, platform, or data source that:

- supplies data or content to a V Ecosystem system through an API call, SDK, or automated fetch
- exists outside the V Ecosystem's internal boundary
- may involve authentication, credentials, rate limits, or cost

Examples include but are not limited to:

- SERP data APIs
- web scraping and crawling services
- search performance APIs (GA4, Search Console)
- social and video platform APIs (YouTube)
- market intelligence or competitive data services
- link and citation data services
- content intelligence platforms
- any paid or unpaid external API that supplies data to the ecosystem

---

## System Ownership Rule

Every external provider integration must be owned by exactly one system.

The owning system is determined by what the provider supplies and how it is used:

### VEDA owns providers that supply observatory inputs
If the provider supplies data that VEDA observes and records as external reality — search data, performance data, platform signals, crawled external content — the integration belongs to VEDA.

VEDA is the primary owner of external data provider integrations in the V Ecosystem because VEDA is the pure observatory. Most external data enters the ecosystem through VEDA.

### V Forge owns providers that supply execution tooling
If the provider supplies tools or services that V Forge uses during execution — publishing APIs, CMS integrations, deployment services, content delivery tools — the integration belongs to V Forge.

### Project V owns providers that supply planning-support data
If the provider supplies data used exclusively in planning and never enters the observatory — market sizing tools, research databases used only during intake — the integration belongs to Project V.

### Rule
A provider must not be integrated into multiple systems without explicit justification and governed interface documentation for how data crosses system boundaries.
If a provider supplies data that one system ingests and another consumes, the ingesting system owns the raw data and the consuming system accesses it through a governed interface.

---

## Required Integration Structure

Every external provider integration must implement all of the following before it is considered complete.

### 1. Provider Classification Document
A doc that answers:
- what does this provider supply
- which system owns the integration
- what data class does it produce (observatory signal, execution tooling, planning support)
- what is the provider's data quality and freshness model
- what are the known limitations, biases, or coverage gaps
- is the provider paid or free
- what is the authentication model
- what is the rate limit and volume model

This doc lives in the owning system's docs folder.
Example location: `veda/providers/[provider-name].md`

### 2. Credential Posture
Credentials must:
- be stored in environment variables or a secrets management system — never hardcoded
- be scoped to the minimum access required
- use a consistent naming pattern that identifies the provider and key purpose — document the key name in the provider classification doc, never the value
- be rotatable without requiring code changes

### 3. API Client Layer
Each provider must have a dedicated API client module.

The client must:
- be the single point of entry for all calls to that provider
- handle authentication internally — callers must not manage credentials directly
- handle rate limiting and retry behavior
- return normalized responses in a stable internal shape
- never be called directly from business logic — it must be called through the ingest layer

The client is thin. It is a transport layer, not a business logic layer.

### 4. Ingest Layer
The ingest layer sits between the API client and the database.

The ingest layer must:
- validate provider responses before persistence
- normalize data into the owning system's schema
- enforce project scoping — all ingested records must be scoped to a project
- enforce idempotency — safe replay must not create duplicates
- emit canonical event log entries where required
- handle partial and failed ingestion explicitly — partial data must not be persisted as complete data
- record the source and capture time on every persisted record

Ingest must not bypass validation.
Ingest must not write directly to the database without going through the defined ingest path.

### 5. Database Schema
Provider data must persist in explicit, well-defined tables.

Schema requirements:
- every table that stores provider data must include a `projectId` foreign key (unless explicitly global)
- capture time (`capturedAt`) must be a first-class field on observation records
- raw provider payloads may be stored as JSON for evidence but hot query fields must be promoted to explicit columns
- uniqueness constraints must reflect real ownership scope

### 6. Trust Classification
Before provider data is used for planning, observatory, or execution purposes, the source must be classified:

- **Trusted** — data quality, freshness, and reliability are well understood and meet the ecosystem's requirements
- **Provisional** — data is usable but has known limitations that downstream consumers must account for
- **Unverified** — data has not been fully evaluated and must not be treated as clean evidence

Trust classification must be documented in the provider classification doc.
Provider data must not be presented to downstream systems as clean evidence until a trust classification has been established.

### 7. Hammer Verification
Every provider integration must have a hammer verification module.

The hammer must verify:
- the API client correctly authenticates and returns valid responses
- the ingest layer correctly validates and normalizes responses
- project isolation is enforced — data from one project cannot be accessed by another
- idempotency holds — safe replay does not create duplicates or emit false events
- partial and failed ingestion behaves correctly
- schema assumptions hold under real execution

The hammer is part of the integration. It is not optional.

### 8. Documentation
Every integration requires:
- the provider classification doc (described above)
- inline comments in the API client and ingest layer explaining non-obvious behavior
- an entry in the owning system's provider registry (see below)

---

## Provider Registry

Each system that owns provider integrations must maintain a provider registry.

The registry is a simple table in a doc that lists:

| Provider | Data class | Status | Paid | Trust level | Owner doc |
|---|---|---|---|---|---|
| Example Provider | SERP data | Active | Yes | Trusted | `providers/example-provider.md` |

The registry gives any LLM or operator a fast view of what providers exist and their current status.

Registry location: `[system]/providers/registry.md`

---

## Paid Provider Governance

If a provider charges per call, per record, per volume, or consumes a billable quota, it is a paid provider and the paid data pull governance rules apply in full.

Key requirements:
- paid providers must be explicitly authorized before the integration is built
- spend must be bounded before any calls are made
- agents must not self-authorize paid provider calls
- every paid call must produce a reportable outcome
- the provider classification doc must document the spend model clearly

The full paid data pull governance rules are defined in `../governance/paid-data-pull-governance.md`.

---

## Adding a New Provider — Required Steps

When a new external provider needs to be integrated, these steps must be completed in order:

### Step 1 — Classify the provider
Determine which system owns the integration.
Document the provider's data class, trust posture, authentication model, and spend model.
If paid, obtain explicit authorization before proceeding.

### Step 2 — Write the provider classification doc
Create the provider classification doc in the owning system's providers folder.
Get the trust classification established before any data is used downstream.

### Step 3 — Build the API client
Create the dedicated API client module.
Credentials must come from environment variables only.

### Step 4 — Build the ingest layer
Create the ingest layer with validation, normalization, project scoping, idempotency, and event logging.

### Step 5 — Define the database schema
Add the required tables with proper project scoping, capture time fields, and uniqueness constraints.

### Step 6 — Write the hammer module
Create the hammer verification module for this provider.
Run it against a test environment before the integration goes to production.

### Step 7 — Update the provider registry
Add the provider to the owning system's provider registry.
The provider registry is the durable record of what providers exist and their current status.

### Step 8 — Record as an ADR if the integration crosses ecosystem boundaries
If the new provider affects how systems interact, what data crosses system boundaries, or what trust posture applies ecosystem-wide, record the decision in `ecosystem/decisions/` as an ADR.
If the integration is purely internal to one system with no cross-system consequences, the provider registry entry and classification doc are sufficient — no ADR is required.

---

## Removing or Deprecating a Provider

When a provider is no longer needed:

- mark it as deprecated in the provider registry
- do not delete historical data without explicit governance approval
- remove the API client and ingest layer from active code paths
- preserve the provider classification doc in the owning system's archive
- record the deprecation decision as an ADR if it affects downstream systems

Silent removal of a provider that other systems depend on is a governance failure.

---

## Anti-Patterns

The following are forbidden:

- calling a provider API directly from business logic without an API client layer
- persisting provider data without going through the ingest layer
- storing provider data without project scoping
- using provider data downstream without trust classification
- adding a provider without a hammer module
- adding a paid provider without explicit authorization
- using one provider's credentials for a different provider
- treating a provider integration as an internal implementation detail that does not require documentation

---

## Human-In-The-Loop Principle

Adding a new external provider is a governed event because:

- it expands the ecosystem's external surface
- it may introduce cost
- it introduces data of unknown trust quality until classified
- it requires schema changes that must not break existing integrations

Human review is required before:

- any paid provider is added
- any provider that supplies data used in planning decisions is added
- any provider whose trust posture is uncertain is added

An LLM may build the integration.
A human must authorize the addition of the provider.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- adding a provider requires classification, a client layer, an ingest layer, schema, hammer verification, and documentation
- provider data is not trustworthy until explicitly classified
- paid providers require explicit human authorization before the integration is built
- the API client is thin — it is transport only
- the ingest layer owns all validation, normalization, and project scoping
- every integration must have a hammer module
- the provider registry is the durable operational record — not a session doc or execution plan entry

If an LLM treats adding a new API as a casual implementation task requiring only a fetch call and a database write, this doctrine is failing.

---

## Usage

This document should be used:

- when any new external data provider needs to be added to any V Ecosystem system
- when reviewing whether an existing integration follows the required structure
- when deciding which system should own a new provider integration
- when building the hammer module for a provider integration
- as the primary reference for LLM-assisted provider integration work

---

## Related Docs

- `vocabulary.md`
- `doctrine-vs-operational-state.md`
- `../governance/paid-data-pull-governance.md`
- `../governance/external-action-governance.md`
- `../governance/testing-and-verification-doctrine.md`
- `../veda/veda.md`
- `../veda/evidence-and-source-provenance.md`
- `../ecosystem/db-posture.md`
