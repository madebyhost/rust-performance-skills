# async-mpsc-queue

## id
async-mpsc-queue

## severity
high

## trigger
Use `mpsc` channels for async message queues between tasks. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
use std::sync::mpsc;  // Wrong! Blocks the async runtime

let (tx, rx) = std::sync::mpsc::channel();

tokio::spawn(async move {
    tx.send("hello").unwrap();  // Might block
});

tokio::spawn(async move {
    let msg = rx.recv().unwrap();  // BLOCKS the executor thread!
});
```

## good
```rust
use tokio::sync::mpsc;

let (tx, mut rx) = mpsc::channel::<String>(100);

tokio::spawn(async move {
    tx.send("hello".to_string()).await.unwrap();
});

tokio::spawn(async move {
    while let Some(msg) = rx.recv().await {
        println!("Received: {}", msg);
    }
});
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
- async-broadcast-pubsub
- async-oneshot-response
