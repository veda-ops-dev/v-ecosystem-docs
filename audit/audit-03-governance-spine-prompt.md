# Audit 03 — Governance Spine Audit Prompt

Use this prompt for the third Claude audit pass.

---

You are performing a **Governance Spine Audit** of the V Ecosystem docs.

Use the audit posture below and follow it strictly.

[PASTE THE FULL CONTENTS OF `audit-posture.md` HERE]

---

## Audit goal

I want you to audit whether the **governance docs** actually function as a coherent enforcement spine for the V Ecosystem.

This is the layer that should constrain:
- agent behavior
- approvals and escalation
- evidence continuity
- decision continuity
- reporting posture
- failure and recovery posture
- testing and verification posture
- external action posture
- invalidation and supersedence posture

This is **not** the ecosystem foundation audit anymore.
This is **not** the deep Project V / VEDA / V Forge audit yet.
This is the governance-law audit.

Stay focused on:
- internal governance coherence
- enforceability
- overlap vs separation
- approval/continuity/failure/reporting alignment
- whether the governance spine is actually load-bearing
- whether a capable LLM could follow and enforce it without guessing

Do not drift into detailed system redesign.
Do not treat implementation companions as part of this layer unless a governance doc explicitly depends on them.

---

## Audit target

Review the governance cluster as one enforcement spine:

- `governance/agent-operating-doctrine.md`
- `governance/allowed-agent-actions-matrix.md`
- `governance/approval-and-escalation-model.md`
- `governance/auth-and-actor-model.md`
- `governance/daily-report-doctrine.md`
- `governance/decision-continuity-doctrine.md`
- `governance/evidence-continuity-model.md`
- `governance/external-action-governance.md`
- `governance/failure-and-recovery-doctrine.md`
- `governance/invalidation-and-supersedence-doctrine.md`
- `governance/paid-data-pull-governance.md`
- `governance/recommendation-packaging-doctrine.md`
- `governance/report-structure-and-required-fields.md`
- `governance/testing-and-verification-doctrine.md`

You are not auditing every downstream system doc yet.
You are auditing whether this governance cluster provides a strong enough cross-system enforcement law that the rest of the corpus can rely on it.

---

## Core questions

Answer these with specifics:

1. Do the governance docs form a coherent enforcement spine, or do they feel like adjacent policy docs without a strong center?
2. Are the governance docs mutually consistent in approval posture, evidence posture, continuity posture, reporting posture, and failure posture?
3. Are any governance docs duplicating each other or carrying unclear responsibility boundaries?
4. Does the governance layer clearly distinguish:
   - recommendation vs decision
   - evidence vs continuity artifact
   - approval vs authorization
   - failure handling vs replanning
   - reportability vs canonical authority
5. Are the governance docs strong enough that a capable LLM could avoid hidden-governance drift while operating or implementing the ecosystem?
6. Are any important governance terms underdefined, multiply defined, or used inconsistently across the cluster?
7. Is there any governance-law gap that would confuse later system audits or implementation work?
8. Which governance docs are the strongest, and which are underperforming their role?

---

## What I want from you

Organize your answer exactly like this:

# 1. Direct judgment

Give a blunt judgment on the governance spine.
Examples:
- strong and load-bearing
- mostly coherent with bounded cleanup needed
- conceptually good but enforcement-fragmented
- or whatever you think is accurate

Explain briefly.

# 2. Governance-spine coherence audit

Assess whether the governance docs work together as one real enforcement layer.
Call out:
- strongest docs
- weakest docs
- any doc that is underperforming its role
- whether the layer feels centralized enough to govern the ecosystem

# 3. Approval / authority / actor audit

Audit how the governance cluster handles:
- approval classes
- escalation
- actor legitimacy
- allowed actions
- external action control

I want to know whether this part of the spine is coherent and enforceable.

# 4. Continuity / evidence / reporting audit

Audit how the governance cluster handles:
- evidence continuity
- decision continuity
- invalidation and supersedence
- daily reporting
- report structure
- recommendation packaging

Call out overlaps, gaps, or confusing seams.

# 5. Failure / verification audit

Audit how the governance cluster handles:
- failure classification and response
- recovery posture
- testing and verification
- hammer posture
- whether failure and verification are linked correctly to the rest of governance

# 6. Vocabulary / term-discipline audit

Call out any governance terms that are:
- underdefined
- multiply defined
- used inconsistently
- likely to confuse an LLM or implementer

Only call out real issues.

# 7. Bounded fixes

Split into:

## Fix now
Real governance-spine issues worth correcting immediately.

## Fix later
Real but lower-priority improvements.

## Leave alone
Things that may look imperfect but are functioning correctly.

# 8. Final verdict

End by answering:

> Is the governance spine strong enough for the system-specific and runtime audits to proceed cleanly?

Then answer:
- yes
- yes, with small cleanup first
- no

And explain why in a short final paragraph.

---

## Important constraints

- This is not the ecosystem-foundation audit anymore.
- This is not the deep Project V / VEDA / V Forge audit yet.
- Do not ask for giant rewrites.
- Do not collapse governance docs and ecosystem docs into one layer.
- Do not drift into implementation-companion detail unless a governance doc truly depends on it.
- Do not invent doctrine gaps unless they are real and consequential.
- Prefer bounded fixes over structural churn.

I want a sharp governance-spine audit, not a policy summary.
