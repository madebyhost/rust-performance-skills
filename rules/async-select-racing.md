# async-select-racing

## id
async-select-racing

## severity
high

## trigger
Use `select!` to race futures and handle the first to complete. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
// Can't express "whichever finishes first"
async fn fetch_with_fallback() -> Data {
    match fetch_primary().await {
        Ok(data) => data,
        Err(_) => fetch_fallback().await.unwrap(),  // Sequential, not racing
    }
}

// Manual timeout is error-prone
async fn fetch_with_timeout() -> Option<Data> {
    let start = Instant::now();
    loop {
        if start.elapsed() > Duration::from_secs(5) {
            return None;
        }
        // How do we check timeout while awaiting?
    }
}
```

## good
```rust
use tokio::select;

async fn fetch_with_timeout() -> Result<Data, Error> {
    select! {
        result = fetch_data() => result,
        _ = tokio::time::sleep(Duration::from_secs(5)) => {
            Err(Error::Timeout)
        }
    }
}

async fn fetch_with_fallback() -> Data {
    select! {
        result = fetch_primary() => {
            match result {
                Ok(data) => data,
                Err(_) => fetch_fallback().await.unwrap()
            }
        }
        _ = tokio::time::sleep(Duration::from_secs(1)) => {
            // Primary too slow, use fallback
            fetch_fallback().await.unwrap()
        }
    }
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
- async-bounded-channel
- async-cancellation-token
- async-join-parallel
