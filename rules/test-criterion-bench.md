# test-criterion-bench

## id
test-criterion-bench

## severity
medium

## trigger
Use `criterion` for benchmarking. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
Avoid applying `test-criterion-bench` blindly. The risky pattern is code that ignores: Use `criterion` for benchmarking.

## good
Prefer the design encouraged by `test-criterion-bench`: Use `criterion` for benchmarking. Keep it explicit and testable.

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Verify the test fails before the fix and covers the intended behavior rather than implementation detail.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- perf-black-box-bench
- perf-profile-first
