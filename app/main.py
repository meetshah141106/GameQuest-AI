"""Agentic Game Debugger — Streamlit interface.

Entry point for the interactive demo.  Run with::

    streamlit run app/main.py
"""

import json
import sys
from pathlib import Path

# Ensure project root is on sys.path so all packages resolve.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st
from app.components.dashboard import render_dashboard
from app.components.results import render_results
from graph.workflow import run_pipeline

# ── Page configuration ───────────────────────────────────────
st.set_page_config(
    page_title="Agentic Game Debugger",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS for polish ────────────────────────────────────
st.markdown(
    """
    <style>
        /* gradient header */
        .main-header {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #7c3aed, #ec4899, #f97316);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            color: #9ca3af;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        /* metric cards */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #1e1b2e 0%, #272340 100%);
            border: 1px solid #3b3563;
            border-radius: 14px;
            padding: 18px 20px;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.6rem;
        }
        /* pipeline button */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #7c3aed, #ec4899);
            border: none;
            font-weight: 700;
            font-size: 1.1rem;
            padding: 0.7rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ───────────────────────────────────────────────────
st.markdown(
    '<div class="main-header">🎮 Agentic Game Debugger</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">'
    "LangGraph-powered pipeline for automated bug detection, "
    "root-cause analysis, and fixing in video games"
    "</div>",
    unsafe_allow_html=True,
)
st.warning(
    "**Educational PoC** — This is a controlled demonstration using "
    "predefined game bugs and deterministic agents.  It does not execute "
    "arbitrary code or connect to production systems.",
    icon="⚠️",
)

# ── Dashboard & bug selection ────────────────────────────────
case, source_code = render_dashboard()

st.divider()

# ── Run pipeline ─────────────────────────────────────────────
run_btn = st.button(
    "🚀 Run Debugging Pipeline",
    type="primary",
    use_container_width=True,
    help="Execute the full LangGraph workflow: detect → analyse → fix → test → decide",
)

if run_btn:
    with st.status("Running LangGraph debugging pipeline…", expanded=True) as status:
        st.write("🔍 **Bug Detection Agent** — analysing source code…")
        st.write("🔬 **Root Cause Analyser** — tracing the fault…")
        st.write("🔧 **Fix Generator** — crafting a patch…")
        st.write("🧪 **Test Verifier** — running tests in sandbox…")
        st.write("📊 **Decision Agent** — evaluating results…")

        result = run_pipeline(
            case, source_code, case["source_file"], case["test_file"],
        )

        if result.get("final_outcome") == "FIX VERIFIED":
            status.update(label="✅ Pipeline Complete — Fix Verified!", state="complete")
        else:
            status.update(label="⚠️ Pipeline Complete — Human Review Required", state="error")

    st.divider()
    render_results(result, case)

# ── Architecture footer ──────────────────────────────────────
st.divider()
with st.expander("🏗️ Pipeline Architecture", expanded=False):
    st.markdown(
        """
```text
START
  │
  ▼
bug_detector ──► root_cause_analyzer ──► fix_generator ◄── retry_fix
                                              │                 ▲
                                              ▼                 │
                                        test_verifier           │
                                              │                 │
                                              ▼                 │
                                       decision_agent ──────────┘
                                        ╱          ╲
                                   success       human_review
                                     │               │
                                    END             END
```

**Agents:**
1. **Bug Detector** — pattern-matches source code to identify suspected bugs.
2. **Root Cause Analyser** — explains *why* the code fails.
3. **Fix Generator** — produces a minimal string-replacement patch.
4. **Test Verifier** — runs ``pytest`` before & after the patch in a temp dir.
5. **Decision Agent** — routes to success, retry, or human review.
        """
    )

with st.expander("ℹ️ About This Project"):
    st.markdown(
        """
This project demonstrates how **Agentic AI** and **LangGraph** can
orchestrate a multi-step debugging workflow for video games.

- **No API key required** — runs in fully deterministic mode.
- **Safe execution** — patches are applied only to temporary copies.
- **LangGraph features** — `StateGraph`, typed state, normal edges,
  conditional edges, and a retry loop.

Built with Python · LangGraph · Streamlit · pytest
        """
    )
