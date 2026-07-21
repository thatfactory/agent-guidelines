# Swift

## Language and SDK guidance

- Use the Swift language and platform versions declared by the consumer repository.
- Use current official Apple documentation through Xcode documentation search when API behavior or availability matters.
- Use current `swift-collections` documentation when working with its collection types.
- Import the module that owns an API. For example, APIs specific to `OrderedCollections` require `import OrderedCollections`.
- Maintain a zero-warning policy for warnings introduced by the change.

## Implementation

- Prefer concise, readable, maintainable code over clever abstractions.
- Prefer structured concurrency with `async`/`await`, task groups, actors, and `Task` where appropriate.
- Do not introduce `DispatchQueue.async` as a substitute for structured concurrency.
- Respect strict concurrency and the repository's default actor isolation.
- Prefer compiler-synthesized `Codable`, `Equatable`, `Hashable`, and `Sendable` conformances when their semantics are correct.
- Write manual serialization, equality, or hashing only when a documented requirement prevents synthesis.
- Import the narrowest framework the file requires. Models should not import SwiftUI merely to gain transitive access to Foundation types.
- A new Swift file must contain at least one required import; use `import Foundation` when it otherwise needs no module.

## State and isolation

- Treat actor isolation as part of an API's contract.
- Mark UI-bound reference models `@MainActor` unless the target's default actor isolation already provides it.
- Avoid adding `@MainActor` to tests or domain types merely to silence a diagnostic. Resolve the actual isolation boundary.
- Use `Sendable` where values cross concurrency domains and their stored values support it.

## C-family interoperability

When a target exposes or consumes C, Objective-C, or C++ interfaces, use Xcode's current `adopt-c-bounds-safety` skill and official compiler documentation for that scoped work. Do not apply C bounds-safety rules to pure Swift targets.

## Documentation

Follow [Swift style](SwiftStyle.md) for source formatting and [Documentation](../Documentation.md) for DocC and project-level guidance.
