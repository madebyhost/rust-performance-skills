# unsafe-minimize-scope

## id
unsafe-minimize-scope

## severity
critical

## trigger
Keep `unsafe` blocks as small as possible - mark only the operation that requires unsafety, not the surrounding safe code.. Trigger when working on unsafe soundness and the code shows `unsafe`-class risk.

## bad
```rust
// Entire function body marked unsafe - safe arithmetic, bounds checks,
// and the single unsafe dereference are all equally "dangerous" to a reader.
unsafe fn sum_at(ptr: *const i32, len: usize, index: usize) -> i32 {
    let adjusted_len = len.saturating_sub(1); // safe - but looks unsafe
    assert!(index <= adjusted_len);           // safe - but looks unsafe
    let value = *ptr.add(index);              // the only actually unsafe op
    value + 1                                 // safe - but looks unsafe
}
```

```rust
// Huge unsafe block wrapping safe logic inside an unsafe fn (2024 edition
// now requires unsafe {} here anyway, but large blocks are still bad style).
pub unsafe fn process(ptr: *const u8, len: usize) -> Vec<u8> {
    unsafe {
        let mut result = Vec::with_capacity(len); // safe
        for i in 0..len {                         // safe
            result.push(*ptr.add(i));             // unsafe - buried in noise
        }
        result
    }
}
```

## good
```rust
// Safe wrapper: the single unsafe operation is clearly isolated.
fn sum_at(ptr: *const i32, len: usize, index: usize) -> i32 {
    assert!(index < len, "index out of bounds");
    // SAFETY: index < len guarantees ptr.add(index) is within the allocation.
    let value = unsafe { *ptr.add(index) };
    value + 1
}
```

```rust
// In a genuinely unsafe fn, 2024 edition still requires unsafe {} per op.
/// # Safety
///
/// `ptr` must be valid for reads for `len` bytes and properly aligned.
pub unsafe fn process(ptr: *const u8, len: usize) -> Vec<u8> {
    let mut result = Vec::with_capacity(len); // safe - outside any unsafe block
    for i in 0..len {
        // SAFETY: caller guarantees ptr is valid for len bytes; i < len.
        let byte = unsafe { *ptr.add(i) };
        result.push(byte);
    }
    result
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
- unsafe-safety-comment
- unsafe-send-sync-manual
