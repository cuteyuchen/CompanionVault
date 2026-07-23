from __future__ import annotations

import json
import urllib.request
from pathlib import Path

DEFAULT_BASE = "https://cuteyuchen.github.io/CompanionVault"


def local_root() -> Path | None:
    cursor = Path.cwd().resolve()
    for candidate in (cursor, *cursor.parents):
        if (candidate / "personas").exists() and (candidate / "pyproject.toml").exists():
            return candidate
    return None


def load_registry(base_url: str = DEFAULT_BASE) -> tuple[dict, str]:
    root = local_root()
    if root and (root / "dist/registry.json").exists():
        return json.loads((root / "dist/registry.json").read_text(encoding="utf-8")), (root / "dist").as_uri()
    with urllib.request.urlopen(base_url.rstrip("/") + "/assets/registry.json", timeout=20) as response:
        return json.load(response), base_url.rstrip("/") + "/downloads"


def fetch_artifact(base: str, relative_path: str) -> bytes:
    if base.startswith("file:"):
        from urllib.parse import urlparse
        return (Path(urlparse(base).path) / relative_path).read_bytes()
    with urllib.request.urlopen(base.rstrip("/") + "/" + relative_path, timeout=30) as response:
        return response.read()
