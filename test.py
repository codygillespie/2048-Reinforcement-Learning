import unittest

from game import GameState


class TestGameMove(unittest.TestCase):
    def test_move_up_simple(self):
        input: GameState = GameState([0, 0, 0, 0,
                                       0, 0, 2, 0,
                                       0, 0, 0, 0,
                                       0, 2, 0, 0])
        expected: GameState = GameState([0, 2, 2, 0,
                                      0, 0, 0, 0,
                                      0, 0, 0, 0,
                                      0, 0, 0, 0])
        self.assertListEqual(input.up().cells, expected.cells)

    def test_move_down_simple(self):
        input: GameState = GameState([0, 0, 0, 0,
                                       0, 0, 2, 0,
                                       0, 0, 0, 0,
                                       0, 2, 0, 0])
        expected: GameState = GameState([0, 0, 0, 0,
                                      0, 0, 0, 0,
                                      0, 0, 0, 0,
                                      0, 2, 2, 0])
        self.assertListEqual(input.down().cells, expected.cells)

    def test_move_left_simple(self):
        input: GameState = GameState([0, 0, 0, 0,
                                       0, 0, 2, 0,
                                       0, 0, 0, 0,
                                       0, 2, 0, 0])
        expected: GameState = GameState([0, 0, 0, 0,
                                      2, 0, 0, 0,
                                      0, 0, 0, 0,
                                      2, 0, 0, 0])
        self.assertListEqual(input.left().cells, expected.cells)

    def test_move_right_simple(self):
            input: GameState = GameState([0, 0, 0, 0,
                                          0, 0, 2, 0,
                                          0, 0, 0, 0,
                                          0, 2, 0, 0])
            expected: GameState = GameState([0, 0, 0, 0,
                                             0, 0, 0, 2,
                                             0, 0, 0, 0,
                                             0, 0, 0, 2])
            self.assertListEqual(input.right().cells, expected.cells)

    def test_merge_down_simple(self):
            input: GameState = GameState([0, 0, 0, 2,
                                           0, 0, 0, 2,
                                           0, 0, 0, 0,
                                           0, 0, 2, 2])
            expected: GameState = GameState([0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 0, 2,
                                          0, 0, 2, 4])
            self.assertListEqual(input.down().cells, expected.cells)

    def test_merge_right_simple(self):
            before: GameState = GameState([0, 0, 0, 0,
                                           0, 0, 0, 0,
                                           0, 2, 2, 2,
                                           0, 4, 4, 4])
            after: GameState = GameState([0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 2, 4,
                                          0, 0, 4, 8])
            self.assertListEqual(before.right().cells, after.cells)