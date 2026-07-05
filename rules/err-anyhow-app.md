# err-anyhow-app

## id
err-anyhow-app

## severity
critical

## trigger
Use `anyhow` for application error handling. Trigger when working on error handling and the code shows `err`-class risk.

## bad
```rust
// Tedious type management
fn load_config() -> Result<Config, Box<dyn std::error::Error>> {
    let path = find_config()?;  // Returns FindError
    let content = std::fs::read_to_string(&path)?;  // Returns io::Error
    let config: Config = toml::from_str(&content)?;  // Returns toml::Error
    validate(&config)?;  // Returns ValidationError
    Ok(config)
}

// No context - hard to debug
fn process() -> Result<(), Box<dyn std::error::Error>> {
    let data = fetch()?;  // Which fetch failed?
    transform(data)?;     // What was being transformed?
    save()?;              // Where was it saving to?
    Ok(())
}
```

## good
```rust
use anyhow::{Context, Result};

fn load_config() -> Result<Config> {
    let path = find_config()
        .context("failed to locate config file")?;

    let content = std::fs::read_to_string(&path)
        .with_context(|| format!("failed to read config from {}", path.display()))?;

    let config: Config = toml::from_str(&content)
        .context("failed to parse config as TOML")?;

    validate(&config)
        .context("config validation failed")?;

    Ok(config)
}

// Error message: "config validation failed: field 'port' must be > 0"
// Full chain preserved for debugging
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
- err-thiserror-lib
