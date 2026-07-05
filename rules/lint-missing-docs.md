# lint-missing-docs

## id
lint-missing-docs

## severity
low

## trigger
Warn on missing documentation for public items. Trigger when working on linting and the code shows `lint`-class risk.

## bad
Avoid applying `lint-missing-docs` blindly. The risky pattern is code that ignores: Warn on missing documentation for public items.

## good
```rust
#![warn(missing_docs)]

//! User management module.

/// Represents a registered user in the system.
pub struct User {
    /// The user's display name.
    pub name: String,
    /// The user's age in years.
    pub age: u32,
}

/// Processes pending user requests.
///
/// # Examples
///
/// ```
/// process();
/// ```
pub fn process() { }

/// Handler trait for request processing.
pub trait Handler {
    /// Handle an incoming request.
    fn handle(&self);
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Run cargo clippy with the intended lint level and document any allow with a narrow reason.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- doc-all-public
- doc-examples-section
- lint-unsafe-doc
