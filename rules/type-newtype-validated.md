# type-newtype-validated

## id
type-newtype-validated

## severity
medium

## trigger
Use newtypes to enforce validation at construction time. Trigger when working on type-system invariants and the code shows `type`-class risk.

## bad
```rust
// Validation scattered throughout code
fn send_email(to: &str, body: &str) -> Result<(), Error> {
    if !is_valid_email(to) {  // Must check every time
        return Err(Error::InvalidEmail);
    }
    // ...
}

fn add_recipient(list: &mut Vec<String>, email: &str) -> Result<(), Error> {
    if !is_valid_email(email) {  // Check again
        return Err(Error::InvalidEmail);
    }
    list.push(email.to_string());
    Ok(())
}
```

## good
```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Email(String);

impl Email {
    pub fn new(s: &str) -> Result<Self, EmailError> {
        if is_valid_email(s) {
            Ok(Email(s.to_string()))
        } else {
            Err(EmailError::Invalid(s.to_string()))
        }
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

// No validation needed - Email is always valid
fn send_email(to: &Email, body: &str) -> Result<(), Error> {
    // to is guaranteed valid
    send_to_address(to.as_str(), body)
}

fn add_recipient(list: &mut Vec<Email>, email: Email) {
    // email is guaranteed valid
    list.push(email);
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
- api-newtype-safety
- api-parse-dont-validate
- conv-fromstr-parsing
- serde-try-from-validate
- type-newtype-ids
