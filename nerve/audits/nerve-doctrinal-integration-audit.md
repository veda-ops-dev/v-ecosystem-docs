# Doctrinal Integration Audit: Borrowing Runtime Patterns from claw-code

**Type**: Audit report — doctrinal compliance assessment
**Auditor posture**: V Ecosystem authority-first
**Date**: 2026-04-01
**Status**: Investigation wave complete — see `planning/nerve-runtime-roadmap.md` for current state

---

# NOTE — STATUS

This document reflects the **investigation / audit phase** of the Nerve runtime direction.

- The recommendations and sequencing judgments in this document have already been evaluated and used.
- This document should now be read as **audit context**, not as the current live execution plan.
- For current phase status, completed artifacts, and next bounded moves, refer to:

```text
planning/nerve-runtime-roadmap.md
```

---

# 1. Audit Conclusion in Plain English

You can borrow five things from claw-code safely: the `TokenBudget` trigger model, the `CompactStrategy` trait interface, the `Tool` trait shape, the `ToolOrchestrator` read-only/mutating partition pattern, and the per-turn token accumulation counters. These are mechanical patterns that do not touch authority, governance, or memory.

Everything else requires adaptation, and some of that adaptation is heavy enough that what you're really doing is writing fresh V code informed by a claw-code pattern — not borrowing.

The core risk is not any single pattern. The core risk is that the claw-code codebase was designed for a **single-user, single-workspace, ungoverned coding assistant** and the V Ecosystem is a **multi-system, governed, authority-separated operational platform**. Every pattern in claw-code was built under the assumption that the operator *is* the authority, the workspace *is* the ground truth, and compaction is a convenience operation with no governance consequences. None of those assumptions hold in V.

The prior analysis correctly identified the high-value patterns and correctly rejected the product-shell and plugin layers. Where it is too loose is in the compaction and memory areas — it treats these as "strong adaptation required" when several of them are closer to "write from scratch using V doctrine, with claw-code as one of several reference inputs." The prior analysis also under-weights how much the existing V doctrine already constrains these areas. The doctrine is not silent on compaction, memory, or tool assembly — it has detailed rules. The implementation docs are companions to existing doctrine, not replacements for absent doctrine.

**The single most important thing to get right is this:** V's existing extension-memory-and-continuity-model.md already defines compaction classes, compaction blocking rules, compaction failure posture, protected context rules, compact boundary requirements, memory classes, freshness rules, and anti-drift rules in load-bearing detail. Any implementation doc must be subordinate to that existing doctrine, not a parallel authority.

---

# 2. What Earlier Analysis Got Right

## Historical note

The findings in this section are retained because they explain why the first-wave and second-wave doc decisions were made.
They are no longer the live planning source.

The prior analysis (integration analysis + source-mapped reference) is directionally correct on these points:

**Correct: substrate vs product shell distinction.** The separation of claw-code into reusable runtime patterns versus CLI product shell is clean and accurate. The reject list (REPL, slash commands, plugin hooks, provider abstraction, workspace detection) is correct.

**Correct: compaction is the highest-priority runtime concern.** Without a compaction implementation, long V sessions die. This is the right first priority.

**Correct: `TruncateStrategy` is not sufficient for V.** The source code confirms it's a naive oldest-message dropper with no concept of protected content. V needs a governed variant, not a borrowed one.

**Correct: the `Tool` trait needs V-specific extensions.** Adding `owning_system()`, `required_scope()`, and `action_class()` to the trait is the right adaptation direction for absent-affordance enforcement.

**Correct: the permission layer needs to be richer than claw-code's.** `RuleBasedPolicy` with glob matching is a starting point, but V's governance model (four action classes, per-system rules, per-scope rules, approval-required gates) demands a fundamentally different policy implementation.

**Correct: plugin/hook system is a reject.** Ungoverned capability expansion is incompatible with V's governed surface model. This judgment is sound.

**Correct: pre-compaction memory flush does not exist in the source code.** The prior analysis correctly identifies that this is a conceptual pattern from the broader OpenClaw ecosystem, not something with actual code to borrow. V has to build it.

**Correct: token/cost tracking is pure utility.** The `SessionState` counters and `QueryEvent::Usage` emission are directly reusable with minimal adaptation and zero governance risk.

