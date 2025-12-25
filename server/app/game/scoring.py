from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from app.game.state import GameState


@dataclass(frozen=True, slots=True)
class RoundResult:
    scores: Dict[str, int]          # player_id -> score
    winners: List[str]              # 1+ winners in tie
    lowest_score: int


def compute_scores(state: GameState) -> Dict[str, int]:
    return {
        pid: sum(card.value for card in p.cards)
        for pid, p in state.players.items()
    }


def compute_round_result(state: GameState) -> RoundResult:
    scores = compute_scores(state)
    lowest = min(scores.values())
    winners = [pid for pid, s in scores.items() if s == lowest]
    return RoundResult(scores=scores, winners=winners, lowest_score=lowest)
