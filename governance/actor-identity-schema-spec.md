# Actor Identity Schema Spec

## Purpose

This document formalizes the schema-facing identity contract for actor fields
used by the ecosystem activity trail, approval-related records, and downstream
system schema authority docs.

It exists to answer:

```text
For each canonical actor type, what kind of thing is actor_id, what is the
complete canonical value set for actor_type and actor_system, how must External
Actor be handled at the schema layer, and how must approving actors be referenced
in approval records so that governance is reviewable and queryable after the fact?
```

This is a Tier 1 governance schema companion document.

---

## Scope

This document governs:

- the canonical schema-facing `actor_type` value set and its finalization
- the canonical schema-facing `actor_system` value set
- the `actor_id` value-class contract per `actor_type`
- the schema-facing scope decision for External Actor
- how actor identity must be referenced in approval records
- how actor identity must be treated in activity trail records
- anti-drift rules for actor identity at the schema layer

---

## Out of Scope

This document does not define:

- implementation-specific authentication mechanisms or flows
- vendor-specific identity provider configuration
- OAuth, OIDC, SAML, or token schema design
- email address or username format rules
- detailed database ACL or permission system design
- session token or credential handling
- project-specific actor variations beyond what the canonical classes cover

Those belong in implementation, infrastructure, and project-specific docs.
This document establishes the value-class contract — what kind of thing an
identifier must be — not how that identifier is issued, stored, or verified.

---

## System

- governance

---

## Relationship to Existing Authority Docs

This document extends `governance/auth-and-actor-model.md` into schema-facing
identity value-space rules. `auth-and-actor-model.md` establishes actor classes,
the identity principle, the attribution principle, and the minimum actor semantics.
This document translates those into the concrete `actor_type` enumeration, the
`actor_id` value-class contract per type, and the External Actor scope decision
that the schema layer requires.

This document formalizes the actor fields already defined by name in
`ecosystem/activity-trail-model.md` (`actor_type`, `actor_id`, `actor_system`)
and referenced as a pending artifact in `ecosystem/ecosystem-schema-spine.md`.
The ecosystem schema spine defers `actor_id` value-class precision to this
document; that deferral is now resolved here.

This document supports downstream schema authority docs
(`project-v/project-v-schema-authority.md`, `veda/veda-schema-authority.md`,
`v-forge/v-forge-schema-authority.md`) by providing the identity contract that
approval records and activity trail records will reference.

This document does not replace `governance/auth-and-actor-model.md`. It does not
redesign authentication architecture or introduce new governance classes. Every
value and rule here is derivable from the current merged baseline.

---

## Core Rule

Actor identity in the V Ecosystem must be classifiable, attributable, stable,
and queryable.

Every governed action in the activity trail must carry an `actor_type` from the
canonical enumeration, an `actor_id` that is a stable durable reference within
the value class defined for that type, and an `actor_system` from the canonical
enumeration.

Free-text labels, session-local tokens, claimed roles, and anonymous identifiers
are not valid actor identity for governed records.

---

## Actor Type Value Set

The canonical schema-facing `actor_type` enumeration is:

| Value | Doctrine class | Description |
|---|---|---|
| `agent` | Agent | An LLM-driven or software-driven actor assisting with governed work |
| `operator` | Human Operator | A human participant with review, direction, or approval responsibilities |
| `system` | System Process | A non-agent automated process operating within a bounded system function |

**This is the complete canonical enumeration.** No other values are valid for
`actor_type` in activity trail records or approval records on the current merged
baseline.

The `System Process` doctrine class in `governance/auth-and-actor-model.md`
maps to the `system` value. The `Human Operator` doctrine class maps to the
`operator` value. The `Agent` doctrine class maps to the `agent` value.

See the External Actor Scope Decision section below for the explicit scope ruling
on the fourth doctrine class.

---

## Actor System Value Set

The canonical schema-facing `actor_system` enumeration is:

| Value | Description |
|---|---|
| `project_v` | The Project V planning and orchestration system |
| `veda` | The VEDA observatory and signal system |
| `v_forge` | The V Forge execution system |
| `ecosystem` | Ecosystem-level processes not owned by a single system |
| `extension` | Governed extensions or integrations operating under an explicit ecosystem authority grant |

**This is the complete canonical enumeration.** No other values are valid for
`actor_system` on the current merged baseline.

