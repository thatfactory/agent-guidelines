"""Tests for consumer agent-guidelines integration validation."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


VALIDATOR_PATH = (
    Path(__file__).resolve().parents[1] / "Scripts" / "validate_consumer_setup.py"
)
SPEC = importlib.util.spec_from_file_location("validate_consumer_setup", VALIDATOR_PATH)
assert SPEC is not None
assert SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ConsumerSetupTests(unittest.TestCase):
    """Verifies checked-in consumer guidance and symlink wiring."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory(dir=VALIDATOR.GUIDELINES_ROOT)
        self.consumer_root = Path(self.temporary_directory.name)
        (self.consumer_root / "AgentGuidelines").symlink_to(
            VALIDATOR.GUIDELINES_ROOT,
            target_is_directory=True,
        )

        template = (
            VALIDATOR.GUIDELINES_ROOT / "Templates" / "AGENTS.md"
        ).read_text(encoding="utf-8")
        contract_errors: list[str] = []
        contract = VALIDATOR.extract_contract(template, contract_errors, "template")
        self.assertEqual(contract_errors, [])
        self.assertIsNotNone(contract)

        agents = f"""# Project Instructions

{contract}

## Codex review scope

For consumer pull requests, verify exact tagged-tree provenance before excluding
`AgentGuidelines/**`, and confirm the required `.gitattributes` rule.
"""
        (self.consumer_root / "AGENTS.md").write_text(agents, encoding="utf-8")
        (self.consumer_root / ".gitattributes").write_text(
            "AgentGuidelines/** linguist-generated\n",
            encoding="utf-8",
        )

        skill_parent = self.consumer_root / ".agents" / "skills"
        skill_parent.mkdir(parents=True)
        (skill_parent / "agent-guidelines-audit").symlink_to(
            VALIDATOR.GUIDELINES_ROOT
            / ".agents"
            / "skills"
            / "agent-guidelines-audit",
            target_is_directory=True,
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def validate(self, require_swift_format_links: bool = False) -> list[str]:
        errors: list[str] = []
        VALIDATOR.validate_consumer_setup(
            errors,
            self.consumer_root,
            require_swift_format_links=require_swift_format_links,
        )
        return errors

    def test_valid_consumer_setup(self) -> None:
        """Accepts a synchronized root contract and repository skill symlink."""
        self.assertEqual(self.validate(), [])

    def test_rejects_stale_code_review_contract(self) -> None:
        """Rejects a consumer root contract that drifted from the template."""
        agents_path = self.consumer_root / "AGENTS.md"
        agents = agents_path.read_text(encoding="utf-8")
        agents_path.write_text(agents.replace("P0/P1", "P0", 1), encoding="utf-8")

        self.assertTrue(
            any("code-review contract does not match" in error for error in self.validate())
        )

    def test_rejects_copied_audit_skill(self) -> None:
        """Rejects a stale-copy risk in place of the repository symlink."""
        skill = self.consumer_root / ".agents" / "skills" / "agent-guidelines-audit"
        skill.unlink()
        skill.mkdir()
        (skill / "SKILL.md").write_text("stale copy\n", encoding="utf-8")

        self.assertTrue(any("must be a symlink" in error for error in self.validate()))

    def test_requires_generated_attribute(self) -> None:
        """Rejects a consumer without the collapsed subtree diff rule."""
        (self.consumer_root / ".gitattributes").write_text("*.md text\n", encoding="utf-8")

        self.assertTrue(any("linguist-generated" in error for error in self.validate()))

    def test_rejects_missing_local_agent_link(self) -> None:
        """Rejects a local guideline pointer that does not resolve."""
        agents_path = self.consumer_root / "AGENTS.md"
        agents = agents_path.read_text(encoding="utf-8")
        agents_path.write_text(
            f"{agents}\n[Missing guide](AgentGuidelines/Guidelines/Missing.md)\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("missing local link target" in error for error in self.validate())
        )

    def test_optionally_requires_formatter_symlinks(self) -> None:
        """Requires formatter links only when the caller declares shared formatting."""
        self.assertEqual(self.validate(), [])

        errors = self.validate(require_swift_format_links=True)

        self.assertTrue(any("consumer .swift-format" in error for error in errors))
        self.assertTrue(any("consumer .editorconfig" in error for error in errors))

    def test_accepts_required_formatter_symlinks(self) -> None:
        """Accepts formatter links that resolve to the synchronized configurations."""
        (self.consumer_root / ".swift-format").symlink_to(
            VALIDATOR.GUIDELINES_ROOT / "Configurations" / "Swift" / ".swift-format"
        )
        (self.consumer_root / ".editorconfig").symlink_to(
            VALIDATOR.GUIDELINES_ROOT / "Configurations" / "Swift" / ".editorconfig"
        )

        self.assertEqual(self.validate(require_swift_format_links=True), [])


if __name__ == "__main__":
    unittest.main()
