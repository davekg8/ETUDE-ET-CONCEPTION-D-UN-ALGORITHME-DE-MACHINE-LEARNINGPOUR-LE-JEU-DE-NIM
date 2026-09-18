import unittest

from nim_rl.game import NimGame


class NimGameTests(unittest.TestCase):
    def test_available_actions(self):
        self.assertEqual(NimGame.available_actions((1, 2)), {(0, 1), (1, 1), (1, 2)})

    def test_last_move_wins(self):
        game = NimGame([1])
        game.move((0, 1))
        self.assertEqual(game.winner, 0)

    def test_invalid_move(self):
        game = NimGame([1])
        with self.assertRaises(ValueError):
            game.move((0, 2))


if __name__ == "__main__":
    unittest.main()
