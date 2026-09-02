#!/usr/bin/env python3
"""Validate String Catalogs and generated-symbol Swift source usage."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from prepare_localizable_symbols import symbol_issues


FORMAT_SPECIFIER_PATTERN = re.compile(
    r"%(?!%)"
    r"(?:(?P<position>[1-9]\d*)\$)?"
    r"(?:\((?P<name>[A-Za-z_][A-Za-z0-9_]*)\))?"
    r"(?P<format>[-+ #0']*(?:\d+|\*)?(?:\.(?:\d+|\*))?"
    r"(?:hh|h|ll|l|q|L|z|t|j)?[diouxXfFeEgGaAcCsSp@])"
)


def format_signature(value: str) -> tuple[tuple[int, str | None, str], ...]:
    """Return position, semantic name, and type for every printf placeholder."""
    signature: list[tuple[int, str | None, str]] = []
    implicit_position = 1
    for match in FORMAT_SPECIFIER_PATTERN.finditer(value):
        position_text = match.group("position")
        position = int(position_text) if position_text else implicit_position
        signature.append((position, match.group("name"), match.group("format")))
        implicit_position += 1
    return tuple(sorted(signature))


def string_unit_values(value: object) -> list[str]:
    """Return every leaf String Catalog value below one localization."""
    if isinstance(value, dict):
        string_unit = value.get("stringUnit")
        values = []
        if isinstance(string_unit, dict) and isinstance(string_unit.get("value"), str):
            values.append(string_unit["value"])
        for key, child in value.items():
            if key != "stringUnit":
                values.extend(string_unit_values(child))
        return values
    if isinstance(value, list):
        return [item for child in value for item in string_unit_values(child)]
    return []


def string_unit_states(value: object) -> list[str]:
    """Return every leaf String Catalog state below one localization."""
    if isinstance(value, dict):
        string_unit = value.get("stringUnit")
        states = []
        if isinstance(string_unit, dict) and isinstance(string_unit.get("state"), str):
            states.append(string_unit["state"])
        for key, child in value.items():
            if key != "stringUnit":
                states.extend(string_unit_states(child))
        return states
    if isinstance(value, list):
        return [item for child in value for item in string_unit_states(child)]
    return []


def display_signature(signature: tuple[tuple[int, str | None, str], ...]) -> str:
    """Render a normalized placeholder signature for diagnostics."""
    specifiers = [
        f"%{f'({name})' if name else ''}{format_value}"
        for _, name, format_value in signature
    ]
    return ", ".join(specifiers) or "none"


def format_signature_issues(catalog: dict[str, object]) -> list[str]:
    """Return translated values whose placeholder signature differs from source."""
    source_language = catalog.get("sourceLanguage")
    strings = catalog.get("strings")
    if not isinstance(source_language, str) or not isinstance(strings, dict):
        return ["catalog structure is invalid"]

    issues: list[str] = []
    for key, entry in strings.items():
        if not isinstance(entry, dict) or entry.get("extractionState") == "stale":
            continue
        localizations = entry.get("localizations")
        if not isinstance(localizations, dict):
            continue
        source = localizations.get(source_language)
        source_signatures = {format_signature(value) for value in string_unit_values(source)}
        if len(source_signatures) != 1:
            issues.append(f"{key}: source variants have inconsistent format specifiers")
            continue
        expected = next(iter(source_signatures))
        for language, localization in localizations.items():
            if language == source_language:
                continue
            for value in string_unit_values(localization):
                actual = format_signature(value)
                if actual != expected:
                    issues.append(
                        f"{key} [{language}]: format specifiers {display_signature(actual)} "
                        f"do not match {display_signature(expected)}"
                    )
    return issues


def translation_state_issues(
    catalog: dict[str, object], required_languages: set[str]
) -> list[str]:
    """Return missing required localizations and unfinished translated values."""
    source_language = catalog.get("sourceLanguage")
    strings = catalog.get("strings")
    if not isinstance(source_language, str) or not isinstance(strings, dict):
        return ["catalog structure is invalid"]

    issues: list[str] = []
    for key, entry in strings.items():
        if not isinstance(entry, dict) or entry.get("extractionState") == "stale":
            continue
        localizations = entry.get("localizations")
        if not isinstance(localizations, dict):
            localizations = {}
        for language in sorted(required_languages - {source_language}):
            if language not in localizations:
                issues.append(f"{key} [{language}]: required localization is missing")
        for language, localization in localizations.items():
            if language == source_language:
                continue
            states = string_unit_states(localization)
            if not states:
                issues.append(f"{key} [{language}]: localization has no string units")
                continue
            unfinished = sorted({state for state in states if state in {"new", "needs_review"}})
            if unfinished:
                issues.append(f"{key} [{language}]: unfinished states {', '.join(unfinished)}")
    return issues


def literal_localization_references(source_directories: list[Path]) -> list[str]:
    """Return checked-in Swift locations that still use localization literals."""
    source_paths = sorted(
        {
            path
            for directory in source_directories
            for path in directory.rglob("*.swift")
            if path.is_file()
        }
    )
    if not source_paths:
        return []

    with tempfile.TemporaryDirectory() as output_directory:
        command = [
            "xcrun",
            "xcstringstool",
            "extract",
            "--modern-localizable-strings",
            "--SwiftUI",
            "--omit-empty-stringsdata",
            "--output-directory",
            output_directory,
            *map(str, source_paths),
        ]
        result = subprocess.run(command, capture_output=True, check=False, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "xcstringstool extract failed")

        references: list[str] = []
        for stringsdata_path in sorted(Path(output_directory).glob("*.stringsdata")):
            with stringsdata_path.open(encoding="utf-8") as stringsdata_file:
                stringsdata = json.load(stringsdata_file)
            source = Path(stringsdata.get("source", stringsdata_path.name))
            for entry in stringsdata.get("tables", {}).get("Localizable", []):
                location = entry.get("location", {})
                line = location.get("startingLine", "?")
                key = entry.get("key", "<unknown>")
                references.append(f"{source}:{line}: {key}")
        return sorted(references)


def main(argv: list[str] | None = None) -> int:
    """Validate configured catalogs and Swift source directories."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog-directory",
        action="append",
        required=True,
        type=Path,
        help="Directory containing managed .xcstrings files; repeat as needed.",
    )
    parser.add_argument(
        "--source-directory",
        action="append",
        required=True,
        type=Path,
        help="Directory containing checked-in Swift source; repeat as needed.",
    )
    parser.add_argument(
        "--symbol-catalog",
        action="append",
        default=[],
        type=Path,
        help="Catalog required to use generated symbols; defaults to discovered Localizable.xcstrings files.",
    )
    parser.add_argument(
        "--required-language",
        action="append",
        default=[],
        help="Language identifier required on every active entry; repeat as needed.",
    )
    arguments = parser.parse_args(argv)

    catalog_paths = sorted(
        {
            path
            for directory in arguments.catalog_directory
            for path in directory.rglob("*.xcstrings")
            if path.is_file()
        }
    )
    if not catalog_paths:
        print("No String Catalogs found in the configured directories.", file=sys.stderr)
        return 1

    symbol_catalogs = set(arguments.symbol_catalog) or {
        path for path in catalog_paths if path.name == "Localizable.xcstrings"
    }
    unknown_symbol_catalogs = symbol_catalogs - set(catalog_paths)
    if unknown_symbol_catalogs:
        for path in sorted(unknown_symbol_catalogs):
            print(f"{path}: generated-symbol catalog is outside the configured catalogs.", file=sys.stderr)
        return 1

    required_languages = set(arguments.required_language)
    failed = False
    for catalog_path in catalog_paths:
        try:
            with catalog_path.open(encoding="utf-8") as catalog_file:
                catalog = json.load(catalog_file)
        except (OSError, json.JSONDecodeError) as error:
            print(f"{catalog_path}: {error}", file=sys.stderr)
            failed = True
            continue

        strings = catalog.get("strings")
        if not isinstance(strings, dict):
            print(f"{catalog_path}: catalog has no strings dictionary.", file=sys.stderr)
            failed = True
            continue

        stale_keys = sorted(
            key
            for key, entry in strings.items()
            if isinstance(entry, dict) and entry.get("extractionState") == "stale"
        )
        if stale_keys:
            failed = True
            print(f"{catalog_path}: stale extracted strings:", file=sys.stderr)
            for key in stale_keys:
                print(f"  - {key}", file=sys.stderr)

        if catalog_path in symbol_catalogs:
            issues = symbol_issues(catalog)
            if issues:
                failed = True
                print(f"{catalog_path}: entries that are not symbol-ready:", file=sys.stderr)
                for issue in issues:
                    print(f"  - {issue}", file=sys.stderr)

        format_issues = format_signature_issues(catalog)
        if format_issues:
            failed = True
            print(f"{catalog_path}: format-specifier mismatches:", file=sys.stderr)
            for issue in format_issues:
                print(f"  - {issue}", file=sys.stderr)

        state_issues = translation_state_issues(catalog, required_languages)
        if state_issues:
            failed = True
            print(f"{catalog_path}: localization-state issues:", file=sys.stderr)
            for issue in state_issues:
                print(f"  - {issue}", file=sys.stderr)

    try:
        references = literal_localization_references(arguments.source_directory)
    except (OSError, RuntimeError, json.JSONDecodeError) as error:
        print(f"Could not validate Swift localization literals: {error}", file=sys.stderr)
        return 1

    if references:
        failed = True
        print("Checked-in Swift localization literals must use generated symbols:", file=sys.stderr)
        for reference in references:
            print(f"  - {reference}", file=sys.stderr)

    if failed:
        print(
            "Prepare generated-symbol catalogs, migrate reported Swift literals, and resolve catalog issues.",
            file=sys.stderr,
        )
        return 1

    print("String Catalog validation passed: symbols, states, format signatures, and Swift source are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
