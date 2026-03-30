# VEDA-001: YouTube Observatory Truth Surface

## Status

Accepted — future implementation only.
This decision preserves the architectural choice for when YouTube observatory
work is promoted from deferred to active planning.
It does not authorize implementation now.

---

## Context

VEDA includes YouTube as an observatory domain. A YouTube lens requires a
declared primary truth surface before it can be designed responsibly.

The core question is: what instrument should VEDA treat as the primary source
of YouTube search/discovery snapshots?

Three candidates were evaluated:
- raw YouTube UI
- official YouTube Data API
- vendor SERP source (e.g. DataForSEO)

No single instrument satisfies all observatory needs. The correct architecture
assigns different roles to different instruments.

---

## Decision

**Primary snapshot instrument:** vendor SERP source
**Secondary enrichment instrument:** YouTube Data API
**Validation instrument:** manual/UI spot checks

In one sentence:

> Use vendor snapshots to observe the discovery surface, use the official API
> to enrich the observed objects, and use UI checks to validate that the
> telescope is still pointed at the real sky.

---

## Instrument Role Assignments

### Vendor SERP source — primary snapshot role
Captures: query snapshots, ordered block composition, typed element capture,
visible prominence, result-type share, block presence tracking.

### YouTube Data API — enrichment role
Provides: stable identifiers, video/channel metadata, category data,
publish dates, statistics snapshots, durable object references.

### Manual/UI review — validation role
Used for: spot checks, drift review, unusual query debugging, validating
that vendor fidelity assumptions remain accurate.

---

## Why Vendor Primary

VEDA's aim is to observe a discovery surface, not merely collect metadata.
The vendor route best captures page composition, block structure, and ordered
result elements while remaining operationally practical.

UI-only: maximum fidelity but fragile, high compliance burden, not sustainable
as a primary architecture.
API-only: clean metadata model but may not match visible search surface;
risks producing a misleading observatory.

---

## Telescope Principle Alignment

This decision keeps VEDA within its telescope role.
The YouTube lens observes what the discovery ecosystem shows.
It does not manage creators, workflows, publishing, or execution.

---

## When This Decision Becomes Active

Before implementation begins, the YouTube observatory design must declare:
- primary truth surface (confirmed: vendor SERP source)
- enrichment source (confirmed: YouTube Data API)
- validation source (confirmed: UI spot checks)
- baseline lens definition
- ranking semantics derived from the snapshot model
- drift review expectations

---

## Related Docs

- `../veda.md`
- `../system-invariants.md`
- `../observability-and-signal-role.md`
- `../../ecosystem/external-provider-integration-doctrine.md`
- `../providers/registry.md`