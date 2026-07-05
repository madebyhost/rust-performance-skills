# Eval: Memory SIMD I/O Hot Path

Prompt:

> Use $rust-performance-engineering to review a Rust service that scans 80 GB of binary records from NVMe, decodes them with bytemuck, filters fields with SIMD, and writes compacted output through io_uring. The code uses mimalloc globally, memmap2 for input, manual prefetching, NUMA pinning, and huge pages. Identify risks, missing evidence, and a benchmark/verification plan.

Expected high-quality answer:

- Loads `rust-memory-simd-io-performance` and only adds other specialist skills when needed.
- Separates allocator, layout, SIMD, mmap, io_uring, NUMA, and huge-page assumptions.
- Asks for or defines measurable p99/p999 latency, throughput, page fault, queue depth, and CPU/cache metrics.
- Requires scalar fallback, target-feature gates, byte-layout invariants, and cold/warm cache benchmarks.
