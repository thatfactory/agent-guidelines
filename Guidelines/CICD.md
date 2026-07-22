# CI/CD

## Workflow principles

- Keep CI deterministic, reproducible, and aligned with the repository's supported Xcode, Swift, and platform versions.
- Treat warnings introduced by a change as failures even when the compiler does not.
- Prefer the smallest permissions required by each workflow and job.
- For a new workflow, use the latest stable major version of every GitHub Action available at the time of creation.
- Do not copy an older major version into a fresh workflow unless a documented compatibility constraint requires it.
- For existing workflows, review action release notes and update deliberately rather than allowing runtime deprecation warnings to accumulate.
- Pin third-party actions to an intentional version and review updates.
- Do not place secrets in workflow files, logs, fixtures, or command arguments that may be echoed.
- Keep release workflows separate from pull-request validation when their permissions differ.

## `ci-pr.yml`

Projects using GitHub Actions should keep pull-request validation in `.github/workflows/ci-pr.yml`, triggered by `pull_request` events for `opened`, `synchronize`, and `reopened`.

Use self-hosted runners identified by the repository's declared `Runner labels:`. Do not hard-code a particular machine name in shared guidance.

A typical Swift package validates:

- package resolution;
- build;
- Swift Testing tests;
- DocC generation when the package publishes documentation;
- repository-specific lint or validation scripts.

An Xcode application validates its declared scheme and test plan. Use the same project/workspace, configuration, and platform assumptions documented for local development.

For Xcode projects, test with `xcodebuild test` and explicit simulators, then validate compilation with `xcodebuild build CODE_SIGNING_ALLOWED=NO` across the supported platforms. For Swift packages, use Swift Package Manager commands such as `swift test` and `swift build`; packages do not require simulator selection or signing configuration. CI validates tests and compile health, not app-store distribution.

## `ci.yml`

Validation of merges to `main` should live in `.github/workflows/ci.yml`, triggered by `push` on `main`. Use the same build, test, lint, and platform coverage as pull-request validation unless the repository documents a deliberate difference.

## Failure investigation

1. Use GitHub MCP connector tools to inspect check runs and logs for the failing commit or pull request.
2. Use `gh` for fast local triage when needed.
3. Reproduce locally with the exact build or test command shown in the failing job logs.

Useful commands:

```bash
gh run list --limit 10
gh run view <run-id>
gh run view <run-id> --log
```

Distinguish compiler errors from lint violations, test failures from simulator or runtime infrastructure failures, and single-job failures from cross-platform matrix failures. Identify the first meaningful failing step, fix the narrowest root cause, and re-run affected validation.

## Releases

- A release tag and GitHub release must match the intended semantic version.
- Release notes summarize user- or integrator-relevant changes since the previous release.
- Use a notes file for multiline CLI release descriptions.
- Do not publish a release from an unverified or dirty worktree.
- Follow the consumer's local instructions for deployment, signing, notarization, App Store, or documentation publishing steps.
