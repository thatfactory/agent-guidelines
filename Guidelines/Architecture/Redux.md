# Redux Architecture

Use this guide for applications that explicitly adopt the ThatFactory Redux architecture. Do not apply it to reusable packages or repositories whose local instructions choose another architecture.

## Principles

- Keep one application store as the source of truth for durable application state.
- Views read state and dispatch actions; they do not mutate application state directly.
- Actions describe events or intent, not implementation steps.
- Reducers are pure and synchronous.
- Middleware performs asynchronous work and other side effects.
- Services wrap external frameworks, packages, persistence, clocks, APIs, and system capabilities.
- Selectors derive shared domain information from state.
- Render-ready view state and view-only projections live beside their consuming views.
- Every side-effect result returns to the store as an action before it changes state.

## Data flow

```text
                         await dispatch(Action)
    +--------------+ --------------------------> +-----------+
    | SwiftUI view |                             | Store     |
    |              | <-------------------------- |           |
    +--------------+      observable state       | 1. Reducer|
                                                 | 2. Middle-|
                                                 |    ware   |
                                                 +-----+-----+
                                                       |
                                                       | side effect
                                                       v
                                                +--------------+
                                                | Service      |
                                                | package/API  |
                                                +------+-------+
                                                       |
                                                       | Action?
                                                       v
                                                   Store again
```

The store reduces the original action first, then awaits middleware and sequentially dispatches returned follow-up actions. Keep ordering observable and deterministic. Do not start unstructured work inside reducers or hide state changes inside services.

## Canonical physical folders

These are filesystem folders, not Xcode groups. New single-application repositories use this structure by default:

```text
<AppName>/
|-- App/
|-- Model/
|-- Redux/
|   |-- Action/
|   |-- Middleware/
|   |-- Reducer/
|   |-- Selector/
|   |-- State/
|   `-- Store.swift
|-- Services/
|-- Tools/
|-- View/
|   `-- <Feature>/
`-- Resources/

<AppName>Tests/
|-- Mocks/
|-- Model/
|-- Redux/
|   |-- Action/
|   |-- Middleware/
|   |-- Reducer/
|   |-- Selector/
|   `-- State/
|-- Services/
|-- Tools/
`-- View/
    `-- <Feature>/
```

A multi-target application may use a shared source root such as `Shared/Redux/` and target-specific roots such as `<AppName>/View/`. Its root `AGENTS.md` must provide a concrete path map:

```markdown
| Role | Physical folder |
|---|---|
| Redux | `Shared/Redux/` |
| Models | `Shared/Model/` |
| Services | `Shared/Services/` |
| Views | `<AppName>/View/` |
| Unit tests | `<AppName>Tests/` |
```

Once mapped, use the same component layout beneath those roots. Never guess a destination or create a parallel folder spelling such as `Views/` when the project declares `View/`.

## Placement rules

### App

Put application bootstrap, app delegates, scene definitions, store construction, environment wiring, and root configuration in `App/`. Do not place feature logic there.

### Model

Put reusable domain values in `Model/`. Keep each important type in a focused file. Do not hide response models, payloads, or domain values inside action or service files merely because only one caller currently uses them.

### Action

Put domain action enums in `Redux/Action/`. Use a root routing action that wraps focused feature actions:

```swift
enum AppAction: Equatable {
    case account(AccountAction)
    case navigation(NavigationAction)
}
```

Name actions after what happened or what the user requested. Keep cases in the order required by the project's Swift style guide.

### State

Put the root state and domain sub-states in `Redux/State/`. Prefer focused value types with compiler-synthesized conformances. Add a new sub-state for a durable domain instead of folding unrelated values into an existing feature.

State stores durable facts. Avoid storing values that are cheap, deterministic derivations unless caching is an explicit measured requirement.

### Reducer

Put reducer functions in `Redux/Reducer/`. A reducer receives state and an action and returns new state. It must not:

- perform asynchronous work;
- call services or packages;
- read the clock or generate random values;
- access files, databases, network clients, or system APIs;
- dispatch actions;
- trigger UI behavior directly.

Use the smallest state and action inputs that correctly express the transition. Root reducers compose domain reducers.

### Middleware

Put middleware in `Redux/Middleware/`. Middleware may call injected services and return a follow-up action. It must not mutate store state directly.

