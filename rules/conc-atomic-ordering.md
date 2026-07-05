# conc-atomic-ordering

## id
conc-atomic-ordering

## severity
high

## trigger
Use the weakest correct memory `Ordering` for every atomic operation. Trigger when working on concurrency and synchronization and the code shows `conc`-class risk.

## bad
```rust
use std::sync::atomic::{AtomicU64, AtomicBool, Ordering};

static COUNTER: AtomicU64 = AtomicU64::new(0);
static READY: AtomicBool = AtomicBool::new(false);
static mut DATA: u64 = 0;

// SeqCst everywhere - correct, but unnecessarily expensive
fn increment() {
    COUNTER.fetch_add(1, Ordering::SeqCst);
}

fn producer() {
    unsafe { DATA = 42; }
    READY.store(true, Ordering::SeqCst); // overkill for a single flag
}

fn consumer() -> Option<u64> {
    if READY.load(Ordering::SeqCst) {
        Some(unsafe { DATA })
    } else {
        None
    }
}
```

## good
```rust
use std::sync::atomic::{AtomicU64, AtomicBool, Ordering};

static COUNTER: AtomicU64 = AtomicU64::new(0);

// Relaxed: no ordering relative to other memory - fine for independent counters
fn increment() {
    COUNTER.fetch_add(1, Ordering::Relaxed);
}

fn total() -> u64 {
    COUNTER.load(Ordering::Relaxed)
}

// Acquire/Release: paired handoff - producer writes data THEN sets flag (Release);
// consumer loads flag (Acquire) and is guaranteed to see the preceding write.
static READY: AtomicBool = AtomicBool::new(false);
static VALUE: AtomicU64 = AtomicU64::new(0);

fn producer(value: u64) {
    VALUE.store(value, Ordering::Relaxed);   // write payload first
    READY.store(true, Ordering::Release);    // publish with Release
}

fn consumer() -> Option<u64> {
    if READY.load(Ordering::Acquire) {       // synchronize with Release store
        Some(VALUE.load(Ordering::Relaxed))  // payload visible after Acquire
    } else {
        None
    }
}

// SeqCst: only when you need a single total order across *multiple* atomics.
// Example: Dekker-style mutual exclusion involving two independent flags.
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not add shared mutable state, atomics, or lock-free structures when ownership transfer or single-threaded design is simpler.

## verification
Use stress tests, loom where practical, and contention measurements for shared state.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- conc-scoped-threads
- own-mutex-interior
- test-loom-concurrency
