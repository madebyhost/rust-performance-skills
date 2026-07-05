# err-from-impl

## id
err-from-impl

## severity
critical

## trigger
Implement `From<E>` for error conversions to enable `?` operator. Trigger when working on error handling and the code shows `err`-class risk.

## bad
```rust
#[derive(Debug)]
enum AppError {
    Io(std::io::Error),
    Parse(serde_json::Error),
    Database(diesel::result::Error),
}

fn load_config(path: &str) -> Result<Config, AppError> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| AppError::Io(e))?;  // Manual conversion everywhere

    let config: Config = serde_json::from_str(&content)
        .map_err(|e| AppError::Parse(e))?;  // Repeated boilerplate

    save_to_db(&config)
        .map_err(|e| AppError::Database(e))?;  // Gets tedious

    Ok(config)
}
```

## good
```rust
#[derive(Debug)]
enum AppError {
    Io(std::io::Error),
    Parse(serde_json::Error),
    Database(diesel::result::Error),
}

// Implement From for each source error type
impl From<std::io::Error> for AppError {
    fn from(err: std::io::Error) -> Self {
        AppError::Io(err)
    }
}

impl From<serde_json::Error> for AppError {
    fn from(err: serde_json::Error) -> Self {
        AppError::Parse(err)
    }
}

impl From<diesel::result::Error> for AppError {
    fn from(err: diesel::result::Error) -> Self {
        AppError::Database(err)
    }
}

fn load_config(path: &str) -> Result<Config, AppError> {
    let content = std::fs::read_to_string(path)?;  // Auto-converts
    let config: Config = serde_json::from_str(&content)?;  // Clean!
    save_to_db(&config)?;
    Ok(config)
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
- conv-tryfrom-fallible
- err-question-mark
- err-source-chain
- err-thiserror-lib
