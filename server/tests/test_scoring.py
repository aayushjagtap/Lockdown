from app.game.state import GameState
from app.game.scoring import compute_scores, compute_round_result
from app.game.card import Card, Suit


def test_compute_scores_basic():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)

    gs.players["p1"].cards = [Card("A", Suit.CLUBS)]           # 1
    gs.players["p2"].cards = [Card("K", Suit.HEARTS)]          # red king = -1
    gs.players["p3"].cards = [Card("Q", Suit.SPADES)]          # 12
    gs.players["p4"].cards = [Card("10", Suit.DIAMONDS)]       # 10

    scores = compute_scores(gs)
    assert scores["p1"] == 1
    assert scores["p2"] == -1
    assert scores["p3"] == 12
    assert scores["p4"] == 10


def test_round_result_winner_and_tie():
    gs = GameState.new_game(["p1", "p2", "p3", "p4"], seed=1)

    gs.players["p1"].cards = [Card("2", Suit.CLUBS)]   # 2
    gs.players["p2"].cards = [Card("2", Suit.SPADES)]  # 2
    gs.players["p3"].cards = [Card("5", Suit.HEARTS)]  # 5
    gs.players["p4"].cards = [Card("A", Suit.CLUBS)]   # 1

    result = compute_round_result(gs)
    assert result.lowest_score == 1
    assert result.winners == ["p4"]
