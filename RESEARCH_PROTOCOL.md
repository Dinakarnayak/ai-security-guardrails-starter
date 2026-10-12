# Research Protocol: Evaluating Local AI Guardrails

## Status and claim boundary

This repository is an educational research prototype, not a clinically validated system. “PhD-level” describes the intended rigour of the research process, not an achieved degree, peer-reviewed result, or evidence that the controls are safe. Current benchmark examples are synthetic and illustrative.

## Research question

How do deterministic input and output guardrails trade off risk detection, false-positive burden, category-level coverage, and local inference overhead around a small quantized language model?

## Hypotheses to test

- H1: Input controls reduce policy-defined risky prompts reaching generation compared with an unguarded baseline.
- H2: Output validation reduces configured unsafe response patterns reaching the user compared with raw model output.
- H3: Broader rules improve recall at the cost of more false positives.
- H4: Guardrail overhead is measurable and should be reported separately from generation latency.

These are hypotheses, not results.

## Experimental conditions

Evaluate at least these conditions on the same frozen cases:

1. Baseline: no input or output guardrail, using offline replay only.
2. Input only: input inspection before model invocation.
3. Output only: output validation after generation.
4. Layered: input inspection and output validation.
5. Ablation: remove one rule family at a time (urgent symptoms, privacy, prompt injection, medication requests, unsafe dosage, diagnosis assertion).

Keep model checksum, quantisation, inference parameters, Python version, hardware, prompt template, and test-set version fixed and record them.

## Dataset design

The checked-in evaluation/cases.jsonl is a smoke-test set, not a research benchmark. A defensible study needs a larger, independently labelled set containing benign, risky, ambiguous, misspelled, multilingual, and paraphrased examples. Record category, stage, expected action, severity and provenance. Use no real patient data or private conversations. Keep a held-out test split that is not used to tune rules, document annotation guidance, and adjudicate disagreements.

Avoid using synthetic examples alone to support generalisation claims. Do not collect or release personal health information without necessary ethical, legal and governance approvals.

## Metrics

Report sample count and class prevalence with exact action and category accuracy, precision, recall, false-positive rate, false-negative rate, category-level confusion counts and uncertainty intervals. For model-backed runs, measure p50/p95 latency, throughput and peak memory. Break results down by perturbation type and severity.

The included evaluator reports deterministic policy metrics. Its labels are illustrative and require independent review. A zero false-negative count on a small set does not establish zero real-world risk.

## Statistical reporting

Pre-register primary metrics and acceptance thresholds. For proportions, report confidence intervals (e.g. Wilson intervals); use paired comparisons on identical examples for ablations and report effect sizes. If multiple configurations are tuned, reserve a held-out set and disclose the selection procedure. Do not infer clinical outcomes from pattern-match metrics.

## Reproducibility checklist

- [ ] Record commit SHA and dataset version/hash.
- [ ] Record Python, OS, hardware and dependency versions.
- [ ] Record model name, licence, quantisation and SHA-256 checksum.
- [ ] Fix random seeds where applicable and report nondeterminism.
- [ ] Keep raw outputs only in a controlled, consented research setting; default audit logging is designed to store hashes/metadata.
- [ ] Run unit tests and evaluation from a clean environment.
- [ ] Publish failures, false positives, false negatives and limitations.

## Ethics, safety and governance

This healthcare scenario is for safety-engineering education only. Do not use the prototype to diagnose, triage, prescribe, or make patient-care decisions. Urgent-symptom phrase matching is not clinical triage. Pattern rules can be bypassed by paraphrases, misspellings, languages and context; they can also block benign content. Local inference reduces transfer to cloud services but does not itself establish privacy, correctness, or regulatory compliance.

Any human-subject study or use of real clinical data requires appropriate institutional ethics review, consent and data-protection governance before collection or analysis.
