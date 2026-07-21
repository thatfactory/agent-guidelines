# Development

## Reusability first

When developing a new feature or responding to a feature request, consider shared code first. If the code fits an existing package, suggest extending that package instead of adding the implementation directly to an application. Also consider whether the change belongs in a new Swift package, even when that package does not exist yet. Prefer reusable, focused package APIs when they can serve more than one consumer.

## Guidelines version

Before changing a project, verify that it uses the latest released version of `agent-guidelines`. Check the project's `AgentGuidelines/VERSION` against the latest release, update the subtree or equivalent when it is behind, and read the updated applicable guides before starting implementation. This check is manual and must be performed at the beginning of each project task.
