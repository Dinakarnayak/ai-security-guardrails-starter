# AI Security Guardrails — Local Starter

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Dinakarnayak/ai-security-guardrails-starter/blob/main/AI_Security_Guardrails_Colab.ipynb)

This MSc-level learning prototype uses a healthcare-information scenario and
layered controls: system-prompt governance, input filtering and escalation,
privacy and prompt-injection checks, output validation, and an optional local
audit trail. It is not a medical service. Pattern rules can miss risks and can
also flag benign text.

## Run the guardrail demonstration first

The self-test uses only Python's standard library. You can run it before you
install a model binding or download a model:

```powershell
py -3.11 app.py --self-test
```

Expected checks cover a harmless question, medication request, urgent symptoms,
prompt injection, contact details, unsafe dose instruction, and overconfident
diagnosis.

## MSc-level design notes

Read [EVALUATION.md](EVALUATION.md) before recording. It explains the threat
model, rationale for each control, risk policy, residual limitations, data
minimisation, and a credible evaluation approach. The CLI prints each decision's
action, category, risk score, and reason for a live explanation.

## Optional local model setup

Use a small quantized GGUF model whose model card and licence you have checked.
The model is not included. After downloading it, keep it in a local `models`
folder. For example:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py --model "models\YOUR_MODEL_FILE.gguf" --audit-log "audit\events.jsonl"
```

`llama-cpp-python` loads the GGUF file from disk and runs inference locally.
The program contains no cloud API calls. The model response is still untrusted:
the input and output rules are simple examples, not a guarantee that every unsafe
answer will be caught.

The optional audit log is local JSON Lines. It contains event metadata and a
SHA-256 hash of text, never raw prompts or model answers. Retain it only as long
as needed for a demonstration.

## Optional Google Colab companion

[`AI_Security_Guardrails_Colab.ipynb`](AI_Security_Guardrails_Colab.ipynb) runs
the deterministic self-test in Google Colab. It is useful for learning and
previewing the rules, but it does not meet the coursework requirement to run the
assessed system locally unless the module convenor has approved the stated
device-access exception.

## Assignment demonstration reminder

The attached assessment brief requires a continuous Teams recording of about
four minutes, with camera and screen sharing, a live explanation, at least two
guardrail-triggering scenarios, and direct MP4 upload to Blackboard. It says the
video is the only submission and that you must understand and explain any code
you present. Check the brief for all recording and identity requirements.
