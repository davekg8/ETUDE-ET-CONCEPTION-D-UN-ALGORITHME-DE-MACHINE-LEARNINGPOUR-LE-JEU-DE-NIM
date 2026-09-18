"""Nim reinforcement-learning package."""

from .agent import QLearningAgent
from .game import NimGame
from .opponents import NimSumOpponent, RandomOpponent

__all__ = ["NimGame", "QLearningAgent", "NimSumOpponent", "RandomOpponent"]
