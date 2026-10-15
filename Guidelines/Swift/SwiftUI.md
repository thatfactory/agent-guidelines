# SwiftUI

Use official Apple documentation and Xcode's current SwiftUI skills for API-specific behavior. This guide captures stable project policy rather than reproducing the current SDK's API catalog.

## View structure

- Put SwiftUI dynamic properties such as `@Environment`, `@Query`, `@State`, and `@Binding` before ordinary stored `let` and `var` properties. Keep injected environment dependencies before locally owned state when both are present.
- Keep a parent view focused on composition.
- Model meaningful sections such as headers, lists, metadata, sidebars, and footers as separate `View` types with narrow inputs.
- Keep each independently meaningful `View` in its own file, including private supporting views. Give every view its own deterministic preview when the required dependencies can be represented safely; when they cannot, document the concrete limitation in the handoff.
- Do not extract sections into computed `some View` properties merely to shorten `body`; computed properties remain in the parent's invalidation boundary.
- Tiny fragments reused within one body may use a small helper when they have no independent state, input, or invalidation story.
- Keep view initializers cheap. Do not decode data, access files, build large structures, or allocate formatters in `init`.
- Avoid a single-child `Group` that adds no structure or behavior.

## Data flow

- Pass a view only the value-type fields it reads or forwards.
- Use private `@State` for state genuinely owned by the view.
- Use `Binding` when a child edits state owned by its parent.
- In non-Redux designs, prefer `@Observable` to `ObservableObject` for new shared reference models when platform support allows it.
- In Redux applications, keep durable app and domain state in Redux. Do not introduce an observable view model as a parallel source of truth.
- Make observable stored-property types `Equatable` when equality matches their semantics, allowing redundant assignments to avoid unnecessary invalidation.
- Isolate side effects in `.task`, `.onChange`, actions, or explicit async functions rather than hiding them in rendering logic.
- Use the current `.onChange(of:)` form and read the updated captured value when the previous value is unnecessary.
- Avoid closure-based bindings when a writable key-path binding expresses the same relationship.

With SDKs where `@State` is a macro, do not give a state property a declaration default and then attempt to replace that value in `init`. Choose one initialization source and verify current compiler guidance when migrating existing code.

## Collections and identity

- Give `ForEach`, `List`, `Table`, and similar data-driven views stable, unique element identity.
- Prefer meaningful `Identifiable` conformance when the model has natural identity.
- Do not use collection indices, offsets, or transient UUIDs as identity for mutable collections.
- Do not sort, filter, or map large collections inline inside a frequently evaluated view body. Prepare the collection before rendering.
- Use a dedicated row `View` for meaningful rows and pass it narrow inputs.
- Avoid `AnyView` in collection rows.

## Modifiers and environment

- Preserve stable view identity. Prefer modifiers whose values change over conditionally adding and removing modifier branches.
- Do not place high-frequency values in the environment when explicit narrow inputs work.
- Avoid unstable environment defaults and freshly created closures that invalidate large subtrees.
- Do not hide unstable values behind fake `Equatable` implementations.

## Scrolling

- Apply `.scrollBounceBehavior(.basedOnSize)` to new or changed `ScrollView` instances on supported deployment targets, especially inside modally presented sheets. Content that fits should stay still; content that exceeds the viewport can still scroll and bounce.
- Match the modifier's `axes` to the scroll view. The default affects only the vertical axis, so specify `.horizontal` for horizontal scrolling and both axes when needed.
- Keep the modifier on the intended scroll view or its narrowest suitable container. The setting propagates through the environment to descendant scrollable views, so check nested scrolling before applying it to a broader hierarchy.
- Preserve a different bounce behavior only when the supported interaction requires it, and record that reason in consumer guidance. Check Apple API availability for the consumer's deployment targets before applying the modifier.

## Modern APIs and scope

- Do not introduce APIs that current Xcode documentation identifies as deprecated or soft-deprecated.
- When fixing a feature, modernize only the code directly required by the task unless the user requests a broader migration.
- For SDK-sensitive features, search current Apple documentation through Xcode rather than relying on remembered signatures.
- Apply the current Xcode SwiftUI skill when a new SDK changes source behavior, builder resolution, state initialization, or modifier availability.

## Native components and presentation

