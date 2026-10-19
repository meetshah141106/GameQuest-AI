"""LangGraph workflow builder for the game-bug debugging pipeline.

Wires the five specialised agents into a ``StateGraph`` with normal
edges, one conditional edge (decision routing), and a retry loop.
"""

from __future__ import annotations
from langgraph.graph import StateGraph, START, END

from graph.state import PipelineState
from graph.routing import route_decision
from agents.bug_detector import detect_bug
from agents.root_cause_analyzer import analyze_root_cause
from agents.fix_generator import generate_fix
from agents.test_verifier import verify_fix
from agents.decision_agent import make_decision


# ── Terminal helper nodes ────────────────────────────────────

def _report_success(state: PipelineState) -> dict:
    """Terminal node — fix verified and accepted."""
    history = list(state.get("workflow_history", []))
    history.append({"node": "fix_success", "message": "Fix verified and accepted."})
    return {
        "status": "completed",
        "final_outcome": "FIX VERIFIED",
        "workflow_history": history,
    }


def _report_human_review(state: PipelineState) -> dict:
    """Terminal node — escalated to human review."""
    reasons = state.get("review_reasons", ["Unresolved after maximum attempts."])
    history = list(state.get("workflow_history", []))
    history.append({
        "node": "human_review",
        "message": "Escalated to human review.",
        "reasons": reasons,
    })
    return {
        "status": "human_review",
        "final_outcome": "NEEDS HUMAN REVIEW",
        "workflow_history": history,
    }


# ── Graph construction ───────────────────────────────────────

def build_workflow():
    """Build and compile the LangGraph debugging workflow.

    Graph structure::

        START
          │
          ▼
        bug_detector ──► root_cause_analyzer ──► fix_generator
                                                      │
                                                      ▼
                                                test_verifier
                                                      │
                                                      ▼
                                               decision_agent
                                               ╱      │      ╲
                                          success   retry    review
                                            │         │        │
                                           END   fix_generator END
    """
    graph = StateGraph(PipelineState)

    # Nodes
    graph.add_node("bug_detector", detect_bug)
    graph.add_node("root_cause_analyzer", analyze_root_cause)
    graph.add_node("fix_generator", generate_fix)
    graph.add_node("test_verifier", verify_fix)
    graph.add_node("decision_agent", make_decision)
    graph.add_node("fix_success", _report_success)
    graph.add_node("human_review", _report_human_review)

    # Normal (sequential) edges
    graph.add_edge(START, "bug_detector")
    graph.add_edge("bug_detector", "root_cause_analyzer")
    graph.add_edge("root_cause_analyzer", "fix_generator")
    graph.add_edge("fix_generator", "test_verifier")
    graph.add_edge("test_verifier", "decision_agent")

    # Conditional edge — decision routing
    graph.add_conditional_edges(
        "decision_agent",
        route_decision,
        {
            "fix_success": "fix_success",
            "retry_fix": "fix_generator",       # ← retry loop
            "human_review": "human_review",
        },
    )

    # Terminal edges
    graph.add_edge("fix_success", END)
    graph.add_edge("human_review", END)

    return graph.compile()


def run_pipeline(
    bug_report: dict,
    source_code: str,
    source_file: str,
    test_file: str,
) -> dict:
    """Execute the full debugging pipeline for one bug report."""
    workflow = build_workflow()
    initial_state: PipelineState = {
        "bug_report": bug_report,
        "source_code": source_code,
        "source_file": source_file,
        "test_file": test_file,
        "attempt_count": 0,
        "max_attempts": 3,
        "workflow_history": [],
        "previous_failures": [],
        "review_reasons": [],
    }
    return workflow.invoke(initial_state)
