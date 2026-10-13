"""Evaluate deterministic guardrails against a JSONL case set.

Usage:
  py -3.11 evaluate_guardrails.py
  py -3.11 evaluate_guardrails.py --cases evaluation/cases.jsonl --output evaluation/results.json

Cases are illustrative, synthetic and require independent label review.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from app import inspect_input, validate_output


def score_case(case: dict[str, Any]) -> dict[str, Any]:
    if case["stage"] == "input":
        decision = inspect_input(case["text"])
    elif case["stage"] == "output":
        decision = validate_output(case["text"])
    else:
        raise ValueError(f"Unsupported stage: {case['stage']!r}")
    actual_risk = int(decision.action != "ALLOW")
    expected_risk = int(case["risk_label"])
    return {
        **case,
        "actual_action": decision.action,
        "actual_category": decision.category,
        "risk_score": decision.risk_score,
        "reason": decision.reason,
        "exact_action_match": decision.action == case["expected_action"],
        "category_match": decision.category == case["expected_category"],
        "actual_risk_label": actual_risk,
        "risk_label_match": actual_risk == expected_risk,
        "false_positive": expected_risk == 0 and actual_risk == 1,
        "false_negative": expected_risk == 1 and actual_risk == 0,
    }


def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tp = sum(r["risk_label"] == 1 and r["actual_risk_label"] == 1 for r in rows)
    tn = sum(r["risk_label"] == 0 and r["actual_risk_label"] == 0 for r in rows)
    fp = sum(r["false_positive"] for r in rows)
    fn = sum(r["false_negative"] for r in rows)
    n = len(rows)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {
        "n": n,
        "exact_action_accuracy": sum(r["exact_action_match"] for r in rows) / n if n else 0.0,
        "category_accuracy": sum(r["category_match"] for r in rows) / n if n else 0.0,
        "risk_accuracy": (tp + tn) / n if n else 0.0,
        "precision": precision,
        "recall": recall,
        "false_positive_rate": fp / (fp + tn) if fp + tn else 0.0,
        "false_negative_rate": fn / (fn + tp) if fn + tp else 0.0,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path("evaluation/cases.jsonl"))
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    cases = [json.loads(line) for line in args.cases.read_text(encoding="utf-8").splitlines() if line.strip()]
    rows = [score_case(case) for case in cases]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["stage"]].append(row)
    report = {
        "benchmark": str(args.cases),
        "warning": "Synthetic illustrative cases only; labels require independent review. Not a clinical safety claim.",
        "overall": metrics(rows),
        "by_stage": {stage: metrics(group) for stage, group in sorted(grouped.items())},
        "cases": rows,
        "errors": [
            {"id": r["id"], "stage": r["stage"], "expected_action": r["expected_action"],
             "actual_action": r["actual_action"], "expected_category": r["expected_category"],
             "actual_category": r["actual_category"], "rationale": r["rationale"]}
            for r in rows if not r["exact_action_match"] or not r["category_match"]
        ],
    }
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}, indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Full report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
