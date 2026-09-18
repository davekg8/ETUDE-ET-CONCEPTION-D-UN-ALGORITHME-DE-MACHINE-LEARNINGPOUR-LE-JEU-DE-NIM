# Nim AI — Reinforcement Learning with Q-Learning

> An experimental reinforcement learning project exploring how an AI agent can learn to play the mathematical game of Nim through experience.

## Overview

This project studies the **Game of Nim** as a simple environment for experimenting with **reinforcement learning**.

Instead of explicitly programming the optimal strategy into the learning agent, the goal is to let an AI progressively learn which actions are valuable by repeatedly playing the game and updating its decisions using **Q-Learning**.

The project was originally developed as part of a **TIPE academic project** and includes several experiments around learning strategies, self-play and comparison against a mathematically informed opponent.

## The Game of Nim

Nim is a two-player mathematical strategy game. The board consists of several piles of objects. At each turn, a player selects one pile and removes one or more objects from it. In this implementation, the player taking the last object wins.

A typical state can be represented as:

```text
[1, 3, 5, 7]
```

An action is represented by `(pile_index, number_of_objects_removed)`. For example, `(2, 3)` means removing three objects from the third pile.

Despite its simple rules, Nim is particularly interesting for reinforcement learning because an **optimal mathematical strategy is known**, making it possible to compare a learned policy with a strong reference strategy.

## Reinforcement Learning Approach

The main agent is implemented using **Q-Learning**. Each state-action pair is associated with a Q-value, `Q(state, action)`, estimating the long-term value of performing that action.

The agent updates its Q-values according to:

```text
Q(s, a) ← Q(s, a) + α × [r + max Q(s', a') − Q(s, a)]
```

where `α` is the learning rate, `r` the reward, `s'` the next state, and `max Q(s', a')` the best estimated future reward.

The learned knowledge is stored in a Python dictionary mapping:

```text
(state, action) -> Q-value
```

This provides a simple and interpretable implementation of tabular reinforcement learning.

## Exploration vs Exploitation

The agent supports an **ε-greedy strategy**. During exploration, it can choose a random legal action instead of the action with the highest known Q-value.

This creates the classic trade-off between **exploration**, discovering potentially better strategies, and **exploitation**, using actions that already appear effective. The behaviour can be controlled through the `epsilon` parameter.

## Training Strategies

### Self-play

The Q-learning agent can learn by playing repeated games against itself. Neither side initially knows the optimal strategy; knowledge progressively emerges from rewards obtained after winning or losing games.

### Training against a strong opponent

A second experiment trains the Q-learning agent against an opponent implementing the mathematical strategy of Nim.

The opponent computes the **Nim-sum** of the piles using XOR operations and attempts to move the game toward a theoretically favourable state:

```python
nim_sum = pile_1 ^ pile_2 ^ ... ^ pile_n
```

This provides a stronger training opponent than purely random self-play and makes it possible to study how the learning agent behaves against a strategy derived from the mathematical structure of the game.

## Performance Tracking

Training performance is monitored by recording game outcomes over successive episodes.

Because individual wins and losses are noisy, the project also computes a rolling win rate over a configurable window:

```python
GRAPH_SMOOTHING = 100
```

The resulting plots make it possible to visualize how the behaviour of the Q-learning agent evolves during training. Several experimental figures and training results are available in `TIPE/tipepresentation/`.

## Human vs AI

The project also contains an interactive mode where a trained agent can play against a human player directly from the terminal.

At each turn, the current piles are displayed and the player selects a pile and the number of objects to remove. The AI then chooses its move according to the Q-values learned during training.

## Project Structure

```text
.
├── README.md
├── pyproject.toml
├── src/
│   └── nim_rl/
│       ├── game.py        # Nim environment and legal actions
│       ├── agent.py       # Tabular Q-learning agent
│       ├── opponents.py   # Random and deterministic Nim-sum policies
│       ├── training.py    # Training loop with real epsilon-greedy exploration
│       └── evaluation.py  # Deterministic evaluation separated from training
├── tests/
│   ├── test_game.py
│   └── test_agent.py
└── TIPE/                  # Original academic work preserved as an archive
```

The original TIPE implementation remains available for traceability, while the maintained code is organized as a small Python package under `src/nim_rl`. The refactor separates the game, learning agent, opponents, training and evaluation concerns and adds basic automated tests.

The modernized training loop explicitly enables epsilon-greedy exploration. Evaluation disables exploration and is kept separate from training. The Nim-sum opponent is deterministic, unlike the historical experimental opponent which deliberately included random moves.

## Technologies

- **Python**
- **Q-Learning**
- **Reinforcement Learning**
- **Matplotlib**
- **Game Theory**
- **Nim-Sum / XOR strategy**

## What This Project Explores

Beyond implementing the game itself, this project explores several fundamental machine-learning concepts:

- modelling a problem as **states, actions and rewards**;
- implementing tabular Q-Learning from scratch;
- balancing exploration and exploitation;
- training an agent through repeated interactions;
- experimenting with self-play;
- comparing a learned strategy with a mathematically derived opponent;
- monitoring learning behaviour through experimental metrics and visualizations.

The project illustrates how a relatively simple mathematical game can be used as a controlled environment to understand the foundations of **reinforcement learning and sequential decision-making**.

## Limitations

This project is primarily an educational and experimental implementation.

The Q-table approach works well for a small discrete environment such as Nim, but it does not scale efficiently when the state space becomes very large.

A natural extension would therefore be to replace the tabular representation with function approximation or a neural network and compare the resulting agent with the classical Q-Learning implementation.

## Author

**David Egbakou**

Data Science & Machine Learning
