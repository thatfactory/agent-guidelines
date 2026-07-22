# Changelog

All notable changes to this project are documented in this file.

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
