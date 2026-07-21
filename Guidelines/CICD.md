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

## Pull-request CI

A typical Swift package validates:

- package resolution;
- build;
- Swift Testing tests;
- DocC generation when the package publishes documentation;
- repository-specific lint or validation scripts.

An Xcode application validates its declared scheme and test plan. Use the same project/workspace, configuration, and platform assumptions documented for local development.

## Investigation

1. Identify the first meaningful failing step rather than treating later cancellations as independent failures.
2. Reproduce locally with the closest supported toolchain when practical.
3. Separate infrastructure or dependency-resolution failures from code failures.
4. Fix the root cause in the narrowest appropriate layer.
5. Re-run the affected local validation before relying on remote CI.
6. Update durable CI documentation when the workflow or investigation process changes.

## Releases

- A release tag and GitHub release must match the intended semantic version.
- Release notes summarize user- or integrator-relevant changes since the previous release.
- Use a notes file for multiline CLI release descriptions.
- Do not publish a release from an unverified or dirty worktree.
- Follow the consumer's local instructions for deployment, signing, notarization, App Store, or documentation publishing steps.
