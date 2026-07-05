# mem-clone-from

## id
mem-clone-from

## severity
critical

## trigger
Use `clone_from()` to reuse allocations when repeatedly cloning. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
let mut buffer = String::with_capacity(1024);

for source in sources {
    buffer = source.clone();  // Drops old allocation, allocates new
    process(&buffer);
}

// Each iteration:
// 1. Drops buffer's 1024-byte allocation
// 2. Allocates new memory for source.clone()
// Allocator thrashing!
```

## good
```rust
let mut buffer = String::with_capacity(1024);

for source in sources {
    buffer.clone_from(source);  // Reuses allocation if capacity sufficient
    process(&buffer);
}

// If source.len() <= 1024, no allocation happens
// Just copies bytes into existing buffer
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
- mem-reuse-collections
- mem-with-capacity
- own-clone-explicit
