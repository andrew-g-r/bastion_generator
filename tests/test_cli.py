import json
import subprocess
import sys
import unittest

class CLITests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, '-m', 'bastion', *args], capture_output=True, text=True)
    def test_generation_and_seed(self):
        result = self.run_cli('generate', '--name', 'Mira', '--seed', '42', '--format', 'json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['name'], 'Mira')
        self.assertEqual(result.stdout, self.run_cli('generate', '--name', 'Mira', '--seed', '42', '--format', 'json').stdout)
    def test_manifest_records_a_reusable_seed(self):
        result = self.run_cli('generate','--manifest')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        repeat = json.loads(self.run_cli('generate','--manifest','--seed',str(data['seed'])).stdout)
        self.assertEqual(data, repeat)
    def test_validate_bundled_catalog(self):
        result = self.run_cli('validate')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('10 careers', result.stdout)
    def test_search_careers(self):
        result = self.run_cli('careers','--search','gutter')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('GUTTER MINDER', result.stdout)
        self.assertNotIn('STAR BLESSED', result.stdout)
    def test_unknown_option_is_an_error(self):
        self.assertEqual(self.run_cli('generate', '--wat').returncode, 2)
