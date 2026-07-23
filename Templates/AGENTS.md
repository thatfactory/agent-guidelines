# Project Instructions

## Context

Describe the product or package, supported platforms, and durable constraints. Link to the project README or product documentation instead of duplicating it.

## Shared guidelines

Read only the guides relevant to the task:

- [Swift](AgentGuidelines/Guidelines/Swift/Swift.md)
- [Swift style](AgentGuidelines/Guidelines/Swift/SwiftStyle.md)
- [SwiftUI](AgentGuidelines/Guidelines/Swift/SwiftUI.md)
- [SwiftLint](AgentGuidelines/Guidelines/Swift/SwiftLint.md)
- [Localization](AgentGuidelines/Guidelines/Swift/Localization.md)
- [Unit and integration testing](AgentGuidelines/Guidelines/Testing/UnitTesting.md)
- [Documentation](AgentGuidelines/Guidelines/Documentation.md)
- [Logging](AgentGuidelines/Guidelines/Logging.md)
- [Packages](AgentGuidelines/Guidelines/Packages.md)
- [CI/CD](AgentGuidelines/Guidelines/CICD.md)
- [Git repositories and SSH-first cloning](AgentGuidelines/Guidelines/Git/Repositories.md)
- [GitHub pull requests](AgentGuidelines/Guidelines/GitHub/PullRequests.md)
- [Xcode MCP and visual verification](AgentGuidelines/Guidelines/Xcode/MCP.md)
- [Xcode security audits](AgentGuidelines/Guidelines/Xcode/Security.md)

For an application that uses Redux, also read [Redux architecture](AgentGuidelines/Guidelines/Architecture/Redux.md).

## Physical folder map

Replace these examples with exact repository paths:

| Role | Physical folder |
|---|---|
| Application sources | `<AppName>/` |
| Redux | `<AppName>/Redux/` |
| Views | `<AppName>/View/` |
| Services | `<AppName>/Services/` |
| Unit tests | `<AppName>Tests/` |

## Local specialization

State only rules that specialize or override the shared baseline. Explain their scope and point to local source-of-truth documentation.
