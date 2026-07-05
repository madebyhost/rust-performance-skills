# mem-drop-order

## id
mem-drop-order

## severity
critical

## trigger
Know and control drop order: struct fields drop top-to-bottom, locals in reverse. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
use std::sync::{Mutex, MutexGuard};

struct DatabaseSession {
    // BUG: `guard` is declared first, so it drops FIRST.
    // But `guard` protects the connection - dropping the lock
    // before the transaction is committed lets another thread
    // see the connection in a partial state.
    guard: MutexGuard<'static, ()>,
    transaction: Transaction,
}

struct Transaction; // pretend this commits on drop

impl Drop for Transaction {
    fn drop(&mut self) {
        println!("transaction committed");
    }
}
```

In this struct, `guard` drops before `transaction`, releasing the mutex while the transaction is still in-flight.

## good
```rust
use std::sync::{Mutex, MutexGuard};

struct Transaction; // commits on drop

impl Drop for Transaction {
    fn drop(&mut self) {
        println!("transaction committed");
    }
}

struct DatabaseSession {
    // CORRECT: `transaction` is declared first, so it drops first
    // (commit happens), THEN `guard` drops (lock released).
    transaction: Transaction,
    guard: MutexGuard<'static, ()>,
}
```

Fields drop in declaration order, so the field at the top of the struct drops first.

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply when ownership is required for correctness, lifetime complexity would dominate the API, or measurement shows no meaningful allocation/copy cost.

## verification
Measure allocations, copies, cache misses, and benchmark deltas on representative inputs.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- mem-take-replace
- own-mutex-interior
- test-fixture-raii
