"""Evaluation helpers separated from training."""

from __future__ import annotations

import random
from collections.abc import Callable

from .agent import QLearningAgent
from .game import NimGame
from .opponents import NimSumOpponent, RandomOpponent
from .training import random_state


def evaluate(agent: QLearningAgent, games: int = 1000, opponent: str = "optimal", seed: int = 42) -> float:
    """Return the agent win rate with exploration disabled."""
    rng = random.Random(seed)
    rival = NimSumOpponent() if opponent == "optimal" else RandomOpponent(seed)
    wins = 0
    for _ in range(games):
        game = NimGame(random_state(rng))
        while game.winner is None:
            action = agent.choose_action(game.state, explore=False) if game.player == 0 else rival.choose_action(game.state)
            game.move(action)
        wins += game.winner == 0
    return wins / games
