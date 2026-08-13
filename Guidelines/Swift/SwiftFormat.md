# Swift Format

## Workflow

- Treat formatting and lint rules as readability and correctness tools, not as architecture.
- Use the shared configuration under `Configurations/Swift/`; consumers expose it through root `.swift-format` and `.editorconfig` symlinks so Xcode, local commands, and CI agree. Configuration discovery is hierarchical, while an explicit `--configuration` path is unconditional.
- In Xcode, use **Editor > Structure > Format File with 'swift-format'** (or the corresponding selection command) when you want to rewrite source.
- After changing Swift source, humans and agents run `AgentGuidelines/Scripts/swift_format.sh format-and-lint <paths...>` before handoff. Do this even when a later build would provide the same safety net.
- Run `AgentGuidelines/Scripts/swift_format.sh format <paths...>` when only rewriting source is required.
- Run `AgentGuidelines/Scripts/swift_format.sh lint <paths...>` for non-blocking local warnings and `lint-strict` for errors that block CI.
- Fix findings introduced by a change. Formatter-supported rules are corrected by `format`; linter-only rules require a source change.

## Xcode build integration

- Add a **Swift Format** run-script phase to every independently buildable app or test target that compiles Swift source. Place it before **Compile Sources** so compilation consumes the formatted files.
- Skip the phase when `CI=true`; CI must remain non-mutating and run `lint-strict` in one dedicated job.
- Invoke `AgentGuidelines/Scripts/swift_format.sh format-and-lint` only over source folders compiled by that target, including shared folders it consumes. Exclude unrelated app and test sources so an invalid file outside the selected build cannot block compilation.
- Run the phase on every build rather than using dependency analysis. A no-op formatting pass is intentionally cheaper than allowing locally generated formatting debt.
- Source mutation requires either declared source inputs and outputs or disabling Xcode's **User Script Sandboxing** for the affected configurations. Record and review that choice locally; never disable sandboxing without the formatting phase requiring it.
- Validate the integration in Xcode with an open, deliberately misformatted file. Confirm formatting happens before compilation and that editor saving, cursor state, and undo behavior remain acceptable.

## Shared customizations

The checked-in configuration starts from the exhaustive Xcode toolchain dump. These deliberate overrides are the shared policy and must be reapplied when the toolchain changes.

### Xcode-aligned layout

- `indentation`: 4 spaces
- `tabWidth`: 4
- `lineLength`: 120
- `indentSwitchCaseLabels`: `false`
- Swift-only EditorConfig settings mirror indentation, line length, LF newlines, final newlines, and trailing-whitespace cleanup.

### Rules enabled beyond the dumped defaults

- `AlwaysUseLiteralForEmptyCollectionInit`: keeps empty arrays concise and replaces the relevant SwiftLint array/empty-collection checks.
- `NeverUseForceTry`: retains a production safety check; swift-format exempts supported test code.
- `NoEmptyLinesOpeningClosingBraces`: replaces SwiftLint's opening- and closing-brace vertical-whitespace checks.
- `UseWhereClausesInForLoops`: preserves the former SwiftLint `for_where` behavior.
- `ValidateDocumentationComments`: validates documentation already present, including parameter coverage after signature changes, without requiring every declaration to be documented.
- `includeConditionalImports`: sorts imports inside conditional-compilation blocks together with ordinary imports.

Rules not listed here retain the exhaustive Xcode dump values. In particular, universal public documentation, force-unwrap rejection, implicit-return rewriting, early-exit rewriting, leading-underscore rejection, and implicitly unwrapped optional rejection remain disabled until adopted deliberately. swift-format has no equivalent for repository-specific import bans or sorted enum cases.

Declaration layout rules from [Swift style](SwiftStyle.md), including keeping modifiers on the declaration line and preserving an intentionally multiline signature, remain review-guided. The formatter preserves a correctly authored layout, but it has no focused rule that forces those shapes; disabling `respectsExistingLineBreaks` would broadly reflow otherwise intentional source formatting.

## Focused exceptions

- Prefer a focused `// swift-format-ignore: RuleName` immediately before the affected declaration or statement when a rule conflicts with required semantics. Add a short preceding comment explaining why.
- Do not ignore a whole file or disable a shared rule to avoid fixing one occurrence.

## Toolchain updates

- When the supported Xcode toolchain changes, regenerate the exhaustive configuration with `xcrun swift-format dump-configuration`, reapply the documented Xcode-aligned values, review the resulting policy change, and release it centrally before consumer adoption.

See swift-format's [configuration](https://github.com/swiftlang/swift-format/blob/main/Documentation/Configuration.md), [rule](https://github.com/swiftlang/swift-format/blob/main/Documentation/RuleDocumentation.md), and [focused suppression](https://github.com/swiftlang/swift-format/blob/main/Documentation/IgnoringSource.md) documentation for the underlying behavior.
