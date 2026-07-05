# mem-assert-type-size

## id
mem-assert-type-size

## severity
critical

## trigger
Use static assertions to guard against accidental type size growth. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
struct Event {
    timestamp: u64,
    kind: EventKind,
    payload: [u8; 32],
}

// Later, someone adds a field without realizing the impact
struct Event {
    timestamp: u64,
    kind: EventKind,
    payload: [u8; 32],
    metadata: String,  // Silently adds 24 bytes!
}

// 10 million events now use 240MB more memory
// No warning, no review trigger
```

## good
```rust
struct Event {
    timestamp: u64,
    kind: EventKind,
    payload: [u8; 32],
}

// Static assertion - breaks compile if size changes
const _: () = assert!(std::mem::size_of::<Event>() == 48);

// Or with static_assertions crate
use static_assertions::assert_eq_size;
assert_eq_size!(Event, [u8; 48]);

// Now adding metadata triggers compile error:
// error: assertion failed: std::mem::size_of::<Event>() == 48
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
- mem-box-large-variant
- mem-smaller-integers
- opt-cache-friendly
