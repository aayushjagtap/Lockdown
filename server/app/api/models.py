from __future__ import annotations

from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class JoinRequest(BaseModel):
    room_id: str
    player_id: str


class ActionRequest(BaseModel):
    type: str  # "draw_discard" | "draw_swap" | "take_discard_swap" | "call_lockdown"
    card_index: Optional[int] = None


class ServerMessage(BaseModel):
    type: str  # "state" | "error" | "info"
    payload: Dict[str, Any]
