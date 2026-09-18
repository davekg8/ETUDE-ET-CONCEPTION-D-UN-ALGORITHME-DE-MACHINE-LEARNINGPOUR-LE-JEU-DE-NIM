import math
import random
import time
import matplotlib.pyplot as plt

GRAPH_SMOOTHING=100

class Nim():
    def __init__(self, initial=[1, 3, 5, 7]):
        """
        Initialize game board.
        Each game board has
            - `piles`: a list of how many elements remain in each pile
            - `player`: 0 or 1 to indicate which player's turn
            - `winner`: None, 0, or 1 to indicate who the winner is
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Nim.available_actions(piles) takes a `piles` list as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of removing `j` items
        from pile `i` (where piles are 0-indexed).
        """
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Nim.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player
        self.switch_player()

class NimAI():

    def __init__(self, alpha=0.1, epsilon=0.8):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """

        if (tuple(state),action) in self.q:
            return self.q[(tuple(state),action)]
        else:
            return 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        self.q[(tuple(state),action)] = old_q + self.alpha*(reward + future_rewards - old_q)

    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """

        actions = Nim.available_actions(state)
        if not actions:
            return 0

        max_q = float('-inf')
        for action in actions:
            q_value = self.get_q_value(state, action)
            max_q = max(max_q, q_value)

        if max_q == float('-inf'):
            return 0
        else:
            return max_q

    def choose_action(self, state, epsilon=False):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        actions = Nim.available_actions(state)
        if not actions:
            return None

        if epsilon and random.random() < self.epsilon:
            return random.choice(list(actions))

        max_q = float('-inf')
        best_actions = []
        for action in actions:
            q_value = self.get_q_value(state, action)
            if q_value > max_q:
                max_q = q_value
                best_actions = [action]
            elif q_value == max_q:
                best_actions.append(action)

        return random.choice(best_actions)

class OptimalPlayer:

    def __init__(self, player=0, epsilon=0.2):
        self.epsilon = epsilon
        self.player = player

    def set_player(self, player=0, j=-1):
        self.player = player
        if j != -1:
            self.player = 0 if j % 2 == 0 else 1

    def randomMove(self, piles):
        piles_avail = [i for i in range(len(piles)) if piles[i] > 0]
        chosen_pile = random.choice(piles_avail)
        n_obj = random.choice(range(1, piles[chosen_pile] + 1))
        return (chosen_pile, n_obj)

    def compute_nim_sum(self, piles):
        nim = 0
        for i in piles:
            nim = nim ^ i
        return nim

    def act(self, piles, **kwargs):
        if random.random() < self.epsilon:
            return self.randomMove(piles)

        else:
            nim_sum = self.compute_nim_sum(piles)
            if nim_sum == 0:
                count_non_0 = sum(x > 0 for x in piles)
                if count_non_0 == 0:
                    return (-1, -1)
                else:
                    return (piles.index(max(piles)), 1)

            for index, pile in enumerate(piles):
                target_size = pile ^ nim_sum
                if target_size < pile:
                    amount_to_remove = pile - target_size
                    return (index, amount_to_remove)




