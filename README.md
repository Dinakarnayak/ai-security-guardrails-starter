# AI Security Guardrails — Research Prototype

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Dinakarnayak/ai-security-guardrails-starter/blob/main/AI_Security_Guardrails_Colab.ipynb)

An offline-first Python research prototype for studying layered guardrails around a small quantized language model in a healthcare-information scenario. It combines system-prompt governance, deterministic input policy checks, output validation, and optional privacy-conscious local audit metadata.

**Research integrity:** this repository is a prototype, not a clinically validated system and not evidence of a completed PhD-level study. The included cases are synthetic smoke tests. Pattern matching can miss risks and block benign content. Never use it for diagnosis, triage, prescribing, or patient care.

## Quick start on Windows

Python 3.11 is recommended.

```powershell
git clone https://github.com/Dinakarnayak/ai-security-guardrails-starter.git
cd ai-security-guardrails-starter
py -3.11 app.py --self-test
py -3.11 -m unittest discover -s tests -v
py -3.11 evaluate_guardrails.py
```

The self-test uses only the Python standard library. The unit tests cover core rule behaviour. The evaluation script reports action/category accuracy, precision, recall, false-positive and false-negative rates, plus per-stage results and case-level errors. Review all labels in `evaluation/cases.jsonl` before interpreting metrics; the cases are illustrative, small, and not independently adjudicated.

To save a machine-readable report:

```powershell
py -3.11 evaluate_guardrails.py --output evaluation/results.json
```

## Research artefacts

- [Research protocol](RESEARCH_PROTOCOL.md): research question, hypotheses, experimental conditions, metrics, statistical reporting, reproducibility and ethics.
- [Evaluation notes](EVALUATION.md): threat model, risk policy, limitations and evaluation workflow.
- [Labelled smoke-test cases](evaluation/cases.jsonl): small synthetic JSONL set, including edge cases intended to reveal gaps.
- [Unit tests](tests/test_guardrails.py): regression checks for deterministic controls.
- [Evaluation harness](evaluate_guardrails.py): reproducible metric calculation and error export.

## Optional local model

The GGUF model is not included. Check the model card, licence, origin and SHA-256 checksum before use. Use a compatible small quantized model and keep it in a local `models` folder.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
New-Item -ItemType Directory -Force models
python app.py --model "models\YOUR_MODEL_FILE.gguf" --audit-log "audit\events.jsonl"
```

Replace the placeholder with the exact local model filename. The model is loaded from disk; the app contains no cloud API calls. Model output remains untrusted and can pass through incomplete pattern rules. Installation of `llama-cpp-python` may require a compatible Python version, compiler/runtime or platform-specific wheel.

The optional audit log records event metadata and a SHA-256 hash of text, not raw prompts or answers. Hashes and metadata may still be sensitive; define a retention period and do not log real health information.

## Evaluation plan

Do not present smoke-test metrics as general safety performance. A credible research study should include independently labelled benign, risky, ambiguous, paraphrased, misspelled and multilingual cases; a held-out test set; baseline and ablation comparisons; uncertainty intervals; category-level error analysis; and measured latency/memory. See [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md).

## Coursework demonstration

For the associated local-assistant coursework, use the local execution path and follow the current assessment brief. The prior brief indicated an approximately four-minute continuous Teams recording with camera and screen sharing, at least two triggered guardrail scenarios, and MP4 submission to Blackboard; verify the official brief for current requirements. Be ready to explain and defend the code yourself.

## Scope and safety

This is educational software engineering, not medical software. Urgent-symptom matching is not clinical triage. Do not use real patient data without appropriate ethics review, consent, and data-protection governance. A local model reduces cloud transfer but does not guarantee correctness, privacy, or regulatory compliance.
