# Crate Release Engineering

## Pre-Release Checks

- `cargo fmt --all --check`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo nextest run --all-features` or `cargo test --all-targets --all-features`
- `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features`
- `cargo deny check`
- `cargo semver-checks check-release` for public libraries

## Cargo Metadata

- Confirm `name`, `version`, `edition`, `license` or `license-file`, `repository`, `readme`, `description`, `keywords`, and `categories`.
- Keep feature flags additive. Avoid default features that pull heavy optional runtimes unless justified.
- For workspaces, verify each publishable crate has accurate metadata and dependency versions.

## Artifact Types

- Library crate: run semver checks, docs, examples, feature matrix, and `cargo package --list`.
- Binary crate: include `Cargo.lock`, release profile, config docs, and smoke tests.
- PyO3/maturin: run `maturin build --release`, install the wheel in a clean environment, and run import/API tests.
- Wasm: run `wasm-pack build --release`, test browser/node target as relevant, and inspect bundle size.
- FFI: generate headers, verify ABI expectations, ownership rules, and panic boundaries.

## Release Notes

- Document compatibility changes, performance changes, unsafe changes, feature changes, MSRV, and migration steps.
- Do not claim performance improvements without benchmark evidence and hardware/context notes.
