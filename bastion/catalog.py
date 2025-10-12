"""Load and validate the bundled sample careers or a custom catalog."""
import json
from pathlib import Path

DEFAULT_CATALOG = Path(__file__).with_name('data') / 'careers.json'
REQUIRED = ('id', 'title', 'desc', 'sample_names', 'get', 'debt1', 'debt2')

def load_catalog(path: str | Path | None = None) -> dict[str, dict]:
    source = Path(path) if path is not None else DEFAULT_CATALOG
    raw = json.loads(source.read_text(encoding='utf-8'))
    if not isinstance(raw, dict) or not isinstance(raw.get('career'), list) or not raw['career']:
        raise ValueError('Catalog must contain a nonempty career list')
    result = {}
    for entry in raw['career']:
        if not isinstance(entry, dict) or any(not isinstance(entry.get(k), str) or not entry[k].strip() for k in REQUIRED):
            raise ValueError('Every career requires nonempty text fields: ' + ', '.join(REQUIRED))
        key = entry['id']
        if not key.isdecimal() or not 1 <= int(key) <= 100 or str(int(key)) != key or key in result:
            raise ValueError(f'Career ID must be unique and between 1 and 100: {key}')
        tables = entry.get('tables')
        if not isinstance(tables, dict):
            raise ValueError(f'Career {key} requires tables')
        for n in (1, 2):
            table = tables.get(f'table{n}')
            prompt = tables.get(f'prompt{n}')
            if not isinstance(prompt, str) or not prompt.strip() or not isinstance(table, dict):
                raise ValueError(f'Career {key} has an invalid prompt or table {n}')
            if set(table) != set('123456') or any(not isinstance(v, str) or not v.strip() for v in table.values()):
                raise ValueError(f'Career {key} table {n} must define all six die outcomes')
        result[key] = entry
    return result
