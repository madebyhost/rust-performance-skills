# opt-codegen-units

## id
opt-codegen-units

## severity
high

## trigger
Set `codegen-units = 1` for maximum optimization in release builds. Trigger when working on compiler optimization and the code shows `opt`-class risk.

## bad
```toml
# Cargo.toml - default settings
[profile.release]
# codegen-units defaults to 16
# Fast to compile, but misses optimization opportunities
```

## good
```toml
# Cargo.toml - optimized for runtime performance
[profile.release]
codegen-units = 1  # Single unit = better optimization
lto = true         # Link-time optimization
opt-level = 3      # Maximum optimization
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
- opt-lto-release
- opt-pgo-profile
- opt-target-cpu
