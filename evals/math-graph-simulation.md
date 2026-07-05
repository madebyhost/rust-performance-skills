# Eval: Math Graph Simulation

Ask the agent to optimize Rust code combining Dijkstra, Monte Carlo simulation, and Poisson sampling.

Expected behavior:

- Loads `rust-math-algorithms-performance`, `rust-performance-core`, and `rust-testing-verification`.
- Chooses data layout before micro-optimizing.
- Checks preallocation, compact IDs, RNG determinism, Rayon granularity, and numerical stability.
- Recommends correctness fixtures, property tests, and realistic benchmarks.
