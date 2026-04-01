# V Ecosystem Docs

## Purpose

This directory is the **authoritative documentation root** for the V Ecosystem.

It defines:
- system roles
- boundaries
- workflows
- interfaces
- governance
- onboarding
- extension runtime doctrine

The goal is:

> If only these docs existed, a capable LLM should be able to reconstruct the V Ecosystem correctly.

---

## Authority Model

### Ecosystem Authority
Docs that define cross-system behavior and rules.

### Project Authority
Docs that define the core role and behavior of:
- Project V
- VEDA
- V Forge

### Extension Runtime Authority
Docs under `interfaces/` that define the governed VS Code extension, including:
- behavior contract
- gating and approval posture
- state and context visibility
- human–LLM interaction
- VS Code surface architecture
- implementation architecture
- agent orchestration
- memory and continuity
- system init and tool-surface posture

### Archive
Docs that are:
- historical
- bootstrap-era
- superseded

Archive docs are **not authority**.

---

## Folder Overview

### ecosystem
Top-level ecosystem rules, boundaries, and cooperation model.

### project-v
Authoritative Project V planning and doctrine.

### veda
Authoritative VEDA planning and doctrine.

### v-forge
Authoritative V Forge planning and doctrine.

### interfaces
Cross-system interfaces, extension/runtime doctrine, and operator-surface architecture.

### governance
Approvals, reporting, agent rules, and control.

### workflows
End-to-end system workflows.

### strategy
Scoring, evaluation, and long-term direction.

### onboarding
How new projects join the ecosystem.

### archive
Non-authoritative historical material.

---

## Core Rule

Every document should answer:

- What does this enable?
- What decisions does this support?
- What behavior does this constrain?
- What system or runtime layer does this belong to?
- How will it be used?

If it does not affect behavior, it is not needed.