This value set is unchanged from the existing canon in
`ecosystem/activity-trail-model.md` and `ecosystem/ecosystem-schema-spine.md`.
It is restated here for completeness and to confirm that no expansion is required
at this time.

---

## Actor ID Value-Class Contract

The `actor_id` field must carry a stable, durable reference to the acting entity.
The required value class differs by `actor_type`. The following defines what kind
of thing `actor_id` must be for each type.

This is a value-class contract, not a format specification. It defines the
durability and queryability requirements for the identifier, not the character
encoding, length, or database type. Implementation-specific format decisions
(UUID vs. numeric ID vs. slug) are left to the implementing system provided
the value-class requirements below are satisfied.

---

### `actor_type: operator`

**Value class:** A stable user record identifier assigned to the human operator
by the ecosystem's identity management layer and persisted in the operator's
user record.

**Requirements:**

- Must be assigned to a specific, identifiable human account — not to a session,
  a browser instance, or an ephemeral token.
- Must be stable across sessions: the same human operator must carry the same
  `actor_id` in activity records across separate sessions and separate days.
- Must be resolvable: given the `actor_id`, it must be possible to retrieve the
  corresponding operator record from the identity management layer.
- Must not be an email address, username, or display name used as the primary
  identifier. Those may appear as secondary attributes of the operator record;
  the `actor_id` must be the stable record identifier, not a mutable display
  attribute.
- Must not be a session token, an auth credential, or a one-time value.

**Schema implication:** Approval records that reference an approving human
operator must carry this stable user record identifier as the `actor_id` value.
Approval records where `actor_type: operator` and `actor_id` is a free-text name
or session-local label are not valid governed approval records.

---

### `actor_type: agent`

**Value class:** A stable governed agent identifier that identifies either the
agent type or a specific agent instance at the level required for governance
replay.

**Requirements:**

- Must identify the agent at the level needed to attribute the action in later
  review. At minimum, the agent type or agent role must be attributable from the
  `actor_id` value.
- Where a specific agent instance is relevant to governance replay (e.g., for
  auditing which agent session produced a specific approval request or execution
  event), the `actor_id` must identify that instance, not only the agent type.
- Must be stable within the scope of a governed session or execution context.
  An agent that operates across multiple sessions may carry a stable agent-type
  identifier common across sessions, plus a session-scoped identifier in
  `ecosystem_session_id`. The `actor_id` must not change mid-session.
- Must not be a prompt-claimed role label. A value like `"planning_agent"` is
  only a valid `actor_id` if it is an assigned, governed identifier — not a
  self-asserted label from prompt content. See Anti-Drift Rules below.
- Must not be a bare LLM session hash or inference ID unless that hash is
  explicitly governed as the stable agent identifier for that context.

**Schema implication:** Activity trail records produced by agents must carry an
`actor_id` that is governable — traceable back to a specific governed agent role
or instance. Records where `actor_id` is an anonymous string, an inference ID
with no governed meaning, or a self-asserted prompt label are insufficient for
governance replay.

---

### `actor_type: system`

**Value class:** A stable system process identifier assigned to the automated
process by the system that owns it.

**Requirements:**

- Must identify the specific system process or service — not a generic label for
  the entire system. Where a system runs multiple distinct automated processes
  (e.g., scheduled reporting, workflow handler, ingest pipeline), the `actor_id`
  must distinguish between them.
- Must be stable: the same process must carry the same `actor_id` across
  invocations within its defined operating scope.
- Must be resolvable: given the `actor_id`, it must be possible to identify what
  system process produced the record and under what bounded function it was
  operating.
- Must not be a generic system name alone (e.g., `"veda"` is not a valid
  `actor_id` for a `system` actor — `"veda"` appears in `actor_system`; the
  `actor_id` must identify the specific process within that system).

**Schema implication:** System process activity records must carry sufficient
`actor_id` specificity to support audit queries filtering by process type. A
record where `actor_type: system` and `actor_id` is the system name alone is
insufficiently attributed.

---

## External Actor Scope Decision

**Decision: External Actor is outside the canonical `actor_type` enumeration.
`external` is not a valid `actor_type` value. External Actor events do not
produce activity trail records under external attribution.**

**Rationale derived from current docs:**

`governance/auth-and-actor-model.md` defines External Actor as a governance
doctrine class with a clear rule: "External actors may provide signal, requests,
or external-world inputs. They are not automatically governed internal authority
actors." The same doc states that planning-relevant external input enters the
ecosystem through the VEDA signal interface or the project intake workflow.

