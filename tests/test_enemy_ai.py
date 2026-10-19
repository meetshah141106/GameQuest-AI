"""Tests for the EnemyAI state machine.

These tests verify CORRECT behavior.  The idle-reset test will **FAIL**
on the buggy implementation and **PASS** after the fix.
"""

from game_project.enemy_ai import EnemyAI


# ── Test that FAILS on buggy code ────────────────────────────

def test_returns_to_idle_when_player_leaves():
    """Enemy should go back to IDLE when player leaves detection radius."""
    enemy = EnemyAI("Goblin", detection_radius=10.0)
    # Step 1: player enters range → PURSUING
    enemy.update((5.0, 0.0))
    assert enemy.state == EnemyAI.PURSUING
    # Step 2: player moves far away → should be IDLE
    enemy.update((50.0, 0.0))
    assert enemy.state == EnemyAI.IDLE, f"State is '{enemy.state}', expected 'idle'"


# ── Regression tests ─────────────────────────────────────────

def test_pursues_when_in_detection_range():
    """Enemy should pursue when player is within detection radius."""
    enemy = EnemyAI("Goblin", detection_radius=10.0)
    enemy.update((8.0, 0.0))
    assert enemy.state == EnemyAI.PURSUING


def test_attacks_when_very_close():
    """Enemy should attack when player is within attack radius."""
    enemy = EnemyAI("Goblin", detection_radius=10.0, attack_radius=2.0)
    enemy.update((1.0, 0.0))
    assert enemy.state == EnemyAI.ATTACKING


def test_starts_in_idle():
    """Enemy should start in IDLE state."""
    enemy = EnemyAI("Goblin")
    assert enemy.state == EnemyAI.IDLE


def test_stays_idle_when_player_far():
    """Enemy should remain IDLE when player is always far away."""
    enemy = EnemyAI("Goblin", detection_radius=10.0)
    enemy.update((100.0, 100.0))
    assert enemy.state == EnemyAI.IDLE
