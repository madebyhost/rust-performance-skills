# doc-examples-section

## id
doc-examples-section

## severity
medium

## trigger
Include `# Examples` with runnable code. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```rust
/// Parses a string into a Foo.
pub fn parse(s: &str) -> Result<Foo, Error> {
    // No examples - users have to guess usage
}

/// A widget for doing things.
///
/// This widget is very useful.
pub struct Widget {
    // Still no examples
}
```

## good
```rust
/// Parses a string into a Foo.
///
/// # Examples
///
/// ```
/// use my_crate::parse;
///
/// let foo = parse("hello").unwrap();
/// assert_eq!(foo.name(), "hello");
/// ```
///
/// Handles empty strings:
///
/// ```
/// use my_crate::parse;
///
/// let foo = parse("").unwrap();
/// assert!(foo.is_empty());
/// ```
pub fn parse(s: &str) -> Result<Foo, Error> {
    // ...
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Add focused tests or static checks that prove the intended behavior and prevent regression.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- doc-errors-section
- doc-hidden-setup
- doc-question-mark
