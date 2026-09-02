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
LOCALIZATION_GUIDELINE = ROOT / "Guidelines" / "Swift" / "Localization.md"
XCODE_PROJECT_SETTINGS_GUIDELINE = ROOT / "Guidelines" / "Xcode" / "ProjectSettings.md"
LOCALIZATION_PREPARATION_SCRIPT = ROOT / "Scripts" / "prepare_localizable_symbols.py"
LOCALIZATION_VALIDATION_SCRIPT = ROOT / "Scripts" / "validate_string_catalogs.py"
CONSUMER_SETUP_SCRIPT = ROOT / "Scripts" / "validate_consumer_setup.py"
AUDIT_SKILL = ROOT / ".agents" / "skills" / "agent-guidelines-audit" / "SKILL.md"
MARKDOWN_WRAPPING_SCRIPT = (
    ROOT
    / ".agents"
    / "skills"
    / "agent-guidelines-audit"
    / "scripts"
    / "check_markdown_wrapping.py"
)
DEVELOPMENT_GUIDELINE = ROOT / "Guidelines" / "Development.md"
DOCUMENTATION_GUIDELINE = ROOT / "Guidelines" / "Documentation.md"
PACKAGES_GUIDELINE = ROOT / "Guidelines" / "Packages.md"
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
UPCOMING_FEATURE_SETTINGS = (
    "SWIFT_UPCOMING_FEATURE_CONCISE_MAGIC_FILE",
    "SWIFT_UPCOMING_FEATURE_DEPRECATE_APPLICATION_MAIN",
    "SWIFT_UPCOMING_FEATURE_DISABLE_OUTWARD_ACTOR_ISOLATION",
    "SWIFT_UPCOMING_FEATURE_DYNAMIC_ACTOR_ISOLATION",
    "SWIFT_UPCOMING_FEATURE_EXISTENTIAL_ANY",
    "SWIFT_UPCOMING_FEATURE_FORWARD_TRAILING_CLOSURES",
    "SWIFT_UPCOMING_FEATURE_GLOBAL_ACTOR_ISOLATED_TYPES_USABILITY",
    "SWIFT_UPCOMING_FEATURE_GLOBAL_CONCURRENCY",
    "SWIFT_UPCOMING_FEATURE_IMPLICIT_OPEN_EXISTENTIALS",
    "SWIFT_UPCOMING_FEATURE_IMPORT_OBJC_FORWARD_DECLS",
    "SWIFT_UPCOMING_FEATURE_INFER_ISOLATED_CONFORMANCES",
    "SWIFT_UPCOMING_FEATURE_INFER_SENDABLE_FROM_CAPTURES",
    "SWIFT_UPCOMING_FEATURE_INTERNAL_IMPORTS_BY_DEFAULT",
    "SWIFT_UPCOMING_FEATURE_ISOLATED_DEFAULT_VALUES",
    "SWIFT_UPCOMING_FEATURE_MEMBER_IMPORT_VISIBILITY",
    "SWIFT_UPCOMING_FEATURE_NONFROZEN_ENUM_EXHAUSTIVITY",
    "SWIFT_UPCOMING_FEATURE_NONISOLATED_NONSENDING_BY_DEFAULT",
    "SWIFT_UPCOMING_FEATURE_REGION_BASED_ISOLATION",
)


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
        'alt="Xcode MCP"': "Xcode MCP badge alt text",
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
        "documentation-maintenance contract": "documentation contract synchronization",
        "external-dependency contract": "external dependency contract synchronization",
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


def validate_documentation_guideline(errors: list[str]) -> None:
    contents = DOCUMENTATION_GUIDELINE.read_text(encoding="utf-8")
    required = {
        "Documentation is part of implementation": "implementation-time documentation rule",
        "Regardless of change size": "existing-document staleness rule",
        "inaccurate, incomplete, misleading, or obsolete": "stale documentation criteria",
        "A small change that leaves durable knowledge and existing documentation accurate": (
            "minor-change documentation churn guardrail"
        ),
    }
    for value, description in required.items():
        if value not in contents:
            errors.append(
                f"{DOCUMENTATION_GUIDELINE.relative_to(ROOT)}: "
                f"missing {description}: {value!r}"
            )


