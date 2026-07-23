from __future__ import annotations

import shutil
from importlib import resources
from pathlib import Path
from typing import Any

TARGETS={"claude":{"project":Path(".claude/skills"),"global":Path.home()/".claude/skills"},"codex":{"project":Path(".codex/skills"),"global":Path.home()/".codex/skills"},"agents":{"project":Path(".agents/skills"),"global":Path.home()/".agents/skills"},"opencode":{"project":Path(".opencode/skills"),"global":Path.home()/".config/opencode/skills"},"generic":{"project":Path("skills"),"global":Path.home()/".local/share/agent-skills"}}

def _copy_traversable(source:Any,destination:Path)->None:
    destination.mkdir(parents=True,exist_ok=True)
    for child in source.iterdir():
        target=destination/child.name
        _copy_traversable(child,target) if child.is_dir() else target.write_bytes(child.read_bytes())

def install_skill(root:Path|None,target:str,scope:str,destination:Path|None=None)->Path:
    if target not in TARGETS: raise ValueError(f"unsupported skill target: {target}")
    output=(destination or TARGETS[target][scope]).expanduser().resolve()/"persona-distiller"
    if output.exists(): shutil.rmtree(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    checkout=root/"skills/persona-distiller" if root else None
    if checkout and checkout.exists(): shutil.copytree(checkout,output)
    else: _copy_traversable(resources.files("companion_vault").joinpath("data/persona-distiller"),output)
    return output
