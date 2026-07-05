# pat-exhaustive-enum

## id
pat-exhaustive-enum

## severity
medium

## trigger
Match owned enums exhaustively; avoid catch-all `_` that hides new variants. Trigger when working on pattern matching and the code shows `pat`-class risk.

## bad
```rust
#[derive(Debug)]
enum Status {
    Active,
    Pending,
    Closed,
}

fn describe(s: &Status) -> &'static str {
    match s {
        Status::Active => "active",
        _ => "inactive", // hides Status::Pending silently; adding a new variant goes unnoticed
    }
}
```

If `Status::Suspended` is later added, `describe` compiles and silently returns `"inactive"` for it - a logic bug the compiler never catches.

## good
```rust
#[derive(Debug)]
enum Status {
    Active,
    Pending,
    Closed,
}

fn describe(s: &Status) -> &'static str {
    match s {
        Status::Active => "active",
        Status::Pending => "pending",
        Status::Closed => "closed",
        // Adding Status::Suspended now causes a compile error here - intended.
    }
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
- pat-matches-macro
- type-enum-states
