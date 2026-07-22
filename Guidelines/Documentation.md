# Documentation

- Use PascalCase Markdown filenames without spaces.
- Keep the folder flat until one topic genuinely requires several files.
- Prefer current implementation over speculative future design; label known gaps explicitly.

## Code-level documentation

- Document structs, classes, enums, protocols, actors, and other significant types with focused `///` DocC comments.
- Update documentation when changing a documented API, parameter, behavior, or invariant.
- End documentation sentences with periods.
- Explain intent, contracts, units, side effects, isolation, and non-obvious constraints; do not restate syntax.
- Add a short Swift example when it materially clarifies correct use.
- Keep documentation close to the declaration it describes.

## Project-level documentation

- Keep durable architecture and cross-cutting guides in the consumer's declared documentation folder.
- Update a guide when a change alters the documented architecture, data flow, public API, persistence, navigation, localization process, testing workflow, or delivery workflow.
- Do not update broad guides for minor implementation changes already explained by code and DocC.
- Remove or rewrite stale documentation when its feature or workflow is removed.
- Keep investigations, temporary plans, and one-time spike notes out of durable documentation unless they become lasting guidance.
- Prefer ASCII diagrams in fenced code blocks when universal rendering matters.

## Review checklist

When reviewing a change, ask:

- Does it alter a documented public API or invariant?
- Does it introduce a reusable architectural pattern?
- Does it change data flow, ownership, persistence, localization, testing, or delivery?
- Does it remove or supersede an existing guide?
- Are code comments and project guides consistent with the implementation?

Flag missing documentation only when the change affects durable knowledge. Avoid documentation churn for small fixes.

## Shared versus local guidance

This repository owns reusable policy. Consumer documentation owns its product domain, concrete paths, package relationships, feature registries, and explicit exceptions. Link across those layers instead of copying shared prose locally.
