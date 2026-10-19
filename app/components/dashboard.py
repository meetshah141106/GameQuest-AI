"""Dashboard component — header, metrics, and bug-scenario selection."""

from __future__ import annotations
import json
from pathlib import Path
import streamlit as st

_BUG_CASES_DIR = Path(__file__).resolve().parent.parent.parent / "bug_cases"
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


@st.cache_data
def load_bug_cases() -> dict[str, dict]:
    """Load all ``bug_cases/*.json`` files into a dict keyed by title."""
    cases: dict[str, dict] = {}
    for f in sorted(_BUG_CASES_DIR.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        cases[data["title"]] = data
    return cases


def render_dashboard() -> tuple[dict, str]:
    """Render the dashboard and bug selector.

    Returns
    -------
    (selected_case, source_code) — the chosen bug report dict and
    the full source code of the buggy file.
    """
    bug_cases = load_bug_cases()

    # ── Metrics row ──────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🐛 Bug Scenarios", len(bug_cases))
    c2.metric("🤖 Pipeline Agents", "5")
    c3.metric("🔄 Max Retries", "2")
    c4.metric("🛡️ Mode", "Deterministic")

    st.divider()

    # ── Bug selector ─────────────────────────────────────
    selected = st.selectbox(
        "🎯 Select a bug scenario to debug",
        list(bug_cases.keys()),
        help="Choose one of the demo bugs to run through the pipeline.",
    )
    case = bug_cases[selected]

    # ── Bug info + source code ───────────────────────────
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📋 Bug Report")
        st.markdown(
            f"| Field | Value |\n"
            f"|---|---|\n"
            f"| **ID** | `{case['id']}` |\n"
            f"| **Title** | {case['title']} |\n"
            f"| **Type** | `{case['bug_type']}` |\n"
            f"| **Severity** | `{case['severity']}` |\n"
            f"| **File** | `{case['source_file']}` |\n"
            f"| **Function** | `{case['affected_function']}` |"
        )
        st.markdown("**Reproduction Steps:**")
        for step in case.get("reproduction_steps", []):
            st.markdown(f"- {step}")
        st.markdown(f"**Expected:** {case['expected_behavior']}")
        st.markdown(f"**Actual:** {case['actual_behavior']}")

    source_file = case["source_file"]
    source_code = (_PROJECT_ROOT / source_file).read_text(encoding="utf-8")

    with col_right:
        st.subheader("💻 Buggy Source Code")
        st.code(source_code, language="python", line_numbers=True)

    return case, source_code
