from pathlib import Path
import tempfile
import unittest
from bastion.storage import save

class StorageTests(unittest.TestCase):
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
