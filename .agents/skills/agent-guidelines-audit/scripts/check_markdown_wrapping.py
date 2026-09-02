#!/usr/bin/env python3
"""Report Markdown prose blocks that span multiple physical lines."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING = re.compile(r"^\s{0,3}#{1,6}(?:\s|$)")
LIST_ITEM = re.compile(r"^(\s{0,3})(?:[-+*]|\d+[.)])\s+(.*)$")
LINK_DEFINITION = re.compile(r"^\s{0,3}\[[^]]+\]:\s*\S+")
THEMATIC_BREAK = re.compile(r"^\s{0,3}(?:(?:\*\s*){3,}|(?:-\s*){3,}|(?:_\s*){3,})$")
SETEXT_UNDERLINE = re.compile(r"^\s{0,3}(?:=+|-+)\s*$")
TABLE_DELIMITER = re.compile(r"^\s*\|?(?:\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?\s*$")


@dataclass(frozen=True)
class Finding:
    """A prose block that should occupy one physical line."""

    path: Path
    start: int
    end: int
    kind: str


@dataclass
class Block:
    """A candidate prose block being assembled."""

    kind: str
    start: int
    end: int


def is_table_row(line: str) -> bool:
    """Return whether a line has the shape of a Markdown table row."""
    stripped = line.strip()
    return TABLE_DELIMITER.fullmatch(stripped) is not None or (
        stripped.startswith("|") and stripped.endswith("|")
    )


def is_verbatim_or_structure(line: str) -> bool:
    """Return whether a line should terminate prose-block detection."""
    stripped = line.strip()
    return (
        not stripped
        or HEADING.match(line) is not None
        or THEMATIC_BREAK.fullmatch(line) is not None
        or SETEXT_UNDERLINE.fullmatch(line) is not None
        or LINK_DEFINITION.match(line) is not None
        or LIST_ITEM.match(line) is not None
        or is_table_row(line)
        or line.startswith("    ")
        or stripped.startswith("<")
    )


def markdown_files(paths: list[Path]) -> list[Path]:
    """Expand file and directory arguments into unique Markdown files."""
    files: set[Path] = set()
    for path in paths:
        if path.is_dir():
            files.update(candidate for candidate in path.rglob("*.md") if candidate.is_file())
        elif path.is_file() and path.suffix.lower() == ".md":
            files.add(path)
        elif not path.exists():
            raise FileNotFoundError(path)
    return sorted(files)


def findings_for(path: Path) -> list[Finding]:
    """Find prose blocks that span multiple physical lines in one Markdown file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    findings: list[Finding] = []
    block: Block | None = None
    fence_marker: str | None = None
    in_comment = False
    in_frontmatter = bool(lines and lines[0].strip() == "---")

    def finish_block() -> None:
        nonlocal block
        if block is not None and block.end > block.start:
            findings.append(Finding(path, block.start, block.end, block.kind))
        block = None

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()

        if in_frontmatter:
            if line_number > 1 and stripped == "---":
                in_frontmatter = False
            continue

        fence = FENCE.match(line)
        if fence is not None:
            marker = fence.group(1)
            if fence_marker is None:
                finish_block()
                fence_marker = marker[0]
            elif marker[0] == fence_marker:
                fence_marker = None
            continue
        if fence_marker is not None:
            continue

        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line:
            finish_block()
            if "-->" not in line.split("<!--", maxsplit=1)[1]:
                in_comment = True
            continue

        quote_depth = 0
        quote_content = line
        while re.match(r"^\s{0,3}>\s?", quote_content):
            quote_content = re.sub(r"^\s{0,3}>\s?", "", quote_content, count=1)
            quote_depth += 1
        if quote_depth:
            if is_verbatim_or_structure(quote_content):
                finish_block()
                continue
            kind = f"block quote (depth {quote_depth})"
            if block is not None and block.kind == kind:
                block.end = line_number
            else:
                finish_block()
                block = Block(kind, line_number, line_number)
            continue

        list_item = LIST_ITEM.match(line)
        if list_item is not None:
            finish_block()
            content = list_item.group(2)
            if content and not is_verbatim_or_structure(content):
                block = Block("list item", line_number, line_number)
            continue

        if block is not None and block.kind == "list item" and line.startswith(("  ", "\t")):
            if is_verbatim_or_structure(line.lstrip()):
                finish_block()
            else:
                block.end = line_number
            continue

        if is_verbatim_or_structure(line):
            finish_block()
            continue

        if block is not None and block.kind == "paragraph":
            block.end = line_number
        else:
            finish_block()
            block = Block("paragraph", line_number, line_number)

    finish_block()
    return findings


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Report Markdown prose that is hard-wrapped across physical lines."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown files or folders")
    return parser.parse_args()


def main() -> int:
    """Run the wrapping audit and return a lint-style status code."""
    arguments = parse_arguments()
    try:
        files = markdown_files(arguments.paths)
    except FileNotFoundError as error:
        print(f"Markdown wrapping audit failed: path does not exist: {error}", file=sys.stderr)
        return 2

    findings = [finding for path in files for finding in findings_for(path)]
    for finding in findings:
        print(
            f"{finding.path}:{finding.start}: {finding.kind} spans physical lines "
            f"{finding.start}-{finding.end}; keep its prose on one line"
        )

    if findings:
        print(f"Found {len(findings)} hard-wrapped Markdown prose block(s).", file=sys.stderr)
        return 1

    print(f"Checked {len(files)} Markdown file(s); no hard-wrapped prose found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
