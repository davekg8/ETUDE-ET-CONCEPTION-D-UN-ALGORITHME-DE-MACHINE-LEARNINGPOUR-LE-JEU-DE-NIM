"""Training routines for the Q-learning agent."""

from __future__ import annotations

import random
from collections.abc import Callable

from .agent import QLearningAgent
from .game import NimGame, State
from .opponents import NimSumOpponent

StateFactory = Callable[[random.Random], list[int]]


def random_state(rng: random.Random) -> list[int]:
    return [rng.randint(1, 10) for _ in range(4)]


def train_against_opponent(agent: QLearningAgent, episodes: int = 4000, seed: int | None = None,
                           state_factory: StateFactory = random_state) -> QLearningAgent:
    """Train player 0 against a deterministic Nim-sum opponent."""
    rng = random.Random(seed)
    opponent = NimSumOpponent()
    for _ in range(episodes):
        game = NimGame(state_factory(rng))
        previous: tuple[State, tuple[int, int]] | None = None
        while game.winner is None:
            state = game.state
            if game.player == 0:
                if previous is not None:
                    agent.update(*previous, state, 0.0)
                action = agent.choose_action(state, explore=True)
                previous = (state, action)
            else:
                action = opponent.choose_action(state)
            game.move(action)
        if previous is not None:
            reward = 1.0 if game.winner == 0 else -1.0
            agent.update(*previous, game.state, reward)
    return agent
