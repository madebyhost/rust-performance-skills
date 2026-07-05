# opt-cold-unlikely

## id
opt-cold-unlikely

## severity
high

## trigger
Mark unlikely code paths with `#[cold]` to help compiler optimization. Trigger when working on compiler optimization and the code shows `opt`-class risk.

## bad
```rust
// All branches treated equally
fn validate(input: &str) -> Result<Data, ValidationError> {
    if input.is_empty() {
        return Err(ValidationError::Empty);  // Rare
    }

    if input.len() > 1000 {
        return Err(ValidationError::TooLong);  // Rare
    }

    if !input.is_ascii() {
        return Err(ValidationError::NonAscii);  // Rare
    }

    // This is the common case
    Ok(parse_data(input))
}
```

## good
```rust
fn validate(input: &str) -> Result<Data, ValidationError> {
    if input.is_empty() {
        return cold_empty_error();
    }

    if input.len() > 1000 {
        return cold_too_long_error();
    }

    if !input.is_ascii() {
        return cold_non_ascii_error();
    }

    Ok(parse_data(input))
}

#[cold]
fn cold_empty_error() -> Result<Data, ValidationError> {
    Err(ValidationError::Empty)
}

#[cold]
fn cold_too_long_error() -> Result<Data, ValidationError> {
    Err(ValidationError::TooLong)
}

#[cold]
fn cold_non_ascii_error() -> Result<Data, ValidationError> {
    Err(ValidationError::NonAscii)
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply compiler hints globally or speculatively; keep them for measured hot paths and deployment-specific profiles.

## verification
Inspect release profile, generated code when useful, and benchmark hot paths before keeping the change.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- err-result-over-panic
- opt-inline-never-cold
- opt-likely-hint
