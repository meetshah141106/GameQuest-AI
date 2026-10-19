"""Enemy AI module for the sample video game project.

Contains the EnemyAI class with a finite-state machine for enemy behavior.
This module intentionally contains a bug for demonstration purposes:
the update method does not reset the state to IDLE when the player
moves outside the detection radius.
"""

import math


class EnemyAI:
    """Represents an enemy with a simple state machine."""

    IDLE = "idle"
    PURSUING = "pursuing"
    ATTACKING = "attacking"

    def __init__(
        self,
        name: str,
        detection_radius: float = 10.0,
        attack_radius: float = 2.0,
    ):
        self.name = name
        self.state = self.IDLE
        self.detection_radius = detection_radius
        self.attack_radius = attack_radius
        self.position: tuple[float, float] = (0.0, 0.0)

    def update(self, player_position: tuple[float, float]) -> None:
        """Update the enemy state based on the player's position.

        BUG: When the player moves beyond the detection radius the state
        is never reset to IDLE, so the enemy stays in PURSUING or ATTACKING.
        Expected: add an else branch that sets self.state = self.IDLE.
        """
        distance = self._calculate_distance(player_position)

        if distance <= self.attack_radius:
            self.state = self.ATTACKING
        elif distance <= self.detection_radius:
            self.state = self.PURSUING
        # BUG: missing else — state is never reset to IDLE

    def _calculate_distance(self, target: tuple[float, float]) -> float:
        """Euclidean distance from self.position to target."""
        dx = self.position[0] - target[0]
        dy = self.position[1] - target[1]
        return math.sqrt(dx * dx + dy * dy)

    def __repr__(self) -> str:
        return f"EnemyAI(name={self.name!r}, state={self.state!r})"
