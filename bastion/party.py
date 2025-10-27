"""Bounded party generation with one continuous random sequence."""
import random
from .generator import generate

def generate_party(count, *, seed=None, name='Adventurer', **options):
    if type(count) is not int or not 1 <= count <= 1000:
        raise ValueError('Party size must be between 1 and 1000')
    rng = random.Random(seed)
    return [generate(name if count == 1 else f'{name} {i+1}', rng=rng, **options) for i in range(count)]
