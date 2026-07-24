---
name: persona-builder
description: Build a private PersonaDock persona from natural-language requirements, optional examples, and optional selected reference material. Turn descriptions such as “when the user is tired, respond gently but do not lecture” into a compact SOUL, detailed scenario Skill, reviewed Memory, tests, and a portable PersonaPack.
argument-hint: [persona-description] [output-project]
version: 0.1.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# PersonaDock Persona Builder

## Purpose

Create or refine a PersonaDock-compatible local persona project from what the user describes in natural language. The user may provide:

- a one-sentence concept
- identity, personality, voice, relationship, or boundary requirements
- rules written as “when X happens, they do Y”
- desired strengths, flaws, habits, emotional reactions, and examples
- optional reference files or selected chats
- an existing PersonaDock project that needs refinement

The result must be a normal PersonaDock project and, when requested, a validated `.personapack`.

## Modes

Choose the mode automatically from the request:

1. **Create:** build a new persona from natural-language requirements.
2. **Refine:** edit an existing PersonaDock project without discarding reviewed content.
3. **Hybrid:** combine desired traits with selected examples or chat records. Desired traits are design requirements; observations from records are evidence. Keep the two distinguishable when they conflict.

For evidence-first imitation of a real speaker, use `persona-distiller`. This Skill may still consume user-selected references when the goal is design rather than strict reconstruction.

## Core rules

1. Default to a private local project. Do not require GitHub, a fork, a PR, or publication.
2. Ask only for concrete missing information that materially changes the persona. Do not force a long questionnaire when the user has already supplied enough detail.
3. Convert vague adjectives into observable behavior. Write rules as: trigger -> behavior -> limit.
4. Keep SOUL concise. Put identity, stable traits, hard boundaries, Skill routing, and memory honesty in SOUL; put detailed scenes and examples in Skill references.
5. Do not invent user history. User-authored fictional canon may be stored as persona background; real user facts and shared events require explicit confirmation before entering packaged Memory.
6. Preserve deliberate flaws and disagreements when requested. Do not flatten every persona into a universally agreeable assistant.
7. Resolve contradictions explicitly. Prefer the user's latest direct requirement, then document remaining uncertainty under `.private/design-notes.md`.
8. Do not publish or upload anything unless the user explicitly asks.

## Workflow

### 1. Understand the persona

Extract concrete requirements into these groups:

- identity and relationship role
- 3–7 stable core traits
- voice, vocabulary, reply length, rhythm, and prohibited styles
- strengths and intentional flaws
- emotional behavior
- daily, playful, serious, conflict, repair, boundary, and reunion scenarios
- relationship progression
- memory policy and canonical background

For short requests, infer reasonable non-sensitive defaults and mark them as design choices rather than user facts.

### 2. Create or locate the project

For a new project:

```bash
personadock init "<output-project>" --id "<persona-id>" --name "<display-name>"
```

For an existing project, locate `companion.yaml` and edit in place. Never overwrite reviewed Memory or user-authored references without showing the change.

### 3. Build by layer

- **SOUL:** stable identity, core traits, compact voice, hard boundaries, Skill triggers, and memory lookup rules.
- **Persona Skill:** detailed behavior and routing in `skills/persona/SKILL.md`.
- **References:** write `voice.md`, `daily-scenarios.md`, `emotional-support.md`, `conflict-repair.md`, `relationship-stages.md`, and `examples.md`.
- **Memory:** keep real-user facts out unless explicitly confirmed. Put unconfirmed candidates in `.private/memory-candidates.jsonl`.
- **Tests:** cover the user's important “when X, do Y” rules, memory honesty, routing, boundaries, conflict, and style consistency.

Follow `references/output-contract.md` and `references/prompt-contract.md`.

### 4. Show a review summary

Before packaging, show:

- the compact SOUL design
- the main scenario rules added to the persona Skill
- intentional flaws and boundaries
- assumptions or unresolved contradictions
- any proposed Memory entries

A user may approve the design as a whole, but each real-user Memory entry must still be explicit and reviewable.

### 5. Validate and package

```bash
personadock validate "<output-project>"
personadock build "<output-project>"
personadock pack "<output-project>"
personadock inspect "<output-project>/dist/<id>-<version>.personapack"
```

Fix source files when validation fails. Do not bypass validation.

### 6. Optional installation

Only when requested:

```bash
personadock install "<package.personapack>" --target hermes
personadock install "<package.personapack>" --target openclaw
```

## Example request translation

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

## Completion checks

- `personadock validate` passes.
- SOUL stays below `hard_limit_chars`.
- Every important “when X” requirement appears in a Skill reference or test.
- Detailed persona information is not overloaded into SOUL.
- Raw references and private notes are absent from the package.
- Every packaged real-user Memory entry has `reviewed: true`.
- `personadock inspect` reports `integrity: ok`.
