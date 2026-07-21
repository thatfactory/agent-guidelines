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

Example:

```swift
guard isEnabled else {
    return
}

withAnimation {
    isPresented = true
}
```
