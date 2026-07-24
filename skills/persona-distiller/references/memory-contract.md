# PersonaDock Memory Contract

## Candidate memory

Before approval, write memory candidates only to:

```text
.private/memory-candidates.jsonl
```

Recommended candidate record:

```json
{
  "id": "candidate-001",
  "type": "preference",
  "summary": "The user prefers listening before advice.",
  "event_time": null,
  "tags": ["support-style"],
  "confidence": 0.86,
  "source_refs": ["chat-a.txt:120-126"],
  "sensitivity": "private",
  "reviewed": false
}
```

## Packaged memory

Move a record to `memory/seed.jsonl` only after explicit user approval. A packaged record must include:

```json
{
  "id": "memory-001",
  "type": "preference",
  "summary": "The user prefers listening before advice.",
  "event_time": null,
  "tags": ["support-style"],
  "confidence": 0.86,
  "source_refs": ["chat-a.txt:120-126"],
  "sensitivity": "private",
  "reviewed": true
}
```

## Rules

- Do not store inferred thoughts, motives, or feelings as facts.
- Do not turn uncertainty into reviewed memory.
- Keep source references so the user can correct or delete a memory.
- Do not include raw chat text when a concise factual summary is enough.
- Do not place source records under `memory/`; keep them under `.private/` or in their original location.
- The user may reject, edit, or delete any candidate before packaging.