---

# 3. What Earlier Analysis Is Still Too Loose or Risky

The contents of this section are preserved as audit findings.
Any sequencing or execution implications should now be interpreted through the roadmap rather than read as direct live instructions.

## 3.1 — Compaction is treated as a single new doc when V already has extensive doctrine

The prior analysis recommends writing `extension-runtime-compaction-lifecycle.md` as a "single document that defines the complete compaction lifecycle." This under-appreciates that `extension-memory-and-continuity-model.md` already defines:

- three compaction classes (micro-compaction, working-memory extraction, full conversational compaction)
- compaction blocking rules (seven specific blocking conditions)
- compaction failure posture (halt, surface, preserve in review-required posture)
- compact boundary requirements (visible, attributed, not converted to canonical state)
- protected context categories (nine specific items)

The implementation doc should be a **companion design note subordinate to the existing doctrine**, not a standalone lifecycle document that risks becoming a parallel authority on compaction. The prior analysis does not reference these existing compaction rules at all, which suggests the analyst did not read the memory-and-continuity doc closely enough before recommending the doc shape.

**Correction**: The implementation doc must explicitly subordinate itself to `extension-memory-and-continuity-model.md` and reference its compaction classes, blocking rules, and failure posture by name. It adds mechanical detail. It does not redefine the doctrinal posture.

## 3.2 — Protected context is treated as a new concept when it already has detailed rules

The prior analysis frames protected context as something that needs a "mechanical model" as if the concept is under-specified. But the memory-and-continuity doc already lists protected context categories:

- current project scope
- current system posture
- current workflow-stage state
- active approval and gating state
- loaded decision continuity context
- loaded evidence basis markers and freshness state
- session integrity state
- active runtime warnings

The implementation doc needs to specify how these existing categories map to a mechanical flag-and-preserve system — not rediscover or redefine them.

## 3.3 — Memory flush governance is under-specified relative to V's existing rules

The prior analysis recommends a "memory flush governance note" but does not anchor it to the existing memory-and-continuity doctrine's:

- non-authority vocabulary rule (which already constrains what language flush artifacts may use)
- freshness/aging/supersedence rule (which already constrains how flush artifacts age)
- source attribution rule (which already requires attribution on all non-trivial artifacts)
- continuity admission rule (which already requires explicit admission before artifacts participate)
- operator visibility and control rule (which already requires operator review capability)

The flush governance is already substantially constrained by existing doctrine. What's missing is the mechanical trigger, write scope, and integration with the compaction lifecycle — not the governance posture, which already exists.

## 3.4 — The source-mapped reference overreaches on `VSessionState` fields

The source-mapped reference proposes a `VSessionState` with a `governance_context_valid: bool` field that flips to false after compaction and requires re-validation. This is dangerously simplistic for V's context model. V's `extension-state-and-context-model.md` defines nine distinct state categories, each with its own freshness, synchronization, and invalidation rules. A single boolean cannot represent the post-compaction validity state of nine independent categories.

**Correction**: Post-compaction validation should be per-state-category, not a single flag. Each of the nine categories in the state-and-context model has its own invalidation triggers and refresh requirements. The implementation must check each one after compaction, not just flip a boolean.

## 3.5 — The `SystemInitAssembler` proposal does not account for refresh posture

The source-mapped reference proposes a multi-source system-init assembler, which is correct directionally. But it does not account for the session refresh posture already defined in the system-init-and-tool-surface model, which requires material refresh on:

- project scope change
- current-system change
- workflow-stage change
- approval-state change
- evidence-basis refresh or invalidation
- meaningful compaction event
- delegated work completion

The assembler is not a one-shot boot-time thing. It must support bounded re-assembly triggered by invalidation events. The prior analysis treats it as a boot-time pipeline, which is incomplete.

## 3.6 — Worker/sub-agent patterns are too casually treated

The prior analysis gives worker delegation "Medium" value and says V's orchestration doctrine is "already stronger." This is correct but underestimates the implementation risk. The orchestration doc defines detailed rules about scope inheritance, output typing, governance preservation, approval-in-flight behavior, and visibility requirements. Any task/worker implementation must comply with all of these. The claw-code `TaskManager` with its simple `register/update_state/drain_notifications` model is architecturally insufficient for V. It would need such heavy adaptation that it's not really borrowing anymore.

