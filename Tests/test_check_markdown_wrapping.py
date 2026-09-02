"""Tests for the audit skill's Markdown wrapping checker."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


CHECKER_PATH = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "agent-guidelines-audit"
    / "scripts"
    / "check_markdown_wrapping.py"
)
SPEC = importlib.util.spec_from_file_location("check_markdown_wrapping", CHECKER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


class MarkdownWrappingTests(unittest.TestCase):
    """Verifies prose detection and verbatim-content exclusions."""

    def findings(self, contents: str) -> list[object]:
        """Return findings for a temporary Markdown fixture."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "Example.md"
            path.write_text(contents, encoding="utf-8")
            return CHECKER.findings_for(path)

    def test_reports_paragraph_list_and_blockquote_wrapping(self) -> None:
        """Reports every governed prose form that spans physical lines."""
        findings = self.findings(
            """# Example

This paragraph was split
across physical lines.

- This list item was split
  across physical lines too.

> This quotation was split
> across physical lines as well.
"""
        )

        self.assertEqual(
            [(finding.start, finding.end, finding.kind) for finding in findings],
            [
                (3, 4, "paragraph"),
                (6, 7, "list item"),
                (9, 10, "block quote (depth 1)"),
            ],
        )

    def test_accepts_single_line_prose_and_markdown_structure(self) -> None:
        """Does not report separate items, tables, fences, or diagrams."""
        findings = self.findings(
            """---
title: Example
---

# Example

This paragraph occupies one physical line even though it is intentionally long.

- First list item.
- Second list item.

| Role | Folder |
|---|---|
| App | `App/` |

```text
┌─────┐
│ App │
└─────┘
```

<p align="center">
  <a href="https://example.com">Badge</a>
</p>

> - First quoted item.
> - Second quoted item.

- Parent item.
  - Nested item.
"""
        )

        self.assertEqual(findings, [])

    def test_reports_headroom_style_wrapping(self) -> None:
        """Catches the consumer pattern that motivated the audit."""
        findings = self.findings(
            """# Logging

The application uses the shared logging package
for application-owned diagnostics. The application owns orchestration,
transport, protocol, refresh, and authentication logs.

## Identity

All production messages go through the logging gateway, which applies the subsystem,
category, and emoji consistently.
"""
        )

        self.assertEqual(
            [(finding.start, finding.end) for finding in findings],
            [(3, 5), (9, 10)],
        )


if __name__ == "__main__":
    unittest.main()
