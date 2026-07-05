# async-clone-before-await

## id
async-clone-before-await

## severity
high

## trigger
Clone Arc/Rc data before await points to avoid holding references across suspension. Trigger when working on async runtime and cancellation and the code shows `async`-class risk.

## bad
```rust
use std::sync::Arc;

async fn process(data: Arc<Data>) {
    // Borrow extends across await - future is not Send
    let slice = &data.items[..];  // Borrow of Arc contents

    expensive_async_operation().await;  // Await with active borrow

    use_slice(slice);  // Still using the borrow
}

// Error: future cannot be sent between threads safely
// because `&[Item]` cannot be sent between threads safely
tokio::spawn(process(data));
```

## good
```rust
use std::sync::Arc;

async fn process(data: Arc<Data>) {
    // Clone what you need before await
    let items = data.items.clone();  // Owned Vec

    expensive_async_operation().await;

    use_items(&items);  // Using owned data
}

// Or clone the Arc itself
async fn share_data(data: Arc<Data>) {
    let data = data.clone();  // Another Arc handle

    some_async_work().await;

    process(&data);  // Safe - we own the Arc
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
- async-spawn-blocking
- own-arc-shared
