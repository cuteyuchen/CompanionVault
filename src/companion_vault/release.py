from __future__ import annotations

import json
import zipfile
from pathlib import Path

FIXED_DATE = (2020, 1, 1, 0, 0, 0)


def deterministic_zip(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(path.relative_to(source).as_posix(), FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())


def package_personas(root: Path) -> list[Path]:
    registry = json.loads((root / "dist/registry.json").read_text(encoding="utf-8"))
    output = root / "dist/packages"
    results = []
    for persona in registry["personas"]:
        archive = output / f"{persona['id']}-{persona['version']}.zip"
        deterministic_zip(root / "dist" / persona["id"], archive)
        results.append(archive)
    return results