- Prefer native SwiftUI or platform controls and presentation APIs whenever they express the supported interaction. Evaluate sheets, alerts, confirmation dialogs, navigation, menus, pickers, popovers, and similar components before implementing an equivalent. Consult official Apple/Xcode documentation for behavior and availability on the current deployment target, following [documentation lookup](../Xcode/MCP.md#documentation-lookup).
- Keep branded content and styling inside native components. Custom fonts, button styles, and content inside a native sheet are compatible with this policy when the system retains presentation and dismissal ownership.
- Do not substitute a sheet-shaped `ZStack`, offset animation, or custom scrim for a suitable native sheet API. The same rule applies to other simulated system components, including custom discard dialogs. Pixel fidelity to a static design and preserving mounted state are insufficient reasons to replace native presentation behavior; a mockup is not approval for an exception.
- Use a custom equivalent only for an actual native capability gap verified against the supported platform and deployment target. Before implementation, obtain explicit repository-owner approval and record a durable exception in consumer documentation: the required interaction, evaluated native alternatives, concrete missing capability and documentation or reproducible evidence, approved scope, lifecycle ownership, compensating validation, and revisit condition. Do not invent a capability gap or infer approval from existing custom code. An unapproved or undocumented replacement blocks completion.

### Presentation ownership

- Present from the active hierarchy. When a child presentation launches a system picker or editor, attach that presentation to the active child hierarchy rather than an obscured ancestor or unrelated host.
- Give each child independent dismissal. Read the dismissal action in the child's presentation environment or use its own presentation binding; do not route a child close button or downward dismissal gesture to the parent editor. Keep parent-owned draft state alive across child presentation and dismissal without committing or discarding it implicitly.
- Make cancellation idempotent across explicit cancel, interactive dismissal, parent dismissal, and asynchronous callbacks. Cancel owned work and reject stale completions after dismissal or replacement so an old result cannot mutate a retained draft or a later presentation.
- Perform cleanup that depends on completed dismissal through the presentation's dismissal-completion callback, such as `onDismiss`, rather than treating a dismiss request, animation delay, or arbitrary disappearance as proof of completion. Coordinate cleanup with cancellation so repeated callbacks cannot clear parent state or a newer child session.

### Required interaction evidence

For changed native presentations and approved custom equivalents, exercise the supported lifecycle on a simulator or device using [runtime interaction and reporting](../Xcode/MCP.md#build-run-and-interaction). Record the platform, scenario, action, observed outcome, and relevant hierarchy or visual evidence:

- Verify presentation and dismissal animation/dimming, supported interactive dismissal and gesture routing, and parent survival with draft retention. If interactive dismissal is intentionally disabled, verify the restriction and the explicit exit path. Exercise reopening and repeated cancellation.
- Launch and dismiss any nested system picker or editor from the active child; confirm the expected presentation remains active after each exit.
- Inspect safe areas, controls and shadow clipping, keyboard/focus restoration, and relevant Dynamic Type and localization layouts during the flow.
- Exercise asynchronous cancellation and stale completion after dismissal or replacement when work can outlive the presentation; use deterministic tests where they improve coverage of these races alongside runtime interaction.

A static screenshot or a no-op automation call is not evidence that gestures work. Require an actual gesture and its observed result, or recorded manual verification when automation cannot exercise it. Missing relevant runtime evidence blocks completion; report the exact unverified behavior instead of claiming the lifecycle passed.

Use these decisions when auditing an implementation:

| Decision | Audit outcome |
| --- | --- |
| Simulated sheet with a suitable native API and no approved durable exception | Blocked |
| Native nested sheet with branded content, correct ownership, and required interaction evidence | Accepted |
| Custom equivalent for a verified capability gap with owner approval, durable exception, and compensating evidence | Accepted within the approved scope |
| Presentation with missing relevant runtime evidence | Blocked |

## Animation

- Use native SwiftUI animation to make apps fluid rather than static. Apply it purposefully to buttons, transitions, interactions, selection, colors, and other visible state changes that benefit from feedback; do not animate every update or add motion for its own sake.
- Prefer the default SwiftUI animation, using `withAnimation { ... }` or `.animation(.default, value: ...)`, unless the task prompt explicitly requests a specific animation. Prefer system-provided transitions and SF Symbol effects when they fit the interaction instead of recreating them with custom timing, curves, or rendering.
- Scope animation to the relevant state change or view. Preserve responsive controls, stable layout, and uninterrupted user interaction; avoid blanket animations that also animate unrelated state changes.
- Do not introduce app-level Reduce Motion guards unless the task prompt explicitly requests them. This includes reading `accessibilityReduceMotion` to replace animation with `nil`, remove symbol effects, or otherwise suppress app-authored animation. Preserve any accessibility behavior provided automatically by native system components; this policy governs additional app-level overrides.

## Previews

- Put previews at the end of the file under `// MARK: - Preview`.
- Use `#Preview`.
- Use `@Previewable` for interactive preview state when appropriate.
- Keep preview fixtures deterministic and lightweight.
- After UI changes, follow [Xcode MCP and visual verification](../Xcode/MCP.md) when runtime verification adds meaningful confidence.

## Localization

Follow [Localization](../Localization.md) for user-facing text, layout direction, formatting, and package bundles.
