# Doctrine vs Operational State

## Purpose

This document defines the foundational split between documentation and database in the V Ecosystem.

It exists to answer:

```text
What belongs in docs, what belongs in the database, and why must that split remain explicit so LLMs can operate correctly without confusion about where to find or store information?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the definition of doctrine and operational state
- what kinds of information belong in each
- why the split matters for LLM-assisted operation
- what happens when the split is violated
- how LLMs should orient when starting a session

---

## Out of Scope

This document does not define:

- specific schema design for any system's database
- specific doc structure for any individual doc
- MCP tool design
- API design

Those belong in system-specific, interface, and governance docs.

---

## System

- ecosystem

---

## Core Rule

Docs are the build spec.
The database is operational truth.

These are not interchangeable.
A capable LLM must know which to consult for which kind of question.

---

## What Belongs in Docs

Docs own everything that defines how the ecosystem works, what it is, and what it must be.

Docs own:

- system roles, boundaries, and identity
- invariants and anti-drift rules
- vocabulary and canonical terms
- governance rules and approval posture
- interface contracts and handoff definitions
- workflow steps and lifecycle definitions
- methodology and audit doctrine (BYDA, hammer)
- onboarding requirements for new projects and providers
- architecture decisions (ADRs)
- build specifications — everything an LLM needs to build the ecosystem correctly

Docs are written once and updated deliberately when doctrine changes.
Docs do not change session to session.
Docs are versioned on GitHub.

A doc that contains project-specific current status, live scores, or session history is in the wrong place.

---

## What Belongs in the Database

The database owns everything that reflects the current state of the ecosystem and its projects as they actually exist and change over time.

The database owns:

- current project status and lifecycle phase
- BYDA audit scores and audit run history
- decision log entries for individual projects
- session context — what was worked on, what was decided in a session
- VEDA observatory records — SERP snapshots, GA4 data, Search Console data, keyword targets
- content graph records — pages, topics, entities, internal links
- execution records — what V Forge built, what it reported
- handoff records
- event logs
- approval records
- reporting records

Operational state changes constantly.
It belongs in the database, not in documents.

---

## Why This Split Matters for LLM Operation

Without this split being explicit, LLMs drift in two common failure modes:

### Failure Mode 1 — Looking for current state in docs
An LLM reads a doc hoping to find what phase a project is in, what the current BYDA score is, or what was decided in the last session. That information is not in docs. It is in the database. The LLM must query the database through MCP tools, not infer state from doc content.

### Failure Mode 2 — Writing operational state into docs
An LLM tries to record a project decision, a BYDA result, or a session outcome by updating a markdown file. That is wrong. Operational state belongs in the database where it is queryable, structured, and properly scoped. Docs are not a substitute for a database.

Both failure modes produce incorrect behavior and drift over time.

---

## How an LLM Should Orient at Session Start

When an LLM starts a session in the V Ecosystem it should follow this orientation model:

### What to load from docs
- The relevant doctrine docs for the kind of work being done
- System identity docs for the systems being worked on
- Governance docs relevant to the session's actions
- Interface docs for any cross-system interaction planned

Docs answer: what is this system, what are the rules, what is the right way to build or operate this.

### What to query from the database
- The active project's current phase and status
- Recent BYDA audit results for the active project
- Relevant decision history for the active project
- Session context from prior sessions if available

The database answers: where does this project stand right now, what happened recently, what is the current state.

### The session scope
The active project is set by the human operator in the VSCode extension.
The LLM does not determine project scope. It inherits it through the session token provided by the MCP layer.
All database queries are automatically scoped to the active project.

---

## The Build Spec Principle

The docs are written primarily for an LLM to build the V Ecosystem correctly.

This means every doc should answer at least one of:

- what does this system need to do
- what rules must the code enforce
- what must the database schema support
- what must the API expose or protect
- what must the MCP tools wrap
- what must the hammer verify

If a doc does not affect how the ecosystem gets built or operated, it is likely unnecessary.

The docs are strong enough when: if the code disappeared, a capable LLM could rebuild the V Ecosystem correctly from the docs without relying on hidden tribal knowledge.

---

## The Database Completeness Principle

The database must be complete enough that an LLM can operate a session effectively without asking the human operator to re-explain current project state.

This means the database must capture:

- enough project state that an LLM can answer "where are we with this project" from a query
- enough decision history that an LLM can answer "what did we already decide about this" from a query
- enough session context that an LLM can answer "what was worked on last time" from a query
- enough audit history that an LLM can answer "what is the current BYDA readiness posture" from a query

If the operator has to re-explain current state at the start of every session, the database is not doing its job.

---

## Violation Patterns

The doctrine vs operational state split has been violated when:

- a doc is updated every session to reflect current project status
- a doc contains project-specific BYDA scores, phase indicators, or decision logs
- an LLM creates markdown files to record session outcomes instead of writing to the database
- the database contains doctrine — rules, invariants, vocabulary — that should be in docs
- an LLM reads a doc to determine what phase a project is in instead of querying the database
- session context is stored in conversation history only and not persisted anywhere durable

These are all operational failures with compounding consequences.

---

## Human-In-The-Loop Principle

The operator controls what is worked on by selecting the active project in the extension.
The operator reviews what the LLM produces before it affects doctrine or significant state.
The operator approves governance-sensitive actions before they occur.

The LLM operates within that scope using docs for orientation and the database for current state.
The split keeps those roles clear.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- docs answer "how does this work and what are the rules"
- the database answers "where do things stand right now"
- operational state must never be stored in docs
- doctrine must never be stored in the database
- project scope comes from the session token, not from docs or LLM reasoning
- a session starts by loading docs for orientation and querying the database for current state

If an LLM treats docs as a substitute for database queries or treats the database as a substitute for doctrine, this doc is failing.

---

## Usage

This document should be used:

- as the primary orientation reference for how docs and the database divide responsibility
- when deciding whether a piece of information belongs in a doc or the database
- when reviewing whether an LLM is looking for state in the wrong place
- when building the database schema to ensure it captures all required operational state
- when building MCP tools to ensure they expose the right operational state for LLM consumption

---

## Related Docs

- `v-ecosystem-overview.md`
- `vocabulary.md`
- `db-posture.md`
- `../interfaces/mcp-coordination-model.md`
- `../governance/agent-operating-doctrine.md`
- `../project-v/schema-authority.md`
