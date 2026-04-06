## Pass 2 Findings — Vocabulary & Term Consistency

Session: A
Folders audited: ecosystem, governance
Date: 2026-04-05

### Undefined load-bearing terms
- operator | governance docs across Session A | definition found? N | Used to drive allowed actions, approval behavior, reviewability, and runtime posture, but not defined in `ecosystem/vocabulary.md`.
- governance-sensitive | governance docs across Session A | definition found? N | Used to determine whether actions may proceed, require approval, or must escalate, but absent from canonical vocabulary.
- material / materiality | governance docs across Session A | definition found? N | Used to determine whether changes, uncertainty, or approval context are significant enough to alter behavior, but not canonically defined.
- scope excess | governance docs across Session A | definition found? N | Used as a behavioral boundary condition for escalation / refusal posture, but not defined in the loaded canonical vocabulary.
- task | ecosystem + governance docs across Session A | definition found? N | Appears in action vocab and runtime/governance behavior, but no canonical definition was found in the loaded set.

### Near-synonym sprawl
- activity record vs activity log entry | Session A docs discussing the activity trail | canonical term: activity record | intentional? N | Appears to refer to the same governed unit in the activity trail, creating avoidable terminology drift.
- meaningful vs material | `ecosystem/activity-trail-model.md` and governance docs such as `daily-report-doctrine.md` | canonical term not determinable from loaded docs | intentional? N | `daily-report-doctrine.md` partially distinguishes importance language, but `activity-trail-model.md` uses “meaningful action” as an unanchored threshold term that overlaps with “material” behavior elsewhere.

### Canonical terms used incorrectly
- governance-sensitive | `governance/agent-operating-doctrine.md` | Used with a behaviorally divergent meaning relative to `governance/approval-and-escalation-model.md`; one framing includes triggers such as paid actions and handoff activation while the other defines the class differently, creating consequential approval ambiguity.

### Vague references
- the current system | `governance/agent-operating-doctrine.md` | Ambiguous in a cross-system governance context because it leaves unclear whether the reference means the active runtime posture, the current ecosystem system, or the current document’s governing system.

### Capitalization inconsistencies
None found.

### Summary
Session A vocabulary health is mostly strong, but several load-bearing governance terms are operating without canonical anchors. The most urgent issues are the missing definitions for “operator” and “governance-sensitive,” plus the divergent use of “governance-sensitive” across governance docs because that affects approval and escalation behavior.

### Out-of-scope observations not included in findings
- None.
