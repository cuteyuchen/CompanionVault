---
name: persona-builder
description: Create, distill, refine, or hybrid-build a private PersonaDock persona from natural-language requirements, user-selected chat records, optional examples, and existing projects. Automatically choose the correct workflow and produce a compact SOUL, detailed persona Skill, reviewed Memory, tests, and a portable PersonaPack.
argument-hint: [persona-description-or-selected-sources] [output-project]
version: 0.1.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# PersonaDock Persona Builder

## Purpose

Create or refine a normal PersonaDock project from any combination of:

- a short natural-language concept
- identity, personality, voice, relationship, flaw, and boundary requirements
- rules written as “when X happens, they do Y”
- user-selected chat records or writing samples
- an existing PersonaDock project

The final result must use the standard PersonaDock project structure and, when requested, become a validated `.personapack`.

## Automatic mode routing

Determine the mode from the user’s actual goal. Do not ask the user to choose a technical mode unless the goal is genuinely ambiguous.

1. **Create mode** — natural-language requirements are the primary source of truth.
2. **Distill mode** — selected records are the primary source and the goal is to reconstruct observed behavior with evidence.
3. **Hybrid mode** — explicit design requirements and selected records both matter.
4. **Refine mode** — an existing PersonaDock project must be edited without discarding reviewed content.

Routing rules:

- “Create/design/make a persona who…” with no required source imitation -> Create.
- “Analyze these chats and reproduce how this speaker behaves” -> Distill.
- “Use my description as the design, but learn rhythm or examples from these chats” -> Hybrid.
- “Change this existing persona…” -> Refine.
- If selected records are only inspiration, do not treat their private facts or relationships as persona canon.

## Precedence and conflict rules

Use this precedence unless the user explicitly requests evidence-first reconstruction:

1. the user’s latest direct requirement
2. reviewed content in an existing PersonaDock project
3. supported observations from selected sources
4. clearly marked non-sensitive defaults

In Distill mode, do not rewrite contradictory evidence into a clean fictional trait. Record uncertainty and show the conflict to the user. In Hybrid mode, keep design requirements and source observations distinguishable when they disagree.

## Core rules

1. Default to a private local project. Do not require GitHub, a fork, a PR, or publication.
2. Read only files or directories explicitly selected by the user.
3. Never modify source records. Put normalized records, evidence, assumptions, and unreviewed candidates under `.private/`.
4. Convert vague adjectives into observable behavior using: trigger -> behavior -> limit.
5. Keep SOUL concise. Put identity, stable traits, hard boundaries, Skill routing, and memory honesty in SOUL; put detailed scenes and examples in Skill references.
6. Do not invent user history. Fictional persona canon may be stored as background, but real user facts and shared events require explicit approval before packaged Memory.
7. Preserve deliberate flaws, independent judgment, and disagreement when requested. Do not flatten every persona into a universally agreeable assistant.
8. Never claim an evidence-derived persona is the real person represented by source material.
9. Do not publish or upload anything unless the user explicitly asks.

## Workflow

### 1. Understand the request

Extract concrete requirements into:

- identity and relationship role
- 3–7 stable core traits
- voice, vocabulary, reply length, rhythm, and prohibited styles
- strengths and intentional flaws
- emotional behavior
- daily, playful, serious, conflict, repair, boundary, and reunion scenarios
- relationship progression
- memory policy and canonical background
- selected source files, target speaker, and evidence scope when records are provided

For short design requests, infer reasonable non-sensitive defaults and label them as design choices rather than facts. Ask only for missing information that materially changes the result.

### 2. Create or locate the project

For a new project:

```bash
personadock init "<output-project>" --id "<persona-id>" --name "<display-name>"
```

For an existing project, locate `companion.yaml` and edit in place. Never overwrite reviewed Memory or user-authored references without showing the change.

Follow `references/output-contract.md` for the project tree.

