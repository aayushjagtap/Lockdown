import pytest

from app.game.state import GameState


def test_new_game_deals_4_each_and_reduces_deck():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)
    assert all(gs.players[p].card_count() == 4 for p in gs.player_order)
    # 52 - (4 players * 4 cards) = 36
    assert gs.deck.remaining() == 36


def test_turn_advances_in_order():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)
    assert gs.current_player_id() == "p1"
    gs.advance_turn()
    assert gs.current_player_id() == "p2"
    gs.advance_turn()
    assert gs.current_player_id() == "p3"


def test_call_lockdown_sets_state_and_skips_caller():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)
    assert gs.current_player_id() == "p1"
    gs.call_lockdown("p1")

    assert gs.lockdown_called_by == "p1"
    assert gs.lockdown_turns_remaining == 3
    assert gs.current_player_id() == "p2"


def test_lockdown_countdown_ends_after_others_take_turns():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)
    gs.call_lockdown("p1")

    # p2 final turn
    gs.advance_turn()
    assert gs.lockdown_turns_remaining == 2
    # p3 final turn
    gs.advance_turn()
    assert gs.lockdown_turns_remaining == 1
    # p4 final turn
    gs.advance_turn()
    assert gs.lockdown_turns_remaining == 0
    assert gs.is_round_over() is True


def test_only_current_player_can_call_lockdown():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)
    with pytest.raises(RuntimeError):
        gs.call_lockdown("p2")
