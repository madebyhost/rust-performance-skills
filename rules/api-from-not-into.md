# api-from-not-into

## id
api-from-not-into

## severity
high

## trigger
Implement `From<T>`, not `Into<U>` - From gives you Into for free. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
struct UserId(u64);

// Non-idiomatic: implementing Into directly
impl Into<UserId> for u64 {
    fn into(self) -> UserId {
        UserId(self)
    }
}

// Works, but now you can't use From syntax
let id = UserId::from(42);  // Error: From not implemented
let id: UserId = 42.into(); // Works, but limited
```

## good
```rust
struct UserId(u64);

// Idiomatic: implement From
impl From<u64> for UserId {
    fn from(id: u64) -> Self {
        UserId(id)
    }
}

// Now both work automatically
let id = UserId::from(42);   // From syntax
let id: UserId = 42.into();  // Into syntax (via blanket impl)

// And Into bound works in generics
fn process(id: impl Into<UserId>) {
    let id: UserId = id.into();
}
process(42u64);  // Works!
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
- api-impl-into
- api-newtype-safety
- conv-fromstr-parsing
- conv-tryfrom-fallible
- err-from-impl
