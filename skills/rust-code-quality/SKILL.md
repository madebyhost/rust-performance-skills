---
name: rust-code-quality
description: "Use when writing, reviewing, or refactoring Rust code for idiomatic quality, API design, maintainability, tests, documentation, crate hygiene, clippy/rustfmt/lints, error handling, public interfaces, and long-term contributor experience."
---

# Rust Code Quality

Use this skill to improve code quality before chasing performance tricks. Load `references/code-quality.md` for detailed checklists. Load `rust-api-type-system-design` when public API contracts, validated types, serde compatibility, macros, traits, feature flags, or semver-sensitive type boundaries dominate the review.

## Workflow

1. Inspect the actual crate shape: `Cargo.toml`, module layout, public API, tests, docs, lints, examples.
2. Separate public API quality from internal implementation quality.
3. Prefer type-driven invariants, clear ownership, explicit errors, and minimal public surface.
4. Run or recommend `cargo fmt`, `cargo clippy --all-targets --all-features`, `cargo test --all-targets --all-features`, and docs checks.

## Defaults

- Prefer `Result<T, E>` with typed errors for libraries; use `anyhow` mainly at application edges.
- Prefer newtypes for domain invariants.
- Keep public APIs generic over borrowed data when it avoids allocation without lifetime pain.
- Document panics, errors, safety, and performance-sensitive behavior.
- Use Clippy groups intentionally; cherry-pick strict lints rather than enabling every restriction lint.

## Output

Return findings grouped as correctness, API, maintainability, tests/docs, and performance-adjacent quality. Include exact commands to verify.
