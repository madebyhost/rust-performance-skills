# unsafe-maybeuninit

## id
unsafe-maybeuninit

## severity
critical

## trigger
Use `MaybeUninit<T>` for uninitialized memory; never use `mem::uninitialized()` or `mem::zeroed()` for types with validity invariants.. Trigger when working on unsafe soundness and the code shows `unsafe`-class risk.

## bad
```rust
use std::mem;

// Instant UB: `bool` has validity invariants; uninitialized bits are not
// guaranteed to be 0 or 1. The optimizer may miscompile code that follows.
let b: bool = unsafe { mem::uninitialized() };

// Also UB for references - a zero reference is immediately invalid.
let r: &u32 = unsafe { mem::zeroed() };

// Uninitialized array the wrong way - triggers UB during construction.
let mut buf: [u8; 1024] = unsafe { mem::uninitialized() };
```

## good
```rust
use std::mem::MaybeUninit;

// ---- 1. Single value ----
let mut x = MaybeUninit::<u32>::uninit();
x.write(42);
// SAFETY: we just wrote a valid u32 via `write`, so the value is initialized.
let value: u32 = unsafe { x.assume_init() };

// ---- 2. Array initialization (manual, element-by-element) ----
// `[const { MaybeUninit::uninit() }; N]` works for any `T` (no `Copy` bound).
let mut buf: [MaybeUninit<u8>; 1024] = [const { MaybeUninit::uninit() }; 1024];
for elem in &mut buf {
    elem.write(0u8);
}
// SAFETY: every element was written above.
// `From<[MaybeUninit<T>; N]> for MaybeUninit<[T; N]>` is stable since Rust 1.95.
let buf: [u8; 1024] = unsafe {
    MaybeUninit::<[u8; 1024]>::from(buf).assume_init()
};

// ---- 3. Growing a Vec into spare capacity ----
fn fill_vec(v: &mut Vec<u8>, extra: usize) {
    v.reserve(extra);
    let spare = v.spare_capacity_mut(); // &mut [MaybeUninit<u8>]
    for slot in spare.iter_mut().take(extra) {
        slot.write(0u8);
    }
    // SAFETY: we initialized `extra` elements in the spare capacity.
    unsafe { v.set_len(v.len() + extra) };
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
- mem-with-capacity
- unsafe-safety-comment
