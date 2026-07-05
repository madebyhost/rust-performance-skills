# perf-iter-lazy

## id
perf-iter-lazy

## severity
medium

## trigger
Keep iterators lazy, collect only when needed. Trigger when working on performance patterns and the code shows `perf`-class risk.

## bad
```rust
// Collects intermediate results unnecessarily
fn process(data: Vec<i32>) -> Vec<i32> {
    let filtered: Vec<_> = data.into_iter()
        .filter(|x| *x > 0)
        .collect();  // Unnecessary allocation

    let mapped: Vec<_> = filtered.into_iter()
        .map(|x| x * 2)
        .collect();  // Another unnecessary allocation

    mapped.into_iter()
        .take(10)
        .collect()
}

// Collects before checking existence
fn has_positive(data: &[i32]) -> bool {
    let positives: Vec<_> = data.iter()
        .filter(|&&x| x > 0)
        .collect();  // Allocates entire filtered result

    !positives.is_empty()
}
```

## good
```rust
// Single chain, single collect
fn process(data: Vec<i32>) -> Vec<i32> {
    data.into_iter()
        .filter(|x| *x > 0)
        .map(|x| x * 2)
        .take(10)
        .collect()
}

// Short-circuits on first match
fn has_positive(data: &[i32]) -> bool {
    data.iter().any(|&x| x > 0)
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
- anti-collect-intermediate
- perf-collect-once
- perf-iter-over-index
