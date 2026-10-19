"""Results component — renders pipeline output across multiple tabs."""

from __future__ import annotations
import json
import streamlit as st


def render_results(result: dict, case: dict) -> None:
    """Display the full pipeline results in an organised tab layout."""

    # ── Outcome banner ───────────────────────────────────
    if result.get("final_outcome") == "FIX VERIFIED":
        st.success(
            f"**{result['final_outcome']}** — The proposed fix passed all tests.",
            icon="✅",
        )
    else:
        reasons = "; ".join(result.get("review_reasons", []))
        st.error(
            f"**{result.get('final_outcome', 'UNKNOWN')}** — {reasons}",
            icon="🔴",
        )

    # ── Summary metrics ──────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Decision", result.get("decision", "N/A"))
    m2.metric("Confidence", f"{result.get('detection_confidence', 0):.0%}")
    m3.metric("Attempts", result.get("attempt_count", 0))
    m4.metric("Tests Passed", "✅" if result.get("post_fix_tests_passed") else "❌")

    # ── Detailed tabs ────────────────────────────────────
    tabs = st.tabs([
        "🔍 Detection",
        "🔬 Root Cause",
        "🔧 Patch",
        "🧪 Tests",
        "📊 Routing",
        "📄 Report",
    ])

    # Tab 1 — Detection
    with tabs[0]:
        st.subheader("Bug Detection Results")
        st.markdown(
            f"| Field | Value |\n"
            f"|---|---|\n"
            f"| **Bug Type** | `{result.get('bug_type', 'N/A')}` |\n"
            f"| **Severity** | `{result.get('severity', 'N/A')}` |\n"
            f"| **Affected Function** | `{result.get('affected_function', 'N/A')}` |\n"
            f"| **Confidence** | `{result.get('detection_confidence', 0):.0%}` |"
        )
        st.info(result.get("evidence", ""), icon="🔍")

    # Tab 2 — Root Cause
    with tabs[1]:
        st.subheader("Root Cause Analysis")
        st.markdown("**Root Cause:**")
        st.write(result.get("root_cause", "N/A"))
        st.markdown("**Faulty Condition:**")
        st.code(result.get("faulty_condition", ""), language="python")
        st.markdown("**Recommendation:**")
        st.info(result.get("recommendation", ""), icon="💡")

    # Tab 3 — Patch
    with tabs[2]:
        st.subheader("Proposed Patch")
        st.write(result.get("patch_explanation", ""))
        fix_l, fix_r = st.columns(2)
        with fix_l:
            st.markdown("**Original (buggy):**")
            st.code(result.get("original_code", ""), language="python")
        with fix_r:
            st.markdown("**Fixed:**")
            st.code(result.get("fixed_code", ""), language="python")
        if result.get("patch_diff"):
            with st.expander("📄 Unified Diff", expanded=True):
                st.code(result["patch_diff"], language="diff")

    # Tab 4 — Tests
    with tabs[3]:
        st.subheader("Test Results")
        tl, tr = st.columns(2)
        with tl:
            st.markdown("**Baseline (buggy code):**")
            if result.get("baseline_tests_passed"):
                st.success("Tests passed (unexpected)")
            else:
                st.error("Tests failed — confirms the bug exists")
            with st.expander("Test Output"):
                st.code(result.get("baseline_test_output", ""), language="text")
        with tr:
            st.markdown("**Post-Fix (patched code):**")
            if result.get("post_fix_tests_passed"):
                st.success("All tests passed ✅")
            else:
                st.error("Tests still failing ❌")
            with st.expander("Test Output"):
                st.code(result.get("post_fix_test_output", ""), language="text")

    # Tab 5 — Routing / Decision
    with tabs[4]:
        st.subheader("Decision & Routing")
        st.markdown(
            f"| Field | Value |\n"
            f"|---|---|\n"
            f"| **Decision** | `{result.get('decision', 'N/A')}` |\n"
            f"| **Route Taken** | `{result.get('route', 'N/A')}` |\n"
            f"| **Attempts** | `{result.get('attempt_count', 0)}` / "
            f"`{result.get('max_attempts', 3)}` |"
        )
        if result.get("review_reasons"):
            st.warning("**Review Reasons:**")
            for r in result["review_reasons"]:
                st.write(f"- {r}")
        if result.get("previous_failures"):
            with st.expander("Previous Failure Log"):
                for f in result["previous_failures"]:
                    st.write(f)
        st.subheader("Graph Route")
        route = result.get("route", "unknown")
        st.code(
            f"START → bug_detector → root_cause_analyzer → fix_generator → "
            f"test_verifier → decision_agent → {route} → END",
            language="text",
        )

    # Tab 6 — Full Report
    with tabs[5]:
        st.subheader("Full Execution Report")
        report = {
            "bug_id": case.get("id"),
            "bug_title": case.get("title"),
            "source_file": case.get("source_file"),
            "affected_function": result.get("affected_function"),
            "bug_type": result.get("bug_type"),
            "severity": result.get("severity"),
            "detection_confidence": result.get("detection_confidence"),
            "root_cause": result.get("root_cause"),
            "patch_explanation": result.get("patch_explanation"),
            "original_code": result.get("original_code"),
            "fixed_code": result.get("fixed_code"),
            "baseline_tests_passed": result.get("baseline_tests_passed"),
            "post_fix_tests_passed": result.get("post_fix_tests_passed"),
            "attempts": result.get("attempt_count"),
            "decision": result.get("decision"),
            "final_outcome": result.get("final_outcome"),
            "route": result.get("route"),
        }
        st.json(report)

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                "📥 Download Report (JSON)",
                json.dumps(report, indent=2),
                file_name="debug_report.json",
                mime="application/json",
                use_container_width=True,
            )
        with dl2:
            st.download_button(
                "📥 Download Patch",
                result.get("patch_diff", "No patch available"),
                file_name="fix.patch",
                mime="text/plain",
                use_container_width=True,
            )
