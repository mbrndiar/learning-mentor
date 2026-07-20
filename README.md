# Learning Mentor

Shared agent and guided-learning policy for hands-on `learning-*` repositories.

## Status

This repository is in the extraction phase. The state engine is covered by its
existing unit tests, but course integration has not yet passed the planned
GitHub Copilot CLI, OpenAI Codex, and Claude Code pilot.

Codex custom-agent TOML currently describes a subagent. The pilot must prove
that switching into and steering that agent thread provides a satisfactory
long-running mentoring conversation; otherwise Codex will need a thin
main-thread launcher that still reads the same canonical agent and skill.

## Components

| Path | Role |
| --- | --- |
| [`agents/learning-mentor.agent.md`](agents/learning-mentor.agent.md) | Canonical cross-course mentor prompt |
| [`skills/guided-learning/`](skills/guided-learning/) | Teaching, evidence, state, review, solution-lock, and learner-ownership policy |
| [`integrations/codex/learning-mentor.toml`](integrations/codex/learning-mentor.toml) | Thin Codex custom-agent launcher |

Courses retain their own `<ecosystem>-learning-path` skills. The shared mentor
does not own course commands, diagnostics, manifests, selectors, or milestones.

## Target course layout

Each course pins this repository once:

```text
.learning-mentor/                         # Git submodule
.agents/skills/guided-learning            # link to shared skill
.agents/skills/<ecosystem>-learning-path  # course-owned skill
.github/agents/learning-mentor.agent.md    # Copilot entrypoint
.claude/agents/learning-mentor.md          # Claude entrypoint
.claude/skills/...                         # Claude skill entrypoints
.codex/agents/learning-mentor.toml         # Codex entrypoint
.learning-mentor.toml                      # course integration descriptor
```

Clone a migrated course with:

```bash
git clone --recurse-submodules REPOSITORY_URL
```

Initialize a missing submodule with:

```bash
git submodule update --init --recursive
```

## State compatibility

The initial extraction intentionally preserves:

- `COPILOT_LEARNING_TUTOR_DB`;
- `COPILOT_LEARNING_TUTOR_BUSY_TIMEOUT_MS`;
- `$XDG_DATA_HOME/copilot-learning-tutor/state.sqlite3`;
- the existing SQLite schema; and
- remote plus Git commit course identity.

Renaming those compatibility surfaces is a separate migration, not part of
extracting the shared mentor.

## Development

Run the dependency-free tests:

```bash
python -m unittest discover -s skills/guided-learning/tests -p "test_*.py"
python -m unittest discover -s tests -p "test_*.py"
```

The second command covers distribution structure and common agent metadata.
