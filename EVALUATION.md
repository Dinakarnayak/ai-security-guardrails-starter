# Design and Evaluation Notes

## System boundary

The local GGUF model is an untrusted component. Input controls run before generation and output validation runs after generation. The controls implement a small demonstrator policy; they cannot make clinical decisions or guarantee safety.

| Layer | Control | Risk addressed | Limitation |
| --- | --- | --- | --- |
| Governance | System prompt | Role drift | Model may ignore it |
| Input | Urgent-symptom escalation | Delay in seeking emergency help | Phrase matching is not triage |
| Input | Medication, privacy and injection filters | Personalised advice, disclosure, policy override | Paraphrases and unseen patterns can bypass rules |
| Output | Dose and diagnosis validation | Configured unsafe patterns reaching a user | Other unsafe formulations can evade rules |
| Accountability | Hashed local audit events | Demonstration traceability without storing raw text | Metadata and hashes still need retention controls |

## Risk policy

ALLOW has score 0. BLOCK and REPLACE have score 70. ESCALATE has score 100 and takes priority over other input rules. These are policy-priority values, not calibrated probabilities or clinical severity estimates.

## Reproducible checks

Run the following from the repository root with Python 3.11:

```powershell
py -3.11 app.py --self-test
py -3.11 -m unittest discover -s tests -v
py -3.11 evaluate_guardrails.py --output evaluation/results.json
```

The evaluator emits overall and stage-level metrics plus a list of mismatches. Inspect false negatives and false positives individually. Labels in the included synthetic smoke-test set require independent review; do not cite the resulting numbers as a benchmark or generalisable safety result.

## Research-grade next steps

Use [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md) to plan frozen baseline/input-only/output-only/layered conditions and rule ablations. Expand the dataset with independent annotation and a held-out split. Pre-register metrics, report confidence intervals and paired comparisons, record model/hardware/dependency versions, and publish limitations as well as failures.

## Governance limitation

This prototype must not be deployed for patient care. It has no clinical knowledge verification, consent workflow, identity assurance, expert review or validated emergency triage. Local inference reduces cloud data transfer; it does not make outputs correct or establish compliance.
