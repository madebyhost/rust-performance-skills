# api-builder-must-use

## id
api-builder-must-use

## severity
high

## trigger
Mark builder methods with `#[must_use]` to prevent silent drops. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
struct RequestBuilder {
    url: String,
    timeout: Option<Duration>,
    headers: Vec<(String, String)>,
}

impl RequestBuilder {
    fn timeout(mut self, duration: Duration) -> Self {
        self.timeout = Some(duration);
        self
    }

    fn header(mut self, key: &str, value: &str) -> Self {
        self.headers.push((key.to_string(), value.to_string()));
        self
    }
}

// Bug: builder methods are ignored - no warning!
let request = RequestBuilder::new("https://api.example.com");
request.timeout(Duration::from_secs(30));  // Dropped silently!
request.header("Authorization", "Bearer token");  // Dropped silently!
let response = request.send();  // Sends with no timeout or headers
```

## good
```rust
struct RequestBuilder {
    url: String,
    timeout: Option<Duration>,
    headers: Vec<(String, String)>,
}

impl RequestBuilder {
    #[must_use = "builder methods return modified builder - chain or assign"]
    fn timeout(mut self, duration: Duration) -> Self {
        self.timeout = Some(duration);
        self
    }

    #[must_use = "builder methods return modified builder - chain or assign"]
    fn header(mut self, key: &str, value: &str) -> Self {
        self.headers.push((key.to_string(), value.to_string()));
        self
    }
}

// Now warns: unused return value that must be used
let request = RequestBuilder::new("https://api.example.com");
request.timeout(Duration::from_secs(30));  // Warning!

// Correct: chain methods
let response = RequestBuilder::new("https://api.example.com")
    .timeout(Duration::from_secs(30))
    .header("Authorization", "Bearer token")
    .send();
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
- api-builder-pattern
- api-must-use
- err-result-over-panic
