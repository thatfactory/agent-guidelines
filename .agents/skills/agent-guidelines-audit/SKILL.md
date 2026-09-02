---
name: agent-guidelines-audit
description: Audit completed repository work and checked-in consumer integration against applicable agent-guidelines, local AGENTS.md instructions, requested scope, and declared validation workflow. Use after implementing changes and before claiming completion, handing work to the user, preparing, opening, or updating a pull request, declaring merge readiness, or preparing a release. Do not use for simple answers, read-only exploration, or work that is still actively being implemented.
---

# Agent Guidelines Audit

Perform a final, evidence-based compliance pass. Treat the applicable guidelines and local instructions as the source of truth; do not duplicate their full content in this skill.

## Establish the audit scope

1. Re-read the user request and list every requested outcome and explicit constraint.
2. Locate the repository root and every applicable `AGENTS.md` from the current directory to that root.
3. Read the shared guides referenced by those instructions that apply to the changed files and workflow.
4. Inspect `git status`, the complete diff, and relevant untracked files. Preserve unrelated user changes.
5. Check the consumer's `AgentGuidelines/VERSION` and provenance when the task changes or depends on the synchronized subtree. Do not update it implicitly.
6. When the repository contains an `AgentGuidelines/` subtree, run `python3 AgentGuidelines/Scripts/validate_consumer_setup.py` from the consumer root. The validator detects Swift-format adoption from the root `AGENTS.md`; add `--require-swift-format` only when the repository must adopt it before that link is present. Treat failures as integration drift to fix or report before handoff.

Do not inspect or require the user's global Codex instructions. They are user-level state outside the repository audit boundary; validate the checked-in root `AGENTS.md` contract instead.

## Audit the implementation

Review the actual change rather than only checking whether files exist:

