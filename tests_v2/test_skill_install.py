from pathlib import Path

from persona_dock.cli import main
from persona_dock.skill_install import install_skill


def test_install_unified_skill_to_custom_directory(tmp_path: Path) -> None:
    output = install_skill("codex", "global", tmp_path)

    assert output == tmp_path / "persona-builder"
    assert (output / "SKILL.md").is_file()
    assert (output / "references/output-contract.md").is_file()
    assert (output / "references/prompt-contract.md").is_file()
    assert (output / "references/evidence-contract.md").is_file()
    assert (output / "references/memory-contract.md").is_file()
    assert not (tmp_path / "persona-distiller").exists()

    content = (output / "SKILL.md").read_text(encoding="utf-8")
    assert "Create mode" in content
    assert "Distill mode" in content
    assert "Hybrid mode" in content
    assert "personadock pack" in content


def test_cli_skill_install(tmp_path: Path) -> None:
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
    assert (tmp_path / "persona-builder/references/evidence-contract.md").is_file()
    assert not (tmp_path / "persona-distiller").exists()
