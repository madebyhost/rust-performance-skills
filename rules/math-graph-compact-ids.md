# math-graph-compact-ids

## id
math-graph-compact-ids

## severity
high

## trigger
BFS, DFS, Dijkstra, A*, Markov chains, Monte Carlo, or graph/numerical kernels with many node lookups.

## bad
```rust
let mut distance: HashMap<NodeId, f64> = HashMap::new();
for neighbor in graph.neighbors(node) {
    distance.insert(neighbor.clone(), next);
}
```

## good
```rust
let mut distance = vec![f64::INFINITY; graph.node_count()];
for neighbor in graph.neighbors_idx(node_idx) {
    distance[neighbor] = next;
}
```

## when
Use when node IDs can be compacted and the algorithm is memory-bandwidth or cache-latency sensitive.

## when_not
Do not compact IDs if stable external identifiers dominate API clarity and the graph is small or sparse enough.

## verification
Measure asymptotic complexity, allocation count, cache misses, deterministic seeds, and adversarial graph cases.

## sources
- rust-performance-skills: https://github.com/madebyhost/rust-performance-skills
- petgraph: https://docs.rs/petgraph/
- Rayon: https://docs.rs/rayon/

## related_rules
- coll-hashmap-capacity
- mem-with-capacity
- num-float-compare
