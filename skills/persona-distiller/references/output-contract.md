# PersonaDock Distillation Output Contract

The distiller must create a normal PersonaDock project. It must not invent a separate intermediate format.

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
│   ├── normalized.jsonl
│   ├── evidence.jsonl
│   ├── memory-candidates.jsonl
│   └── REVIEW.md
└── .gitignore
```

## companion.yaml

Use `schema_version: 2` and these top-level fields:

```yaml
schema_version: 2
id: example-persona
version: 0.1.0
name: Example Persona
locale: zh-CN
summary: A private PersonaDock persona generated from reviewed evidence.

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
- Skill references hold detailed behavior, scenes, examples, and relationship progression.
- Memory holds only real, reviewable facts.
- `.private/` holds raw or uncertain material and is never packaged.

## Validation

The final project must pass:

```bash
personadock validate <project>
```
