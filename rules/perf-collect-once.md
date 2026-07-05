# perf-collect-once

## id
perf-collect-once

## severity
medium

## trigger
Don't collect intermediate iterators. Trigger when working on performance patterns and the code shows `perf`-class risk.

## bad
```rust
// Three allocations, three passes
fn process_users(users: Vec<User>) -> Vec<String> {
    let active: Vec<_> = users.into_iter()
        .filter(|u| u.is_active)
        .collect();

    let verified: Vec<_> = active.into_iter()
        .filter(|u| u.is_verified)
        .collect();

    verified.into_iter()
        .map(|u| u.name)
        .collect()
}

// Collecting to count
fn count_valid(items: &[Item]) -> usize {
    items.iter()
        .filter(|i| i.is_valid())
        .collect::<Vec<_>>()  // Unnecessary!
        .len()
}
```

## good
```rust
// One allocation, one pass
fn process_users(users: Vec<User>) -> Vec<String> {
    users.into_iter()
        .filter(|u| u.is_active)
        .filter(|u| u.is_verified)
        .map(|u| u.name)
        .collect()
}

// No allocation needed
fn count_valid(items: &[Item]) -> usize {
    items.iter()
        .filter(|i| i.is_valid())
        .count()
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
- mem-with-capacity
- perf-iter-lazy
