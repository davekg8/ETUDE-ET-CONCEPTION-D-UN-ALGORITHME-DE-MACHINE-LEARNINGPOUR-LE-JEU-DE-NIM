import math
import random
import time
import matplotlib.pyplot as plt
import pandas as pd

GRAPH_SMOOTHING = 100

class Nim:
    def __init__(self, initial=[1, 2, 5, 7]):
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        return 0 if player == 1 else 1

    def switch_player(self):
        self.player = Nim.other_player(self.player)

    def move(self, action):
        pile, count = action
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")
        self.piles[pile] -= count
        self.switch_player()
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player

class NimAI:
    def __init__(self, alpha=0.1, epsilon=0.8):
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        return self.q.get((tuple(state), action), 0)

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        self.q[(tuple(state), action)] = old_q + self.alpha * (reward + future_rewards - old_q)

    def best_future_reward(self, state):
        actions = Nim.available_actions(state)
        if not actions:
            return 0
        return max(self.get_q_value(state, action) for action in actions)

    def choose_action(self, state, epsilon=True):
        actions = Nim.available_actions(state)
        if not actions:
            return None
        if epsilon and random.random() < self.epsilon:
            return random.choice(list(actions))
        return max(actions, key=lambda action: self.get_q_value(state, action))

def smart_move(board):
    def winning_position(a):
        q = (a[0] ^ a[1] ^ a[2] ^ a[3]) == 0
        r = (a[0] | a[1] | a[2] | a[3]) == 1
        return q ^ r

    for i, pile in enumerate(board):
        for j in range(1, pile + 1):
            board[i] -= j
            if winning_position(board):
                return i, j
            board[i] += j
    return random.choice(list(Nim.available_actions(board)))

def train_smart(ai=NimAI(), n=100000):
    wins = []
    for episode in range(1, n + 1):
        game = Nim()
        last = {"state": None, "action": None}
        while True:
            state = game.piles.copy()
            if game.winner is not None:
                reward = 1 if game.winner == 0 else -1
                if last["state"] is not None:
                    ai.update(last["state"], last["action"], state, reward)
                wins.append(1 if game.winner == 0 else 0)
                break
            if game.player == 0:
                action = ai.choose_action(state)
            else:
                action = smart_move(state)
            if game.player == 0 and last["state"] is not None:
                ai.update(last["state"], last["action"], state, 0)
            last["state"] = state
            last["action"] = action
            game.move(action)

    # Utilisation de pandas pour une moyenne mobile
    win_series = pd.Series(wins)
    win_rate = win_series.rolling(GRAPH_SMOOTHING).mean()

    plt.plot(win_rate, label="Q-Learner Win Rate")
    plt.fill_between(win_rate.index, 0, win_rate, alpha=0.2)
    plt.title(f"Win Rate (Rolling Window Size = {GRAPH_SMOOTHING} Games)")
    plt.xlabel("Games Played")
    plt.ylabel("Win Rate")
    plt.legend()
    plt.show()
    return ai

def play(ai, human_player=None):
    if human_player is None:
        human_player = random.randint(0, 1)
    game = Nim()
    while True:
        print("\nPiles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")
        game.move((pile, count))
        if game.winner is not None:
            print("\nGAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return
