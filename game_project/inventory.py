"""Inventory module for the sample video game project.

Contains the Inventory class with item management functionality.
This module intentionally contains a bug for demonstration purposes:
the add_item method does not enforce the capacity limit.
"""


class Inventory:
    """Represents a player's inventory with a fixed capacity."""

    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.items: list[str] = []

    def add_item(self, item: str) -> bool:
        """Add an item to the inventory.

        BUG: Does not check whether inventory is already at capacity.
        Expected: reject the item and return False when full.
        """
        self.items.append(item)  # BUG: no capacity check
        return True

    def remove_item(self, item: str) -> bool:
        """Remove an item from the inventory. Returns False if not found."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    @property
    def is_full(self) -> bool:
        """Return True if inventory is at capacity."""
        return len(self.items) >= self.capacity

    @property
    def item_count(self) -> int:
        """Return the number of items currently held."""
        return len(self.items)

    def __repr__(self) -> str:
        return f"Inventory(capacity={self.capacity}, items={self.items})"
