"""Test & Verification Agent — runs tests before and after the patch.

1. Copies the game project and tests into an isolated temporary directory.
2. Runs the relevant test suite against the *buggy* code (baseline).
3. Applies the proposed patch via string replacement.
4. Runs the same tests against the *patched* code (post-fix).
5. Returns structured results so the Decision Agent can evaluate them.

Safety: the original project files are **never** modified.
"""

from __future__ import annotations
import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

from graph.state import PipelineState

# Project root — two levels up from this file (agents/ → project root)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def verify_fix(state: PipelineState) -> dict:
    """Run tests against both the original and patched code."""
    source_file = state.get("source_file", "")
    test_file = state.get("test_file", "")
    original_snippet = state.get("original_code", "")
    fixed_snippet = state.get("fixed_code", "")
    history = list(state.get("workflow_history", []))

    # ── Guard: nothing to verify ─────────────────────────
    if not fixed_snippet or not original_snippet:
        history.append({"node": "test_verifier", "message": "No patch to verify."})
        return {
            "baseline_test_output": "",
            "baseline_tests_passed": False,
            "post_fix_test_output": "No patch was provided.",
            "post_fix_tests_passed": False,
            "workflow_history": history,
        }

    temp_dir = tempfile.mkdtemp(prefix="game_debug_")
    try:
        # Copy game_project and tests into the sandbox
        shutil.copytree(
            _PROJECT_ROOT / "game_project",
            Path(temp_dir) / "game_project",
        )
        shutil.copytree(
            _PROJECT_ROOT / "tests",
            Path(temp_dir) / "tests",
        )

        # ── Baseline: run tests against BUGGY code ───────
        baseline = _run_tests(temp_dir, test_file)

        # ── Apply the patch ──────────────────────────────
        target = Path(temp_dir) / source_file
        content = target.read_text(encoding="utf-8")
        patched = content.replace(original_snippet, fixed_snippet)

        if patched == content:
            history.append({
                "node": "test_verifier",
                "message": "Patch snippet not found in target file.",
            })
            return {
                "baseline_test_output": baseline["output"],
                "baseline_tests_passed": baseline["passed"],
                "post_fix_test_output": "Patch could not be applied — snippet not found.",
                "post_fix_tests_passed": False,
                "workflow_history": history,
            }

        target.write_text(patched, encoding="utf-8")

        # ── Post-fix: run tests against PATCHED code ─────
        post_fix = _run_tests(temp_dir, test_file)

        result = {
            "baseline_test_output": baseline["output"],
            "baseline_tests_passed": baseline["passed"],
            "post_fix_test_output": post_fix["output"],
            "post_fix_tests_passed": post_fix["passed"],
        }
        history.append({"node": "test_verifier", "result": {
            "baseline_passed": baseline["passed"],
            "post_fix_passed": post_fix["passed"],
        }})
        result["workflow_history"] = history
        return result

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ── Helper ───────────────────────────────────────────────────

def _run_tests(work_dir: str, test_file: str) -> dict:
    """Run ``pytest`` in a subprocess and return structured results."""
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", f"tests/{test_file}", "-v", "--tb=short"],
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "passed": proc.returncode == 0,
            "output": proc.stdout + ("\n" + proc.stderr if proc.stderr else ""),
            "returncode": proc.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "passed": False,
            "output": "Test execution timed out after 30 seconds.",
            "returncode": -1,
        }
    except Exception as exc:
        return {
            "passed": False,
            "output": f"Error running tests: {exc}",
            "returncode": -1,
        }
