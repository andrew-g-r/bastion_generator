"""Human-readable and machine-readable character exports."""
import json

def text(character):
    c = character
    return (f'{c.name} — {c.career}\n'
            f'STR {c.abilities[0]} · DEX {c.abilities[1]} · CHA {c.abilities[2]}\n'
            f'HP {c.hp} · Pocket money £{c.money}\n\n{c.description}\n{c.equipment}\n'
            f'\n{c.prompts[0]}\n{c.answers[0]}\n\n{c.prompts[1]}\n{c.answers[1]}\n'
            f'\nGroup debt (if youngest): {c.debt}\nNotes: {c.notes}')

def render(characters, format='json'):
    if format == 'json':
        values = [c.to_dict() for c in characters]
        return json.dumps(values[0] if len(values) == 1 else values, ensure_ascii=False, indent=2)
    if format == 'text':
        return '\n\n' .join(text(c) for c in characters)
    raise ValueError(f'Unknown output format: {format}')
