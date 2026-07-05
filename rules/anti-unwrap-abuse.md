# anti-unwrap-abuse

## id
anti-unwrap-abuse

## severity
reference

## trigger
Don't use `.unwrap()` in production code. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// Crashes if file doesn't exist
let content = std::fs::read_to_string("config.toml").unwrap();

// Crashes on invalid input
let num: i32 = user_input.parse().unwrap();

// Crashes if key missing
let value = map.get("key").unwrap();

// Crashes if channel closed
let msg = receiver.recv().unwrap();
```

## good
```rust
// Propagate with ?
fn load_config() -> Result<Config, Error> {
    let content = std::fs::read_to_string("config.toml")?;
    Ok(toml::from_str(&content)?)
}

// Provide default
let num: i32 = user_input.parse().unwrap_or(0);

// Handle missing key
let value = map.get("key").ok_or(Error::MissingKey)?;

// Or use if-let
if let Some(value) = map.get("key") {
    process(value);
}

// Channel with proper handling
match receiver.recv() {
    Ok(msg) => handle(msg),
    Err(_) => break,  // Channel closed
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
- anti-expect-lazy
- err-question-mark
- err-result-over-panic
