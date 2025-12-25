import pytest

from app.game.card import Card, Suit
from app.game.player import PlayerState


def make_cards(n: int):
    return [Card("2", Suit.CLUBS) for _ in range(n)]


def test_initial_card_count():
    p = PlayerState("p1", cards=make_cards(4))
    assert p.card_count() == 4


def test_peek_once_only():
    p = PlayerState("p1", cards=make_cards(4))
    c = p.peek(0)
    assert isinstance(c, Card)

    with pytest.raises(RuntimeError):
        p.peek(1)


def test_peek_invalid_index():
    p = PlayerState("p1", cards=make_cards(4))
    with pytest.raises(IndexError):
        p.peek(10)


def test_add_card_increases_count():
    p = PlayerState("p1", cards=make_cards(4))
    p.add_card(Card("A", Suit.HEARTS))
    assert p.card_count() == 5


def test_remove_card_decreases_count():
    p = PlayerState("p1", cards=make_cards(4))
    removed = p.remove_card(2)
    assert isinstance(removed, Card)
    assert p.card_count() == 3


def test_replace_card():
    p = PlayerState("p1", cards=make_cards(4))
    old = p.replace_card(1, Card("K", Suit.SPADES))
    assert isinstance(old, Card)
    assert p.cards[1].rank == "K"
