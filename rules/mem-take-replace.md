# mem-take-replace

## id
mem-take-replace

## severity
critical

## trigger
Use `mem::take` / `mem::replace` to move a value out of a `&mut` without cloning. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
struct Processor {
    items: Vec<String>,
}

impl Processor {
    // clones the entire Vec just to drain it - unnecessary allocation
    fn flush(&mut self) -> Vec<String> {
        let v = self.items.clone();
        self.items.clear();
        v
    }
}
```

## good
```rust
use std::mem;

struct Processor {
    items: Vec<String>,
}

impl Processor {
    // moves the Vec out in one step, leaving an empty Vec behind
    fn flush(&mut self) -> Vec<String> {
        mem::take(&mut self.items)
    }
}
```

`mem::take` is equivalent to `mem::replace(&mut self.items, Vec::new())` but shorter when the replacement value is `Default::default()`.

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
- mem-clone-from
- own-borrow-over-clone
- own-move-large