### 3. Handle selected records in Distill or Hybrid mode

When source records are present:

1. Confirm the target speaker and selected files.
2. Normalize only the required material into `.private/normalized.jsonl` when useful.
3. Store evidence records in `.private/evidence.jsonl` using `references/evidence-contract.md`.
4. Separate observable style and behavior from real-world facts, inferred motives, and private events.
5. Look for repeated behavior across dates and situations instead of overfitting to one message.
6. Preserve contradictions and low-confidence observations as review items.
7. Put unapproved factual memories only in `.private/memory-candidates.jsonl`.

Do not use MBTI, astrology, occupation, or a single event as a substitute for behavioral evidence.

### 4. Build by layer

- **SOUL:** stable identity, core traits, compact voice, hard boundaries, Skill triggers, and memory lookup rules.
- **Persona Skill:** detailed behavior and routing in `skills/persona/SKILL.md`.
- **References:** write `voice.md`, `daily-scenarios.md`, `emotional-support.md`, `conflict-repair.md`, `relationship-stages.md`, and `examples.md`.
- **Memory:** keep real-user facts out unless explicitly confirmed. Put unconfirmed candidates in `.private/memory-candidates.jsonl`.
- **Tests:** cover important “when X, do Y” rules, evidence limits, memory honesty, routing, boundaries, conflict, and style consistency.

Use `references/prompt-contract.md` for natural-language requirements, `references/evidence-contract.md` for selected records, and `references/memory-contract.md` for real facts.

### 5. Show a review summary

Before packaging, show:

- the selected mode and why it was chosen
- the compact SOUL design or evidence-backed conclusions
- the main scenario rules added to the persona Skill
- intentional flaws and boundaries
- assumptions, low-confidence evidence, or unresolved contradictions
- proposed Memory entries with source references when applicable

A user may approve the overall design, but each real-user Memory entry must remain explicit and reviewable. Unapproved memory stays private and must not be packaged.

### 6. Validate and package

```bash
personadock validate "<output-project>"
personadock build "<output-project>"
personadock pack "<output-project>"
personadock inspect "<output-project>/dist/<id>-<version>.personapack"
```

Fix source files when validation fails. Never bypass validation.

### 7. Optional installation

Only when requested:

```bash
personadock install "<package.personapack>" --target hermes
personadock install "<package.personapack>" --target openclaw
```

## Example: natural-language design

User request:

> I want a proud but soft-hearted cyber companion. She teases during daily chat, becomes direct when I am genuinely upset, admits mistakes after conflict, and never pretends to remember events I did not provide.

Translate it into:

- SOUL traits: proud, soft-hearted, independent
- voice reference: light teasing in safe daily scenes; direct language in serious scenes
- emotional-support rule: distress -> stop teasing -> acknowledge -> ask whether to listen or help
- conflict-repair rule: own the specific mistake -> allow explanation -> apologize without deflection
- memory boundary: search first; missing result -> state uncertainty
- tests for each rule

Do not merely paste the paragraph into SOUL.

## Example: evidence-first distillation

User request:

> Read the selected chat files, focus on speaker Xiaoyou, and create a private persona that reflects her repeated speaking and conflict-repair patterns.

Use Distill mode:

- only read the selected records
- create source-linked evidence entries
- distinguish repeated behavior from isolated events
- show uncertain or conflicting observations
- keep raw records and unapproved memory under `.private/`
- never claim the generated persona is the real Xiaoyou

## Completion checks

- `personadock validate` passes.
- SOUL stays below `hard_limit_chars`.
- Every important “when X” requirement appears in a Skill reference or test.
- Evidence-derived conclusions have source references and confidence levels.
- Detailed persona information is not overloaded into SOUL.
- Raw references and private notes are absent from the package.
- Every packaged real-user Memory entry has `reviewed: true`.
- `personadock inspect` reports `integrity: ok`.
- No PR or public upload was created without an explicit request.
