from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path
from typing import Any

from .compiler import compile_project
from .io import sha256_file
from .project import find_project

FIXED_DATE = (2020, 1, 1, 0, 0, 0)


def _write_zip(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(path.relative_to(source).as_posix(), FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())


def pack_project(root: Path, destination: Path | None = None, targets: list[str] | None = None) -> Path:
    root = find_project(root)
    build = compile_project(root, targets=targets)
    manifest = json.loads((build / "manifest.json").read_text(encoding="utf-8"))
    destination = destination or root / "dist" / f"{manifest['id']}-{manifest['version']}.personapack"
    destination = destination.expanduser().resolve()
    _write_zip(build, destination)
    return destination


def inspect_package(package: Path) -> dict[str, Any]:
    package = package.expanduser().resolve()
    with zipfile.ZipFile(package) as archive:
        names = set(archive.namelist())
        if "manifest.json" not in names:
            raise ValueError("not a PersonaPack: manifest.json is missing")
        manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
        expected = manifest.get("files", {})
        mismatches: list[str] = []
        for name, digest in expected.items():
            if name not in names:
                mismatches.append(f"missing {name}")
                continue
            import hashlib

            actual = hashlib.sha256(archive.read(name)).hexdigest()
            if actual != digest:
                mismatches.append(f"checksum mismatch: {name}")
        manifest["integrity"] = "ok" if not mismatches else "failed"
        manifest["integrity_errors"] = mismatches
        manifest["package_sha256"] = sha256_file(package)
        return manifest


def extract_package(package: Path, destination: Path) -> dict[str, Any]:
    info = inspect_package(package)
    if info["integrity"] != "ok":
        raise ValueError("PersonaPack integrity check failed")
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package) as archive:
        for member in archive.infolist():
            path = Path(member.filename)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"unsafe package path: {member.filename}")
        archive.extractall(destination)
    return info


def export_public(root: Path, destination: Path | None = None) -> Path:
    root = find_project(root)
    build = compile_project(root)
    manifest = json.loads((build / "manifest.json").read_text(encoding="utf-8"))
    destination = destination or root / "dist" / f"{manifest['id']}-{manifest['version']}-public"
    destination = destination.expanduser().resolve()
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(build, destination)
    for memory_file in destination.glob("targets/*/memory/seed.jsonl"):
        memory_file.write_text("", encoding="utf-8")
    for memory_md in destination.glob("targets/*/memory/MEMORY.md"):
        memory_md.write_text("# Public PersonaPack\n\nPrivate memory was removed.\n", encoding="utf-8")
    manifest_path = destination / "manifest.json"
    public_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    public_manifest["privacy"]["memory_policy"] = "none"
    public_manifest["files"] = {
        path.relative_to(destination).as_posix(): sha256_file(path)
        for path in sorted(p for p in destination.rglob("*") if p.is_file() and p.name != "manifest.json")
    }
    manifest_path.write_text(json.dumps(public_manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return destination
