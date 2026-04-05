# Session 24 — MVP Shell and Surface Priority
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Sessions 1–23 (all surfaces designed, visual language finalized, component behaviors specified)
**This is the final planned session in the UX work plan.**

---

## 1. What This Session Is

The work plan defines Session 24 as: "The actual build sequence for engineering. By this point every surface is designed and schema-blocked items are either resolved or explicitly held. This session translates the design sequence into a build sequence and identifies what the minimum viable operator loop looks like."

This session does not design new surfaces. It does not revisit decisions from sessions 3–23. It answers three questions:

1. **What is the minimum viable operator loop?** What must be working for the V Ecosystem desktop application to support real governance work, even before the full surface set is complete?

2. **What is the build sequence?** In what order should engineering build the components, stores, services, and surfaces from Sessions 3–23 — and which sessions map to which implementation phases?

3. **What is the surface priority tier structure?** Which surfaces are MVP-required, which are important but not blocking, and which are enhancements that come after the loop is proven?

---

## 2. What the MVP Operator Loop Is

The V Ecosystem desktop application exists to support a specific governing behavior: an operator who frames work, receives typed bounded outputs from the LLM, reviews those outputs against canonical state, and — when a governed action is warranted — completes the review-before-gate sequence and persists an approval event.

**The MVP operator loop is:**

```
1. Open the application with a project selected
2. See the current project scope, system, stage, and session health (topbar)
3. See the nine state categories loaded in the context strip
4. Frame work in the operator input field
5. Receive a typed bounded output (Recommendation or Review Summary)
6. Navigate to a record in the left nav (Project V tree)
7. Review the record in the center workspace
8. Complete the Class B review checkpoint sequence
9. The gate widget activates
10. Click [Approve]
11. Approval record is persisted
12. Activation path proceeds
```

Everything else — the portfolio view, the lower trace, the command palette, the VEDA and V Forge trees, the session integrity overlay, the full notification system, the power features — is either in service of this loop or an extension of it.

**The MVP loop requires exactly these surfaces:**
- Topbar (Session 3)
- Context strip in the right panel (Session 4)
- Right panel shell + operator input (Session 5)
- Left nav shell + Project V tree (Session 6)
- Center workspace foundation (Session 9)
- Class B inline approval widget (Session 10, Class B only)
- Review-to-gate routing (Session 11)
- Session start integrity check, minimal (Session 12, Phase 1 only)
- Handoff review UX (Session 13)
- Output card system — Recommendation and Approval Request Package (Session 1, two types only)

**The MVP loop does not require:**
- VEDA tree (Session 7) — needed for VEDA-system work; not blocking the Project V handoff loop
- V Forge tree (Session 8) — same
- Class C modal gate (Session 10) — launch authorization is later workflow
- Class D escalation banner (Session 10) — edge case; not blocking normal operation
- Full session integrity overlay (Session 12) — the topbar badges and minimal startup check are enough for MVP
- Return trigger review full surface (Session 13) — partial; the basic routing works without the full surface
- Launch readiness (Session 14) — a later workflow stage
- Maintenance/ranking (Session 15) — even later
- Intake (Session 16) — blocked on schema
- Portfolio triage (Session 17) — power feature; multi-project work comes after single-project loop
- Lower trace (Session 18) — observability enhancement
- Decision timeline (Session 19) — schema-blocked
- Evidence freshness views (Session 20) — schema-blocked
- Command palette (Session 21) — keyboard shortcuts are an enhancement; nav tree + right panel are sufficient
- Visual language formalization (Session 22) — critical for production polish; not blocking function
- Component behavior patterns (Session 23) — transitions are enhancement; static states are MVP-sufficient

---

## 3. MVP Definition — Precise Scope

The MVP is the smallest buildable application that supports a real governance event through the complete governed path. It must be shippable to real operators doing real Project V planning work with real approval consequences.

### MVP must have — non-negotiable

**Shell:**
- Tauri window with topbar, left nav, center workspace, right panel at correct widths (260/flex/320px)
- Topbar: all 8 elements, all states, project/system switching functional
- Project scope enforced — session token bound to one project

**State:**
- All 9 context strip categories loaded and displayed
- Invalidation event handling for Events 1–12 (the core governance events)
- Session integrity state visible in topbar badges
- SCOPE, SYSTEM, STAGE, DECISIONS, EVIDENCE, INTEGRITY categories freshness-aware

