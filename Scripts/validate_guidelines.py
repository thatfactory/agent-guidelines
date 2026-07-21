#!/usr/bin/env python3
"""Validate the structure and public safety of the guideline repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
VERSION = ROOT / "VERSION"
CHANGELOG = ROOT / "CHANGELOG.md"

MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)\."
    r"(0|[1-9][0-9]*)"
    r"(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
FORBIDDEN = {
    "/" + "Users" + "/": "personal absolute path",
    "file" + "://": "local file URL",
    "mobile-ios-" + "chauffeur": "work-repository identifier",
    "black" + "lane": "work-repository identifier",
}


def text_files() -> list[Path]:
    suffixes = {".md", ".py", ".yml", ".yaml", ".txt"}
    files = [path for path in ROOT.rglob("*") if path.is_file() and path.suffix in suffixes]
    files.extend(path for path in (ROOT / "VERSION", ROOT / "LICENSE") if path.is_file())
    return sorted(set(files))


def resolve_link(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().strip("<>").split("#", maxsplit=1)[0]
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None

    parts = PurePosixPath(target).parts
    if "AgentGuidelines" in parts:
        index = parts.index("AgentGuidelines")
        return ROOT.joinpath(*parts[index + 1 :]).resolve()

    return (source.parent / target).resolve()


def validate_links(errors: list[str]) -> None:
    for source in sorted(ROOT.rglob("*.md")):
        for raw_target in MARKDOWN_LINK.findall(source.read_text(encoding="utf-8")):
            resolved = resolve_link(source, raw_target)
            if resolved is not None and not resolved.exists():
                relative_source = source.relative_to(ROOT)
                errors.append(f"{relative_source}: missing link target {raw_target!r}")


def validate_catalog(errors: list[str]) -> None:
    readme = README.read_text(encoding="utf-8")
    for guide in sorted((ROOT / "Guidelines").rglob("*.md")):
        relative = guide.relative_to(ROOT).as_posix()
        if f"]({relative})" not in readme:
            errors.append(f"README.md: guideline is not cataloged: {relative}")


def validate_version(errors: list[str]) -> None:
    version = VERSION.read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        errors.append(f"VERSION: invalid semantic version {version!r}")

    changelog = CHANGELOG.read_text(encoding="utf-8")
    if f"## [{version}]" not in changelog:
        errors.append(f"CHANGELOG.md: missing release heading for {version}")


def validate_readme_contract(errors: list[str]) -> None:
    readme = README.read_text(encoding="utf-8")
    required = {
        'alt="Xcode"': "Xcode badge alt text",
        "thatfactory/agent-guidelines/actions/workflows/ci.yml": "CI badge repository",
        "--prefix=AgentGuidelines": "subtree destination",
        "https://github.com/thatfactory/agent-guidelines.git": "subtree remote",
        "git subtree add": "subtree installation command",
        "git subtree pull": "subtree update command",
    }
    for value, description in required.items():
        if value not in readme:
            errors.append(f"README.md: missing {description}: {value!r}")


def validate_public_content(errors: list[str]) -> None:
    for path in text_files():
        contents = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for forbidden, description in FORBIDDEN.items():
            if forbidden.lower() in contents.lower():
                errors.append(f"{relative}: contains {description}: {forbidden!r}")


def main() -> int:
    errors: list[str] = []
    validate_links(errors)
    validate_catalog(errors)
    validate_version(errors)
    validate_readme_contract(errors)
    validate_public_content(errors)

    if errors:
        print("Guideline validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    guide_count = len(list((ROOT / "Guidelines").rglob("*.md")))
    print(f"Validated {guide_count} guidelines for version {VERSION.read_text().strip()}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
