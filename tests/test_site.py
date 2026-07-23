from pathlib import Path
import hashlib

from companion_vault.compiler import build_all
from companion_vault.release import package_personas
from companion_vault.site import build_site


def test_site_build(tmp_path):
    root = Path(__file__).resolve().parents[1]
    out = build_site(root, tmp_path / "site")
    assert (out / "index.html").exists()
    assert (out / "assets/registry.json").exists()


def test_packages_are_reproducible(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[1]
    build_all(root, root / "dist")
    files1 = package_personas(root)
    hashes1 = [hashlib.sha256(p.read_bytes()).hexdigest() for p in files1]
    files2 = package_personas(root)
    hashes2 = [hashlib.sha256(p.read_bytes()).hexdigest() for p in files2]
    assert hashes1 == hashes2
