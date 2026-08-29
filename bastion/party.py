"""Bounded party generation with one continuous random sequence."""

import random

from .generator import generate


def generate_party(count, *, seed=None, name="Adventurer", **options):
    if type(count) is not int or not 1 <= count <= 1000:
        raise ValueError("Party size must be between 1 and 1000")
    rng = random.Random(seed)
    return [
        generate(name if count == 1 else f"{name} {i + 1}", rng=rng, **options)
        for i in range(count)
    ]


def party_summary(characters, youngest=1):
    if not characters or type(youngest) is not int or not 1 <= youngest <= len(characters):
        raise ValueError("Youngest player must be a 1-based index into the party")
    return {
        "characters": len(characters),
        "total_hp": sum(c.hp for c in characters),
        "total_money": sum(c.money for c in characters),
        "group_debt_pounds": 10000,
        "creditor": characters[youngest - 1].debt,
        "youngest": characters[youngest - 1].name,
    }
