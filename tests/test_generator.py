import random
import unittest
from bastion.generator import generate, career_number

class GeneratorTests(unittest.TestCase):
    def test_reproducible_without_mutating_global_random(self):
        random.seed(27)
        before = random.getstate()
        self.assertEqual(generate(rng=random.Random(42)), generate(rng=random.Random(42)))
        self.assertEqual(before, random.getstate())
    def test_original_mapping_boundary_cases(self):
        for abilities, expected in [((3,3,3),1), ((10,10,10),15), ((3,11,9),16), ((18,18,18),94)]:
            self.assertEqual(career_number(abilities), expected)
    def test_many_characters_preserve_starting_ranges(self):
        rng = random.Random(12)
        for _ in range(500):
            c = generate(rng=rng)
            self.assertTrue(all(3 <= a <= 18 for a in c.abilities))
            self.assertTrue(1 <= c.hp <= 6 and 1 <= c.money <= 6)
