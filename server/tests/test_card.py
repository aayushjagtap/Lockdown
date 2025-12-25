import pytest

from app.game.card import Card, Suit


def test_card_value_numeric():
    assert Card("2", Suit.CLUBS).value == 2
    assert Card("10", Suit.SPADES).value == 10


def test_card_value_faces():
    assert Card("A", Suit.HEARTS).value == 1
    assert Card("J", Suit.DIAMONDS).value == 11
    assert Card("Q", Suit.SPADES).value == 12
    assert Card("K", Suit.CLUBS).value == 13


def test_red_king_is_negative_one():
    assert Card("K", Suit.HEARTS).value == -1
    assert Card("K", Suit.DIAMONDS).value == -1


def test_black_king_is_thirteen():
    assert Card("K", Suit.SPADES).value == 13
    assert Card("K", Suit.CLUBS).value == 13


def test_invalid_rank_raises():
    with pytest.raises(ValueError):
        Card("1", Suit.CLUBS)

    with pytest.raises(ValueError):
        Card("Z", Suit.CLUBS)
