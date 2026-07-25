"""Tests for the guideline repository validator."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


VALIDATOR_PATH = Path(__file__).resolve().parents[1] / "Scripts" / "validate_guidelines.py"
SPEC = importlib.util.spec_from_file_location("validate_guidelines", VALIDATOR_PATH)
assert SPEC is not None
assert SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class SemanticVersionTests(unittest.TestCase):
    """Verifies the supported Semantic Versioning grammar."""

    def test_valid_versions(self) -> None:
        """Accepts core, prerelease, and build metadata forms."""
        versions = (
            "0.0.2",
            "1.2.3-rc.1+build.5",
            "1.0.0-alpha-beta",
            "1.0.0+001",
        )

        for version in versions:
            with self.subTest(version=version):
                self.assertIsNotNone(VALIDATOR.SEMVER.fullmatch(version))

    def test_invalid_versions(self) -> None:
        """Rejects leading zeroes and incomplete identifiers."""
        versions = (
            "01.2.3",
            "1.02.3",
            "1.2.03",
            "1.2.3-01",
            "1.2.3-rc.01",
            "1.2.3+",
            "1.2.3-",
        )

        for version in versions:
            with self.subTest(version=version):
                self.assertIsNone(VALIDATOR.SEMVER.fullmatch(version))


class SwiftFormattingConfigurationTests(unittest.TestCase):
    """Verifies the shared Swift formatting contract."""

    def test_swift_format_configuration(self) -> None:
        """Accepts the exhaustive Xcode-aligned swift-format configuration."""
        errors: list[str] = []

        VALIDATOR.validate_swift_format_configuration(errors)

        self.assertEqual(errors, [])

    def test_swift_format_configuration_rejects_undocumented_rule_change(self) -> None:
        """Rejects a changed rule value even when the exhaustive key set is unchanged."""
        configuration = json.loads(
            VALIDATOR.SWIFT_FORMAT_CONFIGURATION.read_text(encoding="utf-8")
        )
        configuration["rules"]["NeverForceUnwrap"] = True

        with tempfile.TemporaryDirectory(dir=VALIDATOR.ROOT) as directory:
            path = Path(directory) / ".swift-format"
            path.write_text(json.dumps(configuration), encoding="utf-8")
            errors: list[str] = []

            with mock.patch.object(VALIDATOR, "SWIFT_FORMAT_CONFIGURATION", path):
                VALIDATOR.validate_swift_format_configuration(errors)

        self.assertTrue(
            any("NeverForceUnwrap must be False, found True" in error for error in errors)
        )

    def test_swift_format_configuration_requires_conditional_import_sorting(self) -> None:
        """Rejects disabling conditional import sorting."""
        configuration = json.loads(
            VALIDATOR.SWIFT_FORMAT_CONFIGURATION.read_text(encoding="utf-8")
        )
        configuration["orderedImports"]["includeConditionalImports"] = False

        with tempfile.TemporaryDirectory(dir=VALIDATOR.ROOT) as directory:
            path = Path(directory) / ".swift-format"
            path.write_text(json.dumps(configuration), encoding="utf-8")
            errors: list[str] = []

            with mock.patch.object(VALIDATOR, "SWIFT_FORMAT_CONFIGURATION", path):
                VALIDATOR.validate_swift_format_configuration(errors)

        self.assertTrue(
            any(
                "orderedImports.includeConditionalImports must be True" in error
                for error in errors
            )
        )

    def test_editor_configuration(self) -> None:
        """Accepts the shared Swift EditorConfig values."""
        errors: list[str] = []

        VALIDATOR.validate_editor_configuration(errors)

        self.assertEqual(errors, [])


class AgentGuidelinesAuditSkillTests(unittest.TestCase):
    """Verifies the mandatory completion-audit skill contract."""

    def test_audit_skill_contract(self) -> None:
        """Accepts the skill, Development rule, and consumer template."""
        errors: list[str] = []

        VALIDATOR.validate_audit_skill(errors)

        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
