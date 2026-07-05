# doc-cargo-metadata

## id
doc-cargo-metadata

## severity
medium

## trigger
Fill `Cargo.toml` metadata for published crates. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```toml
[package]
name = "my-awesome-crate"
version = "0.1.0"
edition = "2021"

[dependencies]
# ...
```

## good
```toml
[package]
name = "my-awesome-crate"
version = "0.1.0"
edition = "2021"
rust-version = "1.70"

# Required for crates.io
description = "A fast, ergonomic HTTP client for Rust"
license = "MIT OR Apache-2.0"
repository = "https://github.com/username/my-awesome-crate"

# Highly recommended
documentation = "https://docs.rs/my-awesome-crate"
readme = "README.md"
keywords = ["http", "client", "async", "networking"]
categories = ["network-programming", "web-programming::http-client"]
authors = ["Your Name <you@example.com>"]
homepage = "https://my-awesome-crate.dev"

# Optional but helpful
include = ["src/**/*", "Cargo.toml", "LICENSE*", "README.md"]
exclude = ["tests/fixtures/*", ".github/*"]

[badges]
maintenance = { status = "actively-developed" }

[dependencies]
# ...
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
- doc-module-inner
- lint-cargo-metadata
- proj-workspace-deps
