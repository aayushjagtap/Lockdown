from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Dict, Set

from fastapi import WebSocket

from app.game.actions import TurnActions
from app.game.state import GameState
from app.game.scoring import compute_round_result


@dataclass
class Room:
    room_id: str
    state: GameState
    sockets: Set[WebSocket] = field(default_factory=set)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    def snapshot_public(self) -> Dict:
        """
        Return a public-safe state snapshot (no hidden cards).
        """
        return {
            "room_id": self.room_id,
            "players": {
                pid: {
                    "card_count": p.card_count(),
                    "called_lockdown": p.called_lockdown,
                }
                for pid, p in self.state.players.items()
            },
            "turn": {
                "current_player": self.state.current_player_id(),
                "lockdown_called_by": self.state.lockdown_called_by,
                "lockdown_turns_remaining": self.state.lockdown_turns_remaining,
                "round_over": self.state.is_round_over(),
            },
            "discard_top": (
                str(self.state.deck.discard_top()) if self.state.deck.discard_top() else None
            ),
        }

    def maybe_result(self) -> Dict:
        if not self.state.is_round_over():
            return {"available": False}
        result = compute_round_result(self.state)
        return {
            "available": True,
            "scores": result.scores,
            "winners": result.winners,
            "lowest_score": result.lowest_score,
        }


class RoomManager:
    def __init__(self) -> None:
        self.rooms: Dict[str, Room] = {}

    def create_room(self, room_id: str, player_ids: list[str], seed: int | None = None) -> Room:
        if room_id in self.rooms:
            raise RuntimeError("Room already exists")
        state = GameState.new_game(player_ids, seed=seed)
        room = Room(room_id=room_id, state=state)
        self.rooms[room_id] = room
        return room

    def get_room(self, room_id: str) -> Room:
        if room_id not in self.rooms:
            raise RuntimeError("Room not found")
        return self.rooms[room_id]
