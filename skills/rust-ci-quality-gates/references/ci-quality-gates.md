# CI Quality Gates

## Baseline PR Gates

- Format: `cargo fmt --all --check`
- Lint: `cargo clippy --all-targets --all-features -- -D warnings`
- Tests: `cargo nextest run --all-features` when installed, otherwise `cargo test --all-targets --all-features`
- Docs: `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features`
- Dependency policy: `cargo deny check`

## Security And Supply Chain

- Prefer `cargo-deny` for enforceable advisory, license, duplicate, and source policy.
- Use `cargo-audit` as a simpler advisory gate when no deny policy exists.
- Check `Cargo.lock` in applications and binary services. For libraries, document the lockfile choice.
- Avoid CI recipes that run unpinned remote code beyond standard tool installation actions.

## Release Gates

- Public crates: `cargo semver-checks check-release` before publishing.
- Library APIs: include docs, examples, and feature matrix checks.
- PyO3/maturin: build wheels with `maturin build --release` and test import/install from the wheel.
- Wasm: run `wasm-pack build --release` and boundary tests with `wasm-pack test`.

## Expensive Or Targeted Gates

- Unsafe or parser-heavy crates: run `cargo +nightly miri test` on targeted tests where dependencies support it.
- Protocol parsers and wire formats: run `cargo fuzz run <target>` in scheduled CI or dedicated jobs.
- Hot paths: run benchmark smoke checks on PRs and full `cargo bench` on controlled hardware.
- Coverage: prefer `cargo llvm-cov nextest` and publish summary artifacts.

## Template Selection

- Use `templates/ci/rust-library.yml` for normal crates and workspaces.
- Use `templates/ci/pyo3-maturin.yml` when `pyo3` or `maturin` is present.
- Use `templates/ci/wasm.yml` when `wasm-bindgen`, `web-sys`, or `js-sys` is present.
- Use `templates/ci/hft-perf.yml` only when latency benchmarks need controlled, repeatable jobs.
