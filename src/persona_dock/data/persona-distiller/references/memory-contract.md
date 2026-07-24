# PersonaDock Memory Contract

Write unapproved memory candidates to `.private/memory-candidates.jsonl` with `reviewed: false` and source references.

Move a record to `memory/seed.jsonl` only after explicit user approval. Packaged records must use `reviewed: true` and should include an ID, type, concise factual summary, source references, sensitivity, and optional event time, tags, and confidence.

Do not store inferred thoughts or motives as facts. Do not convert uncertainty into reviewed memory. Keep raw chat outside `memory/` and let the user edit or reject every candidate before packaging.
