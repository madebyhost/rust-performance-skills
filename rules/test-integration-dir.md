# test-integration-dir

## id
test-integration-dir

## severity
medium

## trigger
Put integration tests in the `tests/` directory. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
```rust
// src/lib.rs
// Mixing integration test logic in library code
#[test]
fn integration_test_full_workflow() {
    // This is a unit test location, not integration
}
```

## good
```rust
// tests/integration_test.rs
use my_crate::{Client, Config};  // Uses public API only

#[test]
fn test_full_workflow() {
    let config = Config::default();
    let client = Client::new(config);

    let result = client.process("input");
    assert!(result.is_ok());
}

#[test]
fn test_error_handling() {
    let client = Client::new(Config::strict());

    let result = client.process("invalid");
    assert!(matches!(result, Err(Error::InvalidInput { .. })));
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
- test-cfg-test-module
- test-descriptive-names
- test-tokio-async