## 3.7 — The doc sequence does not prioritize getting the subordination relationship right

The prior recommended sequence writes new docs first, then patches existing docs. This is backwards for V's authority model. The existing Tier 1 docs define the constraints. Any new doc must be written *knowing* exactly what constraints it operates under. The correct sequence should verify the existing doctrine is sufficient first, then write implementation companions that explicitly reference and subordinate to it.

---

# 4. Audit Table — Candidate by Candidate

| Candidate Pattern | Safe to Borrow? | Required Adaptation | Primary Doctrine Risk | Blocked Until | Best Doc Destination |
|---|---|---|---|---|---|
| **TokenBudget struct** (trigger model) | Yes, with minor extension | Add `protected_reserve` field for V's protected-context budget | None | Nothing | Implementation detail in compaction design note |
| **CompactStrategy trait** (async interface) | Yes | None needed — trait shape is clean and pluggable | None — V implements its own strategy | Nothing | Implementation detail in compaction design note |
| **TruncateStrategy impl** | No | V needs a `GovernedCompactStrategy` that respects protected context, compaction blocking rules, and compaction classes. The truncation approach is architecturally insufficient. | Compaction shredding protected context (governance-critical) | Compaction design note written and subordinated to existing memory/continuity doctrine | Fresh V code |
| **compact_session() in query.rs** | No | The function is a naive oldest-half drainer with no protected context, no flush, no blocking checks, no compact-boundary creation. V must build from scratch. | Every compaction risk in the doctrine — silent protected-context loss, invisible compaction, no operator visibility, no compact boundary | Compaction design note | Fresh V code |
| **Pre-compaction memory flush** | Not yet (no source exists) | Must be built fresh. Must comply with: non-authority vocabulary rule, freshness rule, source attribution rule, admission rule, operator visibility rule — all from existing memory/continuity doctrine. | Memory becoming fake authority — the #1 risk | Compaction design note + flush scope defined as governed action class in agent-operating-doctrine | Fresh V code with doctrine compliance |
| **Memory tiering (ephemeral/session-durable/cross-session)** | Not yet — V doctrine already defines this | V's memory-and-continuity model already defines three memory classes with detailed admission, freshness, and anti-drift rules. Implementation must comply, not reinvent. | Loosening existing doctrine by treating it as under-specified | Nothing — doctrine exists | Implementation companion to existing memory/continuity doc |
| **System-init assembly** | Yes, with strict adaptation | The `build_system_prompt()` two-string concat is a pattern seed only. V needs a multi-source, ordered, budget-aware, refreshable assembler subordinate to the system-init-and-tool-surface model's seven required categories and refresh triggers. | Stale basis surviving material context changes | System-init doctrine is already written; implementation companion can proceed | Implementation companion to existing system-init doc |
| **Tool trait** (name/desc/schema/execute) | Yes, with extension | Add `owning_system()`, `required_scope()`, `action_class()` for V's absent-affordance enforcement | None from the trait itself — risk is in filtering logic | Nothing | Implementation detail in tool-surface design note |
| **ToolContext struct** | Yes, with extension | Add `active_system`, `project_scope_token`, `operator_id` | Access-as-authority confusion if scope fields are not enforced | Nothing | Implementation detail in tool-surface design note |
| **ToolRegistry** | Yes, with extension | Add `filtered_definitions()` that enforces current-system, scope, and action-posture filtering per the system-init-and-tool-surface model | Tool overexposure — LLM sees wrong-system tools | Nothing | Implementation detail in tool-surface design note |
| **ToolOrchestrator** (read-only/mutating partition, permission check) | Yes, with strict adaptation | Must add system-boundary checks, scope checks, action-class checks. Must integrate with V's four-class governance model, not just read-only/mutating binary. | Cross-system mutation through tool dispatch, delegation privilege expansion | Tool-surface design note + governance integration spec | Implementation companion |
| **PermissionPolicy trait** | Yes | Clean trait interface, directly reusable | None from the trait | Nothing | Implementation detail |
| **PermissionMode / ResourceKind** | Yes, with extension | Add V-specific resource kinds (ProjectVRead, VForgeExecute, VForgeApprovalRequired, etc.) | None from the types | Nothing | Implementation detail |
| **RuleBasedPolicy** (glob matching) | No | V needs a `VGovernedPolicy` that consults the four-class action model, per-system rules, per-scope rules, approval state, and active gating posture. Glob matching is architecturally insufficient. | Governance theater — policy that appears to check permissions but doesn't enforce the real governance model | Governance-and-gating model integration design | Fresh V code |
| **Token/cost tracking** (SessionState counters + QueryEvent::Usage) | Yes | Directly reusable. Add `context_fill_pct()` method. | None | Nothing | Implementation detail |
| **Session state container** (SessionConfig + SessionState) | Yes, with strict adaptation | Must carry V's nine state categories, per-category freshness tracking, per-category invalidation flags. A single `governance_context_valid` bool is insufficient. | Session state mistaken for canonical records; single-boolean validation hides per-category failures | Compaction + state-model integration design | Implementation companion to state-and-context model |
| **Transcript persistence** | Not yet | V's memory-and-continuity doc already defines transcript artifact posture: not canonical, not decisions, not approvals, not evidence. Implementation must enforce non-authority vocabulary rule and operator visibility rule. | Transcripts becoming pseudo-governance records | Memory/continuity doctrine already covers this; implementation companion can proceed after compaction design note | Implementation companion |
| **Task lifecycle** (TaskState/TaskInfo/TaskManager) | Yes, with strict adaptation | Must add attribution, authority-class labeling, inert-output typing per orchestration model. Must enforce scope inheritance, tool-surface narrowing, governance preservation. | Worker findings becoming shadow evidence; delegation privilege expansion | Orchestration model is already written; implementation can proceed | Implementation companion to orchestration model |
| **Worker/sub-agent delegation** | Yes, with strict adaptation | Must comply with full orchestration model: scope inheritance, output typing, governance preservation, approval-in-flight awareness, visibility, cancellation. | Hidden approval paths; authority amplification by delegation; self-authorization | Orchestration model already covers this; implementation companion can proceed | Implementation companion to orchestration model |
| **Worker permission bridge** | Not yet | V's orchestration model requires delegated tool-surface narrowing. Workers must not gain broader authority than parent session. Permission bridge must enforce this structurally. | Delegation privilege expansion | Tool-surface design note + orchestration implementation companion | Fresh V code |
| **Worker memory sync** | Not yet | Worker findings must be attributable, non-canonical, reviewable. Sync must comply with memory-and-continuity doctrine's delegated-findings rules. | Worker findings becoming automatic truth; cross-scope bleed | Memory/continuity doctrine already covers this; compaction design note needed first | Implementation companion |
| **Plugin/hook extensibility** | No | Ungoverned capability expansion. Incompatible with V's governed surface model, absent-affordance doctrine, and structural enforcement requirements. | Capability sprawl, governance bypass, hidden tool injection | Permanently rejected unless V's governance model fundamentally changes | N/A — reject |
| **CLI/product-shell posture** | No | V is extension-centered. CLI REPL, slash commands, terminal rendering, workspace detection heuristics are all product-shell concerns that leak terminal-first assumptions. | Extension becoming a CLI wrapper; operator surface degrading from governed panel to terminal emulator | Permanently rejected | N/A — reject |

