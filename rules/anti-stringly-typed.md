# anti-stringly-typed

## id
anti-stringly-typed

## severity
reference

## trigger
Don't use strings where enums or newtypes would provide type safety. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
fn process_order(status: &str, priority: &str) {
    // What are valid statuses? "pending"? "Pending"? "PENDING"?
    // What are valid priorities? "high"? "1"? "urgent"?
    match status {
        "pending" => { ... }
        "completed" => { ... }
        _ => panic!("unknown status"),  // Runtime error
    }
}

struct User {
    email: String,    // Any string, even "not an email"
    phone: String,    // Any string, even "hello"
    user_id: String,  // Could be confused with other string IDs
}

// Easy to make mistakes
process_order("complete", "high");  // Typo: "complete" vs "completed"
process_order("high", "pending");   // Swapped arguments - compiles!
```

## good
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum OrderStatus {
    Pending,
    Processing,
    Completed,
    Cancelled,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
enum Priority {
    Low,
    Medium,
    High,
    Critical,
}

fn process_order(status: OrderStatus, priority: Priority) {
    match status {
        OrderStatus::Pending => { ... }
        OrderStatus::Processing => { ... }
        OrderStatus::Completed => { ... }
        OrderStatus::Cancelled => { ... }
    }  // Exhaustive - compiler checks all cases
}

// Validated newtypes
struct Email(String);
struct PhoneNumber(String);
struct UserId(u64);

impl Email {
    pub fn new(s: &str) -> Result<Self, ValidationError> {
        if is_valid_email(s) {
            Ok(Email(s.to_string()))
        } else {
            Err(ValidationError::InvalidEmail)
        }
    }
}

struct User {
    email: Email,       // Must be valid email
    phone: PhoneNumber, // Must be valid phone
    user_id: UserId,    // Can't confuse with other IDs
}

// Compile errors catch mistakes
process_order(OrderStatus::Completed, Priority::High);  // Clear and correct
process_order(Priority::High, OrderStatus::Pending);    // Compile error!
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
- api-newtype-safety
- api-parse-dont-validate
- type-newtype-ids
