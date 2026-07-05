# test-cfg-test-module

## id
test-cfg-test-module

## severity
medium

## trigger
Put unit tests in `#[cfg(test)] mod tests { }` within each module. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
```rust
// Tests without cfg(test) - compiled into release binary
mod tests {
    #[test]
    fn test_something() { ... }  // Included in release build!
}

// Tests in separate file without access to private items
// src/my_module.rs
fn private_helper() { ... }

// tests/my_module_test.rs
// Can't access private_helper!
```

## good
```rust
// src/my_module.rs

fn public_api() -> i32 {
    private_helper() * 2
}

fn private_helper() -> i32 {
    21
}

#[cfg(test)]
mod tests {
    use super::*;  // Access to private items

    #[test]
    fn test_public_api() {
        assert_eq!(public_api(), 42);
    }

    #[test]
    fn test_private_helper() {
        assert_eq!(private_helper(), 21);  // Can test private!
    }
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
- test-integration-dir
- test-use-super
