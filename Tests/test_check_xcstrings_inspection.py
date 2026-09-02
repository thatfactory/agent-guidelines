"""Tests for the audit skill's String Catalog inspection evidence gate."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath


CHECKER_PATH = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "agent-guidelines-audit"
    / "scripts"
    / "check_xcstrings_inspection.py"
)
SPEC = importlib.util.spec_from_file_location("check_xcstrings_inspection", CHECKER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


class StringCatalogInspectionTests(unittest.TestCase):
    """Verifies changed-catalog discovery and fail-closed evidence coverage."""

    def git(self, root: Path, *arguments: str) -> None:
        """Run a Git fixture command."""
        subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True)

    def test_discovers_modified_and_untracked_catalogs(self) -> None:
        """Finds catalog changes across the base diff and untracked files."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.git(root, "init")
            self.git(root, "config", "user.email", "agent@example.com")
            self.git(root, "config", "user.name", "Agent")
            catalog = root / "Sources" / "Localizable.xcstrings"
            catalog.parent.mkdir(parents=True)
            catalog.write_text("{}\n", encoding="utf-8")
            self.git(root, "add", ".")
            self.git(root, "commit", "-m", "Initial fixture")

            catalog.write_text('{"sourceLanguage":"en"}\n', encoding="utf-8")
            untracked = root / "Tests" / "Fixtures.xcstrings"
            untracked.parent.mkdir(parents=True)
            untracked.write_text("{}\n", encoding="utf-8")

            self.assertEqual(
                CHECKER.changed_catalogs(root, "HEAD"),
                {
                    PurePosixPath("Sources/Localizable.xcstrings"),
                    PurePosixPath("Tests/Fixtures.xcstrings"),
                },
            )

    def test_reports_missing_and_unexpected_inspection_evidence(self) -> None:
        """Rejects incomplete or mismatched catalog-editor inspection claims."""
        changed = {PurePosixPath("Sources/Localizable.xcstrings")}
        inspected = {PurePosixPath("Sources/Other.xcstrings")}

        self.assertEqual(
            CHECKER.inspection_coverage_errors(changed, inspected),
            [
                "missing Xcode catalog-editor inspection evidence: "
                "Sources/Localizable.xcstrings",
                "inspection evidence does not match a changed String Catalog: "
                "Sources/Other.xcstrings",
            ],
        )

    def test_command_fails_closed_without_editor_evidence(self) -> None:
        """Returns failure when a changed catalog has no inspection record."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.git(root, "init")
            self.git(root, "config", "user.email", "agent@example.com")
            self.git(root, "config", "user.name", "Agent")
            catalog = root / "Localizable.xcstrings"
            catalog.write_text("{}\n", encoding="utf-8")
            self.git(root, "add", ".")
            self.git(root, "commit", "-m", "Initial fixture")
            catalog.write_text('{"sourceLanguage":"en"}\n', encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(CHECKER_PATH),
                    "--repository",
                    str(root),
                    "--base-ref",
                    "HEAD",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn(
                "missing Xcode catalog-editor inspection evidence: Localizable.xcstrings",
                result.stderr,
            )
            self.assertIn("--evidence-output is required", result.stderr)

    def test_writes_zero_diagnostic_evidence(self) -> None:
        """Records the base, Xcode build, and zero diagnostics for every catalog."""
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            root = temporary / "repository"
            root.mkdir()
            output = temporary / "evidence.json"

            CHECKER.write_evidence(
                output,
                root,
                "origin/main",
                "Xcode 27.0\nBuild version 18A1",
                {PurePosixPath("Sources/Localizable.xcstrings")},
            )

            evidence = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(evidence["baseRef"], "origin/main")
            self.assertEqual(evidence["xcodeVersion"], "Xcode 27.0\nBuild version 18A1")
            self.assertEqual(
                evidence["catalogs"],
                [
                    {
                        "path": "Sources/Localizable.xcstrings",
                        "catalogEditorErrors": 0,
                        "catalogEditorWarnings": 0,
                    }
                ],
            )


if __name__ == "__main__":
    unittest.main()
