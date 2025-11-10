"""Command-line character generator."""
import argparse
import json
import random
import sys
from . import __version__
from .party import generate_party
from .formats import render

def parser():
    root = argparse.ArgumentParser(description='Generate Electric Bastionland sample-career characters')
    root.add_argument('--version', action='version', version=__version__)
    commands = root.add_subparsers(dest='command', required=True)
    create = commands.add_parser('generate', help='Generate a character')
    create.add_argument('--name', default='Adventurer')
    create.add_argument('--career', help='Choose a career ID from the catalog')
    create.add_argument('--abilities', type=int, nargs=3, metavar=('STR','DEX','CHA'))
    create.add_argument('--seed', type=int)
    create.add_argument('--count', type=int, default=1)
    create.add_argument('--format', choices=['json','text','markdown','jsonl','csv'], default='text')
    return root

def main(argv=None):
    root = parser()
    args = root.parse_args(argv)
    try:
        characters = generate_party(args.count, seed=args.seed, name=args.name, career=args.career, abilities=args.abilities)
        print(render(characters, args.format))
        return 0
    except (ValueError, OSError) as error:
        root.exit(2, f'error: {error}\n')
    except BrokenPipeError:
        return 0
