# Swift Packages

## README badges

Start a new ThatFactory project or package README with a centered HTML badge block:

```html
<p align="center">
  <!-- Badges in the standard order. -->
</p>
```

For example, a repository using all supported badge configurations could use:

```html
<p align="center">
  <a href="https://developer.apple.com/swift/"><img alt="Swift Version" src="https://img.shields.io/badge/Swift-6.4-ea7a50.svg?logo=swift&logoColor=white"></a>
  <a href="https://developer.apple.com/xcode/"><img alt="Xcode Version" src="https://img.shields.io/badge/Xcode-27-50ace8.svg?logo=xcode&logoColor=white"></a>
  <a href="https://forums.swift.org/t/introducing-anyappleos/85728"><img alt="Platforms" src="https://img.shields.io/badge/AnyAppleOS-26%2B-lightgrey.svg?logo=apple&logoColor=white"></a>
  <a href="https://en.wikipedia.org/wiki/List_of_Apple_operating_systems"><img alt="Platforms" src="https://img.shields.io/badge/Platforms-iOS%2026%2B%20%7C%20macOS%2026%2B%20%7C%20tvOS%2026%2B-lightgrey.svg?logo=apple&logoColor=white"></a>
  <a href="https://developer.apple.com/documentation/xcode/swift-packages"><img alt="SPM" src="https://img.shields.io/badge/SPM-ready-b68f6a.svg?logo=gitlfs&logoColor=white"></a>
  <a href="https://www.npmjs.com/package/@thatfactory/xcode-cloud-mcp"><img alt="NPM" src="https://img.shields.io/badge/NPM-ready-CB3837.svg?logo=npm&logoColor=white"></a>
  <a href="https://developer.apple.com/xcode/"><img alt="Xcode MCP" src="https://img.shields.io/badge/Xcode-MCP-50ace8.svg?logo=xcode&logoColor=white"></a>
  <a href="https://developers.openai.com/codex/mcp"><img alt="Codex MCP" src="https://img.shields.io/badge/Codex-MCP-1F70C1.svg?logo=icloud&logoColor=white"></a>
  <a href="https://docs.anthropic.com/en/docs/claude-code/mcp"><img alt="Claude MCP" src="https://img.shields.io/badge/Claude-MCP-D97757.svg?logo=claude&logoColor=white"></a>
  <a href="https://thatfactory.github.io/applogger/documentation/applogger/"><img alt="DocC" src="https://img.shields.io/badge/DocC-documentation-0288D1.svg?logo=bookstack&logoColor=white"></a>
  <a href="https://en.wikipedia.org/wiki/MIT_License"><img alt="License" src="https://img.shields.io/badge/License-MIT-67ac5b.svg?logo=googledocs&logoColor=white"></a>
  <a href="https://github.com/thatfactory/swift-package-collection/commits/main/"><img alt="Updated" src="https://img.shields.io/endpoint?url=https://thatfactory.github.io/swift-package-collection/badges/updated.json&logo=convertio&logoColor=white"></a>
  <a href="https://github.com/thatfactory/swift-package-collection/blob/main/CHANGELOG.md"><img alt="Revision" src="https://img.shields.io/endpoint?url=https://thatfactory.github.io/swift-package-collection/badges/revision.json&logo=gitbook&logoColor=white"></a>
  <a href="https://github.com/thatfactory/agent-guidelines/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/thatfactory/agent-guidelines/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/thatfactory/swift-package-collection/actions/workflows/publish.yml"><img alt="Publish" src="https://github.com/thatfactory/swift-package-collection/actions/workflows/publish.yml/badge.svg"></a>
  <a href="https://github.com/thatfactory/xcode-cloud-mcp/actions/workflows/nightly.yml"><img alt="Nightly" src="https://github.com/thatfactory/xcode-cloud-mcp/actions/workflows/nightly.yml/badge.svg"></a>
</p>
```

Use only badges that describe the repository, in this order:

1. Swift version.
2. Xcode version.
3. Supported platforms.
4. Relevant package manager, runtime, or ecosystem badges, such as SPM or NPM.
5. Relevant agent or tooling badges, such as Xcode MCP, Codex, or Claude.
6. DocC, documentation.
7. License.
8. Updated date.
9. Revision or latest release.
10. CI badges.
11. Release/publishing status when applicable.

The common package baseline is Swift, Xcode, Platforms, License, and CI. Add optional badges only when they convey useful repository-specific information. Keep the order stable even when some positions are omitted.

