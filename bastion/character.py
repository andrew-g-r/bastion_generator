"""Versioned character records independent of presentation."""
from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class Character:
    name: str
    abilities: tuple[int, int, int]
    hp: int
    money: int
    career_id: str
    career: str
    description: str
    equipment: str
    debt: str
    prompts: tuple[str, str]
    answers: tuple[str, str]
    notes: str = ''

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip() or len(self.name) > 200:
            raise ValueError('Name must contain 1–200 characters')
        if len(self.abilities) != 3 or any(type(v) is not int or not 3 <= v <= 18 for v in self.abilities):
            raise ValueError('STR, DEX and CHA must each be integers from 3 to 18')
        if type(self.hp) is not int or type(self.money) is not int or not 1 <= self.hp <= 6 or not 1 <= self.money <= 6:
            raise ValueError('Starting HP and money must each be 1–6')
        if len(self.prompts) != 2 or len(self.answers) != 2:
            raise ValueError('Characters require two career prompts and answers')
        for text in [self.career_id, self.career, self.description, self.equipment, self.debt, *self.prompts, *self.answers, self.notes]:
            if not isinstance(text, str):
                raise ValueError('Character text fields must be strings')

    def to_dict(self):
        return {'schema_version': 1, **asdict(self)}
