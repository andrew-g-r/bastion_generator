import unittest
from bastion.party import generate_party

class PartyTests(unittest.TestCase):
    def test_party_is_reproducible_and_members_are_distinct(self):
        party = generate_party(5, seed=10)
        self.assertEqual(party, generate_party(5, seed=10))
        self.assertEqual(len({c.name for c in party}), 5)
        self.assertGreater(len({c.abilities for c in party}), 1)
    def test_boundaries(self):
        for count in [0, -1, 1001, True]:
            with self.assertRaises(ValueError):
                generate_party(count)
