---
name: rust-crate-release-engineering
description: "Use when preparing, reviewing, or fixing Rust crate releases, workspace publishing, versioning, public API compatibility, feature flags, Cargo metadata, docs.rs, semver checks, changelogs, PyO3/maturin wheels, Wasm packages, FFI artifacts, and CI release workflows."
---

# Rust Crate Release Engineering

Use this skill for release readiness and packaging quality. Load `references/crate-release-engineering.md` for release checklists.

## Workflow

1. Inspect crate metadata, feature flags, public API, docs, examples, license files, README, CI, and release workflows.
2. Classify release target: library crate, binary, workspace, PyO3 wheel, Wasm package, FFI package, or internal service.
3. Protect compatibility first: run tests, docs, clippy, and semver checks before packaging.
4. Build release artifacts from clean state with locked toolchains where possible.
5. Document performance-relevant release settings and feature combinations.

## Defaults

- Public libraries need `cargo semver-checks`, docs, examples, and a feature matrix.
- Applications should commit `Cargo.lock` and document runtime configuration.
- PyO3/maturin packages should test built wheels, not just source builds.
- Wasm packages should test generated JS bindings and boundary behavior.
- FFI releases should define ownership, ABI stability, headers, and symbol/versioning expectations.

## Output

Return a release checklist with blocking issues, commands, artifact expectations, and rollback or compatibility risks.