---

# 5. Real Doctrine Gates

## Historical note

This section is preserved because it explains why the initial governance-gate and implementation-companion sequence was chosen.
The gated sequence described here has already been executed where appropriate.
For the live current sequence, use the roadmap.

## Absolute prerequisites (must exist before risky imports go live)

### Gate 1 — Compaction design note subordinated to existing memory/continuity doctrine

**What**: An implementation companion doc that defines the mechanical compaction lifecycle — trigger conditions, budget model, strategy interface, protected-context flag mechanics, pre-compaction flush integration point, compact-boundary creation, post-compaction per-category re-validation — explicitly subordinated to `extension-memory-and-continuity-model.md`.

**Why absolute**: Without this, compaction either doesn't exist (sessions die) or is implemented ad-hoc (governance constraints get shredded). The existing doctrine defines *what* must be preserved and *when* compaction is blocked. This design note defines *how*.

**Existing doctrine it must reference by name**: Three compaction classes. Seven compaction blocking conditions. Compaction failure posture (halt, surface, review-required). Protected context categories (all nine). Compact boundary requirements.

### Gate 2 — Pre-compaction flush write scope as a governed action class

**What**: A bounded patch to `governance/agent-operating-doctrine.md` that classifies the pre-compaction memory flush as a governed action with constrained write scope.

