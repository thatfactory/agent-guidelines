# Agent Guidelines

## Purpose

This public repository is the versioned source of truth for reusable ThatFactory agent guidance. Keep it generic enough to apply to multiple applications and Swift packages. Product decisions, concrete project paths, and exceptions belong in each consumer repository.

## Sources of truth

- Use official Apple documentation for Apple APIs and Xcode behavior.
- Distill durable policy from Xcode-provided skills; do not copy exported Apple skills into this repository.
- Do not include private company information, credentials, personal absolute paths, or consumer-specific implementation details.
- When shared and consumer guidance differ, the consumer's nearest applicable `AGENTS.md` is the explicit specialization.
- Before changing this repository, verify that the consumer's checked-in guidelines version is current where applicable.

## Documentation changes

- Keep each rule in the narrowest relevant guide and link to it rather than duplicating it.
- Use physical folder terminology for Xcode projects. Do not call filesystem folders Xcode groups.
- Keep examples generic and concise.
- Use relative Markdown links inside this repository.
- Update `README.md` when adding, moving, or removing a guide.
- Keep the README guideline catalog sorted alphabetically by link label.
- Update `CHANGELOG.md` and `VERSION` for a release.
- When releasing a new version, update the version in both the README installation command and the README consumer-update command. Keep both commands aligned with the new release, for example:

  ```sh
  git subtree add \
    --prefix=AgentGuidelines \
    https://github.com/thatfactory/agent-guidelines.git \
    <version> \
    --squash

  git subtree pull \
    --prefix=AgentGuidelines \
    https://github.com/thatfactory/agent-guidelines.git \
    <version> \
    --squash
  ```

<!-- BEGIN THATFACTORY CODE REVIEW CONTRACT v1 -->
## Code Review Rules

Review for release-blocking defects introduced or materially exposed by the pull request. A clean review means no unresolved P0/P1 findings; it does not mean exhaustive or perfect software.

A blocking finding must identify a concrete, reachable path in a supported use case or the documented threat model that can cause a credible security-boundary bypass, durable data loss or corruption, a crash or deadlock, loss of availability, violation of an explicit acceptance criterion, or a serious compatibility regression.

For every blocking finding, state the severity, preconditions, execution path, impact, evidence, and actionable remediation. Group manifestations that share the same root cause into one finding.

Treat P2/P3 observations as non-blocking, including defense-in-depth, theoretical completeness, unsupported use cases, malformed state that trusted code cannot produce, behavior by components outside the threat model, style preferences, and speculative refactoring. Record a useful lower-severity observation once as deferred, declined, duplicate, or follow-up work; do not keep the review loop open for it.

In an initial review, report substantiated blockers together. A follow-up review is limited to unresolved P0/P1 findings, changes since the last reviewed commit, and code directly affected by those changes. Do not restart an unrestricted review of unchanged code. A new follow-up finding must be a P0/P1 defect introduced by the remediation or genuinely hidden by the previous blocker.

Automatic Codex review is the initial review. Do not request a manual Codex review unless the repository owner explicitly asks. Never request another review after each remediation commit. Within the normal review budget, at most one owner-authorized, delta-scoped verification review may be requested under [the pull-request review workflow](Guidelines/GitHub/PullRequests.md).
<!-- END THATFACTORY CODE REVIEW CONTRACT v1 -->

## Validation

Run:

```sh
python3 Scripts/validate_guidelines.py
```

Fix every validation failure before releasing a version.

## Consumer pull-request review scope

When reviewing a consumer pull request, do not review or comment on files under `AgentGuidelines/**` after exact tagged-tree provenance has been verified. That subtree is a tracked, synchronized copy marked `linguist-generated`; substantive guideline changes are reviewed in this repository. Verify the intended `AgentGuidelines/VERSION`, compare the subtree tree with the matching central tag (for example with `git subtree split --prefix=AgentGuidelines HEAD` and a tree comparison after fetching that tag), and verify the required `.gitattributes` rule. If provenance does not match exactly, review the subtree contents and stop the merge. Report substantive guideline feedback against the central `agent-guidelines` pull request instead.

## Releases

- Use semantic versioning.
- Create a Git tag and GitHub release matching `VERSION`.
- Consumer repositories adopt releases deliberately through Git subtree updates.
- Follow [the pull-request review workflow](Guidelines/GitHub/PullRequests.md) before merging any release change.
