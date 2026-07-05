# err-question-mark

## id
err-question-mark

## severity
critical

## trigger
Use `?` operator for clean propagation. Trigger when working on error handling and the code shows `err`-class risk.

## bad
```rust
// Verbose match-based error handling
fn load_config() -> Result<Config, Error> {
    let content = match std::fs::read_to_string("config.toml") {
        Ok(c) => c,
        Err(e) => return Err(Error::Io(e)),
    };

    let config = match toml::from_str(&content) {
        Ok(c) => c,
        Err(e) => return Err(Error::Parse(e)),
    };

    Ok(config)
}

// Or worse - using unwrap
fn load_config_bad() -> Config {
    let content = std::fs::read_to_string("config.toml").unwrap();
    toml::from_str(&content).unwrap()
}
```

## good
```rust
fn load_config() -> Result<Config, Error> {
    let content = std::fs::read_to_string("config.toml")?;
    let config = toml::from_str(&content)?;
    Ok(config)
}

// Even more concise
fn load_config() -> Result<Config, Error> {
    Ok(toml::from_str(&std::fs::read_to_string("config.toml")?)?)
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
- err-anyhow-app
- err-context-chain
- err-from-impl