`ecosystem/activity-trail-model.md` defines `actor_type` as one of `agent`,
`operator`, `system` — three values, no `external`. The External Actor doctrine
class has no corresponding canonical `actor_type` value on the current merged
baseline.

These two facts together establish the correct schema-layer posture:

- External Actor is a governance concept that explains how to classify and handle
  inputs from outside the ecosystem boundary.
- At the schema layer, external-origin inputs that enter the ecosystem through
  governed interfaces are recorded under the attribution of the receiving governed
  actor (the VEDA system process that ingested external signal, the operator who
  initiated the intake workflow, etc.).
- The resulting activity trail record carries `actor_type: system` or
  `actor_type: operator` depending on which governed actor handled the external
  input — not an `external` actor type.

**Consequence for external-origin context:**

Where the provenance of an external input is relevant to governance review,
it must be preserved in the `details` field of the activity record under a
source context field (e.g., `external_source_ref`, `external_input_type`) —
not by inventing an `external` `actor_type`. The governed actor remains the
attributable actor for the record. The external origin is context within that
record.

**This decision must not be reopened by adding `external` to `actor_type`
without a canon-change edit to `ecosystem/activity-trail-model.md` first.**

---

## Approval Record Actor Reference Posture

Approval records must reference the approving actor using the same identity
contract defined in this document. The following rules apply specifically to
actor references in approval-related contexts.

**Stable identity required.** The approving actor in an approval record must be
identified by a stable `actor_id` value as defined in the Actor ID Value-Class
Contract above. For human approvals, this means the operator's stable user record
identifier. A free-text name, a display label, or a session-local reference is not
a valid approving actor identifier in a governed approval record.

**`actor_type` must be `operator` for human approvals.** The
`governance/approval-and-escalation-model.md` Reviewability Principle states that
the ecosystem must be able to determine "who approved it." For approval events
where a human must grant the decision (`approval.decide` records), the `actor_type`
must be `operator` and the `actor_id` must be the stable operator user record
identifier. An `agent` actor must not appear as the approving actor in a
`approval.decide` record for an action that requires human approval posture.

**Approval records must support the Reviewability Principle queries.** Given an
`actor_id` on an approval record, it must be possible to determine:

- which human operator (or system process, for automated approvals within
  permitted scope) granted the approval
- under what system context and session the approval was granted
- that the actor had the class of authority required for that approval class

**Approval records are not satisfied by agent-produced content.** An agent may
produce the `approval.request` record. The `approval.decide` record for a
Human-Required action class must carry an `actor_type: operator` with a stable
operator `actor_id`. Approval records where a human decision is required but
`actor_type` is `agent` or `system` are malformed governed records.

**For system-automated approval-adjacent events** (e.g., expiry of a pending
approval due to time window, automatic escalation by a scheduled process):
`actor_type: system` is permitted for the resulting activity record, provided
the `actor_id` identifies the specific system process and the `action` type
reflects the automated outcome (e.g., `approval.escalate` rather than
`approval.decide`).

---

## Activity Trail Actor Reference Posture

The following rules apply to actor fields in all activity trail records.

**Actor fields are required on every record.** `actor_type`, `actor_id`, and
`actor_system` must be present and non-null on every activity trail record.
There are no activity trail record types that may omit actor attribution.

**`actor_type` must be one of the three canonical values.** Only `agent`,
`operator`, and `system` are valid. The field must not be null, empty, or set
to any other value.

**`actor_system` must be one of the five canonical values.** Only `project_v`,
`veda`, `v_forge`, `ecosystem`, and `extension` are valid. The field must
reflect the system context the actor was operating in when the action was taken
— not the `target_system` of the affected entity.

**`actor_id` must be stable within the value class for the `actor_type`.** The
stability and durability requirements are defined in the Actor ID Value-Class
Contract above. An `actor_id` that is stable for the duration of a single request
but not across sessions is not durable enough for governance replay purposes.

**`details` and `result_summary` must not substitute for actor identity fields.**
The `details` field carries action-specific supplementary context. It must not
be used to encode the actual actor identity when the base actor fields are absent
or insufficient. A record with an anonymous `actor_id` and actor identity buried
in `details` is not a properly attributed record.

**Actor identity must support filtered queries and governance replay.** The
activity trail query model (from `ecosystem/activity-trail-model.md`) requires
filtered queries by actor. This means `actor_type`, `actor_system`, and `actor_id`
must be structured fields with stable values — not free-text narrative fields.
Implementations must index or otherwise support filtering activity records by
actor identity.

