import importlib.util
import unittest
from pathlib import Path


class LegacyTests(unittest.TestCase):
    def test_import_loads_bundled_catalog(self):
        path = Path(__file__).resolve().parents[1] / "bastion_generator.py"
        spec = importlib.util.spec_from_file_location("legacy", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(len(module.data["career"]), 10)
        character = module.fail("Mira")
        self.assertEqual(len(character.stats), 6)
        self.assertEqual(
            character.job_data["tables"]["table1"][str(character.stats[4][0])],
            character.job_answer1,
        )
        self.assertEqual(
            character.job_data["tables"]["table2"][str(character.stats[5][0])],
            character.job_answer2,
        )
        character.notes("first")
        character.notes("second")
        self.assertEqual(character.data["notes"], "second")
