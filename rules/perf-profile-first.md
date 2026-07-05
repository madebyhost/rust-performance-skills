# perf-profile-first

## id
perf-profile-first

## severity
medium

## trigger
Profile before optimizing. Trigger when working on performance patterns and the code shows `perf`-class risk.

## bad
```rust
// Optimizing without measuring
fn process(data: &[Item]) -> Vec<Output> {
    // "I bet this clone is slow..."
    let cloned: Vec<_> = data.iter().cloned().collect();

    // Actually, 99% of time is spent here:
    cloned.iter().map(|x| expensive_computation(x)).collect()
}

// Over-engineering rarely-called code
#[inline(always)]
fn rarely_called() {
    // This runs once at startup...
}
```

## good
```rust
// 1. Profile first
// cargo flamegraph --bin myapp
// cargo instruments -t time --bin myapp (macOS)

// 2. Find the actual bottleneck
// Flamegraph shows expensive_computation takes 95% of time

// 3. Optimize the hot spot
fn process(data: &[Item]) -> Vec<Output> {
    // Clone is fine - only 1% of time
    let cloned: Vec<_> = data.iter().cloned().collect();

    // Focus optimization HERE
    cloned.par_iter()  // Parallelize the expensive part
        .map(|x| expensive_computation(x))
        .collect()
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
- anti-premature-optimize
- opt-lto-release
- test-criterion-bench
