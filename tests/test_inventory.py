"""Tests for the Inventory capacity system.

These tests verify CORRECT behavior.  The capacity-check test will
**FAIL** on the buggy implementation and **PASS** after the fix.
"""

from game_project.inventory import Inventory


# ── Test that FAILS on buggy code ────────────────────────────

def test_cannot_exceed_capacity():
    """Adding items beyond capacity should be rejected."""
    inv = Inventory(capacity=3)
    inv.add_item("Sword")
    inv.add_item("Shield")
    inv.add_item("Potion")
    result = inv.add_item("Helmet")
    assert result is False, "Item was accepted beyond capacity"
    assert inv.item_count == 3, f"Expected 3 items, got {inv.item_count}"


# ── Regression tests ─────────────────────────────────────────

def test_add_item_within_capacity():
    """Adding items under the limit should succeed."""
    inv = Inventory(capacity=5)
    assert inv.add_item("Sword") is True
    assert inv.item_count == 1


def test_is_full_at_capacity():
    """is_full should return True when inventory reaches capacity."""
    inv = Inventory(capacity=2)
    inv.add_item("A")
    inv.add_item("B")
    assert inv.is_full


def test_remove_existing_item():
    """Removing an existing item should succeed."""
    inv = Inventory(capacity=5)
    inv.add_item("Sword")
    assert inv.remove_item("Sword") is True
    assert inv.item_count == 0


def test_remove_nonexistent_item():
    """Removing a missing item should return False."""
    inv = Inventory(capacity=5)
    assert inv.remove_item("Ghost") is False
