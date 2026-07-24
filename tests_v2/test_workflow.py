from __future__ import annotations

import json
from pathlib import Path

import pytest

from persona_dock.compiler import compile_project
from persona_dock.installer import install_package, rollback
from persona_dock.packaging import export_public, inspect_package, pack_project
from persona_dock.project import init_project, validate_project


def reviewed_memory() -> str:
    return json.dumps(
        {
            "id": "mem-1",
            "type": "preference",
            "summary": "用户更喜欢先被倾听，再讨论解决方案。",
            "reviewed": True,
            "sensitivity": "private",
        },
        ensure_ascii=False,
    ) + "\n"


def test_init_validate_build_and_pack(tmp_path: Path) -> None:
    root = init_project(tmp_path / "my-persona", "my-persona", "小岚")
    (root / "memory/seed.jsonl").write_text(reviewed_memory(), encoding="utf-8")

    assert validate_project(root) == []
    build = compile_project(root)
    soul = (build / "targets/hermes/SOUL.md").read_text(encoding="utf-8")
    assert "人格 Skill 路由" in soul
    assert "不得补全或假装记得" in soul
    assert (build / "targets/openclaw/skills/my-persona-persona/SKILL.md").is_file()
    assert (build / "targets/hermes/memory/seed.jsonl").read_text(encoding="utf-8")

    package = pack_project(root)
    assert package.suffix == ".personapack"
    metadata = inspect_package(package)
    assert metadata["integrity"] == "ok"
    assert metadata["id"] == "my-persona"


def test_unreviewed_memory_blocks_build(tmp_path: Path) -> None:
    root = init_project(tmp_path / "persona", "persona", "测试人格")
    candidate = json.loads(reviewed_memory())
    candidate["reviewed"] = False
    (root / "memory/seed.jsonl").write_text(json.dumps(candidate, ensure_ascii=False) + "\n", encoding="utf-8")
    errors = validate_project(root)
    assert any("explicitly reviewed" in error for error in errors)
    with pytest.raises(ValueError):
        compile_project(root)


def test_public_export_removes_memory(tmp_path: Path) -> None:
    root = init_project(tmp_path / "persona", "persona", "测试人格")
    (root / "memory/seed.jsonl").write_text(reviewed_memory(), encoding="utf-8")
    output = export_public(root)
    assert (output / "targets/hermes/memory/seed.jsonl").read_text(encoding="utf-8") == ""
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["privacy"]["memory_policy"] == "none"


def test_install_and_rollback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = init_project(tmp_path / "persona", "persona", "测试人格")
    package = pack_project(root)

    import persona_dock.installer as installer

    monkeypatch.setattr(installer, "STATE_ROOT", tmp_path / "state")
    monkeypatch.setattr(installer, "STATE_FILE", tmp_path / "state/state.json")
    monkeypatch.setattr(installer, "BACKUP_ROOT", tmp_path / "state/backups")

    destination = tmp_path / "hermes"
    destination.mkdir()
    (destination / "SOUL.md").write_text("old soul\n", encoding="utf-8")

    install_package(package, "hermes", destination)
    assert "人格 Skill 路由" in (destination / "SOUL.md").read_text(encoding="utf-8")
    assert (destination / "skills/persona-persona/SKILL.md").is_file()

    rollback("hermes", destination)
    assert (destination / "SOUL.md").read_text(encoding="utf-8") == "old soul\n"
    assert not (destination / "skills/persona-persona").exists()
