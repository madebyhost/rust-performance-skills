# proj-workspace-deps

## id
proj-workspace-deps

## severity
low

## trigger
Use workspace dependency inheritance for consistent versions across crates. Trigger when working on project structure and the code shows `proj`-class risk.

## bad
```toml
# crate-a/Cargo.toml
[dependencies]
serde = "1.0.150"
tokio = "1.25"

# crate-b/Cargo.toml
[dependencies]
serde = "1.0.188"  # Different version!
tokio = "1.32"     # Different version!

# Version drift leads to:
# - Larger binaries (multiple versions)
# - Compilation time increase
# - Subtle behavior differences
```

## good
```toml
# Root Cargo.toml
[workspace]
members = ["crate-a", "crate-b", "crate-c"]

[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1.32", features = ["full"] }
thiserror = "1.0"
anyhow = "1.0"
tracing = "0.1"

# crate-a/Cargo.toml
[dependencies]
serde.workspace = true
tokio.workspace = true

# crate-b/Cargo.toml
[dependencies]
serde.workspace = true
tokio.workspace = true
thiserror.workspace = true
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
- lint-deny-correctness
- proj-lib-main-split
