"""Compatibility API; new applications should import from bastion."""

import pprint

from bastion.catalog import load_catalog
from bastion.dice import roll
from bastion.generator import generate

data = {"career": list(load_catalog().values())}


def closest(k, lst=None):
    choices = lst if lst is not None else list(range(1, 100, 10))
    if not choices:
        raise ValueError("At least one career ID is required")
    return str(min(choices, key=lambda value: (abs(value - k), value)))


def stats():
    return [sum(roll("3d6")) for _ in range(3)]


def json_seek(id_):
    return load_catalog().get(str(id_))


def make_job():
    c = generate()
    return c.career_id, list(c.abilities), [c.hp], [c.money], roll("1d6"), roll("1d6")


class fail:
    kind = "Failed Career"

    def __init__(self, name):
        c = generate(name)
        self.name = name
        self.character = c
        self.job = c.career_id
        self.job_data = json_seek(self.job)
        self.job_title = c.career
        self.job_desc = c.description
        self.job_get = c.equipment
        self.job_debt1 = self.job_data["debt1"]
        self.job_debt2 = c.debt
        self.job_prompt1, self.job_prompt2 = c.prompts
        self.job_answer1, self.job_answer2 = c.answers
        table_rolls = [
            [int(next(key for key, value in self.job_data["tables"][f"table{i+1}"].items() if value == answer))]
            for i, answer in enumerate(c.answers)
        ]
        self.stats = (c.career_id, list(c.abilities), [c.hp], [c.money], *table_rolls)
        self.data = {
            "name": name,
            "career": c.career,
            "desc": c.description,
            "stats": list(c.abilities),
            "hp": [c.hp],
            "pocket money": [c.money],
            "get": c.equipment,
            "debt1": self.job_debt1,
            "debt2": c.debt,
            "prompt1": c.prompts[0],
            "answer1": c.answers[0],
            "prompt2": c.prompts[1],
            "answer2": c.answers[1],
        }

    def notes(self, text):
        self.data["notes"] = str(text)

    def details(self):
        pprint.pp(self.data, sort_dicts=False)
        return self.data


if __name__ == "__main__":
    from bastion.cli import main

    raise SystemExit(main())
