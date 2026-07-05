# err-custom-type

## id
err-custom-type

## severity
critical

## trigger
Define custom error types for domain-specific failures. Trigger when working on error handling and the code shows `err`-class risk.

## bad
```rust
// Generic string errors - no structure
fn validate_user(user: &User) -> Result<(), String> {
    if user.name.is_empty() {
        return Err("Name is empty".to_string());
    }
    if user.age > 150 {
        return Err("Age is invalid".to_string());
    }
    Ok(())
}

// Caller can't match on specific errors
match validate_user(&user) {
    Ok(()) => save(user),
    Err(msg) => {
        // Can only do string comparison - fragile!
        if msg.contains("Name") {
            prompt_for_name()
        }
    }
}
```

## good
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ValidationError {
    #[error("name cannot be empty")]
    EmptyName,

    #[error("name exceeds maximum length of {max} characters")]
    NameTooLong { max: usize, actual: usize },

    #[error("invalid age {0}: must be between 0 and 150")]
    InvalidAge(u8),

    #[error("email format is invalid: {0}")]
    InvalidEmail(String),
}

fn validate_user(user: &User) -> Result<(), ValidationError> {
    if user.name.is_empty() {
        return Err(ValidationError::EmptyName);
    }
    if user.name.len() > 100 {
        return Err(ValidationError::NameTooLong {
            max: 100,
            actual: user.name.len()
        });
    }
    if user.age > 150 {
        return Err(ValidationError::InvalidAge(user.age));
    }
    Ok(())
}

// Caller can match specifically
match validate_user(&user) {
    Ok(()) => save(user),
    Err(ValidationError::EmptyName) => prompt_for_name(),
    Err(ValidationError::InvalidAge(age)) => {
        show_error(&format!("Please enter a valid age (you entered {})", age))
    }
    Err(e) => show_error(&e.to_string()),
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
- api-non-exhaustive
- err-anyhow-app
- err-thiserror-lib
