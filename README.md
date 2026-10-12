# AI Security Guardrails — Local Starter

This small Python demo uses a healthcare-information scenario and two distinct
guardrails: an input filter (with escalation for configured urgent phrases) and
an output validator for numeric medication instructions. It is a learning demo,
not a medical service. The keyword rules can miss risks and can also flag benign
text.

## Run the guardrail demonstration first

The self-test uses only Python's standard library. You can run it before you
install a model binding or download a model:

```powershell
py -3.11 app.py --self-test
```

Expected checks: a general question is allowed, a personal medication-dose
request is blocked, urgent symptoms trigger escalation, and an unsafe simulated
model answer is replaced.

## Optional local model setup

Use a small quantized GGUF model whose model card and licence you have checked.
The model is not included. After downloading it, keep it in a local `models`
folder. For example:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py --model "models\YOUR_MODEL_FILE.gguf"
```

`llama-cpp-python` loads the GGUF file from disk and runs inference locally.
The program contains no cloud API calls. The model response is still untrusted:
the input and output rules are simple examples, not a guarantee that every unsafe
answer will be caught.

## Assignment demonstration reminder

The attached assessment brief requires a continuous Teams recording of about
four minutes, with camera and screen sharing, a live explanation, at least two
guardrail-triggering scenarios, and direct MP4 upload to Blackboard. It says the
video is the only submission and that you must understand and explain any code
you present. Check the brief for all recording and identity requirements.
