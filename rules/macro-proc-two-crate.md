# macro-proc-two-crate

## id
macro-proc-two-crate

## severity
medium

## trigger
Put procedural macros in a dedicated `proc-macro = true` crate and re-export from the facade. Trigger when working on macro API design and the code shows `macro`-class risk.

## bad
```rust
// A single crate with `proc-macro = true` in Cargo.toml that also tries
// to export regular items:
#[proc_macro_derive(Greet)]
pub fn derive_greet(input: TokenStream) -> TokenStream { /* ... */ }

pub trait Greet { fn greet(&self) -> String; } // error: a proc-macro crate
pub struct Config;                              // can only export proc-macros
```

## good
Split into a `proc-macro = true` crate plus a facade that re-exports it (full manifests and code below):

```rust
// users depend only on `mycrate`:
use mycrate::Greet;        // the trait
#[derive(mycrate::Greet)]  // the derive, re-exported from mycrate-derive
struct Robot;
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
- err-thiserror-lib
- macro-private-helpers
- macro-proc-syn-quote
- proj-workspace-deps
