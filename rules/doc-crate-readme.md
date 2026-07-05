# doc-crate-readme

## id
doc-crate-readme

## severity
medium

## trigger
Unify the README and crate root docs with `#![doc = include_str!("../README.md")]`. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```rust
// src/lib.rs - separate doc comment that will drift from README.md
//! # my-crate
//!
//! A library for doing things. (duplicate, will get out of date)
//!
//! ## Usage
//! ...

pub fn do_thing() {}
```

```toml
# Cargo.toml - readme field absent; crates.io shows nothing
[package]
name = "my-crate"
version = "0.1.0"
edition = "2024"
```

## good
```rust
// src/lib.rs - README is the single source of truth
#![doc = include_str!("../README.md")]

pub fn do_thing() {}
```

```toml
# Cargo.toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2024"
readme = "README.md"          # crates.io landing page
documentation = "https://docs.rs/my-crate"
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
- doc-all-public
- doc-cargo-metadata
- doc-module-inner
