# Pass 2 Findings — Vocabulary & Term Consistency

Session: C
Folders audited: `veda/`
Date: 2026-04-05

---

### Files loaded

- `veda/veda.md`
- `veda/system-invariants.md`
- `veda/observability-and-signal-role.md`
- `veda/data-boundaries.md`
- `veda/evidence-and-source-provenance.md`
- `veda/observatory-models.md`
- `veda/schema-reference.md`
- `veda/search-intelligence-layer.md`
- `veda/api-contract-principles.md`
- `veda/validation-and-error-taxonomy.md`
- `veda/mcp-surface.md`
- `veda/operator-surfaces.md`
- `veda/providers/registry.md`
- `veda/decisions/VEDA-001-youtube-observatory-truth-surface.md`
- `ecosystem/vocabulary.md` (canonical reference)
- `audit/findings-pass-1.md` (exclusion check)

### Files excluded based on Pass 1

None found. No `veda/` docs were flagged as stubs, archive material, or self-declared superseded in Pass 1 findings.

---

### Undefined load-bearing terms

None found.

---

### Near-synonym sprawl

**Term pair: `append-friendly` vs `append-only` applied to EventLog**

| Attribute | Value |
|---|---|
| Terms | `append-friendly` / `append-only` |
| Locations | `system-invariants.md` (Invariant 8) uses `append-friendly` for event logs; `schema-reference.md` (EventLog family) and `observatory-models.md` (Category 3) both use `append-only` for the same EventLog record |
| Canonical term | `append-only` — used by both `schema-reference.md` and `observatory-models.md`, each of which defines the EventLog contract explicitly as "no updates, no deletes" |
| Intentional? | N |
| Short note | `append-friendly` and `append-only` are not interchangeable. `append-only` means strictly no updates and no deletes. `append-friendly` means new observations add new rows, but does not rule out all mutation — `SERPSnapshot` and `SearchPerformance` are explicitly `append-friendly` while allowing some write patterns (e.g. re-ingesting a performance window). `system-invariants.md` groups event logs with snapshot records under `append-friendly`, while the two implementation-spec docs that govern the EventLog table directly both specify `append-only`. An implementer reading `system-invariants.md` alone would conclude that EventLog tolerates the same mutation flexibility as `SERPSnapshot`; that conclusion would conflict with the contract defined in `schema-reference.md`. |
| Evidence quote | `system-invariants.md` Invariant 8: "observation records, such as snapshot captures, performance captures, and event logs, are append-friendly and must not have their historical state silently overwritten"; `schema-reference.md` EventLog: "this table is append-only: no updates, no deletes"; `observatory-models.md` Category 3: "strictly append-only: no updates, no deletes" |

---

### Canonical terms used incorrectly

None found.

---

### Vague references

None found.

---

### Capitalization inconsistencies

None found.

`VEDA`, `Project V`, and `V Forge` are consistently capitalized throughout all `veda/` docs.

---

### Summary

`veda/` vocabulary is exceptionally well-maintained. The docs define their domain-specific terms inline (`compute-on-read`, signal type names, governance record vs observation record, append-friendly vs append-only) and use canonical ecosystem terms consistently. The one finding — the `append-friendly` / `append-only` inconsistency for EventLog in `system-invariants.md` — is meaningful because `system-invariants.md` is a Tier 2 core authority doc whose characterization of EventLog conflicts with the implementation-spec docs that define the table. The resolution is clear from the weight of evidence: EventLog is `append-only`, and `system-invariants.md` should not group it with the genuinely `append-friendly` observation ledger records.

---

### Out-of-scope observations not included in findings

- `operator-surfaces.md` and `mcp-surface.md` both refer to "the VSCode extension" as the operator surface. This is the same stale host reference found in Sessions A and B. Not re-flagged here.
- `providers/registry.md` records that no providers have been formally admitted yet. This is a content gap, not a vocabulary finding — belongs in a later pass if relevant.
