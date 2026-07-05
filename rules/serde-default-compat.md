# serde-default-compat

## id
serde-default-compat

## severity
medium

## trigger
Use `#[serde(default)]` for optional and backward-compatible fields. Trigger when working on serialization compatibility and the code shows `serde`-class risk.

## bad
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct Config {
    host: String,
    port: u16,
    timeout_secs: u64,  // newly added - old configs don't have this, so they fail
    retries: u32,       // newly added - same problem
}
```

## good
```rust
use serde::{Serialize, Deserialize};

fn default_timeout() -> u64 { 30 }
fn default_retries() -> u32 { 3 }

#[derive(Serialize, Deserialize, Debug)]
struct Config {
    host: String,
    port: u16,
    // fills from Default::default() (0u64) if missing
    #[serde(default)]
    timeout_secs: u64,
    // fills from the named function if missing
    #[serde(default = "default_retries")]
    retries: u32,
    // fills from Default (None) if missing
    #[serde(default)]
    tls_cert_path: Option<String>,
}

// Alternatively, annotate the whole container so every field uses its Default:
#[derive(Serialize, Deserialize, Debug, Default)]
#[serde(default)]
struct FeatureFlags {
    enable_caching: bool,    // false
    enable_metrics: bool,    // false
    max_connections: u32,    // 0
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
- api-default-impl
- serde-skip-empty
