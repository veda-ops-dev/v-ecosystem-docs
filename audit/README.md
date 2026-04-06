# V Ecosystem Docs Audit

This folder contains prompt templates for structured doc auditing passes.

Each pass targets a specific class of doc quality problem. Run them in order. Each pass assumes the previous pass has been completed.

## Passes

| File | Pass | Scope | Sessions |
|---|---|---|---|
| `pass-1-structural-integrity.md` | Structural Integrity | Full repo | 1 |
| `pass-2-vocabulary-consistency.md` | Vocabulary & Term Consistency | Per system | 3–4 |
| `pass-3-interface-completeness.md` | Interface Completeness | Per interface doc | 1 per doc |
| `pass-4-workflow-codability.md` | Workflow Codability | Per workflow doc | 1 per doc |
| `pass-5-cross-system-consistency.md` | Cross-System Consistency | System pairs | 2–3 |

## How to use

Load the relevant prompt template into a Claude session with MCP filesystem access to `C:\dev\v-ecosystem-docs`.

Follow the instructions in the template. Each template tells you exactly what to load, what to check, and what output to produce.

Do not skip passes. Pass 1 catches structural problems that would corrupt later passes if left unfixed.

## Authority

These audit templates are Tier 3 implementation-support material. They do not override doc content. They surface problems for human review and decision.
