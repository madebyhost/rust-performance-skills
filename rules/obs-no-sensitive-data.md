# obs-no-sensitive-data

## id
obs-no-sensitive-data

## severity
medium

## trigger
Never log secrets or PII; redact or skip them. Trigger when working on observability and the code shows `obs`-class risk.

## bad
```rust
use tracing::instrument;

struct Credentials {
    username: String,
    password: String,   // secret
    api_key: String,    // secret
}

// BAD: instrument auto-captures all args as fields - password becomes a span field
#[instrument]
async fn authenticate(credentials: &Credentials) -> bool {
    // Also BAD: manual logging of the whole struct
    tracing::info!(?credentials, "authenticating user");
    true
}
```

## good
```rust
use tracing::{info, instrument};

// A simple redacting newtype - implement for any sensitive type
#[derive(Clone)]
struct Secret(String);

impl std::fmt::Debug for Secret {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("[redacted]")
    }
}

impl std::fmt::Display for Secret {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("[redacted]")
    }
}

struct Credentials {
    username: String,
    password: Secret,   // redacts in Debug/Display
    api_key: Secret,    // redacts in Debug/Display
}

// GOOD: skip sensitive args by name
#[instrument(skip(credentials), fields(username = %credentials.username))]
async fn authenticate(credentials: &Credentials) -> bool {
    info!("authenticating user");
    // password and api_key never appear in any span field or log line
    verify_password(&credentials.username, &credentials.password)
}

fn verify_password(_username: &str, _password: &Secret) -> bool { true }
```

```rust
// Alternative: use the `secrecy` crate (Secret<T> implements Debug as "[redacted]")
// use secrecy::{Secret, ExposeSecret};
// struct Credentials { username: String, password: Secret<String> }
// credentials.password.expose_secret()  // only call site that reveals value
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
- err-thiserror-lib
- obs-instrument-spans
- obs-structured-fields
