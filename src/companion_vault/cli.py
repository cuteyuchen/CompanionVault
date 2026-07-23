from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .catalog import DEFAULT_BASE, load_registry, local_root
from .compiler import build_all
from .core import dump_yaml, load_yaml, persona_dirs, validate_persona
from .distill import build_candidate
from .installer import default_target, install_catalog_persona
from .release import package_personas
from .site import build_site
from .skill_install import install_skill
from .state import load_state, rollback, save_state, uninstall


def source_root() -> Path:
    root = local_root()
    if not root: raise FileNotFoundError("this command must run inside a CompanionVault source checkout")
    return root


def registry_rows(base_url: str):
    registry, _ = load_registry(base_url)
    return registry["personas"]


def command_list(base_url: str, query: str | None = None) -> int:
    q = (query or "").casefold()
    for p in registry_rows(base_url):
        haystack = " ".join([p["id"], p["name"], p["summary"], *p.get("tags", [])]).casefold()
        if q and q not in haystack: continue
        print(f"{p['id']:<22} {p['name']:<12} {p['summary']}")
    return 0


def command_validate(root: Path, path: str | None) -> int:
    dirs = [Path(path).resolve()] if path else persona_dirs(root); failed = False
    for directory in dirs:
        errors = validate_persona(directory, root)
        if errors:
            failed = True; print(f"FAIL {directory}")
            for error in errors: print(f"  - {error}")
        else: print(f"OK   {directory}")
    return 1 if failed else 0


