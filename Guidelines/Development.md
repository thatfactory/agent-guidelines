# Development

## Reusability first

When developing a new feature or responding to a feature request, consider shared code first. If the code fits an existing package, suggest extending that package instead of adding the implementation directly to an application. Also consider whether the change belongs in a new Swift package, even when that package does not exist yet. Prefer reusable, focused package APIs when they can serve more than one consumer.

## Guidelines version

Before changing a project, verify that it uses the latest released version of `agent-guidelines`. Check the project's `AgentGuidelines/VERSION` against the latest release, update the subtree or equivalent when it is behind, and read the updated applicable guides before starting implementation. This check is manual and must be performed at the beginning of each project task.

## Guidelines changes in pull requests

Keep `AgentGuidelines/` tracked so consumers retain a reproducible, versioned copy for agents and CI. Do not add the subtree to `.gitignore`. Instead, add this rule to the consumer's tracked `.gitattributes` so GitHub collapses synchronized guideline files in pull-request diffs by default while reviewers can still expand them:

```gitattributes
# Synced from thatfactory/agent-guidelines; keep tracked but collapse GitHub diffs.
AgentGuidelines/** linguist-generated
```

Keep each subtree update in its own commit. In the pull-request description, state the old and new guideline versions and link to the central release or pull request where the guideline changes were reviewed. Continue validating the checked-in subtree in CI. Because generated-file diffs are collapsed by default, never edit the subtree locally; make shared changes in the source repository and consume a tagged release.

## Logging

Applications own their orchestration, lifecycle, and product-domain diagnostics. Follow the shared [logging guide](Logging.md) and rely on each dependency to log its own implementation. Do not duplicate or reformat package-internal operations in the application log.
