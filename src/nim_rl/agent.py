"""Tabular Q-learning agent for Nim."""

from __future__ import annotations

import random
from collections import defaultdict

from .game import Action, NimGame, State


class QLearningAgent:
    def __init__(self, alpha: float = 0.1, epsilon: float = 0.2, gamma: float = 1.0, seed: int | None = None):
        if not 0 < alpha <= 1:
            raise ValueError("alpha must be in (0, 1]")
        if not 0 <= epsilon <= 1:
            raise ValueError("epsilon must be in [0, 1]")
        if not 0 <= gamma <= 1:
            raise ValueError("gamma must be in [0, 1]")
        self.alpha, self.epsilon, self.gamma = alpha, epsilon, gamma
        self.q: dict[tuple[State, Action], float] = defaultdict(float)
        self.rng = random.Random(seed)

    def value(self, state: State, action: Action) -> float:
        return self.q[(state, action)]

    def best_future_reward(self, state: State) -> float:
        actions = NimGame.available_actions(state)
        return max((self.value(state, action) for action in actions), default=0.0)

    def update(self, state: State, action: Action, next_state: State, reward: float) -> None:
        old = self.value(state, action)
        target = reward + self.gamma * self.best_future_reward(next_state)
        self.q[(state, action)] = old + self.alpha * (target - old)

    def choose_action(self, state: State, explore: bool = True) -> Action:
        actions = list(NimGame.available_actions(state))
        if not actions:
            raise ValueError("no legal actions available")
        if explore and self.rng.random() < self.epsilon:
            return self.rng.choice(actions)
        best = max(self.value(state, action) for action in actions)
        candidates = [action for action in actions if self.value(state, action) == best]
        return self.rng.choice(candidates)
