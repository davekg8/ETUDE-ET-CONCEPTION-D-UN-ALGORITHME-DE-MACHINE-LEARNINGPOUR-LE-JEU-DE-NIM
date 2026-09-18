"""Reference opponents for Nim."""

from __future__ import annotations

import random
from functools import reduce
from operator import xor

from .game import Action, NimGame, State


class RandomOpponent:
    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

    def choose_action(self, state: State) -> Action:
        return self.rng.choice(list(NimGame.available_actions(state)))


class NimSumOpponent:
    """Deterministic optimal normal-play Nim policy."""

    def choose_action(self, state: State) -> Action:
        nim_sum = reduce(xor, state, 0)
        if nim_sum:
            for index, pile in enumerate(state):
                target = pile ^ nim_sum
                if target < pile:
                    return index, pile - target
        # Every move loses against perfect play from a zero Nim-sum state.
        return min(NimGame.available_actions(state))
