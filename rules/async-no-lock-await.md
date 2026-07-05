# async-no-lock-await

## id
async-no-lock-await

## severity
high

## trigger
Never hold `Mutex`/`RwLock` across `.await`. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
use tokio::sync::Mutex;

async fn bad_update(state: &Mutex<State>) {
    let mut guard = state.lock().await;

    // BAD: Lock held across await!
    let data = fetch_from_network().await;

    guard.value = data;
}  // Lock finally released

// This can deadlock or starve other tasks
```

## good
```rust
use tokio::sync::Mutex;

async fn good_update(state: &Mutex<State>) {
    // Fetch data BEFORE taking the lock
    let data = fetch_from_network().await;

    // Lock only for the quick update
    let mut guard = state.lock().await;
    guard.value = data;
}  // Lock released immediately

// Alternative: Clone data out, process, then update
async fn good_update_v2(state: &Mutex<State>) {
    // Extract what we need
    let id = {
        let guard = state.lock().await;
        guard.id.clone()
    };  // Lock released!

    // Do async work without lock
    let data = fetch_by_id(id).await;

    // Quick update
    state.lock().await.value = data;
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
- anti-lock-across-await
- async-clone-before-await
- async-spawn-blocking
