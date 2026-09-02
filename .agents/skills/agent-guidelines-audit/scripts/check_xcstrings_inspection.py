#!/usr/bin/env python3
"""Require recorded Xcode editor inspection for every changed String Catalog."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath


def run(command: list[str], repository_root: Path) -> str:
    """Run a command in the repository and return its standard output."""
    result = subprocess.run(
        command,
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "command failed"
        raise RuntimeError(f"{' '.join(command)}: {detail}")
    return result.stdout


def repository_root(repository: Path) -> Path:
    """Return the Git repository root containing the requested path."""
    root = run(["git", "rev-parse", "--show-toplevel"], repository.resolve()).strip()
    return Path(root).resolve()


def nul_separated_paths(output: str) -> set[PurePosixPath]:
    """Parse NUL-separated Git paths and retain existing String Catalogs."""
    return {
        PurePosixPath(value)
        for value in output.split("\0")
        if value and PurePosixPath(value).suffix == ".xcstrings"
    }


def changed_catalogs(root: Path, base_ref: str) -> set[PurePosixPath]:
    """Return added, copied, modified, renamed, and untracked String Catalogs."""
    run(["git", "rev-parse", "--verify", f"{base_ref}^{{commit}}"], root)
    tracked = run(
        ["git", "diff", "--name-only", "-z", "--diff-filter=ACMR", base_ref, "--"],
        root,
    )
    untracked = run(["git", "ls-files", "--others", "--exclude-standard", "-z"], root)
    return nul_separated_paths(tracked) | nul_separated_paths(untracked)


def normalized_inspections(values: list[str]) -> set[PurePosixPath]:
    """Normalize repository-relative catalog paths supplied as inspection evidence."""
    inspections: set[PurePosixPath] = set()
    for value in values:
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or path.suffix != ".xcstrings":
            raise ValueError(
                "--inspected-catalog values must be repository-relative .xcstrings paths"
            )
        inspections.add(path)
    return inspections


def inspection_coverage_errors(
    changed: set[PurePosixPath], inspected: set[PurePosixPath]
) -> list[str]:
    """Return fail-closed coverage errors for catalog-editor inspection evidence."""
    errors = [
        f"missing Xcode catalog-editor inspection evidence: {path.as_posix()}"
        for path in sorted(changed - inspected)
    ]
    errors.extend(
        f"inspection evidence does not match a changed String Catalog: {path.as_posix()}"
        for path in sorted(inspected - changed)
    )
    return errors


def selected_xcode_version(root: Path) -> str:
    """Return the selected Xcode version and build used for the inspection record."""
    return run(["xcodebuild", "-version"], root).strip()


def write_evidence(
    output: Path,
    root: Path,
    base_ref: str,
    xcode_version: str,
    catalogs: set[PurePosixPath],
) -> None:
    """Write structured, non-repository evidence for the completed editor inspection."""
    resolved_output = output.expanduser().resolve()
    if resolved_output == root or root in resolved_output.parents:
        raise ValueError("--evidence-output must be outside the repository")
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    evidence = {
        "schemaVersion": 1,
        "recordedAt": datetime.now(UTC).isoformat(),
        "baseRef": base_ref,
        "xcodeVersion": xcode_version,
        "catalogs": [
            {
                "path": path.as_posix(),
                "catalogEditorErrors": 0,
                "catalogEditorWarnings": 0,
            }
            for path in sorted(catalogs)
        ],
    }
    resolved_output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Fail unless every changed .xcstrings file has an explicit zero-error, "
            "zero-warning Xcode catalog-editor inspection record."
        )
    )
    parser.add_argument(
        "--repository",
        type=Path,
        default=Path.cwd(),
        help="Path inside the Git repository; defaults to the current directory.",
    )
    parser.add_argument(
        "--base-ref",
        required=True,
        help="Git base commit or ref against which changed catalogs are discovered.",
    )
    parser.add_argument(
        "--inspected-catalog",
        action="append",
        default=[],
        help=(
            "Repository-relative catalog path opened in Xcode and observed with zero "
            "editor errors and zero editor warnings; repeat for every changed catalog."
        ),
    )
    parser.add_argument(
        "--evidence-output",
        type=Path,
        help="JSON evidence destination outside the repository; required when catalogs changed.",
    )
    return parser.parse_args()


def main() -> int:
    """Validate inspection coverage and write the structured evidence record."""
    arguments = parse_arguments()
    try:
        root = repository_root(arguments.repository)
        changed = changed_catalogs(root, arguments.base_ref)
        inspected = normalized_inspections(arguments.inspected_catalog)
        errors = inspection_coverage_errors(changed, inspected)
        if changed and arguments.evidence_output is None:
            errors.append("--evidence-output is required when String Catalogs changed")
        if errors:
            for error in errors:
                print(f"String Catalog inspection audit failed: {error}", file=sys.stderr)
            return 1
        if not changed:
            print(
                f"No changed String Catalogs relative to {arguments.base_ref}; "
                "Xcode catalog-editor inspection evidence is not required."
            )
            return 0

        xcode_version = selected_xcode_version(root)
        write_evidence(
            arguments.evidence_output,
            root,
            arguments.base_ref,
            xcode_version,
            changed,
        )
    except (OSError, RuntimeError, ValueError) as error:
        print(f"String Catalog inspection audit failed: {error}", file=sys.stderr)
        return 2

    print(
        f"Recorded zero Xcode catalog-editor errors and warnings for "
        f"{len(changed)} changed String Catalog(s) at {arguments.evidence_output}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