def validate_localization_guideline(errors: list[str]) -> None:
    contents = LOCALIZATION_GUIDELINE.read_text(encoding="utf-8")
    required = {
        "using-generated-localizable-symbols-in-your-code": "Apple generated-symbol reference",
        "localizing-your-app-using-agents": "Apple agent-localization reference",
        "Xcode-generated `LocalizedStringResource` symbols": "generated-symbol default",
        "prepare_localizable_symbols.py": "shared symbol-preparation workflow",
        "validate_string_catalogs.py": "shared catalog-validation workflow",
        "stale extracted entry": "stale-entry policy",
        "marked `new` or `needs_review`": "translation-state policy",
        "placeholder positions, semantic names, and conversion types": (
            "format-signature policy"
        ),
        "product voice, terminology": "consumer-specific translation boundary",
        "small repository-owned wrapper": "consumer configuration boundary",
    }
    for value, description in required.items():
        if value not in contents:
            errors.append(
                f"{LOCALIZATION_GUIDELINE.relative_to(ROOT)}: "
                f"missing {description}: {value!r}"
            )


def validate_localization_scripts(errors: list[str]) -> None:
    scripts = {
        LOCALIZATION_PREPARATION_SCRIPT: (
            "Prepare String Catalog entries for generated Swift symbols",
            "symbol_issues",
            "--check",
        ),
        LOCALIZATION_VALIDATION_SCRIPT: (
            "Validate String Catalogs and generated-symbol Swift source usage",
            "--catalog-directory",
            "--source-directory",
            "--required-language",
            "format_signature_issues",
            "translation_state_issues",
            "literal_localization_references",
        ),
    }
    for script, required_values in scripts.items():
        if not script.is_file():
            errors.append(f"{script.relative_to(ROOT)}: missing localization script")
            continue
        if not os.access(script, os.X_OK):
            errors.append(f"{script.relative_to(ROOT)}: localization script is not executable")
        contents = script.read_text(encoding="utf-8")
        if "Headroom" in contents:
            errors.append(f"{script.relative_to(ROOT)}: contains consumer-specific logic")
        for value in required_values:
            if value not in contents:
                errors.append(
                    f"{script.relative_to(ROOT)}: missing localization behavior {value!r}"
                )


def validate_xcode_project_settings_guideline(errors: list[str]) -> None:
    contents = XCODE_PROJECT_SETTINGS_GUIDELINE.read_text(encoding="utf-8")
    required = {
        "https://developer.apple.com/documentation/xcode/build-settings-reference": (
            "official Apple build-settings reference"
        ),
        "GCC_TREAT_WARNINGS_AS_ERRORS": "C and Objective-C warning policy",
        "MTL_TREAT_WARNINGS_AS_ERRORS": "Metal warning policy",
        "SWIFT_TREAT_WARNINGS_AS_ERRORS": "Swift warning policy",
        "SWIFT_APPROACHABLE_CONCURRENCY = YES": "approachable concurrency baseline",
        "SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor": "default actor isolation baseline",
        "SWIFT_STRICT_CONCURRENCY = complete": "strict concurrency baseline",
        "newest stable Swift language mode": "future-facing Swift language policy",
        "Enable each feature that remains opt-in": "language-mode-aware upcoming-feature policy",
        "warnings-as-errors can turn that diagnostic into a build failure": (
            "redundant upcoming-feature safety rule"
        ),
        "Xcode 27 inventory to evaluate": "Xcode 27 upcoming-feature inventory",
        "project-level `.xcconfig`": "project-level configuration ownership",
        "unit-test and UI-test targets": "test-target effective-value audit",
        "nearest applicable `AGENTS.md`": "local exception source",
        "condition for removing or revisiting the exception": "exception lifecycle",
    }
    for value, description in required.items():
        if value not in contents:
            errors.append(
                f"{XCODE_PROJECT_SETTINGS_GUIDELINE.relative_to(ROOT)}: "
                f"missing {description}: {value!r}"
            )

    for setting in UPCOMING_FEATURE_SETTINGS:
        if setting not in contents:
            errors.append(
                f"{XCODE_PROJECT_SETTINGS_GUIDELINE.relative_to(ROOT)}: "
                f"missing Xcode 27 upcoming-feature inventory entry: {setting!r}"
            )


