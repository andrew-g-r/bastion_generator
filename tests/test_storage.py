from pathlib import Path
import tempfile
import unittest
from bastion.storage import save, load_characters
from bastion.formats import render
from bastion.generator import generate

class StorageTests(unittest.TestCase):
    def test_character_roundtrip_and_version_rejection(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'sheet.json'
            character = generate('Mira')
            save(path, render([character]))
            self.assertEqual(load_characters(path), [character])
            path.write_text('{"schema_version": 9}')
            with self.assertRaises(ValueError):
                load_characters(path)
    def test_no_overwrite_and_atomic_replacement(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'sheet.txt'
            save(path, 'original')
            with self.assertRaises(FileExistsError):
                save(path, 'replacement')
            self.assertEqual(path.read_text(), 'original\n')
            save(path, 'replacement', force=True)
            self.assertEqual(path.read_text(), 'replacement\n')
            self.assertEqual(list(Path(folder).iterdir()), [path])
