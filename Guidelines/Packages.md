# Swift Packages

## Package boundaries

- Keep a reusable package focused on one coherent capability.
- Prefer UI-agnostic domain APIs unless UI is the package's explicit purpose.
- Do not add application Redux, navigation, persistence, or product policy to a generic package.
- Keep public APIs minimal and stable. Prefer composing focused types over introducing umbrella abstractions before multiple consumers need them.
- Declare platform and Swift toolchain requirements explicitly in `Package.swift`.
- Put sources under `Sources/<Target>/` and tests under `Tests/<Target>Tests/`.
- Keep resources in the target that owns them and use the package bundle for lookup.

## Development workflow

1. Read the package's local `AGENTS.md`, README, DocC, and public API before changing behavior.
2. Add or update tests in the package itself.
3. Update DocC and README examples when public behavior changes.
4. Run the focused tests, then `swift test` or the package's declared Xcode test workflow.
5. Integrate the package into a consumer locally only when consumer behavior must also be verified.
6. Avoid committing consumer-specific workarounds into the package when the behavior belongs in the consumer.

## Local integration

- Use Xcode's local-package workflow or an explicit temporary local dependency while developing package and consumer changes together.
- Do not commit machine-specific absolute package paths.
- Before release, restore the consumer to the tagged remote dependency unless its local instructions intentionally retain a monorepo relationship.
- Verify the final remote version resolves on a clean checkout.

## Releases

For ThatFactory packages, “release a new version” means:

1. Choose a semantic version appropriate to compatibility.
2. Update public documentation and release notes.
3. Run the declared CI/test workflow.
4. Commit the release state.
5. Create and push the matching Git tag.
6. Create a GitHub release for that tag.
7. Use real multiline release notes and backticks around technical names and versions.

When using a CLI, pass multiline notes through a file so GitHub renders line breaks correctly.

## Consumer updates

- Review package release notes and API changes before updating.
- Update one dependency relationship intentionally; do not rewrite unrelated resolved versions.
- Build and test the affected consumer behavior.
- Update the consumer's package integration documentation when roles, mappings, or workflows change.