def validate_external_dependency_policy(errors: list[str]) -> None:
    development = DEVELOPMENT_GUIDELINE.read_text(encoding="utf-8")
    required_development = {
        "## External dependencies": "external dependency policy section",
        "Do not introduce a new third-party source or binary dependency": (
            "native and first-party default"
        ),
        "explicit approval from the repository owner": "repository-owner approval gate",
        "durable repository documentation": "durable exception record",
        "Tooling dependencies explicitly required by these shared guidelines": (
            "tooling-only exception"
        ),
    }
    for value, description in required_development.items():
        if value not in development:
            errors.append(
                f"{DEVELOPMENT_GUIDELINE.relative_to(ROOT)}: "
                f"missing {description}: {value!r}"
            )

    packages = PACKAGES_GUIDELINE.read_text(encoding="utf-8")
    required_packages = {
        "[external dependency policy](Development.md#external-dependencies)": (
            "package dependency policy pointer"
        ),
        "must not introduce or conceal a third-party runtime dependency": (
            "first-party package boundary"
        ),
        "guideline-mandated tooling dependency": "DocC tooling exception",
    }
    for value, description in required_packages.items():
        if value not in packages:
            errors.append(
                f"{PACKAGES_GUIDELINE.relative_to(ROOT)}: "
                f"missing {description}: {value!r}"
            )

    template = AGENTS_TEMPLATE.read_text(encoding="utf-8")
    if "BEGIN THATFACTORY EXTERNAL DEPENDENCY CONTRACT v1" not in template:
        errors.append(
            f"{AGENTS_TEMPLATE.relative_to(ROOT)}: missing external-dependency contract"
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
        "AppLogger": "AppLogger integration audit",
        "Logging.md": "shared Logging guide reference",
        "## Audit documentation consistency": "documentation drift audit",
        "Known stale documentation blocks completion": "stale documentation stopping rule",
        "## Audit documentation formatting": "documentation formatting audit",
        "check_markdown_wrapping.py": "Markdown line-wrapping check",
        "existing root Markdown files and declared durable documentation folders": (
            "documentation-convention adoption pass"
        ),
        "new third-party dependency": "third-party dependency audit",
        "repository-owner approval": "third-party dependency approval gate",
        "no unresolved P0/P1 blocker remains": "Codex review stopping rule",
        "## Audit Xcode project settings": "Xcode project-settings audit",
        "Xcode/ProjectSettings.md": "shared Xcode project-settings guide reference",
        "GCC_TREAT_WARNINGS_AS_ERRORS": "warnings-as-errors project audit",
        "SWIFT_UPCOMING_FEATURE_": "future-facing upcoming-feature audit",
        "SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor": "actor-isolation project audit",
        "SWIFT_VERSION": "Swift language-version project audit",
        "xcodebuild -showBuildSettings": "effective target build-setting inspection",
        "nearest applicable `AGENTS.md`": "project-setting exception lookup",
        "## Audit localization": "localization audit",
        "Swift/Localization.md": "shared Localization guide reference",
        "prepare_localizable_symbols.py": "generated-symbol preparation audit",
        "validate_string_catalogs.py": "String Catalog validation audit",
        "A local wrapper may": "consumer localization-wrapper boundary",
    }
    for value, description in required_skill_values.items():
        if value not in skill:
            errors.append(
                f"{AUDIT_SKILL.relative_to(ROOT)}: missing {description}: {value!r}"
            )

    if not MARKDOWN_WRAPPING_SCRIPT.is_file():
        errors.append(
            f"{MARKDOWN_WRAPPING_SCRIPT.relative_to(ROOT)}: missing Markdown wrapping checker"
        )
    elif not os.access(MARKDOWN_WRAPPING_SCRIPT, os.X_OK):
        errors.append(
            f"{MARKDOWN_WRAPPING_SCRIPT.relative_to(ROOT)}: checker is not executable"
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
    if "BEGIN THATFACTORY DOCUMENTATION MAINTENANCE CONTRACT v1" not in agents_template:
        errors.append(
            f"{AGENTS_TEMPLATE.relative_to(ROOT)}: missing documentation-maintenance contract"
        )
    if "BEGIN THATFACTORY EXTERNAL DEPENDENCY CONTRACT v1" not in agents_template:
        errors.append(
            f"{AGENTS_TEMPLATE.relative_to(ROOT)}: missing external-dependency contract"
        )
    if "AgentGuidelines/Guidelines/Documentation.md" not in agents_template:
        errors.append(
            f"{AGENTS_TEMPLATE.relative_to(ROOT)}: missing Documentation.md pointer"
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
    validate_documentation_guideline(errors)
    validate_localization_guideline(errors)
    validate_localization_scripts(errors)
    validate_xcode_project_settings_guideline(errors)
    validate_external_dependency_policy(errors)
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
