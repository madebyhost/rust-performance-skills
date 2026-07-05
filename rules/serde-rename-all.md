# serde-rename-all

## id
serde-rename-all

## severity
medium

## trigger
Match the external naming convention with `#[serde(rename_all = ...)]`. Trigger when working on serialization compatibility and the code shows `serde`-class risk.

## bad
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct UserProfile {
    #[serde(rename = "firstName")]
    first_name: String,
    #[serde(rename = "lastName")]
    last_name: String,
    #[serde(rename = "emailAddress")]
    email_address: String,
    #[serde(rename = "isActive")]
    is_active: bool,
}
```

## good
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct UserProfile {
    first_name: String,
    last_name: String,
    email_address: String,
    is_active: bool,
    // per-field override: "type" is a keyword in Rust, so we rename it explicitly
    #[serde(rename = "type")]
    user_type: String,
}

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
enum Status {
    Active,
    Inactive,
    PendingVerification,
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not make serde strict when extension fields are expected or when backward compatibility requires tolerance.

## verification
Use golden fixtures, versioned payload tests, and compatibility checks for unknown or missing fields.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-serde-optional
- serde-default-compat
