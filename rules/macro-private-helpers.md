# macro-private-helpers

## id
macro-private-helpers

## severity
medium

## trigger
Hide macro-generated helper items behind a `#[doc(hidden)] pub mod __private`. Trigger when working on macro API design and the code shows `macro`-class risk.

## bad
```rust
// lib.rs - helper leaks into the public API
pub fn __format_value(v: &dyn std::fmt::Debug) -> String {
    format!("{v:?}")
}

#[macro_export]
macro_rules! debug_print {
    ($val:expr) => {
        println!("{}", $crate::__format_value(&$val));
    };
}
```

```text
// A user sees `__format_value` in the docs and may depend on it.
// Removing it later is a semver-breaking change.
```

## good
```rust
// lib.rs

#[doc(hidden)]
pub mod __private {
    // Everything re-exported here is technically public (required for
    // macro call sites), but hidden from rendered docs and clearly
    // marked as an unstable implementation detail.
    pub use crate::helpers::format_value;
}

// Internal module - not public.
mod helpers {
    pub fn format_value(v: &dyn std::fmt::Debug) -> String {
        format!("{v:?}")
    }
}

#[macro_export]
macro_rules! debug_print {
    ($val:expr) => {
        // Reference through __private; never through the bare crate root.
        println!("{}", $crate::__private::format_value(&$val));
    };
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
- doc-all-public
- macro-proc-two-crate
- macro-rules-hygiene