**Left nav (Project V only):**
- Shell + Project V tree
- Objectives, Initiatives, Work Items, Gaps, Handoffs sections
- Return triggers section (appears when active)
- Intake section (honest schema-blocked display)
- All status dots and handoff status badges
- Navigation to center workspace on item click

**Right panel:**
- Context strip (all 9 rows, expandable, compact-mode toggle)
- Output area: Recommendation cards and Approval Request Package cards
- Operator input: framing input + mode selector (Brainstorm, Recommend, Review, Approval Req.) + submit
- `[Proceed to Approval Gate]` on ARP cards

**Center workspace:**
- Tab bar (open/close/switch tabs, max 5)
- Generic record detail view template (Overview/Evidence/Decisions/History/Actions sections)
- Handoff record detail view with full review content
- Class B inline approval widget (inactive → active → post-approval states)
- Review checkpoint model (all shared + handoff-specific checkpoints)
- Inline banner system for staleness notices and context changes

**Governance pipeline:**
- Approval record write before activation
- Rejection record write
- Stale-context warning blocks gate
- Checkpoint model enforced structurally

**Output cards (2 types):**
- Recommendation card (all required fields, action class badge, response options)
- Approval Request Package card (all required fields, `[Proceed to Approval Gate]` CTA)

**Session integrity (minimal):**
- Session start check: unresolved items from prior session surfaced at startup
- Topbar attention badges for pending approvals and return triggers
- `[Review Items]` navigation to session integrity view
- Session integrity view (basic list — no full overlay required for MVP)

### MVP should have — important but not phase-blocking

**Shell polish:**
- Panel resize handles (functional but transition behavior can be Phase 2)
- Right panel collapse to 40px rail
- Lower trace toggle chip (even if lower trace itself is Phase 2)

**Left nav:**
- VEDA tree (Session 7) — needed as soon as VEDA work begins
- V Forge tree (Session 8) — needed as soon as V Forge work begins
- System switching fully functional between all three trees

**Output cards (remaining types):**
- Review Summary card
- Uncertainty Notice card
- Continuity Reminder card
- Execution Report card (when V Forge work begins)
- Finding card (when orchestration begins)

**Gate surfaces:**
- Class C modal gate — required before launch readiness workflow begins
- Class D escalation banner — required before any boundary-edge governance work begins

**Workflow surfaces:**
- Return trigger review surface (full, not minimal)
- Launch readiness surface (Session 14) — required before launch workflow
- Maintenance/ranking (Session 15) — required before maintenance workflow

### MVP can defer — enhancements after loop is proven

- Portfolio triage view (Session 17)
- Lower trace surface (Session 18)
- Command palette (Session 21)
- Full component motion and transitions (Session 23 — static states sufficient for MVP)
- Schema-blocked surfaces (Sessions 16, 19, 20 — unblock when schema settles)

---

## 4. Build Sequence

This section maps the UX sessions to the implementation architecture's 9 phases, then expands each phase into a concrete build order. Each item references the UX session that specifies it.

The implementation architecture's phase order (from `desktop-implementation-architecture.md`) is the authoritative sequence. This session's job is to populate it with UX-session references and surface-level specifics.

---

### Phase 1 — Shell and Scope

**What to build:** The visual shell with no backend connection. Static layout. Project selection UI. Topbar. Left nav shell. Center workspace shell. Right panel shell. Command routing skeleton.

**UX sessions:**
- Session 2 (token system — CSS custom properties as the first code artifact)
- Session 3 (topbar — all 8 elements, all states, project/system switching UI)
- Session 5 (right panel shell — three regions, resize handle, collapse)
- Session 6 (left nav shell — header, footer, scroll region, system switcher)
- Session 9 (center workspace shell — tab bar, view header, empty state)

**Concrete build order:**

1. **CSS token file** — implement the complete Session 22 final token reference (§13) as a single `:root` CSS custom property block. This is the first engineering artifact. All subsequent styling pulls from this file.

2. **Tauri window shell** — four-region layout: topbar (48px), left nav (260px), center workspace (flex), right panel (320px). Resize logic for right panel and lower trace. No content yet. Background colors from token file.

