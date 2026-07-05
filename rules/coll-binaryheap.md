# coll-binaryheap

## id
coll-binaryheap

## severity
medium

## trigger
Use `BinaryHeap` for a priority queue or repeated max-extraction. Trigger when working on collections and the code shows `coll`-class risk.

## bad
```rust
fn top_priority_task(tasks: &mut Vec<(u32, String)>) -> Option<String> {
    if tasks.is_empty() {
        return None;
    }
    // O(n) scan to find the max, then O(n) shift to remove it - O(n) per call.
    let max_idx = tasks
        .iter()
        .enumerate()
        .max_by_key(|(_, (p, _))| *p)
        .map(|(i, _)| i)?;
    Some(tasks.remove(max_idx).1)
}

fn main() {
    let mut tasks = vec![
        (3, "low priority".to_string()),
        (10, "urgent".to_string()),
        (7, "medium priority".to_string()),
    ];
    // Repeated calls become O(n) overall.
    while let Some(task) = top_priority_task(&mut tasks) {
        println!("running: {task}");
    }
}
```

## good
```rust
use std::cmp::Reverse;
use std::collections::BinaryHeap;

#[derive(Eq, PartialEq, Ord, PartialOrd)]
struct Task {
    priority: u32, // higher = more urgent
    name: String,
}

fn run_scheduler(tasks: impl IntoIterator<Item = (u32, &'static str)>) {
    // BinaryHeap: O(log n) push and pop - max-priority task extracted first.
    let mut heap: BinaryHeap<Task> = tasks
        .into_iter()
        .map(|(priority, name)| Task {
            priority,
            name: name.to_string(),
        })
        .collect();

    while let Some(task) = heap.pop() {
        println!("running [priority={}]: {}", task.priority, task.name);
    }
}

fn top_k_largest(values: &[i32], k: usize) -> Vec<i32> {
    // Min-heap of size k using Reverse<i32>: keeps the k largest elements.
    let mut min_heap: BinaryHeap<Reverse<i32>> = BinaryHeap::with_capacity(k + 1);
    for &v in values {
        min_heap.push(Reverse(v));
        if min_heap.len() > k {
            min_heap.pop(); // discard the current minimum
        }
    }
    // Drain from min to max for a sorted result.
    let mut result: Vec<i32> = min_heap.into_iter().map(|Reverse(v)| v).collect();
    result.sort_unstable_by(|a, b| b.cmp(a));
    result
}

fn main() {
    run_scheduler([
        (3, "low priority task"),
        (10, "urgent task"),
        (7, "medium priority task"),
        (10, "equally urgent task"),
    ]);
    // Output order: urgent, equally urgent, medium, low

    let top3 = top_k_largest(&[4, 1, 9, 2, 7, 5, 8], 3);
    println!("top 3: {top3:?}"); // [9, 8, 7]
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
- coll-seq-choice
- perf-iter-over-index
