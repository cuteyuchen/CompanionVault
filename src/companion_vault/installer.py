from __future__ import annotations

from pathlib import Path

from .catalog import fetch_artifact, load_registry
from .state import install_bytes


def default_target(target: str) -> Path:
    if target == "hermes": return Path.home() / ".hermes" / "SOUL.md"
    if target == "generic": return Path.cwd() / "system-prompt.md"
    if target == "sillytavern": return Path.cwd() / "character.json"
    raise ValueError(f"unsupported target: {target}")


def install_catalog_persona(persona_id: str, target: str, destination: Path | None = None, base_url: str | None = None) -> Path:
    registry, base = load_registry(base_url) if base_url else load_registry()
    match = next((p for p in registry["personas"] if p["id"] == persona_id), None)
    if not match: raise KeyError(persona_id)
    asset = match["files"][target]["path"]
    return install_bytes(fetch_artifact(base, asset), destination or default_target(target), persona_id, match["version"], target)
