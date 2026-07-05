# name-variants-camel

## id
name-variants-camel

## severity
medium

## trigger
Use `UpperCamelCase` for enum variants. Trigger when working on naming and readability and the code shows `name`-class risk.

## bad
```rust
enum Status {
    pending,       // warning: variant `pending` should have an upper camel case name
    in_progress,   // warning
    COMPLETED,     // Not idiomatic
}

enum Color {
    RED,           // Screaming case - not Rust style
    GREEN,
    BLUE,
}
```

## good
```rust
enum Status {
    Pending,
    InProgress,
    Completed,
    Failed,
}

enum Color {
    Red,
    Green,
    Blue,
    Custom(u8, u8, u8),
}

enum HttpMethod {
    Get,
    Post,
    Put,
    Delete,
    Patch,
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
- name-types-camel
- type-enum-states
