---
name: rust-performance-engineering
description: "Primary router for Rust performance and quality work. Use when designing, implementing, optimizing, auditing, or reviewing Rust systems, Rust-backed Python extensions, WebAssembly modules, FFI/bindings, low-latency/HFT systems, async services, libraries, crates, or any code path with explicit or implied quality, safety, latency, throughput, memory, zero-copy, concurrency, cache, or packaging constraints."
---

# Rust Performance Engineering

Use this as the router. Load the smallest specialist skill set that matches the task, then answer with explicit constraints, tradeoffs, and verification.

## Operating Workflow

1. Establish the performance contract.
   - Ask or infer p50/p95/p99 latency targets, throughput, memory ceiling, jitter tolerance, and correctness constraints.
   - Identify whether the code path is hot, warm, cold, startup-only, packaging, or operational tooling.
2. Inspect the actual code and runtime surface.
   - Check `Cargo.toml`, feature flags, build profile, lints, async runtime, data structures, queues, serialization, network and disk I/O, bindings, allocation points, locks, clones, and `unsafe`.
3. Measure or preserve measurability.
   - Prefer `criterion`, `iai-callgrind`, `cargo flamegraph`, `perf`, `heaptrack`, `dhat`, `tokio-console`, tracing, and targeted counters where available.
   - If benchmarks do not exist, add a minimal benchmark or state which evidence is missing.
4. Choose the smallest performance intervention that matches the bottleneck.
   - Do not add lock-free, `unsafe`, SIMD, arena allocation, CPU pinning, Wasm rewrites, PyO3 bindings, or disruptor-style architecture unless the constraint justifies it.
5. Validate behavior and performance assumptions.
   - Run tests, benchmarks, or static checks that match the change. If true performance validation is not possible, state the missing measurement clearly.

## Specialist Skill Routing

Load these specialist skills as needed:

- `rust-code-quality`: idiomatic Rust, API design, crate hygiene, docs, clippy, tests, maintainability.
- `rust-performance-core`: profiling, Cargo profiles, allocations, cache, bounds checks, inlining, data layout.
- `rust-async-concurrency`: Tokio, Rayon, channels, backpressure, scheduling, locks, atomics, Send/Sync.
- `rust-low-latency-hft`: market data, ring buffers, UDP multicast, disruptor, CPU/cache/NUMA/kernel tuning.
- `rust-python-pyo3-maturin`: accelerate Python with Rust, PyO3, maturin, GIL/free-threading, wheels, stubs.
- `rust-wasm-engineering`: wasm-bindgen, JS boundary cost, code size, memory transfer, browser/node packaging.
- `rust-ffi-bindings`: C/C++/Node/Python interop, bindgen/cbindgen/napi-rs, ABI and ownership boundaries.
- `rust-unsafe-soundness`: unsafe review, invariants, Miri/sanitizers, safe wrapper design.
- `rust-architecture-patterns`: onion, hexagonal, DDD, ECS, actor, pipeline, disruptor, hot-path exceptions.
- `rust-review-auditor`: PR/repository audit workflow for Rust quality, safety, and performance.

Load these local references when the task is broad or does not map cleanly to one specialist:

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
- Treat bindings as boundary design. Avoid crossing Python/JS/FFI boundaries per item in a hot loop.

## Required Output

For Rust design, implementation, optimization, or review, include:

- the performance contract or the missing contract;
- the suspected bottleneck class: allocation, copy, lock/contention, cache locality, scheduler, syscalls, I/O, serialization, algorithmic complexity, or architecture;
- the recommended design;
- the tradeoffs and failure modes;
- how to verify the recommendation.

For PyO3/maturin or Wasm work, also mention boundary crossing cost, packaging target, release/profile settings, and benchmark strategy.

For HFT or ultra-low-latency work, also mention tail latency, jitter, warmup, kernel/network path, CPU isolation, clocking/timestamps, packet loss, and recovery behavior.
