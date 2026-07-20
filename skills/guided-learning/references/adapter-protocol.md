# Learning-path adapter protocol

## Purpose

The Learning Mentor owns teaching and evidence policy. A course-owned
`<ecosystem>-learning-path` skill owns course discovery, native commands,
diagnostics, selectors, and milestone routing. The adapter protocol connects
them without teaching the shared mentor a particular language, build tool, or
repository layout.

## Course descriptor

Each course provides `.learning-mentor.toml` at its Git root:

```toml
schema_version = 1

[adapter]
protocol = "1"
skill = ".agents/skills/python-learning-path/SKILL.md"
command = [
  "python",
  ".agents/skills/python-learning-path/scripts/course_adapter.py",
]

[state]
command = [
  "python",
  ".agents/skills/guided-learning/scripts/learning_state.py",
]
```

Rules:

- `schema_version` must equal `1`.
- `adapter.protocol` must equal `"1"`.
- `adapter.skill` must be a repository-relative path to an existing `SKILL.md`.
- `adapter.command` and `state.command` must be non-empty arrays of non-empty
  strings.
- Commands are argument vectors. Do not store shell operators, pipelines,
  redirections, substitutions, or environment assignments in them.
- Relative paths must remain inside the course repository.
- The descriptor selects exactly one learning-path skill.
- A missing or invalid field is a startup error, not permission to infer a
  replacement.

## Adapter operations

Append one operation to the declared `adapter.command`.

### `validate`

Validates the course manifest, required paths, stable IDs, prerequisites,
commands, selectors, outcomes, solution locks, and adapter-specific support
boundary.

Success:

- exits with status zero;
- writes one compact JSON object to standard output;
- includes `"status":"valid"`;
- identifies the adapter protocol and manifest schema; and
- includes no warnings disguised as success.

Failure:

- exits nonzero;
- writes a concise categorized diagnostic to standard error; and
- does not emit success-shaped JSON.

### `state-projection`

Produces the neutral graph consumed by `learning_state.py`.

Success writes:

```json
{
  "concepts": [
    {
      "id": "concept.example",
      "title": "Example",
      "order": 10,
      "prerequisites": [],
      "solution_unlock_after": 1
    }
  ]
}
```

Requirements:

- `id` is the manifest's stable objective ID.
- `title` is display text and never the state key.
- `order` is an integer used only for deterministic selection.
- `prerequisites` contains known stable IDs.
- `solution_unlock_after` is an integer greater than or equal to one.
- The graph is acyclic.
- Every trackable objective appears exactly once.
- Output is deterministic for an unchanged manifest.

The shared skill consumes this projection but does not parse the course
manifest.

## JSON and process boundary

- Parse standard output as JSON only after exit status zero.
- Keep diagnostics on standard error.
- Do not import adapter modules directly.
- Do not replace production commands with test fixtures.
- When piping projection into `init-course`, verify both producer and consumer
  statuses.
- A timeout, invalid JSON document, unsupported version, or missing executable
  makes current course state unavailable.

## Versioning

The descriptor schema, adapter protocol, state projection, and state database
schema are separate compatibility axes.

A breaking adapter change follows expand/migrate/contract:

1. `guided-learning` supports old and new protocols.
2. Course learning paths migrate independently.
3. The supported course matrix passes.
4. A later major release removes the old protocol.

Stable objective IDs and course identity do not change merely because an agent,
skill, path, or protocol implementation is renamed.