**Why absolute**: The flush is an agent-initiated write to durable storage. If it's not classified as a governed action, there's no doctrinal basis for constraining what it writes. The existing memory/continuity doc constrains what memory artifacts *look like* (non-authority vocabulary, attribution, freshness) but doesn't classify the *act of writing them* as an action class.

**What the patch should say**: The pre-compaction flush is a bounded Class A action (non-mutating to canonical state) with constrained write scope: it may write to designated non-authoritative memory artifacts only, must use observational language per the non-authority vocabulary rule, and must carry source attribution per the memory source attribution rule.

### Gate 3 — Tool-surface implementation note subordinated to existing system-init/tool-surface doctrine

**What**: An implementation companion doc that defines the mechanical tool registry, session-scoped filtering, and absent-affordance enforcement — subordinated to `extension-system-init-and-tool-surface-model.md`.

**Why absolute**: Without this, the tool surface is either unfiltered (LLM sees wrong-system tools) or filtered ad-hoc (inconsistent with doctrine). The existing doctrine defines *what* must be filtered and *why*. This note defines *how*.

## Later refinements (important but not blocking)

### Gate 4 — Token/cost tracking design note

Low risk, no governance dependencies. Can be written anytime.

### Gate 5 — Task/worker implementation companion subordinated to orchestration model

Important for V Forge execution support but not blocking initial compaction and tool-surface work.

### Gate 6 — Transcript persistence implementation companion

Subordinated to existing memory/continuity doctrine. Not blocking initial compaction work.

---

# 6. Correct Next Doc Sequence

## Historical note

This sequence is preserved as the audit-era recommendation that informed the first implementation wave.
It is no longer the live execution source.
Use `planning/nerve-runtime-roadmap.md` for current sequencing and active next steps.

## Step 1 — Patch `governance/agent-operating-doctrine.md`

**Type**: Bounded patch to existing doc

**What**: Add pre-compaction memory flush as a governed action class. One paragraph. Classify it as bounded Class A with constrained write scope to non-authoritative memory artifacts. Reference the non-authority vocabulary rule and source attribution rule from the memory/continuity doc.

**Why first**: This is the smallest, fastest gate to clear. It takes five minutes and unlocks the compaction design note's ability to reference the flush as a governed action. Without it, the flush integration point in the compaction design note has no doctrinal anchor for write-scope constraints.

## Step 2 — Write `interfaces/extension-compaction-implementation-design.md`

**Type**: New bounded implementation companion doc (Tier 3)

**What**: The mechanical compaction lifecycle, explicitly subordinated to `extension-memory-and-continuity-model.md`. Covers: trigger conditions (based on `TokenBudget` pattern), per-category protected-context flagging (mapped to the nine categories in the state-and-context model), pre-compaction flush integration (referencing the governed action class from Step 1), strategy interface (based on `CompactStrategy` trait), compact-boundary creation (per existing doctrine), post-compaction per-category re-validation (per existing invalidation triggers in state-and-context model).

**Why second**: This is the highest-leverage new artifact. It bridges existing Tier 1 doctrine to implementation without creating a parallel authority. It must reference by name: the three compaction classes, the seven blocking conditions, the compaction failure posture, the nine protected context categories, and the compact boundary requirements — all from existing docs.

## Step 3 — Write `interfaces/extension-tool-surface-implementation-design.md`

**Type**: New bounded implementation companion doc (Tier 3)

**What**: The mechanical tool registry, filtering, and absent-affordance enforcement, explicitly subordinated to `extension-system-init-and-tool-surface-model.md`. Covers: registry interface (based on `ToolRegistry` + `Tool` trait patterns), session-scoped filtering by current-system, project-scope, and action-class (mapped to the tool-surface assembly rule), referenced-system read posture (per existing doctrine), delegated tool-surface narrowing (per orchestration model), absent-affordance structural enforcement.

