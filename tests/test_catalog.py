import json
import tempfile
import unittest
from pathlib import Path

from bastion.catalog import DEFAULT_CATALOG, load_catalog


class CatalogTests(unittest.TestCase):
    def test_bundled_catalog_is_complete(self):
        self.assertEqual(set(load_catalog()), {str(n) for n in range(1, 100, 10)})

    def test_duplicate_and_incomplete_tables_are_rejected(self):
        raw = json.loads(DEFAULT_CATALOG.read_text())
        for broken in [{"career": [raw["career"][0], raw["career"][0]]}, {"career": []}]:
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "catalog.json"
                path.write_text(json.dumps(broken))
                with self.assertRaises(ValueError):
                    load_catalog(path)
