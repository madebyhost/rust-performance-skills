# err-source-chain

## id
err-source-chain

## severity
critical

## trigger
Preserve error chains with `#[source]` or `source()` method. Trigger when working on error handling and the code shows `err`-class risk.

## bad
```rust
#[derive(Debug)]
enum ConfigError {
    ParseFailed(String),  // Lost the original serde_json::Error
}

fn load_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| ConfigError::ParseFailed(e.to_string()))?;  // Chain lost!

    serde_json::from_str(&content)
        .map_err(|e| ConfigError::ParseFailed(e.to_string()))?  // No source
}

// Error output: "Parse failed: invalid type: ..."
// Missing: which file? what line? what was the parent error?
```

## good
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum ConfigError {
    #[error("Failed to read config file '{path}'")]
    ReadFailed {
        path: String,
        #[source]  // Preserves the error chain
        source: std::io::Error,
    },

    #[error("Failed to parse config file '{path}'")]
    ParseFailed {
        path: String,
        #[source]  // Original parse error preserved
        source: serde_json::Error,
    },
}

fn load_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|source| ConfigError::ReadFailed {
            path: path.to_string(),
            source,  // Chain preserved
        })?;

    serde_json::from_str(&content)
        .map_err(|source| ConfigError::ParseFailed {
            path: path.to_string(),
            source,
        })
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
- err-context-chain
- err-from-impl
- err-thiserror-lib
