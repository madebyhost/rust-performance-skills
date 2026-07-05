# doc-intra-links

## id
doc-intra-links

## severity
medium

## trigger
Use intra-doc links to reference types and items. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```rust
/// Returns the length of the buffer.
///
/// See also `capacity()` for the allocated size, and the
/// `Buffer` struct for more details.
pub fn len(&self) -> usize {
    self.data.len()
}

/// Parses the input using std::str::FromStr trait.
/// Check the Error enum for possible failures.
pub fn parse<T: FromStr>(input: &str) -> Result<T, Error> {
    // ...
}
```

## good
```rust
/// Returns the length of the buffer.
///
/// See also [`capacity()`](Self::capacity) for the allocated size, and
/// [`Buffer`] for more details.
pub fn len(&self) -> usize {
    self.data.len()
}

/// Parses the input using [`FromStr`] trait.
/// Check [`Error`] for possible failures.
///
/// [`FromStr`]: std::str::FromStr
pub fn parse<T: FromStr>(input: &str) -> Result<T, Error> {
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
- doc-all-public
- doc-errors-section
- doc-examples-section
