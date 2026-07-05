# async-broadcast-pubsub

## id
async-broadcast-pubsub

## severity
high

## trigger
Use `broadcast` channel for pub/sub where all subscribers receive all messages. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
use tokio::sync::mpsc;

// mpsc only delivers to ONE consumer
let (tx, mut rx) = mpsc::channel::<Event>(100);

// Only one of these receives each message!
let mut rx2 = ???;  // Can't clone receiver
```

## good
```rust
use tokio::sync::broadcast;

// broadcast delivers to ALL subscribers
let (tx, _) = broadcast::channel::<Event>(100);

// Each subscriber gets ALL messages
let mut rx1 = tx.subscribe();
let mut rx2 = tx.subscribe();

tokio::spawn(async move {
    while let Ok(event) = rx1.recv().await {
        handle_in_logger(event);
    }
});

tokio::spawn(async move {
    while let Ok(event) = rx2.recv().await {
        handle_in_metrics(event);
    }
});

// Both subscribers receive this
tx.send(Event::UserLogin { user_id: 42 })?;
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
- async-bounded-channel
- async-mpsc-queue
- async-watch-latest
