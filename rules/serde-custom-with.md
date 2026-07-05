# serde-custom-with

## id
serde-custom-with

## severity
medium

## trigger
Customize a field's (de)serialization with `with` / `serialize_with` / `deserialize_with`. Trigger when working on serialization compatibility and the code shows `serde`-class risk.

## bad
```rust
use serde::{Serialize, Deserialize};

// Forces a u64 "seconds" field instead of the natural Duration type
#[derive(Serialize, Deserialize, Debug)]
struct Task {
    name: String,
    timeout_secs: u64,   // callers must manually convert to/from Duration
}
```

## good
```rust
use serde::{Serialize, Deserialize, Serializer, Deserializer};
use std::time::Duration;

mod duration_secs {
    use super::*;

    pub fn serialize<S>(duration: &Duration, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        serializer.serialize_u64(duration.as_secs())
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<Duration, D::Error>
    where
        D: Deserializer<'de>,
    {
        let secs = u64::deserialize(deserializer)?;
        Ok(Duration::from_secs(secs))
    }
}

#[derive(Serialize, Deserialize, Debug)]
struct Task {
    name: String,
    // wire format: {"name":"...", "timeout": 30}
    // Rust type: Duration - no manual conversion needed at call sites
    #[serde(with = "duration_secs", rename = "timeout")]
    timeout: Duration,
}

// One-sided variants when you only need to customize one direction:
#[derive(Serialize, Deserialize, Debug)]
struct Report {
    title: String,
    #[serde(serialize_with = "duration_secs::serialize")]
    elapsed: Duration,
    // deserialize_with leaves the deserialize direction at its default
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
- serde-try-from-validate
- type-newtype-validated
