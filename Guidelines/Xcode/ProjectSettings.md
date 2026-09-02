# Xcode Project Settings

Use Apple's [Build settings reference](https://developer.apple.com/documentation/xcode/build-settings-reference) for the current setting names and behavior. Apply this baseline to every checked-in Xcode project.

## Project-level ownership

Define the required settings in every project build configuration so application, extension, framework, unit-test, UI-test, and other targets inherit one baseline. An `.xcconfig` counts as project-level ownership only when the project's build configurations reference it; a target-only configuration does not.

Do not satisfy this policy with repeated target-level values. Remove redundant target copies so inheritance remains visible. A target may override a project value only under a documented exception that names that target and setting.

## Required baseline

Set all warning policies to `YES`:

- `GCC_TREAT_WARNINGS_AS_ERRORS`
- `MTL_TREAT_WARNINGS_AS_ERRORS`
- `SWIFT_TREAT_WARNINGS_AS_ERRORS`

Set the concurrency baseline:

- `SWIFT_APPROACHABLE_CONCURRENCY = YES`
- `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`
- `SWIFT_STRICT_CONCURRENCY = complete`

Set `SWIFT_VERSION` to the newest stable Swift language mode supported by the selected Xcode. The current language mode is Swift 6, serialized as `SWIFT_VERSION = 6.0`; move to 7, 8, 9, and later stable modes when their supporting Xcode releases are adopted. Do not confuse the compiler's minor release, such as Swift 6.4, with the Swift language mode.

Enable every build setting exposed by the selected Xcode whose name begins with `SWIFT_UPCOMING_FEATURE_`. `SWIFT_APPROACHABLE_CONCURRENCY` enables a subset of concurrency features but does not replace the explicit upcoming-feature settings. Keep an exposed setting explicitly enabled even when the current language mode enables that behavior implicitly, so the project contract remains visible.

The Xcode 27 baseline is:

- `SWIFT_UPCOMING_FEATURE_CONCISE_MAGIC_FILE = YES`
- `SWIFT_UPCOMING_FEATURE_DEPRECATE_APPLICATION_MAIN = YES`
- `SWIFT_UPCOMING_FEATURE_DISABLE_OUTWARD_ACTOR_ISOLATION = YES`
- `SWIFT_UPCOMING_FEATURE_DYNAMIC_ACTOR_ISOLATION = YES`
- `SWIFT_UPCOMING_FEATURE_EXISTENTIAL_ANY = YES`
- `SWIFT_UPCOMING_FEATURE_FORWARD_TRAILING_CLOSURES = YES`
- `SWIFT_UPCOMING_FEATURE_GLOBAL_ACTOR_ISOLATED_TYPES_USABILITY = YES`
- `SWIFT_UPCOMING_FEATURE_GLOBAL_CONCURRENCY = YES`
- `SWIFT_UPCOMING_FEATURE_IMPLICIT_OPEN_EXISTENTIALS = YES`
- `SWIFT_UPCOMING_FEATURE_IMPORT_OBJC_FORWARD_DECLS = YES`
- `SWIFT_UPCOMING_FEATURE_INFER_ISOLATED_CONFORMANCES = YES`
- `SWIFT_UPCOMING_FEATURE_INFER_SENDABLE_FROM_CAPTURES = YES`
- `SWIFT_UPCOMING_FEATURE_INTERNAL_IMPORTS_BY_DEFAULT = YES`
- `SWIFT_UPCOMING_FEATURE_ISOLATED_DEFAULT_VALUES = YES`
- `SWIFT_UPCOMING_FEATURE_MEMBER_IMPORT_VISIBILITY = YES`
- `SWIFT_UPCOMING_FEATURE_NONFROZEN_ENUM_EXHAUSTIVITY = YES`
- `SWIFT_UPCOMING_FEATURE_NONISOLATED_NONSENDING_BY_DEFAULT = YES`
- `SWIFT_UPCOMING_FEATURE_REGION_BASED_ISOLATION = YES`

Treat this list as a minimum for Xcode 27, not a permanent exhaustive list. When adopting a newer Xcode, compare its build settings with this prefix and add any newly exposed setting to every project configuration.

## Audit procedure

1. Identify the selected Xcode version and its newest stable Swift language mode.
2. Inspect the `PBXProject` build configurations and any project-level `.xcconfig` files. Confirm every Debug, Release, and custom configuration defines the complete baseline.
3. Compare the active Xcode's build settings with the `SWIFT_UPCOMING_FEATURE_` prefix so newly introduced settings are not missed.
4. Enumerate every target, including unit-test and UI-test targets, and every supported configuration. Use Xcode project-aware tooling or `xcodebuild -showBuildSettings` to verify the effective values.
5. Inspect target build configurations for redundant copies, disabling values, or overrides. Remove redundant copies and resolve undocumented overrides.
6. Build the relevant configurations and treat every warning as a failure unless an applicable documented exception explicitly covers the setting that would otherwise promote it.

## Exceptions

An incompatible project or target requirement may specialize one or more settings only when the nearest applicable `AGENTS.md`, or durable project documentation linked from it, records:

- each exact setting name;
- the affected project, configurations, and targets;
- the concrete requirement that prevents the baseline value;
- the replacement value or omitted setting and its engineering impact;
- compensating validation where relevant; and
- the condition for removing or revisiting the exception.

The audit accepts an applicable documented exception and reports the deviation without failing the project for that setting. A transient discussion, generic statement that a project uses different settings, or the existing target configuration by itself is not an exception.