Inject services, clocks, identifier generators, and providers through parameters so middleware tests remain deterministic. Register middleware in one root composition file such as `AppMiddlewares.swift`.

Create a feature subfolder when a domain has multiple middleware files:

```text
Redux/Middleware/Account/
|-- AccountMiddleware.swift
|-- LoadAccountMiddleware.swift
`-- UpdateAccountMiddleware.swift
```

### Selector

Put pure, reusable domain extraction in `Redux/Selector/`. A selector may answer questions such as the current signed-in account, whether a capability is enabled, or which domain items are visible.

Do not put SwiftUI types, colors, images, localized display strings, or render-ready screen state in selectors.

### Services

Put focused external-boundary abstractions in `Services/<Capability>/`. Services wrap APIs, persistence, packages, frameworks, sensors, system features, and other impure operations. Middleware calls services; views and reducers do not.

Prefer a protocol or otherwise injectable contract when a service must be replaced in tests. Keep transport-specific details behind the service boundary.

### Tools

Put genuinely cross-cutting implementation utilities in `Tools/`. This is not a miscellaneous folder. Feature-only formatters, helpers, constants, or factories stay beside that feature. Promote them to `Tools/` only after they have a clear cross-feature role.

### View

Put SwiftUI screens and components in `View/<Feature>/`. A new view belongs to the feature it renders, not in Redux. Reusable visual components may use `View/Generic/` or another explicitly declared shared-view folder.

Render-facing view-state types and projections live beside the consuming view:

```text
View/Account/
|-- AccountView.swift
|-- AccountViewState.swift
`-- AccountViewStateProjection.swift
```

If a projection exists only to render one screen, it is view-layer code even when its input is `AppState`.

### Resources

Put catalogs, assets, preview assets, configuration resources, and test plans in `Resources/` or the concrete resource folders declared locally. Production targets must not depend on test fixtures.

## File organization

- Prefer one primary concern per file.
- When a feature has several files of one Redux component, introduce a feature subfolder under that component.
- Keep root routing and composition at the component root; keep feature implementations below it.
- File names match their primary type or clearly describe their primary pure function.
- Do not introduce artificial enum namespaces solely to satisfy filename lint rules.
- Mirror production organization in tests so components are easy to locate.

## SwiftUI connection

Create and inject the store at the application root. Views observe only the state they need and dispatch actions for application events.

Keep view-local interaction state in private `@State` when it is not durable application state. Do not create an `@Observable` view model as a second source of truth for Redux-owned state.

Prefer narrow view inputs or a focused view-state projection. This aligns SwiftUI invalidation with the smallest useful surface while Redux remains the durable source of truth.

## Adding a feature

| Step | Change | Default destination |
|---|---|---|
| 1 | Define domain models | `Model/<Feature>/` |
| 2 | Define feature state | `Redux/State/<Feature>State.swift` |
| 3 | Add it to root state | `Redux/State/AppState.swift` |
| 4 | Define feature actions | `Redux/Action/<Feature>Action.swift` |
| 5 | Route them through the root action | `Redux/Action/AppAction.swift` |
| 6 | Implement the reducer | `Redux/Reducer/<Feature>Reducer.swift` |
| 7 | Compose the reducer | `Redux/Reducer/AppReducer.swift` |
| 8 | Add side effects if needed | `Redux/Middleware/<Feature>/` |
| 9 | Register middleware | `Redux/Middleware/AppMiddlewares.swift` |
| 10 | Add external boundaries if needed | `Services/<Capability>/` |
| 11 | Add shared domain selectors if needed | `Redux/Selector/<Feature>/` |
| 12 | Build the feature UI | `View/<Feature>/` |
| 13 | Mirror tests | `<AppName>Tests/` |

Skip components that provide no value. A state-only transition needs no middleware; a screen-only projection does not need a Redux selector.

## Testing responsibilities

- Reducer tests provide state plus an action and assert the returned state.
- Selector tests provide state and assert the derived domain result.
- Middleware tests inject mocks, execute an action, and assert the returned follow-up action.
- Service tests exercise the external boundary without involving views.
- View-state projection tests live under the matching `Tests/View/<Feature>/` folder.
- Test mocks and fixture data live under the test target's `Mocks/` folder.

Follow [Unit testing](../Testing/UnitTesting.md) for framework and concurrency conventions.
