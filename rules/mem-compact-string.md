# mem-compact-string

## id
mem-compact-string

## severity
critical

## trigger
Use compact string types for memory-constrained string storage. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
struct User {
    id: u64,
    // Most usernames are < 24 chars, but String is always 24 bytes + heap
    username: String,
    email: String,
}

// 1 million users = 24 bytes * 2 * 1M = 48MB just for String metadata
// Plus all the heap allocations for actual content
```

## good
```rust
use compact_str::CompactString;

struct User {
    id: u64,
    // CompactString: 24 bytes, but strings <= 23 bytes are inline (no heap)
    username: CompactString,
    email: CompactString,
}

// Most usernames fit inline = zero heap allocations
// Same memory footprint as String but way fewer allocations
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
- mem-boxed-slice
- mem-smallvec
- own-cow-conditional
