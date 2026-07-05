---
name: rust-memory-simd-io-performance
description: "Use when optimizing or reviewing Rust hot paths involving allocators, arenas, memory layout, SIMD, core::arch, std::simd, mmap, memmap2, io_uring, direct I/O, page faults, huge pages, NUMA, cache lines, prefetching, bytemuck, zerocopy, or zero-copy buffer ownership."
---

# Rust Memory SIMD I/O Performance

Use this skill when the bottleneck is likely memory movement, allocation lifetime, CPU vectorization, or kernel/storage I/O. Load `references/memory-simd-io-performance.md` for detailed checklists.

## Workflow

1. Establish the workload shape: item size, batch size, lifetime, alignment, locality, I/O size, queue depth, latency target, and tail tolerance.
2. Measure the current path: allocations, copies, cache misses, page faults, syscalls, I/O wait, queue depth, and scalar vs vector throughput.
3. Choose the smallest intervention: preallocation, arena, layout change, safe zero-copy cast, SIMD specialization, mmap, direct I/O, or io_uring.
4. Keep fallbacks explicit: scalar path for SIMD, normal read/write path for mmap or io_uring, and system allocator path for allocator experiments.
5. Verify with correctness tests, feature-gated builds, and benchmarks that include cold start, warm path, p99/p999 latency, and production-like sizes.

## Defaults

- Prefer better layout and fewer copies before custom allocators or SIMD.
- Prefer measured allocator swaps over global allocator cargo-culting.
- Prefer `core::arch` only behind target-feature gates and safe wrappers.
- Treat `std::simd` as nightly-only until the target toolchain proves otherwise.
- Treat `mmap`, huge pages, NUMA, and direct I/O as operational choices with portability and failure-mode costs.
- Use `bytemuck` or `zerocopy` only when representation, alignment, padding, and lifetime invariants are documented.

## Output

Return bottleneck class, memory/layout plan, SIMD or scalar strategy, I/O strategy, OS assumptions, fallback path, benchmark design, and exact verification commands.
