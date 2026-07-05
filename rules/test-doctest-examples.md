# test-doctest-examples

## id
test-doctest-examples

## severity
medium

## trigger
Keep documentation examples as executable doctests. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
```rust
/// Parses a number from a string.
///
/// Example:
/// let n = parse("42");  // Not tested!
/// assert_eq!(n, 42);
pub fn parse(s: &str) -> i32 {
    s.parse().unwrap()
}

// Documentation can become outdated:
/// Adds two numbers.
///
/// ```
/// let sum = add(1, 2, 3);  // Wrong number of args - not caught!
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## good
```rust
/// Parses a number from a string.
///
/// # Examples
///
/// ```
/// use my_crate::parse;
///
/// let n = parse("42");
/// assert_eq!(n, 42);
/// ```
pub fn parse(s: &str) -> i32 {
    s.parse().unwrap()
}

/// Adds two numbers.
///
/// # Examples
///
/// ```
/// use my_crate::add;
///
/// let sum = add(1, 2);
/// assert_eq!(sum, 3);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
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
- doc-examples-section
- doc-hidden-setup
- doc-question-mark
