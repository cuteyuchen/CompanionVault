from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def default_target(target: str) -> Path:
    if target == "hermes":
        return Path.home() / ".hermes" / "SOUL.md"
    if target == "generic":
        return Path.cwd() / "system-prompt.md"
    if target == "sillytavern":
        return Path.cwd() / "character.json"
    raise ValueError(f"unsupported target: {target}")


def install_from_dist(root: Path, persona_id: str, target: str, destination: Path | None = None) -> Path:
    mapping = {"hermes": "hermes/SOUL.md", "generic": "generic/system-prompt.md", "sillytavern": "sillytavern/character.json"}
    source = root / "dist" / persona_id / mapping[target]
    if not source.exists():
        raise FileNotFoundError(f"build artifact not found: {source}; run companion-vault build first")
    destination = destination or default_target(target)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        backup = destination.with_name(destination.name + f".backup-{stamp}")
        shutil.copy2(destination, backup)
    shutil.copy2(source, destination)
    state_dir = Path.home() / ".companion-vault"
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "installation.json").write_text(json.dumps({
        "persona": persona_id, "target": target, "destination": str(destination),
        "installed_at": datetime.now(timezone.utc).isoformat(),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return destination
