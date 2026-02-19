import random
import unittest
from bastion.formats import render
from bastion.generator import generate

class FormatTests(unittest.TestCase):
    def test_html_never_interprets_names_as_markup(self):
        output = render([generate('<script>alert(1)</script>')], 'html')
        self.assertIn('&lt;script&gt;', output)
        self.assertNotIn('<script>', output)
    def test_csv_defuses_formulas_and_preserves_commas(self):
        import csv, io
        rows = list(csv.reader(io.StringIO(render([generate('=sum(1,2)')], 'csv'))))
        self.assertEqual(rows[1][0], "'=sum(1,2)")
    def test_jsonl_has_one_record_per_character(self):
        import json
        self.assertEqual(len([json.loads(row) for row in render([generate(),generate()], 'jsonl').splitlines()]), 2)
    def test_markdown_escapes_names(self):
        self.assertIn(r'\<script\>', render([generate('<script>')], 'markdown'))
    def test_text_labels_abilities_and_debt(self):
        c = generate('Mira', rng=random.Random(4))
        output = render([c], 'text')
        for field in ['Mira', 'STR', 'DEX', 'CHA', 'Group debt', c.equipment]:
            self.assertIn(field, output)
