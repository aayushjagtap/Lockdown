from app.game.state import GameState
from app.game.tap import TapManager, TapTarget
from app.game.card import Card, Suit


def test_failed_tap_penalizes_tapper():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)
    tm = TapManager(gs)

    # force discard top and p1 card to be different
    gs.deck.discard(Card("2", Suit.CLUBS))
    gs.players["p1"].cards[0] = Card("5", Suit.HEARTS)

    before = gs.players["p1"].card_count()
    res = tm.attempt_tap("p1", TapTarget("player", "p1", 0), TapTarget("discard"))

    assert res.success is False
    assert res.tapper_penalized is True
    assert gs.players["p1"].card_count() == before + 1


def test_successful_player_discard_tap_removes_player_card():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)
    tm = TapManager(gs)

    gs.deck.discard(Card("7", Suit.CLUBS))
    gs.players["p1"].cards[0] = Card("7", Suit.HEARTS)

    before = gs.players["p1"].card_count()
    res = tm.attempt_tap("p1", TapTarget("player", "p1", 0), TapTarget("discard"))

    assert res.success is True
    assert gs.players["p1"].card_count() == before - 1


def test_successful_player_vs_player_tap_penalizes_other():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)
    tm = TapManager(gs)

    gs.players["p1"].cards[0] = Card("9", Suit.CLUBS)
    gs.players["p2"].cards[0] = Card("9", Suit.SPADES)

    p1_before = gs.players["p1"].card_count()
    p2_before = gs.players["p2"].card_count()

    res = tm.attempt_tap("p1", TapTarget("player", "p1", 0), TapTarget("player", "p2", 0))

    assert res.success is True
    assert gs.players["p1"].card_count() == p1_before - 1
    assert gs.players["p2"].card_count() == p2_before  # removed 1, then +1 penalty => net same
    assert res.other_penalized_player == "p2"


def test_cannot_tap_two_own_cards():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)
    tm = TapManager(gs)

    res = tm.attempt_tap("p1", TapTarget("player", "p1", 0), TapTarget("player", "p1", 1))
    assert res.success is False


def test_caller_cannot_tap_after_lockdown():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)
    gs.call_lockdown("p1")
    tm = TapManager(gs)

    res = tm.attempt_tap("p1", TapTarget("player", "p1", 0), TapTarget("discard"))
    assert res.success is False
