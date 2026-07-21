# Localization

Follow Apple's [Localizing your app using agents](https://developer.apple.com/documentation/xcode/localizing-your-app-using-agents) workflow and current Xcode localization tools. Consumer repositories declare their supported languages, catalog locations, key conventions, and generated-symbol policy locally.

## Source artifacts

- Use the consumer's existing String Catalogs (`.xcstrings`) as the source of truth.
- Do not create a parallel catalog or migrate an existing `.strings` setup unless the task includes that migration.
- An app target uses its main bundle by default. Swift packages and frameworks must resolve localized resources from their own bundle, using the current Apple-recommended bundle API.
- Keep one source of truth for translator context: either the source comment or the catalog comment.

## User-facing values

- Let SwiftUI's localized string initializers preserve localization context.
- Use `LocalizedStringResource` when a model, view state, notification, or other non-view value carries user-facing text that should resolve later.
- Use `String(localized:)` when a resolved localized `String` is genuinely required outside SwiftUI.
- Use `Text(verbatim:)` for intentional non-localized literals such as debug identifiers.
- Do not pass a runtime `String` to a localized initializer and expect Xcode to extract it as a catalog key.

## Sentences and formatting

- Interpolate values into one localizable sentence rather than concatenating translated fragments.
- Add translator comments for ambiguous language and describe interpolated placeholders by position and meaning.
- Use locale-aware `FormatStyle` APIs for dates, numbers, lists, measurements, and currencies.
- Avoid runtime case transformations for localized interface text; allow translations to choose appropriate casing.

## Layout

- Use leading and trailing instead of left and right for directional layout.
- Avoid fixed text frames that cannot accommodate translation length or script height.
- Prefer semantic text styles to fixed point sizes.
- Use the SwiftUI environment locale for view behavior that must respond to preview or subtree locale overrides.

## Agent workflow

1. Inspect the consumer's local localization instructions and catalogs.
2. Ask Xcode's current documentation or localization capability for the supported workflow.
3. Add or update source-language content and translator context.
4. Update only the languages in scope.
5. Build to validate catalog syntax, extraction, generated symbols, and bundle lookup.
6. Use previews or runtime visual verification for truncation, layout direction, and formatting when relevant.

Do not invent translations from an unrelated project's conventions. Product vocabulary and tone remain consumer-specific.