**Why third**: Can be written in parallel with Step 2. No dependency between them. Placed third because compaction is more operationally urgent.

## Step 4 — Patch `interfaces/extension-memory-and-continuity-model.md`

**Type**: Bounded patch to existing doc

**What**: Add a cross-reference to the compaction implementation design note (Step 2). Add a note in the compaction section stating: "The mechanical trigger, strategy, and per-category re-validation model for compaction are defined in the companion implementation design doc `extension-compaction-implementation-design.md`."

**Why fourth**: Integrates the new companion doc into the existing doctrine spine. Small patch. Must follow Step 2 because it references it.

## Step 5 — Patch `interfaces/extension-system-init-and-tool-surface-model.md`

**Type**: Bounded patch to existing doc

**What**: Add cross-reference to the tool-surface implementation design note (Step 3). Add a note about system-init re-assembly after compaction — the init message may need partial re-construction to restore any governance context that compaction summarized.

**Why fifth**: Integrates Step 3. Must follow Step 3.

## Step 6 — Write `interfaces/extension-token-and-cost-tracking-design.md`

**Type**: New bounded implementation companion doc (Tier 3)

**What**: Usage struct shape, per-turn and cumulative tracking, context fill percentage model, operator visibility surfaces. Based directly on claw-code's `SessionState` counters and `QueryEvent::Usage` pattern.

**Why sixth**: Pure utility, zero governance risk. Can be written anytime. Placed here because it's quick and independent.

## Step 7 — Patch `interfaces/extension-state-and-context-model.md`

**Type**: Bounded patch to existing doc

**What**: Add context fill percentage as a visible runtime state attribute, cross-referencing the token-tracking design note. This maps to category 9 (Session Tool-Surface Posture) or could be a new visibility item under the core state categories.

**Why seventh**: Small cleanup patch. Must follow Step 6.

---

# 7. Seductive Implementation Mistakes

## Seductive implementation mistakes

### Treating compaction as a convenience operation
In claw-code, `/compact` is routine maintenance. In V, compaction is a governance-relevant event because it changes what the LLM "knows" about active constraints. Treating it as routine leads to silent protected-context loss.

### Using a single boolean for post-compaction validity
The source-mapped reference proposes `governance_context_valid: bool`. V's state model has nine independent categories, each with its own invalidation triggers. A single boolean hides per-category failures. One category passing validation does not mean all nine passed.

### Writing the compaction doc as a standalone lifecycle authority
The existing memory/continuity doc already defines compaction doctrine in substantial detail. Writing a new "lifecycle" doc that doesn't explicitly subordinate itself creates a parallel authority. Two docs both claiming to define compaction posture is worse than one.

### Implementing tool filtering as a nice-to-have
Tool filtering is not a nice-to-have for V. It is the mechanical enforcement layer for absent-affordance doctrine. Without it, the LLM sees tools it should not see and proposes actions it should not propose. Absent-affordance is structural — it must be enforced by construction, not by hoping the LLM chooses well.

### Borrowing the `RuleBasedPolicy` and calling it done
Glob/prefix matching against file paths is not the same as checking whether an action is Class B, whether the current system owns the tool, whether the project scope matches, or whether an approval gate is required. V's permission model is fundamentally richer.

### Implementing memory flush without classifying it as a governed action
If the flush is not classified as a governed action class, there's no doctrinal basis for constraining what it writes. The flush agent could write decision-language, approval-language, or evidence-language, and there would be no rule it was violating. The agent-operating-doctrine patch (Step 1) closes this gap.

### Implementing session resume without fresh canonical loading
The state-and-context model already requires that session start loads all core state categories fresh from governed records. A resume flow that skips this and restores from prior session state violates the doc explicitly. "Prior session cache is not canonical even if it appears current."

### Implementing worker delegation as simple function calls
The orchestration model defines detailed requirements: scope inheritance, output typing, tool-surface narrowing, governance preservation, approval-in-flight awareness, visibility, cancellation. A `TaskManager.register()` + `drain_notifications()` model satisfies almost none of these.

