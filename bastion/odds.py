"""Exact probabilities for the bundled nearest-career selection rule."""

from collections import Counter
from itertools import product

from .catalog import load_catalog
from .generator import career_number


def career_probabilities(catalog=None):
    catalog = load_catalog() if catalog is None else catalog
    weights = Counter(map(sum, product(range(1, 7), repeat=3)))
    counts = Counter()
    for abilities in product(weights, repeat=3):
        number = career_number(abilities)
        key = min(catalog, key=lambda key: (abs(int(key) - number), int(key)))
        counts[key] += weights[abilities[0]] * weights[abilities[1]] * weights[abilities[2]]
    total = 216**3
    return [
        {
            "id": key,
            "career": catalog[key]["title"],
            "outcomes": counts[key],
            "total_outcomes": total,
            "probability": counts[key] / total,
        }
        for key in sorted(catalog, key=int)
    ]
