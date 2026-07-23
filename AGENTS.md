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
