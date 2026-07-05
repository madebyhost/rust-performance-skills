# doc-errors-section

## id
doc-errors-section

## severity
medium

## trigger
Include `# Errors` section for fallible functions. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```rust
/// Opens a file and reads its contents.
pub fn read_file(path: &Path) -> Result<String, Error> {
    // Users have no idea what errors to expect
}

/// Connects to the database.
pub async fn connect(url: &str) -> Result<Connection, DbError> {
    // Multiple failure modes, none documented
}
```

## good
```rust
/// Opens a file and reads its contents as a UTF-8 string.
///
/// # Errors
///
/// Returns an error if:
/// - The file does not exist ([`Error::NotFound`])
/// - The process lacks permission to read the file ([`Error::PermissionDenied`])
/// - The file contains invalid UTF-8 ([`Error::InvalidUtf8`])
pub fn read_file(path: &Path) -> Result<String, Error> {
    // ...
}

/// Establishes a connection to the database.
///
/// # Errors
///
/// This function will return an error if:
/// - The URL is malformed ([`DbError::InvalidUrl`])
/// - The database server is unreachable ([`DbError::ConnectionFailed`])
/// - Authentication fails ([`DbError::AuthenticationFailed`])
/// - The connection pool is exhausted ([`DbError::PoolExhausted`])
pub async fn connect(url: &str) -> Result<Connection, DbError> {
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
- doc-intra-links
- doc-panics-section
- err-doc-errors
