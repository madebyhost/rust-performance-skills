# perf-release-profile

## id
perf-release-profile

## severity
medium

## trigger
Optimize release profile settings. Trigger when working on performance patterns and the code shows `perf`-class risk.

## bad
Avoid applying `perf-release-profile` blindly. The risky pattern is code that ignores: Optimize release profile settings.

## good
Prefer the design encouraged by `perf-release-profile`: Optimize release profile settings. Keep it explicit and testable.

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply when the path is cold, unmeasured, or the optimization makes correctness and maintenance worse than the measured gain.

## verification
Measure before and after with a benchmark that captures the suspected bottleneck.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- opt-codegen-units
- opt-lto-release
- opt-pgo-profile
