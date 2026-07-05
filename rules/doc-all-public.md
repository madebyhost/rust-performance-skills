# doc-all-public

## id
doc-all-public

## severity
medium

## trigger
Document all public items with `///` doc comments. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```rust
pub struct Config {
    pub timeout: Duration,
    pub retries: u32,
    pub base_url: String,
}

pub fn connect(config: Config) -> Result<Connection, Error> {
    // ...
}

pub enum Status {
    Pending,
    Active,
    Failed,
}
```

## good
```rust
/// Configuration for establishing a connection to the service.
///
/// # Examples
///
/// ```
/// use my_crate::Config;
/// use std::time::Duration;
///
/// let config = Config {
///     timeout: Duration::from_secs(30),
///     retries: 3,
///     base_url: "https://api.example.com".to_string(),
/// };
/// ```
pub struct Config {
    /// Maximum time to wait for a response before timing out.
    pub timeout: Duration,

    /// Number of retry attempts for failed requests.
    pub retries: u32,

    /// Base URL for all API requests.
    pub base_url: String,
}

/// Establishes a connection using the provided configuration.
///
/// # Errors
///
/// Returns an error if the connection cannot be established
/// or if the configuration is invalid.
pub fn connect(config: Config) -> Result<Connection, Error> {
    // ...
}

/// Represents the current status of a job.
pub enum Status {
    /// Job is waiting to be processed.
    Pending,
    /// Job is currently being processed.
    Active,
    /// Job has failed and will not be retried.
    Failed,
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
- doc-module-inner
- lint-missing-docs
