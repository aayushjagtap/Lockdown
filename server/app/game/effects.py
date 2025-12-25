from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class EffectResult:
    """
    Describes a special effect that the client/UI must resolve.
    """
    type: str  # "queen", "ten", or "none"
    player_id: str
