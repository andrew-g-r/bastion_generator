"""Command-line character generator."""
import argparse
import json
import random
import sys
from . import __version__
from .party import generate_party

def parser():
    root = argparse.ArgumentParser(description='Generate Electric Bastionland sample-career characters')
    root.add_argument('--version', action='version', version=__version__)
    commands = root.add_subparsers(dest='command', required=True)
    create = commands.add_parser('generate', help='Generate a character')
    create.add_argument('--name', default='Adventurer')
    create.add_argument('--career', help='Choose a career ID from the catalog')
    create.add_argument('--seed', type=int)
    create.add_argument('--count', type=int, default=1)
    return root

def main(argv=None):
    root = parser()
    args = root.parse_args(argv)
    try:
        characters = generate_party(args.count, seed=args.seed, name=args.name, career=args.career)
        data = characters[0].to_dict() if args.count == 1 else [c.to_dict() for c in characters]
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as error:
        root.exit(2, f'error: {error}\n')
    except BrokenPipeError:
        return 0
