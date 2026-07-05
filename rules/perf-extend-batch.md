# perf-extend-batch

## id
perf-extend-batch

## severity
medium

## trigger
Use extend for batch insertions. Trigger when working on performance patterns and the code shows `perf`-class risk.

## bad
```rust
// Multiple potential reallocations
fn collect_results(sources: Vec<Source>) -> Vec<Result> {
    let mut results = Vec::new();

    for source in sources {
        for result in source.get_results() {
            results.push(result);  // May reallocate
        }
    }
    results
}

// Loop with push for known data
fn build_list() -> Vec<i32> {
    let mut list = Vec::new();
    for i in 0..1000 {
        list.push(i);  // Many reallocations
    }
    list
}

// Appending another collection
fn combine(mut a: Vec<i32>, b: Vec<i32>) -> Vec<i32> {
    for item in b {
        a.push(item);
    }
    a
}
```

## good
```rust
// Single extend with size hint
fn collect_results(sources: Vec<Source>) -> Vec<Result> {
    let mut results = Vec::new();

    for source in sources {
        results.extend(source.get_results());
    }
    results
}

// Direct collection from iterator
fn build_list() -> Vec<i32> {
    (0..1000).collect()
}

// Extend for combining
fn combine(mut a: Vec<i32>, b: Vec<i32>) -> Vec<i32> {
    a.extend(b);
    a
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
- perf-drain-reuse
