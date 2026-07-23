#!/usr/bin/env python3
from pathlib import Path
import argparse, json
from companion_vault.distill import load_messages
from companion_vault.privacy import pseudonym, redact_text

p=argparse.ArgumentParser();p.add_argument("input");p.add_argument("--output",required=True);p.add_argument("--public",action="store_true");args=p.parse_args()
messages=load_messages(Path(args.input)); names=list({m.sender for m in messages})
with Path(args.output).open("w",encoding="utf-8") as f:
    for m in messages:
        f.write(json.dumps({"sender":pseudonym(m.sender),"text":redact_text(m.text,names) if args.public else m.text,"timestamp":m.timestamp},ensure_ascii=False)+"\n")
