# mem-write-over-format

## id
mem-write-over-format

## severity
critical

## trigger
Use `write!()` into existing buffers instead of `format!()` allocations. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
fn log_event(event: &Event, output: &mut Vec<u8>) {
    // format! allocates a new String every call
    let line = format!(
        "[{}] {}: {}\n",
        event.timestamp,
        event.level,
        event.message
    );
    output.extend_from_slice(line.as_bytes());
}

fn build_response(items: &[Item]) -> String {
    let mut result = String::new();

    for item in items {
        // format! allocates for each item
        result.push_str(&format!("{}: {}\n", item.name, item.value));
    }

    result
}
```

## good
```rust
use std::fmt::Write;

fn log_event(event: &Event, output: &mut Vec<u8>) {
    use std::io::Write;
    // write! to Vec<u8> directly, no intermediate allocation
    write!(
        output,
        "[{}] {}: {}\n",
        event.timestamp,
        event.level,
        event.message
    ).unwrap();
}

fn build_response(items: &[Item]) -> String {
    use std::fmt::Write;

    let mut result = String::with_capacity(items.len() * 64);

    for item in items {
        // write! into existing String, reuses capacity
        write!(&mut result, "{}: {}\n", item.name, item.value).unwrap();
    }

    result
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
- mem-avoid-format
- mem-reuse-collections
- mem-with-capacity
