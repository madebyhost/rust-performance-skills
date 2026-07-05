# err-result-over-panic

## id
err-result-over-panic

## severity
critical

## trigger
Return `Result<T, E>` instead of panicking for recoverable errors. Trigger when working on error handling and the code shows `err`-class risk.

## bad
```rust
fn parse_config(path: &str) -> Config {
    let content = std::fs::read_to_string(path)
        .expect("Failed to read config");  // Crashes on missing file

    serde_json::from_str(&content)
        .expect("Invalid config format")   // Crashes on bad JSON
}

fn divide(a: i32, b: i32) -> i32 {
    if b == 0 {
        panic!("Division by zero!");  // Crashes the program
    }
    a / b
}
```

Caller has no chance to recover or provide a fallback.

## good
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum ConfigError {
    #[error("Failed to read config file: {0}")]
    Io(#[from] std::io::Error),
    #[error("Invalid config format: {0}")]
    Parse(#[from] serde_json::Error),
}

fn parse_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)?;
    let config = serde_json::from_str(&content)?;
    Ok(config)
}

fn divide(a: i32, b: i32) -> Result<i32, &'static str> {
    if b == 0 {
        return Err("Division by zero");
    }
    Ok(a / b)
}

// Caller decides how to handle
match parse_config("app.json") {
    Ok(config) => run_app(config),
    Err(e) => {
        eprintln!("Using default config: {}", e);
        run_app(Config::default())
    }
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
- anti-unwrap-abuse
- err-anyhow-app
- err-no-unwrap-prod
- err-thiserror-lib