3. **Topbar shell** — eight elements in correct zones. All states wired to `sessionStore` (initially empty). Project/system switcher dropdowns opening but not connected to data.

4. **Left nav shell** — panel with header, scrollable tree region, footer. System switcher mirroring topbar. Empty tree region with loading shimmer.

5. **Right panel shell** — three regions (context strip / output area / operator input). Separator with compact-mode toggle. Input field with mode selector. Context strip rows as empty placeholders.

6. **Center workspace shell** — tab bar with `+ New Tab`. Empty workspace state. View header region. Tab open/close/switch.

7. **Command routing skeleton** — `workspaceRouter` stub: can accept record navigations and open tabs. No record content yet, but the routing plumbing exists.

**Phase 1 is done when:** The shell renders at correct dimensions with all panels visible, the topbar shows static content, the left nav panel is present, the center workspace shows its empty state, and the right panel shows its input region. Nothing is wired to real data. Everything looks like the specs.

---

### Phase 2 — State Spine

**What to build:** All 9 state stores wired to real data. Context loading from backend. Topbar goes live. Context strip goes live. Integrity state visible.

**UX sessions:**
- Session 3 (topbar all states — project indicator, system indicator, stage, badges, health)
- Session 4 (context strip — all 9 rows, freshness markers, staleness treatments, all 18 invalidation events)
- Session 6 (left nav — Project V tree populated from `projectVStore`)
- Session 12 (session start integrity check — minimal: startup overlay + topbar badges)

**Concrete build order:**

1. **`sessionStore`** — active project, current system, session health, connection state. Wire to Tauri IPC + sidecar `runtimeSessionService`.

2. **`contextStore`** — all 9 categories. `contextLoader` service wired to backend APIs via sidecar. Freshness markers implemented. Stale/missing/invalid states per category.

3. **`integrityStore`** — unresolved return triggers, pending approvals, stale readiness states. Wire to topbar badges.

4. **`projectVStore`** — objectives, initiatives, work items, gaps, handoffs loaded. Return triggers.

5. **Topbar goes live** — all 8 elements now show real state from stores. Project switching functional. System switching functional (EVENT-11 fires and propagates). Session health states functional.

6. **Context strip goes live** — all 9 rows rendering real data. Row expand/collapse functional. Compact-mode toggle functional. All invalidation events firing correctly via `refreshCoordinator` for events that affect context strip.

7. **Left nav Project V tree** — all 7 sections populated from `projectVStore`. Status dots and handoff badges correct. Navigation to center workspace functional (stubs to empty detail views for now).

8. **Session start integrity check (minimal)** — on project load, if integrity items exist, show the startup notice. Operator can dismiss. Items visible in topbar attention badges. Basic integrity list view openable from badges.

9. **`refreshCoordinator`** — all 18 invalidation events wired to correct store updates and surface propagation. This is the most complex piece of Phase 2. The matrix from `desktop-invalidation-and-refresh-matrix.md` is the implementation spec — every event, every consequence.

**Phase 2 is done when:** The application loads a real project, shows correct state in the topbar and context strip, navigating the left nav tree populates center workspace tabs (even with empty content), and badge counts in the topbar reflect real pending items.

---

### Phase 3 — Local-First Spine

**What to build:** SQLite support layer. Startup hydration. Draft persistence. Support-state reconciliation.

**UX sessions:** No dedicated UX session — this is infrastructure. The local-first layer is referenced in Sessions 4, 9, 12, and 18 but has no corresponding UX design session. The `local-first-architecture.md` doctrine doc governs this phase.

**Concrete build order:**

1. **SQLite support database schema** — tables for: recently accessed records (for command palette Recent section and tab restoration), draft states, local continuity artifacts, support-state reconciliation markers.

2. **Startup hydration path** — on session start, hydrate from local SQLite for display-speed while awaiting backend load. Mark hydrated state as `local` until backend confirms.

3. **Support-state reconciliation** — EVENT-18 (local state divergence) wired. When backend state differs from local SQLite state, surface the divergence marker.

4. **Recent records persistence** — track the last 10 records opened in center workspace per session. Used by command palette §7 (RECENT section) and tab restoration.

