from pathlib import Path

from persona_dock.cli import main


def test_cli_local_flow(tmp_path: Path, capsys) -> None:
    root = tmp_path / "local-persona"
    assert main(["init", str(root), "--id", "local-persona", "--name", "本地人格"]) == 0
    assert main(["validate", str(root)]) == 0
    assert main(["build", str(root), "--target", "hermes"]) == 0
    package = tmp_path / "local.personapack"
    assert main(["pack", str(root), "--target", "hermes", "--output", str(package)]) == 0
    assert main(["inspect", str(package)]) == 0
    output = capsys.readouterr().out
    assert "local-persona" in output
