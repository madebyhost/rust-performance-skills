# lint-unsafe-doc

## id
lint-unsafe-doc

## severity
low

## trigger
Require documentation for unsafe blocks. Trigger when working on linting and the code shows `lint`-class risk.

## bad
```rust
pub fn read_data(ptr: *const u8, len: usize) -> &[u8] {
    unsafe {
        std::slice::from_raw_parts(ptr, len)  // WARN: undocumented
    }
}

impl Buffer {
    pub fn get_unchecked(&self, index: usize) -> &u8 {
        unsafe { self.data.get_unchecked(index) }  // WARN
    }
}
```

## good
```rust
pub fn read_data(ptr: *const u8, len: usize) -> &[u8] {
    // SAFETY: Caller guarantees:
    // - ptr is valid for reads of len bytes
    // - ptr is properly aligned for u8
    // - the memory is initialized
    // - no mutable references exist to this memory
    unsafe {
        std::slice::from_raw_parts(ptr, len)
    }
}

impl Buffer {
    pub fn get_unchecked(&self, index: usize) -> &u8 {
        debug_assert!(index < self.len(), "index out of bounds");
        // SAFETY: We verified index < len in debug builds.
        // Callers must ensure index is within bounds.
        unsafe { self.data.get_unchecked(index) }
    }
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Run cargo clippy with the intended lint level and document any allow with a narrow reason.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- doc-safety-section
- lint-deny-correctness
- type-repr-transparent
