# lint-workspace-lints

## id
lint-workspace-lints

## severity
low

## trigger
Configure lints at workspace level for consistent enforcement. Trigger when working on linting and the code shows `lint`-class risk.

## bad
```toml
# crate-a/Cargo.toml - strict
[lints.clippy]
unwrap_used = "deny"

# crate-b/Cargo.toml - lenient
# No lint config

# crate-c/Cargo.toml - different
[lints.clippy]
unwrap_used = "warn"

# Inconsistent enforcement, some issues slip through
```

## good
```toml
# Root Cargo.toml
[workspace.lints.rust]
unsafe_code = "deny"
missing_docs = "warn"

[workspace.lints.clippy]
# Correctness
unwrap_used = "deny"
expect_used = "warn"
panic = "deny"

# Style
needless_pass_by_value = "warn"
redundant_clone = "warn"

# Complexity
cognitive_complexity = "warn"

[workspace.lints.rustdoc]
broken_intra_doc_links = "deny"

# crate-a/Cargo.toml
[lints]
workspace = true

# crate-b/Cargo.toml
[lints]
workspace = true
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Run cargo clippy with the intended lint level and document any allow with a narrow reason.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- anti-unwrap-abuse
- lint-deny-correctness
- proj-workspace-deps
