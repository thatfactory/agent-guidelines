"""Tests for shared String Catalog preparation and validation."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "Scripts"
sys.path.insert(0, str(SCRIPTS))
import prepare_localizable_symbols as PREPARATION  # noqa: E402
import validate_string_catalogs as VALIDATION  # noqa: E402


def localization(value: str, state: str = "translated") -> dict[str, object]:
    """Create one simple String Catalog localization fixture."""
    return {"stringUnit": {"state": state, "value": value}}


class SymbolPreparationTests(unittest.TestCase):
    """Verifies bounded legacy-catalog preparation."""

    def test_prepares_active_entries_and_preserves_stale_entries(self) -> None:
        """Makes active values symbol-ready without silently reviving stale keys."""
        stale = {"extractionState": "stale", "localizations": {"en": localization("Old")}}
        catalog = {
            "sourceLanguage": "en",
            "strings": {
                "Legacy value": {
                    "comment": "Visible title",
                    "extractionState": "extracted_with_value",
                    "localizations": {"de": localization("Alter Wert")},
                },
                "Old value": stale,
            },
            "version": "1.1",
        }

        prepared = PREPARATION.prepare_catalog(catalog)

        entry = prepared["strings"]["Legacy value"]
        self.assertEqual(entry["extractionState"], "manual")
        self.assertEqual(entry["comment"], "Visible title")
        self.assertEqual(entry["localizations"]["en"], localization("Legacy value"))
        self.assertEqual(entry["localizations"]["de"], localization("Alter Wert"))
        self.assertEqual(prepared["strings"]["Old value"], stale)

    def test_rejects_manual_entry_without_source_value(self) -> None:
        """Does not invent source copy for an already-semantic manual key."""
        catalog = {
            "sourceLanguage": "en",
            "strings": {
                "semanticKey": {
                    "extractionState": "manual",
                    "localizations": {"de": localization("Wert")},
                }
            },
        }

        with self.assertRaisesRegex(ValueError, "manual entry has no en source value"):
            PREPARATION.prepare_catalog(catalog)


class CatalogValidationTests(unittest.TestCase):
    """Verifies generic catalog invariants without project-specific paths."""

    def test_accepts_matching_named_format_signatures(self) -> None:
        """Accepts translated placeholders with identical position, name, and type."""
        catalog = {
            "sourceLanguage": "en",
            "strings": {
                "summary": {
                    "extractionState": "manual",
                    "localizations": {
                        "en": localization("%1$(count)lld items"),
                        "de": localization("%1$(count)lld Einträge", "machine_translated"),
                    },
                }
            },
        }

        self.assertEqual(VALIDATION.format_signature_issues(catalog), [])
        self.assertEqual(VALIDATION.translation_state_issues(catalog, {"de"}), [])

    def test_rejects_format_mismatch_missing_language_and_unfinished_state(self) -> None:
        """Reports translation defects independently from consumer vocabulary."""
        catalog = {
            "sourceLanguage": "en",
            "strings": {
                "count": {
                    "extractionState": "manual",
                    "localizations": {
                        "en": localization("%1$(count)lld items"),
                        "de": localization("%1$(value)@ Einträge", "needs_review"),
                    },
                }
            },
        }

        format_issues = VALIDATION.format_signature_issues(catalog)
        state_issues = VALIDATION.translation_state_issues(catalog, {"de", "fr"})

        self.assertTrue(any("do not match" in issue for issue in format_issues))
        self.assertIn("count [fr]: required localization is missing", state_issues)
        self.assertIn("count [de]: unfinished states needs_review", state_issues)

    def test_symbol_issues_ignore_stale_entries(self) -> None:
        """Leaves stale-entry disposition to the dedicated stale-key validation."""
        catalog = {
            "sourceLanguage": "en",
            "strings": {"Old": {"extractionState": "stale"}},
        }

        self.assertEqual(PREPARATION.symbol_issues(catalog), [])


if __name__ == "__main__":
    unittest.main()
