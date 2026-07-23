from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compiler import build_all
from .core import dump_yaml, load_yaml, persona_dirs, repo_root, validate_persona
from .installer import install_from_dist


def command_list(root: Path) -> int:
    for directory in persona_dirs(root):
        p = load_yaml(directory / "persona.yaml")
        print(f"{p['id']:<22} {p['name']:<12} {p['summary']}")
    return 0


def command_validate(root: Path, path: str | None) -> int:
    dirs = [Path(path).resolve()] if path else persona_dirs(root)
    failed = False
    for directory in dirs:
        errors = validate_persona(directory, root)
        if errors:
            failed = True
            print(f"FAIL {directory}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {directory}")
    return 1 if failed else 0


def command_new(root: Path, persona_id: str, name: str, locale: str) -> int:
    directory = root / "personas" / locale / persona_id
    if directory.exists():
        raise FileExistsError(directory)
    directory.mkdir(parents=True)
    persona = {
        "schema_version": 1, "id": persona_id, "version": "0.1.0", "locale": locale,
        "name": name, "summary": "请填写不少于十个字的人格简介", "author": {"github": "your-name"},
        "license": "CC-BY-4.0", "tags": ["日常陪伴", "待完善"],
        "baseline": ["healthy-companion", "natural-conversation", "relationship-boundaries"],
        "identity": {"role": "请填写", "self_concept": "请填写", "relationship_start": "请填写"},
        "personality": {"core_traits": [{"name": "特征一", "intensity": 5, "behavior": "请填写"}, {"name": "特征二", "intensity": 5, "behavior": "请填写"}, {"name": "特征三", "intensity": 5, "behavior": "请填写"}], "strengths": ["请填写", "请填写"], "flaws": ["请填写"], "values": ["真诚", "尊重"]},
        "features": [{"id": "feature-one", "name": "特征一", "trigger": "请填写", "behavior": "请填写", "limit": "请填写"}, {"id": "feature-two", "name": "特征二", "trigger": "请填写", "behavior": "请填写", "limit": "请填写"}, {"id": "feature-three", "name": "特征三", "trigger": "请填写", "behavior": "请填写", "limit": "请填写"}],
        "voice": {"language": "简体中文", "default_length": "short", "sentence_style": "自然口语", "habits": ["请填写"], "avoid": ["机械安慰"]},
        "emotional_behavior": {"sadness": {"response": "请填写"}},
        "relationship": {"progression": [{"stage": "familiar", "behavior": ["请填写"]}], "conflict_repair": ["承认具体错误", "允许对方解释"]},
        "memory": {"remember": ["用户主动提供的偏好"], "never_invent": ["不存在的共同经历"]},
        "safety": {"no_exclusivity": True, "no_dependency_pressure": True, "no_professional_claims": True, "respect_real_relationships": True},
    }
    (directory / "persona.yaml").write_text(dump_yaml(persona), encoding="utf-8")
    (directory / "examples.yaml").write_text("schema_version: 1\nexamples: []\n", encoding="utf-8")
    (directory / "tests.yaml").write_text("schema_version: 1\ntests: []\n", encoding="utf-8")
    (directory / "README.md").write_text(f"# {name}\n\n请补充人格介绍。\n", encoding="utf-8")
    print(directory)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="companion-vault")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    p_validate = sub.add_parser("validate"); p_validate.add_argument("path", nargs="?")
    p_build = sub.add_parser("build"); p_build.add_argument("--output", default="dist")
    p_install = sub.add_parser("install"); p_install.add_argument("persona"); p_install.add_argument("--target", choices=["hermes", "generic", "sillytavern"], default="hermes"); p_install.add_argument("--path")
    p_new = sub.add_parser("new-persona"); p_new.add_argument("id"); p_new.add_argument("--name", required=True); p_new.add_argument("--locale", default="zh-CN")
    args = parser.parse_args(argv)
    root = repo_root()
    if args.command == "list": return command_list(root)
    if args.command == "validate": return command_validate(root, args.path)
    if args.command == "build": build_all(root, root / args.output); print(root / args.output); return 0
    if args.command == "install":
        build_all(root, root / "dist")
        path = install_from_dist(root, args.persona, args.target, Path(args.path).expanduser() if args.path else None)
        print(path); return 0
    if args.command == "new-persona": return command_new(root, args.id, args.name, args.locale)
    return 2

if __name__ == "__main__":
    sys.exit(main())
