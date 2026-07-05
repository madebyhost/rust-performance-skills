# test-tokio-async

## id
test-tokio-async

## severity
medium

## trigger
Use `#[tokio::test]` for async tests. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
```rust
// Won't compile - async fn can't be called without runtime
#[test]
async fn test_async_function() {  // Error!
    let result = fetch_data().await;
    assert!(result.is_ok());
}

// Manual runtime - verbose and error-prone
#[test]
fn test_async_function() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        let result = fetch_data().await;
        assert!(result.is_ok());
    });
}
```

## good
```rust
#[tokio::test]
async fn test_async_function() {
    let result = fetch_data().await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_concurrent_operations() {
    let (a, b) = tokio::join!(
        fetch_user(1),
        fetch_user(2),
    );
    assert!(a.is_ok());
    assert!(b.is_ok());
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
- async-tokio-runtime
- test-fixture-raii
- test-mock-traits
