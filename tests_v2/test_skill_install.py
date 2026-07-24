from pathlib import Path

from persona_dock.cli import main
from persona_dock.skill_install import install_skills


def test_install_all_skills_to_custom_directory(tmp_path: Path) -> None:
    outputs = install_skills("codex", "global", "all", tmp_path)

    assert [path.name for path in outputs] == ["persona-builder", "persona-distiller"]
    assert (tmp_path / "persona-builder/SKILL.md").is_file()
    assert (tmp_path / "persona-builder/references/prompt-contract.md").is_file()
    assert (tmp_path / "persona-builder/references/memory-contract.md").is_file()
    assert (tmp_path / "persona-distiller/SKILL.md").is_file()
    assert (tmp_path / "persona-distiller/references/output-contract.md").is_file()
    assert (tmp_path / "persona-distiller/references/memory-contract.md").is_file()


def test_install_single_skill(tmp_path: Path) -> None:
    outputs = install_skills("generic", "project", "persona-builder", tmp_path)

    assert outputs == [tmp_path / "persona-builder"]
    assert (tmp_path / "persona-builder/SKILL.md").is_file()
    assert not (tmp_path / "persona-distiller").exists()


def test_cli_skill_install_defaults_to_all(tmp_path: Path) -> None:
    assert main(
        [
            "skill",
            "install",
            "--target",
            "generic",
            "--scope",
            "project",
            "--path",
            str(tmp_path),
        ]
    ) == 0
    assert (tmp_path / "persona-builder/SKILL.md").is_file()
    assert (tmp_path / "persona-distiller/SKILL.md").is_file()


def test_cli_skill_install_selects_one(tmp_path: Path) -> None:
    assert main(
        [
            "skill",
            "install",
            "--target",
            "generic",
            "--scope",
            "project",
            "--skill",
            "persona-builder",
            "--path",
            str(tmp_path),
        ]
    ) == 0
    assert (tmp_path / "persona-builder/SKILL.md").is_file()
    assert not (tmp_path / "persona-distiller").exists()
