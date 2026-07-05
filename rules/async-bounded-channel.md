# async-bounded-channel

## id
async-bounded-channel

## severity
high

## trigger
Use bounded channels to apply backpressure and prevent unbounded memory growth. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
use tokio::sync::mpsc;

// Unbounded channel - can grow forever
let (tx, mut rx) = mpsc::unbounded_channel::<Message>();

// Fast producer, slow consumer = unbounded memory growth
tokio::spawn(async move {
    loop {
        let msg = generate_message();
        tx.send(msg).unwrap();  // Never blocks, never fails (until OOM)
    }
});

tokio::spawn(async move {
    while let Some(msg) = rx.recv().await {
        slow_process(msg).await;  // Can't keep up
    }
});
// Memory grows unboundedly until crash
```

## good
```rust
use tokio::sync::mpsc;

// Bounded channel - backpressure when full
let (tx, mut rx) = mpsc::channel::<Message>(100);  // Max 100 items

// Producer waits when channel full
tokio::spawn(async move {
    loop {
        let msg = generate_message();
        // Blocks if channel is full - natural backpressure
        tx.send(msg).await.unwrap();
    }
});

tokio::spawn(async move {
    while let Some(msg) = rx.recv().await {
        slow_process(msg).await;
    }
});
// Memory usage capped at ~100 messages
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
- async-mpsc-queue
- async-oneshot-response
- async-watch-latest
