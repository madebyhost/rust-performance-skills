# own-cow-conditional

## id
own-cow-conditional

## severity
critical

## trigger
Use `Cow<'a, T>` for conditional ownership. Trigger when working on ownership and borrowing and the code shows `own`-class risk.

## bad
```rust
// Always allocates, even when input doesn't need modification
fn normalize_path(path: &str) -> String {
    if path.contains("//") {
        path.replace("//", "/")  // Allocation needed
    } else {
        path.to_string()  // Unnecessary allocation!
    }
}

// Always clones the error message
fn format_error(code: u32) -> String {
    match code {
        404 => "Not Found".to_string(),      // Unnecessary!
        500 => "Internal Error".to_string(), // Unnecessary!
        _ => format!("Error {}", code),      // This one needs allocation
    }
}
```

## good
```rust
use std::borrow::Cow;

// Only allocates when needed
fn normalize_path(path: &str) -> Cow<'_, str> {
    if path.contains("//") {
        Cow::Owned(path.replace("//", "/"))  // Allocate
    } else {
        Cow::Borrowed(path)  // Zero-cost borrow
    }
}

// Static strings stay borrowed
fn format_error(code: u32) -> Cow<'static, str> {
    match code {
        404 => Cow::Borrowed("Not Found"),      // No allocation
        500 => Cow::Borrowed("Internal Error"), // No allocation
        _ => Cow::Owned(format!("Error {}", code)), // Allocate only for unknown
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
- mem-avoid-format
- own-borrow-over-clone
