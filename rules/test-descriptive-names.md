# test-descriptive-names

## id
test-descriptive-names

## severity
medium

## trigger
Use descriptive test names that explain what is being tested. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
```rust
#[test]
fn test1() { ... }

#[test]
fn test_parse() { ... }  // Parse what? What behavior?

#[test]
fn it_works() { ... }

#[test]
fn test_function() { ... }

// Failure output: "test test_parse ... FAILED"
// What failed? No idea.
```

## good
```rust
#[test]
fn parse_returns_error_for_empty_input() { ... }

#[test]
fn parse_handles_unicode_characters() { ... }

#[test]
fn user_creation_requires_valid_email() { ... }

#[test]
fn expired_token_is_rejected() { ... }

// Failure output: "test parse_returns_error_for_empty_input ... FAILED"
// Immediately know what broke!
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
- doc-examples-section
- test-arrange-act-assert
- test-cfg-test-module
