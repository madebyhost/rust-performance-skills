# doc-safety-section

## id
doc-safety-section

## severity
medium

## trigger
Include `# Safety` section for unsafe functions. Trigger when working on documentation and the code shows `doc`-class risk.

## bad
```rust
/// Reads a value from a raw pointer.
pub unsafe fn read_ptr<T>(ptr: *const T) -> T {
    // What guarantees must the caller provide? Unknown!
    ptr.read()
}

/// Creates a string from raw parts.
pub unsafe fn string_from_raw(ptr: *mut u8, len: usize, cap: usize) -> String {
    String::from_raw_parts(ptr, len, cap)
}
```

## good
```rust
/// Reads a value from a raw pointer.
///
/// # Safety
///
/// The caller must ensure that:
/// - `ptr` is valid for reads of `size_of::<T>()` bytes
/// - `ptr` is properly aligned for type `T`
/// - `ptr` points to a properly initialized value of type `T`
/// - The memory referenced by `ptr` is not mutated during this call
pub unsafe fn read_ptr<T>(ptr: *const T) -> T {
    ptr.read()
}

/// Creates a `String` from raw parts.
///
/// # Safety
///
/// The caller must guarantee that:
/// - `ptr` was allocated by the same allocator that `String` uses
/// - `len` is less than or equal to `cap`
/// - The first `len` bytes at `ptr` are valid UTF-8
/// - `cap` is the capacity that `ptr` was allocated with
/// - No other code will use `ptr` after this call (ownership is transferred)
///
/// Violating these requirements leads to undefined behavior including
/// memory corruption, use-after-free, or invalid UTF-8 in strings.
pub unsafe fn string_from_raw(ptr: *mut u8, len: usize, cap: usize) -> String {
    String::from_raw_parts(ptr, len, cap)
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
- doc-errors-section
- doc-panics-section
- lint-unsafe-doc
