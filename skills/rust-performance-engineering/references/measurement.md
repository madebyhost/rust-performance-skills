# Measurement And Evidence

Use measurement to prevent speculative optimization.

## First Questions

- What is the latency target: p50, p95, p99, p99.9?
- What is the throughput target and expected concurrency?
- Is the goal lower mean latency, lower tail latency, lower jitter, lower CPU, lower memory, or higher throughput?
- Is the workload CPU-bound, I/O-bound, allocation-bound, lock-bound, scheduler-bound, or cache-bound?
- What changed recently: input size, feature flag, dependency, runtime config, kernel, hardware, deployment topology?

## Rust Tooling

- Microbenchmarks: `criterion`.
- Instruction/cache profiling: `perf`, `cargo flamegraph`, `iai-callgrind`.
- Allocation profiling: `heaptrack`, `valgrind massif`, `dhat`.
- Async/runtime behavior: `tokio-console`, task counts, queue depth, poll duration histograms.
- Binary inspection: `cargo asm`, `cargo llvm-lines`, `objdump`.
- Lints: `cargo clippy --all-targets --all-features`, especially clone, allocation, and lock hints.

## Cargo Profile Baseline

For production performance, inspect:

```toml
[profile.release]
opt-level = 3
lto = "thin"
codegen-units = 1
panic = "abort"
debug = "line-tables-only"
```

These are not universal defaults. For very large services, `codegen-units = 1` and LTO can slow builds materially. For profiling, keep enough debug info to map samples.

## Evidence Standard

Strong evidence:

- benchmark before and after on representative input;
- profiler sample showing the changed bottleneck;
- allocation count or byte delta;
- tail latency histogram under load;
- flamegraph or lock contention trace.

Weak evidence:

- code "looks faster";
- single local wall-clock run;
- optimizing a cold path;
- replacing safe code with `unsafe` without measured gain;
- adding concurrency without queue/backpressure metrics.

## Agent Rule

When a user asks for performance changes and no benchmark exists, either add the smallest relevant benchmark or state that the recommendation is a design hypothesis awaiting measurement.
