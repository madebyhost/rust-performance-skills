# mem-thinvec

## id
mem-thinvec

## severity
critical

## trigger
Use `ThinVec<T>` for nullable collections with minimal overhead. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
struct TreeNode {
    value: i32,
    // Each node pays 24 bytes for children, even leaves
    children: Vec<TreeNode>,  // Most nodes are leaves with empty Vec
}

// Or using Option<Vec<T>>
struct SparseData {
    // Option<Vec> = 24 bytes (Vec is never null-pointer optimized)
    tags: Option<Vec<String>>,
    metadata: Option<Vec<Metadata>>,
    // 48 bytes for usually-None fields
}
```

## good
```rust
use thin_vec::ThinVec;

struct TreeNode {
    value: i32,
    // Empty ThinVec is just a null pointer - 8 bytes
    children: ThinVec<TreeNode>,
}

struct SparseData {
    // ThinVec empty = 8 bytes each
    tags: ThinVec<String>,
    metadata: ThinVec<Metadata>,
    // 16 bytes vs 48 bytes
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
- mem-boxed-slice
- mem-smallvec
- mem-with-capacity
