# Project Instructions

## Context

Describe the product or package, supported platforms, and durable constraints. Link to the project README or product documentation instead of duplicating it.

## Shared guidelines

Read only the guides relevant to the task:

- [Agent workflow](AgentGuidelines/Guidelines/AgentWorkflow.md)
- [Swift](AgentGuidelines/Guidelines/Swift/Swift.md)
- [Swift style](AgentGuidelines/Guidelines/Swift/SwiftStyle.md)
- [SwiftUI](AgentGuidelines/Guidelines/Swift/SwiftUI.md)
- [Swift format](AgentGuidelines/Guidelines/Swift/SwiftFormat.md)
- [Localization](AgentGuidelines/Guidelines/Swift/Localization.md)
- [Unit and integration testing](AgentGuidelines/Guidelines/Testing/UnitTesting.md)
- [Documentation](AgentGuidelines/Guidelines/Documentation.md)
- [Logging](AgentGuidelines/Guidelines/Logging.md)
- [Packages](AgentGuidelines/Guidelines/Packages.md)
- [Development workflow](AgentGuidelines/Guidelines/Development.md)
- [CI/CD](AgentGuidelines/Guidelines/CICD.md)
- [Git repositories and SSH-first cloning](AgentGuidelines/Guidelines/Git/Repositories.md)
- [GitHub pull requests](AgentGuidelines/Guidelines/GitHub/PullRequests.md)
- [Xcode MCP and visual verification](AgentGuidelines/Guidelines/Xcode/MCP.md)
- [Xcode security audits](AgentGuidelines/Guidelines/Xcode/Security.md)

For an application that uses Redux, also read [Redux architecture](AgentGuidelines/Guidelines/Architecture/Redux.md).

Keep the following marked contract in the consumer repository's root `AGENTS.md` so it is loaded directly for root-level Codex and pull-request work. Copy it unchanged and update it when the marker version changes in this template; a Markdown link to the detailed workflow is not an instruction include.

```md
<!-- BEGIN THATFACTORY CODE REVIEW CONTRACT v1 -->
## Code Review Rules

Review for release-blocking defects introduced or materially exposed by the pull request. A clean review means no unresolved P0/P1 findings; it does not mean exhaustive or perfect software.

A blocking finding must identify a concrete, reachable path in a supported use case or the documented threat model that can cause a credible security-boundary bypass, durable data loss or corruption, a crash or deadlock, loss of availability, violation of an explicit acceptance criterion, or a serious compatibility regression.

For every blocking finding, state the severity, preconditions, execution path, impact, evidence, and actionable remediation. Group manifestations that share the same root cause into one finding.

Treat P2/P3 observations as non-blocking, including defense-in-depth, theoretical completeness, unsupported use cases, malformed state that trusted code cannot produce, behavior by components outside the threat model, style preferences, and speculative refactoring. Record a useful lower-severity observation once as deferred, declined, duplicate, or follow-up work; do not keep the review loop open for it.

In an initial review, report substantiated blockers together. A follow-up review is limited to unresolved P0/P1 findings, changes since the last reviewed commit, and code directly affected by those changes. Do not restart an unrestricted review of unchanged code. A new follow-up finding must be a P0/P1 defect introduced by the remediation or genuinely hidden by the previous blocker.

Automatic Codex review is the initial review. Do not request a manual Codex review unless the repository owner explicitly asks. Never request another review after each remediation commit. Within the normal review budget, at most one owner-authorized, delta-scoped verification review may be requested under [the pull-request review workflow](AgentGuidelines/Guidelines/GitHub/PullRequests.md).
<!-- END THATFACTORY CODE REVIEW CONTRACT v1 -->

## Codex review scope

For consumer pull requests, do not substantively review `AgentGuidelines/**` after exact tagged-tree provenance has been verified. Verify its `VERSION`, compare its tree with the matching central tag, and verify the required `.gitattributes` rule. If provenance does not match exactly, review the subtree contents and stop the merge. Report substantive guideline feedback against the central `agent-guidelines` pull request.
```

The marked block is intentional controlled duplication of the shared review policy. The tracked, synchronized subtree is reviewed centrally in `thatfactory/agent-guidelines`; the root-level instructions ensure the review contract and subtree scope are loaded even when Codex starts from the repository root.

## Physical folder map

Replace these examples with exact repository paths:

| Role | Physical folder |
|---|---|
| Application sources | `<AppName>/` |
| Redux | `<AppName>/Redux/` |
| Views | `<AppName>/View/` |
| Services | `<AppName>/Services/` |
| Unit tests | `<AppName>Tests/` |

## Stack

Record the supported Xcode, Swift, and platform versions. State strict-concurrency mode, default actor isolation, infer-isolated-conformance behavior, and `nonisolated(nonsending)` defaults when they apply. Clarify whether application, package, and test targets share those settings.

## Local specialization

State only rules that specialize or override the shared baseline. Explain their scope and point to local source-of-truth documentation.
