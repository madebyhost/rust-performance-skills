# API Type System Design Reference

## Boundary First

- Classify the API before changing it: public crate API, internal module seam, serde DTO, protocol frame, macro API, FFI wrapper, or domain model.
- Public APIs are semver contracts; internal APIs can prioritize clarity and refactorability.
- Prefer narrow `pub(crate)` and re-export deliberate public entry points.

## Type-Driven Invariants

- Parse external values into validated types at boundaries instead of passing raw strings and re-validating everywhere.
- Use newtypes for IDs, money, units, validated strings, handles, permissions, and protocol identifiers.
- Use typestate when invalid transitions are real domain bugs and the state graph is small enough to stay readable.
- Use `PhantomData` to express ownership, lifetime, variance, or state relationships without runtime fields.

## Traits And Dispatch

- Prefer concrete types until multiple implementations exist.
- Prefer generics or `impl Trait` for hot homogeneous paths where inlining matters.
- Prefer `dyn Trait` for heterogeneous collections, plugin-like APIs, or binary-size-sensitive call sites.
- Use associated types when each implementation has one natural output; use generics when multiple input/output combinations are valid.
- Seal traits when outside implementations would break invariants or future trait evolution.

## Serde And Compatibility

- Gate serde support behind an additive feature for reusable libraries unless serialization is the core purpose.
- Use field-level `#[serde(default)]` for backward-compatible additions.
- Use `#[serde(deny_unknown_fields)]` for strict configs and public contracts; avoid it when extension metadata is expected.
- Treat `#[serde(flatten)]` as a compatibility and ambiguity decision, not a formatting shortcut.
- Add golden fixtures for serialized public formats.

## Patterns, Macros, And Cfgs

- Match owned enums exhaustively; avoid `_` arms that hide future variants you control.
- Use `let else`, `matches!`, and if-let chains when they reduce nesting without hiding errors.
- Prefer functions over macros unless syntax, repetition, or compile-time generation is the real requirement.
- Use `$crate` for exported macro paths and keep helper items hidden.
- Keep Cargo features additive. Use `std` as an enabling feature for no-std-capable crates.
- Enable `unexpected_cfgs` for custom cfg names and feature-gate typo detection.

## Verification

- Compile-fail or trybuild tests for typestate, sealed traits, and macro APIs.
- Serde compatibility fixtures for defaults, unknown fields, renamed fields, and versioned payloads.
- Property tests for validated constructors and conversion round trips.
- `cargo semver-checks` for public API changes.
- Docs and examples that compile under the intended feature matrix.

## Red Flags

- Raw `String`/`u64` domain identifiers in public APIs when semantic newtypes are cheap.
- Generic traits with one implementation and no extension plan.
- Public traits that external crates can implement without invariant checks.
- Serde defaults that silently accept malformed config.
- Wildcard enum matches on enums owned by the current crate.
- Macros using `crate::` paths instead of `$crate`.
