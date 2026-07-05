# Math Algorithms Performance Reference

## Graph Algorithms

- BFS/DFS: use compact node IDs, adjacency arrays, preallocated queue/stack, and visited bitset.
- Dijkstra: use binary heap for general positive weights; consider buckets/radix heaps for bounded integer weights.
- A*: use only when the heuristic is admissible, cheap, and prunes enough nodes to offset overhead.
- Stable sparse graph: CSR/CSC is often faster than pointer-heavy structures for traversal.

## Stochastic And Simulation

- Monte Carlo: separate RNG stream setup from hot sampling, batch work, and use deterministic seeds in tests.
- Markov chains: store transition matrices in dense or sparse layout matching access pattern.
- Poisson workflows: distinguish distribution sampling, process simulation, and rate estimation.
- Avoid hidden allocation in distribution construction inside inner loops.

## Rust Tool Choices

- `petgraph`: useful for correctness and general graph APIs; inspect layout before hot-path use.
- `ndarray`: useful for dense numeric arrays and views; check strides, ownership, and bounds.
- `rayon`: useful for coarse independent parallelism and reductions.
- `statrs`, `rand`, `rand_distr`: useful for distributions; keep construction outside hot loops.
- SIMD: use after scalar algorithm/layout is correct and benchmarked.

## Verification

- Correctness fixtures for small known graphs and distributions.
- Property tests for invariants such as path optimality and probability bounds.
- Benchmarks at realistic graph sizes, sparsity, and distribution parameters.
- Numerical tests for overflow, underflow, cancellation, convergence, and reproducibility.

## Red Flags

- HashMap-heavy graph traversal in a hot loop when compact IDs are possible.
- Allocating visited/distance vectors per query.
- Parallelizing tiny tasks or shared mutable frontier state.
- Benchmarking random toy graphs that do not match production topology.
