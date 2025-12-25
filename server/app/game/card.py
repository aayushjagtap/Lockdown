from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Suit(str, Enum):
    CLUBS = "C"
    DIAMONDS = "D"
    HEARTS = "H"
    SPADES = "S"


@dataclass(frozen=True, slots=True)
class Card:
    """
    A standard playing card.

    rank:
      "A", "2".."10", "J", "Q", "K"
    suit:
      Suit enum (C, D, H, S)

    Value rules (Lockdown):
      - Red King (D/H K): -1
      - A–10: face value (A=1)
      - J: 11
      - Q: 12
      - Black King (C/S K): 13
    """
    rank: str
    suit: Suit

    def __post_init__(self) -> None:
        valid_ranks = {"A", "J", "Q", "K"} | {str(n) for n in range(2, 11)}
        if self.rank not in valid_ranks:
            raise ValueError(f"Invalid rank: {self.rank}")
        if not isinstance(self.suit, Suit):
            raise ValueError(f"Invalid suit: {self.suit}")

    @property
    def is_red(self) -> bool:
        return self.suit in (Suit.DIAMONDS, Suit.HEARTS)

    @property
    def is_red_king(self) -> bool:
        return self.rank == "K" and self.is_red

    @property
    def value(self) -> int:
        if self.is_red_king:
            return -1
        if self.rank == "A":
            return 1
        if self.rank in {"J", "Q", "K"}:
            return {"J": 11, "Q": 12, "K": 13}[self.rank]
        # 2..10
        return int(self.rank)

    def __str__(self) -> str:
        return f"{self.rank}{self.suit.value}"
