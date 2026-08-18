#!/usr/bin/env python3
"""Validate the structure and public safety of the guideline repository."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
VERSION = ROOT / "VERSION"
CHANGELOG = ROOT / "CHANGELOG.md"
SWIFT_FORMAT_CONFIGURATION = ROOT / "Configurations" / "Swift" / ".swift-format"
EDITOR_CONFIGURATION = ROOT / "Configurations" / "Swift" / ".editorconfig"
SWIFT_FORMAT_SCRIPT = ROOT / "Scripts" / "swift_format.sh"
SWIFT_FORMAT_GUIDELINE = ROOT / "Guidelines" / "Swift" / "SwiftFormat.md"
CONSUMER_SETUP_SCRIPT = ROOT / "Scripts" / "validate_consumer_setup.py"
AUDIT_SKILL = ROOT / ".agents" / "skills" / "agent-guidelines-audit" / "SKILL.md"
DEVELOPMENT_GUIDELINE = ROOT / "Guidelines" / "Development.md"
AGENTS_TEMPLATE = ROOT / "Templates" / "AGENTS.md"
EXPECTED_SWIFT_FORMAT_RULES = {
    "AllPublicDeclarationsHaveDocumentation": False,
    "AlwaysUseLiteralForEmptyCollectionInit": True,
    "AlwaysUseLowerCamelCase": True,
    "AmbiguousTrailingClosureOverload": True,
    "AvoidRetroactiveConformances": True,
    "BeginDocumentationCommentWithOneLineSummary": False,
    "DoNotUseSemicolons": True,
    "DontRepeatTypeInStaticProperties": True,
    "FileScopedDeclarationPrivacy": True,
    "FullyIndirectEnum": True,
    "GroupNumericLiterals": True,
    "IdentifiersMustBeASCII": True,
    "NeverForceUnwrap": False,
    "NeverUseForceTry": True,
    "NeverUseImplicitlyUnwrappedOptionals": False,
    "NoAccessLevelOnExtensionDeclaration": True,
    "NoAssignmentInExpressions": True,
    "NoBlockComments": True,
    "NoCasesWithOnlyFallthrough": True,
    "NoEmptyLinesOpeningClosingBraces": True,
    "NoEmptyTrailingClosureParentheses": True,
    "NoLabelsInCasePatterns": True,
    "NoLeadingUnderscores": False,
    "NoParensAroundConditions": True,
    "NoPlaygroundLiterals": True,
    "NoVoidReturnOnFunctionSignature": True,
    "OmitExplicitReturns": False,
    "OneCasePerLine": True,
    "OneVariableDeclarationPerLine": True,
    "OnlyOneTrailingClosureArgument": True,
    "OrderedImports": True,
    "ReplaceForEachWithForLoop": True,
    "ReturnVoidInsteadOfEmptyTuple": True,
    "TypeNamesShouldBeCapitalized": True,
    "UseEarlyExits": False,
    "UseExplicitNilCheckInConditions": True,
    "UseLetInEveryBoundCaseVariable": True,
    "UseShorthandTypeNames": True,
    "UseSingleLinePropertyGetter": True,
    "UseSynthesizedInitializer": True,
    "UseTripleSlashForDocumentationComments": True,
    "UseWhereClausesInForLoops": True,
    "ValidateDocumentationComments": True,
}

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
    suffixes = {".md", ".py", ".swift", ".yml", ".yaml", ".txt"}
    files = [path for path in ROOT.rglob("*") if path.is_file() and path.suffix in suffixes]
    files.extend(path for path in (ROOT / "VERSION", ROOT / "LICENSE") if path.is_file())
    files.extend(
        path
        for path in (SWIFT_FORMAT_CONFIGURATION, EDITOR_CONFIGURATION)
        if path.is_file()
    )
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
        "AgentGuidelines/** linguist-generated": "generated subtree attribute",
        "AgentGuidelines/Configurations/Swift/.swift-format": "swift-format symlink command",
        "AgentGuidelines/Configurations/Swift/.editorconfig": "EditorConfig symlink command",
        ".agents/skills/agent-guidelines-audit": "completion-audit skill setup",
        "validate_consumer_setup.py": "consumer setup validation command",
        "--require-swift-format": "explicit Swift-format adoption validation",
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


def validate_swift_format_configuration(errors: list[str]) -> None:
    try:
        configuration = json.loads(SWIFT_FORMAT_CONFIGURATION.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{SWIFT_FORMAT_CONFIGURATION.relative_to(ROOT)}: invalid JSON: {error}")
        return

    expected_values = {
        "indentation": {"spaces": 4},
        "indentSwitchCaseLabels": False,
        "lineLength": 120,
        "tabWidth": 4,
        "version": 1,
    }
    for key, expected in expected_values.items():
        actual = configuration.get(key)
        if actual != expected:
            errors.append(
                f"{SWIFT_FORMAT_CONFIGURATION.relative_to(ROOT)}: "
                f"{key} must be {expected!r}, found {actual!r}"
            )

    include_conditional_imports = configuration.get("orderedImports", {}).get(
        "includeConditionalImports"
    )
    if include_conditional_imports is not True:
        errors.append(
            f"{SWIFT_FORMAT_CONFIGURATION.relative_to(ROOT)}: "
            "orderedImports.includeConditionalImports must be True, "
            f"found {include_conditional_imports!r}"
        )

    rules = configuration.get("rules")
    if not isinstance(rules, dict) or not rules:
        errors.append(
            f"{SWIFT_FORMAT_CONFIGURATION.relative_to(ROOT)}: "
            "rules must be an exhaustive non-empty object"
        )
    else:
        missing = sorted(set(EXPECTED_SWIFT_FORMAT_RULES) - set(rules))
        unexpected = sorted(set(rules) - set(EXPECTED_SWIFT_FORMAT_RULES))
        if missing or unexpected:
            errors.append(
                f"{SWIFT_FORMAT_CONFIGURATION.relative_to(ROOT)}: "
                f"rule map mismatch; missing={missing!r}, unexpected={unexpected!r}"
            )
        for rule in sorted(set(rules) & set(EXPECTED_SWIFT_FORMAT_RULES)):
            expected = EXPECTED_SWIFT_FORMAT_RULES[rule]
            actual = rules[rule]
            if actual != expected:
                errors.append(
                    f"{SWIFT_FORMAT_CONFIGURATION.relative_to(ROOT)}: "
                    f"{rule} must be {expected!r}, found {actual!r}"
                )


def validate_editor_configuration(errors: list[str]) -> None:
    try:
        contents = EDITOR_CONFIGURATION.read_text(encoding="utf-8")
    except OSError as error:
        errors.append(
            f"{EDITOR_CONFIGURATION.relative_to(ROOT)}: cannot read configuration: {error}"
        )
        return
    required = {
        "root = true",
        "[*.swift]",
        "indent_style = space",
        "indent_size = 4",
        "tab_width = 4",
        "max_line_length = 120",
        "end_of_line = lf",
        "insert_final_newline = true",
        "trim_trailing_whitespace = true",
    }
    for value in sorted(required):
        if value not in contents:
            errors.append(
                f"{EDITOR_CONFIGURATION.relative_to(ROOT)}: missing {value!r}"
            )


def validate_swift_format_script(errors: list[str]) -> None:
    if not SWIFT_FORMAT_SCRIPT.is_file():
        errors.append(f"{SWIFT_FORMAT_SCRIPT.relative_to(ROOT)}: missing script")
    elif not os.access(SWIFT_FORMAT_SCRIPT, os.X_OK):
        errors.append(f"{SWIFT_FORMAT_SCRIPT.relative_to(ROOT)}: script is not executable")


def validate_swift_format_guideline(errors: list[str]) -> None:
    contents = SWIFT_FORMAT_GUIDELINE.read_text(encoding="utf-8")
    required = {
        "## Swift package integration": "Swift package workflow",
        "format-and-lint \\": "local package formatting command",
        "Package.swift": "package manifest formatting scope",
        "## CI integration": "CI workflow",
        "lint-strict \\": "strict CI command",
        "Never run `format` or `format-and-lint` in CI": "non-mutating CI rule",
    }
    for value, description in required.items():
        if value not in contents:
            errors.append(
                f"{SWIFT_FORMAT_GUIDELINE.relative_to(ROOT)}: "
                f"missing {description}: {value!r}"
            )


def validate_consumer_setup_script(errors: list[str]) -> None:
    if not CONSUMER_SETUP_SCRIPT.is_file():
        errors.append(f"{CONSUMER_SETUP_SCRIPT.relative_to(ROOT)}: missing script")
    elif not os.access(CONSUMER_SETUP_SCRIPT, os.X_OK):
        errors.append(
            f"{CONSUMER_SETUP_SCRIPT.relative_to(ROOT)}: script is not executable"
        )


def validate_audit_skill(errors: list[str]) -> None:
    if not AUDIT_SKILL.is_file():
        errors.append(f"{AUDIT_SKILL.relative_to(ROOT)}: missing audit skill")
        return

    skill = AUDIT_SKILL.read_text(encoding="utf-8")
    required_skill_values = {
        "name: agent-guidelines-audit": "skill name",
        "before claiming completion": "completion trigger",
        "git diff --check": "diff validation",
        "validate_consumer_setup.py": "consumer integration validation",
        "format-and-lint": "local Swift-format audit",
        "lint-strict": "strict Swift-format CI audit",
        "no unresolved P0/P1 blocker remains": "Codex review stopping rule",
    }
    for value, description in required_skill_values.items():
        if value not in skill:
            errors.append(
                f"{AUDIT_SKILL.relative_to(ROOT)}: missing {description}: {value!r}"
            )

    development = DEVELOPMENT_GUIDELINE.read_text(encoding="utf-8")
    if "$agent-guidelines-audit" not in development:
        errors.append(
            f"{DEVELOPMENT_GUIDELINE.relative_to(ROOT)}: "
            "missing mandatory $agent-guidelines-audit invocation"
        )

    agents_template = AGENTS_TEMPLATE.read_text(encoding="utf-8")
    if "AgentGuidelines/Guidelines/Development.md" not in agents_template:
        errors.append(
            f"{AGENTS_TEMPLATE.relative_to(ROOT)}: missing Development.md pointer"
        )
    if "## Stack" not in agents_template:
        errors.append(f"{AGENTS_TEMPLATE.relative_to(ROOT)}: missing Stack section")


def main() -> int:
    errors: list[str] = []
    validate_links(errors)
    validate_catalog(errors)
    validate_version(errors)
    validate_readme_contract(errors)
    validate_public_content(errors)
    validate_swift_format_configuration(errors)
    validate_editor_configuration(errors)
    validate_swift_format_script(errors)
    validate_swift_format_guideline(errors)
    validate_consumer_setup_script(errors)
    validate_audit_skill(errors)

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
