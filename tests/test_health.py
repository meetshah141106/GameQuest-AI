"""Tests for the Player health system.

These tests verify CORRECT behavior.  They will **FAIL** against the
buggy implementation and **PASS** after the fix is applied.
"""

from game_project.player import Player


# ── Tests that FAIL on buggy code (confirm the bug exists) ───

def test_health_does_not_go_negative():
    """Taking damage exceeding current health should clamp to 0."""
    player = Player("TestHero", health=100)
    player.take_damage(150)
    assert player.health >= 0, f"Health went negative: {player.health}"


def test_overkill_clamps_to_zero():
    """Massive overkill damage should still result in health == 0."""
    player = Player("TestHero", health=30)
    player.take_damage(100)
    assert player.health == 0, f"Expected 0, got {player.health}"


# ── Regression tests (should PASS on both buggy and fixed) ───

def test_normal_damage_reduces_health():
    """Normal damage should reduce health correctly."""
    player = Player("TestHero", health=100)
    player.take_damage(30)
    assert player.health == 70


def test_exact_lethal_damage():
    """Damage exactly equal to health should result in 0."""
    player = Player("TestHero", health=50)
    player.take_damage(50)
    assert player.health == 0


def test_heal_respects_max_health():
    """Healing should not exceed max_health."""
    player = Player("TestHero", health=50, max_health=100)
    player.heal(200)
    assert player.health == 100


def test_is_alive_false_at_zero():
    """Player should not be alive at 0 health."""
    player = Player("TestHero", health=100)
    player.take_damage(100)
    assert not player.is_alive
