# async-joinset-structured

## id
async-joinset-structured

## severity
high

## trigger
Use `JoinSet` for managing dynamic collections of spawned tasks. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
// Manual handle management
let mut handles: Vec<JoinHandle<Result<Data>>> = Vec::new();

for url in urls {
    handles.push(tokio::spawn(fetch(url)));
}

// Wait for all, in order (not as they complete)
let results = futures::future::join_all(handles).await;

// No easy way to cancel all, handle errors progressively, or add more tasks
```

## good
```rust
use tokio::task::JoinSet;

let mut set = JoinSet::new();

for url in urls {
    set.spawn(fetch(url.clone()));
}

// Process results as they complete
while let Some(result) = set.join_next().await {
    match result {
        Ok(Ok(data)) => process(data),
        Ok(Err(e)) => log::error!("Task failed: {}", e),
        Err(e) => log::error!("Task panicked: {}", e),
    }
}

// All tasks done, set is empty
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
- async-cancellation-token
- async-join-parallel
- async-try-join
