# User Experience

Preserve the user's intent, work, and sense of place. Automatic work must serve a current need without making the user manage the application's housekeeping. Apply this guide to app and game interfaces regardless of implementation framework; use [Animations](Animations.md) for motion quality and [SwiftUI](../Swift/SwiftUI.md) for implementation policy.

These are ThatFactory experience requirements, informed by Apple's [launching](https://developer.apple.com/design/human-interface-guidelines/launching) and [loading](https://developer.apple.com/design/human-interface-guidelines/loading) guidance. Product-specific freshness requirements and necessary interruptions belong in durable consumer documentation.

## Preserve the current task

- Returning from another app should resume the current task. Preserve the active editor or presentation, unsaved input, selection, navigation, and relevant scroll and focus context. A brief app switch to copy information is part of that task, not a request to start over.
- Foreground activation alone does not justify dismissing a flow, returning to a root screen, covering usable content with loading UI, or taking input focus. Retaining the draft underneath an unnecessary overlay still interrupts the user.
- Distinguish a temporary absence from initial loading, a new user request, and an actual change that invalidates access or makes continuing unsafe. Do not replay the startup experience on every activation.
- When interruption is necessary, limit it to the affected task, explain the reason and recovery path, and preserve recoverable work where safe. Genuine account changes, revoked access, and unsafe or invalid data must still be handled promptly; continuity never authorizes exposing another account's content or committing invalid work.

## Perform automatic work for a current reason

- Identify the trigger, the current need, and the user-visible effect of each automatic refresh or reload. A lifecycle callback is an opportunity to assess that need, not proof that a disruptive reload is required.
- Prefer quiet, nonblocking updates when they can preserve the current task and valid content. Do not replace usable content with a startup or full-screen loading state merely because a routine refresh is in progress. A background operation that unexpectedly replaces a draft, moves the user's location, or steals focus is still disruptive.
- For an opportunistic foreground refresh that would disturb an active task, skip that attempt when the user is busy. Do not queue it for replay when an editor, chooser, search, settings, or another flow closes. Finishing or cancelling a task is not, by itself, a new refresh request.
- Reassess at a new independent trigger, such as a later eligible foreground activation, an explicit refresh, or a relevant data change. A save or deletion can legitimately synchronize the mutation it just made; it does not justify replaying an unrelated skipped refresh.
- Defer required work only when it remains necessary for a concrete operation or documented freshness requirement. Record why it cannot be skipped, when it becomes eligible, how its need is rechecked, and what the user will experience. Do not invent deferred work merely to ensure that every lifecycle event eventually causes a reload.
- Reassess before showing loading UI or publishing a disruptive result if the user has started another task since the work began. An earlier idle state does not authorize interrupting a newly opened editor or presentation.

## Make waiting proportionate and understandable

- Show blocking loading UI only when the affected task cannot safely continue without the result. Keep unaffected content and actions available when possible, and make clear what is loading.
- Scope progress, failure, and retry to the operation that needs them. Do not turn a routine refresh failure into an unrelated modal interruption when the current task can continue safely.
- Preserve valid user context through completion and failure. Avoid surprise loading screens after dismissal, duplicate reloads for the same need, and artificial waits added only to make an animation or loading screen visible.

## Acceptance scenarios

Exercise the changed paths and directly affected flows. Record the platform/OS, app revision, initial state, trigger, actions, and observed result. Use runtime interaction for continuity and visible loading, with deterministic tests or event evidence where needed to distinguish a skipped request from a silently deferred one. Static screenshots cannot establish continuity across an interruption.

| Scenario | Required outcome |
| --- | --- |
| Switch away with unsaved edits, then return | The editor and draft remain usable without an unnecessary overlay or navigation reset |
| Switch away while entering a value or choosing options, then return | Input, selection, presentation, and relevant focus context survive |
| Routine foreground refresh is skipped during a task; then save, cancel, or dismiss it | No catch-up refresh is caused solely by closing the flow; any mutation synchronization has its own reason |
| A later eligible activation or explicit refresh occurs | Freshness is reassessed for that new trigger; a valid refresh can proceed |
| An automatic refresh begins while idle; the user then opens an editor | Completion or loading UI does not displace the new task |
| Access is actually revoked or the active account changes | Unsafe access stops promptly, with an appropriate explanation and safe handling of recoverable work |

An unnecessary interruption, an unjustified catch-up refresh, lost task context, or missing applicable evidence prevents [audit completion](../../.agents/skills/agent-guidelines-audit/SKILL.md#audit-user-experience). Documentation-only policy work uses scenario walkthroughs; it does not establish compliance in a consumer application.
