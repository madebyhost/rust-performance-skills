# unsafe-send-sync-manual

## id
unsafe-send-sync-manual

## severity
critical

## trigger
Document the invariants when manually implementing `Send` or `Sync`; prefer letting the compiler derive them automatically.. Trigger when working on unsafe soundness and the code shows `unsafe`-class risk.

## bad
```rust
use std::cell::Cell;
use std::sync::Arc;

// Cell<T> is !Sync because it allows non-atomic interior mutation.
// This manual impl removes that protection with no explanation.
struct SharedCounter {
    value: Cell<u32>,
}

unsafe impl Sync for SharedCounter {} // data race waiting to happen - no SAFETY comment
unsafe impl Send for SharedCounter {} // likewise
```

```rust
// Wrapping a raw pointer but forgetting to opt out of auto-Send/Sync.
struct MyBuffer {
    ptr: *mut u8,
    len: usize,
}
// *mut u8 is already !Send + !Sync, so the compiler correctly withholds
// auto-impls - but if you blindly add unsafe impls without justification,
// you may send the pointer to another thread while something else mutates it.
unsafe impl Send for MyBuffer {}  // no SAFETY: comment - why is this sound?
```

## good
```rust
use std::marker::PhantomData;

// ---- 1. Opt OUT of Send/Sync using PhantomData ----
// If your type logically owns a *const T (e.g. an intrusive pointer),
// use PhantomData to prevent the compiler from auto-deriving Send/Sync.
struct IntrinsiveRef<T> {
    ptr: *const T,
    // PhantomData<*const T> makes this type !Send + !Sync automatically,
    // matching the semantics of a raw non-owning pointer.
    _marker: PhantomData<*const T>,
}
// No unsafe impl needed - the compiler correctly withholds Send/Sync.

// ---- 2. Opt IN with a documented unsafe impl ----
use std::sync::Mutex;

/// A buffer owned exclusively by one thread at a time.
/// The raw pointer always points to a heap allocation this struct owns;
/// no other reference to that allocation exists outside this struct.
struct OwnedBuffer {
    ptr: *mut u8,
    len: usize,
}

// SAFETY: OwnedBuffer owns its allocation exclusively (no aliasing),
// and access is protected by the caller's Mutex<OwnedBuffer> at usage sites.
// The pointer is valid for the entire lifetime of OwnedBuffer.
unsafe impl Send for OwnedBuffer {}

// SAFETY: OwnedBuffer exposes no shared mutation - all methods require &mut self.
// Concurrent & references cannot mutate the buffer.
unsafe impl Sync for OwnedBuffer {}

// ---- 3. Prefer newtype wrappers around Arc for sharing ----
// Instead of manual Sync, wrap in Arc<Mutex<T>> so the compiler handles it.
use std::sync::Arc;

struct SafeCounter {
    value: Mutex<u32>,
}

// Arc<Mutex<u32>> is Send + Sync automatically - no manual impl required.
fn make_shared() -> Arc<SafeCounter> {
    Arc::new(SafeCounter { value: Mutex::new(0) })
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
- own-arc-shared
- type-phantom-marker
- unsafe-safety-comment