---

# 8. Red Lines

## Red lines

1. **Compaction must not silently drop protected context.** The memory/continuity doc is explicit: "If compaction removes protected context, the runtime has violated continuity doctrine even if the session still appears usable." This is a hard rule, not a best-effort guideline.

2. **Memory artifacts must not use decision, approval, or authorization language.** The non-authority vocabulary rule exists for a reason. Flush artifacts saying "decided," "approved," or "authorized" create authority confusion even if labeled non-canonical.

3. **Continuity artifacts must not satisfy governance gates.** The governance-and-gating model is explicit: "Continuity artifacts, transcript artifacts, compaction products, and worker findings may improve operator usefulness. They do not satisfy governance gates."

4. **Delegated workers must not gain broader tool access than the parent session.** The system-init-and-tool-surface model requires delegated tool-surface narrowing. The orchestration model requires scope inheritance without widening.

5. **The compaction implementation doc must not become a parallel authority to the memory/continuity doctrine.** It is a Tier 3 companion, not a Tier 1 replacement.

6. **Post-compaction validation must be per-state-category, not a single flag.** Nine categories, nine independent checks. A single boolean is insufficient.

7. **Tool filtering must be structural, not instructional.** Absent-affordance enforcement means wrong tools are structurally absent, not merely discouraged. The governance-and-gating model's structural enforcement requirement #4 is explicit about this.

8. **Session resume must load canonical state fresh.** The state-and-context model forbids treating prior session cache as canonical current state.

9. **The plugin/hook architecture must not be imported in any form.** Ungoverned capability expansion is permanently incompatible with V's governed surface model.

10. **Orchestration must not become a shadow approval path.** The orchestration model's anti-drift rule #2: "A coordinator or specialist must not become a secret approval path."

---

# 9. Final Recommendation

## Historical note

This recommendation is retained because it explains the audit rationale that shaped the first implementation wave.
It should not be treated as the current live next-step plan.
Use the roadmap for live status and sequencing.

## 5 safest imports

1. **`TokenBudget` struct** — mechanical trigger model, zero governance risk
2. **`CompactStrategy` trait interface** — clean async trait, V implements its own strategy
3. **Token accumulation counters** (`total_input_tokens`, `total_output_tokens`, `last_input_tokens`) — pure metrics
4. **`QueryEvent::Usage` event emission pattern** — operator visibility, no state mutation
5. **`Tool` trait shape** (name/description/schema/execute/is_read_only) — clean, extensible

## 5 highest-risk imports

1. **Pre-compaction memory flush** — doesn't exist in source; must be built with strict write-scope governance; highest memory-as-authority risk
2. **Session state container** — must carry nine state categories with per-category invalidation; simplistic borrowing creates hidden governance failures
3. **Worker/sub-agent delegation** — must comply with full orchestration model; claw-code's ungoverned model is architecturally insufficient
4. **Session resume/persistence** — must reload canonical state fresh; carrying forward stale session state violates state-and-context model
5. **Full conversational compaction** — highest-risk compaction class; must comply with all seven blocking conditions, failure posture, and compact boundary requirements

## 5 clear rejects

1. **Plugin/hook system** — ungoverned capability expansion, permanent reject
2. **CLI REPL and terminal product shell** — V is extension-centered, permanent reject
3. **`RuleBasedPolicy` with glob matching** — architecturally insufficient for V's four-class governance model
4. **`compact_session()` as implemented** — naive oldest-half drainer with no governance awareness, cannot be adapted
5. **Multi-provider abstraction** — V uses specific provider wiring; generic abstraction adds complexity without value

## Single best next bounded artifact

**This audit originally recommended a bounded patch to `governance/agent-operating-doctrine.md` classifying the pre-compaction memory flush as a governed action class. That recommendation has already been executed.**

## Final suggestion for the smartest path forward

The audit-era recommendation was:

1. patch the governed flush action class
2. write the compaction implementation companion
3. write the tool-surface implementation companion
4. stop and build

That first-wave logic was correct and has now been absorbed into the actual Nerve roadmap and canonical doc spine.
For the current live path forward, use:

```text
planning/nerve-runtime-roadmap.md
```
