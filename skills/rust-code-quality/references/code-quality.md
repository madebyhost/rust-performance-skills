# Rust Code Quality Reference

## API Design

- Follow the Rust API Guidelines as a review checklist, not as a mandate.
- Keep constructors explicit when invariants are enforced.
- Avoid exposing implementation-specific collections unless callers need them.
- Prefer `impl Trait` for returned iterators when the concrete type is not part of the contract.
- Prefer `AsRef<[T]>`, `&[T]`, and iterator inputs when ownership is not required.

## Crate Hygiene

- Set `edition = "2024"` for new crates when supported by the MSRV.
- Declare MSRV intentionally for libraries.
- Use `rustfmt` and CI formatting checks.
- Run Clippy with all targets and all features.
- Keep examples and docs compiling where possible.

## Error Handling

- Library APIs should expose meaningful error types.
- Application binaries can use contextual dynamic errors at the boundary.
- Avoid panic in library code except for documented programmer errors.

## Test Shape

- Unit-test invariants and edge cases.
- Integration-test public API behavior.
- Add regression tests before refactors.
- Use property tests or fuzzing for parsers, protocols, and unsafe boundaries.

## Quality Red Flags

- broad `pub` surface without reason;
- hidden `.unwrap()` in library code;
- stringly typed domain concepts;
- generic traits with one implementation;
- examples that do not compile;
- Clippy allowances without local justification.
