# anti-lock-across-await

## id
anti-lock-across-await

## severity
reference

## trigger
Don't hold locks across await points. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
use std::sync::Mutex;
use tokio::sync::Mutex as AsyncMutex;

// DEADLOCK RISK: std::sync::Mutex held across await
async fn bad_std_mutex(data: &Mutex<Vec<i32>>) {
    let mut guard = data.lock().unwrap();
    do_async_work().await;  // Lock held during await!
    guard.push(42);
}

// BLOCKS OTHER TASKS: tokio Mutex held across await
async fn bad_async_mutex(data: &AsyncMutex<Vec<i32>>) {
    let mut guard = data.lock().await;
    slow_network_call().await;  // Lock held for entire call!
    guard.push(42);
}
```

## good
```rust
use std::sync::Mutex;
use tokio::sync::Mutex as AsyncMutex;

// Release lock before await
async fn good_approach(data: &Mutex<Vec<i32>>) {
    let value = {
        let guard = data.lock().unwrap();
        guard.last().copied()  // Extract what you need
    };  // Lock released here

    let result = do_async_work(value).await;

    {
        let mut guard = data.lock().unwrap();
        guard.push(result);
    }
}

// Minimize lock scope with async mutex
async fn good_async_mutex(data: &AsyncMutex<Vec<i32>>, item: i32) {
    // Quick lock, quick release
    data.lock().await.push(item);

    // Async work without lock
    let result = slow_network_call().await;

    // Quick lock again
    data.lock().await.push(result);
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply mechanically when it obscures intent, weakens correctness, or conflicts with local constraints.

## verification
Add focused tests or static checks that prove the intended behavior and prevent regression.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- async-clone-before-await
- async-no-lock-await
- own-mutex-interior
