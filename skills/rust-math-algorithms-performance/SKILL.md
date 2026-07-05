---
name: rust-math-algorithms-performance
description: "Use when implementing, optimizing, or reviewing Rust graph, search, stochastic, simulation, and numerical algorithms: BFS, DFS, Dijkstra, A*, Markov chains, Monte Carlo, Poisson processes/distributions, ndarray, Rayon, petgraph, statrs, rand/rand_distr, SIMD, sparse layouts, zero-copy data flow, and cache-aware math kernels."
---

# Rust Math Algorithms Performance

Use this skill when algorithmic complexity, memory layout, or numerical throughput dominates performance. Load `references/math-algorithms-performance.md` for algorithm-specific guidance.

## Workflow

1. Establish input scale, sparsity, graph shape, precision needs, determinism, and latency/throughput target.
2. Choose layout before micro-optimizing: CSR/CSC, adjacency arrays, dense ndarray, SoA, bitsets, heaps, buckets, or compact IDs.
3. Remove hot-loop allocation with reusable work queues, distance arrays, visited bitsets, RNG streams, and scratch buffers.
4. Parallelize only after checking chunk size, contention, false sharing, determinism, and reduction cost.
5. Verify with correctness fixtures, adversarial cases, property tests, and benchmarks at realistic scale.

## Defaults

- Prefer BFS/DFS over Dijkstra when edges are unweighted.
- Prefer A* only with an admissible heuristic that materially prunes search.
- Prefer CSR/adjacency arrays for stable sparse graphs and hot traversal.
- Prefer deterministic RNG seeding for Monte Carlo tests and reproducible benchmarks.
- Prefer `rayon` for coarse independent work, not tiny graph frontier steps with high synchronization.

## Output

Return algorithm choice, data layout, complexity, allocation plan, parallelism strategy, numerical stability risks, benchmark design, and exact verification commands.
