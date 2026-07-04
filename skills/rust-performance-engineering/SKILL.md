---
name: rust-performance-engineering
description: Use when designing, implementing, optimizing, or reviewing Rust systems where performance, latency, throughput, allocation pressure, zero-copy, async, concurrency, cache behavior, or HFT-style low-latency engineering matters. Applies to Rust services, libraries, trading systems, market-data pipelines, networking, parsers, storage, telemetry, and any code path with explicit or implied performance constraints.
---

# Rust Performance Engineering

Use this skill to make Rust agents behave like performance engineers, not generic code generators.

## Workflow

1. Establish the performance contract.
   - Ask or infer p50/p95/p99 latency targets, throughput, memory ceiling, jitter tolerance, and correctness constraints.
   - Identify whether the path is hot, warm, cold, startup-only, or operational tooling.
2. Inspect the actual code and runtime surface.
   - Check `Cargo.toml`, feature flags, build profile, async runtime, data structures, queues, serialization, network and disk I/O, allocation points, locks, and clones.
3. Measure or preserve measurability.
   - Prefer `criterion`, `iai-callgrind`, `cargo flamegraph`, `perf`, `heaptrack`, `dhat`, `tokio-console`, tracing, and targeted counters where available.
   - If benchmarks do not exist, add a minimal benchmark or explain what evidence is missing before changing hot-path design.
4. Choose the smallest performance intervention that matches the bottleneck.
   - Do not add lock-free, `unsafe`, SIMD, arena allocation, CPU pinning, or disruptor-style architecture unless the constraint justifies it.
5. Validate behavior and performance assumptions.
   - Run tests, benchmarks, or static checks that match the change. If true performance validation is not possible locally, state the missing measurement clearly.

## Reference Routing

Load only the files needed for the task:

- `references/measurement.md`: benchmarking, profiling, Cargo profiles, and evidence standards.
- `references/zero-copy.md`: slices, borrowing, `Bytes`, mmap, serialization, parsing, and lifetime tradeoffs.
- `references/async-concurrency.md`: Tokio, rayon, bounded queues, backpressure, locks, scheduling, and multi-threading.
- `references/low-latency-hft.md`: HFT-style hot paths, UDP multicast, ring buffers, disruptor pattern, CPU affinity, cache lines, padding, NUMA, and kernel/network tuning.
- `references/data-layout-memory.md`: arrays vs vectors, SoA/AoS, cache locality, allocation control, false sharing, and layout.
- `references/architecture.md`: onion, hexagonal, domain-driven, ECS, actor, pipeline, and low-latency boundary choices.
- `references/review-checklists.md`: review questions for PRs, unsafe code, async code, and latency-critical code.

## Default Rust Performance Stance

- Prefer clear safe Rust first, then optimize the measured bottleneck.
- Prefer bounded resources: queues, buffers, tasks, connection pools, memory pools.
- Prefer explicit ownership and borrowing to hidden clones.
- Prefer stable hot-path data layout to abstraction-heavy object graphs.
- Prefer `Arc` for shared immutable state, not for avoiding ownership design.
- Prefer `parking_lot` only when lock profiles justify it.
- Prefer `SmallVec`, `ArrayVec`, arenas, or pools only when size bounds and reuse are clear.
- Prefer `Bytes`/borrowed views for network payloads when lifetimes and ownership boundaries are explicit.
- Prefer `tracing` with disabled-fast-path awareness over ad hoc logging in hot paths.
- Treat `async` as a concurrency model. It is not automatically lower latency than threads.

## Required Output For Design Or Review

When answering a performance-sensitive Rust request, include:

- the performance contract or the missing contract;
- the suspected bottleneck class: allocation, copy, lock/contention, cache locality, scheduler, syscalls, I/O, serialization, algorithmic complexity, or architecture;
- the recommended design;
- the tradeoffs and failure modes;
- how to verify the recommendation.

For HFT or ultra-low-latency work, also mention tail latency, jitter, warmup, kernel/network path, CPU isolation, clocking/timestamps, and recovery behavior.
