from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.game.deck import Deck
from app.game.player import PlayerState


@dataclass(slots=True)
class GameState:
    """
    Owns the authoritative game state for a single round.

    This version supports:
    - Setup + dealing
    - Turn order
    - Calling lockdown and ending after others take one final turn
    """
    player_order: List[str]
    deck: Deck
    players: Dict[str, PlayerState] = field(default_factory=dict)

    turn_index: int = 0
    lockdown_called_by: Optional[str] = None
    lockdown_turns_remaining: Optional[int] = None  # number of non-caller turns left

    @classmethod
    def new_game(cls, player_ids: List[str], seed: Optional[int] = None) -> "GameState":
        if not (4 <= len(player_ids) <= 8):
            raise ValueError("Game must have 4–8 players")

        deck = Deck.standard_52(seed=seed)
        players = {pid: PlayerState(pid) for pid in player_ids}

        # Deal 4 facedown to each player
        for _ in range(4):
            for pid in player_ids:
                players[pid].add_card(deck.draw())

        return cls(player_order=list(player_ids), deck=deck, players=players)

    def current_player_id(self) -> str:
        return self.player_order[self.turn_index]

    def advance_turn(self) -> None:
        """
        Advance to next player's turn.
        Handles lockdown countdown if active.
        """
        if self.lockdown_called_by is not None:
            # During lockdown, only non-caller players get a final turn.
            if self.lockdown_turns_remaining is None:
                raise RuntimeError("Lockdown state corrupted")

            self.lockdown_turns_remaining -= 1
            if self.lockdown_turns_remaining < 0:
                raise RuntimeError("Lockdown turns went below zero")

            # Move turn_index forward skipping caller if needed
            self.turn_index = (self.turn_index + 1) % len(self.player_order)
            if self.current_player_id() == self.lockdown_called_by:
                self.turn_index = (self.turn_index + 1) % len(self.player_order)
            return

        # Normal flow
        self.turn_index = (self.turn_index + 1) % len(self.player_order)

    def call_lockdown(self, caller_id: str) -> None:
        if self.lockdown_called_by is not None:
            raise RuntimeError("Lockdown already called")
        if caller_id != self.current_player_id():
            raise RuntimeError("Only the current player can call lockdown")

        self.lockdown_called_by = caller_id
        self.players[caller_id].called_lockdown = True
        # every OTHER player gets one final turn
        self.lockdown_turns_remaining = len(self.player_order) - 1

        # Advance immediately to the next non-caller player
        self.turn_index = (self.turn_index + 1) % len(self.player_order)
        if self.current_player_id() == caller_id:
            self.turn_index = (self.turn_index + 1) % len(self.player_order)

    def is_round_over(self) -> bool:
        return self.lockdown_called_by is not None and self.lockdown_turns_remaining == 0
