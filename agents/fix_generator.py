"""Fix Generation Agent — produces a minimal code patch.

Generates a targeted string-replacement patch for the detected bug.
The patch is later applied to a *temporary copy* of the source file
by the Test Verifier; the original file is never modified.
"""

from __future__ import annotations
import difflib
from graph.state import PipelineState

# ── Predefined patches keyed by affected_function ────────────
# Each entry maps the *exact* buggy snippet to its corrected replacement.

_PATCHES: dict[str, dict[str, str]] = {
    "take_damage": {
        "original": "        self.health -= amount  # BUG: no lower-bound check",
        "fixed": "        self.health = max(0, self.health - amount)",
        "explanation": (
            "Replaced the unconditional subtraction with "
            "`max(0, self.health - amount)` to clamp health to a "
            "minimum of zero."
        ),
    },
    "add_item": {
        "original": (
            "        self.items.append(item)  # BUG: no capacity check\n"
            "        return True"
        ),
        "fixed": (
            "        if len(self.items) >= self.capacity:\n"
            "            return False\n"
            "        self.items.append(item)\n"
            "        return True"
        ),
        "explanation": (
            "Added a capacity guard before appending.  When the inventory "
            "is full the method now returns ``False`` instead of blindly "
            "accepting the item."
        ),
    },
    "update": {
        "original": "        # BUG: missing else — state is never reset to IDLE",
        "fixed": (
            "        else:\n"
            "            self.state = self.IDLE"
        ),
        "explanation": (
            "Added an ``else`` branch so the enemy returns to IDLE when "
            "the player is outside the detection radius."
        ),
    },
}


def generate_fix(state: PipelineState) -> dict:
    """Generate a minimal code patch for the detected bug.

    On retry attempts the agent receives ``previous_failures`` in the
    state, which could be used by an LLM-enhanced path to refine the
    patch.  The deterministic path always produces the correct patch.
    """
    func = state.get("affected_function", "")
    source = state.get("source_code", "")
    history = list(state.get("workflow_history", []))

    patch = _PATCHES.get(func)
    if patch is None:
        history.append({
            "node": "fix_generator",
            "message": f"No predefined patch for '{func}'.",
        })
        return {
            "original_code": "",
            "fixed_code": "",
            "patch_explanation": f"No deterministic patch available for '{func}'.",
            "patch_diff": "",
            "workflow_history": history,
        }

    original_snippet = patch["original"]
    fixed_snippet = patch["fixed"]

    # Build the full fixed source for the diff
    fixed_source = source.replace(original_snippet, fixed_snippet)

    # Unified diff for display
    diff_lines = difflib.unified_diff(
        source.splitlines(keepends=True),
        fixed_source.splitlines(keepends=True),
        fromfile="original",
        tofile="fixed",
    )
    patch_diff = "".join(diff_lines)

    result = {
        "original_code": original_snippet,
        "fixed_code": fixed_snippet,
        "patch_explanation": patch["explanation"],
        "patch_diff": patch_diff,
    }
    history.append({"node": "fix_generator", "result": {
        "function": func,
        "explanation": patch["explanation"],
    }})
    result["workflow_history"] = history
    return result
