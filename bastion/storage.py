"""Atomic exports that refuse to overwrite existing sheets by default."""

import os
import tempfile
from pathlib import Path


def save(path, content, *, force=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(content + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        if force:
            os.replace(temporary, path)
        else:
            os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def load_characters(path):
    import json

    from .character import Character

    source = Path(path)
    if source.stat().st_size > 5_000_000:
        raise ValueError("Character file exceeds the 5 MB limit")
    raw = json.loads(source.read_text(encoding="utf-8"))
    if isinstance(raw, dict) and "characters" in raw:
        if raw.get("schema_version") != 1:
            raise ValueError("Unsupported party manifest version")
        raw = raw["characters"]
    items = raw if isinstance(raw, list) else [raw]
    if not 1 <= len(items) <= 1000:
        raise ValueError("Character files must contain 1–1000 characters")
    characters = []
    for value in items:
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            raise ValueError("Unsupported character schema; expected schema_version 1")
        data = {k: v for k, v in value.items() if k != "schema_version"}
        try:
            for key in ("abilities", "prompts", "answers"):
                data[key] = tuple(data[key])
            characters.append(Character(**data))
        except (TypeError, KeyError) as error:
            raise ValueError(f"Invalid character record: {error}") from error
    return characters
