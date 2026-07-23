from pathlib import Path

from companion_vault.compiler import build_all
from companion_vault.core import persona_dirs, validate_persona


def test_all_personas_validate():
    root = Path(__file__).resolve().parents[1]
    for directory in persona_dirs(root):
        assert validate_persona(directory, root) == []


def test_build_all(tmp_path):
    root = Path(__file__).resolve().parents[1]
    registry = build_all(root, tmp_path)
    assert len(registry["personas"]) == 3
    assert (tmp_path / "xiaoyou/hermes/SOUL.md").exists()
    assert (tmp_path / "warm-listener/sillytavern/character.json").exists()
