# conc-scoped-threads

## id
conc-scoped-threads

## severity
high

## trigger
Use `std::thread::scope` to borrow stack data across threads. Trigger when working on concurrency and synchronization and the code shows `conc`-class risk.

## bad
```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn parallel_sum(data: &[i64]) -> i64 {
    // Arc + clone just to share a slice - heap overhead, boilerplate
    let data = Arc::new(data.to_vec()); // unnecessary clone of entire slice
    let mid = data.len() / 2;

    let data1 = Arc::clone(&data);
    let h1 = thread::spawn(move || data1[..mid].iter().sum::<i64>());

    let data2 = Arc::clone(&data);
    let h2 = thread::spawn(move || data2[mid..].iter().sum::<i64>());

    h1.join().unwrap() + h2.join().unwrap()
}
```

## good
```rust
use std::thread;

fn parallel_sum(data: &[i64]) -> i64 {
    let mid = data.len() / 2;
    let (left, right) = data.split_at(mid);

    thread::scope(|s| {
        let h1 = s.spawn(|| left.iter().sum::<i64>());
        let h2 = s.spawn(|| right.iter().sum::<i64>());
        h1.join().unwrap() + h2.join().unwrap()
    })
}

// Mutable borrows work too - as long as they don't alias
fn parallel_fill(left: &mut [u8], right: &mut [u8]) {
    thread::scope(|s| {
        s.spawn(|| left.fill(0xAA));
        s.spawn(|| right.fill(0xBB));
    });
    // both halves have been written; scope guarantees completion
}
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
- async-spawn-blocking
- conc-rayon-par-iter
- own-arc-shared
