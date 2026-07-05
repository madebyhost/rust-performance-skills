# proj-feature-additive

## id
proj-feature-additive

## severity
low

## trigger
Design Cargo features to be strictly additive. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
```toml
[features]
# "no_std" disables std - enabling it REMOVES behavior
no_std = []

[dependencies]
# and somewhere in lib.rs:
# #[cfg(not(feature = "no_std"))]
# use std::collections::HashMap;
```

```rust
// lib.rs - toggling off std via a feature is non-additive
#[cfg(not(feature = "no_std"))]
use std::vec::Vec;

#[cfg(feature = "no_std")]
use alloc::vec::Vec;
```

## good
```toml
[features]
# "std" ADDS std support; no_std is the baseline
default = ["std"]
std = []

# Optional integrations - purely additive
serde = ["dep:serde"]
tokio = ["dep:tokio"]

[dependencies]
serde = { version = "1", optional = true }
tokio = { version = "1", optional = true }
```

```rust
// lib.rs - std is opt-in, no_std is the default baseline
#![cfg_attr(not(feature = "std"), no_std)]

#[cfg(feature = "std")]
use std::vec::Vec;

#[cfg(not(feature = "std"))]
use alloc::vec::Vec;
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
- api-serde-optional
- lint-cfg-check
- proj-workspace-deps
