# Doctrine-Aware Context Model — Design Pass

## 1. Purpose

This document captures a bounded design pass for stage-aware, authority-aware context loading in VedaOps.

It is a transition-support output based on:
- `doctrine-aware-context-model-note.md`
- current harness and continuity doctrine
- first-project planning materials

It does not define final doctrine.

---

## 2. Status

Transition-support only.

This model is:
- concrete enough to guide design and audit work
- not yet promoted into authority docs

---

## 3. Problem Being Solved

VedaOps has:
- canonical doctrine
- planning packets
- transition-support notes
- continuity artifacts

But lacks a clear model for:
- what gets loaded
- when it gets loaded
- how it is weighted
- what is excluded

Qdrant can retrieve candidates, but cannot decide admission or authority.

---

## 4. Proposed Context Classes

Keep minimal and usable:

1. **Canonical Authority**
   - System-owned records or authority docs
   - Always authoritative

2. **Referenced Authority**
   - Canonical records from another system
   - Read-only, not re-owned

3. **Derived Intelligence**
   - VEDA Strategy outputs
   - Must carry derivation basis

4. **Planning Packet / Framing**
   - Project-specific planning materials
   - Binding within planning context only

5. **Execution Packet**
   - Handoff / execution-scoped materials
   - Binding within execution scope

6. **Transition-Support**
   - Notes, working docs, inventories
   - Advisory only

7. **Continuity Artifact**
   - Memory, transcript-derived artifacts
   - Non-authority

8. **Inert Model Output**
   - Uncommitted LLM output
   - No authority

---

## 5. Proposed Workflow Stages

Only include stages that materially affect context posture:

1. Intake
2. Planning
3. Handoff Creation
4. Execution
5. Validation
6. Publication / External Mutation
7. Observation Return / Feedback

---

## 6. Stage-by-Stage Loading Posture

### Intake

**Mandatory:**
- Canonical Authority (Project V, ecosystem boundaries)

**Selective:**
- Transition-support
- Planning packet (if provided)

**Exclude:**
- Execution packets
- Continuity artifacts from unrelated work

**Advisory:**
- Transition-support

---

### Planning

**Mandatory:**
- Canonical Authority
- Planning Packet

**Selective:**
- Referenced Authority
- Transition-support

**Exclude:**
- Execution packets
- Raw continuity artifacts

**Advisory:**
- Transition-support

---

### Handoff Creation

**Mandatory:**
- Canonical Authority
- Planning Packet

**Selective:**
- Referenced Authority

**Exclude:**
- Execution outputs
- Validation context

**Advisory:**
- Transition-support

---

### Execution

**Mandatory:**
- Canonical Authority
- Execution Packet

**Selective:**
- Referenced Authority
- Execution-scoped digest of planning decisions, only if deliberately prepared and explicitly scoped for execution use (not the planning packet itself)

**Exclude:**
- Planning packet in any form not explicitly scoped for execution
- Validation artifacts
- Builder continuity artifacts from planning-stage work

**Advisory:**
- Transition-support

---

### Validation

**Mandatory:**
- Canonical Authority
- Execution outputs

**Selective:**
- Referenced Authority

**Exclude:**
- Planning packet
- Builder continuity artifacts

**Advisory:**
- Transition-support

---

### Publication / External Mutation

**Mandatory:**
- Canonical Authority
- Approved execution outputs

**Selective:**
- Referenced Authority

**Exclude:**
- Planning packet
- Raw execution context

---

### Observation Return / Feedback

**Mandatory:**
- Canonical Authority (VEDA — observation record only)

**Selective:**
- Derived Intelligence (VEDA Strategy), carried with derivation basis intact and treated as signal, not as planning instruction

**Exclude:**
- Planning packet
- Execution packet
- Continuity artifacts from prior planning or execution stages

**Advisory:**
- Transition-support

**Posture note:** VEDA Strategy derived intelligence may be present at observation return. It must not be allowed to function as a planning instruction at this stage. Signal informs; it does not command. Any planning implication routes back through Project V intake, not through observation return context.

---

## 7. Authority and Weighting Rules

