# serde-try-from-validate

## id
serde-try-from-validate

## severity
medium

## trigger
Validate while deserializing with `#[serde(try_from = "Raw")]`. Trigger when working on serialization compatibility and the code shows `serde`-class risk.

## bad
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Email(String);

impl Email {
    fn new(s: String) -> Result<Self, String> {
        if s.contains('@') {
            Ok(Email(s))
        } else {
            Err(format!("invalid email: {s}"))
        }
    }
}

// Caller must validate after deserialization - easy to forget:
fn process(json: &str) -> Result<(), Box<dyn std::error::Error>> {
    let email: Email = serde_json::from_str(json)?;
    // nothing stops "notanemail" from being deserialized and used
    println!("{:?}", email);
    Ok(())
}
```

## good
```rust
use serde::{Serialize, Deserialize};
use serde_json;

#[derive(Debug, Clone)]
struct Email(String);

impl TryFrom<String> for Email {
    type Error = String;

    fn try_from(s: String) -> Result<Self, Self::Error> {
        if s.contains('@') && !s.starts_with('@') && !s.ends_with('@') {
            Ok(Email(s))
        } else {
            Err(format!("invalid email address: {s}"))
        }
    }
}

// For the serialize direction: implement From<Email> for String, then add into = "String"
impl From<Email> for String {
    fn from(e: Email) -> String {
        e.0
    }
}

// Deserialize: serde reads a String, then calls Email::try_from - error if invalid.
// Serialize:   serde calls String::from(email) - converts back to the raw type.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(try_from = "String", into = "String")]
struct ValidatedEmail(String);

impl TryFrom<String> for ValidatedEmail {
    type Error = String;

    fn try_from(s: String) -> Result<Self, Self::Error> {
        if s.contains('@') && !s.starts_with('@') && !s.ends_with('@') {
            Ok(ValidatedEmail(s))
        } else {
            Err(format!("invalid email address: {s}"))
        }
    }
}

impl From<ValidatedEmail> for String {
    fn from(e: ValidatedEmail) -> String {
        e.0
    }
}

fn main() {
    // Valid email round-trips fine
    let good = serde_json::from_str::<ValidatedEmail>("\"user@example.com\"").unwrap();
    println!("{}", serde_json::to_string(&good).unwrap());

    // Invalid email is rejected at parse time - never enters the program
    let bad = serde_json::from_str::<ValidatedEmail>("\"notanemail\"");
    assert!(bad.is_err());
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not make serde strict when extension fields are expected or when backward compatibility requires tolerance.

## verification
Use golden fixtures, versioned payload tests, and compatibility checks for unknown or missing fields.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- api-parse-dont-validate
- serde-custom-with
- type-newtype-validated