**Phase 3 is done when:** The application starts fast (local SQLite hydration), reconciles with backend state silently when it arrives, and flags divergence when backend differs from local. EVENT-18 fires correctly.

---

### Phase 4 — Runtime Session Basis

**What to build:** Session initialization, system init builder, tool surface assembly, continuity store, orchestration store, `refreshCoordinator` completion.

**UX sessions:**
- Session 4 (ORCH and CONTINUITY context strip rows — need orchestration and continuity stores populated)
- Session 5 (orchestration summary in right panel — needs `orchestrationStore`)

**Concrete build order:**

1. **`runtimeSessionService`** — full session initialization: scope token lifecycle, health and reconnection posture.

2. **`systemInitBuilder`** — assembles the runtime init object from loaded canonical state. Marks missing/stale categories.

3. **`toolSurfaceAssembler`** — assembles the session tool surface. Filters tools by project scope, current system, action posture.

4. **`continuityStore`** — working memory entries, compact-boundary records, freshness markers. Wire to context strip CONTINUITY row.

5. **`orchestrationStore`** — active orchestrator posture, task lifecycle states. Wire to context strip ORCH row.

6. **`refreshCoordinator` completion** — Events 12–15 (orchestration-related events) wired. The coordinator now handles the full 18-event matrix.

**Phase 4 is done when:** The context strip ORCH and CONTINUITY rows show real state, the session basis is assembled correctly at session start, and orchestration state updates propagate correctly when tasks fire.

---

### Phase 5 — Typed Output Rendering

**What to build:** LLM interaction pipeline. Output card rendering for all 7 types. Validation layer. Operator input functional.

**UX sessions:**
- Session 1 (output card system — all 7 types, all states, staleness markers)
- Session 5 (operator input, mode selector, submit, `[Proceed to Approval Gate]` CTA)
- Session 11 (review-to-gate routing — the ARP card routing into center workspace)

**Concrete build order:**

1. **Operator input → LLM pipeline** — mode selector wired to actual LLM interaction modes. Submit sends to sidecar, which routes to LLM via MCP. Response received as structured typed output.

2. **`recommendationValidator`** and **`approvalRequestValidator`** — validate typed outputs before rendering. Reject malformed outputs; surface validation failure notice.

3. **Output card renderer** — all 7 card types renderable:
   - Recommendation card (MVP-critical)
   - Approval Request Package card (MVP-critical)
   - Review Summary card
   - Uncertainty Notice card
   - Continuity Reminder card
   - Execution Report card
   - Finding card

4. **Staleness markers on output cards** — the invalidation event → staleness marker propagation wired for cards in the output area.

5. **`↓ New output` chip** — auto-scroll suppression and chip behavior.

6. **`[Proceed to Approval Gate]` routing** — ARP card CTA wires to `workspaceRouter` with `intent = 'approval_gate'`. Workspace opens target record.

**Phase 5 is done when:** The operator can type a framing input, receive a Recommendation, receive an Approval Request Package, and click `[Proceed to Approval Gate]` to open the target record in the center workspace.

---

### Phase 6 — Center Review Surfaces

**What to build:** Record detail views. Handoff review surface. Generic detail template fully populated. Inline banners.

**UX sessions:**
- Session 9 (generic record detail view template — all sections)
- Session 10 (Class B widget — inactive/active states, checkpoints, post-approval state)
- Session 13 (handoff review UX — overview, evidence, decisions, history, actions sections with handoff-specific content)

**Concrete build order:**

1. **`workspaceRouter` complete** — record navigation fully wired: left nav click, output card link, `intent = 'approval_gate'` routing. Tab management (max 5, LRU close).

2. **Generic record detail view** — Overview / Evidence / Decisions / History / Actions section template. Content rendering from `projectVStore`. Loading shimmers. 404/403 states.

3. **Inline banner system** — banner position wired for all relevant invalidation events. Staleness banners, context-change banners, session-error banners.

4. **Handoff record detail view** — extends generic template with handoff-specific section content:
   - Overview: handoff metadata, scope definition, out-of-scope items, blocking gaps summary
   - Evidence: linked evidence records with freshness markers
   - Decisions: governing decisions that apply to the handoff
   - History: state change log
   - Actions: review checkpoint list + Class B gate widget

