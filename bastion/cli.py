"""Command-line character generator."""
import argparse
import json
import random
import sys
from . import __version__
from .party import generate_party, party_summary
from .formats import render
from .storage import save, load_characters
from .catalog import load_catalog

def parser():
    root = argparse.ArgumentParser(description='Generate Electric Bastionland sample-career characters')
    root.add_argument('--version', action='version', version=__version__)
    commands = root.add_subparsers(dest='command', required=True)
    create = commands.add_parser('generate', help='Generate a character')
    create.add_argument('--name', default='Adventurer')
    create.add_argument('--output', help='Save to a file instead of stdout')
    create.add_argument('--force', action='store_true', help='Replace an existing output file')
    create.add_argument('--career', help='Choose a career ID from the catalog')
    create.add_argument('--abilities', type=int, nargs=3, metavar=('STR','DEX','CHA'))
    create.add_argument('--seed', type=int)
    create.add_argument('--party-summary', action='store_true', help='Output party totals and group debt as JSON')
    create.add_argument('--youngest', type=int, default=1, help='1-based youngest player index for group debt')
    create.add_argument('--random-name', action='store_true', help='Use a career-specific sample name')
    create.add_argument('--count', type=int, default=1)
    create.add_argument('--format', choices=['json','text','markdown','jsonl','csv','html'], default='text')
    careers = commands.add_parser('careers', help='List or search available careers')
    careers.add_argument('--search', default='')
    validate = commands.add_parser('validate', help='Validate a custom or bundled career catalog')
    for command in (create, careers, validate):
        command.add_argument('--catalog', help='Path to a career catalog JSON file')
    convert = commands.add_parser('render', help='Render saved JSON characters in another format')
    convert.add_argument('source')
    convert.add_argument('--format', choices=['json','text','markdown','jsonl','csv','html'], default='text')
    convert.add_argument('--output')
    convert.add_argument('--force', action='store_true')
    annotate = commands.add_parser('annotate', help='Set notes on saved characters')
    annotate.add_argument('source')
    annotate.add_argument('--notes', required=True)
    annotate.add_argument('--output', required=True)
    annotate.add_argument('--force', action='store_true')
    return root

def main(argv=None):
    root = parser()
    args = root.parse_args(argv)
    try:
        if args.command == 'annotate':
            from dataclasses import replace
            characters = [replace(c, notes=args.notes) for c in load_characters(args.source)]
            save(args.output, render(characters, 'json'), force=args.force)
            return 0
        if args.command == 'render':
            output = render(load_characters(args.source), args.format)
            if args.output:
                save(args.output, output, force=args.force)
            else:
                print(output)
            return 0
        catalog = load_catalog(args.catalog)
        if args.command == 'validate':
            print(f'Valid catalog: {len(catalog)} careers')
            return 0
        if args.command == 'careers':
            entries = catalog.values()
            print('\n'.join(f"{entry['id']:>3}  {entry['title']}" for entry in entries if args.search.casefold() in entry['title'].casefold()))
            return 0
        characters = generate_party(args.count, seed=args.seed, name=args.name, catalog=catalog, career=args.career, abilities=args.abilities, random_name=args.random_name)
        output = json.dumps(party_summary(characters, args.youngest), ensure_ascii=False, indent=2) if args.party_summary else render(characters, args.format)
        if args.output:
            save(args.output, output, force=args.force)
        else:
            print(output)
        return 0
    except (ValueError, OSError) as error:
        root.exit(2, f'error: {error}\n')
    except BrokenPipeError:
        return 0
