import importlib.util
from pathlib import Path
import unittest

class LegacyTests(unittest.TestCase):
    def test_import_loads_bundled_catalog(self):
        path = Path(__file__).resolve().parents[1] / 'bastion_generator.py'
        spec = importlib.util.spec_from_file_location('legacy', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(len(module.data['career']), 10)
        character = module.fail('Mira')
        character.notes('first')
        character.notes('second')
        self.assertEqual(character.data['notes'], 'second')
