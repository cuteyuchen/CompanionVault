from __future__ import annotations

import hashlib
import re

PATTERNS=[(re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),"<PHONE>"),(re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),"<EMAIL>"),(re.compile(r"https?://\S+"),"<URL>"),(re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\d)"),"<ID>"),(re.compile(r"(?<!\d)(?:\d[ -]?){12,19}(?!\d)"),"<NUMBER>")]

def pseudonym(value:str)->str: return "speaker-"+hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]
def redact_text(text:str,names:list[str]|None=None)->str:
    result=text
    for pattern,replacement in PATTERNS: result=pattern.sub(replacement,result)
    for name in sorted((names or []),key=len,reverse=True):
        if name.strip(): result=result.replace(name,"<NAME>")
    return result
