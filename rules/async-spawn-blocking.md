# async-spawn-blocking

## id
async-spawn-blocking

## severity
high

## trigger
Use `spawn_blocking` for CPU-intensive work. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
// BAD: Blocks the async runtime thread
async fn process_image(data: &[u8]) -> ProcessedImage {
    // CPU-intensive work on async thread!
    let resized = resize_image(data);      // Blocks!
    let compressed = compress(resized);     // Blocks!
    compressed
}

// BAD: Synchronous file I/O in async context
async fn read_large_file(path: &Path) -> Vec<u8> {
    std::fs::read(path).unwrap()  // Blocks the runtime!
}
```

## good
```rust
use tokio::task;

// GOOD: Offload CPU work to blocking pool
async fn process_image(data: Vec<u8>) -> ProcessedImage {
    task::spawn_blocking(move || {
        let resized = resize_image(&data);
        compress(resized)
    })
    .await
    .expect("spawn_blocking failed")
}

// GOOD: Use async file I/O
async fn read_large_file(path: &Path) -> tokio::io::Result<Vec<u8>> {
    tokio::fs::read(path).await
}

// GOOD: Or spawn_blocking for unavoidable sync I/O
async fn read_with_sync_lib(path: PathBuf) -> Vec<u8> {
    task::spawn_blocking(move || {
        sync_library::read_file(&path)
    })
    .await
    .unwrap()
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
- async-no-lock-await
- async-tokio-fs
