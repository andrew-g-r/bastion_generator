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
    def test_sample_names_follow_the_seed(self):
        a = generate(random_name=True, rng=random.Random(12))
        self.assertNotEqual(a.name, 'Adventurer')
        self.assertEqual(a, generate(random_name=True, rng=random.Random(12)))
    def test_manual_abilities_are_preserved(self):
        self.assertEqual(generate(abilities=(3, 12, 18)).abilities, (3, 12, 18))
        with self.assertRaises(ValueError):
            generate(abilities=(1, 20, 8))
    def test_explicit_career_and_unknown_id(self):
        self.assertEqual(generate(career='91').career_id, '91')
        with self.assertRaises(ValueError):
            generate(career='404')
    def test_many_characters_preserve_starting_ranges(self):
        rng = random.Random(12)
        for _ in range(500):
            c = generate(rng=rng)
            self.assertTrue(all(3 <= a <= 18 for a in c.abilities))
            self.assertTrue(1 <= c.hp <= 6 and 1 <= c.money <= 6)
