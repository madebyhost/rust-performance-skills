# opt-pgo-profile

## id
opt-pgo-profile

## severity
high

## trigger
Use Profile-Guided Optimization (PGO) for maximum performance. Trigger when working on compiler optimization and the code shows `opt`-class risk.

## bad
Avoid applying `opt-pgo-profile` blindly. The risky pattern is code that ignores: Use Profile-Guided Optimization (PGO) for maximum performance.

## good
Prefer the design encouraged by `opt-pgo-profile`: Use Profile-Guided Optimization (PGO) for maximum performance. Keep it explicit and testable.

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
- perf-profile-first
