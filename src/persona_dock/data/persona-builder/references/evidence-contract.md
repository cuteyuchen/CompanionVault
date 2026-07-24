# PersonaDock Evidence Contract

Use this contract only when the unified Skill is operating in Distill or Hybrid mode with user-selected source material.

## Private evidence files

Keep all intermediate evidence under `.private/`:

```text
.private/
├── normalized.jsonl
├── evidence.jsonl
├── memory-candidates.jsonl
└── REVIEW.md
```

These files must never be packaged into a PersonaPack.

## Normalized record

Recommended shape for `.private/normalized.jsonl`:

```json
{
  "source_ref": "chat-a.txt:120-126",
  "speaker": "Xiaoyou",
  "timestamp": "2026-01-03T12:30:00+08:00",
  "text": "normalized message text",
  "context": "conflict-repair"
}
```

Do not copy unrelated private messages. Preserve enough source location information for review without changing the original files.

## Evidence record

Recommended shape for `.private/evidence.jsonl`:

```json
{
  "id": "evidence-001",
  "category": "voice",
  "claim": "Uses short follow-up questions after acknowledging distress.",
  "rule": {
    "trigger": "the user expresses distress",
    "behavior": "acknowledge first, then ask one short follow-up question",
    "limit": "do not interrogate or immediately lecture"
  },
  "source_refs": [
    "chat-a.txt:120-126",
    "chat-b.json:messages[44:47]"
  ],
  "support_count": 4,
  "counterexamples": [],
  "confidence": 0.88,
  "status": "candidate"
}
```

## Confidence guidance

- **High:** repeated across multiple dates or situations with no material contradiction.
- **Medium:** repeated at least twice with limited context or minor counterexamples.
- **Low:** isolated behavior, ambiguous context, or user interpretation without repeat evidence.

Low-confidence evidence may inform review notes but must not become an unconditional persona rule.

## Separation rules

- Observable speaking or behavior patterns may become persona rules.
- Real-world facts, preferences, relationships, and shared events are Memory candidates, not personality evidence.
- Inferred motives, hidden feelings, diagnoses, and moral judgments are not facts.
- A design requirement in Hybrid mode is not evidence. Label it as a user requirement.
- When evidence conflicts with a direct design requirement, preserve the conflict in `.private/design-notes.md` and follow the mode-specific precedence rules in `SKILL.md`.

## Review

Before packaging, show the user:

- supported conclusions and source references
- low-confidence or conflicting observations
- excluded sensitive details
- proposed Memory candidates

Only approved real-user facts may move to `memory/seed.jsonl`, and they must use `reviewed: true`.
