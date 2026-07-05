# doc-link-types

## id
doc-link-types

## severity
medium

## trigger
Use intra-doc links to connect related types and functions. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```rust
/// Parses input and returns a ParseResult.
///
/// See also: ParseError for error types.
/// Uses the Tokenizer internally.
pub fn parse(input: &str) -> ParseResult {
    // "ParseResult", "ParseError", "Tokenizer" are not clickable
    // No verification they exist
}
```

## good
```rust
/// Parses input and returns a [`ParseResult`].
///
/// # Errors
///
/// Returns [`ParseError::InvalidSyntax`] if the input contains invalid tokens.
/// Returns [`ParseError::UnexpectedEof`] if the input ends prematurely.
///
/// # Related
///
/// - [`Tokenizer`] - The underlying tokenizer used by this parser
/// - [`parse_file`] - Convenience function for parsing files
/// - [`ParseOptions`] - Configuration options for parsing
pub fn parse(input: &str) -> ParseResult {
    // All links are clickable and verified
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
- doc-examples-section
- err-doc-errors
- lint-deny-correctness
