# api-serde-optional

## id
api-serde-optional

## severity
high

## trigger
Make serde a feature flag, not a hard dependency for library crates. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
// Cargo.toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }

// lib.rs
use serde::{Serialize, Deserialize};

// Every user pays for serde, even if they don't need it
#[derive(Serialize, Deserialize)]
pub struct Config {
    pub name: String,
    pub value: i32,
}
```

## good
```rust
// Cargo.toml
[dependencies]
serde = { version = "1.0", features = ["derive"], optional = true }

[features]
default = []
serde = ["dep:serde"]

// lib.rs
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Config {
    pub name: String,
    pub value: i32,
}

// Users opt-in:
// my_crate = { version = "1.0", features = ["serde"] }
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not over-generalize a public API before real consumers or compatibility constraints exist.

## verification
Compile examples, run semver checks for public APIs, and add tests for boundary behavior.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-common-traits
- lint-deny-correctness
- proj-lib-main-split
- serde-rename-all
- serde-try-from-validate
