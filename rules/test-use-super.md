# test-use-super

## id
test-use-super

## severity
medium

## trigger
Use `use super::*;` in test modules to access parent module items. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
```rust
// Verbose imports
#[cfg(test)]
mod tests {
    use crate::my_module::public_function;
    use crate::my_module::MyStruct;
    // Can't access private items this way!

    #[test]
    fn test_function() {
        let result = public_function();
        // ...
    }
}
```

## good
```rust
// src/my_module.rs
pub struct PublicStruct { ... }
struct PrivateStruct { ... }  // Private

pub fn public_function() -> i32 { ... }
fn private_helper() -> i32 { ... }  // Private

#[cfg(test)]
mod tests {
    use super::*;  // Imports everything from parent

    #[test]
    fn test_public_struct() {
        let s = PublicStruct::new();
        // ...
    }

    #[test]
    fn test_private_struct() {
        let s = PrivateStruct::new();  // Can access private!
        // ...
    }

    #[test]
    fn test_private_helper() {
        assert_eq!(private_helper(), 42);  // Can test private!
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
- proj-pub-crate-internal
- test-cfg-test-module
- test-integration-dir
