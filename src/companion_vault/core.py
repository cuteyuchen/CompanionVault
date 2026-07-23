from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

REQUIRED_EXAMPLE_CATEGORIES = {"daily_life", "happiness", "emotional_support", "advice", "disagreement", "conflict_repair", "reunion", "boundary"}


def repo_root(start: Path | None = None) -> Path:
    cursor = (start or Path.cwd()).resolve()
    for candidate in (cursor, *cursor.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "personas").exists(): return candidate
    raise FileNotFoundError("CompanionVault repository root not found")


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict): raise ValueError(f"{path} must contain a YAML object")
    return value


def dump_yaml(value: dict[str, Any]) -> str: return yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=100)
def persona_dirs(root: Path) -> list[Path]: return sorted(p.parent for p in (root / "personas").glob("*/*/persona.yaml"))


def validate_persona(directory: Path, root: Path) -> list[str]:
    errors=[]
    for filename in ["persona.yaml","examples.yaml","tests.yaml","README.md"]:
        if not (directory/filename).exists(): errors.append(f"missing {filename}")
    if errors: return errors
    persona=load_yaml(directory/"persona.yaml"); schema=json.loads((root/"schemas/persona.schema.json").read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(persona): errors.append("persona.yaml: "+"/".join(map(str,error.path))+": "+error.message)
    examples=load_yaml(directory/"examples.yaml").get("examples",[])
    if len(examples)<10: errors.append("examples.yaml must contain at least 10 examples")
    missing=REQUIRED_EXAMPLE_CATEGORIES-{e.get("category") for e in examples if isinstance(e,dict)}
    if missing: errors.append("missing example categories: "+", ".join(sorted(missing)))
    ids=[e.get("id") for e in examples if isinstance(e,dict)]
    if len(ids)!=len(set(ids)): errors.append("example ids must be unique")
    pending=[e.get("id","unknown") for e in examples if isinstance(e,dict) and e.get("review_required") is True]
    if pending: errors.append("examples still require human review: "+", ".join(pending))
    provenance=persona.get("provenance",{})
    if provenance.get("mode")=="public" and provenance.get("consent") not in {"self","authorized","public"}: errors.append("public distilled personas require self, authorized, or public-source consent")
    if provenance.get("raw_content_committed") is True: errors.append("raw chat content must never be committed to a public persona")
    if len(load_yaml(directory/"tests.yaml").get("tests",[]))<6: errors.append("tests.yaml must contain at least 6 behavior tests")
    return errors


def sha256_text(text: str) -> str: return hashlib.sha256(text.encode("utf-8")).hexdigest()
