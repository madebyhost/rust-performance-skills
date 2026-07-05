# async-tokio-fs

## id
async-tokio-fs

## severity
high

## trigger
Use `tokio::fs` instead of `std::fs` in async code. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
async fn process_files(paths: &[PathBuf]) -> Result<Vec<String>> {
    let mut contents = Vec::new();

    for path in paths {
        // BLOCKS the entire executor thread!
        let data = std::fs::read_to_string(path)?;
        contents.push(data);
    }

    Ok(contents)
}

// While reading a file, NO other tasks can run on this thread
```

## good
```rust
use tokio::fs;

async fn process_files(paths: &[PathBuf]) -> Result<Vec<String>> {
    let mut contents = Vec::new();

    for path in paths {
        // Non-blocking: allows other tasks to run
        let data = fs::read_to_string(path).await?;
        contents.push(data);
    }

    Ok(contents)
}

// Even better: concurrent reads
async fn process_files_concurrent(paths: &[PathBuf]) -> Result<Vec<String>> {
    let futures: Vec<_> = paths.iter()
        .map(|path| fs::read_to_string(path))
        .collect();

    futures::future::try_join_all(futures).await
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
- async-spawn-blocking
- async-tokio-runtime
- err-context-chain
