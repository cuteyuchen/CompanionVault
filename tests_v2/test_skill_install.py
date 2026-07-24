from pathlib import Path

from persona_dock.cli import main
from persona_dock.skill_install import install_distiller_skill


def test_install_distiller_skill_to_custom_directory(tmp_path: Path) -> None:
    output = install_distiller_skill("codex", "global", tmp_path)
    assert output == tmp_path / "persona-distiller"
    assert (output / "SKILL.md").is_file()
    assert (output / "references/output-contract.md").is_file()
    assert (output / "references/memory-contract.md").is_file()
    content = (output / "SKILL.md").read_text(encoding="utf-8")
    assert "personadock pack" in content
    assert "built-in distill command is optional" in content


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
    assert (tmp_path / "persona-distiller/SKILL.md").is_file()
