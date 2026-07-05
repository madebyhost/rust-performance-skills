# async-watch-latest

## id
async-watch-latest

## severity
high

## trigger
Use `watch` channel for sharing the latest value with multiple observers. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
// Using broadcast when only latest value matters
let (tx, _) = broadcast::channel::<Config>(100);

// Receivers might process stale configs if they're slow
// And they waste time processing intermediate values

// Using mpsc with buffered stale values
let (tx, mut rx) = mpsc::channel::<Status>(100);
// Receiver might process outdated statuses
```

## good
```rust
use tokio::sync::watch;

let (tx, rx) = watch::channel(Config::default());

// Multiple observers
let rx1 = rx.clone();
let rx2 = rx.clone();

// Observer 1: waits for changes
tokio::spawn(async move {
    let mut rx = rx1;
    while rx.changed().await.is_ok() {
        let config = rx.borrow();
        apply_config(&*config);
    }
});

// Observer 2: also sees all changes
tokio::spawn(async move {
    let mut rx = rx2;
    while rx.changed().await.is_ok() {
        let config = rx.borrow();
        log_config_change(&*config);
    }
});

// Update the value
tx.send(Config::new())?;
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not force async for CPU-bound work without I/O concurrency; prefer threads or Rayon when they fit the workload.

## verification
Add concurrency tests, cancellation tests, and runtime checks for backpressure or lock scope.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- async-broadcast-pubsub
- async-cancellation-token
- async-mpsc-queue
