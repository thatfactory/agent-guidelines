<p align="center">
  <a href="https://developer.apple.com/xcode/"><img alt="Xcode" src="https://img.shields.io/badge/Xcode-MCP-50ace8.svg?logo=xcode&logoColor=white"></a>
  <a href="https://developers.openai.com/codex/mcp"><img alt="Codex" src="https://img.shields.io/badge/Codex-MCP-1F70C1.svg?logo=icloud&logoColor=white"></a>
  <a href="https://github.com/thatfactory/agent-guidelines/commits/main"><img alt="Updated" src="https://img.shields.io/github/last-commit/thatfactory/agent-guidelines?label=Updated&logo=convertio&logoColor=white"></a>
  <a href="https://github.com/thatfactory/agent-guidelines/releases"><img alt="Revision" src="https://img.shields.io/github/v/release/thatfactory/agent-guidelines?label=Revision&logo=gitbook&logoColor=white"></a>
  <a href="https://en.wikipedia.org/wiki/MIT_License"><img alt="License" src="https://img.shields.io/badge/License-MIT-67ac5b.svg?logo=googledocs&logoColor=white"></a>
  <a href="https://github.com/thatfactory/agent-guidelines/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/thatfactory/agent-guidelines/actions/workflows/ci.yml/badge.svg"></a>
</p>

# Agent Guidelines

`agent-guidelines` is ThatFactory's public, versioned source of truth for reusable instructions given to coding agents. It centralizes stable decisions about Swift development, Redux architecture, testing, documentation, logging, packages, CI/CD, localization, and Xcode tooling while leaving product context and exceptions in each consuming repository.

The repository contains documentation, not a Swift product. Consumers install a tagged release as a Git subtree at `AgentGuidelines/`, so every agent sees ordinary version-controlled files at predictable paths.

## How it fits together

```text
                  thatfactory/agent-guidelines
                  versioned GitHub repository
                             |
                       tagged release
                         e.g. 0.0.3
                             |
                    git subtree add/pull
                             |
                             v
+---------------- Consumer project or package ----------------+
|                                                              |
|  AGENTS.md                                                   |
|  |-- local product/package context                           |
|  |-- concrete project paths                                  |
|  |-- local exceptions                                        |
|  `-- pointers to shared guidelines -----------------+        |
|                                                     |        |
|  AgentGuidelines/                                   |        |
|  |-- VERSION                                        |        |
|  `-- Guidelines/ <----------------------------------+        |
|      |-- Architecture/Redux.md                              |
|      |-- Swift/SwiftUI.md                                   |
|      |-- Testing/UnitTesting.md                             |
|      `-- Xcode/MCP.md                                       |
|                                                              |
|  Sources and project files                                   |
+----------------------------+---------------------------------+
                             |
              reads instructions and project files
                  +----------+----------+
                  v                     v
               Codex                Xcode agent
                  |
                  | Xcode MCP (`xcrun mcpbridge`)
                  v
                Xcode
```

The subtree does not automatically import every guide into an agent's context. A consumer's root or folder-scoped `AGENTS.md` tells the agent which shared guides to read for the task. The nearest local `AGENTS.md` can specialize or override the shared baseline.

## Guideline catalog

- [Redux architecture and physical folder organization](Guidelines/Architecture/Redux.md)
- [Swift](Guidelines/Swift/Swift.md)
- [Swift style](Guidelines/Swift/SwiftStyle.md)
- [SwiftUI](Guidelines/Swift/SwiftUI.md)
- [SwiftLint](Guidelines/Swift/SwiftLint.md)
- [Localization](Guidelines/Swift/Localization.md)
- [Unit and integration testing](Guidelines/Testing/UnitTesting.md)
- [Documentation](Guidelines/Documentation.md)
- [Logging](Guidelines/Logging.md)
- [Swift packages](Guidelines/Packages.md)
- [Development and reusability](Guidelines/Development.md)
- [CI/CD](Guidelines/CICD.md)
- [Git repositories and SSH-first cloning](Guidelines/Git/Repositories.md)
- [GitHub pull requests](Guidelines/GitHub/PullRequests.md)
- [Xcode MCP and visual verification](Guidelines/Xcode/MCP.md)
- [Xcode security audits](Guidelines/Xcode/Security.md)

Only reference the guides that apply. A UI-agnostic package normally uses Swift, style, testing, documentation, logging, packages, CI/CD, and Xcode guidance, but not Redux or SwiftUI guidance.

## Add to a consumer

From the consumer repository root, install a tagged release:

```sh
git subtree add \
  --prefix=AgentGuidelines \
  https://github.com/thatfactory/agent-guidelines.git \
  0.0.8 \
  --squash
```

Keep the subtree tracked, but add this to the consumer's tracked `.gitattributes` so GitHub collapses synchronized guideline files in pull-request diffs by default:

```gitattributes
# Synced from thatfactory/agent-guidelines; keep tracked but collapse GitHub diffs.
AgentGuidelines/** linguist-generated
```

Copy and adapt [the consumer template](Templates/AGENTS.md). Keep the consumer file small: describe the product or package, map its concrete physical folders, point to the applicable shared guides, and state only genuine exceptions.

## Update a consumer

Review the target release's changelog, then pull it deliberately:

```sh
git subtree pull \
  --prefix=AgentGuidelines \
  https://github.com/thatfactory/agent-guidelines.git \
  0.0.8 \
  --squash
```

Confirm `AgentGuidelines/VERSION`, ensure the `.gitattributes` rule above is present, review the subtree diff, validate local `AGENTS.md` pointers, and run the consumer's relevant tests. Keep the subtree update in its own commit, and identify the old and new versions plus the central release or pull request in the consumer pull-request description. Updates are intentionally not automatic: one guideline release cannot silently change every project.

## Maintain the source of truth

1. Export current Xcode skills to a temporary review location when a new Xcode release materially changes agent behavior:

   ```sh
   xcrun agent skills export --output-dir <temporary-directory>
   ```

2. Compare relevant guidance with this repository and official Apple documentation.
3. Bring over durable policy, not the exported skill text or an SDK API catalog.
4. Remove obsolete or conflicting rules instead of accumulating historical alternatives.
5. Run `python3 Scripts/validate_guidelines.py`.
6. Update `VERSION` and `CHANGELOG.md`, open a pull request, and wait for approval before merging.
7. After the pull request has merged, create the matching tag and GitHub release.

## Precedence

For a consumer task, apply instructions in this order:

1. The user's explicit request.
2. The nearest applicable consumer `AGENTS.md`.
3. The consumer root `AGENTS.md`.
4. The shared guides explicitly referenced by those files.

Official Apple documentation remains authoritative for API behavior. A local convention can deliberately narrow a choice, but it must not rely on behavior contradicted by the current SDK documentation.
