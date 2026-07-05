# opt-simd-portable

## id
opt-simd-portable

## severity
high

## trigger
Use portable SIMD for vectorized operations across architectures. Trigger when working on compiler optimization and the code shows `opt`-class risk.

## bad
Avoid applying `opt-simd-portable` blindly. The risky pattern is code that ignores: Use portable SIMD for vectorized operations across architectures.

## good
Prefer the design encouraged by `opt-simd-portable`: Use portable SIMD for vectorized operations across architectures. Keep it explicit and testable.

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
- opt-bounds-check
- opt-target-cpu
- perf-profile-first
