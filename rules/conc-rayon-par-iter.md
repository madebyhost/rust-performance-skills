# conc-rayon-par-iter

## id
conc-rayon-par-iter

## severity
high

## trigger
Use rayon's `par_iter()` for CPU-bound data parallelism. Trigger when working on concurrency and synchronization and the code shows `conc`-class risk.

## bad
```rust
// single-threaded - wastes available cores on a CPU-bound workload
fn sum_squares(data: &[f64]) -> f64 {
    data.iter().map(|x| x * x).sum()
}

fn normalize(data: &mut [f64]) {
    let max = data.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    data.iter_mut().for_each(|x| *x /= max);
}
```

## good
```rust
use rayon::prelude::*;

fn sum_squares(data: &[f64]) -> f64 {
    data.par_iter().map(|x| x * x).sum()
}

fn normalize(data: &mut [f64]) {
    let max = data.par_iter().cloned().reduce(|| f64::NEG_INFINITY, f64::max);
    data.par_iter_mut().for_each(|x| *x /= max);
}

fn keep_positive(data: &[f64]) -> Vec<f64> {
    data.par_iter().copied().filter(|&x| x > 0.0).collect()
}

fn sort_large(data: &mut [f64]) {
    // parallel unstable sort - faster than std sort for large slices
    data.par_sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not add shared mutable state, atomics, or lock-free structures when ownership transfer or single-threaded design is simpler.

## verification
Use stress tests, loom where practical, and contention measurements for shared state.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- async-spawn-blocking
- conc-scoped-threads
- perf-iter-over-index
