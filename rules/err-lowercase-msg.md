# err-lowercase-msg

## id
err-lowercase-msg

## severity
critical

## trigger
Start error messages lowercase, no trailing punctuation. Trigger when working on error handling and the code shows `err`-class risk.

## bad
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum ConfigError {
    #[error("Failed to read config file.")]  // Capital F, trailing period
    ReadFailed(#[from] std::io::Error),

    #[error("Invalid JSON format!")]  // Capital I, exclamation
    ParseFailed(#[from] serde_json::Error),

    #[error("The requested key was not found")]  // Reads like a sentence
    KeyNotFound(String),
}

// Chained output: "Config load error: Failed to read config file.: No such file"
// Awkward capitalization and punctuation
```

## good
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum ConfigError {
    #[error("failed to read config file")]  // lowercase, no period
    ReadFailed(#[from] std::io::Error),

    #[error("invalid JSON format")]  // lowercase, no period
    ParseFailed(#[from] serde_json::Error),

    #[error("key not found: {0}")]  // lowercase, data at end
    KeyNotFound(String),
}

// Chained output: "config load error: failed to read config file: no such file"
// Clean, consistent
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
- err-context-chain
- err-thiserror-lib
