# macro-rules-hygiene

## id
macro-rules-hygiene

## severity
medium

## trigger
Rely on `macro_rules!` hygiene and use `$crate` for paths to your crate's items. Trigger when working on macro API design and the code shows `macro`-class risk.

## bad
```rust
// lib.rs
pub fn log_value(v: &str) {
    println!("[log] {v}");
}

#[macro_export]
macro_rules! log {
    ($val:expr) => {
        // WRONG: `crate::` resolves relative to the *caller's* crate,
        // not to the crate that defined this macro.
        crate::log_value(&format!("{:?}", $val));
    };
}
```

```rust
// consumer/src/main.rs
use mylib::log;

fn main() {
    log!(42); // compile error: `crate::log_value` not found in consumer
}
```

## good
```rust
// lib.rs
pub fn log_value(v: &str) {
    println!("[log] {v}");
}

#[macro_export]
macro_rules! log {
    ($val:expr) => {
        // `$crate` always expands to the crate that defined this macro.
        $crate::log_value(&format!("{:?}", $val));
    };
}
```

```rust
// consumer/src/main.rs
use mylib::log;

fn main() {
    log!(42); // correctly calls mylib::log_value
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not write a macro when a function, trait, or const generic expresses the same idea clearly.

## verification
Add compile-pass and compile-fail tests covering exported macro paths and helper visibility.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- macro-export-crate-path
- macro-prefer-functions
- macro-private-helpers
