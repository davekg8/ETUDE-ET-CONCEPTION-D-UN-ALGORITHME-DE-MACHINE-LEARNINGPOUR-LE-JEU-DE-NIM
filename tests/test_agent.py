import unittest

from nim_rl.agent import QLearningAgent


class AgentTests(unittest.TestCase):
    def test_q_update(self):
        agent = QLearningAgent(alpha=0.5, epsilon=0, seed=1)
        agent.update((1,), (0, 1), (0,), 1.0)
        self.assertEqual(agent.value((1,), (0, 1)), 0.5)

    def test_greedy_action(self):
        agent = QLearningAgent(epsilon=0, seed=1)
        agent.q[((1, 2), (1, 2))] = 2.0
        self.assertEqual(agent.choose_action((1, 2), explore=False), (1, 2))


if __name__ == "__main__":
    unittest.main()
