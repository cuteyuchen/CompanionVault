from pathlib import Path
import companion_vault.state as state


def test_install_and_rollback(tmp_path,monkeypatch):
    monkeypatch.setattr(state,"STATE_DIR",tmp_path/"state");monkeypatch.setattr(state,"STATE_FILE",tmp_path/"state/state.json")
    destination=tmp_path/"SOUL.md";destination.write_text("old",encoding="utf-8")
    state.install_bytes(b"new",destination,"xiaoyou","1.0.0","hermes")
    assert destination.read_text()=="new"
    state.rollback(destination)
    assert destination.read_text()=="old"
