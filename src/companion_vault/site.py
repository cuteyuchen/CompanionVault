from __future__ import annotations

import json
import shutil
from pathlib import Path

from .compiler import build_all


def build_site(root: Path, output: Path) -> Path:
    dist = root / "dist"
    registry = build_all(root, dist)
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(root / "site", output)
    (output / "assets").mkdir(parents=True, exist_ok=True)
    (output / "assets/registry.json").write_text(
        json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    shutil.copytree(dist, output / "downloads", dirs_exist_ok=True)
    return output
