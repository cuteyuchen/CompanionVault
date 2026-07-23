from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

REQUIRED_EXAMPLE_CATEGORIES = {
    "daily_life", "happiness", "emotional_support", "advice",
    "disagreement", "conflict_repair", "reunion", "boundary",
}


def repo_root(start: Path | None = None) -> Path:
    cursor = (start or Path.cwd()).resolve()
    for candidate in (cursor, *cursor.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "personas").exists():
            return candidate
    raise FileNotFoundError("CompanionVault repository root not found")


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return value


def dump_yaml(value: dict[str, Any]) -> str:
    return yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=100)


def persona_dirs(root: Path) -> list[Path]:
    return sorted(p.parent for p in (root / "personas").glob("*/*/persona.yaml"))


def validate_persona(directory: Path, root: Path) -> list[str]:
    errors: list[str] = []
    required = ["persona.yaml", "examples.yaml", "tests.yaml", "README.md"]
    for filename in required:
        if not (directory / filename).exists():
            errors.append(f"missing {filename}")
    if errors:
        return errors

    persona = load_yaml(directory / "persona.yaml")
    schema = json.loads((root / "schemas/persona.schema.json").read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(persona):
        errors.append("persona.yaml: " + "/".join(map(str, error.path)) + ": " + error.message)

    examples = load_yaml(directory / "examples.yaml").get("examples", [])
    if len(examples) < 10:
        errors.append("examples.yaml must contain at least 10 examples")
    categories = {e.get("category") for e in examples if isinstance(e, dict)}
    missing_categories = REQUIRED_EXAMPLE_CATEGORIES - categories
    if missing_categories:
        errors.append("missing example categories: " + ", ".join(sorted(missing_categories)))
    ids = [e.get("id") for e in examples if isinstance(e, dict)]
    if len(ids) != len(set(ids)):
        errors.append("example ids must be unique")

    tests = load_yaml(directory / "tests.yaml").get("tests", [])
    if len(tests) < 6:
        errors.append("tests.yaml must contain at least 6 behavior tests")
    return errors


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
