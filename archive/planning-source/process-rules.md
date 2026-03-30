# Process Rules

## Purpose

This document captures load-bearing process rules for the V Ecosystem docs refoundation effort.

It exists to prevent execution drift, stale-memory writing, and false continuity while the new shared-root authority set is being built.

This is a temporary planning/process control document.
It may later be archived, superseded, or absorbed into more permanent governance doctrine if needed.

---

## Rule 1 — Shared-root drafting must stay source-grounded

Shared-root drafting must remain grounded in the source repos.

Do not continue writing from memory, momentum, or assumed continuity when relevant source docs already exist.

If the source repos contain load-bearing doctrine, testing rules, data posture, boundary rules, migration rules, or system-specific non-negotiables, those source docs must be treated as active source material for the refoundation pass.

The old repos are not the new authority home.
But they are still source truth inputs until the new shared-root authority set fully replaces them.

---

## Rule 2 — Re-read relevant source docs before drafting adjacent authority docs

Before drafting a new shared-root authority doc, re-read the relevant source docs for that topic.

This is especially required for topics involving:

- database posture
- hammer/testing doctrine
- auth and actor rules
- lifecycle and state models
- cross-system boundaries
- interfaces and handoffs
- schema and migration behavior
- system-specific invariants

Do not rely on memory of what the repos said.
Relevant source docs must be re-read before drafting or deciding adjacent authority docs.

---

## Rule 3 — Do not confuse prior conversation momentum with current source-grounded reality

A prior writing sequence, previous recommendation, or remembered plan step does not override newly re-read source material.

If a source repo doc reveals a load-bearing rule that was not active in the current conversation state, the drafting process must sync to that reality rather than continuing as though the rule does not exist.

Examples include:

- existing hammer doctrine being rediscovered
- existing DB boundary doctrine already being present in a source repo
- existing migration or schema rules that constrain a planned shared-root doc

Source-grounded correction is not drift.
Ignoring source-grounded correction is drift.

---

## Rule 4 — Source-grounded continuity beats memory continuity

The goal is not to preserve the illusion of uninterrupted momentum.
The goal is to preserve accurate continuity.

Accurate continuity means:

- reading what actually exists
- carrying forward what is load-bearing
- rewriting cleanly into the shared-root authority set
- avoiding omissions caused by stale memory

Do not optimize for smoothness over correctness.

---

## Rule 5 — Load-bearing source doctrine must be surfaced, not silently assumed

If a source repo contains a real doctrine layer that affects system behavior, it should be surfaced explicitly in the refoundation effort.

Do not leave it buried in the source repo while drafting adjacent shared-root docs as though it does not exist.

Examples include:

- hammer doctrine
- DB boundary doctrine
- schema authority doctrine
- system invariants
- auditability doctrine
- ingest discipline

Load-bearing source doctrine should either:

- be carried into the shared root directly
- be referenced in planning as a required source input
- or be explicitly marked as deferred but recognized

It must not be forgotten by omission.

---

## Rule 6 — Keep the execution plan and working process synced to discovered source truth

When a newly re-read source doc materially changes the drafting context, planning context, or dependency order, update the working process and execution planning accordingly.

Do not let the refoundation continue from stale assumptions once better-grounded source reality is known.

---

## Final Rule

Read the repos continuously.
Not once.
Not from memory.
Not by vibe.

Relevant source docs must be re-read before drafting adjacent shared-root authority docs so the V Ecosystem refoundation stays accurate, bounded, and grounded in real source truth.
