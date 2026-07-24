# Swift Format

- Treat formatting and lint rules as readability and correctness tools, not as architecture.
- Use the shared configuration under `Configurations/Swift/`; consumers expose it through root `.swift-format` and `.editorconfig` symlinks so Xcode, local commands, and CI agree. Configuration discovery is hierarchical, while an explicit `--configuration` path is unconditional.
- In Xcode, use **Editor > Structure > Format File with 'swift-format'** (or the corresponding selection command) when you want to rewrite source.
- Run `AgentGuidelines/Scripts/swift_format.sh format <paths...>` explicitly to rewrite source. Do not format source files from an Xcode build phase.
- Run `AgentGuidelines/Scripts/swift_format.sh lint <paths...>` for non-blocking local warnings and `lint-strict` for errors that block CI.
- Fix findings introduced by a change. Formatter-supported rules are corrected by `format`; linter-only rules require a source change.
- Prefer a focused `// swift-format-ignore: RuleName` immediately before the affected declaration or statement when a rule conflicts with required semantics. Add a short preceding comment explaining why.
- Do not ignore a whole file or disable a shared rule to avoid fixing one occurrence.
- When the supported Xcode toolchain changes, regenerate the exhaustive configuration with `xcrun swift-format dump-configuration`, reapply the documented Xcode-aligned values, review the resulting policy change, and release it centrally before consumer adoption.

See swift-format's [configuration](https://github.com/swiftlang/swift-format/blob/main/Documentation/Configuration.md) and [focused suppression](https://github.com/swiftlang/swift-format/blob/main/Documentation/IgnoringSource.md) documentation for the underlying behavior.