---

## Anti-Drift Rules

The following rules prevent common actor identity failures at the schema layer.
All rules are consistent with existing doctrine in `governance/auth-and-actor-model.md`.

**Claimed role is not schema-defined actor identity.** An agent that receives a
prompt asserting `"you are acting as the planning authority"` must not use that
claimed role as its `actor_id`. Prompt-asserted roles are not governed actor
identifiers. The `actor_id` must come from the governed identity record for the
actor, not from prompt content.

**Free-text labels are not `actor_id` values.** Display names, role titles, team
names, and descriptive strings are not valid `actor_id` values. A valid `actor_id`
is a stable record identifier of the appropriate value class, not a human-readable
label.

**Session artifacts are not durable actor identity unless explicitly governed.**
A session token, an inference ID, or an ephemeral request identifier may be useful
for within-session correlation but is not a durable `actor_id` unless the ecosystem
has explicitly established it as the governed stable identifier for that actor.
Using an ephemeral session artifact as the `actor_id` in an activity trail record
produces a record that cannot be replayed or audited by actor identity.

**Local per-system actor formats must not replace the canonical value-class posture.**
Each system may have internal identifiers for its operators, agents, and processes.
Those internal identifiers are acceptable as `actor_id` values provided they satisfy
the value-class requirements above (stable, durable, resolvable, of the correct
class for the `actor_type`). Systems must not invent alternate `actor_type` values
or alternate `actor_system` values to accommodate local identity formats.

**Access or capability does not change actor classification.** An agent that has
read access to operator-level data is still `actor_type: agent`. An agent that is
capable of performing an operator-level action through a tool does not thereby
become `actor_type: operator`. Actor classification is determined by the actor class
of the entity taking the action, not by the capabilities or data visible to that actor.

**External-origin context must not be smuggled into `actor_type`.** External inputs
that enter the ecosystem through governed interfaces are attributed to the governed
actor that processed them. Adding `external` as an `actor_type` value in a record —
without a prior canon-change edit to `ecosystem/activity-trail-model.md` — is
a schema violation. External provenance is recorded in `details`, not in `actor_type`.

**`actor_system` must reflect the actor's system context, not the target.** An
operator working in Project V who triggers a cross-system action carries
`actor_system: project_v`, not the `actor_system` of the target system. The
`actor_system` field describes where the actor was operating, not what was affected.
The target is captured by `target_system`.

**Anonymous output is not sufficient for governed approval records.** An approval
record where the approving actor's `actor_id` cannot be resolved to a specific
governed human operator (for Human-Required actions) is not a valid governed
approval record, regardless of how detailed or confident the approval content appears.

---

## Usage

This document should be used:

- when implementing the activity trail record schema: use the Actor ID Value-Class
  Contract to finalize the `actor_id` format for each actor type
- when designing approval record schemas: use the Approval Record Actor Reference
  Posture to ensure approving actors are referenced by stable, durable identifiers
- when building activity trail query infrastructure: ensure `actor_type`,
  `actor_system`, and `actor_id` are indexable fields supporting filtered queries
  by actor
- when reviewing whether an activity trail record is sufficiently attributed:
  check `actor_type`, `actor_id`, and `actor_system` against the value-class
  requirements here
- when the Project V, VEDA, or V Forge schema authority docs define entity schemas
  that include actor references: reference this document for the identity contract
  those references must satisfy
- when an implementation proposes a new actor identity format: verify it satisfies
  the value-class requirements above before adopting it

---

## Related Docs

- `governance/auth-and-actor-model.md` *(Tier 1 authority — actor classes, identity principle, attribution principle, minimum actor semantics)*
- `governance/approval-and-escalation-model.md` *(approval posture, reviewability principle, approval request principle)*
- `governance/allowed-agent-actions-matrix.md` *(agent action permissions, Human-Required action classes)*
- `ecosystem/activity-trail-model.md` *(actor field definitions, activity trail canon)*
- `ecosystem/ecosystem-schema-spine.md` *(actor_type and actor_system enumerations as ecosystem schema contracts)*
- `project-v/project-v-schema-authority.md` *(Project V entity schemas including approval_record — to be created)*
- `veda/veda-schema-authority.md` *(VEDA entity schemas — to be created)*
- `v-forge/v-forge-schema-authority.md` *(V Forge entity schemas — to be created)*
