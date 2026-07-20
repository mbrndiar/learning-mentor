from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SKILL = ROOT / "skills" / "guided-learning" / "SKILL.md"
AGENT = ROOT / "agents" / "learning-mentor.agent.md"
CODEX = ROOT / "integrations" / "codex" / "learning-mentor.toml"


def frontmatter_value(path: Path, key: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+)$", text)
    if match is None:
        raise AssertionError(f"{path} has no {key!r} frontmatter")
    return match.group(1).strip()


class DistributionTests(unittest.TestCase):
    def test_skill_name_matches_directory(self) -> None:
        self.assertEqual(frontmatter_value(SKILL, "name"), SKILL.parent.name)

    def test_agent_uses_portable_frontmatter_and_generic_sources(self) -> None:
        text = AGENT.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        self.assertEqual(frontmatter_value(AGENT, "name"), "learning-mentor")
        self.assertNotIn("tools:", frontmatter)
        self.assertNotIn("model:", frontmatter)
        self.assertIn(".learning-mentor.toml", text)
        self.assertIn(".agents/skills/guided-learning/SKILL.md", text)
        self.assertIn(
            ".learning-mentor/skills/guided-learning/SKILL.md",
            text,
        )
        self.assertRegex(text, r"invalid course\s+integration")
        self.assertIn("Never describe state as repository-local", text)
        self.assertNotIn("learning-python-adapter", text)
        self.assertNotIn(".github/skills/learning-tutor-core", text)

    def test_codex_launcher_only_points_to_canonical_sources(self) -> None:
        with CODEX.open("rb") as stream:
            configuration = tomllib.load(stream)
        instructions = configuration["developer_instructions"]
        self.assertEqual(configuration["name"], "learning-mentor")
        self.assertIn(
            ".learning-mentor/agents/learning-mentor.agent.md",
            instructions,
        )
        self.assertIn(
            ".agents/skills/guided-learning/SKILL.md",
            instructions,
        )
        self.assertLess(len(instructions.splitlines()), 10)

    def test_required_shared_files_exist(self) -> None:
        expected = (
            SKILL,
            AGENT,
            CODEX,
            ROOT / "skills" / "guided-learning" / "references" / "adapter-protocol.md",
            ROOT / "skills" / "guided-learning" / "references" / "socratic-policy.md",
            ROOT / "skills" / "guided-learning" / "references" / "state-model.md",
            ROOT / "skills" / "guided-learning" / "scripts" / "learning_state.py",
        )
        self.assertEqual([path for path in expected if not path.is_file()], [])


if __name__ == "__main__":
    unittest.main()