**Ranked ordering (highest to lowest within any stage):**
1. Canonical Authority — always outranks everything else
2. Referenced Authority — read-only, bounded to its owning system
3. Execution Packet (within execution scope) / Planning Packet (within planning scope)
4. Derived Intelligence — requires visible derivation basis; outranks transition-support, not canonical records
5. Transition-Support — advisory only, never outranks governed material
6. Continuity Artifacts — non-authority, cannot outrank canonical state
7. Inert Model Output — no authority
8. Retrieval results — must be filtered through class + stage before admission; never treated as authority on their own

**Additional rules:**
- Planning packets outrank transition-support within planning only; they do not transfer authority into execution
- Execution packets outrank planning context during execution; a planning packet without an execution-scoped digest is excluded, not demoted
- Derived Intelligence requires visible derivation basis at all times; a VEDA Strategy signal whose basis has been compacted away is not a usable signal
- Continuity artifacts never outrank canonical state
- Retrieval results are candidates, not facts; admission through this ranked model is required

---

## 8. Validation-Independence Rule

Validation must not inherit:
- planning packet
- builder continuity artifacts from planning or execution stages
- intermediate reasoning or working hypotheses from prior stages
- transition-support notes that carry planning intent framing

Validation must load:
- Canonical Authority (the rules being validated against)
- Execution outputs being evaluated
- Referenced Authority where the validation rule set requires it

Validation must not load:
- Any context that was produced by the builder/executor and that could bias the assessment of whether the execution met the canonical rules

**Enforcement note:** Validation context should be assembled independently of the execution-stage context assembly. They are not the same load. If the same context bundle is used for execution and validation, the harness is not enforcing independence.

---

## 9. First-Project Proving Case Mapping

### Planning stage

Load:
- project shape doc
- planning packet
- Project V doctrine

Selective:
- transition notes

Risk:
- retrieval surfacing irrelevant affiliate patterns

---

### Execution stage

Load:
- execution packet (derived from planning)
- V Forge doctrine

Selective:
- referenced authority

Risk:
- loading planning packet directly → drift

---

### Validation stage

Load:
- execution outputs
- canonical rules

Exclude:
- planning packet

Risk:
- bias from planning intent

---

### Retrieval role

Useful for:
- finding relevant doctrine
- finding related examples

Dangerous when:
- treated as authority
- bypassing stage filtering

---

## 10. Support for Loaf Audit

**What this model enables:**
- stage-by-stage traceability of context loading decisions
- context auditability against class + stage rules
- detection of boundary violations (wrong class at wrong stage, retrieval bypassing authority ranking, planning context bleeding into validation)

**What a Loaf Audit could check against this model:**
- what context was loaded at each stage
- whether the loaded context class matched the stage rules in Section 6
- whether authority weighting from Section 7 was respected
- whether validation independence from Section 8 was preserved
- whether excluded context was actually excluded, not just deprioritized

**Current readiness caveat:** This model is a necessary precondition for a Loaf Audit, not a sufficient one. A Loaf Audit also requires the harness to actually enforce these rules at runtime and to produce inspectable load records. The enforcement mechanism is currently open (see Section 11). This model is partially Loaf Audit ready: the audit criteria are defined; the enforcement that would make them verifiable is not yet built.

---

## 11. Open Questions

- **Enforcement mechanism in harness:** How the harness actually enforces the class + stage loading rules at runtime. Until this is built, the model is advisory. This is the primary gap between the model and Loaf Audit readiness.
- **Stage isolation strictness:** How strict stage isolation should be — specifically, whether a stage transition requires a context flush or whether context accumulates across stages with explicit pruning. Not resolved here.
- **Excluded context surfacing:** How to surface excluded context to the operator so they can inspect what was deliberately not loaded. Necessary for auditability; design is open.
- **Execution-scoped planning digest:** What form a legitimately scoped planning digest for execution use should take, who produces it, and what governs its contents. Not settled; flagged by the Execution stage posture above.
- **First-project proving-case failure posture:** If the first project exposes that this model's stage rules are wrong in practice, the model should be revised rather than the project bent to fit it. That feedback loop is not yet formalized.

---

## 12. Recommended Next Move

- test this model against first-project execution simulation
- identify failure points
- refine before promoting to doctrine

---

## 13. Related Files

- doctrine-aware-context-model-note.md
- ../first-project-entity-driven-gift-discovery-site.md
- ../first-project-entity-driven-gift-discovery-planning-packet.md
- llm-harness-architecture.md
- desktop-memory-and-continuity-model.md
- ../transition-plan.md
