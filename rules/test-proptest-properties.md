# test-proptest-properties

## id
test-proptest-properties

## severity
medium

## trigger
Use proptest for property-based testing. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
Avoid applying `test-proptest-properties` blindly. The risky pattern is code that ignores: Use proptest for property-based testing.

## good
Prefer the design encouraged by `test-proptest-properties`: Use proptest for property-based testing. Keep it explicit and testable.

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
- test-arrange-act-assert
- test-criterion-bench
- test-mockall-mocking
