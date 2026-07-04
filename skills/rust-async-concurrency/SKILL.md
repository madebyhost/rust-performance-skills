---
name: rust-async-concurrency
description: "Use for Rust async and concurrency design: Tokio, Rayon, threads, tasks, channels, backpressure, locks, atomics, Send/Sync errors, contention, scheduler behavior, CPU-bound vs I/O-bound work, and parallelism."
---

# Rust Async Concurrency

Use this skill to choose the concurrency model before adding primitives. Load `references/async-concurrency.md` for details.

## Decision Flow

1. CPU-bound: prefer Rayon or dedicated threads.
2. I/O-bound: prefer async runtime with bounded work and observability.
3. Mixed: isolate CPU-heavy work from async workers.
4. Shared state: prefer ownership transfer, immutable sharing, sharding, or message passing before global locks.

## Review Checks

- Are channels bounded?
- Are locks held across `.await`?
- Is blocking work on async worker threads?
- Are queue depth, task count, poll duration, and tail latency observable?
- Are Send/Sync bounds solving a real thread-boundary requirement?

## Output

Name the workload type, sharing model, recommended primitive, failure modes, and verification method.
