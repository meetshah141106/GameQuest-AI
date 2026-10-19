"""Pipeline state definition for the LangGraph workflow.

All agents read from and write to this shared TypedDict.
"""

from __future__ import annotations
from typing import TypedDict, Any


class PipelineState(TypedDict, total=False):
    """Shared state passed through every node of the LangGraph workflow."""

    # ── Input ────────────────────────────────────────────────
    bug_report: dict[str, Any]
    source_code: str
    source_file: str
    test_file: str

    # ── Bug Detection ────────────────────────────────────────
    bug_type: str
    severity: str
    affected_function: str
    evidence: str
    detection_confidence: float
    detection_summary: str

    # ── Root Cause Analysis ──────────────────────────────────
    root_cause: str
    faulty_condition: str
    recommendation: str

    # ── Fix Generation ───────────────────────────────────────
    original_code: str
    fixed_code: str
    patch_explanation: str
    patch_diff: str

    # ── Testing ──────────────────────────────────────────────
    baseline_test_output: str
    baseline_tests_passed: bool
    post_fix_test_output: str
    post_fix_tests_passed: bool

    # ── Decision / Routing ───────────────────────────────────
    attempt_count: int
    max_attempts: int
    decision: str
    route: str
    review_reasons: list[str]
    previous_failures: list[str]

    # ── Final ────────────────────────────────────────────────
    status: str
    final_outcome: str
    workflow_history: list[dict[str, Any]]
