# anti-collect-intermediate

## id
anti-collect-intermediate

## severity
reference

## trigger
Don't collect intermediate iterators. Trigger when working on anti-patterns and the code shows `anti`-class risk.

## bad
```rust
// Three allocations, three passes
fn process(data: Vec<i32>) -> Vec<i32> {
    let step1: Vec<_> = data.into_iter()
        .filter(|x| *x > 0)
        .collect();

    let step2: Vec<_> = step1.into_iter()
        .map(|x| x * 2)
        .collect();

    step2.into_iter()
        .filter(|x| *x < 100)
        .collect()
}

// Collecting just to check length
fn has_valid_items(items: &[Item]) -> bool {
    let valid: Vec<_> = items.iter()
        .filter(|i| i.is_valid())
        .collect();
    !valid.is_empty()
}

// Collecting to iterate again
fn sum_valid(items: &[Item]) -> i64 {
    let valid: Vec<_> = items.iter()
        .filter(|i| i.is_valid())
        .collect();
    valid.iter().map(|i| i.value).sum()
}
```

## good
```rust
// Single allocation, single pass
fn process(data: Vec<i32>) -> Vec<i32> {
    data.into_iter()
        .filter(|x| *x > 0)
        .map(|x| x * 2)
        .filter(|x| *x < 100)
        .collect()
}

// No allocation - iterator short-circuits
fn has_valid_items(items: &[Item]) -> bool {
    items.iter().any(|i| i.is_valid())
}

// No intermediate allocation
fn sum_valid(items: &[Item]) -> i64 {
    items.iter()
        .filter(|i| i.is_valid())
        .map(|i| i.value)
        .sum()
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
- perf-collect-once
- perf-iter-lazy
- perf-iter-over-index
