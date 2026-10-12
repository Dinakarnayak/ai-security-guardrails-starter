# MSc-level design and evaluation notes

## System boundary

The local GGUF model is an untrusted component. Guardrails run before and after
generation; they enforce a policy but cannot make clinical decisions.

| Layer | Control | Risk addressed | Limitation |
| --- | --- | --- | --- |
| Governance | System prompt | Role drift | A model can ignore it |
| Input | Urgent-symptom escalation | Delayed emergency action | Phrase matching is not triage |
| Input | Medication, privacy, injection filters | Harmful advice, data disclosure, policy override | New wording can bypass patterns |
| Output | Dose and diagnosis validation | Unsafe advice reaching a user | Paraphrases can evade rules |
| Accountability | Hashed local audit events | Evidence without storing raw content | Metadata still needs retention controls |

## Risk policy

`ALLOW` has score 0. `BLOCK` and `REPLACE` have score 70. `ESCALATE` has score
100 and takes priority over every other input rule. The scores express policy
priority, not a clinical probability.

## Evaluation approach

Run `py -3.11 app.py --self-test` for representative cases. A real evaluation
would use a separately maintained labelled test set including benign,
adversarial, ambiguous, and misspelled prompts. Report false positives and
false negatives by category, then review harmful misses with experts.

## Governance limitation

This prototype must not be deployed for patient care. It has no clinical
knowledge verification, consent workflow, identity assurance, or human review.
Local inference reduces cloud data transfer; it does not make output correct.
