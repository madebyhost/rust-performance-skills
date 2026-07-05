# perf-iter-over-index

## id
perf-iter-over-index

## severity
medium

## trigger
Prefer iterators over manual indexing. Trigger when working on performance patterns and the code shows `perf`-class risk.

## bad
```rust
// Manual indexing - bounds checked every iteration
fn sum_squares(data: &[i32]) -> i64 {
    let mut sum = 0i64;
    for i in 0..data.len() {
        sum += (data[i] as i64) * (data[i] as i64);
    }
    sum
}

// Index-based iteration with multiple collections
fn dot_product(a: &[f64], b: &[f64]) -> f64 {
    let mut sum = 0.0;
    for i in 0..a.len().min(b.len()) {
        sum += a[i] * b[i];
    }
    sum
}

// Mutating with indices
fn double_values(data: &mut [i32]) {
    for i in 0..data.len() {
        data[i] *= 2;
    }
}
```

## good
```rust
// Iterator - bounds checks eliminated, SIMD-friendly
fn sum_squares(data: &[i32]) -> i64 {
    data.iter()
        .map(|&x| (x as i64) * (x as i64))
        .sum()
}

// Zip iterators - no manual length handling
fn dot_product(a: &[f64], b: &[f64]) -> f64 {
    a.iter()
        .zip(b.iter())
        .map(|(&x, &y)| x * y)
        .sum()
}

// Mutable iteration
fn double_values(data: &mut [i32]) {
    for x in data.iter_mut() {
        *x *= 2;
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
- anti-index-over-iter
- conc-rayon-par-iter
- opt-bounds-check
- perf-iter-lazy
