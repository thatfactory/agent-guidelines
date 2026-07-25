# Swift Style

- Keep conditional, loop, and closure bodies on separate lines.
- Keep `guard` exits on separate lines.
- Prefer seconds-based duration APIs such as `Task.sleep(for: .seconds(10))` over nanosecond literals.
- Use `///` for documentation comments and end documentation sentences with periods.
- Use meaningful names of at least three characters. Widely established type-level conventions are allowed only when the consumer explicitly uses them.
- Keep enum cases alphabetical unless ordering communicates behavior or a local lint suppression documents the exception.
- Use `// MARK: -` to separate meaningful sections.
- Use `// MARK: - Private` when separating private implementation from non-private declarations in the same file.
- Do not add Xcode boilerplate filename, author, or creation-date headers.
- Prefer one primary type or concern per file.
- Match a type file's name to its primary type.
- Put the declaration named by the file immediately after imports and file-level directives. Opening `EffectAssetLoader.swift`, for example, must reveal `EffectAssetLoader` before supporting declarations. A shared canonical template may retain type aliases that its documented layout deliberately places first.
- Put a supporting type used only by one primary type inside an extension of that primary type when the relationship forms a natural namespace. Put a supporting type used by other files in its own named file instead.
- Keep physical folders flat until one topic genuinely contains several files. When grouping becomes useful, organize related models, services, tools, views, and Redux components by a familiar domain, feature, or capability so readers can reason about them together.

Example:

```swift
guard isEnabled else {
    return
}

withAnimation {
    isPresented = true
}
```

Namespaced supporting types keep their ownership visible:

```swift
struct Measurement {
    // ...
}

// MARK: - Errors

extension Measurement {
    enum ValidationError: Error {
        case invalidValue
    }
}
```
