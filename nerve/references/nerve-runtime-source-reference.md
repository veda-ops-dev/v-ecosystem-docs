# V Ecosystem — Claw-Code Source-Mapped Implementation Reference

**Type**: Planning artifact — code-grounded reference for implementation
**Source repo**: `claw-cli/claw-code-rust` (clean-room Rust decomposition of Claude Code agent harness)
**Date**: 2026-04-01

---

## How to read this document

Each section maps a V Ecosystem implementation need to **exact source code** in the claw-code-rust repo. Every struct, trait, and function referenced here exists and was read before writing this document.

The source tree structure:

```
claw-code-rust/crates/
  compact/src/    → budget.rs, strategy.rs
  core/src/       → message.rs, session.rs, query.rs, error.rs
  tools/src/      → tool.rs, context.rs, registry.rs, orchestrator.rs
  permissions/src/→ types.rs, policy.rs, rules.rs
  tasks/src/      → task.rs, manager.rs
  provider/src/   → provider.rs, request.rs, response.rs, anthropic.rs
  mcp/src/        → lib.rs (stub)
  claw-cli/src/   → main.rs, config.rs (product shell — skip)
```

---

## 1. Compaction Pipeline

### What V needs

A mechanism to keep long sessions within token budget without destroying governance constraints. The V extension doctrine (`extension-memory-and-continuity-model.md`) defines protected-context categories and compaction posture but has no implementation-grade design.

### Source code map

**Budget trigger** — `compact/src/budget.rs`

```rust
pub struct TokenBudget {
    pub context_window: usize,       // e.g. 200_000
    pub max_output_tokens: usize,    // e.g. 16_000
    pub compact_threshold: f64,      // e.g. 0.80
}
```

Key methods:
- `input_budget()` → `context_window - max_output_tokens` (available input tokens)
- `should_compact(current_tokens)` → fires when `current_tokens > input_budget * compact_threshold`

**V adaptation**: This struct needs one addition for V — a `protected_reserve: usize` field representing the token budget that protected context (governance constraints, project scope, system identity) permanently occupies. The compaction trigger should account for it: compaction fires when `current_tokens > (input_budget - protected_reserve) * compact_threshold`.

**Strategy trait** — `compact/src/strategy.rs`

```rust
#[async_trait]
pub trait CompactStrategy: Send + Sync {
    async fn compact(
        &self,
        messages: Vec<CompactMessage>,
        budget: usize,
    ) -> anyhow::Result<CompactResult>;
}
```

Where `CompactMessage` is `{ role, content, token_estimate }` and `CompactResult` is `{ messages, removed_count, tokens_saved }`.

The only shipped implementation is `TruncateStrategy` — drops oldest messages until under budget, keeping recent messages. It iterates from the end, accumulating until budget is exceeded.

**V adaptation**: V needs a `GovernedCompactStrategy` that:
1. Partitions messages into `protected` (flagged, never discarded) and `compactable`
2. Applies compaction only to the compactable set
3. Optionally summarizes (LLM call) rather than just truncating
4. Returns a `CompactResult` that also reports what protected context survived

The `CompactMessage` struct needs a `protected: bool` field. Alternatively, V can use a separate `ProtectedContextRegistry` that marks message indices as immune.

**Main loop integration** — `core/src/query.rs`, lines in the `loop {}` body

```rust
// Check token budget and compact before building the request
if session.last_input_tokens > 0
    && session.config.token_budget.should_compact(session.last_input_tokens)
{
    compact_session(session);
}
```

The `compact_session()` function (same file) is a simple in-place drainer — it calculates `avg_tokens_per_msg`, targets 70% of `input_budget`, and removes the oldest messages via `session.messages.drain(..remove_count)`.

**V adaptation**: Replace `compact_session()` with a call to the `GovernedCompactStrategy` trait. Before calling it, V must:
1. Run the pre-compaction memory flush (see §2)
2. Flag all protected messages
3. After compaction, re-validate that governance context survived

