# perf-entry-api

## id
perf-entry-api

## severity
medium

## trigger
Use entry API for map insert-or-update. Trigger when working on performance patterns and the code shows `perf`-class risk.

## bad
```rust
use std::collections::HashMap;

// Double lookup: contains_key + insert
fn increment(map: &mut HashMap<String, u32>, key: String) {
    if map.contains_key(&key) {
        *map.get_mut(&key).unwrap() += 1;
    } else {
        map.insert(key, 1);
    }
}

// Double lookup with get + insert
fn get_or_insert(map: &mut HashMap<String, Vec<i32>>, key: String) -> &mut Vec<i32> {
    if !map.contains_key(&key) {
        map.insert(key.clone(), Vec::new());
    }
    map.get_mut(&key).unwrap()
}

// Triple lookup pattern
fn update_or_default(map: &mut HashMap<String, Config>, key: &str, value: i32) {
    match map.get(key) {
        Some(config) => {
            let mut new_config = config.clone();
            new_config.value = value;
            map.insert(key.to_string(), new_config);
        }
        None => {
            map.insert(key.to_string(), Config::default());
        }
    }
}
```

## good
```rust
use std::collections::HashMap;
use std::collections::hash_map::Entry;

// Single lookup with entry
fn increment(map: &mut HashMap<String, u32>, key: String) {
    *map.entry(key).or_insert(0) += 1;
}

// Single lookup, returns mutable reference
fn get_or_insert(map: &mut HashMap<String, Vec<i32>>, key: String) -> &mut Vec<i32> {
    map.entry(key).or_insert_with(Vec::new)
}

// Single lookup with and_modify
fn update_or_default(map: &mut HashMap<String, Config>, key: String, value: i32) {
    map.entry(key)
        .and_modify(|config| config.value = value)
        .or_insert_with(Config::default);
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
- coll-map-choice
- mem-with-capacity
- perf-drain-reuse
- perf-extend-batch
