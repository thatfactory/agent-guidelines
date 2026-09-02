#!/usr/bin/env python3
"""Prepare String Catalog entries for generated Swift symbols."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any


def mark_string_units_translated(value: Any) -> None:
    """Mark every source-language string unit in a localization as translated."""
    if isinstance(value, dict):
        string_unit = value.get("stringUnit")
        if isinstance(string_unit, dict):
            string_unit["state"] = "translated"
        for child in value.values():
            mark_string_units_translated(child)
    elif isinstance(value, list):
        for child in value:
            mark_string_units_translated(child)


def prepare_entry(key: str, entry: dict[str, Any], source_language: str) -> dict[str, Any]:
    """Return one symbol-ready entry while preserving comments and translations."""
    if entry.get("extractionState") == "stale":
        return entry

    localizations = copy.deepcopy(entry.get("localizations"))
    if not isinstance(localizations, dict):
        localizations = {}

    source_localization = localizations.get(source_language)
    if not isinstance(source_localization, dict):
        if entry.get("extractionState") == "manual":
            raise ValueError(f"{key}: manual entry has no {source_language} source value")
        source_localization = {
            "stringUnit": {
                "state": "translated",
                "value": key,
            }
        }
        localizations[source_language] = source_localization
    else:
        mark_string_units_translated(source_localization)

    prepared: dict[str, Any] = {}
    inserted_symbol_fields = False
    for field, value in entry.items():
        if field in {"extractionState", "localizations"}:
            if not inserted_symbol_fields:
                prepared["extractionState"] = "manual"
                prepared["localizations"] = localizations
                inserted_symbol_fields = True
            continue
        prepared[field] = value

    if not inserted_symbol_fields:
        prepared["extractionState"] = "manual"
        prepared["localizations"] = localizations

    return prepared


def prepare_catalog(catalog: dict[str, Any]) -> dict[str, Any]:
    """Return a catalog whose active entries generate localized Swift symbols."""
    source_language = catalog.get("sourceLanguage")
    strings = catalog.get("strings")
    if not isinstance(source_language, str) or not source_language:
        raise ValueError("catalog has no sourceLanguage")
    if not isinstance(strings, dict):
        raise ValueError("catalog has no strings dictionary")
    if any(not isinstance(entry, dict) for entry in strings.values()):
        raise ValueError("catalog contains a non-dictionary string entry")

    prepared = dict(catalog)
    prepared["strings"] = {
        key: prepare_entry(key, entry, source_language)
        for key, entry in strings.items()
    }
    return prepared


def symbol_issues(catalog: dict[str, Any]) -> list[str]:
    """Return active catalog entries that cannot generate expected Swift symbols."""
    source_language = catalog.get("sourceLanguage")
    strings = catalog.get("strings")
    if not isinstance(source_language, str) or not isinstance(strings, dict):
        return ["catalog structure is invalid"]

    issues: list[str] = []
    for key, entry in strings.items():
        if not isinstance(entry, dict):
            issues.append(f"{key}: entry is not a dictionary")
            continue
        if entry.get("extractionState") == "stale":
            continue
        if entry.get("extractionState") != "manual":
            issues.append(f"{key}: extractionState is not manual")
        source = entry.get("localizations", {}).get(source_language)
        if not isinstance(source, dict):
            issues.append(f"{key}: source localization {source_language} is missing")
    return issues


def render_json(value: Any, indentation: int = 0) -> str:
    """Render JSON with the spacing used by Xcode String Catalogs."""
    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = ["{"]
        items = list(value.items())
        for index, (key, child) in enumerate(items):
            rendered = render_json(child, indentation + 2).splitlines()
            prefix = " " * (indentation + 2) + json.dumps(key, ensure_ascii=False) + " : "
            lines.append(prefix + rendered[0])
            lines.extend(rendered[1:])
            if index < len(items) - 1:
                lines[-1] += ","
        lines.append(" " * indentation + "}")
        return "\n".join(lines)

    if isinstance(value, list):
        if not value:
            return "[]"
        lines = ["["]
        for index, child in enumerate(value):
            rendered = render_json(child, indentation + 2).splitlines()
            rendered[0] = " " * (indentation + 2) + rendered[0]
            lines.extend(rendered)
            if index < len(value) - 1:
                lines[-1] += ","
        lines.append(" " * indentation + "]")
        return "\n".join(lines)

    return json.dumps(value, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    """Prepare explicit catalogs in place or check whether preparation is needed."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalogs", nargs="+", type=Path, help="String Catalog files to prepare")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report entries that are not symbol-ready without modifying catalogs.",
    )
    arguments = parser.parse_args(argv)

    failed = False
    for path in arguments.catalogs:
        try:
            with path.open(encoding="utf-8") as catalog_file:
                catalog = json.load(catalog_file)
            prepared = prepare_catalog(catalog)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print(f"{path}: {error}", file=sys.stderr)
            failed = True
            continue

        if prepared == catalog:
            print(f"{path}: already symbol-ready.")
            continue
        if arguments.check:
            print(
                f"{path}: run this script without --check to prepare generated symbols.",
                file=sys.stderr,
            )
            failed = True
            continue

        path.write_text(render_json(prepared) + "\n", encoding="utf-8")
        print(f"{path}: prepared {len(prepared['strings'])} generated symbols.")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
