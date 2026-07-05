# coll-set-membership

## id
coll-set-membership

## severity
medium

## trigger
Use `HashSet`/`BTreeSet` for membership tests and dedup, not linear `Vec::contains`. Trigger when working on collections and the code shows `coll`-class risk.

## bad
```rust
fn find_common(all_users: &[String], active_ids: &[String]) -> Vec<String> {
    let mut common = Vec::new();
    for user in all_users {
        // O(n) per iteration -> O(n * m) total
        if active_ids.contains(user) {
            common.push(user.clone());
        }
    }
    common
}

fn deduplicate(items: Vec<String>) -> Vec<String> {
    let mut seen: Vec<String> = Vec::new();
    for item in items {
        // O(n) per item - quadratic overall
        if !seen.contains(&item) {
            seen.push(item);
        }
    }
    seen
}
```

## good
```rust
use std::collections::{BTreeSet, HashSet};

// O(n + m): build the set once, then test each user in O(1).
fn find_common(all_users: &[String], active_ids: &[String]) -> Vec<String> {
    let active: HashSet<&String> = active_ids.iter().collect();
    all_users
        .iter()
        .filter(|u| active.contains(u))
        .cloned()
        .collect()
}

// Dedup while preserving order: track seen items in a HashSet.
fn deduplicate_ordered(items: Vec<String>) -> Vec<String> {
    let mut seen = HashSet::with_capacity(items.len());
    items.into_iter().filter(|s| seen.insert(s.clone())).collect()
}

// Dedup into a sorted, unique collection - use BTreeSet.
fn unique_sorted(items: Vec<String>) -> Vec<String> {
    items.into_iter().collect::<BTreeSet<_>>().into_iter().collect()
}

fn main() {
    let users = vec!["alice".to_string(), "bob".to_string(), "carol".to_string()];
    let active = vec!["bob".to_string(), "carol".to_string(), "dave".to_string()];
    println!("{:?}", find_common(&users, &active)); // ["bob", "carol"]

    let raw = vec!["x".to_string(), "y".to_string(), "x".to_string(), "z".to_string()];
    println!("{:?}", deduplicate_ordered(raw)); // ["x", "y", "z"]
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
- coll-map-choice
- perf-ahash
