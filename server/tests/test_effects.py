from app.game.actions import TurnActions
from app.game.state import GameState
from app.game.card import Card, Suit


def test_queen_triggers_effect():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"])
    actions = TurnActions(gs)

    gs.deck.draw_pile.append(Card("Q", Suit.SPADES))
    effect = actions.draw_and_discard("p1")

    assert effect.type == "queen"


def test_ten_triggers_effect():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"])
    actions = TurnActions(gs)

    gs.deck.draw_pile.append(Card("10", Suit.CLUBS))
    effect = actions.draw_and_discard("p1")

    assert effect.type == "ten"


def test_other_cards_no_effect():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"])
    actions = TurnActions(gs)

    gs.deck.draw_pile.append(Card("5", Suit.HEARTS))
    effect = actions.draw_and_discard("p1")

    assert effect.type == "none"
