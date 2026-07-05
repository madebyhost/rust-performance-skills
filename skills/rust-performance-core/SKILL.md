---
name: rust-performance-core
description: "Use for core Rust performance optimization: profiling, benchmarking, Cargo profiles, allocations, copies, cache behavior, type sizes, bounds checks, inlining, hashing, iterators, I/O, logging overhead, and data layout."
---

# Rust Performance Core

Use this skill for measured Rust optimization. Load `references/performance-core.md` for detailed tactics. Load `rust-memory-simd-io-performance` when allocator choice, SIMD, mmap, io_uring, huge pages, NUMA, or zero-copy byte layout dominates the change. Load `rust-expert-rulebook` when choosing or reviewing a concrete optimization rule.

## Workflow

1. Establish the metric: latency, throughput, CPU, memory, code size, or compile time.
2. Identify evidence: benchmark, flamegraph, allocation profile, cache profile, tracing, or production telemetry.
3. Classify bottleneck: algorithm, data structure, allocation, copy, cache, lock, I/O, logging, serialization, compiler profile.
4. Apply the smallest measured change.
5. Re-run the same measurement and report before/after.

## Defaults

- Prefer algorithm/data-layout changes before micro-optimizations.
- Prefer iteration and slices to repeated indexed bounds checks in hot loops.
- Prefer preallocation and buffer reuse when sizes are known.
- Tune `profile.release` only with build-time and debugging tradeoffs documented.

## Output

Report bottleneck class, recommendation, applicable rule IDs, complexity cost, verification command, and expected measurement.