5. **Class B approval widget** — full implementation:
   - Inactive state (checkpoints incomplete)
   - Checkpoint completion logic (5-second timers, explicit interaction requirements)
   - Active state with `--transition-spring` gate activation
   - `[Approve]` / `[Reject]` / `[Defer]` controls
   - Rejection reason prompt
   - Stale-context warning block (§4.7)
   - Post-approval confirmation state with `[Proceed to Activation ›]`

6. **Return trigger record detail view** — extends generic template with return trigger content and routing response selection (basic MVP version; full surface is enhancement).

**Phase 6 is done when:** The operator can navigate to a handoff record, see all review sections, complete all checkpoints, activate the gate widget, click `[Approve]`, and see the post-approval confirmation with `[Proceed to Activation ›]`.

---

### Phase 7 — Approval Pipeline

**What to build:** Full governance write path. Approval and rejection persistence. Typed confirmation flow. Stale approval detection. Activation precondition checks.

**UX sessions:**
- Session 10 (Class C modal gate — typed confirmation input, irreversibility notice)
- Session 11 (review-to-gate routing — the full 5-step state sequence)

**Concrete build order:**

1. **`approvalService`** (sidecar) — receives approval commands from frontend via IPC, validates preconditions, makes the backend API call to write the approval record, returns result. This is the most governance-critical service in the application.

2. **Approval persistence flow** — `[Approve]` click → IPC → `approvalService` → backend API → write approval record → return success → frontend shows post-approval state. No optimistic UI.

3. **Rejection flow** — `[Reject]` click → rejection reason prompt → `[Confirm Rejection]` → write rejection record.

4. **Stale approval detection** — `approvalService` checks approval freshness before presenting gate controls. Expired or invalidated approvals surface correctly.

5. **Activation precondition checks** — after approval written, `[Proceed to Activation ›]` triggers the activation API call. Preconditions checked before call (approval record confirmed, context not subsequently invalidated).

6. **Class C modal gate** — for launch authorization:
   - `[Proceed to Authorization Gate]` button in Actions section (blocked until all Phase 6 checkpoints + launch-specific checkpoints complete)
   - Modal structure, scrim, irreversibility notice
   - Typed confirmation input with exact-match validation
   - `[Confirm Authorization]` active only when phrase correct
   - Context-change handling mid-modal
   - `approvalService` wired for Class C write

7. **`approvalFlowController`** — ties together the five-step routing sequence from Session 11: card state → center workspace → review → gate activation → post-approval.

8. **`conflictDetector`** — decision conflict detection, approval state conflict detection, cross-record conflicts surfaced.

**Phase 7 is done when:** An approval event is persisted to the backend, the approval record is verifiable, the activation API is called only after confirmed write, rejection records are written, and the Class C typed confirmation flow works end-to-end.

---

### Phase 8 — Runtime Power Features

**What to build:** Orchestration service. Memory manager. Compaction. Transcript. Lower trace surface.

**UX sessions:**
- Session 18 (lower trace surface — Orchestration/Compaction/Transcript views)

**Concrete build order:**

1. **`orchestrationService`** — subtask creation, specialist invocation, task lifecycle management, cancellation and failure handling.

2. **`memoryManager`** — working continuity artifacts, freshness/age metadata, source attribution, clear/dismiss operations.

3. **`compactionService`** — micro-compaction, working-memory extraction, full conversational compaction. Protected context preservation. Post-compaction per-category validation. Compact-boundary records.

4. **`transcriptService`** — transcript capture, artifact retrieval, orchestration event log integration.

5. **Lower trace surface** — three views (Orchestration/Compaction/Transcript), non-authority labels, task lifecycle display, compaction event blocks with post-validation tables, transcript event ledger. EVENT-12, EVENT-13, EVENT-14 wired.

6. **`[Cancel]` on running tasks** — the only action in the lower trace. Wired to `orchestrationService` cancellation.

**Phase 8 is done when:** Delegated tasks are visible in the lower trace surface with correct lifecycle states, compaction events appear with per-category validation results, the transcript logs all session events, and `[Cancel]` works.

---

### Phase 9 — Workflow Drill-Down

**What to build:** Remaining workflow-specific surfaces. VEDA and V Forge trees. Remaining gate surfaces.

