"""Command-line character generator."""
import argparse
import json
import random
import sys
from . import __version__
from .generator import generate

def parser():
    root = argparse.ArgumentParser(description='Generate Electric Bastionland sample-career characters')
    root.add_argument('--version', action='version', version=__version__)
    commands = root.add_subparsers(dest='command', required=True)
    create = commands.add_parser('generate', help='Generate a character')
    create.add_argument('--name', default='Adventurer')
    create.add_argument('--seed', type=int)
    return root

def main(argv=None):
    root = parser()
    args = root.parse_args(argv)
    try:
        character = generate(args.name, rng=random.Random(args.seed))
        print(json.dumps(character.to_dict(), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as error:
        root.exit(2, f'error: {error}\n')
    except BrokenPipeError:
        return 0
