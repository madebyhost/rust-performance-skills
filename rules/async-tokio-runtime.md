# async-tokio-runtime

## id
async-tokio-runtime

## severity
high

## trigger
Configure Tokio runtime appropriately for your workload. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
// Default runtime for everything - not optimal
#[tokio::main]
async fn main() {
    // CPU-heavy work on async executor starves IO tasks
    for data in datasets {
        let result = heavy_computation(data).await;
    }
}

// Single-threaded when multi-threaded is needed
#[tokio::main(flavor = "current_thread")]
async fn main() {
    // Can't utilize multiple cores for concurrent tasks
    for _ in 0..1000 {
        tokio::spawn(async { /* IO work */ });
    }
}
```

## good
```rust
// Multi-threaded for concurrent IO (default)
#[tokio::main]
async fn main() {
    // Good for many concurrent network connections
    let handles: Vec<_> = urls.iter()
        .map(|url| tokio::spawn(fetch(url.clone())))
        .collect();

    futures::future::join_all(handles).await;
}

// Current-thread for single-threaded scenarios
#[tokio::main(flavor = "current_thread")]
async fn main() {
    // Good for single-connection clients, simpler debugging
    let client = Client::new();
    client.run().await;
}

// Custom configuration
#[tokio::main(worker_threads = 4)]
async fn main() {
    // Limit to 4 worker threads
}

// Or manual setup for more control
fn main() {
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(4)
        .enable_all()
        .thread_name("my-worker")
        .build()
        .unwrap();

    runtime.block_on(async_main());
}
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
- async-no-lock-await
- async-spawn-blocking
