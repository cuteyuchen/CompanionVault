---
name: persona-distiller
description: Distill user-selected chat records into an evidence-backed private PersonaDock project. Generate a compact SOUL, detailed persona Skill, reviewed Memory candidates, tests, and a portable PersonaPack. Use persona-builder instead when natural-language design requirements are primary.
argument-hint: [selected-chat-files] [output-project]
version: 0.1.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# PersonaDock Persona Distiller

## Purpose

Use only the chat records selected by the user to create a PersonaDock-compatible local project:

```text
companion.yaml
skills/persona/SKILL.md
skills/persona/references/*.md
memory/profile.yaml
memory/seed.jsonl
memory/policy.yaml
tests/scenarios.yaml
.private/
```

This Skill is the preferred evidence-first distillation workflow. `personadock distill` is only a lightweight fallback. When the user primarily describes the personality they want rather than reconstructing observed behavior, use `persona-builder`; when both are present, use its hybrid mode and keep design requirements distinct from evidence.

## Rules

1. Read only files or directories explicitly selected by the user.
2. Default to a private local project. Do not require GitHub, a fork, a PR, or publication.
3. Keep source records, evidence, and unreviewed memory candidates under `.private/`.
4. Keep SOUL concise: identity, stable traits, boundaries, Skill routing, and memory honesty only.
5. Put detailed situations, language patterns, relationship behavior, and examples in Skill references.
6. Put a fact into `memory/seed.jsonl` only after the user explicitly approves it and set `reviewed: true`.
7. Never claim the generated persona is the real person represented by source material.
8. Do not publish unless the user explicitly requests a public export.

## Workflow

### 1. Create the project

When PersonaDock is installed:

```bash
personadock init "<output-project>" --id "<persona-id>" --name "<display-name>"
```

Without the CLI, create the same structure using `references/output-contract.md`.

### 2. Prepare private evidence

Use `.private/` for normalized records, evidence, memory candidates, and a review checklist. Never modify the selected source files.

### 3. Distill by layer

- **SOUL:** stable identity, 3–7 high-confidence traits, compact voice guidance, hard boundaries, Skill triggers, and memory lookup rules.
- **Skill:** write detailed behavior to `skills/persona/SKILL.md` and `references/voice.md`, `daily-scenarios.md`, `emotional-support.md`, `conflict-repair.md`, `relationship-stages.md`, and `examples.md`.
- **Memory:** put stable preferences in `memory/profile.yaml`; put event candidates in `.private/memory-candidates.jsonl`; move only approved facts into `memory/seed.jsonl`.
- **Tests:** cover memory honesty, Skill routing, privacy, corrections, non-impersonation, and relationship boundaries.

Write behavioral rules as: trigger -> observable behavior -> limit.

### 4. Review

Show the user:

- proposed SOUL conclusions
- changed Skill references
- memory candidates with source references
- uncertain or conflicting evidence
- excluded sensitive details

Unapproved memory remains private and must not be packaged.

### 5. Validate and package

```bash
personadock validate "<output-project>"
personadock build "<output-project>"
personadock pack "<output-project>"
personadock inspect "<output-project>/dist/<id>-<version>.personapack"
```

Fix source data when validation fails. Never bypass validation.

### 6. Optional installation

Only when requested:

```bash
personadock install "<package.personapack>" --target hermes
personadock install "<package.personapack>" --target openclaw
```

## Completion checks

- `personadock validate` passes.
- SOUL stays below `hard_limit_chars`.
- Detailed persona information lives in Skill references.
- Raw records are absent from the build and package.
- Every packaged memory has `reviewed: true`.
- `personadock inspect` reports `integrity: ok`.
- No PR or public upload was created without an explicit request.
