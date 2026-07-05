---
name: rust-low-latency-hft
description: "Use for ultra-low-latency Rust and HFT-style systems: market data, order routing, UDP multicast, ring buffers, disruptor pattern, lock-free structures, CPU affinity, cache lines, padding, NUMA, kernel/network tuning, p99/p999 latency, jitter, packet loss, replay, and recovery."
---

# Rust Low-Latency HFT

Use this skill when tail latency and jitter dominate design. Load `references/low-latency-hft.md` for detailed checks.

## Workflow

1. Define p50/p99/p999, max latency, throughput bursts, packet loss, replay, and recovery targets.
2. Identify the hot loop and remove cold-path concerns from it.
3. Bound allocation, queues, logging, syscalls, and locks after warmup.
4. Choose SPSC ring, MPSC queue, actor, pipeline, or disruptor based on fanout and ordering.
5. Load `rust-sbe-binary-codecs` for binary market-data codecs and `rust-ebpf-kernel-performance` for XDP, AF_XDP, tc, or probe-based kernel paths.
6. Verify with replayed production-like market data and tail latency histograms.

## Output

Always include slow-consumer policy, backpressure/drop policy, warmup assumptions, timestamping, and operational recovery.
