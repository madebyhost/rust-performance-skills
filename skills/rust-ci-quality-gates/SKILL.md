---
name: rust-ci-quality-gates
description: "Use when designing, reviewing, or fixing CI quality gates for Rust crates, workspaces, PyO3/maturin extensions, Wasm packages, unsafe-heavy crates, low-latency systems, release checks, dependency security, formatting, linting, testing, coverage, fuzzing, Miri, and benchmark workflows."
---

# Rust CI Quality Gates

Use this skill when a Rust project needs repeatable CI gates rather than ad hoc local checks. Load `references/ci-quality-gates.md` for the command matrix and template selection rules.

## Workflow

1. Inspect `Cargo.toml`, workspace layout, `Cargo.lock`, `deny.toml`, `.config/nextest`, fuzz targets, benchmarks, bindings, and existing workflows.
2. Separate mandatory gates from expensive optional gates.
3. Prefer deterministic gates before performance gates: format, lint, tests, dependency policy, docs, semver, coverage.
4. Add expensive gates only where they prove a real risk: Miri for unsafe/parser logic, fuzz for parsers/protocols, benches for hot paths, wasm-pack for Wasm, maturin for PyO3.
5. Keep CI commands copy-pastable and project-local.

## Gate Defaults

- Always include `cargo fmt --check`, `cargo clippy --all-targets --all-features`, and tests.
- Prefer `cargo nextest run` for Rust test execution when available.
- Use `cargo deny check` for license, advisory, duplicate, and source policy.
- Use `cargo audit` when the project does not yet have a cargo-deny policy.
- Use `cargo semver-checks` for public crates and release branches.
- Use `cargo llvm-cov nextest` or equivalent when coverage is part of the contribution contract.
- Use `cargo +nightly miri test` only for suitable crates and targeted tests; document unsupported dependencies.

## Output

Return the CI command set grouped by mandatory, release, security, performance, and binding-specific gates. State expected runtime cost and which gates should be PR, nightly, or release-only.
