# anti-panic-expected

## id
anti-panic-expected

## severity
reference

## trigger
Don't panic on expected or recoverable errors. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// Network failures are expected
fn fetch_data(url: &str) -> Data {
    let response = reqwest::blocking::get(url)
        .expect("network error");  // Crashes on timeout
    response.json().expect("invalid json")  // Crashes on bad response
}

// User input is often invalid
fn parse_config(input: &str) -> Config {
    toml::from_str(input).expect("invalid config")  // Crashes on typo
}

// Files may not exist
fn load_settings() -> Settings {
    let content = fs::read_to_string("settings.json")
        .expect("settings not found");  // Crashes if missing
    serde_json::from_str(&content).expect("invalid settings")
}

// Custom panic for validation
fn process_age(age: i32) {
    if age < 0 {
        panic!("age cannot be negative");  // Should return error
    }
}
```

## good
```rust
// Return errors for expected failures
fn fetch_data(url: &str) -> Result<Data, FetchError> {
    let response = reqwest::blocking::get(url)
        .context("failed to connect")?;
    let data = response.json()
        .context("failed to parse response")?;
    Ok(data)
}

// Validate and return Result
fn parse_config(input: &str) -> Result<Config, ConfigError> {
    toml::from_str(input).map_err(ConfigError::Parse)
}

// Handle missing files gracefully
fn load_settings() -> Result<Settings, SettingsError> {
    let content = fs::read_to_string("settings.json")?;
    let settings = serde_json::from_str(&content)?;
    Ok(settings)
}

// Return error for validation failure
fn process_age(age: i32) -> Result<(), ValidationError> {
    if age < 0 {
        return Err(ValidationError::NegativeAge);
    }
    Ok(())
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
- err-expect-bugs-only
- err-result-over-panic
