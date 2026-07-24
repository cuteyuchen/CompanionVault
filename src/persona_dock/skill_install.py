from __future__ import annotations

import shutil
from importlib import resources
from pathlib import Path
from typing import Any

TARGETS = {
    "codex": {
        "project": Path(".codex/skills"),
        "global": Path.home() / ".codex/skills",
    },
    "claude": {
        "project": Path(".claude/skills"),
        "global": Path.home() / ".claude/skills",
    },
    "opencode": {
        "project": Path(".opencode/skills"),
        "global": Path.home() / ".config/opencode/skills",
    },
    "agents": {
        "project": Path(".agents/skills"),
        "global": Path.home() / ".agents/skills",
    },
    "generic": {
        "project": Path("skills"),
        "global": Path.home() / ".local/share/agent-skills",
    },
}

SKILL_NAME = "persona-builder"


def _source_checkout(start: Path | None = None) -> Path | None:
    cursor = (start or Path.cwd()).expanduser().resolve()
    for candidate in (cursor, *cursor.parents):
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "skills" / SKILL_NAME / "SKILL.md"
        ).is_file():
            return candidate
    return None


def _copy_traversable(source: Any, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for child in source.iterdir():
        target = destination / child.name
        if child.is_dir():
            _copy_traversable(child, target)
        else:
            target.write_bytes(child.read_bytes())


def install_skill(
    target: str,
    scope: str = "global",
    destination: Path | None = None,
    checkout: Path | None = None,
) -> Path:
    if target not in TARGETS:
        raise ValueError(f"unsupported skill target: {target}")
    if scope not in {"project", "global"}:
        raise ValueError("scope must be project or global")

    base = (destination or TARGETS[target][scope]).expanduser().resolve()
    output = base / SKILL_NAME
    if output.exists():
        shutil.rmtree(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    source_root = checkout or _source_checkout()
    source = source_root / "skills" / SKILL_NAME if source_root else None
    if source and source.is_dir():
        shutil.copytree(source, output)
    else:
        bundled = resources.files("persona_dock").joinpath("data", SKILL_NAME)
        _copy_traversable(bundled, output)
    return output
