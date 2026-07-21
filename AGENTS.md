# Agent Guidelines

## Purpose

This public repository is the versioned source of truth for reusable ThatFactory agent guidance. Keep it generic enough to apply to multiple applications and Swift packages. Product decisions, concrete project paths, and exceptions belong in each consumer repository.

## Sources of truth

- Use official Apple documentation for Apple APIs and Xcode behavior.
- Distill durable policy from Xcode-provided skills; do not copy exported Apple skills into this repository.
- Do not include private company information, credentials, personal absolute paths, or consumer-specific implementation details.
- When shared and consumer guidance differ, the consumer's nearest applicable `AGENTS.md` is the explicit specialization.

## Documentation changes

- Keep each rule in the narrowest relevant guide and link to it rather than duplicating it.
- Use physical folder terminology for Xcode projects. Do not call filesystem folders Xcode groups.
- Keep examples generic and concise.
- Use relative Markdown links inside this repository.
- Update `README.md` when adding, moving, or removing a guide.
- Update `CHANGELOG.md` and `VERSION` for a release.

## Validation

Run:

```sh
python3 Scripts/validate_guidelines.py
```

Fix every validation failure before releasing a version.

## Releases

- Use semantic versioning.
- Create a Git tag and GitHub release matching `VERSION`.
- Consumer repositories adopt releases deliberately through Git subtree updates.

