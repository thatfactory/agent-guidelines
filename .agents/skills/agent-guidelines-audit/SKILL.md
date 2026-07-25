---
name: agent-guidelines-audit
description: Audit completed repository work against the consumer's applicable agent-guidelines, local AGENTS.md instructions, requested scope, and declared validation workflow. Use after implementing changes and before claiming completion, handing work to the user, preparing, opening, or updating a pull request, declaring merge readiness, or preparing a release. Do not use for simple answers, read-only exploration, or work that is still actively being implemented.
---

# Agent Guidelines Audit

Perform a final, evidence-based compliance pass. Treat the applicable guidelines and local instructions as the source of truth; do not duplicate their full content in this skill.

## Establish the audit scope

1. Re-read the user request and list every requested outcome and explicit constraint.
2. Locate the repository root and every applicable `AGENTS.md` from the current directory to that root.
3. Read the shared guides referenced by those instructions that apply to the changed files and workflow.
4. Inspect `git status`, the complete diff, and relevant untracked files. Preserve unrelated user changes.
5. Check the consumer's `AgentGuidelines/VERSION` and provenance when the task changes or depends on the synchronized subtree. Do not update it implicitly.

## Audit the implementation

Review the actual change rather than only checking whether files exist:

- Confirm every requested outcome is implemented and no material behavior was dropped.
- Confirm physical folders, familiar domain grouping, filenames, declaration order, type ownership, namespacing, documentation, and `MARK` organization follow the applicable guides. Distinguish values that describe data from tools that primarily execute algorithms or accumulate behavior.
- For Redux applications, trace actions, state, reducers, middleware, services, tools, presentation models, views, and side-effect results through the complete data flow. Confirm each Redux component folder contains only that component type.
- Check that framework objects, persistence, logging, and asynchronous work remain in their allowed boundaries.
- Check SwiftUI composition, narrow inputs, local versus durable state, localization, accessibility, and safe deterministic previews where applicable.
- Check tests for the required framework, mirrored paths, shared tags, Given/When/Then structure, deterministic seams, and coverage of changed behavior and failure paths.
- Check logging ownership, subsystem, categories, emoji, privacy, severity, metadata stability, and noise controls when logging changed.
- Check durable documentation, package configuration, CI/CD, Xcode project configuration, security-sensitive changes, and physical-device limitations when they are in scope. Compare documented Swift and concurrency settings with the effective application and test-target settings; flag both redundant isolation annotations and missing annotations at compiler-verified boundaries.
- Search for stale type names, superseded files, direct APIs forbidden by the new architecture, empty folders, and references to removed behavior.

## Validate the evidence

Run the repository's declared non-destructive checks in proportion to the change:

- formatter and strict lint;
- focused tests, followed by the declared broader test plan when warranted;
- relevant builds or package validation;
- repository-specific validators;
- `git diff --check`.

Use fresh successful evidence already produced in the same task instead of rerunning expensive checks without reason. Distinguish automated compilation and simulator evidence from hardware, signing, deployment, or manual validation that automation cannot prove.

## Resolve findings

- When the user authorized implementation, fix safe in-scope findings and rerun the affected checks.
- For review-only work, report findings without modifying code.
- Do not broaden the feature, rewrite unrelated files, edit a synchronized `AgentGuidelines/` subtree, or perform commits, pushes, pull requests, merges, tags, or releases without the required authority.
- Treat an unresolved required guideline violation or missing relevant validation as a blocker to claiming completion.

## Hand off

Summarize:

- the instruction and guideline areas audited;
- findings fixed during the audit;
- validation commands and outcomes;
- any deliberate deviations, unavailable evidence, or remaining blockers.

Do not say the work is done merely because the audit ran. Say it is ready only when the requested outcome is complete and the relevant evidence passes.
