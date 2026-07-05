# opt-likely-hint

## id
opt-likely-hint

## severity
high

## trigger
Use code structure to hint at likely branches; use intrinsics on nightly. Trigger when working on compiler optimization and the code shows `opt`-class risk.

## bad
Avoid applying `opt-likely-hint` blindly. The risky pattern is code that ignores: Use code structure to hint at likely branches; use intrinsics on nightly.

## good
Prefer the design encouraged by `opt-likely-hint`: Use code structure to hint at likely branches; use intrinsics on nightly. Keep it explicit and testable.

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
- opt-cold-unlikely
- opt-inline-never-cold
- perf-profile-first
