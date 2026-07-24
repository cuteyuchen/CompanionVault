# PersonaDock Distillation Output Contract

Create a normal PersonaDock project. Do not invent a separate output format.

## Required tree

```text
<project>/
├── companion.yaml
├── skills/persona/SKILL.md
├── skills/persona/references/
├── memory/profile.yaml
├── memory/seed.jsonl
├── memory/policy.yaml
├── tests/scenarios.yaml
├── .private/
└── .gitignore
```

## companion.yaml

Use `schema_version: 2` and include: `id`, `version`, `name`, `locale`, `summary`, `soul`, `skill`, `memory`, and `targets`.

SOUL contains concise identity, core traits, voice, boundaries, Skill triggers, and character budgets. Skill details live under `skills/persona/`. Memory defaults to private and only reviewed records may be packaged.

Recommended targets:

```yaml
targets:
  - hermes
  - openclaw
  - generic
```

The final project must pass:

```bash
personadock validate <project>
```
