"""Bug Detection Agent — inspects source code and identifies suspected bugs.

Uses deterministic pattern-matching rules to detect known categories of
game bugs (boundary-condition errors, missing state transitions, etc.).
An optional LLM enhancement path is stubbed but not required for the demo.
"""

from __future__ import annotations
import re
from graph.state import PipelineState

# ── Deterministic detection rules ────────────────────────────
# Each rule looks for a *suspicious pattern* and checks whether the
# expected *safeguard* is absent.

_DETECTION_RULES = [
    {
        "pattern": r"def take_damage.*?self\.health\s*[-]=",
        "missing": r"self\.health\s*=\s*max\s*\(",
        "bug_type": "boundary_condition",
        "severity": "high",
        "function": "take_damage",
        "evidence": (
            "The `take_damage` method subtracts damage from `self.health` "
            "without a lower-bound clamp.  When damage exceeds current "
            "health the value becomes negative."
        ),
        "confidence": 0.95,
    },
    {
        "pattern": r"def add_item.*?self\.items\.append",
        "missing": r"if\s+len\(self\.items\)\s*>=?\s*self\.capacity",
        "bug_type": "boundary_condition",
        "severity": "medium",
        "function": "add_item",
        "evidence": (
            "Items are appended to `self.items` without checking whether "
            "the inventory has reached its maximum `self.capacity`."
        ),
        "confidence": 0.93,
    },
    {
        "pattern": r"def update.*?self\.state\s*=\s*self\.PURSUING",
        "missing": r"else:\s*\n\s*self\.state\s*=\s*self\.IDLE",
        "bug_type": "state_management",
        "severity": "medium",
        "function": "update",
        "evidence": (
            "The `update` method transitions the enemy to PURSUING or "
            "ATTACKING but never resets the state to IDLE when the player "
            "moves beyond the detection radius."
        ),
        "confidence": 0.92,
    },
]


def _strip_docs_and_comments(source: str) -> str:
    """Remove triple-quoted strings and ``# ...`` comments from source.

    This ensures that 'missing-safeguard' regex checks only match actual
    executable code, not documentation describing the expected fix.
    """
    # Remove triple-quoted strings (docstrings)
    source = re.sub(r'""".*?"""', '', source, flags=re.DOTALL)
    source = re.sub(r"'''.*?'''", '', source, flags=re.DOTALL)
    # Remove inline comments
    source = re.sub(r'#.*$', '', source, flags=re.MULTILINE)
    return source


def detect_bug(state: PipelineState) -> dict:
    """Inspect the source code and produce a structured detection report.

    Returns fields that update the shared pipeline state.
    """
    source = state.get("source_code", "")
    report = state.get("bug_report", {})
    history = list(state.get("workflow_history", []))

    # Strip docstrings and comments so 'missing' checks only match real code
    code_only = _strip_docs_and_comments(source)

    # Try each deterministic rule
    for rule in _DETECTION_RULES:
        if re.search(rule["pattern"], source, re.DOTALL):
            if not re.search(rule["missing"], code_only, re.DOTALL | re.MULTILINE):
                result = {
                    "bug_type": rule["bug_type"],
                    "severity": rule["severity"],
                    "affected_function": rule["function"],
                    "evidence": rule["evidence"],
                    "detection_confidence": rule["confidence"],
                    "detection_summary": (
                        f"Detected **{rule['bug_type']}** bug in "
                        f"`{rule['function']}` — {rule['evidence']} "
                        f"(severity: {rule['severity']}, "
                        f"confidence: {rule['confidence']:.0%})"
                    ),
                }
                history.append({"node": "bug_detector", "result": result})
                result["workflow_history"] = history
                return result

    # Fallback — use the metadata from the bug report
    result = {
        "bug_type": report.get("bug_type", "unknown"),
        "severity": report.get("severity", "medium"),
        "affected_function": report.get("affected_function", "unknown"),
        "evidence": report.get("description", "No specific pattern matched."),
        "detection_confidence": 0.60,
        "detection_summary": (
            f"Fallback detection via bug-report metadata: possible "
            f"`{report.get('bug_type', 'unknown')}` in "
            f"`{report.get('affected_function', 'unknown')}`."
        ),
    }
    history.append({"node": "bug_detector", "result": result})
    result["workflow_history"] = history
    return result
