# pat-matches-macro

## id
pat-matches-macro

## severity
medium

## trigger
Use `matches!()` for boolean pattern tests. Trigger when working on pattern matching and the code shows `pat`-class risk.

## bad
```rust
enum Status {
    Active,
    Pending,
    Closed,
}

fn is_active(s: &Status) -> bool {
    match s {
        Status::Active => true,
        _ => false,
    }
}

fn is_small_digit(n: u32) -> bool {
    match n {
        1..=9 => true,
        _ => false,
    }
}

fn is_positive(opt: Option<i32>) -> bool {
    match opt {
        Some(v) if v > 0 => true,
        _ => false,
    }
}
```

## good
```rust
enum Status {
    Active,
    Pending,
    Closed,
}

fn is_active(s: &Status) -> bool {
    matches!(s, Status::Active)
}

fn is_small_digit(n: u32) -> bool {
    matches!(n, 1..=9)
}

fn is_positive(opt: Option<i32>) -> bool {
    matches!(opt, Some(v) if v > 0)
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
- name-is-has-bool
- pat-exhaustive-enum
