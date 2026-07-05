# macro-export-crate-path

## id
macro-export-crate-path

## severity
medium

## trigger
Export declarative macros with `#[macro_export]` and a clean import path. Trigger when working on macro API design and the code shows `macro`-class risk.

## bad
```rust
// lib.rs - legacy style
// Requires callers to write `#[macro_use] extern crate mylib;`
// and dumps all macros into the caller's global scope.
macro_rules! greet {
    ($name:expr) => {
        println!("hello, {}", $name);
    };
}
```

```rust
// consumer/src/main.rs - legacy
#[macro_use]
extern crate mylib; // order-sensitive; pollutes namespace

fn main() {
    greet!("world");
}
```

## good
```rust
// lib.rs - modern style
#[macro_export]
macro_rules! greet {
    ($name:expr) => {
        $crate::__private::print_greeting($name);
    };
}

// Re-export so `use mylib::greet;` resolves through the crate's public path.
// (The re-export is implicit when using #[macro_export]; this is just for clarity
// or when you want to place it under a module path.)
pub use greet;
```

```rust
// consumer/src/main.rs - modern
use mylib::greet;

fn main() {
    greet!("world");
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
- macro-private-helpers
- macro-rules-hygiene
- proj-workspace-deps
