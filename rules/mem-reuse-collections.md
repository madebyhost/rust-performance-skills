# mem-reuse-collections

## id
mem-reuse-collections

## severity
critical

## trigger
Clear and reuse collections instead of creating new ones in loops. Trigger when working on memory and allocation and the code shows `mem`-class risk.

## bad
```rust
fn process_batches(batches: &[Batch]) -> Vec<Result> {
    let mut results = Vec::new();

    for batch in batches {
        let mut temp = Vec::new();  // Allocates every iteration

        for item in &batch.items {
            temp.push(transform(item));
        }

        results.push(aggregate(&temp));
        // temp dropped here, deallocation
    }

    results
}

fn format_lines(items: &[Item]) -> String {
    let mut output = String::new();

    for item in items {
        let line = format!("{}: {}", item.name, item.value);  // Allocates
        output.push_str(&line);
        output.push('\n');
    }

    output
}
```

## good
```rust
fn process_batches(batches: &[Batch]) -> Vec<Result> {
    let mut results = Vec::with_capacity(batches.len());
    let mut temp = Vec::new();  // Allocate once outside loop

    for batch in batches {
        temp.clear();  // Reuse allocation, just reset length

        for item in &batch.items {
            temp.push(transform(item));
        }

        results.push(aggregate(&temp));
        // temp keeps its capacity for next iteration
    }

    results
}

fn format_lines(items: &[Item]) -> String {
    use std::fmt::Write;

    let mut output = String::new();
    let mut line = String::new();  // Reusable buffer

    for item in items {
        line.clear();
        write!(&mut line, "{}: {}", item.name, item.value).unwrap();
        output.push_str(&line);
        output.push('\n');
    }

    output
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
- mem-clone-from
- mem-with-capacity
- mem-write-over-format
