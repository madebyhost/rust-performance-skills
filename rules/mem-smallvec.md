# mem-smallvec

## id
mem-smallvec

## severity
critical

## trigger
Use `SmallVec` for usually-small collections. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
// Always heap-allocates, even for 1-2 elements
fn get_path_components(path: &str) -> Vec<&str> {
    path.split('/').collect()  // Usually 2-4 components
}

// Always heap-allocates for error list
fn validate(input: &Input) -> Vec<ValidationError> {
    let mut errors = Vec::new();  // Usually 0-3 errors
    // validation logic...
    errors
}
```

## good
```rust
use smallvec::{smallvec, SmallVec};

// Stack-allocated for typical paths (1-8 components)
fn get_path_components(path: &str) -> SmallVec<[&str; 8]> {
    path.split('/').collect()
}

// Stack-allocated for typical error counts
fn validate(input: &Input) -> SmallVec<[ValidationError; 4]> {
    let mut errors = SmallVec::new();
    // validation logic...
    errors
}

// Using smallvec! macro
let v: SmallVec<[i32; 4]> = smallvec![1, 2, 3];
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
- mem-arrayvec
- mem-thinvec
- mem-with-capacity