**UX sessions:**
- Session 7 (VEDA tree — observatory domains, provider sections, signal packages)
- Session 8 (V Forge tree — execution state, return triggers, content graph)
- Session 14 (launch readiness UX)
- Session 15 (maintenance/ranking UX)
- Session 17 (portfolio triage)
- Session 21 (command palette)

**Concrete build order:**

1. **VEDA tree** (Session 7) — needed when VEDA-system work begins. Observatory domains, provider health indicators, signal packages. Paid data pull routing to Class C gate.

2. **V Forge tree** (Session 8) — needed when V Forge-system work begins. Execution entries, content graph, return trigger representation.

3. **Class D escalation banner** (Session 10) — needed for any boundary-edge governance work. Escalation recording flow and `[Document and Hold]` write path.

4. **Launch readiness surface** (Session 14) — three-dimension confirmation strip, blocking conditions panel, Class C gate checkpoint for cross-system confirmation.

5. **Maintenance/ranking surface** (Session 15) — execution maintenance tracking, replanning trigger visibility, portfolio ranking.

6. **Portfolio triage view** (Session 17) — cross-project read-only aggregate using global API endpoints. `[Switch to this project ›]` routing.

7. **Command palette** (Session 21) — `⌘K` trigger, 57 commands, default contextual suggestions, record search sub-mode.

8. **Full session integrity overlay** (Session 12) — beyond the minimal MVP: full 4-group overlay, `[Review Items]` / `[Dismiss All]` controls, all 7 staleness marker types.

9. **Full notification system** (Session 12) — toast notifications, in-app notification surface, event scaling.

**Phase 9 is done when:** All non-blocked workflow surfaces are functional and all three system trees are populated. The full operator loop is available across all three systems.

---

## 5. Surface Priority Tiers

This translates the build phases into a priority tier structure for engineering planning.

### Tier 1 — MVP Critical (Phases 1–6)

Build sequence is strictly ordered. Each must complete before the next begins.

| Surface | UX Session | Phase |
|---|---|---|
| CSS token system | Session 22 | 1 |
| Tauri shell + layout | Sessions 3, 5, 6, 9 | 1 |
| Topbar (all 8 elements) | Session 3 | 1–2 |
| Context strip (all 9 rows) | Session 4 | 2 |
| Right panel shell + operator input | Session 5 | 1, 5 |
| Left nav shell + Project V tree | Session 6 | 1, 2 |
| Session store + context store + integrity store | Sessions 3, 4, 12 | 2 |
| Project V store + refresh coordinator | Sessions 6, 4 | 2 |
| Session start integrity check (minimal) | Session 12 | 2 |
| Local-first SQLite spine | (architecture doc) | 3 |
| Runtime session service + system init | (architecture doc) | 4 |
| Typed output rendering (Rec + ARP) | Session 1, 5 | 5 |
| `[Proceed to Approval Gate]` routing | Sessions 5, 11 | 5 |
| Generic record detail view template | Session 9 | 6 |
| Handoff record detail view | Session 13 | 6 |
| Class B approval widget (all states) | Session 10 | 6 |
| Inline banner system | Sessions 9, 10 | 6 |
| Approval persistence (approvalService) | Sessions 10, 11 | 7 |
| Rejection flow | Session 10 | 7 |
| Approval flow controller | Session 11 | 7 |

### Tier 2 — Important, Not MVP-Blocking (Phase 7–8 scope)

Can be built in parallel with late Phase 6 / early Phase 7 work. Required before full workflow coverage.

| Surface | UX Session | Notes |
|---|---|---|
| Remaining output card types (5 types) | Session 1 | Add after MVP loop proven |
| Return trigger review (full surface) | Session 13 | Partial works for MVP |
| Class C modal gate + typed confirmation | Session 10 | Required before launch readiness |
| Class D escalation banner | Session 10 | Required before edge governance work |
| Full session integrity overlay | Session 12 | Minimal version is MVP; full is enhancement |
| Full notification/toast system | Session 12 | Topbar badges are MVP; toasts are Tier 2 |
| Orchestration service + lower trace | Sessions 18, architecture | Required when delegation work begins |
| VEDA tree | Session 7 | Required when VEDA work begins |
| V Forge tree | Session 8 | Required when V Forge work begins |
| Context store ORCH + CONTINUITY rows live | Session 4 | Required when orchestration active |
| Component motion patterns | Session 23 | Static states are MVP; motion is Tier 2 |

