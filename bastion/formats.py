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
    if format == 'html':
        return html_document(characters)
    if format == 'jsonl':
        return '\n'.join(json.dumps(c.to_dict(), ensure_ascii=False) for c in characters)
    if format == 'csv':
        import csv
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['name','career','STR','DEX','CHA','hp','money','notes'])
        for c in characters:
            row = [c.name,c.career,*c.abilities,c.hp,c.money,c.notes]
            writer.writerow(["'"+v if isinstance(v,str) and v.startswith(('=','+','-','@','\t','\r')) else v for v in row])
        return output.getvalue().rstrip('\r\n')
    if format == 'json':
        values = [c.to_dict() for c in characters]
        return json.dumps(values[0] if len(values) == 1 else values, ensure_ascii=False, indent=2)
    if format == 'markdown':
        return '\n\n---\n\n'.join(markdown(c) for c in characters)
    if format == 'text':
        return '\n\n' .join(text(c) for c in characters)
    raise ValueError(f'Unknown output format: {format}')


def markdown(c):
    def escape(value):
        import re
        return re.sub(r'([\\`*_{}\[\]<>()#+.!|>~-])', r'\\\1', value)
    return (f'# {escape(c.name)}\n\n## {escape(c.career)}\n\n'
            f'| STR | DEX | CHA | HP | £ |\n| --- | --- | --- | --- | --- |\n'
            f'| {c.abilities[0]} | {c.abilities[1]} | {c.abilities[2]} | {c.hp} | {c.money} |\n\n'
            + '\n\n'.join(escape(value) for value in [c.description, c.equipment,
              *[item for pair in zip(c.prompts,c.answers) for item in pair],
              'Group debt (if youngest): '+c.debt, 'Notes: '+c.notes]))


def html_document(characters):
    from html import escape
    sheets = ''.join('<article><pre>' + escape(text(c)) + '</pre></article>' for c in characters)
    return ('<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Bastion character sheets</title><style>'
            'body{font:16px system-ui;background:#f5f0e7;color:#222;margin:2rem}'
            'article{max-width:48rem;margin:0 auto 2rem;padding:2rem;background:white;border:1px solid #999}'
            'pre{font:inherit;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.5}'
            '@media print{body{margin:0;background:white}article{break-after:page;border:0;margin:0}}'
            '</style><body>' + sheets + '</body></html>')
