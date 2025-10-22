import unittest
from bastion.character import Character

class CharacterTests(unittest.TestCase):
    def test_invalid_abilities_fail_early(self):
        with self.assertRaises(ValueError):
            Character('A', (1, 9, 9), 1, 1, '1', 'Job', '', '', '', ('',''), ('',''))
    def test_json_schema_version(self):
        c = Character('A', (9, 9, 9), 1, 1, '1', 'Job', '', '', '', ('',''), ('',''))
        self.assertEqual(c.to_dict()['schema_version'], 1)