### Tier 3 — Enhancements (Phase 9 scope)

Build after the core operator loop is proven and stable.

| Surface | UX Session | Notes |
|---|---|---|
| Launch readiness surface | Session 14 | Required for launch workflow |
| Maintenance/ranking surface | Session 15 | Required for maintenance workflow |
| Portfolio triage view | Session 17 | Multi-project capability |
| Command palette | Session 21 | Keyboard-first; nav tree is sufficient for MVP |
| Full visual language polish | Session 22 | Tokens are MVP; full polish is Tier 3 |
| Panel resize behavior (full spec) | Session 23 | Basic resize is MVP; full snap/spring is Tier 3 |

### Tier 4 — Schema-Unblocked When Schema Settles

Build when schema conditions are met.

| Surface | UX Session | Unblock Condition |
|---|---|---|
| Intake UX | Session 16 | IntakeRecord schema defined |
| Decision continuity timeline | Session 19 | DecisionRecord superseded-by linkage + `invalidated` status |
| Evidence freshness / signal views | Session 20 | VEDA SignalPackage / EvidenceRecord schema defined |

---

## 6. The Minimum Viable Operator Loop — Acceptance Criteria

The MVP is complete when the following sequence works end-to-end against a real backend with real data:

**Setup:** A Project V project with at least one handoff in `awaiting approval` state. An approval request package for that handoff has been generated and is in the right panel output area.

**Test sequence:**

1. **Application opens** → topbar shows correct project name, `V: Project V` system, `Handoff — Awaiting Approval` stage, amber `⊕` pending approval badge → **PASS**

2. **Context strip loaded** → all 9 rows visible with real data; SCOPE shows project ID; STAGE shows `Handoff — Awaiting Approval`; INTEGRITY shows the pending approval item → **PASS**

3. **Left nav** → HANDOFFS section shows the target handoff with `awaiting approval` status badge → **PASS**

4. **Right panel** → ARP card is visible in output area; `[Proceed to Approval Gate]` CTA is present with amber border → **PASS**

5. **Click `[Proceed to Approval Gate]`** → center workspace opens the handoff record in a new tab; Actions section is active; gate widget is visible in inactive state; checkpoint list shows all checkpoints incomplete → **PASS**

6. **Navigate to Overview section** → wait 5 seconds; `Overview section reviewed` checkpoint transitions to `✓` → **PASS**

7. **Navigate to Evidence section** → wait 5 seconds; `Evidence basis reviewed` checkpoint transitions to `✓` → **PASS**

8. **Navigate to Decisions section (or expand DECISIONS in context strip)** → `Governing decisions reviewed` checkpoint transitions to `✓` → **PASS**

9. **Confirm no blocking gaps** → `No blocking gaps` checkpoint shows `✓` (or resolves when gaps are clear) → **PASS**

10. **Navigate to Actions section** → all checkpoints show `✓`; gate widget transitions from inactive to active with amber border glow; `[Approve]` button is fully active → **PASS**

11. **Click `[Approve]`** → button shows loading state briefly; post-approval confirmation appears: `✓ APPROVED — [timestamp] · Approval record written`; `[Proceed to Activation ›]` button appears → **PASS**

12. **Verify persistence** → approval record exists in the backend with correct fields (project ID, handoff ID, actor, timestamp, approval type) → **PASS**

13. **Left nav updates** → handoff status badge changes from `awaiting approval` to `handed off` → **PASS**

14. **Topbar badge updates** → `⊕` pending approval badge count decreases by 1 (or disappears if this was the only one) → **PASS**

**MVP is done when all 14 steps pass.**

---

## 7. Schema-Blocked Items — Living Document Update

This is the final update to the schema-blocked items tracker as of the completion of the UX work plan.

