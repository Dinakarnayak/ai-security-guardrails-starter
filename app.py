"""A small local healthcare assistant demo with simple, explainable guardrails.

The rules below are demonstrations, not medical advice or a complete safety
system. The self-test runs with the Python standard library and needs no model.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Decision:
    action: str
    reason: str


# A small keyword list illustrates escalation. It cannot recognize every
# emergency or understand context, so the demo also explains that limitation.
URGENT_PHRASES = (
    "chest pain",
    "trouble breathing",
    "difficulty breathing",
    "can't breathe",
    "cannot breathe",
    "signs of a stroke",
    "face drooping",
    "severe bleeding",
    "overdose",
    "severe allergic reaction",
    "suicidal",
)

MEDICATION_REQUEST_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bwhat\s+(?:is\s+)?(?:dose|dosage)\b",
        r"\bhow\s+many\b.{0,80}\b(?:mg|mcg|µg|ml|milliliters?|pills?|tablets?)\b",
        r"\bhow\s+much\b.{0,80}\b(?:medicine|medication|drug|insulin|painkiller)\b",
        r"\bshould\s+i\s+(?:take|stop|increase|decrease|double)\b.{0,80}\b(?:medicine|medication|drug|pill|tablet|dose|dosage|insulin)\b",
        r"\b(?:change|adjust|increase|decrease|double|stop)\s+(?:my\s+)?(?:dose|dosage|medication)\b",
        r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|µg|ml|units?)\b.{0,60}\b(?:should\s+i|can\s+i|take|dose)\b",
    )
)

UNSAFE_DOSE_INSTRUCTION = re.compile(
    r"\b(?:take|start|increase|double|stop|skip|reduce|decrease|administer)\b"
    r"[^.!?\n]{0,80}\b\d+(?:\.\d+)?\s*(?:mg|mcg|µg|ml|units?)\b",
    re.IGNORECASE,
)

SYSTEM_PROMPT = (
    "You are an educational health-information assistant, not a clinician. "
    "Do not diagnose, prescribe, or recommend a personal medication dose. "
    "For urgent symptoms, tell the user to contact local emergency services. "
    "Give general information in cautious language and encourage professional care."
)

SAFE_FALLBACK = (
    "I can’t provide that medication instruction. Please check with your "
    "prescriber or pharmacist before changing how you take a medicine."
)


def inspect_input(text: str) -> Decision:
    """Apply the input filter and urgent-symptom escalation rule."""
    normalized = " ".join(text.casefold().split())

    for phrase in URGENT_PHRASES:
        if phrase in normalized:
            return Decision("ESCALATE", f"urgent phrase detected: {phrase!r}")

    for pattern in MEDICATION_REQUEST_PATTERNS:
        if pattern.search(normalized):
            return Decision(
                "BLOCK",
                "the question appears to request a personal medication decision",
            )

    return Decision("ALLOW", "no configured high-risk pattern matched")


def validate_output(text: str) -> tuple[bool, str]:
    """Reject a generated answer that gives a numeric medication instruction."""
    if UNSAFE_DOSE_INSTRUCTION.search(text):
        return False, "numeric medication instruction detected"
    return True, "no configured unsafe-dose pattern matched"


def run_self_test() -> int:
    """Run deterministic examples of both guardrails and the escalation path."""
    checks: list[tuple[str, bool, str]] = []

    harmless = inspect_input("What does a blood pressure reading measure?")
    checks.append(("Harmless question is allowed", harmless.action == "ALLOW", harmless.action))

    dosage = inspect_input("What dose of my medication should I take: 20 mg?")
    checks.append(("Personal medication-dose request is blocked", dosage.action == "BLOCK", dosage.action))

    urgent = inspect_input("I have chest pain and trouble breathing.")
    checks.append(("Urgent symptoms trigger escalation", urgent.action == "ESCALATE", urgent.action))

    simulated_unsafe_answer = "Take 20 mg tonight and double it tomorrow."
    is_safe, reason = validate_output(simulated_unsafe_answer)
    replacement = simulated_unsafe_answer if is_safe else SAFE_FALLBACK
    checks.append(
        (
            "Unsafe simulated answer is replaced by output validator",
            not is_safe and replacement == SAFE_FALLBACK,
            "REPLACED" if not is_safe else "PASSED THROUGH",
        )
    )

    for label, passed, result in checks:
        print(f"[{'PASS' if passed else 'FAIL'}] {label} — {result}")

    failed = sum(not passed for _, passed, _ in checks)
    print(f"\n{len(checks) - failed}/{len(checks)} self-test checks passed.")
    print("Rules are deterministic demonstrations; they do not prove complete safety.")
    if not is_safe:
        print(f"Output validator reason: {reason}.")
    return 0 if failed == 0 else 1


def load_local_model(model_path: Path) -> Any:
    """Load a GGUF model through llama.cpp's Python binding."""
    if not model_path.is_file():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    try:
        from llama_cpp import Llama
    except ImportError as exc:
        raise RuntimeError(
            "llama-cpp-python is not installed. Activate the virtual environment "
            "and run: python -m pip install llama-cpp-python"
        ) from exc

    # The model is opened from this local path; this program makes no API calls.
    return Llama(model_path=str(model_path), n_ctx=2048, verbose=False)


def run_assistant(model: Any) -> None:
    print("Local healthcare information demo. Type 'exit' to quit.")
    print("This is not a medical service; the keyword rules have known gaps.\n")

    while True:
        try:
            user_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if user_text.casefold() in {"exit", "quit"}:
            return
        if not user_text:
            continue

        decision = inspect_input(user_text)
        print(f"Input guardrail: {decision.action} ({decision.reason})")

        if decision.action == "ESCALATE":
            print(
                "Assistant: These symptoms may need urgent attention. Contact your "
                "local emergency service now. I cannot assess an emergency.\n"
            )
            continue
        if decision.action == "BLOCK":
            print(f"Assistant: {SAFE_FALLBACK}\n")
            continue

        response = model.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            max_tokens=256,
            temperature=0.2,
        )
        answer = response["choices"][0]["message"]["content"] or ""
        is_safe, reason = validate_output(answer)
        print(f"Output validator: {'ALLOW' if is_safe else 'REPLACE'} ({reason})")
        print(f"Assistant: {answer.strip() if is_safe else SAFE_FALLBACK}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Local healthcare assistant guardrail demo")
    parser.add_argument("--self-test", action="store_true", help="run rule demonstrations without loading a model")
    parser.add_argument("--model", type=Path, help="path to a local GGUF model file")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if args.model is None:
        parser.error("provide --self-test or --model PATH")

    try:
        model = load_local_model(args.model)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    run_assistant(model)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
