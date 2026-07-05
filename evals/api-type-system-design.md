# Eval: API Type System Design

Prompt:

> Use $rust-performance-engineering to review a public Rust library API that exposes raw `String` IDs, a runtime-checked request builder, a public trait intended only for internal drivers, serde config structs without compatibility tests, exported `macro_rules!` macros, and feature flags for `serde`, `std`, and `tokio`. Identify what should be encoded in types, what is a semver risk, and which tests should be added.

Expected high-quality answer:

- Loads `rust-api-type-system-design`.
- Recommends validated newtypes or typestate only where invariants and states are real.
- Distinguishes generics, concrete types, sealed traits, and `dyn Trait` by API contract and dispatch cost.
- Checks serde defaults, unknown fields, feature additivity, macro `$crate` hygiene, and semver verification.
