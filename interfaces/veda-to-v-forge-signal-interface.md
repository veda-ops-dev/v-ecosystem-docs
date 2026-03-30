# VEDA to V Forge Signal Interface

## Purpose

This document defines the interface by which V Forge consumes bounded observatory signal from VEDA.

It exists to answer:

```text
How does V Forge read VEDA's observatory signal, what signal is available, what are the boundary rules that prevent V Forge from absorbing signal ownership, and how does the consumed signal feed execution intelligence without crossing into observability ownership?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what signal V Forge may consume from VEDA through this interface
- how V Forge accesses that signal
- what V Forge may do with the signal once consumed
- what V Forge must not do with the signal
- boundary rules that preserve VEDA's observatory ownership
- how execution intelligence is produced without creating signal ownership drift

---

## Out of Scope

This document does not define:

- the detailed internal schema of VEDA's observatory tables
- the detailed content graph schema owned by V Forge
- the specific execution intelligence algorithms V Forge uses
- the detailed MCP tool list for this interface
- provider-specific ingest mechanics inside VEDA

Those belong in VEDA-specific, V Forge-specific, and implementation docs.

---

## System

- interfaces

---

## Core Rule

V Forge reads VEDA signal. V Forge does not own VEDA signal.

Reading observatory signal through this interface does not transfer signal ownership to V Forge.
VEDA remains the observatory. V Forge remains the executor.

The signal tells V Forge how external reality is responding to what was built.
V Forge crosses that signal against the content graph it owns to produce execution intelligence.
That cross-referencing happens inside V Forge, using signal V Forge consumed from VEDA.
The raw signal never becomes V Forge's canonical truth.

---

## Why This Interface Exists

V Forge owns the content graph — the structural model of what a project has built.
VEDA owns the observatory signal — how external reality (search, performance, platform behavior) is responding to the project.

Neither system can answer the full execution intelligence question alone.

V Forge asking "how is what we built performing and where are the gaps" requires:
- what was built (content graph — owned by V Forge)
- how it is performing externally (observatory signal — owned by VEDA)

This interface governs the second half of that equation — how VEDA's signal reaches V Forge for execution intelligence purposes without blurring system ownership.

---

## Signal Available Through This Interface

V Forge may consume the following signal classes from VEDA through this interface:

### Search Performance Signal
- SERP position and ranking data for keyword targets associated with the project
- search performance metrics from Google Search Console — impressions, clicks, CTR, position trends
- indexation status and coverage signals from Search Console

### Owned Performance Signal
- traffic and engagement metrics from Google Analytics 4 for the project's properties
- page-level performance trends
- acquisition and channel data relevant to execution planning

### Search Intelligence Signal
- keyword volatility, intent drift, and change classification for tracked keywords
- SERP feature composition changes relevant to content strategy
- domain dominance signals for competitive context

### Observatory Context
- bounded source capture content where relevant to execution intelligence — captured external pages, research material, or reference content ingested through VEDA's source capture surface

### What Is Not Available Through This Interface
- VEDA's internal event log — event logs are VEDA's own audit trail for observatory state changes, not a signal package for consumption by V Forge
- raw provider payloads from other projects — all signal is project-scoped
- planning state from Project V — that comes through the Project V handoff interface
- signal that has not been project-scoped by VEDA

---

## Access Model

V Forge accesses VEDA signal through VEDA's API.

The access model:

```text
V Forge execution intelligence layer
→ MCP tool call (project-scoped session token)
→ VEDA API endpoint (enforces project scope, ownership, and read-only posture)
→ VEDA database (VEDA owns this — V Forge never touches it directly)
→ Response returned to V Forge
```

Rules:

- all access is read-only — V Forge does not write to VEDA's database through this interface
- all access is project-scoped — V Forge can only read signal for the active project
- the VEDA API is the enforcement layer — V Forge cannot bypass it
- V Forge does not have credentials to VEDA's database

---

## What V Forge May Do With Consumed Signal

V Forge may:

- cross the consumed signal against the content graph to identify execution-side gaps
- use the signal to inform execution decisions within approved scope
- preserve the signal as a reference within execution intelligence records
- include signal-derived context in execution reports and findings returned to Project V
- use the signal to determine whether executed work is achieving the intended external effect

---

## What V Forge Must Not Do With Consumed Signal

V Forge must not:

- store consumed VEDA signal as canonical V Forge truth — it remains VEDA-owned signal
- accumulate open-ended signal archives that duplicate VEDA's observatory function
- use signal consumption as justification for taking on signal-system responsibilities
- present consumed signal to Project V as though V Forge were the signal source
- treat signal strength as self-authorization for execution decisions requiring human approval

V Forge reads what VEDA observed.
V Forge does not become the observer.

---

## The Execution Intelligence Boundary

Execution intelligence is the analytical layer that V Forge produces by crossing the content graph against VEDA signal.

This is V Forge's capability, not VEDA's.

Examples of execution intelligence that V Forge owns:

- "our content graph has pages targeting these keywords but SERP data shows we are underperforming on these specific terms — here are the structural gaps"
- "Search Console shows these pages have declining impressions but the content graph shows no changes — possible external signal shift worth investigating"
- "GA4 shows traffic dropping on these content graph nodes — execution intelligence identifies this as a priority for maintenance"

In all cases:
- VEDA owns the raw signal that informed the analysis
- V Forge owns the content graph that provided the structural context
- the execution intelligence output belongs to V Forge as the result of that cross-referencing

VEDA does not produce these outputs.
V Forge produces them by consuming VEDA signal.

---

## Project Isolation Rule

All signal consumed through this interface must be project-scoped.

V Forge's execution intelligence layer must not:

- query VEDA signal for a different project than the active session project
- blend signal from multiple projects into one execution intelligence view
- use cross-project signal to justify execution decisions for the active project

VEDA enforces project scoping at the API level.
V Forge must not attempt to work around project scoping.

---

## Signal Freshness and Trust

Signal consumed from VEDA should be treated according to VEDA's trust classification for that signal class.

V Forge must:

- respect the trust posture established for each signal class
- not present provisional or unverified signal as clean evidence in execution reports
- note when execution intelligence is based on signal with known limitations

V Forge must not:

- assume all VEDA signal is equally trustworthy
- present VEDA signal as V Forge-originated evidence

Signal consumed from VEDA is still VEDA-originated evidence with VEDA's trust posture.

---

## Returning Signal-Informed Findings to Project V

When V Forge's execution intelligence produces findings that require planning reconsideration, those findings return to Project V through the return-to-planning interface.

When findings are signal-informed:

- V Forge should note that the finding is based on VEDA signal consumed at a specific time
- V Forge should preserve the signal source and trust posture in the finding
- V Forge should not present signal-derived conclusions as V Forge-originated observations

The return-to-planning interface is defined in `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`.

---

## Hammer Verification

The hammer verification for this interface must confirm:

- V Forge can read signal for the active project through VEDA's API
- V Forge cannot read signal for a different project (cross-project probe must fail with 404)
- V Forge cannot write to VEDA through this interface
- consumed signal is correctly project-scoped in all cases
- the VEDA API correctly enforces read-only posture for this interface

The cross-project violation probe is required. It must be tested, not assumed.

---

## Failure Behavior

If VEDA signal is unavailable, stale, or returns an error:

- V Forge must not fabricate signal to fill the gap
- V Forge must preserve the signal gap explicitly in execution intelligence outputs
- V Forge must not halt execution entirely unless the missing signal is critical to safe execution within the approved scope
- V Forge may include the signal unavailability as a finding returned to Project V if it materially affects execution quality

Signal absence is honest execution context.
It must be reported, not hidden.

---

## Human-In-The-Loop Principle

Signal consumption through this interface is generally read-only and low-governance-sensitivity.

Human review remains important when:

- execution intelligence based on consumed signal leads to a significant execution change recommendation
- signal indicates a material external change that may require planning reconsideration
- signal quality or trust posture is uncertain and the execution intelligence depends on it heavily

V Forge should surface these conditions explicitly rather than proceeding on uncertain signal without disclosure.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- V Forge reads VEDA signal but does not own it
- consuming VEDA signal does not make V Forge the observer
- execution intelligence is V Forge's analytical output, not a VEDA output
- all signal consumption is read-only and project-scoped
- VEDA's internal event log is not a signal package — it is not available through this interface
- cross-project signal access must fail at the VEDA API level
- signal absence must be reported honestly, not papered over

If an LLM treats VEDA signal consumption as granting V Forge signal ownership or observatory responsibilities, this document is failing.

---

## Usage

This document should be used:

- when building V Forge's execution intelligence layer
- when designing the VEDA API endpoints that V Forge will consume
- when building the MCP tools that expose VEDA signal for V Forge use
- when reviewing whether V Forge is accumulating signal ownership rather than consuming bounded signal
- when building the hammer module for this interface

---

## Related Docs

- `../veda/veda.md`
- `../veda/system-invariants.md`
- `../veda/observability-and-signal-role.md`
- `../v-forge/v-forge.md`
- `../v-forge/system-invariants.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/mcp-coordination-model.md`
- `../ecosystem/cross-system-boundaries.md`
- `../governance/testing-and-verification-doctrine.md`
