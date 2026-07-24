from __future__ import annotations

import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .packaging import extract_package, inspect_package

STATE_ROOT = Path.home() / ".personadock"
STATE_FILE = STATE_ROOT / "state.json"
BACKUP_ROOT = STATE_ROOT / "backups"


def default_target(target: str) -> Path:
    if target == "hermes":
        return Path.home() / ".hermes"
    if target == "openclaw":
        return Path.home() / ".openclaw" / "workspace"
    if target == "generic":
        return STATE_ROOT / "agents" / "generic"
    raise ValueError(f"unsupported target: {target}")


def _load_state() -> dict[str, Any]:
    if not STATE_FILE.is_file():
        return {"installations": {}}
    value = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("invalid PersonaDock state")
    value.setdefault("installations", {})
    return value


def _save_state(state: dict[str, Any]) -> None:
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def _copy_with_backup(source: Path, destination: Path, backup_root: Path, managed: list[str], backups: dict[str, str]) -> None:
    relative_key = destination.as_posix()
    if destination.exists():
        backup = backup_root / f"{len(backups):04d}"
        backup.parent.mkdir(parents=True, exist_ok=True)
        if destination.is_dir():
            shutil.copytree(destination, backup)
        else:
            shutil.copy2(destination, backup)
        backups[relative_key] = str(backup)
        if destination.is_dir():
            shutil.rmtree(destination)
        else:
            destination.unlink()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)
    managed.append(relative_key)


def install_package(package: Path, target: str, destination: Path | None = None) -> Path:
    info = inspect_package(package)
    if info["integrity"] != "ok":
        raise ValueError("PersonaPack integrity check failed")
    if target not in info.get("targets", {}):
        raise ValueError(f"package does not contain target {target}")

    destination = (destination or default_target(target)).expanduser().resolve()
    key = f"{target}:{destination}"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = BACKUP_ROOT / info["id"] / timestamp
    managed: list[str] = []
    backups: dict[str, str] = {}

    with tempfile.TemporaryDirectory(prefix="personadock-") as temporary:
        extracted = Path(temporary)
        extract_package(package, extracted)
        source = extracted / "targets" / target
        skill_id = next((p.name for p in (source / "skills").iterdir()), None) if (source / "skills").is_dir() else None

        if target in {"hermes", "openclaw"}:
            _copy_with_backup(source / "SOUL.md", destination / "SOUL.md", backup_root, managed, backups)
            if skill_id:
                _copy_with_backup(
                    source / "skills" / skill_id,
                    destination / "skills" / skill_id,
                    backup_root,
                    managed,
                    backups,
                )
            if (source / "memory").is_dir():
                memory_destination = destination / "memory" / f"personadock-{info['id']}"
                _copy_with_backup(source / "memory", memory_destination, backup_root, managed, backups)
        else:
            _copy_with_backup(source, destination / info["id"], backup_root, managed, backups)

    state = _load_state()
    state["installations"][key] = {
        "id": info["id"],
        "name": info["name"],
        "version": info["version"],
        "target": target,
        "destination": str(destination),
        "package": str(package.expanduser().resolve()),
        "installed_at": timestamp,
        "managed": managed,
        "backups": backups,
    }
    _save_state(state)
    return destination


def _find_record(target: str, destination: Path | None = None) -> tuple[str, dict[str, Any], dict[str, Any]]:
    destination = (destination or default_target(target)).expanduser().resolve()
    key = f"{target}:{destination}"
    state = _load_state()
    record = state.get("installations", {}).get(key)
    if not record:
        raise ValueError(f"no PersonaDock installation found at {destination}")
    return key, state, record


def rollback(target: str, destination: Path | None = None) -> Path:
    key, state, record = _find_record(target, destination)
    for managed_path in record.get("managed", []):
        path = Path(managed_path)
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()
    for destination_path, backup_path in record.get("backups", {}).items():
        source = Path(backup_path)
        destination_path_obj = Path(destination_path)
        destination_path_obj.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination_path_obj)
        elif source.exists():
            shutil.copy2(source, destination_path_obj)
    state["installations"].pop(key, None)
    _save_state(state)
    return Path(record["destination"])


def uninstall(target: str, destination: Path | None = None, restore_previous: bool = True) -> Path:
    if restore_previous:
        return rollback(target, destination)
    key, state, record = _find_record(target, destination)
    for managed_path in record.get("managed", []):
        path = Path(managed_path)
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()
    state["installations"].pop(key, None)
    _save_state(state)
    return Path(record["destination"])


def status() -> list[dict[str, Any]]:
    return list(_load_state().get("installations", {}).values())
