# type-no-stringly

## id
type-no-stringly

## severity
medium

## trigger
Avoid stringly-typed APIs; use enums, newtypes, or validated types. Trigger when working on type-system invariants and the code shows `type`-class risk.

## bad
```rust
// Status as string - easy to get wrong
fn set_status(status: &str) {
    match status {
        "pending" => { ... }
        "active" => { ... }
        "completed" => { ... }
        _ => panic!("Unknown status"),  // Runtime error
    }
}

// Easy to misuse
set_status("pending");   // OK
set_status("Pending");   // Runtime error - wrong case
set_status("aktive");    // Runtime error - typo
set_status("done");      // Runtime error - wrong word

// Configuration as strings
fn configure(key: &str, value: &str) {
    // No type safety, no validation
}
```

## good
```rust
// Status as enum - compile-time safety
enum Status {
    Pending,
    Active,
    Completed,
}

fn set_status(status: Status) {
    match status {
        Status::Pending => { ... }
        Status::Active => { ... }
        Status::Completed => { ... }
    }  // Exhaustive - compiler checks all cases
}

// Can only pass valid values
set_status(Status::Pending);  // OK
set_status(Status::Aktivev);  // Compile error - typo caught!

// Configuration with typed builder
struct Config {
    timeout: Duration,
    retries: u32,
    mode: Mode,
}

enum Mode { Fast, Safe, Balanced }
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
- anti-stringly-typed
- type-enum-states
- type-newtype-validated
