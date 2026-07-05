# coll-map-choice

## id
coll-map-choice

## severity
medium

## trigger
Pick the map by access pattern: `HashMap` (fast, unordered), `BTreeMap` (sorted / range queries), `IndexMap` (insertion order). Trigger when working on collections and the code shows `coll`-class risk.

## bad
```rust
use std::collections::HashMap;

fn word_counts(text: &str) -> HashMap<&str, usize> {
    let mut counts = HashMap::new();
    for word in text.split_whitespace() {
        *counts.entry(word).or_insert(0) += 1;
    }
    counts
    // Iterating this for a report produces random order every run.
    // Caller has to sort externally - meaning repeated, avoidable work.
}

fn main() {
    let counts = word_counts("the quick brown fox jumps over the lazy dog");
    // Non-deterministic output: order changes between runs.
    for (word, count) in &counts {
        println!("{word}: {count}");
    }
}
```

## good
```rust
// --- 1. HashMap: default, fast, unordered ---
use std::collections::HashMap;

fn total_scores<'a>(records: &[(&'a str, u32)]) -> HashMap<&'a str, u32> {
    let mut scores: HashMap<&'a str, u32> = HashMap::new();
    for &(name, score) in records {
        *scores.entry(name).or_insert(0) += score;
    }
    scores
}

// --- 2. BTreeMap: sorted keys, range queries ---
use std::collections::BTreeMap;

fn events_in_range(
    log: &BTreeMap<u64, String>,
    start: u64,
    end: u64,
) -> Vec<(&u64, &String)> {
    // range() is only possible because BTreeMap keeps keys sorted.
    log.range(start..=end).collect()
}

fn build_log() -> BTreeMap<u64, String> {
    let mut log = BTreeMap::new();
    log.insert(1_000, "server started".to_string());
    log.insert(2_000, "request received".to_string());
    log.insert(3_000, "response sent".to_string());
    log
}

// --- 3. IndexMap: insertion order + O(1) lookup ---
use indexmap::IndexMap;

fn parse_config(pairs: &[(&str, &str)]) -> IndexMap<String, String> {
    // Keys iterated in the order they were inserted - deterministic output.
    pairs
        .iter()
        .map(|(k, v)| (k.to_string(), v.to_string()))
        .collect()
}

fn main() {
    // BTreeMap range query
    let log = build_log();
    let window = events_in_range(&log, 1_000, 2_500);
    for (ts, msg) in window {
        println!("{ts}: {msg}");
    }

    // IndexMap preserves insertion order
    let cfg = parse_config(&[("host", "localhost"), ("port", "8080"), ("debug", "true")]);
    for (k, v) in &cfg {
        println!("{k} = {v}"); // always: host, port, debug
    }
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
- coll-seq-choice
- perf-ahash
- perf-entry-api
