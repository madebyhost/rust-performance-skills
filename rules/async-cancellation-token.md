# async-cancellation-token

## id
async-cancellation-token

## severity
high

## trigger
Use `CancellationToken` for graceful shutdown and task cancellation. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
// Dropping handle doesn't stop the task
let handle = tokio::spawn(async {
    loop {
        do_work().await;
    }
});

drop(handle);  // Task continues running in background!

// Using bool flag - not async-aware
let running = Arc::new(AtomicBool::new(true));

tokio::spawn({
    let running = running.clone();
    async move {
        while running.load(Ordering::Relaxed) {
            do_work().await;  // Can't wake up if blocked here
        }
    }
});

running.store(false, Ordering::Relaxed);
// Task won't stop until current do_work() completes
```

## good
```rust
use tokio_util::sync::CancellationToken;

let token = CancellationToken::new();

let handle = tokio::spawn({
    let token = token.clone();
    async move {
        loop {
            tokio::select! {
                _ = token.cancelled() => {
                    println!("Shutting down gracefully");
                    cleanup().await;
                    break;
                }
                _ = do_work() => {
                    // Work completed
                }
            }
        }
    }
});

// Later: trigger cancellation
token.cancel();
handle.await?;  // Task completes cleanly
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
- async-joinset-structured
- async-select-racing
- async-tokio-runtime
