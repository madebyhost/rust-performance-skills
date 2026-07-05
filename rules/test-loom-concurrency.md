# test-loom-concurrency

## id
test-loom-concurrency

## severity
medium

## trigger
Use `loom` to exhaustively test lock-free and concurrent code. Trigger when working on testing strategy and the code shows `test`-class risk.

## bad
```rust
// Stress test: might pass a billion times, still doesn't prove correctness
#[test]
fn stress_test_flag() {
    use std::sync::{Arc, atomic::{AtomicBool, Ordering}};
    let flag = Arc::new(AtomicBool::new(false));
    for _ in 0..1_000_000 {
        let flag = Arc::clone(&flag);
        std::thread::spawn(move || {
            flag.store(true, Ordering::Relaxed);
        });
    }
    // races may never surface under the OS scheduler used here
}
```

## good
Gate concurrent primitives behind `#[cfg(loom)]` so the same code runs with loom's instrumented types during model checking and with std types in production:

```rust
// src/flag.rs
#[cfg(loom)]
use loom::sync::atomic::{AtomicBool, Ordering};
#[cfg(not(loom))]
use std::sync::atomic::{AtomicBool, Ordering};

pub struct Flag(AtomicBool);

impl Flag {
    pub const fn new() -> Self {
        Self(AtomicBool::new(false))
    }

    pub fn set(&self) {
        self.0.store(true, Ordering::Release);
    }

    pub fn is_set(&self) -> bool {
        self.0.load(Ordering::Acquire)
    }
}
```

```rust
// tests/loom_flag.rs  (or inside a #[cfg(loom)] mod in the crate)
#[cfg(loom)]
mod tests {
    use loom::sync::Arc;
    use super::Flag;

    #[test]
    fn flag_set_visible_to_other_thread() {
        loom::model(|| {
            let flag = Arc::new(Flag::new());

            let flag2 = Arc::clone(&flag);
            let writer = loom::thread::spawn(move || {
                flag2.set();
            });

            // All interleavings: either writer runs first or reader does.
            // loom verifies the Acquire/Release pair holds in both cases.
            let seen = flag.is_set();
            writer.join().unwrap();

            // After join, writer must have completed; flag must be set.
            assert!(flag.is_set(), "flag must be set after join");
            // 'seen' may be false if reader ran before writer - that is valid.
            let _ = seen;
        });
    }
}
```

Run loom tests with the feature flag:

```bash
RUSTFLAGS="--cfg loom" cargo test --test loom_flag
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Verify the test fails before the fix and covers the intended behavior rather than implementation detail.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- conc-atomic-ordering
- test-criterion-bench
