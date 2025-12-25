from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from app.game.card import Card


@dataclass(slots=True)
class PlayerState:
    """
    Represents a single player’s hidden card state.

    - Cards are face-down to others.
    - Player may peek at exactly one card once at game start.
    """
    player_id: str
    cards: List[Card] = field(default_factory=list)
    peek_used: bool = False
    called_lockdown: bool = False

    def card_count(self) -> int:
        return len(self.cards)

    def peek(self, index: int) -> Card:
        """
        Allows the player to look at exactly one of their cards, once.
        """
        if self.peek_used:
            raise RuntimeError("Peek already used")
        if index < 0 or index >= len(self.cards):
            raise IndexError("Invalid card index")

        self.peek_used = True
        return self.cards[index]

    def add_card(self, card: Card) -> None:
        """
        Add a facedown card (used for penalties).
        """
        self.cards.append(card)

    def remove_card(self, index: int) -> Card:
        """
        Remove a card from the player (used for tapping rewards).
        """
        if index < 0 or index >= len(self.cards):
            raise IndexError("Invalid card index")
        return self.cards.pop(index)

    def replace_card(self, index: int, new_card: Card) -> Card:
        """
        Swap a card at index with a new card.
        Returns the old card.
        """
        if index < 0 or index >= len(self.cards):
            raise IndexError("Invalid card index")
        old = self.cards[index]
        self.cards[index] = new_card
        return old
