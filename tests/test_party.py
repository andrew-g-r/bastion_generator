import unittest

from bastion.party import generate_party, party_summary


class PartyTests(unittest.TestCase):
    def test_party_is_reproducible_and_members_are_distinct(self):
        party = generate_party(5, seed=10)
        self.assertEqual(party, generate_party(5, seed=10))
        self.assertEqual(len({c.name for c in party}), 5)
        self.assertGreater(len({c.abilities for c in party}), 1)

    def test_group_debt_uses_youngest_player_once(self):
        party = generate_party(3, seed=8)
        summary = party_summary(party, 2)
        self.assertEqual(summary["creditor"], party[1].debt)
        self.assertEqual(summary["group_debt_pounds"], 10000)
        with self.assertRaises(ValueError):
            party_summary(party, 0)

    def test_boundaries(self):
        for count in [0, -1, 1001, True]:
            with self.assertRaises(ValueError):
                generate_party(count)
