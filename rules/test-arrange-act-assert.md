# test-arrange-act-assert

## id
test-arrange-act-assert

## severity
medium

## trigger
Structure tests with clear Arrange, Act, Assert sections. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
```rust
#[test]
fn test_user() {
    assert_eq!(User::new("alice", "alice@example.com").unwrap().name(), "alice");
    assert!(User::new("", "email@example.com").is_err());
    let u = User::new("bob", "bob@example.com").unwrap();
    assert!(u.validate());
    assert_eq!(u.email(), "bob@example.com");
}
// Multiple concerns, hard to understand, hard to debug
```

## good
```rust
#[test]
fn new_user_has_correct_name() {
    // Arrange
    let name = "alice";
    let email = "alice@example.com";

    // Act
    let user = User::new(name, email).unwrap();

    // Assert
    assert_eq!(user.name(), "alice");
}

#[test]
fn user_creation_fails_with_empty_name() {
    // Arrange
    let name = "";
    let email = "email@example.com";

    // Act
    let result = User::new(name, email);

    // Assert
    assert!(result.is_err());
    assert!(matches!(result, Err(UserError::EmptyName)));
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
- test-descriptive-names
- test-fixture-raii
- test-mock-traits
