# VEDA to Project V Signal Interface

## Purpose

This document defines the interface by which VEDA delivers bounded signal and
evidence packages to Project V for planning use.

It exists to answer:

```text
How does VEDA deliver planning-relevant signal to Project V, what must a valid
delivery package carry, what triggers delivery, how is receipt confirmed, and
what happens when delivery fails or signal is stale?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the access model for VEDA → Project V signal delivery
- what triggers delivery (proactive vs request-response)
- the minimum semantic contents of a valid signal delivery package
- receipt confirmation requirements
- degraded-mode and recovery behavior
- boundary and authority rules after delivery
- activity trail requirements for delivery events
- cost and accountability posture

---

## Out of Scope

This document does not define:

- VEDA internal evidence-gathering or signal production workflow
- Project V internal planning workflow
- detailed source trust policy
- full approval policy — that belongs in `../governance/approval-and-escalation-model.md`
  and `../governance/approval-mechanics-seam-model.md`
- the Project V → VEDA evidence request leg — that is a separate interface
  (see `project-v-to-veda-evidence-request-interface.md`)
- transport-layer implementation details or API schemas

Those belong in VEDA docs, Project V docs, governance docs, workflow docs, and
implementation-specific docs.

---

## System

- interfaces

---

## Core Rule

VEDA delivers bounded planning-relevant signal packages to Project V through this
interface. Delivery is VEDA-initiated and requires Project V receipt confirmation.

A delivered signal package does not transfer planning ownership to VEDA.
A delivered signal package does not transfer signal-system ownership to Project V.
Receipt of signal is not the same as a planning decision.

---

## Access Model

**This interface uses VEDA-initiated push delivery with receipt confirmation.**

VEDA initiates every delivery on this interface. Project V does not poll or query
this interface directly. Delivery is not complete until Project V confirms receipt.

This model reflects that VEDA is the signal-system owner and is in the best position
to determine when planning-relevant signal has been produced and is ready for
delivery. Project V cannot know independently when VEDA has relevant signal to provide.

### Delivery triggers

Delivery on this interface may be triggered by two distinct causes:

**Trigger 1 — VEDA-proactive delivery**
VEDA determines that planning-relevant signal has been produced and delivers it to
Project V without a prior request. This is the default delivery mode. VEDA curates
what is planning-relevant and initiates delivery when signal quality and freshness
support an honest transfer.

**Trigger 2 — Request-response delivery**
Project V has sent a bounded evidence request through the evidence request interface
(`project-v-to-veda-evidence-request-interface.md`). VEDA has curated a response
package and now delivers it to Project V through this interface. The delivery
mechanics on this interface are the same as Trigger 1; what differs is the
initiation context and the activity trail record (see Activity Trail section).

The return delivery leg is this interface in both cases. The request leg is a
separate interface and is not defined here.

---

## Signal Retention Principle

Not all signal or evidence collected by VEDA should be transferred to Project V.

Signal transfer to Project V is warranted when the signal:

- affects what planning should consider
- affects project creation, prioritization, or readiness
- affects whether an existing plan remains valid
- affects whether a handoff should be prepared, revised, delayed, or withheld
- affects what Project V should reconsider at a planning level

Signal that does not affect planning, prioritization, readiness, project creation,
handoff readiness, or planning reconsideration should remain inside VEDA's
observability and evidence domain.

VEDA is responsible for applying the Signal Retention Principle before initiating
delivery. A delivery that crosses the full VEDA observability state is not a valid
signal transfer.

---

## Delivery Package Semantics

A valid VEDA → Project V signal delivery package must be interpretable as carrying
at minimum the following semantic elements.

### Required semantic fields

**Planning context reference**
Which project or planning scope this package is relevant to. The package must be
scoped to a specific project or a bounded planning question rather than being
a generic ecosystem-wide dump.

**Signal/evidence scope**
What class or domain of signal this package represents — e.g., market signal,
search performance signal, competitive signal, source-capture evidence. This
allows Project V to classify what kind of planning input it is receiving.

**Package / delivery identity**
A stable identifier for this delivery event. Required for activity trail records,
receipt confirmation, and de-duplication. Must remain stable between initial
delivery and any re-delivery attempt.

**Observation or capture timestamps**
When the underlying evidence or signal was gathered or observed. This is distinct
from the delivery timestamp. Both must be present so Project V can assess whether
the signal reflects conditions close enough to the current planning moment to be
usable.

**Delivery timestamp**
When VEDA initiated this delivery.

**Freshness classification**
VEDA's assessment of whether the contained signal is fresh, aging, stale, or
of uncertain freshness. Project V must not assume all delivered signal is equally
current. VEDA must not deliver signal it knows to be expired without flagging
the freshness state.

**Trust and provenance metadata**
The source or provider origin of the evidence, the trust classification VEDA
applies to this signal class, and any known limitations or uncertainty. Project V
must preserve this provenance context when using the signal in planning records.
Evidence whose provenance cannot be established must be flagged rather than
silently treated as clean.

**Planning concern or question addressed**
A bounded statement of what planning concern, question, or condition this package
speaks to. This is VEDA's curation rationale — it is not a planning decision.
VEDA states what the signal is relevant to; Project V determines what to do with it.

**Bounded evidence references or included evidence elements**
The actual signal content — the bounded evidence, observations, or findings that
constitute the package. Where signal is inferred rather than directly observed,
the inference basis must be included.

**Delivery trigger context** (when Trigger 2 applies)
If this delivery is a response to a prior Project V evidence request, the package
must carry a reference to the originating request identity. This allows activity
trail records to connect the request and response, and allows Project V to route
the package to the correct intake re-entry point.

### What the package must not contain

A signal delivery package must not contain:

- VEDA's full internal observability state
- planning decisions or recommendations presented as conclusions
- execution instructions
- fabricated or uncorroborated signal presented without provenance
- signal from a different project scope than the delivery is scoped to

---

## Delivery Trigger Distinction

Proactive delivery and request-response delivery use the same delivery interface
and the same package requirements. The distinctions between the two cases are:

| Dimension | Proactive | Request-response |
|---|---|---|
| Initiation | VEDA determines signal is planning-relevant | Project V has sent an evidence request; VEDA is responding |
| Request reference | Not present | Present — package carries originating request identity |
| Activity trail trigger type | `proactive` | `request_response` |
| Package contents | VEDA-curated planning-relevant signal | VEDA-curated response to the stated planning need |
| Routing in Project V | Normal intake | Tied to the specific intake or evaluation context that generated the request |

Both cases require receipt confirmation. Both cases produce activity trail records.
The trigger type field in the activity trail distinguishes them.

---

## Receipt Confirmation

Delivery is not complete until Project V confirms receipt.

**What receipt confirmation means:**
Project V acknowledges that the delivery package has arrived and is available for
planning interpretation. Receipt confirmation does not mean Project V has interpreted
the signal or made any planning decision based on it.

**What VEDA must do if receipt confirmation is not returned:**
VEDA must not treat the delivery as complete. VEDA must retain the delivery package
for re-delivery. VEDA may attempt re-delivery after an appropriate wait interval.
VEDA must not generate a new package to replace an unconfirmed delivery as if the
prior delivery never happened — the package identity must remain stable across
re-delivery attempts.

**What Project V must not assume:**
Project V must not assume that a delivery it has not confirmed has not occurred.
If Project V receives a delivery it has already confirmed (e.g., duplicate delivery
due to retry), it must handle the duplicate gracefully using the package identity.

---

## Signal Transfer Validity Conditions

A signal delivery is valid only when:

- VEDA has produced bounded signal or evidence outputs relevant to planning
- the delivery is limited to planning-relevant signal rather than open-ended
  observability state
- the minimum package semantic fields defined above are present
- the freshness and provenance metadata are present and honest

Signal with significant source-trust concerns or high provenance uncertainty must
not be delivered without clearly flagging that uncertainty in the package.

A delivery that does not meet these conditions must not be treated as a valid signal
transfer by Project V.

---

## Boundary and Authority Rule

After a valid signal delivery and receipt confirmation:

- VEDA remains the owner of signal, evidence, and observability truth
- Project V remains the owner of planning and orchestration truth
- Project V may interpret the delivered signal for planning purposes
- V Forge remains the owner of execution truth

No signal delivery changes the owner of those truth domains.

**VEDA curates and delivers. Project V interprets.**

The planning concern field in the package represents VEDA's signal curation
rationale — it is not a planning instruction, and it does not constrain how
Project V may interpret the signal. VEDA does not make planning decisions.
Project V is responsible for determining what the signal means for planning.

Receiving a signal delivery does not validate the signal for planning action.
Project V must interpret the signal appropriately, accounting for freshness and
provenance metadata, before acting on it.

---

## What a Signal Delivery Does Not Provide

A signal delivery does not provide:

- planning truth
- orchestration truth
- readiness truth as a decision already made
- handoff truth
- execution truth
- permission for VEDA to define what Project V must do next
- full observability state as a planning payload
- planning-validated signal (Project V must perform its own interpretation)

---

## Forbidden Interpretations

A signal delivery must not be interpreted as:

- permission for VEDA to define planning decisions directly
- permission for Project V to absorb VEDA's signal-system role
- permission to treat delivered signal as already-approved planning action
- permission to collapse the distinction between evidence, recommendation, and decision
- permission for Project V to treat all observability state as planning payload
- permission for Project V to treat delivered signal as validated planning-ready
  truth without independent interpretation

---

## Degraded-Mode Behavior

### Project V unavailable at delivery time

If Project V cannot receive the delivery — because it is unavailable or the delivery
cannot be completed — VEDA must:

- not treat the delivery as confirmed
- retain the package for re-delivery
- record the delivery attempt and failure in the activity trail
- not discard the package identity

Project V must not assume delivery has occurred if it has not confirmed receipt.

### Receipt confirmation not returned within expected window

If VEDA has initiated delivery but receipt confirmation has not been returned within
a reasonable window, VEDA must treat delivery as incomplete and follow the same
behavior as "Project V unavailable at delivery time" above.

### Stale signal package

If a delivery package has become materially stale before delivery is confirmed —
because VEDA's underlying observatory records have changed significantly since the
package was produced — VEDA must assess whether the package can still honestly
represent the signal it was curated to represent.

If the staleness is material:
- VEDA should produce an updated package rather than delivering stale content as
  though it is current
- The updated package carries a new delivery identity but may reference the same
  planning concern
- VEDA must not deliver a package it knows to be materially stale without flagging
  the freshness classification appropriately

If the staleness is within the expected freshness window for the signal class,
re-delivery of the original package with the original delivery identity is acceptable.

### Partial package or invalid provenance

If a delivery package cannot be completed because a required semantic field is
absent or provenance for included evidence cannot be established:

- VEDA must not deliver an incomplete or provenance-anonymous package as if it
  were a valid signal transfer
- VEDA must either complete the package or surface the gap explicitly rather than
  proceeding with a deficient package
- Project V must not treat a package missing required fields as a valid signal delivery

---

## Recovery Behavior

After degraded mode clears or a delivery failure is resolved:

- VEDA may re-deliver the same package using the same delivery identity
- VEDA must not silently assume that a prior failed delivery subsequently completed
  without confirmed receipt
- Project V must handle re-delivery gracefully: if the package identity has already
  been confirmed, the re-delivery is a duplicate and should be handled without
  re-processing the same signal as if it were new
- recovery re-delivery does not require generating a new evidence request from
  Project V — VEDA holds the package and re-delivers when the channel is available

---

## Activity Trail

Every signal delivery event on this interface must produce activity trail records.

**Producing system:** VEDA
**Target system:** Project V

The following events must each produce a record:

| Event | When it occurs |
|---|---|
| Delivery initiated | VEDA initiates the push delivery |
| Receipt confirmed | Project V confirms receipt |
| Delivery failed / unconfirmed | Delivery attempt produced no confirmation after the expected window |
| Re-delivery initiated | VEDA re-delivers a package previously unconfirmed |

Each delivery event record must carry, at minimum:

- the package / delivery identity
- the project or planning context scope
- the delivery trigger type: `proactive` or `request_response`
- if `request_response`: the originating evidence request identity
- the freshness classification of the delivered signal
- the trust / provenance classification where applicable
- the receipt confirmation status at the time of the record

The exact canonical action type names for these events must align with the
activity trail model (`../ecosystem/activity-trail-model.md`) and the activity
trail integration map (`../ecosystem/activity-trail-integration-map.md`). The
mapping for this interface is defined in integration map Section 1.

Deliveries that produce no activity trail records are not governed deliveries.

---

## Approval-Sensitive Events

Signal deliveries that influence high-impact planning decisions may require human
review or approval before planning action proceeds.

Conditions that may require human review include:

- strategic importance of the signal
- uncertainty or source-trust concerns
- external paid data implications
- project creation implications
- reprioritization or launch sensitivity

The approval class and seam-level mechanics for these review events are governed by
`../governance/approval-and-escalation-model.md` and
`../governance/approval-mechanics-seam-model.md`.

This interface does not redefine approval mechanics. Signal delivery itself is not
an approval event. Human review, when required, applies to the planning action that
would follow from interpreting the delivered signal.

---

## Cost and Accounting Posture

Signal delivery is a governed system activity. The costs associated with producing
and delivering a signal package — including evidence preparation, provider data
costs, and delivery infrastructure — are attributable to VEDA as the producing
system.

Cost attribution must be:

- reviewable after the fact
- associated with the delivery identity and project scope
- captured in the activity trail where applicable

Project V does not bear production costs for VEDA-initiated proactive delivery.
For request-response delivery triggered by a Project V evidence request, cost
attribution between the request leg and the delivery leg must be traceable to
the originating request identity.

Costs must not be left unattributable to a governed system and project context.

---

## Allowed Use of Delivered Signal by Project V

Project V may use signal delivery inputs to:

- reconsider planning assumptions
- create or reject potential projects
- reconsider prioritization or readiness
- determine whether further bounded evidence is needed through the governed
  evidence request path
- determine whether planning, reprioritization, or handoff preparation should change

---

## Human-In-The-Loop Principle

A signal delivery can influence high-impact planning decisions. See the
Approval-Sensitive Events section above for when human review may be required.

Human review applies to planning decisions informed by the signal, not to
the delivery event itself. VEDA's delivery is a governed system action;
the planning consequences belong to Project V under appropriate governance.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- VEDA initiates signal delivery; Project V does not poll this interface
- delivery is not complete until Project V confirms receipt
- delivery may be proactive or a response to a Project V evidence request
- the package must carry freshness, provenance, and trust metadata — Project V
  must not assume all delivered signal is equally current or trustworthy
- VEDA curates what to deliver; Project V determines what to do with it
- receipt of signal is not a planning decision
- activity trail records are required for every delivery event

If the interface is implemented as an unbounded observability dump, as automatic
planning instruction, or as a delivery that needs no confirmation, the doctrine
is wrong.

---

## Usage

This document should be used:

- when implementing VEDA's signal delivery to Project V
- when implementing Project V's signal delivery reception and confirmation
- when defining planning-relevant signal packages or deliveries
- when reviewing whether a proposed signal delivery is too broad or too weak
- when writing VEDA and Project V workflow docs that involve signal-to-planning flow
- when evaluating whether a signal delivery event should produce an activity trail record

---

## Related Docs

- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/cross-system-access-governance.md`
- `../ecosystem/activity-trail-model.md`
- `../ecosystem/vocabulary.md`
- `../project-v/project-v.md`
- `../veda/veda.md`
- `project-v-to-veda-evidence-request-interface.md` *(companion request-leg interface)*
- `project-v-to-v-forge-handoff-interface.md`
- `../workflows/project-intake-workflow.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`
- `../governance/evidence-continuity-model.md`
- `../ecosystem/external-provider-integration-doctrine.md`