- Confirm every requested outcome is implemented and no material behavior was dropped.
- Confirm physical folders, familiar domain grouping, filenames, declaration order, type ownership, namespacing, documentation, and `MARK` organization follow the applicable guides. Distinguish values that describe data from tools that primarily execute algorithms or accumulate behavior.
- For Redux applications, trace actions, state, reducers, middleware, services, tools, presentation models, views, and side-effect results through the complete data flow. Confirm each Redux component folder contains only that component type.
- Check that framework objects, persistence, logging, and asynchronous work remain in their allowed boundaries.
- Check SwiftUI composition, narrow inputs, local versus durable state, localization, accessibility, and safe deterministic previews where applicable.
- Check tests for the required framework, mirrored paths, shared tags, Given/When/Then structure, deterministic seams, and coverage of changed behavior and failure paths.
- Check logging ownership, subsystem, categories, emoji, privacy, severity, metadata stability, and noise controls when logging changed.
- For every Apple-platform application or Swift package in scope, except the AppLogger provider repository itself, verify integration with the shared [Logging guide](../../../Guidelines/Logging.md): confirm the AppLogger dependency is declared, the `AppLogger` library product is linked to every target that emits diagnostics, and any new project has it available in its primary runtime target before its first log call. Search the actual package or Xcode dependency graph rather than relying on an `import` alone, and treat `print`, direct `Logger` instances, or duplicate logging backends as incomplete integration when they emit project diagnostics. When implementation is authorized, add or repair the dependency and target linkage and migrate affected calls while preserving the guide's ownership, subsystem, category, emoji, privacy, severity, and noise rules; report an exact blocker when target or platform constraints make safe integration ambiguous.
- Inspect dependency manifests, resolver or lock files, Xcode package references, vendored source or binary frameworks, and equivalent dependency declarations. Compare the change with the baseline and identify every new third-party dependency or expansion of an existing third-party dependency into a new target or runtime role. Apply the shared [external dependency policy](../../../Guidelines/Development.md#external-dependencies): require explicit repository-owner approval before the dependency is introduced and require the durable exception record in repository documentation. Do not infer approval merely from an execution plan, pull-request description, implementation convenience, package popularity, or the dependency already appearing in the diff. Treat an unapproved or undocumented third-party dependency as a blocker to completion. Do not flag Apple system frameworks, the Swift standard library, ThatFactory-owned packages, or guideline-mandated tooling used only for its documented tooling role. If a newly resolved transitive third-party package will be linked into or shipped with the product, verify that its owning direct dependency is covered by an approved exception rather than dismissing it solely because it is transitive.
- Check package configuration, CI/CD, Xcode project configuration, security-sensitive changes, and physical-device limitations when they are in scope. For every Xcode project, perform the project-settings audit below. Compare documented Swift and concurrency settings with the effective application and test-target settings; flag both redundant isolation annotations and missing annotations at compiler-verified boundaries.
- Search for stale type names, superseded files, direct APIs forbidden by the new architecture, empty folders, and references to removed behavior.
- For pull-request or merge readiness, apply the root `## Code Review Rules`: confirm the Codex review covers the current head, no allowed Codex review round is pending, every Codex review thread has a disposition, and no unresolved P0/P1 blocker remains. Treat P2/P3 observations as non-blocking and never request another Codex review unless the repository owner explicitly authorizes it. This Codex review-round budget does not apply to otherwise-authorized Reasoning Relay/ChatGPT review delegations; do not block them waiting for a Codex-budget exception.

## Audit Xcode project settings

For every checked-in `.xcodeproj`, read and apply the shared [Xcode project-settings guide](../../../Guidelines/Xcode/ProjectSettings.md):

1. Identify the selected Xcode and its newest stable Swift language mode. Inspect every `PBXProject` build configuration and project-level `.xcconfig`; target-only values do not satisfy project-level ownership.
2. Require `GCC_TREAT_WARNINGS_AS_ERRORS`, `MTL_TREAT_WARNINGS_AS_ERRORS`, and `SWIFT_TREAT_WARNINGS_AS_ERRORS` to be `YES`; require `SWIFT_APPROACHABLE_CONCURRENCY = YES`, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`, and `SWIFT_STRICT_CONCURRENCY = complete`; and require `SWIFT_VERSION` to select that newest stable language mode.
3. Discover every build setting exposed by the active Xcode whose name begins with `SWIFT_UPCOMING_FEATURE_`. For the selected Swift language mode, use the setting documentation and compiler diagnostics to identify which features remain opt-in. Require those settings to be `YES` at project level, and require flags for features already incorporated into the language mode to be absent so warnings-as-errors cannot turn a redundant-feature diagnostic into a build failure. Treat the settings listed in the shared guide as the Xcode 27 discovery inventory, not as flags that must all be enabled and not as a future-exhaustive list.
4. Enumerate every target and configuration, including unit-test and UI-test targets, and inspect effective values with Xcode project-aware tooling or `xcodebuild -showBuildSettings`. Remove redundant target copies and language-mode-redundant upcoming-feature flags. Treat a disabling or different target override for an applicable baseline setting as a violation unless an exact exception applies.
5. Before reporting a failure, search the nearest applicable `AGENTS.md` and durable project documentation linked from it for an exception naming the exact setting, scope, concrete incompatibility, replacement, impact, validation, and revisit condition. Accept and report an applicable documented exception; do not infer one from transient discussion, generic project prose, or the existing build setting itself.
6. When implementation is authorized, move or add compliant values at project level, remove redundant target copies, and rerun build-setting inspection plus relevant builds. For review-only work, report undocumented gaps without editing.

## Audit localization

When the repository contains localized Apple-platform targets or String Catalogs, read the shared [Localization guide](../../../Guidelines/Swift/Localization.md) and the consumer's local translation guidance:

1. Keep supported languages, catalog and source paths, product voice, glossary, non-translatable terms, and project-specific exceptions in consumer documentation. Do not move those specifics into shared guidance or infer them from another product.
2. Confirm the project uses generated localizable symbols for maintained Swift catalog entries, does not check generated Swift into source control, and does not add localizable Swift literals that bypass the generated API.
3. Require the synchronized `prepare_localizable_symbols.py` and `validate_string_catalogs.py` logic. A local wrapper may supply project paths and languages to preserve a stable developer or CI command, but it must not retain a forked copy of shared migration or validation logic.
4. Run the consumer's documented nonmutating preparation check and catalog validator. Confirm CI runs the validator for localized projects and that every configured catalog and Swift source root is covered.
5. Inspect stale entries, required-language coverage, translation states, plural variants, and format placeholders in context. Require Xcode catalog-editor diagnostics plus source/translated-language, long-text, plural, and right-to-left verification when affected.
6. Preserve machine-translation state until fluent review. Treat missing required validation, unresolved catalog errors, or undocumented project-specific deviations as incomplete implementation.

## Audit documentation consistency

When implementation, configuration, or workflow behavior changed, perform an explicit documentation-drift pass:

1. Read the applicable [Documentation guide](../../../Guidelines/Documentation.md) and identify code-level or durable project documentation that describes the affected feature, API, configuration, workflow, or invariant.
2. Compare those documented claims with the final implementation. Require a documentation update when the change alters durable or core behavior, or when any existing documented claim becomes inaccurate, incomplete, misleading, or obsolete, regardless of change size.
3. Search relevant durable documentation for changed names, removed behavior, defaults, examples, diagrams, setup steps, and references. Inspect matches in context rather than assuming a keyword search alone proves consistency.
4. Do not require new project-level prose for incidental implementation details that are not durable and do not affect an existing documented claim.
5. When implementation is authorized, update or remove stale documentation in the same change. For review-only work, report the drift without editing. Known stale documentation blocks completion.

## Audit documentation formatting

Apply the conventions in the applicable [Documentation guide](../../../Guidelines/Documentation.md) to governed Markdown:

1. Audit every added or changed Markdown file outside a synchronized, provenance-verified `AgentGuidelines/` subtree.
2. When the completed change adds or changes a documentation convention, or updates a consumer to a guideline release that does so, also audit the consumer's existing root Markdown files and declared durable documentation folders. This adoption pass is required even when those files did not otherwise change.
3. From the repository root, run `python3 .agents/skills/agent-guidelines-audit/scripts/check_markdown_wrapping.py <paths...>` against those files or folders. The checker is read-only and reports prose paragraphs, list items, and blockquotes that span multiple physical lines while excluding fenced code and other common verbatim Markdown constructs.
4. Inspect each reported span in context. Join confirmed hard-wrapped prose so each paragraph, list item, or blockquote occupies one physical line. Preserve intentional structure such as headings, separate list items, tables, fenced code, and ASCII diagrams.
5. When implementation is authorized, fix confirmed violations and rerun the checker. For review-only work, report them without editing. Do not claim the audit passes while a confirmed line-wrapping violation remains in scope.

## Validate the evidence

Run the repository's declared non-destructive checks in proportion to the change:

- formatter and strict lint;
- focused tests, followed by the declared broader test plan when warranted;
- relevant builds or package validation;
- repository-specific validators;
- `git diff --check`.

When the shared Swift-format guide applies:

- For implementation work, run `AgentGuidelines/Scripts/swift_format.sh format-and-lint` over every changed or applicable checked-in Swift source root before tests. For review-only work, use `lint-strict` so the audit does not mutate files.
- Confirm the root `.swift-format` and `.editorconfig` symlinks resolve to the synchronized shared configurations.
- Confirm pull-request and protected-branch CI run the shared wrapper with `lint-strict` in a dedicated non-mutating job. Reject `format` or `format-and-lint` in CI and verify the listed paths cover the repository's checked-in Swift roots.
- For Xcode projects, verify every independently buildable app or test target has the target-scoped pre-compilation phase described by the guide, including its `CI=true` bypass.
- For Swift packages, format `Package.swift`, `Sources`, `Tests`, and other checked-in Swift roots that exist before running `swift test`. Do not require `swift build` or `swift test` themselves to rewrite source; formatting and testing are consecutive, independently visible checks.

Use fresh successful evidence already produced in the same task instead of rerunning expensive checks without reason. Distinguish automated compilation and simulator evidence from hardware, signing, deployment, or manual validation that automation cannot prove.

## Resolve findings

- When the user authorized implementation, fix safe in-scope findings and rerun the affected checks.
- For review-only work, report findings without modifying code.
- Do not broaden the feature, rewrite unrelated files, edit a synchronized `AgentGuidelines/` subtree, or perform commits, pushes, pull requests, merges, tags, or releases without the required authority.
- Treat an unresolved required guideline violation or missing relevant validation as a blocker to claiming completion.

## Hand off

Summarize:

- the instruction and guideline areas audited;
- consumer-integration validation and any drift found;
- findings fixed during the audit;
- documentation updated or removed, or why no documentation change was required;
- validation commands and outcomes;
- any deliberate deviations, unavailable evidence, or remaining blockers.

Do not say the work is done merely because the audit ran. Say it is ready only when the requested outcome is complete and the relevant evidence passes.
