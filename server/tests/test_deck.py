import pytest

from app.game.card import Card
from app.game.deck import Deck


def test_standard_deck_has_52_unique_cards():
    deck = Deck.standard_52(seed=123)
    assert deck.remaining() == 52

    seen = set()
    for c in deck.draw_pile:
        seen.add((c.rank, c.suit.value))
    assert len(seen) == 52


def test_draw_reduces_count():
    deck = Deck.standard_52(seed=1)
    c = deck.draw()
    assert isinstance(c, Card)
    assert deck.remaining() == 51


def test_discard_adds_to_discard_pile():
    deck = Deck.standard_52(seed=1)
    c = deck.draw()
    deck.discard(c)
    assert deck.discard_top() == c
    assert len(deck.discard_pile) == 1


def test_drawing_empty_deck_raises():
    deck = Deck.standard_52(seed=1)
    for _ in range(52):
        deck.draw()
    with pytest.raises(RuntimeError):
        deck.draw()
