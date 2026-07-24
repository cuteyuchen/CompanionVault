# Natural-language Persona Design Contract

## Input styles

The builder must support all of these without requiring a separate format:

- “Create a calm study partner who becomes strict when I procrastinate.”
- “They are usually playful, but when I am sad they stop joking and listen first.”
- a long character description
- bullet points of traits and scenarios
- corrections to an existing persona
- desired traits combined with selected examples or chats

## Convert descriptions into behavior

For each requirement, derive:

```text
trigger -> observable behavior -> limit -> reference file -> test
```

Example:

```text
User is exhausted
-> use shorter sentences, reduce teasing, offer one small next step
-> do not lecture or repeatedly ask questions
-> emotional-support.md
-> tired-support scenario test
```

Do not leave important rules only as adjectives such as “gentle”, “tsundere”, “mature”, or “cute”.

## Recommended design matrix

Capture at least:

| Area | Questions the design must answer |
|---|---|
| Identity | Who are they and what role do they have? |
| Core traits | Which traits remain stable across scenes? |
| Voice | How long, direct, playful, formal, or expressive are replies? |
| Daily behavior | How do they chat, tease, share, ask, and end topics? |
| Emotional support | What changes for sadness, anxiety, anger, or exhaustion? |
| Conflict | What do they defend, admit, refuse, and repair? |
| Relationship | How does closeness progress without sudden jumps? |
| Flaws | Which imperfections make the persona distinctive? |
| Boundaries | What must they never claim, pressure, reveal, or invent? |
| Memory | Which facts are canonical, private, uncertain, or forbidden? |

## Defaults

When the user gives only a short concept, use conservative defaults:

- natural conversational language
- no invented shared history
- no exclusivity or dependency pressure
- no sudden relationship escalation
- direct, serious language in high-risk or genuinely distressed scenes
- detailed persona behavior stored in Skill references instead of SOUL

Record non-obvious defaults in `.private/design-notes.md` so the user can revise them.

## Contradictions

When requirements conflict:

1. Prefer the user's latest explicit instruction.
2. Preserve scene-specific differences when both can be true.
3. Ask one concrete question only when the conflict changes core behavior.
4. Otherwise choose a safe interpretation and document it.

Example:

```text
“Very talkative” + “short replies”
```

may become:

```text
Uses short consecutive messages in casual chat; switches to one complete response for serious topics.
```

## Fictional canon versus Memory

Persona background such as occupation, setting, fictional history, and relationship premise belongs in identity or Skill references unless the runtime must retrieve it as a fact.

Real user preferences, real shared events, and personal details must not enter `memory/seed.jsonl` without explicit review. User-authored fictional canon may be marked as reviewed only when its fictional status is clear.
