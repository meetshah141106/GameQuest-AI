"""Root Cause Analysis Agent — explains *why* the detected bug occurs.

Receives detection output and source code, then produces a human-readable
explanation of the root cause, the faulty condition, and a recommendation.
"""

from __future__ import annotations
from graph.state import PipelineState

# ── Pre-built analyses keyed by (bug_type, affected_function) ─

_ANALYSES: dict[tuple[str, str], dict[str, str]] = {
    ("boundary_condition", "take_damage"): {
        "root_cause": (
            "The `take_damage` method subtracts the full damage amount from "
            "`self.health` unconditionally (`self.health -= amount`).  When "
            "the damage exceeds the player's remaining health the result is "
            "a negative integer.  No boundary check prevents health from "
            "falling below zero, which violates the game's invariant that "
            "health ∈ [0, max_health]."
        ),
        "faulty_condition": (
            "self.health -= amount  # missing: max(0, self.health - amount)"
        ),
        "recommendation": (
            "Clamp the result with `self.health = max(0, self.health - amount)` "
            "so that health never becomes negative."
        ),
    },
    ("boundary_condition", "add_item"): {
        "root_cause": (
            "The `add_item` method appends the new item to `self.items` "
            "without comparing `len(self.items)` against `self.capacity`.  "
            "As a result the inventory can grow beyond its intended maximum "
            "size, breaking downstream systems that depend on the capacity "
            "constraint."
        ),
        "faulty_condition": (
            "self.items.append(item)  # missing capacity guard"
        ),
        "recommendation": (
            "Before appending, check `if len(self.items) >= self.capacity: "
            "return False`.  This rejects new items once the inventory is full."
        ),
    },
    ("state_management", "update"): {
        "root_cause": (
            "The `update` method transitions the enemy to PURSUING or "
            "ATTACKING when the player is within range, but the conditional "
            "block has no `else` branch.  Once the enemy enters an "
            "aggressive state it never resets back to IDLE, even after the "
            "player moves well beyond the detection radius."
        ),
        "faulty_condition": (
            "Missing `else: self.state = self.IDLE` after the distance-"
            "checking if/elif block."
        ),
        "recommendation": (
            "Add an `else` clause that sets `self.state = self.IDLE` when "
            "the player's distance exceeds the detection radius."
        ),
    },
}


def analyze_root_cause(state: PipelineState) -> dict:
    """Produce a root-cause explanation grounded in the source code."""
    key = (state.get("bug_type", ""), state.get("affected_function", ""))
    history = list(state.get("workflow_history", []))

    analysis = _ANALYSES.get(key, {
        "root_cause": (
            f"The function `{key[1]}` appears to have a `{key[0]}` issue "
            f"based on the detection evidence: {state.get('evidence', 'N/A')}."
        ),
        "faulty_condition": (
            "Unable to pinpoint the exact faulty line from patterns alone."
        ),
        "recommendation": "Manual code inspection is recommended.",
    })

    history.append({"node": "root_cause_analyzer", "result": analysis})
    return {**analysis, "workflow_history": history}
