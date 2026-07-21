"""Tests for the guideline repository validator."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
