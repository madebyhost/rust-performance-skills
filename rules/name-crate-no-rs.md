# name-crate-no-rs

## id
name-crate-no-rs

## severity
medium

## trigger
Don't suffix crate names with `-rs` or `-rust`. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```toml
# Cargo.toml
[package]
name = "json-parser-rs"    # Redundant -rs
name = "my-lib-rust"       # Redundant -rust
name = "http-client-rs"    # We know it's Rust
name = "rust-sqlite"       # rust- prefix equally bad
```

## good
```toml
# Cargo.toml
[package]
name = "json-parser"
name = "my-lib"
name = "http-client"
name = "sqlite-wrapper"

# Real crate examples (no -rs):
# serde (not serde-rs)
# tokio (not tokio-rs)
# reqwest (not reqwest-rs)
# clap (not clap-rs)
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Add focused tests or static checks that prove the intended behavior and prevent regression.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- doc-cargo-metadata
- name-funcs-snake
- proj-workspace-deps
