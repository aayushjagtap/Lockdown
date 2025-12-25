from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.game.card import Card
from app.game.state import GameState
from app.game.effects import EffectResult


@dataclass(slots=True)
class TurnActions:
    state: GameState

    def _ensure_current_player(self, player_id: str) -> None:
        if player_id != self.state.current_player_id():
            raise RuntimeError("Not this player's turn")

    def draw_and_discard(self, player_id: str) -> EffectResult:
        self._ensure_current_player(player_id)

        card = self.state.deck.draw()
        self.state.deck.discard(card)

        effect = "none"
        if card.rank == "Q":
            effect = "queen"
        elif card.rank == "10":
            effect = "ten"
        self.state.advance_turn()
        return EffectResult(type=effect, player_id=player_id)

    def draw_and_swap(self, player_id: str, card_index: int) -> Card:
        self._ensure_current_player(player_id)
        drawn = self.state.deck.draw()
        player = self.state.players[player_id]
        swapped = player.replace_card(card_index, drawn)
        self.state.deck.discard(swapped)
        self.state.advance_turn()
        return swapped

    def take_discard_and_swap(self, player_id: str, card_index: int) -> Card:
        self._ensure_current_player(player_id)

        if not self.state.deck.discard_pile:
            raise RuntimeError("Discard pile is empty")

        taken = self.state.deck.discard_pile.pop()  # remove TOP discard
        player = self.state.players[player_id]

        swapped_out = player.replace_card(card_index, taken)  # player takes discard
        self.state.deck.discard(swapped_out)                  # old player card becomes new top discard

        self.state.advance_turn()
        return swapped_out
