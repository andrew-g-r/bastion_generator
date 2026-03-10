import unittest
from bastion.odds import career_probabilities

class OddsTests(unittest.TestCase):
    def test_all_possible_dice_outcomes_are_accounted_for(self):
        results = career_probabilities()
        self.assertEqual(sum(row['outcomes'] for row in results), 216**3)
        self.assertAlmostEqual(sum(row['probability'] for row in results), 1)
        self.assertEqual(len(results), 10)
