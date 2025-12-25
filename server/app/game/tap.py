from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional, Tuple

from app.game.card import Card
from app.game.state import GameState


TargetType = Literal["player", "discard"]


@dataclass(frozen=True, slots=True)
class TapTarget:
    type: TargetType
    player_id: Optional[str] = None
    index: Optional[int] = None  # only for player targets


@dataclass(slots=True)
class TapResult:
    success: bool
    reason: str
    tapper_penalized: bool = False
    other_penalized_player: Optional[str] = None


class TapManager:
    def __init__(self, state: GameState) -> None:
        self.state = state

    def attempt_tap(self, tapper_id: str, a: TapTarget, b: TapTarget) -> TapResult:
        # cannot tap after calling lockdown
        if self.state.players[tapper_id].called_lockdown:
            return TapResult(False, "Tapper already called lockdown")

        # cannot tap two of your own cards
        if a.type == "player" and b.type == "player":
            if a.player_id == tapper_id and b.player_id == tapper_id:
                return TapResult(False, "Cannot tap two of your own cards")

        # resolve cards
        ca = self._get_card(a)
        cb = self._get_card(b)
        if ca is None or cb is None:
            return TapResult(False, "Invalid tap target")

        # compare by VALUE (not rank)
        if ca.value != cb.value:
            # failed tap => tapper draws one facedown
            self.state.players[tapper_id].add_card(self.state.deck.draw())
            return TapResult(False, "Values do not match", tapper_penalized=True)

        # success => discard involved cards (without replacement)
        self._discard_target(a)
        self._discard_target(b)

        # player-vs-player tap => other player penalized
        other_penalized = None
        if a.type == "player" and b.type == "player":
            other = a.player_id if b.player_id == tapper_id else b.player_id
            if other is not None and other != tapper_id:
                self.state.players[other].add_card(self.state.deck.draw())
                other_penalized = other

        return TapResult(True, "Match", other_penalized_player=other_penalized)

    def _get_card(self, t: TapTarget) -> Optional[Card]:
        if t.type == "discard":
            return self.state.deck.discard_top()
        if t.type == "player":
            if t.player_id is None or t.index is None:
                return None
            p = self.state.players.get(t.player_id)
            if p is None:
                return None
            if t.index < 0 or t.index >= len(p.cards):
                return None
            return p.cards[t.index]
        return None

    def _discard_target(self, t: TapTarget) -> None:
        """
        Remove the tapped card from its source and place into discard.
        - For player cards: remove from player (no replacement), put in discard.
        - For discard: consume the discard top by popping it.
        """
        if t.type == "discard":
            if self.state.deck.discard_pile:
                self.state.deck.discard_pile.pop()
            return

        # player target
        assert t.player_id is not None and t.index is not None
        p = self.state.players[t.player_id]
        removed = p.remove_card(t.index)
        self.state.deck.discard(removed)
