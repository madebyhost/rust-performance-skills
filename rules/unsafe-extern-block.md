# unsafe-extern-block

## id
unsafe-extern-block

## severity
critical

## trigger
In Rust 2024, wrap `extern` blocks in `unsafe extern { }` and annotate each item as `safe` or `unsafe`.. Trigger when working on unsafe soundness and the code shows `unsafe`-class risk.

## bad
```rust
// Rust 2021 style - compiles but forbidden in 2024 edition
extern "C" {
    fn strlen(s: *const std::ffi::c_char) -> usize;
    fn memcpy(dst: *mut u8, src: *const u8, n: usize) -> *mut u8;
    static errno: std::ffi::c_int;
}
```

## good
```rust
// Rust 2024 style
unsafe extern "C" {
    // `strlen` is genuinely unsafe: caller must pass a null-terminated pointer.
    pub unsafe fn strlen(s: *const std::ffi::c_char) -> usize;

    // `memcpy` is unsafe: caller must ensure non-overlapping, valid regions.
    pub unsafe fn memcpy(dst: *mut u8, src: *const u8, n: usize) -> *mut u8;

    // A function that is always safe to call (hypothetical pure query).
    pub safe fn rust_version_major() -> u32;

    // Statics are unsafe to access unless you can guarantee no data races.
    pub unsafe static errno: std::ffi::c_int;
}

// Call sites remain unchanged for `unsafe` items:
fn copy_bytes(dst: *mut u8, src: *const u8, n: usize) {
    // SAFETY: dst and src are non-overlapping, both valid for n bytes.
    unsafe { memcpy(dst, src, n) };
}

// Call sites for `safe` items need no unsafe block:
fn show_version() {
    println!("major: {}", rust_version_major());
}
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
- unsafe-no-mangle-unsafe
