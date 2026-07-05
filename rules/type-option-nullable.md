# type-option-nullable

## id
type-option-nullable

## severity
medium

## trigger
Use `Option<T>` for values that might not exist. Trigger when working on type-system invariants and the code shows `type`-class risk.

## bad
```rust
// Sentinel values - easy to forget to check
fn find_user(id: u64) -> User {
    // Returns "empty" user if not found - caller might not check
    users.get(&id).cloned().unwrap_or(User::empty())
}

// Nullable-style with raw pointers
fn find_user(id: u64) -> *const User {
    // Null if not found - unsafe, no compiler help
}

// Error-prone usage
let user = find_user(42);
println!("{}", user.name);  // Might be empty user - silent bug
```

## good
```rust
// Option makes absence explicit
fn find_user(id: u64) -> Option<User> {
    users.get(&id).cloned()
}

// Must handle the None case
let user = find_user(42);
match user {
    Some(u) => println!("{}", u.name),
    None => println!("User not found"),
}

// Or use combinators
let name = find_user(42)
    .map(|u| u.name)
    .unwrap_or_else(|| "Unknown".to_string());
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
- err-no-unwrap-prod
- type-enum-states
- type-result-fallible
