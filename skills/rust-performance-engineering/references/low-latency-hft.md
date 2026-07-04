# Low-Latency And HFT Patterns

Use these patterns only when latency, jitter, and throughput constraints justify the operational complexity.

## Hot Path Rules

- No heap allocation after warmup unless measured and accepted.
- No logging, formatting, DNS, config lookup, or dynamic dispatch in the innermost loop unless measured.
- Bound every queue and buffer.
- Preallocate message storage, order state, and scratch buffers.
- Treat p99 and p99.9 as first-class outputs.
- Keep recovery, replay, and kill-switch behavior explicit.

## Market Data And Networking

- UDP multicast is common for market data fanout. Design for loss detection, sequence gaps, snapshot recovery, and replay.
- Prefer kernel-bypass only when the team can operate it. Start with socket tuning and measurement.
- Batch syscalls where the protocol allows it.
- Pin feed handlers and strategy loops only after measuring scheduler jitter.
- Track timestamp source and clock synchronization assumptions.

## Ring Buffers And Disruptor Pattern

Use ring buffers when the workload benefits from fixed-capacity, cache-friendly, predictable memory reuse.

- SPSC rings are simpler and faster than general MPMC structures.
- MPSC/MPMC rings require careful contention and memory ordering design.
- Disruptor-style sequencing can work for fanout pipelines with strict ordering and preallocated events.
- Document overwrite, drop, backpressure, and slow-consumer policy.

## CPU, Cache, Memory

- Use cache-line padding for contended counters and producer/consumer indexes.
- Avoid false sharing between hot atomics.
- Prefer structure-of-arrays when scans touch a subset of fields.
- Keep hot structs compact and aligned. Avoid dragging cold fields through L1.
- Consider NUMA locality when threads and memory allocation cross sockets.
- Isolate cores only if the deployment controls the host.

## Disk And Persistence

- Keep persistence off the trading decision hot path unless the business rule requires synchronous durability.
- Use append-only logs for auditability.
- Batch fsync when allowed by risk constraints.
- Separate recovery correctness from live latency code.

## Red Flags

- `println!` or structured logging inside market-data loops.
- dynamic allocation in order-book update paths;
- global lock around strategy state;
- generic async runtime used for a pinned nanosecond-level loop without evidence;
- lock-free queue selected before a bounded blocking queue was measured;
- CPU pinning added without deployment control.

## Verification

- Replay captured market data at target and burst rates.
- Report p50/p95/p99/p99.9, max, drops, sequence gaps, queue depth, and CPU utilization.
- Warm up before measuring.
- Test slow consumer behavior.
- Test packet loss, gap fill, and reconnect paths.
