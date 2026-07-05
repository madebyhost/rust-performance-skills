# lint-cfg-check

## id
lint-cfg-check

## severity
low

## trigger
Enable `unexpected_cfgs` and declare known cfgs to catch feature-gate typos. Trigger when working on linting and the code shows `lint`-class risk.

## bad
```rust
// Typo: "serde_" will never match the "serde" feature.
// Compiles with no warning - the block is silently dead.
#[cfg(feature = "serde_")]
impl serde::Serialize for MyType {}

// Custom cfg used without declaration - also silently ignored.
#[cfg(tokio_unstable)]
pub fn experimental() {}
```

## good
```toml
# Cargo.toml - declare custom cfgs in the lints table
[lints.rust]
unexpected_cfgs = { level = "warn", check-cfg = [
    'cfg(tokio_unstable)',
    'cfg(coverage_nightly)',
] }
```

```rust
// Now "serde_" typo -> compiler warning: unexpected `cfg` condition value
// and tokio_unstable is a known cfg, so it compiles cleanly.
#[cfg(feature = "serde")]      // correct
impl serde::Serialize for MyType {}

#[cfg(tokio_unstable)]         // declared above - no warning
pub fn experimental() {}
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
- lint-warn-suspicious
- lint-workspace-lints
- proj-feature-additive
