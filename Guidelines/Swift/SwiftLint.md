# SwiftLint

- Treat lint rules as readability and correctness tools, not as architecture.
- Fix warnings introduced by a change.
- Do not add enum namespaces, empty wrapper types, or other artificial structures solely to satisfy filename rules for pure-function files such as reducers, selectors, or middleware.
- Prefer a focused local disable with a short reason when a rule conflicts with the intended design.
- Do not disable a rule repository-wide to avoid fixing one occurrence.
- Keep the lint configuration aligned with the physical folder organization and generated-file exclusions of the consumer repository.
