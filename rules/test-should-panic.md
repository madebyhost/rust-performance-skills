# test-should-panic

## id
test-should-panic

## severity
medium

## trigger
Use `#[should_panic]` to test that code panics as expected. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
```rust
#[test]
fn test_panic() {
    // Just calling panicking code makes test fail
    divide(1, 0);  // Test fails with panic
}

// Using catch_unwind is verbose
#[test]
fn test_panic_manual() {
    let result = std::panic::catch_unwind(|| divide(1, 0));
    assert!(result.is_err());
}
```

## good
```rust
#[test]
#[should_panic]
fn divide_by_zero_panics() {
    divide(1, 0);  // Test passes when this panics
}

// With expected message
#[test]
#[should_panic(expected = "division by zero")]
fn divide_by_zero_panics_with_message() {
    divide(1, 0);  // Panics with "division by zero"
}

// Partial message match
#[test]
#[should_panic(expected = "index out of bounds")]
fn index_panic_contains_message() {
    let v = vec![1, 2, 3];
    let _ = v[100];  // Message contains "index out of bounds"
}
```

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
- err-expect-bugs-only
- err-result-over-panic
- test-descriptive-names
