# Eval: HFT Hot Path

Ask the agent to design or review a market-data hot path with UDP multicast, ring buffers, cache-sensitive structs, and p99/p999 targets.

Expected behavior:

- Loads `rust-low-latency-hft`, `rust-performance-core`, `rust-async-concurrency`, and `rust-testing-verification`.
- Separates correctness, packet loss, replay, backpressure, allocation, cache locality, CPU isolation, and kernel/network tuning.
- Avoids recommending unsafe or lock-free code without measured justification and verification.
- Requires tail-latency evidence, warmup, queue depth, drop counters, and benchmark commands.
