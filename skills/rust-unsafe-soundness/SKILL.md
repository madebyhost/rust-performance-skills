---
name: rust-unsafe-soundness
description: "Use for unsafe Rust design and review: raw pointers, transmute, MaybeUninit, NonNull, repr(C), manual Send/Sync, atomics, aliasing, alignment, initialization, lifetimes, panic safety, Miri, sanitizers, FFI soundness, and safe abstractions over unsafe code."
---

# Rust Unsafe Soundness

Use this skill before accepting any `unsafe` block or unsafe API. Load `references/unsafe-soundness.md` for details.

## Required Review

1. State why safe Rust is insufficient.
2. List invariants required by the unsafe code.
3. Confirm aliasing, alignment, initialization, lifetime, thread-safety, and panic-safety.
4. Encapsulate unsafe behind a safe API when possible.
5. Add or request Miri, sanitizer, fuzz, or targeted tests.

## Output

Return a soundness verdict: valid, plausible with gaps, or invalid. Include exact invariants and missing evidence.
