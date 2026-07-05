# test-mockall-mocking

## id
test-mockall-mocking

## severity
medium

## trigger
Use mockall for trait mocking. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
Avoid applying `test-mockall-mocking` blindly. The risky pattern is code that ignores: Use mockall for trait mocking.

## good
Prefer the design encouraged by `test-mockall-mocking`: Use mockall for trait mocking. Keep it explicit and testable.

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
- test-mock-traits
- test-proptest-properties
