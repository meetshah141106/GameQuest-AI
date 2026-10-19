"""Conditional routing logic for the decision agent.

Called by LangGraph's ``add_conditional_edges`` to determine the next
node after the decision agent finishes.
"""

from __future__ import annotations
from graph.state import PipelineState


def route_decision(state: PipelineState) -> str:
    """Return the next node name based on the decision agent's output.

    Possible routes
    ---------------
    * ``"fix_success"``  — tests passed, patch accepted.
    * ``"retry_fix"``    — tests failed but retries remain.
    * ``"human_review"`` — retries exhausted or safety concern.
    """
    return state.get("route", "human_review")
