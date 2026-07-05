# perf-collect-into

## id
perf-collect-into

## severity
medium

## trigger
Use collect_into for reusing containers. Trigger when working on performance patterns and the code shows `perf`-class risk.

## bad
```rust
// Allocates new Vec each time
fn process_batches(batches: Vec<Vec<i32>>) -> Vec<Vec<i32>> {
    batches.into_iter()
        .map(|batch| {
            batch.into_iter()
                .filter(|x| *x > 0)
                .collect::<Vec<_>>()  // New allocation per batch
        })
        .collect()
}

// Can't reuse cleared buffer
fn filter_loop(data: &[Vec<i32>]) {
    for batch in data {
        let filtered: Vec<_> = batch.iter()
            .filter(|&&x| x > 0)
            .copied()
            .collect();  // New allocation each iteration
        process(&filtered);
    }
}
```

## good
Prefer the design encouraged by `perf-collect-into`: Use collect_into for reusing containers. Keep it explicit and testable.

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
- perf-drain-reuse
- perf-extend-batch
