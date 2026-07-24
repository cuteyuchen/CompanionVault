# PersonaDock Project Output Contract

The unified builder must create a normal PersonaDock project. It must not invent a separate final format for creation, distillation, hybrid generation, or refinement.

## Required tree

```text
<project>/
├── companion.yaml
├── skills/
│   └── persona/
│       ├── SKILL.md
│       └── references/
│           ├── voice.md
│           ├── daily-scenarios.md
│           ├── emotional-support.md
│           ├── conflict-repair.md
│           ├── relationship-stages.md
│           └── examples.md
├── memory/
│   ├── profile.yaml
│   ├── seed.jsonl
│   └── policy.yaml
├── tests/
│   └── scenarios.yaml
├── .private/
│   ├── design-notes.md
│   ├── source-notes.md
│   ├── normalized.jsonl
│   ├── evidence.jsonl
│   ├── memory-candidates.jsonl
│   └── REVIEW.md
└── .gitignore
```

Only the private files needed for the selected mode must be created. `.private/` is never packaged.

## companion.yaml

Use `schema_version: 2` and these top-level fields:

```yaml
schema_version: 2
id: example-persona
version: 0.1.0
name: Example Persona
locale: zh-CN
summary: A private PersonaDock persona generated from reviewed requirements or evidence.

soul:
  identity: A concise, stable identity statement.
  core_traits:
    - Stable trait one
    - Stable trait two
    - Stable trait three
  voice: One compact voice rule.
  boundaries:
    - Do not invent memories.
    - Respect user relationships and autonomy.
  skill_triggers:
    - Use the persona Skill for persona-specific expression.
    - Use it for emotional, relationship, or conflict scenarios.
    - Search Memory before answering questions about past facts.
  target_chars: 1800
  hard_limit_chars: 2800

skill:
  id: example-persona-persona
  description: Detailed behavior and scenario guidance.

memory:
  enabled: true
  private_by_default: true
  bundle_policy: reviewed
  never_invent: true

targets:
  - hermes
  - openclaw
  - generic
```

## Layer rules

- SOUL is always-loaded routing and identity data, not a complete persona encyclopedia.
- Skill references hold detailed behavior, scenes, examples, flaws, and relationship progression.
- Memory holds only real, reviewable facts or explicitly approved canonical facts.
- `.private/` holds assumptions, source notes, normalized records, evidence, and uncertain material.
- Design requirements and evidence observations must remain distinguishable in Hybrid mode.

## Validation

The final project must pass:

```bash
personadock validate <project>
```
