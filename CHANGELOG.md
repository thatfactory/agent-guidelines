# Changelog

All notable changes to this project are documented in this file.

## [0.0.18] - 2026-08-18

### Changed

- Corrected the standard README badge order to place DocC/documentation before license, updated date, revision, CI badges, and release/publishing status.

## [0.0.17] - 2026-08-18

### Added

- A version-marked consumer Code Review contract that defines P0/P1 release blockers, non-blocking P2/P3 observations, and bounded follow-up review scope.
- A deterministic consumer-setup validator for review-contract drift, subtree review scope, `.gitattributes`, local guide links, audit-skill wiring, and Swift-format adoption.

### Changed

- Expanded the global Codex instruction template and pull-request workflow to prioritize concrete release risk, group shared root causes, and stop review loops after blockers are resolved.
- Extended the completion-audit skill to verify consumer integration, review convergence, Swift-format configuration, local execution, and non-mutating CI coverage.
- Documented explicit Swift package formatting before tests and added a strict Swift-format CI template with package path coverage.

## [0.0.16] - 2026-08-13

### Changed

- Required SwiftUI dynamic properties to precede ordinary stored properties and clarified deterministic preview expectations.
- Required one top-level type per file, focused function decomposition, logical enum grouping, and consistent declaration-modifier and multiline-signature layout.
- Documented which declaration layout conventions remain review-guided because swift-format cannot enforce them without broad source reflow.

## [0.0.15] - 2026-07-27

### Added

- A shared agent-workflow guide for bounded grouping of independent repository inspections, with dependency, ordering, scope, and output-size safeguards.
- A versioned global Codex instruction template that bootstraps discovery of repository-local guidance without duplicating engineering policy.

### Changed

- Linked the workflow guide from the consumer template, documented the manual global Codex setup, and required alphabetical ordering of the README guideline catalog.
- Clarified that Codex review requests are automatic by default and must not be triggered manually without an explicit user request.

## [0.0.14] - 2026-07-27

### Changed

- Clarify Store/Middleware @MainActor usage.
- Removed workaround for a resolved Xcode issue.

## [0.0.13] - 2026-07-26

### Added

- A reusable `agent-guidelines-audit` skill and mandatory completion gate before handoff, pull requests, merge readiness, and releases.
- A canonical Redux Store template plus dependency-container and middleware-composition guidance.
- Consumer Stack guidance for recording toolchain, platform, strict-concurrency, and actor-isolation settings.

### Changed

- Clarified Redux folder ownership, familiar domain grouping, model-versus-tool classification, service-local helpers, presentation models, and one-component-per-file organization.
- Required documentation for new Swift declarations, meaningful `MARK` sections, one meaningful SwiftUI view per file, and deterministic previews where possible.
- Clarified when target isolation defaults replace explicit annotations and when compiler-verified boundaries still require them.
- Enabled conditional-import sorting and expanded validation for Swift templates, the audit skill, Stack guidance, and formatting policy.

## [0.0.12] - 2026-07-25

### Added

- Login-shell guidance for using explicitly authorized `gh` credentials exported by local shell startup configuration without exposing token values.

## [0.0.11] - 2026-07-25

### Added

- Pre-compilation Xcode build-phase guidance and a reusable `format-and-lint` command for human and agent workflows.
- An easy-to-find record of Xcode-aligned layout settings, enabled rule overrides, and deliberate non-adoptions.
- Pull-request guidance that prevents duplicate manual Codex requests when automatic review is enabled.

### Changed

- Enabled empty-array literals, force-try rejection, brace whitespace cleanup, `where` clauses in eligible loops, and documentation-comment validation.

## [0.0.10] - 2026-07-24

### Added

- Shared Xcode-aligned swift-format and EditorConfig configuration.
- Reusable format, warning-lint, and strict-lint commands for Swift consumers.

### Changed

- Replaced SwiftLint guidance with toolchain-native swift-format guidance.

## [0.0.9] - 2026-07-23

### Added

- Consumer pull-request review scope that excludes synchronized `AgentGuidelines/**` files from substantive Codex and human review outside the central repository.

## [0.0.8] - 2026-07-23

### Added

- Consumer guidance for keeping `AgentGuidelines/` tracked while collapsing synchronized files in GitHub pull-request diffs with `.gitattributes`.
- Pull-request conventions for isolated subtree commits, explicit version notes, central review links, and continued CI validation.

## [0.0.7] - 2026-07-23

### Added

- Shared logging ownership, subsystem, package emoji, message design, privacy, testing, and filtering guidance.
- Logging pointers for application development, Swift packages, and consumer instruction templates.

## [0.0.6] - 2026-07-22

### Added

- Generic Redux store contracts, state/action, service-boundary, projection, and middleware guidance.
- Generic GitHub Actions workflow, self-hosted runner, build strategy, and failure-investigation guidance.
- Shared documentation conventions and test-tag/mock guidance.

## [0.0.5] - 2026-07-21

### Added

- Default DocC documentation and GitHub Pages publishing guidance for Swift packages.

## [0.0.4] - 2026-07-21

### Added

- Development guidance for reusability-first design and checking the latest shared-guidelines version before project work.

### Changed

- Require an approved pull request before releasing `agent-guidelines` or any consumer package.

## [0.0.3] - 2026-07-21

### Added

- A Codex review-monitoring workflow covering paginated processing reactions and review threads, clean reviews, inline feedback, replies, thread resolution, and CI checks.

## [0.0.2] - 2026-07-21

### Added

- Standard README badge conventions for ThatFactory projects and packages.
- Git repository guidance that defaults push-capable clones to SSH remotes.
- GitHub pull-request review and merge-gate guidance.
- Updated and Revision badges to the repository README.

### Changed

- Updated GitHub workflows to `actions/checkout@v7` and documented using current stable action versions in new workflows.
- Clarified the Redux side-effect loop and the canonical view-projection test path.
- Expanded and tested semantic-version validation to support prerelease plus build metadata and reject invalid numeric identifiers.
- Removed the redundant README license section while retaining the MIT license badge and root license file.

## [0.0.1] - 2026-07-21

### Added

- Initial shared guidelines for Redux, Swift, SwiftUI, SwiftLint, localization, testing, documentation, package maintenance, CI/CD, Xcode MCP, and Xcode security audits.
- A consumer `AGENTS.md` template and Git subtree installation workflow.
- Structural validation for links, the documentation catalog, version metadata, subtree instructions, and public-repository safety.
- A tag-driven GitHub release workflow that validates the tag against `VERSION` and publishes changelog notes.
