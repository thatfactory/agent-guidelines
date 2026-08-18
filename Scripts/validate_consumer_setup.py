#!/usr/bin/env python3
"""Validate a consumer repository's checked-in agent-guidelines integration."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


GUIDELINES_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_BEGIN = "<!-- BEGIN THATFACTORY CODE REVIEW CONTRACT v1 -->"
CONTRACT_END = "<!-- END THATFACTORY CODE REVIEW CONTRACT v1 -->"
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
GENERATED_ATTRIBUTE = re.compile(
    r"^\s*AgentGuidelines/\*\*\s+linguist-generated\s*$",
    re.MULTILINE,
)


def read_text(path: Path, errors: list[str], label: str) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        errors.append(f"{label}: cannot read {path}: {error}")
        return None


def extract_contract(contents: str, errors: list[str], label: str) -> str | None:
    if contents.count(CONTRACT_BEGIN) != 1 or contents.count(CONTRACT_END) != 1:
        errors.append(
            f"{label}: expected exactly one {CONTRACT_BEGIN!r} and {CONTRACT_END!r}"
        )
        return None

    start = contents.index(CONTRACT_BEGIN)
    end = contents.index(CONTRACT_END, start) + len(CONTRACT_END)
    return contents[start:end].strip()


def validate_symlink(path: Path, expected: Path, errors: list[str], label: str) -> None:
    if not path.is_symlink():
        errors.append(f"{label}: {path} must be a symlink to {expected}")
        return

    if not path.exists():
        errors.append(f"{label}: {path} is a broken symlink")
        return

    if path.resolve() != expected.resolve():
        errors.append(f"{label}: {path} resolves to {path.resolve()}, expected {expected.resolve()}")


def validate_agent_links(
    agents_path: Path,
    contents: str,
    errors: list[str],
) -> None:
    for raw_target in MARKDOWN_LINK.findall(contents):
        target = raw_target.strip().strip("<>").split("#", maxsplit=1)[0]
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue

        resolved = (agents_path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"AGENTS.md: missing local link target {raw_target!r}")


def validate_consumer_setup(
    errors: list[str],
    consumer_root: Path,
    guidelines_root: Path = GUIDELINES_ROOT,
    require_swift_format_links: bool = False,
) -> None:
    consumer_root = consumer_root.resolve()
    guidelines_root = guidelines_root.resolve()
    subtree = consumer_root / "AgentGuidelines"

    if not subtree.exists():
        errors.append(f"consumer root: missing {subtree}")
    elif subtree.resolve() != guidelines_root:
        errors.append(
            f"consumer root: {subtree} resolves to {subtree.resolve()}, "
            f"expected the active guidelines at {guidelines_root}"
        )

    version_path = guidelines_root / "VERSION"
    version = read_text(version_path, errors, "AgentGuidelines/VERSION")
    if version is not None and not version.strip():
        errors.append("AgentGuidelines/VERSION: version is empty")

    template_path = guidelines_root / "Templates" / "AGENTS.md"
    agents_path = consumer_root / "AGENTS.md"
    template = read_text(template_path, errors, "AgentGuidelines template")
    agents = read_text(agents_path, errors, "consumer AGENTS.md")

    if template is not None and agents is not None:
        expected_contract = extract_contract(template, errors, "AgentGuidelines template")
        actual_contract = extract_contract(agents, errors, "consumer AGENTS.md")
        if (
            expected_contract is not None
            and actual_contract is not None
            and actual_contract != expected_contract
        ):
            errors.append(
                "consumer AGENTS.md: code-review contract does not match "
                "AgentGuidelines/Templates/AGENTS.md"
            )

        required_scope_values = (
            "## Codex review scope",
            "AgentGuidelines/**",
            "exact tagged-tree provenance",
            ".gitattributes",
        )
        for value in required_scope_values:
            if value not in agents:
                errors.append(f"consumer AGENTS.md: missing Codex review scope value {value!r}")

        validate_agent_links(agents_path, agents, errors)

    attributes_path = consumer_root / ".gitattributes"
    attributes = read_text(attributes_path, errors, "consumer .gitattributes")
    if attributes is not None and not GENERATED_ATTRIBUTE.search(attributes):
        errors.append(
            "consumer .gitattributes: missing exact "
            "'AgentGuidelines/** linguist-generated' rule"
        )

    expected_skill = guidelines_root / ".agents" / "skills" / "agent-guidelines-audit"
    consumer_skill = consumer_root / ".agents" / "skills" / "agent-guidelines-audit"
    validate_symlink(consumer_skill, expected_skill, errors, "consumer audit skill")

    formatter_links = {
        ".swift-format": guidelines_root / "Configurations" / "Swift" / ".swift-format",
        ".editorconfig": guidelines_root / "Configurations" / "Swift" / ".editorconfig",
    }
    for name, expected in formatter_links.items():
        path = consumer_root / name
        if require_swift_format_links or path.is_symlink():
            validate_symlink(path, expected, errors, f"consumer {name}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--consumer-root",
        type=Path,
        help="Consumer repository root. Defaults to the parent of an AgentGuidelines subtree.",
    )
    parser.add_argument(
        "--require-swift-format-links",
        action="store_true",
        help="Require .swift-format and .editorconfig symlinks to the shared configurations.",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    consumer_root = arguments.consumer_root
    if consumer_root is None:
        if GUIDELINES_ROOT.name != "AgentGuidelines":
            print(
                "Consumer setup validation failed:\n"
                "- --consumer-root is required when this checkout is not installed "
                "as an AgentGuidelines subtree"
            )
            return 1
        consumer_root = GUIDELINES_ROOT.parent

    errors: list[str] = []
    validate_consumer_setup(
        errors,
        consumer_root,
        require_swift_format_links=arguments.require_swift_format_links,
    )
    if errors:
        print("Consumer setup validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    version = (GUIDELINES_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    print(f"Validated consumer setup for agent-guidelines {version}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
