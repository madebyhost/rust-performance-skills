# api-builder-pattern

## id
api-builder-pattern

## severity
high

## trigger
Use Builder pattern for complex construction. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
// Constructor with many parameters - hard to read, easy to get wrong
let client = Client::new(
    "https://api.example.com",  // Which is which?
    30,                          // Timeout? Retries?
    true,                        // What does this mean?
    None,
    Some("auth_token"),
    false,
);

// Or many Option fields
struct Client {
    url: String,
    timeout: Option<Duration>,
    retries: Option<u32>,
    // ... 10 more optional fields
}
```

## good
```rust
#[derive(Default)]
#[must_use = "builders do nothing unless you call build()"]
pub struct ClientBuilder {
    base_url: Option<String>,
    timeout: Option<Duration>,
    max_retries: u32,
    auth_token: Option<String>,
}

impl ClientBuilder {
    pub fn new() -> Self {
        Self::default()
    }

    /// Sets the base URL for all requests.
    pub fn base_url(mut self, url: impl Into<String>) -> Self {
        self.base_url = Some(url.into());
        self
    }

    /// Sets the request timeout. Default is 30 seconds.
    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = Some(timeout);
        self
    }

    /// Sets the maximum number of retries. Default is 3.
    pub fn max_retries(mut self, n: u32) -> Self {
        self.max_retries = n;
        self
    }

    /// Sets the authentication token.
    pub fn auth_token(mut self, token: impl Into<String>) -> Self {
        self.auth_token = Some(token.into());
        self
    }

    /// Builds the client with the configured options.
    pub fn build(self) -> Result<Client, BuilderError> {
        let base_url = self.base_url
            .ok_or(BuilderError::MissingBaseUrl)?;

        Ok(Client {
            base_url,
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
            max_retries: self.max_retries,
            auth_token: self.auth_token,
        })
    }
}

// Usage - clear and self-documenting
let client = ClientBuilder::new()
    .base_url("https://api.example.com")
    .timeout(Duration::from_secs(10))
    .max_retries(5)
    .auth_token("secret")
    .build()?;
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not over-generalize a public API before real consumers or compatibility constraints exist.

## verification
Compile examples, run semver checks for public APIs, and add tests for boundary behavior.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-builder-must-use
- api-impl-into
- api-typestate
