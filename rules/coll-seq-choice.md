# coll-seq-choice

## id
coll-seq-choice

## severity
medium

## trigger
Default to `Vec`; use `VecDeque` for queue/deque behaviour; avoid `LinkedList`. Trigger when working on collections and the code shows `coll`-class risk.

## bad
```rust
fn process_queue(items: Vec<String>) {
    let mut queue = items;
    while !queue.is_empty() {
        // O(n): every element shifts left after removal.
        let item = queue.remove(0);
        println!("processing: {item}");
    }
}

fn main() {
    process_queue(vec![
        "first".to_string(),
        "second".to_string(),
        "third".to_string(),
    ]);
}
```

`remove(0)` on a `Vec` is O(n) because it must shift every remaining element. A loop of n items becomes O(n).

## good
```rust
use std::collections::VecDeque;

fn process_queue(items: impl IntoIterator<Item = String>) {
    // VecDeque: O(1) pop_front - the right tool for a FIFO queue.
    let mut queue: VecDeque<String> = items.into_iter().collect();
    while let Some(item) = queue.pop_front() {
        println!("processing: {item}");
    }
}

fn sliding_window_max(values: &[i32], k: usize) -> Vec<i32> {
    // VecDeque also shines as a fixed-size sliding window.
    let mut window: VecDeque<i32> = VecDeque::with_capacity(k);
    let mut result = Vec::with_capacity(values.len().saturating_sub(k) + 1);

    for &v in values {
        window.push_back(v);
        if window.len() > k {
            window.pop_front();
        }
        if window.len() == k {
            result.push(*window.iter().max().unwrap());
        }
    }
    result
}

fn main() {
    process_queue(["alpha".to_string(), "beta".to_string(), "gamma".to_string()]);

    let maxima = sliding_window_max(&[3, 1, 2, 5, 4], 3);
    println!("{maxima:?}"); // [3, 5, 5]
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
- coll-map-choice
- mem-with-capacity
- perf-drain-reuse
