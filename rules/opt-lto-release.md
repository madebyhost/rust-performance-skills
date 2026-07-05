# opt-lto-release

## id
opt-lto-release

## severity
high

## trigger
Enable LTO in release builds. Trigger when working on compiler optimization and the code shows `opt`-class risk.

## bad
```toml
# Cargo.toml - default release profile
[profile.release]
opt-level = 3
# No LTO = missed optimization opportunities
```

## good
```toml
# Cargo.toml - optimized release profile
[profile.release]
opt-level = 3
lto = "fat"          # Maximum optimization
codegen-units = 1    # Better optimization (single codegen unit)
panic = "abort"      # Smaller binary, no unwind tables
strip = true         # Remove symbols for smaller binary
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply compiler hints globally or speculatively; keep them for measured hot paths and deployment-specific profiles.

## verification
Inspect release profile, generated code when useful, and benchmark hot paths before keeping the change.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- opt-codegen-units
- opt-pgo-profile
- perf-release-profile
