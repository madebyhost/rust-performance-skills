# mem-with-capacity

## id
mem-with-capacity

## severity
critical

## trigger
Use `with_capacity()` when size is known. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
// Vec starts at capacity 0, reallocates at 4, 8, 16, 32...
let mut results = Vec::new();
for i in 0..1000 {
    results.push(process(i));  // ~10 reallocations!
}

// String grows similarly
let mut output = String::new();
for word in words {
    output.push_str(word);
    output.push(' ');
}

// HashMap default capacity is small
let mut map = HashMap::new();
for (k, v) in pairs {  // Many reallocations
    map.insert(k, v);
}
```

## good
```rust
// Pre-allocate exact size
let mut results = Vec::with_capacity(1000);
for i in 0..1000 {
    results.push(process(i));  // Zero reallocations!
}

// Or use collect with size hint (iterator provides capacity)
let results: Vec<_> = (0..1000).map(process).collect();

// Pre-allocate string
let estimated_len = words.iter().map(|w| w.len() + 1).sum();
let mut output = String::with_capacity(estimated_len);
for word in words {
    output.push_str(word);
    output.push(' ');
}

// Pre-allocate HashMap
let mut map = HashMap::with_capacity(pairs.len());
for (k, v) in pairs {
    map.insert(k, v);
}
```

## when
Apply when the rule's pattern is visible in production code, public API, hot path, or reusable library surface.

## when_not
Do not apply when ownership is required for correctness, lifetime complexity would dominate the API, or measurement shows no meaningful allocation/copy cost.

## verification
Measure allocations, copies, cache misses, and benchmark deltas on representative inputs.

## sources
- leonardomso/rust-skills: https://github.com/leonardomso/rust-skills
- Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

## related_rules
- coll-seq-choice
- mem-reuse-collections
- mem-smallvec
- perf-extend-batch
