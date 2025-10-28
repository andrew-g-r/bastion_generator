"""Character generation using the original sample-career mapping."""
import random
from .catalog import load_catalog
from .character import Character
from .dice import roll

def career_number(abilities):
    low, high = min(abilities), max(abilities)
    if high >= 12:
        return high % 10 * 10 + 2 + min(low, 12)
    if high == 11:
        return 13 + low
    if high == 10:
        return low + 5
    return low - 2

def generate(name='Adventurer', *, rng=None, catalog=None, career=None):
    rng = rng if rng is not None else random.Random()
    catalog = catalog if catalog is not None else load_catalog()
    abilities = tuple(sum(roll('3d6', rng)) for _ in range(3))
    number = career_number(abilities)
    key = min(catalog, key=lambda k: (abs(int(k)-number), int(k)))
    if career is not None:
        key = str(career)
        if key not in catalog:
            raise ValueError(f'Unknown career ID: {key}')
    entry = catalog[key]
    hp, money, first, second = (roll('1d6', rng)[0] for _ in range(4))
    tables = entry['tables']
    return Character(name, abilities, hp, money, key, entry['title'], entry['desc'], entry['get'],
                     entry['debt2'], (tables['prompt1'], tables['prompt2']),
                     (tables['table1'][str(first)], tables['table2'][str(second)]))
