import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "bastion", *map(str, args)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def test_generate_annotate_render_and_compare(self):
        with tempfile.TemporaryDirectory() as folder:
            original = Path(folder) / "one.json"
            edited = Path(folder) / "two.json"
            for args in [
                ("generate", "--seed", 42, "--manifest", "--output", original),
                ("annotate", original, "--notes", "Found a map", "--output", edited),
            ]:
                result = self.cli(*args)
                self.assertEqual(result.returncode, 0, result.stderr)
            changes = self.cli("compare", original, edited)
            self.assertEqual(set(json.loads(changes.stdout)), {"notes"})
            result = self.cli("render", edited, "--format", "html")
            self.assertIn("Found a map", result.stdout)
            self.assertEqual(self.cli("generate", "--output", original).returncode, 2)

    def test_legacy_import_from_another_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            code = f'import sys; sys.path.insert(0, {str(ROOT)!r}); from bastion_generator import fail; c=fail("Mira"); assert c.name=="Mira"'
            result = subprocess.run(
                [sys.executable, "-c", code], cwd=folder, capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
