import random
import unittest

from bastion.dice import roll


class DiceTests(unittest.TestCase):
    def test_seed_reproduces_rolls(self):
        self.assertEqual(roll("3d6", random.Random(23)), roll("3d6", random.Random(23)))

    def test_invalid_and_unbounded_expressions(self):
        for value in ["0d6", "1d1", "-1d6", "1001d6", "1d10001", "3d6+2", "oops"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                roll(value)

    def test_rolls_are_in_range(self):
        values = roll("1000D6", random.Random(1))
        self.assertEqual(len(values), 1000)
        self.assertEqual(set(values), set(range(1, 7)))
