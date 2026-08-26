# Documentation

Documentation is part of implementation. For every codebase change, evaluate whether durable project knowledge or any existing documentation is affected; do not treat documentation as optional cleanup after code and tests are complete.

- Use PascalCase Markdown filenames without spaces.
- Keep the folder flat until one topic genuinely requires several files.
- Prefer current implementation over speculative future design; label known gaps explicitly.

## Code-level documentation

- Document every new struct, class, enum, protocol, actor, and function with focused `///` DocC comments.
- Use `// MARK: -` pragmas to separate meaningful logical sections so source files remain easy to scan and navigate.
- Update documentation when changing a documented API, parameter, behavior, or invariant.
- End documentation sentences with periods.
- Explain intent, contracts, units, side effects, isolation, and non-obvious constraints; do not restate syntax.
- Add a short Swift example when it materially clarifies correct use.
- Keep documentation close to the declaration it describes.

## Project-level documentation

- Keep durable architecture and cross-cutting guides in the consumer's declared documentation folder.
- Update project documentation when a change alters durable or core feature behavior, architecture, data flow, public API, persistence, navigation, localization process, testing workflow, delivery workflow, configuration, or another documented contract.
- Regardless of change size, update or remove existing documentation when the implementation makes a documented statement inaccurate, incomplete, misleading, or obsolete.
- Do not create broad documentation for incidental implementation details that are neither durable knowledge nor already documented. A small change that leaves durable knowledge and existing documentation accurate needs no project-level documentation edit.
- When renaming or removing behavior, search durable documentation for old names, examples, defaults, diagrams, setup steps, and references that may now be stale.
- Keep investigations, temporary plans, and one-time spike notes out of durable documentation unless they become lasting guidance.
- Prefer ASCII diagrams in fenced code blocks when universal rendering matters.

## Review checklist

When reviewing a change, ask:

- Which existing documentation describes the changed feature, API, configuration, workflow, or invariant?
- Does the change alter durable or core feature behavior?
- Would any existing statement become inaccurate, incomplete, misleading, or obsolete even if the implementation change is small?
- Does it introduce a reusable architectural pattern?
- Does it change data flow, ownership, persistence, localization, testing, or delivery?
- Does it remove or supersede an existing guide?
- Are code comments and project guides consistent with the implementation?
- If no documentation changed, is that because no durable knowledge changed and no existing documented claim was affected?

Treat known stale documentation as incomplete implementation. Avoid documentation churn when the change neither affects durable knowledge nor changes an existing documented claim.

## Shared versus local guidance

This repository owns reusable policy. Consumer documentation owns its product domain, concrete paths, package relationships, feature registries, and explicit exceptions. Link across those layers instead of copying shared prose locally.