| Item | Blocked On | Current Status | What Resolves It |
|---|---|---|---|
| Session 16 — Intake UX | `IntakeRecord` / `IntakeCandidate` schema not defined | **BLOCKED** | Define IntakeRecord with id, projectId, title, status, entityType/entityId linkage. Add to `schema-specification.md`. Update controlled vocabularies with intake status values. |
| Session 19 — Decision Continuity Timeline | `DecisionRecord` schema exists but missing `supersededBy` linkage and `invalidated` status | **BLOCKED** | Add `supersededBy uuid null references DecisionRecord(id)` column. Add `invalidated` to decision record status vocabulary. Define the three-way status (`recorded` / `superseded` / `invalidated`) with distinct semantics. |
| Session 20 — Evidence Freshness / Signal Views | VEDA `SignalPackage` / `EvidenceRecord` not defined; GA4 observations deferred | **BLOCKED** | Govern the VEDA SignalPackage family: define what a packaged evidence set looks like for operator consumption. Separately: govern GA4Observation family. Both require explicit governance decisions and additions to `veda/schema-reference.md`. |
| Sessions 13, 14, 15 — Partial schema blocks | `MaintenanceRecord`, `ReplanningRecord` stage anchors missing; three launch readiness stages runtime-derived | **PARTIAL BLOCK** | Settle the maintenance vs replanning record distinction. Anchor launch readiness stages to governed record fields rather than runtime workflow derivation. These partial blocks do not prevent building the surfaces — they affect the `*` notation treatment and block certain checkpoint conditions from being record-verified rather than operator-attested. |

**When any of these conditions is resolved:**
1. Update `v-ecosystem-desktop-ux-work-plan.md` schema-blocked items tracker
2. Move the corresponding session from BLOCKED/HOLD to the active queue
3. Run the UX session using the newly stable schema as the design input
4. Update the build sequence above to include the newly unblocked surface in its appropriate tier

---

## 8. What the Complete UX Work Produced

For the record — the complete output of sessions 1–24:

**TIER 1 (Sessions 1–2):** Output card system (7 types, all states, staleness markers) + minimal token decisions (the working design system baseline).

**TIER 2 (Sessions 3–9):** Full shell backbone — topbar, context strip, right panel shell, left nav shell, all three system trees, center workspace foundation.

**TIER 3 (Sessions 10–12):** Complete gate surface set (Class B/C/D), review-to-gate routing (the canonical 5-step governance path), session integrity system.

**TIER 4 (Sessions 13–15; 16 blocked):** Core workflow surfaces — handoff review, return trigger review, launch readiness, maintenance/ranking. Intake blocked pending schema.

**TIER 5 (Sessions 17–18, 21; 19–20 blocked):** Power features — portfolio triage, lower trace, command palette. Decision timeline and evidence freshness blocked pending schema.

**TIER 6 (Sessions 22–23):** Full Bricks-inspired visual language (the production CSS design system) + complete component behavior patterns (motion, transitions, states).

**TIER 7 (Session 24):** This document.

**Total: 21 complete sessions, 3 schema-blocked sessions held, 4 sessions with partial schema blocks that are buildable to the known boundary.**

The complete specified surface area covers: every governance surface, every shell surface, every workflow surface that has a settled schema anchor, the full visual design system, the complete behavior pattern vocabulary, and a concrete build sequence with MVP acceptance criteria.

---

## 9. What Comes After Session 24

Session 24 is the final session in the UX work plan. The next work is engineering's.

**Immediately actionable for engineering:**
- Phases 1–6 have no schema dependencies. The MVP critical tier can begin today.
- The CSS token file (Session 22 §13) is the first deliverable — one file, paste into `styles/tokens.css`, done.
- The Tauri shell (Session 3 + 5 + 6 + 9 spatial constants) can be scaffolded immediately.

**What engineering needs before starting:**
- The complete session spec files (Sessions 3–23 in `C:\dev\v-ecosystem-docs\ux\desktop\direction\`)
- The Session 22 final token reference (§13) as the CSS file
- The `desktop-implementation-architecture.md` doctrine doc (the phase structure engineering implements)
- The `desktop-invalidation-and-refresh-matrix.md` for `refreshCoordinator` event handling
- The `desktop-governance-and-gating-model.md` for action class enforcement in the approval pipeline

**When schema-blocked items resolve:** Run the corresponding UX session using this document's unblock conditions (§7), then add the resulting surface to the build sequence at the appropriate tier.

**When the MVP loop passes acceptance criteria (§6):** The application supports real governance work. Layer in Tier 2 surfaces in order of the workflow stages the team is actively using. Tier 3 enhancements follow.
