import pytest

from app.game.actions import TurnActions
from app.game.state import GameState


def setup_game():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)
    actions = TurnActions(gs)
    return gs, actions


def test_draw_and_discard_advances_turn():
    gs, actions = setup_game()
    actions.draw_and_discard("p1")
    assert gs.current_player_id() == "p2"
    assert len(gs.deck.discard_pile) == 1


def test_draw_and_swap_replaces_card():
    gs, actions = setup_game()
    before = gs.players["p1"].cards[0]
    swapped = actions.draw_and_swap("p1", 0)
    after = gs.players["p1"].cards[0]
    assert before != after
    assert swapped == before


def test_take_discard_and_swap():
    gs, actions = setup_game()

    # p1 creates a discard
    actions.draw_and_discard("p1")
    top_before = gs.deck.discard_top()
    assert top_before is not None

    # p2 takes discard and swaps -> the swapped-out card becomes new discard top
    old_p2_card0 = gs.players["p2"].cards[0]
    swapped_out = actions.take_discard_and_swap("p2", 0)

    assert gs.players["p2"].cards[0] == top_before   # p2 received the old discard
    assert swapped_out == old_p2_card0               # returned card is what got discarded
    assert gs.deck.discard_top() == old_p2_card0     # discard top is p2's old card


def test_only_current_player_can_act():
    gs, actions = setup_game()
    with pytest.raises(RuntimeError):
        actions.draw_and_discard("p2")
