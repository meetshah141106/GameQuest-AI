"""Integration tests for the complete LangGraph debugging pipeline.

Each test loads a bug case, feeds it through the full pipeline, and
verifies that the fix is detected, applied, tested, and accepted.
"""

import json
from pathlib import Path
from graph.workflow import run_pipeline

_BUG_CASES_DIR = Path(__file__).resolve().parent.parent / "bug_cases"
_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_case(filename: str) -> tuple[dict, str, str, str]:
    """Load a bug case and its corresponding source file."""
    report = json.loads((_BUG_CASES_DIR / filename).read_text(encoding="utf-8"))
    source_file = report["source_file"]
    source_code = (_PROJECT_ROOT / source_file).read_text(encoding="utf-8")
    test_file = report["test_file"]
    return report, source_code, source_file, test_file


# ── Pipeline end-to-end tests ────────────────────────────────

def test_health_bug_pipeline():
    """Health bug should be detected, fixed, and verified."""
    report, source, src_file, test_file = _load_case("health_bug.json")
    result = run_pipeline(report, source, src_file, test_file)
    assert result["final_outcome"] == "FIX VERIFIED"
    assert result["post_fix_tests_passed"] is True
    assert result["baseline_tests_passed"] is False  # confirms the bug


def test_inventory_bug_pipeline():
    """Inventory bug should be detected, fixed, and verified."""
    report, source, src_file, test_file = _load_case("inventory_bug.json")
    result = run_pipeline(report, source, src_file, test_file)
    assert result["final_outcome"] == "FIX VERIFIED"
    assert result["post_fix_tests_passed"] is True
    assert result["baseline_tests_passed"] is False


def test_enemy_ai_bug_pipeline():
    """Enemy AI bug should be detected, fixed, and verified."""
    report, source, src_file, test_file = _load_case("enemy_ai_bug.json")
    result = run_pipeline(report, source, src_file, test_file)
    assert result["final_outcome"] == "FIX VERIFIED"
    assert result["post_fix_tests_passed"] is True
    assert result["baseline_tests_passed"] is False


# ── Routing / retry / review tests ───────────────────────────

def test_pipeline_records_workflow_history():
    """The pipeline should record a workflow history list."""
    report, source, src_file, test_file = _load_case("health_bug.json")
    result = run_pipeline(report, source, src_file, test_file)
    history = result.get("workflow_history", [])
    assert len(history) > 0
    nodes_visited = [h["node"] for h in history]
    assert "bug_detector" in nodes_visited
    assert "root_cause_analyzer" in nodes_visited
    assert "fix_generator" in nodes_visited
    assert "test_verifier" in nodes_visited
    assert "decision_agent" in nodes_visited


def test_original_source_unchanged():
    """The pipeline must never modify original source files."""
    report, source, src_file, test_file = _load_case("health_bug.json")
    original = (_PROJECT_ROOT / src_file).read_text(encoding="utf-8")
    run_pipeline(report, source, src_file, test_file)
    after = (_PROJECT_ROOT / src_file).read_text(encoding="utf-8")
    assert original == after, "Original source was modified!"


def test_demo_runs_without_api_key():
    """The pipeline should complete in deterministic mode with no API key."""
    import os
    # Temporarily clear any API keys
    saved = {k: os.environ.pop(k, None) for k in
             ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]}
    try:
        report, source, src_file, test_file = _load_case("health_bug.json")
        result = run_pipeline(report, source, src_file, test_file)
        assert result["final_outcome"] == "FIX VERIFIED"
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v