def command_new(root: Path, persona_id: str, name: str, locale: str) -> int:
    directory = root / "personas" / locale / persona_id
    if directory.exists(): raise FileExistsError(directory)
    directory.mkdir(parents=True)
    persona = {"schema_version":1,"id":persona_id,"version":"0.1.0","locale":locale,"name":name,"summary":"请填写不少于十个字的人格简介","author":{"github":"your-name"},"license":"CC-BY-4.0","tags":["日常陪伴","待完善"],"baseline":["healthy-companion","natural-conversation","relationship-boundaries"],"identity":{"role":"请填写","self_concept":"请填写","relationship_start":"请填写"},"personality":{"core_traits":[{"name":"特征一","intensity":5,"behavior":"请填写"},{"name":"特征二","intensity":5,"behavior":"请填写"},{"name":"特征三","intensity":5,"behavior":"请填写"}],"strengths":["请填写","请填写"],"flaws":["请填写"],"values":["真诚","尊重"]},"features":[{"id":"feature-one","name":"特征一","trigger":"请填写","behavior":"请填写","limit":"请填写"},{"id":"feature-two","name":"特征二","trigger":"请填写","behavior":"请填写","limit":"请填写"},{"id":"feature-three","name":"特征三","trigger":"请填写","behavior":"请填写","limit":"请填写"}],"voice":{"language":"简体中文","default_length":"short","sentence_style":"自然口语","habits":["请填写"],"avoid":["机械安慰"]},"emotional_behavior":{"sadness":{"response":"请填写"}},"relationship":{"progression":[{"stage":"familiar","behavior":["请填写"]}],"conflict_repair":["承认具体错误","允许对方解释"]},"memory":{"remember":["用户主动提供的偏好"],"never_invent":["不存在的共同经历"]},"safety":{"no_exclusivity":True,"no_dependency_pressure":True,"no_professional_claims":True,"respect_real_relationships":True}}
    (directory/"persona.yaml").write_text(dump_yaml(persona),encoding="utf-8"); (directory/"examples.yaml").write_text("schema_version: 1\nexamples: []\n",encoding="utf-8"); (directory/"tests.yaml").write_text("schema_version: 1\ntests: []\n",encoding="utf-8"); (directory/"README.md").write_text(f"# {name}\n",encoding="utf-8"); print(directory); return 0


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(prog="companion-vault"); parser.add_argument("--registry",default=DEFAULT_BASE); sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("list");p.add_argument("--search")
    p=sub.add_parser("show");p.add_argument("persona")
    p=sub.add_parser("validate");p.add_argument("path",nargs="?")
    p=sub.add_parser("build");p.add_argument("--output",default="dist");p.add_argument("--packages",action="store_true")
    p=sub.add_parser("site-build");p.add_argument("--output",default="_site")
    p=sub.add_parser("install");p.add_argument("persona");p.add_argument("--target",choices=["hermes","generic","sillytavern"],default="hermes");p.add_argument("--path")
    p=sub.add_parser("update");p.add_argument("--target",choices=["hermes","generic","sillytavern"],default="hermes");p.add_argument("--path")
    p=sub.add_parser("rollback");p.add_argument("--target",choices=["hermes","generic","sillytavern"],default="hermes");p.add_argument("--path")
    p=sub.add_parser("uninstall");p.add_argument("--target",choices=["hermes","generic","sillytavern"],default="hermes");p.add_argument("--path")
    p=sub.add_parser("pin");p.add_argument("persona");p.add_argument("version")
    p=sub.add_parser("unpin");p.add_argument("persona")
    p=sub.add_parser("new-persona");p.add_argument("id");p.add_argument("--name",required=True);p.add_argument("--locale",default="zh-CN")
    p=sub.add_parser("distill");p.add_argument("input");p.add_argument("--speaker",required=True);p.add_argument("--id",required=True);p.add_argument("--name",required=True);p.add_argument("--output");p.add_argument("--mode",choices=["public","private"],default="public");p.add_argument("--consent",choices=["self","authorized","public","unknown"],required=True)
    p=sub.add_parser("skill-install");p.add_argument("--target",choices=["claude","codex","agents","opencode","generic"],required=True);p.add_argument("--scope",choices=["project","global"],default="global");p.add_argument("--path")
    args=parser.parse_args(argv)
    if args.command=="list": return command_list(args.registry,args.search)
    if args.command=="show":
        p=next((x for x in registry_rows(args.registry) if x["id"]==args.persona),None)
        if not p: raise KeyError(args.persona)
        print(f"{p['name']} ({p['id']}@{p['version']})\n{p['summary']}\n标签：{'、'.join(p['tags'])}"); return 0
    if args.command=="validate": return command_validate(source_root(),args.path)
    if args.command=="build":
        root=source_root(); build_all(root,root/args.output); package_personas(root) if args.packages else None; print(root/args.output); return 0
    if args.command=="site-build": root=source_root(); print(build_site(root,root/args.output)); return 0
    if args.command=="install": print(install_catalog_persona(args.persona,args.target,Path(args.path) if args.path else None,args.registry)); return 0
    if args.command=="update":
        destination=Path(args.path) if args.path else default_target(args.target)
        state=load_state(); record=state.get("installations",{}).get(str(destination.expanduser().resolve()))
        if not record or not record.get("persona"): raise ValueError("no managed installation found at destination")
        pin=state.get("pins",{}).get(record["persona"])
        current=next((x for x in registry_rows(args.registry) if x["id"]==record["persona"]),None)
        if not current: raise KeyError(record["persona"])
        if pin and current["version"] != pin: raise ValueError(f"{record['persona']} is pinned to {pin}; catalog provides {current['version']}")
        print(install_catalog_persona(record["persona"],args.target,destination,args.registry)); return 0
    if args.command=="rollback": print(rollback(Path(args.path) if args.path else default_target(args.target))); return 0
    if args.command=="uninstall": uninstall(Path(args.path) if args.path else default_target(args.target)); return 0
    if args.command in {"pin","unpin"}:
        state=load_state(); pins=state.setdefault("pins",{}); pins[args.persona]=args.version if args.command=="pin" else None
        if pins.get(args.persona) is None: pins.pop(args.persona,None)
        save_state(state); return 0
    if args.command=="new-persona": return command_new(source_root(),args.id,args.name,args.locale)
    if args.command=="distill":
        root=source_root(); output=Path(args.output) if args.output else root/"candidates"/args.id
        print(build_candidate(Path(args.input),args.speaker,args.id,args.name,output,args.mode,args.consent)); return 0
    if args.command=="skill-install": print(install_skill(local_root(),args.target,args.scope,Path(args.path) if args.path else None)); return 0
    return 2

if __name__=="__main__": sys.exit(main())
