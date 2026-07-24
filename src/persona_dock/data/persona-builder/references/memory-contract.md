# PersonaDock Builder Memory Contract

## Separate three kinds of information

1. **Persona design:** traits, voice, scenario rules, flaws, and boundaries. Store these in SOUL or the persona Skill.
2. **Fictional canon:** explicitly invented setting, background, role, or history. Store this in identity or Skill references unless runtime retrieval is required.
3. **Real Memory:** user preferences, real events, relationship facts, and shared history. Package only after explicit review.

## Candidate memory

Before approval, write real-memory candidates only to:

```text
.private/memory-candidates.jsonl
```

Recommended record:

```json
{
  "id": "candidate-001",
  "type": "preference",
  "summary": "The user prefers listening before advice.",
  "event_time": null,
  "tags": ["support-style"],
  "confidence": 1.0,
  "source_refs": ["user-requirement:4"],
  "sensitivity": "private",
  "reviewed": false
}
```

## Packaged memory

Move a record to `memory/seed.jsonl` only after explicit approval. A packaged record must include `reviewed: true`.

```json
{
  "id": "memory-001",
  "type": "preference",
  "summary": "The user prefers listening before advice.",
  "event_time": null,
  "tags": ["support-style"],
  "confidence": 1.0,
  "source_refs": ["user-approved-requirement:4"],
  "sensitivity": "private",
  "reviewed": true
}
```

## Rules

- Do not convert personality rules into Memory.
- Do not invent shared events to make the persona feel established.
- Do not store inferred thoughts, motives, diagnoses, or feelings as facts.
- Keep source references so the user can correct or delete a Memory.
- Prefer concise summaries over copied private text.
- The user may reject, edit, or delete any candidate before packaging.
