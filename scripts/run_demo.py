"""Quick CLI runner for the debugging pipeline.

Usage::

    python scripts/run_demo.py [health | inventory | enemy_ai]
"""

import json
import sys
from pathlib import Path

# Ensure project root is importable
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from graph.workflow import run_pipeline

BUG_FILES = {
    "health": "health_bug.json",
    "inventory": "inventory_bug.json",
    "enemy_ai": "enemy_ai_bug.json",
}


def main():
    choice = sys.argv[1] if len(sys.argv) > 1 else "health"
    filename = BUG_FILES.get(choice)
    if filename is None:
        print(f"Unknown bug: {choice}.  Choose from: {list(BUG_FILES)}")
        sys.exit(1)

    bug_path = _ROOT / "bug_cases" / filename
    report = json.loads(bug_path.read_text(encoding="utf-8"))

    source_file = report["source_file"]
    source_code = (_ROOT / source_file).read_text(encoding="utf-8")
    test_file = report["test_file"]

    print(f"\n{'=' * 60}")
    print(f"  Bug: {report['title']}")
    print(f"  File: {source_file}  |  Function: {report['affected_function']}")
    print(f"{'=' * 60}\n")

    result = run_pipeline(report, source_code, source_file, test_file)

    print(f"  Decision:      {result.get('decision')}")
    print(f"  Final Outcome: {result.get('final_outcome')}")
    print(f"  Attempts:      {result.get('attempt_count')}")
    print(f"  Baseline Pass: {result.get('baseline_tests_passed')}")
    print(f"  Post-fix Pass: {result.get('post_fix_tests_passed')}")
    print()
    print(f"  Root Cause:    {result.get('root_cause', '')[:120]}")
    print(f"  Fix:           {result.get('patch_explanation', '')[:120]}")
    print()

    # Save full result
    out = _ROOT / "sample_outputs" / f"{choice}_result.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"  Full report saved to: {out}\n")


if __name__ == "__main__":
    main()
