# serde-deny-unknown-fields

## id
serde-deny-unknown-fields

## severity
medium

## trigger
Reject unexpected keys with `#[serde(deny_unknown_fields)]`. Trigger when working on serialization compatibility and the code shows `serde`-class risk.

## bad
```rust
use serde::{Serialize, Deserialize};
use serde_json;

#[derive(Serialize, Deserialize, Debug)]
struct ServerConfig {
    host: String,
    port: u16,
    timeout_secs: u64,
}

fn main() {
    // "timout_secs" is a typo - serde silently ignores it, timeout stays 0
    let json = r#"{"host":"localhost","port":8080,"timout_secs":30}"#;
    let cfg: ServerConfig = serde_json::from_str(json).unwrap();
    println!("{:?}", cfg); // timeout_secs is 0, not 30
}
```

## good
```rust
use serde::{Serialize, Deserialize};
use serde_json;

#[derive(Serialize, Deserialize, Debug)]
#[serde(deny_unknown_fields)]
struct ServerConfig {
    host: String,
    port: u16,
    timeout_secs: u64,
}

fn parse_config(json: &str) -> Result<ServerConfig, serde_json::Error> {
    serde_json::from_str(json)
}

fn main() {
    // Typo is now a hard error
    let bad = r#"{"host":"localhost","port":8080,"timout_secs":30}"#;
    assert!(parse_config(bad).is_err());

    // Correct input still works
    let good = r#"{"host":"localhost","port":8080,"timeout_secs":30}"#;
    let cfg = parse_config(good).unwrap();
    println!("{:?}", cfg);
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
- api-parse-dont-validate
- serde-flatten
