"""Player module for the sample video game project.

Contains the Player class with health management functionality.
This module intentionally contains a bug for demonstration purposes:
the take_damage method does not clamp health to a minimum of zero.
"""


class Player:
    """Represents a game player with health management."""

    def __init__(self, name: str, health: int = 100, max_health: int = 100):
        self.name = name
        self.health = health
        self.max_health = max_health

    def take_damage(self, amount: int) -> None:
        """Apply damage to the player.

        BUG: Health can become negative because there is no lower-bound clamp.
        Expected: self.health = max(0, self.health - amount)
        """
        self.health -= amount  # BUG: no lower-bound check

    def heal(self, amount: int) -> None:
        """Heal the player, capped at max_health."""
        self.health = min(self.health + amount, self.max_health)

    @property
    def is_alive(self) -> bool:
        """Return True if the player has positive health."""
        return self.health > 0

    def __repr__(self) -> str:
        return f"Player(name={self.name!r}, health={self.health}, max_health={self.max_health})"