def train_smart(n=4000):
    """
    Train the AI by playing `n` games against the smart bot.
    Return the trained AI and a PNG image showing the training progress.
    """

    ai=NimAI()
    opti=OptimalPlayer()
    # Initialize performance tracking
    wins = []
    episodes = []

    for episode in range(1, n + 1):
        # Initialize new game
        game = Nim([random.randint(1,10),random.randint(1,10),random.randint(1,10),random.randint(1,10)])
        last = {
            "state": None,
            "action": None
        }

        # Run the game
        while True:
            # Get current state
            state = game.piles.copy()

            # If the game is over, record the result
            if game.winner is not None:
                if game.winner == 0:
                    reward = 1
                else:
                    reward = -1

                # Update Q-value
                if last["state"] is not None:
                    ai.update(last["state"], last["action"], state, reward)

                wins.append(1 if game.winner == 0 else 0)
                episodes.append(episode)
                break

            # Choose action
            if game.player == 0:
                action = ai.choose_action(state)
            else:
                action = None
                while action is None:
                    action = opti.act(state)

            # Keep track of last action
            if game.player == 0 and last["state"] is not None:
                ai.update(last["state"], last["action"], state, 0)

            last["state"] = state
            last["action"] = action

            # Make move
            game.move(action)

    # Plot training progress
    q_win_x = []
    q_win_y = []
    for x in range(GRAPH_SMOOTHING, len(wins)):
        values_to_average = wins[max(0, x - GRAPH_SMOOTHING):x+1]
        rolling_average = float(sum(values_to_average)) / len(values_to_average)
        q_win_y.append(rolling_average)
        q_win_x.append(x)
    plt.plot(q_win_x, q_win_y, label="Q-Learner Win Rate")
    plt.fill_between(q_win_x, 0, q_win_y, label="Q-Learner Win Rate")
    plt.title("Win Rate (Rolling Window Size = " + str(GRAPH_SMOOTHING) +" Games)")
    plt.savefig("result.png")

    plt.scatter(episodes, wins)
    plt.xlabel("Episode")
    plt.ylabel("Wins")
    plt.title("Training Progress of NimAI")
    plt.savefig("nim_ai_evolution.png")
    plt.show()

    return ai




def train(n):
    '''
    Train an AI by playing `n` games against itself.
    '''
    wins=[]
    episodes=[]
    player = NimAI()

    # Play n games
    for epi in range(n):
        # print(f"Playing training game {epi + 1}")
        game = Nim()


        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                wins.append(0 if game.winner == 0 else 1)
                episodes.append(epi)
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    # Plot training progress
    q_win_x = []
    q_win_y = []
    for x in range(GRAPH_SMOOTHING, len(wins)):
        values_to_average = wins[max(0, x - GRAPH_SMOOTHING):x+1]
        rolling_average = float(sum(values_to_average)) / len(values_to_average)
        q_win_y.append(rolling_average)
        q_win_x.append(x)
    plt.plot(q_win_x, q_win_y, label="Q-Learner Win Rate")
    plt.fill_between(q_win_x, 0, q_win_y, label="Q-Learner Win Rate",alpha=0.6)
    plt.title("Win Rate (Rolling Window Size = " + str(GRAPH_SMOOTHING) +" Games)")
    plt.savefig("first.png")

    plt.scatter(episodes, wins)
    plt.xlabel("Episode")
    plt.ylabel("Wins")
    plt.title("Training Progress of NimAI")
    plt.show()
    plt.savefig("nim_ai_training_progress.png")
    # Return the trained AI
    return player


def play(ai, human_player=None):
    '''
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    '''

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim([random.randint(1,10),random.randint(1,10),random.randint(1,10),random.randint(1,10)])

    # Game loop
    while True:

        # Print contents of piles
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()

        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Let human make a move
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI make a move
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Make move
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return


def test(ai=NimAI()):
    """
    Train the AI by playing `n` games against the smart bot.
    Return the trained AI and a PNG image showing the training progress.
    """
    # Initialize performance tracking
    wins = []
    episodes = []

    # Initialize new game
    game = Nim()
    last = {
        "state": None,
        "action": None
    }

    # Run the game
    while True:
        # Get current state
        state = game.piles.copy()

        # If the game is over, record the result
        if game.winner is not None:
            if game.winner == 0:
                reward = 1
            else:
                reward = -1

            # Update Q-value
            if last["state"] is not None:
                ai.update(last["state"], last["action"], state, reward)

            return 1 if game.winner == 0 else 0

        # Choose action
        if game.player == 0:
            action = ai.choose_action(state)
        else:
            action = None
            while action is None:
                action = smartMove(state)

        # Keep track of last action
        if game.player == 0 and last["state"] is not None:
            ai.update(last["state"], last["action"], state, 0)

        last["state"] = state
        last["action"] = action

        # Make move
        game.move(action)

