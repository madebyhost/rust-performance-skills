# type-result-fallible

## id
type-result-fallible

## severity
medium

## trigger
Use `Result<T, E>` for operations that can fail. Trigger when working on type-system invariants and the code shows `type`-class risk.

## bad
```rust
// Returning Option loses error context
fn read_config(path: &str) -> Option<Config> {
    let content = std::fs::read_to_string(path).ok()?;  // Why did it fail?
    toml::from_str(&content).ok()  // Parse error lost
}

// Panicking on errors
fn read_config(path: &str) -> Config {
    let content = std::fs::read_to_string(path).unwrap();  // Crashes
    toml::from_str(&content).unwrap()  // Crashes
}

// Sentinel values
fn divide(a: i32, b: i32) -> i32 {
    if b == 0 { return -1; }  // Magic value, easy to miss
    a / b
}
```

## good
```rust
// Result with clear error type
fn read_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(ConfigError::IoError)?;
    toml::from_str(&content)
        .map_err(ConfigError::ParseError)
}

fn divide(a: i32, b: i32) -> Result<i32, DivisionError> {
    if b == 0 {
        return Err(DivisionError::DivideByZero);
    }
    Ok(a / b)
}

// Caller must handle
match divide(10, 0) {
    Ok(result) => println!("Result: {}", result),
    Err(e) => println!("Error: {}", e),
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not encode every boolean as typestate; use the type system when it removes real invalid states.

## verification
Add constructor tests, compile-fail tests where useful, and property tests for invariants.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- err-question-mark
- err-thiserror-lib
- type-option-nullable
