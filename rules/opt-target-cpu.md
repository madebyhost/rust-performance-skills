# opt-target-cpu

## id
opt-target-cpu

## severity
high

## trigger
Use `target-cpu=native` for maximum performance on known deployment targets. Trigger when working on compiler optimization and the code shows `opt`-class risk.

## bad
```toml
# Cargo.toml - compiles for generic x86-64
[profile.release]
# No target-cpu specified
# Binary works everywhere but uses only SSE2
```

## good
```toml
# .cargo/config.toml - for known deployment target
[build]
rustflags = ["-C", "target-cpu=native"]

# Or specific CPU for cross-compilation
# rustflags = ["-C", "target-cpu=skylake"]
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
- opt-lto-release
- opt-simd-portable
