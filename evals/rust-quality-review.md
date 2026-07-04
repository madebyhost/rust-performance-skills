# Eval: Rust Quality Review

Ask the agent to review a small Rust crate with weak lints, missing tests, and a public API change.

Expected behavior:

- Loads `rust-performance-engineering`, `rust-code-quality`, `rust-ci-quality-gates`, and `rust-testing-verification` as needed.
- Reports correctness and API risks before style.
- Recommends `cargo fmt`, `cargo clippy`, tests, docs, dependency policy, and semver checks when public API is affected.
- States missing evidence rather than claiming performance improvement.
