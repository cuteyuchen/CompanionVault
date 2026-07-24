from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .io import load_jsonl, load_yaml, sha256_file, write_jsonl
from .project import PROJECT_FILE, find_project, validate_project


def _bullets(values: list[Any]) -> str:
    return "\n".join(f"- {value}" for value in values)


def compile_soul(project: dict[str, Any]) -> str:
    soul = project["soul"]
    skill_id = project["skill"]["id"]
    triggers = soul.get("skill_triggers", [])
    boundaries = soul.get("boundaries", [])
    traits = soul.get("core_traits", [])
    return f"""# {project['name']}

## 身份

{soul['identity']}

## 核心人格

{_bullets(traits)}

## 表达

{soul['voice']}

## 不可违反的边界

{_bullets(boundaries)}

## 人格 Skill 路由

你拥有 `{skill_id}` Skill。以下情况应使用该 Skill：

{_bullets(triggers)}

涉及过去经历、用户偏好、共同事件或关系事实时，先检索 Memory。没有可靠记忆时必须明确不确定，不得补全或假装记得。

SOUL 只负责稳定身份、路由和边界；详细场景、表达示例和关系处理规则由人格 Skill 提供。
""".strip() + "\n"


def _memory_markdown(profile: dict[str, Any], records: list[dict[str, Any]], limit: int = 2200) -> str:
    sections = ["# PersonaDock Memory Seed", ""]
    for key, title in [
        ("user_preferences", "用户偏好"),
        ("relationship_facts", "关系事实"),
        ("notes", "其他说明"),
    ]:
        values = profile.get(key, [])
        if values:
            sections.extend([f"## {title}", "", *[f"- {value}" for value in values], ""])
    reviewed = [item for item in records if item.get("reviewed") is True]
    if reviewed:
        sections.extend(["## 已审核记忆", ""])
        for item in reviewed:
            summary = item.get("summary") or item.get("text") or ""
            sections.append(f"- [{item.get('id', 'memory')}] {summary}")
    content = "\n".join(sections).strip() + "\n"
    if len(content) <= limit:
        return content
    suffix = "\n\n> 更多记忆保存在 seed.jsonl，应按需检索。\n"
    return content[: max(0, limit - len(suffix))].rstrip() + suffix


def _copy_skill(root: Path, target: Path, project: dict[str, Any]) -> None:
    source = root / "skills/persona"
    destination = target / "skills" / project["skill"]["id"]
    shutil.copytree(source, destination, dirs_exist_ok=True)


def _copy_memory(root: Path, target: Path, project: dict[str, Any]) -> None:
    profile = load_yaml(root / "memory/profile.yaml")
    records = load_jsonl(root / "memory/seed.jsonl")
    reviewed = [record for record in records if record.get("reviewed") is True]
    memory_dir = target / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    (memory_dir / "MEMORY.md").write_text(_memory_markdown(profile, reviewed), encoding="utf-8")
    write_jsonl(memory_dir / "seed.jsonl", reviewed)
    shutil.copy2(root / "memory/policy.yaml", memory_dir / "policy.yaml")


def compile_project(root: Path, output: Path | None = None, targets: list[str] | None = None) -> Path:
    root = find_project(root)
    errors = validate_project(root)
    if errors:
        raise ValueError("invalid persona project:\n- " + "\n- ".join(errors))
    project = load_yaml(root / PROJECT_FILE)
    selected = targets or list(project.get("targets", []))
    supported = {"hermes", "openclaw", "generic"}
    unknown = set(selected) - supported
    if unknown:
        raise ValueError(f"unsupported targets: {', '.join(sorted(unknown))}")

    output = (output or root / ".personadock/build").expanduser().resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    soul = compile_soul(project)
    hard_limit = int(project["soul"].get("hard_limit_chars", 2800))
    if len(soul) > hard_limit:
        raise ValueError(f"compiled SOUL is {len(soul)} characters; hard limit is {hard_limit}")

    target_manifest: dict[str, Any] = {}
    for target_name in selected:
        target = output / "targets" / target_name
        target.mkdir(parents=True, exist_ok=True)
        if target_name in {"hermes", "openclaw"}:
            (target / "SOUL.md").write_text(soul, encoding="utf-8")
            _copy_skill(root, target, project)
            if project.get("memory", {}).get("enabled", True):
                _copy_memory(root, target, project)
        elif target_name == "generic":
            skill = (root / "skills/persona/SKILL.md").read_text(encoding="utf-8")
            prompt = soul + "\n\n---\n\n" + skill
            (target / "system-prompt.md").write_text(prompt, encoding="utf-8")
            _copy_memory(root, target, project)
        target_manifest[target_name] = {
            "path": f"targets/{target_name}",
            "soul_chars": len(soul),
        }

    source_dir = output / "source"
    source_dir.mkdir()
    shutil.copy2(root / PROJECT_FILE, source_dir / PROJECT_FILE)
    shutil.copytree(root / "tests", output / "tests", dirs_exist_ok=True)

    files: dict[str, str] = {}
    for path in sorted(p for p in output.rglob("*") if p.is_file()):
        if path.name == "manifest.json":
            continue
        files[path.relative_to(output).as_posix()] = sha256_file(path)
    manifest = {
        "format": "personapack",
        "format_version": 1,
        "schema_version": 2,
        "id": project["id"],
        "name": project["name"],
        "version": project["version"],
        "locale": project["locale"],
        "summary": project["summary"],
        "targets": target_manifest,
        "privacy": {
            "raw_chat_included": False,
            "memory_policy": project.get("memory", {}).get("bundle_policy", "reviewed"),
        },
        "files": files,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    return output
