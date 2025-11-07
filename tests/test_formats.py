import random
import unittest
from bastion.formats import render
from bastion.generator import generate

class FormatTests(unittest.TestCase):
    def test_text_labels_abilities_and_debt(self):
        c = generate('Mira', rng=random.Random(4))
        output = render([c], 'text')
        for field in ['Mira', 'STR', 'DEX', 'CHA', 'Group debt', c.equipment]:
            self.assertIn(field, output)
