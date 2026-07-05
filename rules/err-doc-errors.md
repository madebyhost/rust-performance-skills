# err-doc-errors

## id
err-doc-errors

## severity
critical

## trigger
Document error conditions with `# Errors` section in doc comments. Trigger when working on error handling and the code shows `err`-class risk.

## bad
```rust
/// Loads a configuration from the specified path.
pub fn load_config(path: &Path) -> Result<Config, ConfigError> {
    // No documentation of error conditions
    // Caller must read source code to understand what can fail
}

/// Parses and validates the input string.
///
/// Returns the parsed value.  // What about errors?
pub fn parse_input(input: &str) -> Result<Value, ParseError> {
    // ...
}
```

## good
```rust
/// Loads a configuration from the specified path.
///
/// # Errors
///
/// Returns an error if:
/// - The file at `path` does not exist or cannot be read
/// - The file contents are not valid TOML
/// - Required configuration keys are missing
/// - Configuration values are out of valid ranges
///
/// # Examples
///
/// ```
/// # use mylib::{load_config, ConfigError};
/// # fn main() -> Result<(), ConfigError> {
/// let config = load_config("app.toml")?;
/// # Ok(())
/// # }
/// ```
pub fn load_config(path: &Path) -> Result<Config, ConfigError> {
    // ...
}

/// Parses and validates the input string as a positive integer.
///
/// # Errors
///
/// Returns [`ParseError::Empty`] if the input is empty.
/// Returns [`ParseError::InvalidFormat`] if the input contains non-digit characters.
/// Returns [`ParseError::Overflow`] if the value exceeds `i64::MAX`.
/// Returns [`ParseError::NotPositive`] if the value is zero or negative.
pub fn parse_positive_int(input: &str) -> Result<i64, ParseError> {
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
- api-must-use
- doc-examples-section
- err-thiserror-lib