- Point CI, publishing, and documentation badges at workflows in the current repository; never copy another repository's badge URL unchanged.
- Use descriptive `alt` text. Preserve a repository's established Xcode badge convention when the label intentionally records the last verified Xcode version.
- Prefer dynamic Updated and Revision badges backed by repository history or releases so maintainers do not edit dates and versions by hand.
- Do not advertise a platform, integration, package manager, or agent that the repository does not support.
- Keep the repository's license in a root `LICENSE` file when reuse or redistribution is permitted. A README license heading is optional; the badge is a summary, not the license grant.
- Do not add a license to an existing repository without the owner's explicit choice of terms.

## Package boundaries

- Keep a reusable package focused on one coherent capability.
- Prefer UI-agnostic domain APIs unless UI is the package's explicit purpose.
- Do not add application Redux, navigation, persistence, or product policy to a generic package.
- Keep public APIs minimal and stable. Prefer composing focused types over introducing umbrella abstractions before multiple consumers need them.
- Declare platform and Swift toolchain requirements explicitly in `Package.swift`.
- New Swift packages must start on the latest supported Swift language and toolchain version. Before adding a major package capability to an older package, plan and complete the required Swift/toolchain modernization first.
- Put sources under `Sources/<Target>/` and tests under `Tests/<Target>Tests/`.
- Keep resources in the target that owns them and use the package bundle for lookup.

## Logging

Packages own any diagnostics emitted by their implementation. Follow the shared [logging guide](Logging.md) for AppLogger usage, subsystem identity, package emoji prefixes, domain-owned categories, concise messages, privacy, and test coverage. A consuming application must not reproduce package-internal logs.

## Development workflow

1. Read the package's local `AGENTS.md`, README, DocC, and public API before changing behavior.
2. Add or update tests in the package itself.
3. Update DocC and README examples when public behavior changes.
4. Run the focused tests, then `swift test` or the package's declared Xcode test workflow.
5. Integrate the package into a consumer locally only when consumer behavior must also be verified.
6. Avoid committing consumer-specific workarounds into the package when the behavior belongs in the consumer.

## DocC documentation

DocC is the default documentation format for public Swift packages. Document public APIs with `///` DocC comments and keep package-level conceptual material in a DocC catalog when it needs more than declaration comments.

Before adopting the DocC command, an existing package must be updated to the latest supported Swift toolchain and declare the Swift-DocC plugin dependency in `Package.swift` (for example, `.package(url: "https://github.com/swiftlang/swift-docc-plugin", from: "<current-plugin-version>")`). New packages must declare this prerequisite from the beginning when they publish DocC.

Packages that publish documentation must build and deploy their DocC site as part of the release workflow:

1. Run tests before documentation generation.
2. Generate static-hosting documentation with `swift package generate-documentation --target <Target> --disable-indexing --output-path ./public --transform-for-static-hosting --hosting-base-path <repository-name>`.
3. Add a root redirect to `/<repository-name>/documentation/<target-lowercase>/`.
4. Upload `./public` with `actions/upload-pages-artifact` and deploy it with `actions/deploy-pages`.
5. Grant the workflow `pages: write` and `id-token: write` permissions and expose the deployed URL in the README through a DocC badge.

The release job must publish documentation only after the release has been approved, merged, tagged, and published. Verify the generated site locally when practical and keep the README badge URL aligned with the repository's GitHub Pages site.

## Local integration

- Use Xcode's local-package workflow or an explicit temporary local dependency while developing package and consumer changes together.
- Do not commit machine-specific absolute package paths.
- Before release, restore the consumer to the tagged remote dependency unless its local instructions intentionally retain a monorepo relationship.
- Verify the final remote version resolves on a clean checkout.

## Releases

Never release a package directly from unreviewed changes. Every release change must first be submitted through a pull request, reviewed, and approved. This rule applies to `agent-guidelines` itself as well as every consumer package. Create and publish the release only after the PR has merged.

For ThatFactory packages, “release a new version” means:

1. Choose a semantic version appropriate to compatibility.
2. Update public documentation and release notes.
3. Run the declared CI/test workflow.
4. Open a pull request containing the release state and wait for approval.
5. Merge the approved pull request.
6. Create and push the matching Git tag.
7. Create a GitHub release for that tag.
8. Use real multiline release notes and backticks around technical names and versions.

When using a CLI, pass multiline notes through a file so GitHub renders line breaks correctly.

## Consumer updates

- Review package release notes and API changes before updating.
- Update one dependency relationship intentionally; do not rewrite unrelated resolved versions.
- Build and test the affected consumer behavior.
- Update the consumer's package integration documentation when roles, mappings, or workflows change.
