# unsafe-safety-comment

## id
unsafe-safety-comment

## severity
critical

## trigger
Write a `// SAFETY:` comment above every `unsafe` block and a `# Safety` section in every `unsafe fn`.. Trigger when working on unsafe soundness and the code shows `unsafe`-class risk.

## bad
```rust
// unsafe fn with no # Safety section - caller has no idea what's required
pub unsafe fn read_at(ptr: *const u8, offset: usize) -> u8 {
    // no SAFETY comment - why is this dereference sound?
    unsafe { *ptr.add(offset) }
}

// standalone block with no justification
fn process(slice: &[u8]) -> u8 {
    unsafe { *slice.as_ptr().add(10) }
}
```

## good
```rust
/// Returns the byte at `ptr + offset`.
///
/// # Safety
///
/// - `ptr` must be valid for reads for at least `offset + 1` bytes.
/// - `ptr` must not be null and must be properly aligned for `u8`.
/// - The memory must not be mutated for the duration of this call.
pub unsafe fn read_at(ptr: *const u8, offset: usize) -> u8 {
    // SAFETY: caller guarantees ptr is valid for at least offset + 1 bytes,
    // so ptr.add(offset) is in bounds and dereferenceable.
    unsafe { *ptr.add(offset) }
}

fn process(slice: &[u8]) -> Option<u8> {
    if slice.len() > 10 {
        // SAFETY: we just checked that slice has at least 11 elements,
        // so index 10 is within bounds.
        Some(unsafe { *slice.as_ptr().add(10) })
    } else {
        None
    }
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
- doc-safety-section
- lint-unsafe-doc
- unsafe-minimize-scope
