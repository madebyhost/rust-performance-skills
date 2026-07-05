# api-parse-dont-validate

## id
api-parse-dont-validate

## severity
high

## trigger
Parse into validated types at boundaries. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
// Validation scattered throughout codebase
fn send_email(email: &str) -> Result<(), Error> {
    // Did someone validate this already? Who knows!
    if !is_valid_email(email) {
        return Err(Error::InvalidEmail);
    }
    // Send email...
}

fn add_to_mailing_list(email: &str) -> Result<(), Error> {
    // Duplicate validation, or did we forget?
    if !is_valid_email(email) {
        return Err(Error::InvalidEmail);
    }
    // Add to list...
}

// Easy to forget validation
fn process_user_email(email: &str) {
    // Oops, no validation!
    database.store_email(email);
}
```

## good
```rust
/// A validated email address.
/// Can only be constructed via `Email::parse()`.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Email(String);

impl Email {
    /// Parses and validates an email address.
    pub fn parse(s: impl Into<String>) -> Result<Self, EmailError> {
        let s = s.into();
        if Self::is_valid(&s) {
            Ok(Email(s))
        } else {
            Err(EmailError::Invalid)
        }
    }

    fn is_valid(s: &str) -> bool {
        s.contains('@') && s.len() > 3  // Simplified
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

// Now functions can accept Email - guaranteed valid!
fn send_email(email: &Email) -> Result<(), Error> {
    // No validation needed - Email is always valid
    smtp_send(email.as_str())
}

fn add_to_mailing_list(email: Email) {
    // No validation needed
    list.push(email);
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not over-generalize a public API before real consumers or compatibility constraints exist.

## verification
Compile examples, run semver checks for public APIs, and add tests for boundary behavior.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-newtype-safety
- api-typestate
- conv-tryfrom-fallible
- serde-try-from-validate
- type-newtype-validated
