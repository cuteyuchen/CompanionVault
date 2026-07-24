from __future__ import annotations

import re
from pathlib import Path

from .io import write_jsonl
from .project import init_project

LINE = re.compile(r"^\s*([^:：]{1,40})[:：]\s*(.+?)\s*$")


def distill_chat(
    input_path: Path,
    destination: Path,
    persona_id: str,
    name: str,
    speaker: str,
    locale: str = "zh-CN",
) -> Path:
    """Create a reviewable, privacy-safe project from speaker-prefixed chat text."""
    root = init_project(destination, persona_id, name, locale)
    raw = input_path.expanduser().read_text(encoding="utf-8")
    examples: list[str] = []
    memory_candidates: list[dict[str, object]] = []
    for number, line in enumerate(raw.splitlines(), 1):
        match = LINE.match(line)
        if not match:
            continue
        current_speaker, text = match.groups()
        if current_speaker.strip() == speaker:
            examples.append(text.strip())
        else:
            memory_candidates.append(
                {
                    "id": f"candidate-{number}",
                    "type": "episodic-candidate",
                    "summary": text.strip(),
                    "source": "raw-chat",
                    "source_refs": [f"line:{number}"],
                    "reviewed": False,
                    "sensitivity": "private",
                }
            )

    (root / ".private/raw" / input_path.name).write_text(raw, encoding="utf-8")
    reference = root / "skills/persona/references/examples.md"
    reference.write_text(
        "# 从聊天记录提取的表达候选\n\n"
        + "\n\n".join(f"## 示例 {index}\n\n{value}" for index, value in enumerate(examples[:50], 1))
        + "\n",
        encoding="utf-8",
    )
    write_jsonl(root / ".private/memory-candidates.jsonl", memory_candidates)
    (root / ".private/REVIEW.md").write_text(
        "# 蒸馏审核\n\n"
        "1. 检查 `skills/persona/references/examples.md`，提炼稳定表达规律。\n"
        "2. 审核 `.private/memory-candidates.jsonl`。\n"
        "3. 仅将确认真实、愿意保留的记录复制到 `memory/seed.jsonl`，并设置 `reviewed: true`。\n"
        "4. 原始聊天和候选记忆不会进入 PersonaPack。\n",
        encoding="utf-8",
    )
    return root
