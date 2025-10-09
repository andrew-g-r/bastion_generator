"""Bounded dice expressions with isolated random number generators."""
import random
import re

def roll(expression: str, rng: random.Random | None = None) -> list[int]:
    match = re.fullmatch(r'(\d+)[dD](\d+)', expression.strip())
    if not match:
        raise ValueError('Dice must use NdM notation, such as 3d6')
    count, sides = map(int, match.groups())
    if not 1 <= count <= 1000 or not 2 <= sides <= 10000:
        raise ValueError('Use 1–1000 dice with 2–10000 sides')
    generator = rng if rng is not None else random.Random()
    return [generator.randint(1, sides) for _ in range(count)]
