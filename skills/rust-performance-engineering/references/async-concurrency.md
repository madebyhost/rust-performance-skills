# Async And Concurrency

Async Rust improves concurrency under I/O wait. It does not automatically improve CPU latency.

## Choose The Model

- Tokio async tasks: many I/O-bound connections, timers, network services.
- Dedicated OS threads: latency-critical loops, CPU pinning, blocking APIs, predictable scheduling.
- Rayon: CPU-bound parallel data processing.
- Actor model: isolated mutable state and message-passing boundaries.
- Pipeline stages: predictable flow with bounded queues and measurable backpressure.

## Tokio Guidance

- Keep CPU-heavy work off async worker threads. Use dedicated threads or `spawn_blocking` with explicit limits.
- Avoid unbounded channels in production hot paths.
- Track queue depth, task count, task poll duration, and wake frequency.
- Prefer `select!` paths with explicit shutdown and backpressure behavior.
- Be careful with `Mutex` across `.await`; use async-aware locks only when the critical section is not CPU-heavy.

## Multi-Threading

- Prefer ownership transfer over shared mutable state.
- Use `Arc<T>` for shared immutable data.
- Use `Arc<Mutex<T>>` only when contention is measured or bounded.
- Prefer sharding over a single global lock.
- Use atomics only when ordering semantics are understood and documented.

## Queue Choices

- `tokio::sync::mpsc`: async task communication.
- `crossbeam_channel`: thread communication with mature blocking semantics.
- `crossbeam_queue` or ring buffers: low-latency bounded paths.
- Custom SPSC/MPSC rings: only when benchmarks justify maintaining them.

## Red Flags

- unbounded channels in data-plane code;
- one task per tiny CPU operation;
- blocking file/network calls inside async tasks;
- locks held across await points;
- `SeqCst` atomics everywhere without reasoning;
- retries without jitter, timeout, or backpressure.

## Verification

- Run load tests with representative concurrency.
- Inspect queue depth and tail latency, not only throughput.
- Check for task leaks on shutdown.
- Benchmark with runtime worker counts that match deployment.
