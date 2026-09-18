"""Core Nim game environment."""

from __future__ import annotations

from dataclasses import dataclass, field

Action = tuple[int, int]
State = tuple[int, ...]


@dataclass
class NimGame:
    """Two-player normal-play Nim: the player taking the last object wins."""

    piles: list[int] = field(default_factory=lambda: [1, 3, 5, 7])
    player: int = 0
    winner: int | None = None

    def __post_init__(self) -> None:
        if not self.piles or any(pile < 0 for pile in self.piles):
            raise ValueError("piles must be a non-empty sequence of non-negative integers")
        self.piles = list(self.piles)

    @property
    def state(self) -> State:
        return tuple(self.piles)

    @staticmethod
    def available_actions(state: State | list[int]) -> set[Action]:
        return {(i, count) for i, pile in enumerate(state) for count in range(1, pile + 1)}

    def move(self, action: Action) -> None:
        if self.winner is not None:
            raise RuntimeError("game is already over")
        if action not in self.available_actions(self.piles):
            raise ValueError(f"invalid action: {action}")
        pile, count = action
        self.piles[pile] -= count
        if all(value == 0 for value in self.piles):
            self.winner = self.player
        self.player = 1 - self.player
