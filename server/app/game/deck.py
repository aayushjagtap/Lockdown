from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional

from app.game.card import Card, Suit


RANKS: List[str] = ["A"] + [str(n) for n in range(2, 11)] + ["J", "Q", "K"]
SUITS: List[Suit] = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]


@dataclass(slots=True)
class Deck:
    """
    A standard 52-card deck (no jokers).

    - `draw_pile`: face-down stack (top is end of list)
    - `discard_pile`: face-up stack (top is end of list)
    """
    rng: random.Random = field(default_factory=random.Random)
    draw_pile: List[Card] = field(default_factory=list)
    discard_pile: List[Card] = field(default_factory=list)

    @classmethod
    def standard_52(cls, seed: Optional[int] = None) -> "Deck":
        rng = random.Random(seed)
        cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        rng.shuffle(cards)
        return cls(rng=rng, draw_pile=cards, discard_pile=[])

    def remaining(self) -> int:
        return len(self.draw_pile)

    def discard_top(self) -> Optional[Card]:
        return self.discard_pile[-1] if self.discard_pile else None

    def draw(self) -> Card:
        if not self.draw_pile:
            raise RuntimeError("Draw pile is empty")
        return self.draw_pile.pop()

    def discard(self, card: Card) -> None:
        self.discard_pile.append(card)
