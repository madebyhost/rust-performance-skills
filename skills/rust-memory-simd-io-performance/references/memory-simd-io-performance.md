# Memory SIMD I/O Performance Reference

## Memory And Allocation

- Start with allocation profiles and lifetimes. A faster allocator does not fix poor ownership or per-item heap churn.
- Use `Vec::with_capacity`, reusable scratch buffers, slabs, pools, or arenas when object lifetimes are naturally grouped.
- Use `bumpalo` for phase-scoped allocation only when skipped `Drop` behavior is safe or manually handled.
- Compare `mimalloc`, `tikv-jemallocator`, and the system allocator with the same workload, thread count, and lifetime pattern.
- Keep global allocator changes feature-gated or target-specific when portability matters.

## Layout And Zero Copy

- Choose SoA for scanning a few fields across many records; choose AoS when complete records are consumed together.
- Check cache-line ownership before adding padding. Padding can reduce false sharing while increasing bandwidth pressure.
- Use `bytemuck` or `zerocopy` for byte reinterpretation only when layout, padding, endian, alignment, and lifetime invariants are explicit.
- Prefer borrowed views or typed slices over copying into owned structs in decode-heavy paths.

## SIMD

- First make scalar code benchmarkable and layout-friendly.
- Use compiler autovectorization when simple loops and contiguous slices are enough.
- Use `core::arch` behind `#[target_feature]`, runtime detection, and a safe wrapper with scalar fallback.
- Treat `std::simd` as nightly-only unless the project's toolchain policy explicitly accepts it.
- Validate tail handling, alignment assumptions, NaN/overflow behavior, and target-specific code paths.

## I/O And Kernel Boundary

- Use `memmap2` for read-mostly random access or large file views only after modeling page faults and file lifetime.
- Use `io-uring` when batching, registered buffers/files, or reduced syscall overhead are measurable for the workload.
- Direct I/O can reduce page-cache interference but adds alignment and buffering constraints.
- HugeTLB, transparent huge pages, CPU pinning, and NUMA placement belong in deployment docs and benchmark setup, not hidden library defaults.
- Track queue depth, completions, short reads/writes, retries, p99/p999 latency, page faults, and CPU utilization.

## Verification

- Correctness tests for scalar and SIMD paths with the same fixtures.
- Benchmarks for cold and warm cache behavior, realistic batch sizes, and representative file/device characteristics.
- Sanitizers or Miri for unsafe wrappers where supported.
- Platform-gated CI for Linux-only `io_uring` and OS-specific mmap behavior.

## Red Flags

- Replacing the allocator without measuring allocation sites.
- Adding SIMD before fixing data layout or bounds checks.
- Using `transmute` where `bytemuck`/`zerocopy` invariants would reject the layout.
- Benchmarking `mmap` only on hot page cache.
- Enabling NUMA or huge pages without proving page placement and fault behavior.
