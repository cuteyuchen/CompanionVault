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

SKILLS = ("persona-builder", "persona-distiller")
SKILL_SELECTIONS = ("all", *SKILLS)


def _source_checkout(start: Path | None = None) -> Path | None:
    cursor = (start or Path.cwd()).expanduser().resolve()
    for candidate in (cursor, *cursor.parents):
        if not (candidate / "pyproject.toml").is_file():
            continue
        if all((candidate / "skills" / skill / "SKILL.md").is_file() for skill in SKILLS):
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


def _install_one(skill: str, base: Path, source_root: Path | None) -> Path:
    output = base / skill
    if output.exists():
        shutil.rmtree(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    source = source_root / "skills" / skill if source_root else None
    if source and source.is_dir():
        shutil.copytree(source, output)
    else:
        bundled = resources.files("persona_dock").joinpath("data", skill)
        _copy_traversable(bundled, output)
    return output


def install_skills(
    target: str,
    scope: str = "global",
    skill: str = "all",
    destination: Path | None = None,
    checkout: Path | None = None,
) -> list[Path]:
    if target not in TARGETS:
        raise ValueError(f"unsupported skill target: {target}")
    if scope not in {"project", "global"}:
        raise ValueError("scope must be project or global")
    if skill not in SKILL_SELECTIONS:
        raise ValueError(f"unsupported Skill selection: {skill}")

    base = (destination or TARGETS[target][scope]).expanduser().resolve()
    source_root = checkout or _source_checkout()
    selected = SKILLS if skill == "all" else (skill,)
    return [_install_one(name, base, source_root) for name in selected]
