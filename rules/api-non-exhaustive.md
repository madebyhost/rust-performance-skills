# api-non-exhaustive

## id
api-non-exhaustive

## severity
high

## trigger
Use `#[non_exhaustive]` on public enums and structs for forward compatibility. Trigger when working on public API design and the code shows `api`-class risk.

## bad
```rust
// Public enum - adding variant breaks downstream matches
pub enum ErrorKind {
    NotFound,
    PermissionDenied,
    TimedOut,
}

// Downstream code
match error.kind() {
    ErrorKind::NotFound => ...,
    ErrorKind::PermissionDenied => ...,
    ErrorKind::TimedOut => ...,
    // No wildcard - will break when you add ErrorKind::Interrupted
}

// Public struct - adding field breaks downstream construction
pub struct Config {
    pub name: String,
    pub value: i32,
}

// Downstream code
let config = Config { name: "test".into(), value: 42 };
// Will break when you add `pub enabled: bool`
```

## good
```rust
// Can add variants in minor versions
#[non_exhaustive]
pub enum ErrorKind {
    NotFound,
    PermissionDenied,
    TimedOut,
    // Future: can add Interrupted here without breaking changes
}

// Downstream code MUST have wildcard
match error.kind() {
    ErrorKind::NotFound => ...,
    ErrorKind::PermissionDenied => ...,
    ErrorKind::TimedOut => ...,
    _ => ...,  // Required by non_exhaustive
}

// Can add fields in minor versions
#[non_exhaustive]
pub struct Config {
    pub name: String,
    pub value: i32,
}

// Downstream CANNOT use struct literal syntax
// let config = Config { name: "test".into(), value: 42 };  // Error!

// Must use constructor
impl Config {
    pub fn new(name: impl Into<String>, value: i32) -> Self {
        Config { name: name.into(), value }
    }
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
- api-builder-pattern
- api-sealed-trait
- err-custom-type
