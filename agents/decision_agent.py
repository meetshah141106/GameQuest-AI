"""Decision Agent — routes the workflow based on test results.

Deterministic rules:
  1. Tests passed  → ``fix_success``
  2. Tests failed, retries remain → ``retry_fix``
  3. Retries exhausted or safety issue → ``human_review``
"""

from __future__ import annotations
from graph.state import PipelineState


def make_decision(state: PipelineState) -> dict:
    """Decide whether to accept, retry, or escalate the fix."""
    tests_passed = state.get("post_fix_tests_passed", False)
    attempt = state.get("attempt_count", 0) + 1
    max_attempts = state.get("max_attempts", 3)
    history = list(state.get("workflow_history", []))
    previous_failures = list(state.get("previous_failures", []))
    review_reasons: list[str] = []

    # ── Safety: reject empty patches ─────────────────────
    if not state.get("fixed_code"):
        review_reasons.append("No patch was generated.")
        history.append({
            "node": "decision_agent",
            "decision": "human_review",
            "reasons": review_reasons,
        })
        return {
            "attempt_count": attempt,
            "decision": "NEEDS HUMAN REVIEW",
            "route": "human_review",
            "review_reasons": review_reasons,
            "previous_failures": previous_failures,
            "workflow_history": history,
        }

    # ── Tests passed → accept ────────────────────────────
    if tests_passed:
        history.append({"node": "decision_agent", "decision": "fix_success"})
        return {
            "attempt_count": attempt,
            "decision": "FIX VERIFIED",
            "route": "fix_success",
            "review_reasons": [],
            "previous_failures": previous_failures,
            "workflow_history": history,
        }

    # ── Tests failed — can we retry? ─────────────────────
    failure_info = state.get("post_fix_test_output", "Unknown failure")
    previous_failures.append(f"Attempt {attempt}: {failure_info[:300]}")

    if attempt < max_attempts:
        history.append({
            "node": "decision_agent",
            "decision": "retry_fix",
            "attempt": attempt,
        })
        return {
            "attempt_count": attempt,
            "decision": "RETRYING",
            "route": "retry_fix",
            "review_reasons": [],
            "previous_failures": previous_failures,
            "workflow_history": history,
        }

    # ── Retries exhausted → human review ─────────────────
    review_reasons.append(f"Fix failed after {attempt} attempt(s).")
    review_reasons.append(f"Last test output: {failure_info[:200]}")
    history.append({
        "node": "decision_agent",
        "decision": "human_review",
        "reasons": review_reasons,
    })
    return {
        "attempt_count": attempt,
        "decision": "NEEDS HUMAN REVIEW",
        "route": "human_review",
        "review_reasons": review_reasons,
        "previous_failures": previous_failures,
        "workflow_history": history,
    }
