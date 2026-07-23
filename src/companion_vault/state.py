from __future__ import annotations

import json
import shutil
from datetime import datetime,timezone
from pathlib import Path

STATE_DIR=Path.home()/".companion-vault"; STATE_FILE=STATE_DIR/"state.json"
def load_state()->dict: return {"installations":{},"pins":{}} if not STATE_FILE.exists() else json.loads(STATE_FILE.read_text(encoding="utf-8"))
def save_state(state:dict)->None:
    STATE_DIR.mkdir(parents=True,exist_ok=True); STATE_FILE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")
def key_for(destination:Path)->str: return str(destination.expanduser().resolve())
def install_bytes(content:bytes,destination:Path,persona:str,version:str,target:str)->Path:
    destination=destination.expanduser().resolve();destination.parent.mkdir(parents=True,exist_ok=True);state=load_state();key=key_for(destination);record=state["installations"].get(key,{"history":[]})
    if destination.exists():
        stamp=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f");backup=STATE_DIR/"backups"/stamp/destination.name;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(destination,backup);record["history"].append({"backup":str(backup),"persona":record.get("persona"),"version":record.get("version")})
    destination.write_bytes(content);record.update({"destination":str(destination),"persona":persona,"version":version,"target":target,"installed_at":datetime.now(timezone.utc).isoformat()});state["installations"][key]=record;save_state(state);return destination
def rollback(destination:Path)->Path:
    state=load_state();key=key_for(destination);record=state["installations"].get(key)
    if not record or not record.get("history"): raise ValueError("no backup available")
    previous=record["history"].pop();shutil.copy2(previous["backup"],destination);record["persona"]=previous.get("persona");record["version"]=previous.get("version");save_state(state);return destination
def uninstall(destination:Path)->None:
    state=load_state();key=key_for(destination);record=state["installations"].pop(key,None)
    if record and record.get("history"): shutil.copy2(record["history"][-1]["backup"],destination)
    elif destination.exists(): destination.unlink()
    save_state(state)
