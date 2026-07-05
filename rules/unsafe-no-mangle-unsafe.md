# unsafe-no-mangle-unsafe

## id
unsafe-no-mangle-unsafe

## severity
critical

## trigger
In Rust 2024, write `#[unsafe(no_mangle)]`, `#[unsafe(export_name = "...")]`, and `#[unsafe(link_section = "...")]` - not the bare attribute forms.. Trigger when working on unsafe soundness and the code shows `unsafe`-class risk.

## bad
```rust
// Rust 2021 - bare attributes accepted, no warning about linker UB
#[no_mangle]
pub extern "C" fn init() {
    // ...
}

#[export_name = "plugin_entry"]
pub fn plugin_main() {
    // ...
}

#[link_section = ".init_array"]
static INIT: extern "C" fn() = init;
```

## good
```rust
// Rust 2024 - unsafe(...) wrapper makes the risk explicit
#[unsafe(no_mangle)]
pub extern "C" fn init() {
    // ...
}

#[unsafe(export_name = "plugin_entry")]
pub fn plugin_main() {
    // ...
}

#[unsafe(link_section = ".init_array")]
static INIT: extern "C" fn() = init;
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not use unsafe to silence the borrow checker without a written invariant and a safe abstraction boundary.

## verification
Require SAFETY documentation, Miri or sanitizer coverage where possible, and safe-wrapper tests.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- type-repr-transparent
- unsafe-extern-block