**Error-recovery compaction** — also in `query.rs`:

```rust
ErrorClass::ContextTooLong => {
    if context_compacted {
        return Err(AgentError::ContextTooLong);
    }
    compact_session(session);
    context_compacted = true;
    session.turn_count -= 1;
    continue;
}
```

This is the "overflow recovery" path — the API rejected the request, so compaction fires reactively. This is the dangerous path for V because it doesn't get a flush opportunity.

**V adaptation**: V should aim to never hit this path. If it does, V must log a governance warning and re-validate protected context after the emergency compaction.

---

## 2. Pre-Compaction Memory Flush

### What V needs

Before compaction discards older context, the agent must get a chance to write important working state to durable (non-authoritative) storage. Without this, compaction is pure destruction.

### Source code map

**No direct implementation exists in claw-code-rust.** The `compact_session()` function in `query.rs` directly drains messages with no flush step. However, the pattern is well-documented in the OpenClaw ecosystem (where it's called `runMemoryFlushIfNeeded`) and is referenced in the claw-code README's command list (`/compact`, `/memory`).

**Where it would go**: Between the `should_compact()` check and the `compact_session()` call in `query.rs`. The integration point is clear:

```rust
// V's version of the main loop compaction check:
if session.config.token_budget.should_compact(session.last_input_tokens) {
    // STEP 1: Memory flush — run a silent turn asking the agent to
    //         write important working state to durable memory files
    // STEP 2: Flag protected context
    // STEP 3: Compact
    // STEP 4: Re-validate governance constraints survived
}
```

**V adaptation**: V must define the flush as a governed action class. The flush agent may write to designated non-authoritative memory files only. It must not write decisions, approvals, or evidence. All flush artifacts must carry timestamps and `non-authoritative: true` labels. This is doctrine, not code — but the integration point in the code is the compaction check.

---

## 3. Tool Registry + Session-Scoped Filtering

### What V needs

Mechanical enforcement of absent-affordance doctrine — the LLM must only see tools it is currently entitled to use, filtered by current system, scope, and action posture.

### Source code map

**Tool trait** — `tools/src/tool.rs`

```rust
#[async_trait]
pub trait Tool: Send + Sync {
    fn name(&self) -> &str;
    fn description(&self) -> &str;
    fn input_schema(&self) -> serde_json::Value;
    async fn execute(&self, ctx: &ToolContext, input: serde_json::Value) -> Result<ToolOutput>;
    fn is_read_only(&self) -> bool { false }
    fn supports_concurrency(&self) -> bool { self.is_read_only() }
}
```

**V adaptation**: Add to the `Tool` trait:
- `fn owning_system(&self) -> &str` — which V system this tool belongs to (project-v, veda, v-forge, ecosystem)
- `fn required_scope(&self) -> Option<&str>` — what project scope is required (if any)
- `fn action_class(&self) -> ActionClass` — maps to the `allowed-agent-actions-matrix.md` categories

**Tool context** — `tools/src/context.rs`

```rust
pub struct ToolContext {
    pub cwd: PathBuf,
    pub permissions: Arc<dyn PermissionPolicy>,
    pub session_id: String,
}
```

**V adaptation**: Extend to:

```
pub struct VToolContext {
    pub cwd: PathBuf,
    pub permissions: Arc<dyn PermissionPolicy>,
    pub session_id: String,
    pub active_system: String,          // "project-v" | "veda" | "v-forge"
    pub active_project_scope: String,   // project token
    pub operator_id: String,            // for attribution
}
```

**Registry** — `tools/src/registry.rs`

```rust
pub struct ToolRegistry {
    tools: HashMap<String, Arc<dyn Tool>>,
}
```

Methods: `register()`, `get()`, `all()`, `tool_definitions()`.

**V adaptation**: Add a `filtered_definitions()` method:

```
pub fn filtered_definitions(
    &self,
    active_system: &str,
    active_scope: &str,
    action_posture: &ActionPosture,
) -> Vec<ToolDefinition>
```

This is the absent-affordance enforcement point. Only tools that match the current system, have compatible scope requirements, and are allowed by the current action posture should appear in the model's tool list. Tools that don't match are structurally absent — the LLM never sees them.

**Orchestrator** — `tools/src/orchestrator.rs`

```rust
pub struct ToolOrchestrator {
    registry: Arc<ToolRegistry>,
}
```

Key method: `execute_batch()` partitions calls into concurrent (read-only) and sequential (mutating), runs permission checks on mutating tools, wraps errors.

The permission check path:

```rust
if !tool.is_read_only() {
    let request = PermissionRequest {
        tool_name: call.name.clone(),
        resource: ResourceKind::Custom(call.name.clone()),
        description: format!("execute tool {}", call.name),
        target: None,
    };
    match ctx.permissions.check(&request).await {
        PermissionDecision::Allow => {},
        PermissionDecision::Deny { reason } => { /* return error */ },
        PermissionDecision::Ask { message } => { /* return error for now */ },
    }
}
```

**V adaptation**: V's orchestrator must also check:
1. Tool's `owning_system()` matches `active_system` (or is cross-system read-only)
2. Tool's `required_scope()` matches `active_project_scope`
3. Tool's `action_class()` is permitted by the current action posture

These are additional filters beyond the permission policy. They enforce system boundaries at the execution level, not just the visibility level.

---

## 4. Permission Policy Layer

### What V needs

Mechanical enforcement of the agent-operating-doctrine and allowed-agent-actions-matrix at runtime.

### Source code map

**Types** — `permissions/src/types.rs`

```rust
pub enum PermissionMode { AutoApprove, Interactive, Deny }
pub enum ResourceKind { FileRead, FileWrite, ShellExec, Network, Custom(String) }
pub struct PermissionRequest { tool_name, resource, description, target }
pub enum PermissionDecision { Allow, Deny { reason }, Ask { message } }
```

**V adaptation**: Extend `ResourceKind` with V-specific variants:

```
pub enum ResourceKind {
    // ... existing
    ProjectVRead,
    ProjectVWrite,
    VedaRead,
    VedaSignalIngest,
    VForgeRead,
    VForgeExecute,
    VForgeApprovalRequired,
    CrossSystemReference,
}
```

**Policy trait** — `permissions/src/policy.rs`

```rust
#[async_trait]
pub trait PermissionPolicy: Send + Sync {
    async fn check(&self, request: &PermissionRequest) -> PermissionDecision;
}
```

This is clean and directly reusable. V implements this trait with a `VGovernedPolicy` that consults the allowed-agent-actions-matrix, the approval-and-escalation-model, and the current session posture.

**Rule matching** — `permissions/src/rules.rs`

```rust
pub struct RuleBasedPolicy {
    pub mode: PermissionMode,
    pub rules: Vec<PermissionRule>,
}
```

`match_rule()` does glob/prefix matching. `check()` tries rules first, falls back to mode.

**V adaptation**: V needs richer rule matching — per-system rules, per-project-scope rules, and temporal rules (some actions only allowed during active execution phases). The `RuleBasedPolicy` pattern is a starting point but V's policy will be more complex.

---

## 5. Token/Cost Tracking

### What V needs

Operator visibility into token consumption, session cost, context fill percentage.

### Source code map

**Session state counters** — `core/src/session.rs`

```rust
pub struct SessionState {
    // ...
    pub total_input_tokens: usize,
    pub total_output_tokens: usize,
    pub total_cache_creation_tokens: usize,
    pub total_cache_read_tokens: usize,
    pub last_input_tokens: usize,      // most recent turn's input tokens
}
```

**Accumulation** — `core/src/query.rs`, in the `MessageDone` stream event handler:

```rust
session.total_input_tokens += response.usage.input_tokens;
session.total_output_tokens += response.usage.output_tokens;
session.total_cache_creation_tokens +=
    response.usage.cache_creation_input_tokens.unwrap_or(0);
session.total_cache_read_tokens +=
    response.usage.cache_read_input_tokens.unwrap_or(0);
session.last_input_tokens = response.usage.input_tokens;
```

And the event emission:

```rust
emit(QueryEvent::Usage {
    input_tokens: response.usage.input_tokens,
    output_tokens: response.usage.output_tokens,
    cache_creation_input_tokens: response.usage.cache_creation_input_tokens,
    cache_read_input_tokens: response.usage.cache_read_input_tokens,
});
```

**V adaptation**: Directly reusable. Add a `context_fill_pct()` method to `SessionState`:

```
pub fn context_fill_pct(&self) -> f64 {
    if self.last_input_tokens == 0 { return 0.0; }
    self.last_input_tokens as f64 / self.config.token_budget.input_budget() as f64
}
```

Expose this in the operator surface and optionally inject into the runtime line of the system prompt so the LLM has passive context awareness.

---

## 6. System-Init Assembly

### What V needs

Deliberate construction of the system prompt from multiple governed sources, not ad-hoc stuffing.

### Source code map

**Memory prefetch** — `core/src/query.rs`

```rust
fn load_claude_md(cwd: &Path) -> Option<String> {
    let path = cwd.join("CLAUDE.md");
    std::fs::read_to_string(path).ok().filter(|s| !s.is_empty())
}

fn build_system_prompt(base: &str, memory: &Option<String>) -> String {
    match (base.is_empty(), memory) {
        (true, Some(mem)) => mem.clone(),
        (false, Some(mem)) => format!("{}\n\n{}", base, mem),
        _ => base.to_string(),
    }
}
```

Called once before the loop: `let memory_content = load_claude_md(&session.cwd);`

Then per-turn: `let system = build_system_prompt(&session.config.system_prompt, &memory_content);`

**V adaptation**: This is the weakest part of claw-code for V's purposes. V needs a `SystemInitAssembler` that:

1. Loads the core system identity (static, from extension config)
2. Loads the active project scope token and its constraints (from session state)
3. Loads the current-system identity (project-v, veda, v-forge)
4. Loads the active governance constraints (from the allowed-agent-actions matrix)
5. Loads the active tool surface definition (from filtered registry)
6. Loads durable memory files (with truncation limits and freshness checks)
7. Loads the runtime line (model, context fill %, permissions mode)
8. Assembles all sources in defined order with character/token limits per source

The `build_system_prompt()` two-string concatenation is a pattern starting point, but V's assembler is a multi-source, ordered, budget-aware pipeline. Each source has a priority and a max-token allocation. If the total exceeds the system-prompt budget, lower-priority sources are truncated first.

---

## 7. Session State Container

### What V needs

A non-authoritative container for turn-by-turn LLM interaction state, carrying project-scope binding.

### Source code map

**Session config** — `core/src/session.rs`

```rust
pub struct SessionConfig {
    pub model: String,
    pub system_prompt: String,
    pub max_turns: usize,
    pub token_budget: TokenBudget,
    pub permission_mode: PermissionMode,
}
```

**Session state** — same file:

```rust
pub struct SessionState {
    pub id: String,
    pub config: SessionConfig,
    pub messages: Vec<Message>,
    pub cwd: PathBuf,
    pub turn_count: usize,
    // ... token counters
}
```

**V adaptation**: Extend with V-specific fields:

```
pub struct VSessionState {
    // ... all existing fields
    pub active_system: String,
    pub project_scope_token: String,
    pub operator_id: String,
    pub protected_message_indices: HashSet<usize>,
    pub compaction_count: usize,
    pub last_compaction_at: Option<DateTime<Utc>>,
    pub governance_context_valid: bool,  // false after compaction until re-validated
}
```

The `governance_context_valid` flag is critical — after compaction, it flips to `false`. The next turn must re-validate that governance constraints are present in the context before proceeding. If re-validation fails, the session must either re-inject governance context or halt.

---

## 8. Task Lifecycle (V Forge execution support)

### What V needs

Background task tracking for long-running V Forge execution operations.

### Source code map

**Task state machine** — `tasks/src/task.rs`

```rust
pub enum TaskState { Pending, Running, Completed, Failed, Cancelled }

pub struct TaskInfo {
    pub id: String,
    pub name: String,
    pub state: TaskState,
    pub output: Option<String>,
    pub created_at: DateTime<Utc>,
    pub finished_at: Option<DateTime<Utc>>,
}
```

**Task manager** — `tasks/src/manager.rs`

```rust
pub struct TaskManager {
    tasks: Arc<RwLock<HashMap<String, TaskInfo>>>,
    notifications: Arc<RwLock<Vec<TaskNotification>>>,
}
```

Key methods: `register()`, `update_state()`, `set_output()`, `push_notification()`, `drain_notifications()`, `cancel()`.

The `drain_notifications()` pattern is clever — it collects all pending task notifications and clears the queue, allowing them to be injected into the next conversation turn.

**V adaptation**: V's task manager must enforce:
- Task outputs are `inert findings` — they carry attribution (`created_by: worker_id`) and are labeled `non-authoritative`
- Task state is non-canonical — it does not replace V Forge's canonical execution state
- Completed task outputs must go through the appropriate return-to-operator or return-to-planning interface, not be auto-promoted

Add to `TaskInfo`:

```
pub attribution: TaskAttribution,   // { worker_id, delegated_by, timestamp }
pub authority_class: AuthorityClass, // NonAuthoritative (always, for V)
```

---

## Summary: What to take, what to build, what to skip

| Claw-code component | Take as-is | Adapt for V | Build fresh for V | Skip |
|---|---|---|---|---|
| `TokenBudget` struct | | ✓ (add `protected_reserve`) | | |
| `CompactStrategy` trait | ✓ | | | |
| `TruncateStrategy` impl | | | ✓ (`GovernedCompactStrategy`) | |
| `compact_session()` in query.rs | | | ✓ (governed version with flush + protect + validate) | |
| `Tool` trait | | ✓ (add `owning_system`, `required_scope`, `action_class`) | | |
| `ToolContext` struct | | ✓ (add `active_system`, `project_scope`, `operator_id`) | | |
| `ToolRegistry` | | ✓ (add `filtered_definitions()`) | | |
| `ToolOrchestrator` | | ✓ (add system-boundary + scope checks) | | |
| `PermissionPolicy` trait | ✓ | | | |
| `PermissionMode` / `ResourceKind` | | ✓ (add V-specific resource kinds) | | |
| `RuleBasedPolicy` | | | ✓ (`VGovernedPolicy` — richer matching) | |
| `SessionState` counters | ✓ | | | |
| `QueryEvent::Usage` | ✓ | | | |
| `SessionConfig` / `SessionState` | | ✓ (add V-specific fields) | | |
| `build_system_prompt()` | | | ✓ (`SystemInitAssembler` — multi-source, ordered, budget-aware) | |
| `load_claude_md()` | | | ✓ (V's memory rehydration is richer) | |
| `TaskState` / `TaskInfo` | | ✓ (add attribution + authority class) | | |
| `TaskManager` | | ✓ (add governance labeling) | | |
| `Message` / `ContentBlock` / `Role` | ✓ | | | |
| Pre-compaction memory flush | | | ✓ (not implemented in source) | |
| Plugin/hook system | | | | ✓ |
| CLI REPL / main.rs | | | | ✓ |
| Provider abstraction | | | | ✓ |
| LSP / Server / Compat | | | | ✓ |
