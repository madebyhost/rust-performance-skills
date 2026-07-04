# Async And Concurrency Reference

## Primitive Choices

- `tokio::spawn`: I/O-bound tasks that are `Send`.
- `spawn_blocking`: bounded blocking work; not a general CPU pool.
- Rayon: CPU-bound data parallelism.
- Dedicated thread: latency-critical loop, CPU pinning, blocking API.
- `tokio::sync::mpsc`: async actor or pipeline communication.
- `crossbeam_channel`: thread communication.
- Atomics: simple shared state with documented ordering.

## Backpressure

Unbounded queues hide overload and turn latency into memory growth. Define the policy: block, drop newest, drop oldest, shed load, or degrade quality.

## Common Failures

- `Arc<Mutex<T>>` everywhere;
- `std::thread::sleep` in async code;
- holding a lock across `.await`;
- blocking file or network calls inside async workers;
- `SeqCst` by default without ordering reasoning;
- creating tasks faster than they complete.

## Verification

- Load test with production-like concurrency.
- Capture p95/p99 latency and queue depth.
- Check shutdown and cancellation.
- Run under the same Tokio worker count as deployment.
