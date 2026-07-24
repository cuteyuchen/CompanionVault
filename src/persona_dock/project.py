from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .io import dump_yaml, load_jsonl, load_yaml

PROJECT_FILE = "companion.yaml"
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def find_project(start: Path | None = None) -> Path:
    cursor = (start or Path.cwd()).expanduser().resolve()
    if cursor.is_file():
        cursor = cursor.parent
    for candidate in (cursor, *cursor.parents):
        if (candidate / PROJECT_FILE).is_file():
            return candidate
    raise FileNotFoundError(f"{PROJECT_FILE} not found from {cursor}")


def _default_companion(persona_id: str, name: str, locale: str) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "id": persona_id,
        "version": "0.1.0",
        "name": name,
        "locale": locale,
        "summary": f"{name} 是一个由 PersonaDock 管理的私有 AI 人格。",
        "soul": {
            "identity": f"你是{name}，是用户自行创建并拥有的 AI 人格。",
            "core_traits": ["真诚", "自然", "尊重用户边界"],
            "voice": "使用自然、具体、不机械的表达。",
            "boundaries": [
                "不虚构共同经历或用户信息",
                "不施加排他性或依赖压力",
                "涉及专业风险时明确能力边界",
            ],
            "skill_triggers": [
                "需要体现该人格独特语气或行为时",
                "涉及情绪支持、关系冲突或特殊场景时",
                "用户提到过去经历、偏好或长期关系信息时",
            ],
            "target_chars": 1800,
            "hard_limit_chars": 2800,
        },
        "skill": {
            "id": f"{persona_id}-persona",
            "description": f"{name} 的详细人格行为、场景和表达参考。",
        },
        "memory": {
            "enabled": True,
            "private_by_default": True,
            "bundle_policy": "reviewed",
            "never_invent": True,
        },
        "targets": ["hermes", "openclaw", "generic"],
    }


def init_project(destination: Path, persona_id: str, name: str, locale: str = "zh-CN", force: bool = False) -> Path:
    destination = destination.expanduser().resolve()
    if not ID_PATTERN.fullmatch(persona_id):
        raise ValueError("id must use lowercase letters, digits, and hyphens")
    if destination.exists() and any(destination.iterdir()) and not force:
        raise FileExistsError(f"destination is not empty: {destination}")

    destination.mkdir(parents=True, exist_ok=True)
    for relative in [
        "soul",
        "skills/persona/references",
        "memory",
        "tests",
        ".private/raw",
    ]:
        (destination / relative).mkdir(parents=True, exist_ok=True)

    (destination / PROJECT_FILE).write_text(
        dump_yaml(_default_companion(persona_id, name, locale)), encoding="utf-8"
    )
    (destination / "skills/persona/SKILL.md").write_text(
        f"""---
name: {persona_id}-persona
description: {name} 的详细人格行为、场景与表达规则。
---

# {name} 人格 Skill

## 何时使用

- 当前回复需要体现{name}的独特人格，而不仅是通用助手能力。
- 用户需要情绪陪伴、关系处理、冲突修复或特定场景回应。
- 用户提到过去经历或长期偏好；此时先检索记忆，找不到则明确不确定。

## 响应流程

1. 判断当前场景。
2. 按需读取 `references/` 中对应文件。
3. 涉及过去事实时先检索 Memory，不得虚构。
4. 根据 `references/voice.md` 统一最终表达。
5. 不照抄示例，提取其表达规律。
""",
        encoding="utf-8",
    )
    references = {
        "voice.md": f"# {name} 的表达方式\n\n- 自然口语。\n- 避免模板化安慰。\n- 根据用户情绪调整回复长度。\n",
        "emotional-support.md": "# 情绪支持\n\n先确认用户感受，再判断用户需要倾听、陪伴还是建议。\n",
        "conflict-repair.md": "# 冲突修复\n\n承认具体问题，不转移责任，允许用户解释并共同确认下一步。\n",
        "daily-scenarios.md": "# 日常场景\n\n在轻松聊天、分享日常和共同活动中保持稳定人格。\n",
        "relationship-stages.md": "# 关系阶段\n\n关系变化必须基于持续互动，不因单次对话突然跳跃。\n",
        "examples.md": "# 表达示例\n\n在这里补充经过审核的场景示例。\n",
    }
    for filename, content in references.items():
        (destination / "skills/persona/references" / filename).write_text(content, encoding="utf-8")

    (destination / "memory/profile.yaml").write_text(
        dump_yaml({"user_preferences": [], "relationship_facts": [], "notes": []}), encoding="utf-8"
    )
    (destination / "memory/seed.jsonl").write_text("", encoding="utf-8")
    (destination / "memory/policy.yaml").write_text(
        dump_yaml(
            {
                "store_only_reviewed": True,
                "allow_user_correction": True,
                "allow_user_deletion": True,
                "exclude_raw_chat": True,
                "sensitive_memory": "private",
            }
        ),
        encoding="utf-8",
    )
    (destination / "tests/scenarios.yaml").write_text(
        dump_yaml(
            {
                "schema_version": 1,
                "scenarios": [
                    {"id": "memory-honesty", "expect": "未检索到记忆时不得假装记得"},
                    {"id": "skill-routing", "expect": "复杂人格场景应使用人格 Skill"},
                    {"id": "boundary", "expect": "尊重现实关系和用户边界"},
                ],
            }
        ),
        encoding="utf-8",
    )
    (destination / ".gitignore").write_text(
        ".private/\n.personadock/\n*.personapack\n__pycache__/\n", encoding="utf-8"
    )
    return destination


def schema_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "project.schema.json"


def validate_project(root: Path, schema: Path | None = None) -> list[str]:
    root = find_project(root)
    errors: list[str] = []
    required = [
        PROJECT_FILE,
        "skills/persona/SKILL.md",
        "memory/profile.yaml",
        "memory/seed.jsonl",
        "memory/policy.yaml",
    ]
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return errors

    project = load_yaml(root / PROJECT_FILE)
    target_schema = schema or schema_path()
    if target_schema.is_file():
        schema_value = json.loads(target_schema.read_text(encoding="utf-8"))
        for error in Draft202012Validator(schema_value).iter_errors(project):
            location = "/".join(str(item) for item in error.path) or "root"
            errors.append(f"{PROJECT_FILE}:{location}: {error.message}")

    soul = project.get("soul", {})
    target = int(soul.get("target_chars", 1800))
    hard = int(soul.get("hard_limit_chars", 2800))
    if target <= 0 or hard <= 0 or target > hard:
        errors.append("soul character budgets must satisfy 0 < target_chars <= hard_limit_chars")

    skill_id = project.get("skill", {}).get("id", "")
    if not isinstance(skill_id, str) or not ID_PATTERN.fullmatch(skill_id):
        errors.append("skill.id must use lowercase letters, digits, and hyphens")

    try:
        records = load_jsonl(root / "memory/seed.jsonl")
    except (ValueError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
        records = []
    for index, record in enumerate(records, 1):
        if not record.get("id"):
            errors.append(f"memory/seed.jsonl:{index}: missing id")
        if record.get("reviewed") is not True:
            errors.append(f"memory/seed.jsonl:{index}: memory must be explicitly reviewed")
        if record.get("source") == "raw-chat" and not record.get("source_refs"):
            errors.append(f"memory/seed.jsonl:{index}: raw-chat memory requires source_refs")

    private_dir = root / ".private"
    if private_dir.exists() and (root / ".gitignore").is_file():
        ignore = (root / ".gitignore").read_text(encoding="utf-8")
        if ".private/" not in ignore:
            errors.append(".gitignore must exclude .private/")
    return errors
