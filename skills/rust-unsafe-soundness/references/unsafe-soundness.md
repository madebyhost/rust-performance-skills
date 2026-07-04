# Unsafe Soundness Reference

## Minimum Documentation

```rust
// SAFETY: explain each invariant that makes this block sound.
unsafe { ... }

/// # Safety
/// Explain caller obligations.
pub unsafe fn api(...) { ... }
```

## Review Checklist

- pointer is non-null when required;
- pointer is aligned;
- memory is initialized;
- aliasing rules are respected;
- lifetimes outlive references;
- no data race is possible;
- panic cannot leak invalid state;
- manual `Send`/`Sync` is justified;
- layout assumptions are documented.

## Red Flags

- `unsafe` used to avoid borrow checker design;
- `transmute` where conversion APIs exist;
- `mem::zeroed` for references or invalid bit patterns;
- raw pointer API exposed to safe callers;
- `static mut`;
- missing `SAFETY` comments.

## Verification

- Run Miri for UB-prone code where supported.
- Run sanitizers for FFI or memory-heavy code.
- Fuzz parsers and protocol boundaries.
- Add tests for invalid inputs and panic paths.
