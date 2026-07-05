# perf-drain-reuse

## id
perf-drain-reuse

## severity
medium

## trigger
Use drain to reuse allocations. Trigger when working on performance patterns and the code shows `perf`-class risk.

## bad
```rust
// Allocates new Vec every iteration
fn process_batches(data: Vec<Item>) {
    let mut remaining = data;

    while !remaining.is_empty() {
        let batch: Vec<_> = remaining.drain(..100.min(remaining.len())).collect();
        process_batch(batch);
        // remaining keeps its capacity - good
        // but batch allocates new every time - bad
    }
}

// Clears and reallocates
fn reuse_buffer() {
    for _ in 0..1000 {
        let mut buffer = Vec::new();  // Allocates each iteration
        fill_buffer(&mut buffer);
        process(&buffer);
    }
}
```

## good
```rust
// Reuses allocation with drain
fn process_batches(mut data: Vec<Item>) {
    let mut batch = Vec::with_capacity(100);

    while !data.is_empty() {
        batch.extend(data.drain(..100.min(data.len())));
        process_batch(&batch);
        batch.clear();  // Keeps capacity
    }
}

// Reuses buffer across iterations
fn reuse_buffer() {
    let mut buffer = Vec::new();

    for _ in 0..1000 {
        buffer.clear();  // Keeps capacity
        fill_buffer(&mut buffer);
        process(&buffer);
    }
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply when the path is cold, unmeasured, or the optimization makes correctness and maintenance worse than the measured gain.

## verification
Measure before and after with a benchmark that captures the suspected bottleneck.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- mem-reuse-collections
- mem-with-capacity
- perf-extend-batch
