# Project V to VEDA Evidence Request Interface

## Purpose

This document defines the interface by which Project V issues a bounded evidence
request to VEDA and receives the response through the existing VEDA → Project V
signal delivery path.

It exists to answer:

```text
How does Project V express a bounded planning-side evidence need to VEDA, what must
a valid evidence request contain, how does VEDA respond, how does the response
return to Project V, and what activity trail records are required for the request
leg of this interaction?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the conditions under which Project V may issue an evidence request to VEDA
- the minimum semantic contents of a valid evidence request
- the access model for the request leg (Project V → VEDA)
- how VEDA responds and which path the response uses
- receipt confirmation requirements on the response
- degraded-mode and recovery behavior on the request leg
- boundary and authority rules
- activity trail requirements for request-leg events

---

## Out of Scope

This document does not define:

- the VEDA → Project V signal delivery leg — that is governed by
  `veda-to-project-v-signal-interface.md`, which is the return path for
  the response to an evidence request
- VEDA internal evidence-gathering, curation, or signal production workflow
- Project V internal intake or planning workflow
- approval class definitions — those belong in
  `../governance/approval-and-escalation-model.md` and
  `../governance/approval-mechanics-seam-model.md`
- transport-layer implementation details or API schemas

---

## System

- interfaces

---

## Core Rule

Project V may issue a bounded evidence request to VEDA when a specific planning-side
evidence need cannot be satisfied by previously delivered signal.

The request is not open-ended observatory access. Project V states a bounded
planning question. VEDA curates a bounded response package. The response returns
through the existing VEDA → Project V push delivery path.

No new return channel is created. Project V does not query VEDA's observatory
records directly. VEDA determines what to include in the response.

**Project V requests. VEDA curates. The response returns through the existing delivery path.**

---

## Architectural Basis

This interface implements AD-03:

> Project V expresses a bounded planning-side evidence need. VEDA curates the
> response. The response returns through the existing VEDA → Project V signal
> delivery path. Project V does not directly query raw VEDA observatory records.

The request leg defined in this document and the response leg defined in
`veda-to-project-v-signal-interface.md` together constitute the full AD-03
request-for-package interaction.

---

## Access Model

**This interface uses Project V-initiated bounded push-request with VEDA-curated
response.**

Project V initiates the request. VEDA receives it, curates a bounded response
package, and delivers the response through the existing
`veda-to-project-v-signal-interface.md` push delivery path.

The request leg and the response leg are distinct and governed by separate documents.
The response package on the delivery leg will carry `delivery_trigger_type: request_response`
and a reference to the originating request identity, linking the two legs in the
activity trail.

### When a request is valid

A Project V evidence request is valid only when:

- a specific planning-side evidence need exists that cannot be satisfied by
  previously delivered signal
- the need is expressible as a bounded planning question rather than a request
  to dump observatory state
- the request is tied to a specific project or bounded planning scope
- the requesting context is a recognized planning workflow stage — most commonly
  Stage 6 of the project intake workflow, but also valid during maintenance,
  replanning, or launch readiness evaluation when a bounded evidence need arises

An evidence request must not be used:

- as a substitute for proactive VEDA signal delivery
- to request arbitrary access to VEDA observatory records
- as a workaround for signal that VEDA has not yet delivered proactively
- to recover from stale signal by requesting a wholesale signal refresh without
  a bounded planning question
- to request signal for a project or scope Project V does not currently have
  planning authority over

---

## Evidence Request Semantics

A valid Project V → VEDA evidence request must be interpretable as carrying at
minimum the following semantic elements.

### Required semantic fields

**Request identity**
A stable identifier for this evidence request. Required for activity trail records,
for VEDA to link the response package to the originating request, and for
de-duplication. Must remain stable across any re-send attempts.

**Planning context reference**
Which project or bounded planning scope this request is tied to. The request must
be scoped to a specific project or a bounded planning question. An unscoped or
cross-project request is not valid.

**Bounded planning question**
The specific planning-side evidence need being expressed. This is not a list of
record identifiers to retrieve. It is a statement of what planning question requires
more evidence to answer honestly. For example: "we need current market signal on
topic X to evaluate whether this intake item meets threshold Y."

VEDA uses this to determine what to curate. Project V must not pre-specify which
VEDA records to retrieve — that is VEDA's curation judgment, not Project V's.

**Requesting workflow stage and context**
The workflow stage or planning context that generated this request. For example:
Stage 6 of the project intake workflow for an intake item that cannot be
honestly evaluated on current signal. This allows the response to be routed
correctly on return and allows the activity trail to connect the request to
its originating planning context.

**Freshness requirement**
The minimum signal freshness Project V requires to make a planning determination.
VEDA uses this to determine whether available evidence is sufficient to respond
or whether new gathering is required. This is not a command to re-gather — it is
information VEDA needs to curate an honest response.

**Urgency posture** (optional but strongly recommended)
Whether this request is blocking a planning decision that has a time constraint,
or whether it can be fulfilled in VEDA's normal curation cycle. This does not
override VEDA's curation judgment but allows VEDA to prioritize appropriately.

### What the request must not contain

A valid evidence request must not contain:

- specific VEDA record identifiers as a retrieval instruction (that would be
  direct observatory access, which is forbidden by the data boundary model)
- planning decisions presented as conclusions that require evidence to justify
  after the fact (evidence is sought to inform decisions, not to validate them)
- requests for signal unrelated to the stated planning question
- requests that span multiple unrelated projects

---

## Response Path

VEDA's response to a valid evidence request is delivered through the existing
VEDA → Project V signal delivery path governed by
`veda-to-project-v-signal-interface.md`.

On that path:

- VEDA curates a bounded response package appropriate to the stated planning need
- the response package carries `delivery_trigger_type: request_response`
- the response package carries the originating request identity
- VEDA initiates the delivery push; Project V confirms receipt
- receipt confirmation requirements and degraded-mode behavior on the delivery
  leg are defined in `veda-to-project-v-signal-interface.md`

This document does not redefine the response leg. On the response leg,
`veda-to-project-v-signal-interface.md` is the governing authority.

### Re-entry on response receipt

When the evidence response is received and confirmed:

- if the originating context is the project intake workflow Stage 6: re-enter
  at Stage 2 (framing) or Stage 3 (interpretation) as appropriate to how much
  framing context remains established, per `workflows/project-intake-workflow.md`
- for other originating workflow contexts: re-enter at the appropriate workflow
  stage per the governing workflow doc for that context

The originating request identity in the response package links the response to
the correct re-entry context.

---

## VEDA's Curation Judgment

VEDA is not obligated to respond to every evidence request in the form requested.

VEDA may:

- respond with a bounded package that partially addresses the planning question
  if full evidence is not available or is below the stated freshness requirement
- indicate in the response package that certain signal is aging or stale rather
  than withholding the package entirely
- decline to respond if the request is outside the bounded request-for-package
  model (e.g., if the request is effectively a request for raw observatory access)

VEDA must not:

- deliver a full observatory state dump in response to a bounded request
- fabricate or assemble signal without provenance to satisfy a request
- deliver a response package that fails the validity conditions in
  `veda-to-project-v-signal-interface.md`

If VEDA cannot respond with an honest, bounded package, it must communicate
that gap rather than delivering a deficient response as if it were complete.

---

## Boundary and Authority Rule

This interface does not change the ownership model.

After a valid evidence request and VEDA's curated response:

- VEDA remains the owner of signal, evidence, and observability truth
- Project V remains the owner of planning and orchestration truth
- Project V may interpret the delivered evidence for planning purposes
- the evidence request does not transfer signal ownership to Project V
- the evidence request does not grant Project V any ongoing access to
  VEDA observatory records beyond what is delivered in the response package

The request is a governed interaction, not an access grant.

---

## What This Interface Does Not Provide

This interface does not provide:

- direct Project V query access to VEDA observatory records
- ongoing or subscription-based signal delivery triggered by the request
- signal that is not bounded to the stated planning question and project scope
- planning decisions or recommendations from VEDA
- VEDA authority over what Project V does with the evidence

---

## Forbidden Interpretations

This interface must not be interpreted as:

- permission for Project V to access VEDA observatory records directly
- permission for VEDA to make planning decisions or recommendations in the response
- permission to use evidence requests as a substitute for proactive VEDA signal delivery
- permission to bypass the signal delivery validity conditions in
  `veda-to-project-v-signal-interface.md` for request-response deliveries
- permission for Project V to accumulate VEDA evidence records beyond
  what is needed for planning-side traceability

---

## Degraded-Mode Behavior

### VEDA unavailable or unresponsive at request time

If VEDA cannot receive the request, Project V must:

- retain the request in a pending state for re-send
- record the request attempt and failure in the activity trail
- not treat the request as fulfilled

VEDA unavailability does not invalidate the planning need. Project V should
surface the gap explicitly in the originating workflow context.

### VEDA cannot produce an honest response

If VEDA determines it cannot produce a bounded, provenance-supported response to
the stated planning question — for example because relevant evidence is fully
expired and cannot be refreshed within a reasonable window — VEDA must communicate
this explicitly rather than delivering a deficient package.

In this case, Project V must handle the evidence gap honestly in the originating
workflow context rather than proceeding on a fabricated or insufficient basis.
Typically this means the intake item, planning evaluation, or other originating
context should take the defer, hold, or escalation path appropriate to an evidence
gap, per the governing workflow doc.

### Response does not return within expected window

If Project V has sent a valid evidence request and no response has been delivered
within a reasonable window:

- Project V must not treat the absence of a response as a negative answer
- Project V must surface the pending request in the originating workflow context
- Project V may re-send the request with the same request identity if the
  planning question remains open and the originating context has not been resolved
  by other means

---

## Recovery Behavior

- Re-sent requests must use the same request identity as the original request
- VEDA must de-duplicate on request identity to avoid producing redundant response packages
- If the originating planning context has been resolved (e.g., the intake item was
  closed or deferred by other means) before the response arrives, Project V must
  handle the late response gracefully without reactivating a resolved context

---

## Activity Trail

Every evidence request event on this interface must produce activity trail records.

**Producing system:** Project V (for request initiation and any re-send)

The following events must each produce a record:

| Event | When it occurs |
|---|---|
| Request initiated | Project V sends the bounded evidence request to VEDA |
| Request send failed | Request could not be delivered to VEDA |
| Request re-sent | Project V re-sends a prior unacknowledged request |

Each request event record must carry, at minimum:

- the request identity
- the project or planning context scope
- the originating workflow stage and context
- the bounded planning question (summary form is sufficient in the record)
- the freshness requirement
- the delivery status at the time of the record

**Action type:** `evidence.request` — canonical in `../ecosystem/activity-trail-model.md`.
The integration map (`../ecosystem/activity-trail-integration-map.md`) Section 7
defines the full mapping for this interface's request-leg events, including the
required entity reference (`entity_type: evidence_request`) and minimum additional
fields (`planning_context_ref`, `originating_workflow_stage`, `bounded_planning_question_summary`,
`freshness_requirement`).

Implementations must use the canonical action type and fields defined in integration
map Section 7. Do not invent alternate action type names for this seam.

**Response leg activity records:**
Activity records for VEDA's response delivery are governed by
`veda-to-project-v-signal-interface.md` and the integration map Section 1.
This document governs only the request leg.

---

## Approval-Sensitive Events

Evidence requests are generally not themselves approval-sensitive events. The act
of issuing a bounded evidence request to inform a planning decision does not
require human review.

However, if the evidence request is issued in the context of a workflow stage that
is already under a governance review gate — for example, an intake evaluation that
has triggered a Class B review requirement — the evidence request and its response
must be handled within that review context. The pending review must not be treated
as resolved on the basis of a prior evidence state if a new response arrives before
the review resolves.

---

## Cost and Accounting Posture

Evidence request processing on VEDA's side incurs evidence curation and potentially
provider data costs. Cost attribution for request-response delivery must be traceable
to the originating request identity on both legs:

- the request leg: cost of issuing the request is attributable to Project V under
  the project scope
- the response leg: evidence curation and delivery cost is attributable to VEDA
  as the producing system, traceable to the request identity per the cost posture
  in `veda-to-project-v-signal-interface.md`

Costs must not be left unattributable to a governed system and project context.

---

## Human-In-The-Loop Principle

Evidence requests are a governed system action that supports human-meaningful
planning decisions. The planning action that may follow from interpreting the
delivered evidence — not the evidence request itself — is what may require human
review.

See the Approval-Sensitive Events section above and the governing workflow docs
for the specific human review conditions that apply at the originating workflow
stage.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- Project V expresses a bounded planning question; VEDA curates the response
- the response returns through the existing VEDA → Project V push delivery path —
  no new channel is created
- the request is not direct observatory access; Project V does not specify which
  records to retrieve
- the request must be tied to a specific project and a real planning-side evidence need
- activity trail records are required for request-leg events; the canonical action
  type is `evidence.request` per integration map Section 7
- VEDA's curation judgment governs the response contents; Project V cannot override it

If the interface is implemented as direct record-level access, as an unbounded
signal subscription, or as a request where the response bypasses the push delivery
path, the doctrine is wrong.

---

## Usage

This document should be used:

- when implementing Project V's evidence request mechanism to VEDA
- when implementing VEDA's evidence request reception and response curation
- when defining what constitutes a bounded planning question for request purposes
- when reviewing whether a proposed evidence request is within the bounded
  request-for-package model
- when wiring Stage 6 of the project intake workflow to the evidence request path
- when confirming the activity trail action type mapping at integration map Section 7

---

## Related Docs

- `veda-to-project-v-signal-interface.md` *(companion response-leg interface — the return path)*
- `../workflows/project-intake-workflow.md`
- `../workflows/maintenance-and-replanning-workflow.md`
- `../ecosystem/activity-trail-model.md`
- `../ecosystem/activity-trail-integration-map.md`
- `../interfaces/data-boundaries.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../project-v/project-v.md`
- `../veda/veda.md`


---
