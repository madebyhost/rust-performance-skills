# async-oneshot-response

## id
async-oneshot-response

## severity
high

## trigger
Use `oneshot` channel for request-response patterns. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
// Using mpsc for single response - wasteful
let (tx, mut rx) = mpsc::channel::<Response>(1);
send_request().await;
let response = rx.recv().await.unwrap();
// Channel persists, could accidentally receive more

// Using shared state - complex
let result = Arc::new(Mutex::new(None));
send_request(result.clone()).await;
while result.lock().await.is_none() {
    tokio::time::sleep(Duration::from_millis(10)).await;  // Polling!
}
```

## good
```rust
use tokio::sync::oneshot;

let (tx, rx) = oneshot::channel::<Response>();

// Send request with reply channel
send_request(Request { data, reply: tx }).await;

// Wait for response
let response = rx.await?;

// Channel is consumed - can't accidentally reuse
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
- async-select-racing
