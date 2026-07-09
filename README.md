# Bastion Character Workshop

Create Electric Bastionland characters, assemble parties, and keep printable campaign notes. The CLI and local browser app run on Python 3.11+ with **no runtime dependencies**.

```sh
python3 -m pip install .
bastion generate --name Mira --seed 42
bastion serve
```

Open **http://127.0.0.1:8765** for the character workshop. Roll up to 20 characters, choose careers, save parties in your browser, import/export JSON, or print a sheet per character. The server only listens on your own machine.

## Command-line examples

```sh
bastion generate --count 4 --random-name --seed 42 --format markdown
bastion generate --career 11 --abilities 9 12 15 --name Mira
bastion generate --count 4 --seed 42 --manifest --output party.json
bastion render party.json --format html --output party.html
bastion generate --count 4 --seed 42 --party-summary --youngest 2
bastion annotate party.json --notes 'Met the vaultkeeper' --output party-notes.json
bastion careers --search expedition
bastion validate
bastion doctor
bastion roll 3d6 --seed 42
bastion odds
```

Formats: `text`, `json`, `jsonl`, `csv`, `markdown`, `html`. `--output` refuses to replace a file unless `--force` is given. CSV text is escaped to prevent spreadsheet formulas. `compare BEFORE AFTER` compares two single-character JSON saves. All commands have `--help`.

A JSON manifest records the actual random seed, generator version, and catalog fingerprint. The same seed, generator version, catalog, and generation options reproduce a party. `--random-name` uses names from that character's career table. Repeated sample names are possible.

## Rules and content

This is an **unofficial fan utility** by Andrew Russell. Electric Bastionland and its career text belong to their respective creators. See [Chris McDowall's Electric Bastionland free edition](https://www.bastionland.com/2020/04/electric-bastionland-free-edition.html).

The repository contains the original **ten sample careers**, not the full game's career collection. Automatic selection retains this project's original mapping: derive a number from the lowest/highest abilities, then choose the nearest available career ID (lower ID wins ties). This approximation is **not a replacement for the full game's career table**. HP and pocket money each use d6. Each ability uses 3d6. A party has one £10,000 group debt, selected by the youngest player's career; it is not a debt per character.

## Custom careers

Pass `--catalog path/to/careers.json` to `generate`, `careers`, `validate`, or `odds`. The format is a `career` array with unique string IDs `1`–`100`; each entry needs `title`, `desc`, `sample_names`, `get`, `debt1`, `debt2`, and two prompts and six-outcome tables under `tables`. Use the bundled `bastion/data/careers.json` as a format reference. Only include content you are entitled to distribute.

## Python API and compatibility

```python
import random
from bastion.generator import generate
from bastion.party import generate_party

character = generate('Mira', rng=random.Random(42))
party = generate_party(4, seed=42)
```

`from bastion_generator import fail; hero = fail('Mira')` still works. Call `hero.details()` to print a legacy sheet and `hero.notes('...')` to set notes. Object construction no longer prints. New code should use the immutable `Character` record.

## Development

```sh
python3 -m unittest discover -s tests -v
python3 -m pip wheel --no-deps . -w dist
```

Tests cover dice bounds, seeded generation, catalog validation, serialization, file replacement, exports, HTTP errors, and CLI workflows. CI runs on Linux and macOS with Python 3.11 and 3.14. The browser stores parties only when you click Save; use Forget saved party on shared devices.
